# Hardened deployment: agents cannot touch governance files

The framework enforces the chain for every write that goes through it
(ADR-0010), verifies who an agent is (ADR-0011), and detects edits to its
files (ADR-0012). One thing it cannot do from code is **stop a process from
writing a file its OS user can write.** If your agents run as the same user
as the framework, they can edit `runs/` and read `config/integrity.key`.

This page sets up the separation that turns detection into prevention:

- The framework runs as its own OS user.
- Agents reach it only over MCP HTTP.
- Agents never get a shell as that user.

Run `python3 scripts/ticket.py doctor` before and after. It reports what is
and is not enforced.

**Why `config/` matters most.** It holds the integrity key, the agent
registry, and the signed head records. An agent that can write `runs/` but
not `config/` gets caught by tamper detection, including attempts to roll
`runs/` back to an earlier state. An agent that can write `config/` can do
anything.

## What each level gets you

| Setup | An agent can... | Governance is |
|---|---|---|
| Default (same user, no registry, no key) | Act under any id. Edit tickets; the edit is detected. Forge hashes. | Enforced for honest callers. Edits are detected, but not forgery. |
| Registry + key, same user | Read other agents' tokens and the key if it can read their env or files | Strong against mistakes. Weak against an agent trying to cheat. |
| **Registry + key + separate user (this page)** | Only call MCP tools with its own token | Enforced. Edits need the framework user's permissions. |

## macOS: one command (1.2.1+)

On macOS the whole setup is scripted and tested end to end in CI on a real
Mac (`scripts/macos/e2e-test.sh`, ADR-0013).

```bash
git clone https://github.com/paulthorson/agentic-governance.git ~/dev/agentic-governance
cd ~/dev/agentic-governance
sudo scripts/macos/harden.sh --python /opt/homebrew/bin/python3.12
```

It creates a hidden service user `_aggov` and installs to
`/Library/AgenticGovernance`:

| Path | Owner | Mode | Holds |
|---|---|---|---|
| code, `.venv/` | root | read-only for everyone | the framework |
| `runs/` | `_aggov` | 700 | tickets, event log, approvals |
| `config/` | `_aggov` | 700 | integrity key, agent registry, head record, bearer token |

Two launchd daemons run as `_aggov`: the MCP server on
`http://127.0.0.1:8765/mcp` (bearer token required) and recovery every
10 minutes. The installer keys the event log on first run.

Operator commands go through `agctl`, which needs `sudo`. sudo is the
operator gate: an agent that cannot sudo cannot register agents, clear
vetoes, or accept tampering, even with a shell.

```bash
sudo /Library/AgenticGovernance/scripts/macos/agctl agent add <id> --team <team> --roles <stage|review:stage> --principal <runtime>
sudo /Library/AgenticGovernance/scripts/macos/agctl doctor
sudo cat /Library/AgenticGovernance/config/mcp_auth_token   # the bearer token agents send
```

Agents connect over HTTP with `Authorization: Bearer <token>` and pass their
own `agent_token` on every `ticket_*` call. Keep each agent's token only in
that agent's own config.

What the CI test proves on a real Mac, from an ordinary account with a shell:
it cannot list or read `runs/`, read the key, registry, or bearer token,
create an approval, or modify the code; it can work tickets only through
MCP with its token; a same-principal reviewer gets nothing; tampering stops
writes until the operator accepts; launchd restarts a killed server; and
`--uninstall --purge` removes everything.

To remove: `sudo /Library/AgenticGovernance/scripts/macos/harden.sh --uninstall`
(keeps data) or add `--purge` (deletes tickets, log, key, registry, and the
service user; cannot be undone).

Python: 3.11+ from outside your home folder (Homebrew's is fine). The
`python3` that ships with macOS is 3.9 and will not work.

## Steps (Linux)

### 1. Create a framework user and give it the checkout

```bash
sudo useradd --system --create-home --shell /usr/sbin/nologin aggov
sudo chown -R aggov:aggov /srv/agentic-governance
sudo chmod 700 /srv/agentic-governance/runs /srv/agentic-governance/config
```

Agents' OS users must not be in the `aggov` group and must not have sudo.

### 2. Key the log and register agents (as the framework user)

```bash
cd /srv/agentic-governance
sudo -u aggov touch runs/approval.ok
sudo -u aggov python3 scripts/ticket.py integrity init-key
sudo -u aggov touch runs/approval.ok
sudo -u aggov python3 scripts/ticket.py agent add eng-1 --team team-a \
  --roles engineer --principal runtime-claude-a
sudo -u aggov touch runs/approval.ok
sudo -u aggov python3 scripts/ticket.py agent add eng-critic --team team-a \
  --roles review:engineer --principal runtime-gpt-b
```

Each `agent add` prints a token once. Put each token only in that agent's
secret store.

Give the worker and its reviewer **different principals**, meaning different
runtimes, accounts, or vendors. If one runtime holds both tokens, register
both under the same principal. The framework then refuses that runtime's
self-review.

### 3. Run the MCP server over HTTP as the framework user

`/etc/systemd/system/agentic-governance.service`:

```ini
[Unit]
Description=Agentic Governance MCP server
After=network.target

[Service]
User=aggov
WorkingDirectory=/srv/agentic-governance/mcp
Environment=MCP_AUTH_TOKEN=<shared transport token>
# Never set AG_AGENT_TOKEN here: the HTTP server refuses to start with it.
ExecStart=/usr/local/bin/uv run adversarial-mcp --transport streamable-http --port 8000
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Each agent's MCP client config needs two things:

- `Authorization: Bearer <MCP_AUTH_TOKEN>` as a header.
- Its own `agent_token` as an argument on every `ticket_*` call.

The bearer token admits a client to the server. The agent token says which
agent it is.

### 4. Alerts and recovery on a schedule (as the framework user)

```cron
*/10 * * * * cd /srv/agentic-governance && python3 scripts/ticket.py recover --alert
```

Configure an alert channel and set network permission to `allow` in the
setup wizard. Outbound alerts also need operator approval
(`scripts/approval.py`). For the cron job, put `AG_APPROVAL_TOKEN` in the cron
environment, matching `runs/approval.token`. **Approval is not scoped per
action**, so that token also authorizes `clear-veto`, `resolve`, and
`done --override` for any process that holds it. Keep it in the cron
environment only. Without all three, alerts are printed and recorded but
not delivered.

### 5. Optional: append-only attribute on the log (Linux, root)

```bash
sudo chattr +a /srv/agentic-governance/runs/events.jsonl
```

With this set, even the framework user can only append, so earlier events
cannot be rewritten. Remove it (`chattr -a`) before you rotate or archive
the log.

## What is still not covered

- An agent that gets a shell as `aggov` (or root) can do anything.
- Human-only actions check for operator approval, not for who the human is.
  Anyone who can create `runs/approval.ok` as `aggov`, or who holds the
  approval token, can clear vetoes.
- `ticket_list` shows every team's tickets to any authenticated caller.
- Tokens do not expire. Rotate with `agent revoke` then `agent add`.

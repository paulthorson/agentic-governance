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

Install from a fresh clone of a release tag that root owns. The installer
runs as root, so a copy your agents could have edited (any folder your login
user can write, including your usual checkout) would let them run code as
root. The installer refuses a source tree that is not entirely root-owned
(override with `--trust-source` only on a throwaway machine such as CI).
Use `/usr/bin/git` by its full path, since a `git` found through your PATH
may be one your login user can replace, and `sudo -H`, since plain `sudo` on
macOS keeps your HOME and git would read your (agent-writable) `~/.gitconfig`
as root.

```bash
sudo -H /usr/bin/git -c core.hooksPath=/dev/null clone --depth 1 --branch v1.2.2 \
  https://github.com/paulthorson/agentic-governance.git /private/var/root/ag-src
sudo -H /private/var/root/ag-src/scripts/macos/harden.sh
sudo rm -rf /private/var/root/ag-src
```

It creates a hidden service user `_aggov` and installs to
`/Library/AgenticGovernance`:

| Path | Owner | Mode | Holds |
|---|---|---|---|
| code, `.venv/` | root | read-only for everyone | the framework |
| `python/` | root | read-only for everyone | its own Python (see below) |
| `runs/` | `_aggov` | 700 | tickets, event log |
| `config/` | `_aggov` | 700 | integrity key, agent registry, head record, bearer token |

Logs go to `/Library/Logs/AgenticGovernance-app.agenticgovernance/`.

Two launchd daemons run as `_aggov`: the MCP server on
`http://127.0.0.1:8765/mcp` (bearer token required) and recovery every
10 minutes. The installer keys the event log on first run.

Operator commands go through `agctl`, which needs `sudo`. sudo is the
operator gate: an agent that cannot sudo cannot register agents, clear
vetoes, or accept tampering, even with a shell. agctl passes approval only
to the one command it runs, never as a file, so the MCP server never holds
an approval. It refuses to run (exit 4) if any installed file has become
writable by someone other than root.

```bash
sudo /Library/AgenticGovernance/scripts/macos/agctl agent add <id> --team <team> --roles <stage|review:stage> --principal <runtime>
sudo /Library/AgenticGovernance/scripts/macos/agctl doctor
sudo cat /Library/AgenticGovernance/config/mcp_auth_token   # the bearer token agents send
```

Agents connect over HTTP with `Authorization: Bearer <token>` and pass their
own `agent_token` on every `ticket_*` call. Keep each agent's token only in
that agent's own config.

**Check which OS user each agent runs as.** Start your agents, then run
`sudo .../agctl doctor`. For every live connection to the MCP server it
prints the OS user on the other end: `[PASS] agent user <name>` for an
ordinary account, `[FAIL]` for root, an admin, the service user, or the
login you ran sudo from. Any FAIL exits 4, and so does a check that could
not run. An agent that is not connected when doctor runs does not show up:
`no live MCP connections` means nothing was checked, so run doctor while the
agents are up. "Admin" means a member of the `admin` group; sudo rights
granted another way are not detected. On Linux, run
`ticket.py doctor --mcp-port <port>` as the framework user.

What the CI test proves on a real Mac, from an ordinary account with a shell:
it cannot list or read `runs/`, read the key, registry, or bearer token,
create an approval, or modify the code, the interpreter, or the venv; it can
work tickets only through MCP with its token; a same-principal reviewer gets
nothing; a reviewer never sees the worker's summary; `overturn_verdict` is
refused over MCP; tampering stops writes until the operator accepts;
launchd restarts a killed server; a reinstall keeps `config/` at 700; and
`--uninstall --purge` removes everything. It also checks that the installer
refuses a source tree the agent owns, a relative or top-level prefix, a
non-empty folder it did not create, a folder the agent created, and a real
account as the service user, and that `--purge` never deletes a system
group.

To remove: `sudo /Library/AgenticGovernance/scripts/macos/harden.sh --uninstall`
(keeps data) or add `--purge` (deletes tickets, log, key, registry, and the
service user; cannot be undone).

Python: the installer downloads a pinned CPython 3.12 build
(python-build-standalone, checked against a SHA-256 in the script) into
`python/` and owns it as root. It does not use Homebrew's Python: on Apple
Silicon `/opt/homebrew` belongs to your login user, so every agent running
as you could edit that interpreter's standard library and run code as
`_aggov`, or as root on the next reinstall. For an offline install, pass the
same archive with `--python-archive FILE`; the hash still has to match.
`pip` installs `mcp` and `pydantic` from PyPI without hash pinning.

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

# OpenClaw Gateway: Curated Local-First MCP Servers

Story THO-146 (epic THO-22 — MCP Integration Layer).
Status: **implemented** · Approver review pending.

## Scope

Wire a curated set of **local-first, low-risk** MCP servers into the OpenClaw
gateway (`~/.openclaw/openclaw.json` → `mcp.servers`), gate untrusted servers
behind approval, and document the integration.

**Non-goals (explicitly excluded):** no cloud MCP gateways, no servers that
exfiltrate data, no remote/third-party data sinks.

## Configured servers (as of 2026-09-17)

| Name       | Transport | Command (stdio)                                   | Approval |
|------------|-----------|---------------------------------------------------|----------|
| `mempalace`| stdio     | `~/.local/bin/mempalace-mcp`                | —        |
| `filesystem`| stdio    | `npx -y @modelcontextprotocol/server-filesystem <dirs>` | —   |
| `browser`  | stdio     | `npx -y @playwright/mcp@latest`                   | —        |
| `git`      | stdio     | `npx -y @cyanheads/git-mcp-server`                | `prompt` |
| `postgres` | stdio     | `npx -y @microsoft/postgres-mcp run --no-telemetry --profile local` | `prompt` |

### Verified health (2026-09-17)

`openclaw mcp doctor --probe`:

```
- browser:   ok
- filesystem: ok
- git:       ok
- postgres:  ok
```

Gateway hot reload confirmed in `~/Library/Logs/openclaw/gateway.log`:

```
[reload] config hot reload applied (mcp.servers.git)
[reload] config hot reload applied (mcp.servers.postgres)
```

## Why these packages

- **filesystem** — official reference `@modelcontextprotocol/server-filesystem`,
  local path access only.
- **browser** — `@playwright/mcp`, local Playwright-controlled browser.
- **git** — `@cyanheads/git-mcp-server` (v2.15.3, active 2026-08-24, GitHub
  `cyanheads/git-mcp-server`). Local repo operations. **Note:** the npm package
  `mcp-server-git` is `0.0.1-security` (takedown placeholder) and **must not**
  be used.
- **postgres** — `@microsoft/postgres-mcp` (maintained; Apple-Silicon prebuilt
  used on this Mac). Launched with `--no-telemetry` to honor the no-exfiltration
  non-goal. Connection profile `local` → `postgresql://localhost:5432/grimdor`
  (Homebrew PostgreSQL 14, running locally). The official reference
  `@modelcontextprotocol/server-postgres` is **deprecated** on npm and was not
  used.

All changes were made with the sanctioned `openclaw mcp add` CLI (which probes
before saving) — never by hand-editing `openclaw.json`.

## Approval gating

Untrusted/untrusted-tool stdio servers are gated behind operator approval via
the per-server configuration written by the CLI:

```json
"git":      { ..., "codex": { "defaultToolsApprovalMode": "prompt" } }
"postgres": { ..., "codex": { "defaultToolsApprovalMode": "prompt" } }
```

`prompt` asks the operator before the agent invokes a tool from these servers.
Override anytime with `openclaw mcp configure <name> --approval approve|prompt|auto`.

## Calendar & email — not wired (documented gap)

The story's target list included **calendar** and **email**. These are **not**
wired, intentionally:

- No **curated, local-first, non-cloud** calendar MCP server exists. The
  mainstream options (Google Calendar, Microsoft, CoCal) are **cloud** servers
  that require OAuth and exfiltrate calendar data — both explicitly excluded by
  this story's non-goals ("no cloud MCP gateways", "no servers that exfiltrate
  data").
- Same for **email** — maintained options (Gmail, gogcli, tai-mcp) are cloud /
  third-party API services, not local-first.

**Recommendation:** defer calendar/email to a follow-up story scoped to a
local-first option (e.g. a read-only iCalendar/`.ics` file server or a local
IMAP-only server on a trusted port) that does not phone home. Revisit under a
child of THO-22 when such a curated server is available.

## How to add / remove / verify

```bash
openclaw mcp add <name> --command <cmd> --arg <a> ... --approval prompt
openclaw mcp doctor <name> --probe
openclaw mcp configure <name> --approval approve|prompt|auto
openclaw mcp status
```

## See also

- OpenClaw docs: `docs/tools/mcp.md`, `docs/tools/exec-approvals.md`
- Epic THO-22 · story THO-146

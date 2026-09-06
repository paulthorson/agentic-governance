# Adversarial Agents MCP Server

Exposes the adversarial review framework as callable MCP tools so any agent
(Claude Code, Cursor, OpenClaw, or a custom client) can run a governed review
without re-reading the framework files.

## Tools

| Tool | Purpose |
|------|---------|
| `list_domains` | List the 5 domains (ux, engineer, qa, researcher, universal) |
| `list_agents(domain)` | List a domain's adversary agents |
| `list_skills(domain)` | List a domain's stateless skills |
| `get_constitution(domain)` | Fetch a domain's constitutional rules |
| `get_standard(domain)` | Fetch a domain's quality standard |
| `get_agent(domain, agent_name)` | Fetch a full adversary agent body |
| `run_review(domain, work, context)` | Run a governed review → verdict + review prompt |
| `check_veto(domain, text)` | Check if text trips a hard constitutional veto |
| `record_verdict(domain, verdict, summary, ticket)` | Append to the decision record |
| `query_verdicts(domain, limit)` | Query recent verdicts |
| `framework_status()` | Health summary (counts, verdict log) |

## Run

```bash
cd mcp
uv run adversarial-mcp # stdio transport (default for MCP clients)
# or
uv run python -m adversarial_mcp.server
```

Point `ADVERSARIAL_ROOT` at the repo if it isn't `~/adversarial-agents`.

## Wire into a client

**Claude Code** (`~/.claude.json` or project `.mcp.json`):

```json
{
  "mcpServers": {
    "adversarial": {
      "command": "uv",
      "args": ["--directory", "<REPO_ROOT>/mcp", "run", "adversarial-mcp"]
    }
  }
}
```

**Cursor** (`.cursor/mcp.json`): same shape.

**OpenClaw** (`openclaw.json` → `mcp.servers`): same command/args.

## Notes

- Verdicts append to `runs/verdicts.jsonl` (gitignored) — real review history
  never gets committed.
- The structural veto scan is deterministic; the full review prompt is
  assembled for the domain's adversary agents to execute.

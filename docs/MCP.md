# MCP

The framework ships an MCP server (`mcp/`) that exposes the adversarial review
loop as callable tools. Any agent — Claude Code, Cursor, OpenClaw, or a custom
client — can run a governed review without re-reading the framework files.

## Tools

| Tool | Purpose |
|------|---------|
| `list_domains` | List the 5 domains |
| `list_agents(domain)` | List a domain's adversary agents |
| `list_skills(domain)` | List a domain's stateless skills |
| `get_constitution(domain)` | Fetch a domain's constitutional rules |
| `get_standard(domain)` | Fetch a domain's quality standard |
| `get_agent(domain, agent_name)` | Fetch a full adversary agent body |
| `run_review(domain, work, context)` | Run a governed review → verdict + review prompt |
| `run_review_deep(domain, work, context, model)` | Run a governed review, invoking the adversary agents via LLM (Ollama) |
| `check_veto(domain, text)` | Check if text trips a hard constitutional veto |
| `record_verdict(domain, verdict, summary, ticket)` | Append to the decision record |
| `query_verdicts(domain, limit)` | Query recent verdicts |
| `framework_status()` | Health summary (counts, verdict log) |

## Run

```bash
cd mcp
uv run adversarial-mcp # stdio transport (default for MCP clients)
```

Point `ADVERSARIAL_ROOT` at the repo if it isn't `<framework-root>`.

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

**Cursor** (`.cursor/mcp.json`): same shape. **OpenClaw** (`openclaw.json` →
`mcp.servers`): same command/args.

## Design notes

- **Deterministic first pass** — `check_veto` and the structural scan in
  `run_review` are objective keyword scans, giving a fast, reproducible gate.
- **Deep review** — `run_review_deep` actually invokes the adversary agents via
  Ollama (default `gemma3:12b`, safe size; override with `ADVERSARIAL_DEEP_MODEL`
  or per-call `model`). A structural veto always overrides the LLM verdict —
  the veto is absolute.
- **Prompt assembly** — `run_review` assembles the full review prompt
  (work + context + constitution + agent list) for the domain's adversary
  agents to execute.
- **Decision record** — verdicts append to `runs/verdicts.jsonl` (gitignored).
- **v1 API** — pinned `mcp<2` (FastMCP). v2 renamed FastMCP to MCPServer.

## See also

- [[Architecture]] · [[Calibration]] · [[Tooling]] · [[Home]]

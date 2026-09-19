# Onboarding: Claude Code

Wire the agentic-governance MCP server into **Claude Code** so your Claude agents run
governed reviews.

## Prerequisites

- [Claude Code](https://claude.ai/code) installed
- [uv](https://docs.astral.sh/uv/) installed
- The repo cloned (see [README Install](../../README.md#install-framework))

## 1. Install the MCP server

```bash
cd agentic-governance/mcp
uv sync
```

## 2. Wire it into Claude Code

Add the server to your Claude Code MCP config. Either:

**Project-level** (`.mcp.json` in your project root):

```json
{
  "mcpServers": {
    "governance": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/agentic-governance/mcp", "run", "adversarial-mcp"]
    }
  }
}
```

**User-level** (`~/.claude.json` → `mcpServers`): same shape.

> Replace `/absolute/path/to/agentic-governance` with the real path.

## 3. Verify

Restart Claude Code, then ask it to list the governance tools:

```
What MCP tools are available from the governance server?
```

You should see `list_domains`, `run_review`, `check_veto`, `get_constitution`, and the
rest.

## 4. Run a governed review

```
Use the governance server to run a review of this work in the engineer domain:
<your work>
```

Claude Code will call `run_review(domain, work, context)` and return a verdict plus a
review prompt for the domain's adversary agents.

## 5. Adopt your agent (BYOA)

Run the setup wizard to declare your roster and reconcile existing instructions:

```
Run the governance setup wizard and walk me through it.
```

The wizard asks `setup_wizard_start()` then `setup_wizard_answer(.)` for each
question. See [BYOA](byoa.md) for the full walkthrough.

## Notes

- The MCP server uses **stdio transport**, which is Claude Code's default.
- Verdicts append to `runs/verdicts.jsonl` (gitignored) — real review history is never
  committed.

# Onboarding: Cursor

Wire the agentic-governance MCP server into **Cursor** so your Cursor agents run
governed reviews.

## Prerequisites

- [Cursor](https://cursor.com) installed
- [uv](https://docs.astral.sh/uv/) installed
- The repo cloned (see [README Install](../../README.md#install-framework))

## 1. Install the MCP server

```bash
cd agentic-governance/mcp
uv sync
```

## 2. Wire it into Cursor

Add the server to `.cursor/mcp.json` in your project root:

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

> Replace `/absolute/path/to/agentic-governance` with the real path.

## 3. Verify

In Cursor, open the MCP panel (Settings → MCP) and confirm the `governance` server shows
as connected. Ask Cursor to list the governance tools — you should see `list_domains`,
`run_review`, `check_veto`, `get_constitution`, and the rest.

## 4. Run a governed review

```
Use the governance server to run a review of this work in the engineer domain:
<your work>
```

## 5. Adopt your agent (BYOA)

Run the setup wizard to declare your roster and reconcile existing instructions. See
[BYOA](byoa.md) for the full walkthrough.

## Notes

- Cursor also loads the framework's flat agents/skills from `~/.cursor/agents` and
  `~/.cursor/skills` if you run `scripts/consolidate-adversarial.py` (see the
  [README](../README.md)).
- The MCP server uses **stdio transport**, which Cursor supports.
- Verdicts append to `runs/verdicts.jsonl` (gitignored).

# Onboarding: Hermes

Wire the agentic-governance MCP server into **Hermes** so your Hermes agents run
governed reviews.

## Prerequisites

- [Hermes](https://hermes.ai) installed (an MCP-capable agent runtime)
- [uv](https://docs.astral.sh/uv/) installed
- The repo cloned (see [README](../README.md#quick-start-any-system))

## 1. Install the MCP server

```bash
cd agentic-governance/mcp
uv sync
```

## 2. Wire it into Hermes

Hermes supports MCP servers via its MCP configuration. Add the governance server using
the same stdio shape as other clients:

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

> Replace `/absolute/path/to/agentic-governance` with the real path. If Hermes uses a
> different config location or transport, adapt the wiring accordingly — the server
> itself is transport-agnostic.

## 3. Verify

Ask Hermes to list the governance tools. You should see `list_domains`, `run_review`,
`check_veto`, `get_constitution`, and the rest.

## 4. Run a governed review

```
Use the governance server to run a review of this work in the engineer domain:
<your work>
```

## 5. Adopt your agent (BYOA)

Run the setup wizard to declare your roster and reconcile existing instructions. See
[BYOA](byoa.md) for the full walkthrough.

## Notes

- The MCP server uses **stdio transport** by default. If Hermes only supports remote
  (HTTP/SSE) transport, see [Other MCP clients](other-mcp-clients.md).
- Verdicts append to `runs/verdicts.jsonl` (gitignored).

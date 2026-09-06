# Onboarding: ChatGPT / Codex

Wire the agentic-governance MCP server into **ChatGPT** or **Codex** (OpenAI's agentic
coding tool) so your OpenAI agents run governed reviews.

## Prerequisites

- [ChatGPT](https://chatgpt.com) or [Codex](https://openai.com/codex) with MCP support
- [uv](https://docs.astral.sh/uv/) installed
- The repo cloned (see [README](../README.md#quick-start-any-system))

## 1. Install the MCP server

```bash
cd agentic-governance/mcp
uv sync
```

## 2. Wire it into ChatGPT / Codex

OpenAI's MCP support lets you add a local (stdio) MCP server. The exact steps depend on
your client:

- **Codex CLI:** add the server to your MCP config (`.mcp.json` or the Codex config),
  same shape as Claude Code:

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

- **ChatGPT desktop / web:** use the MCP connector to point at a local server, or run
  the server and connect via the supported transport.

> Replace `/absolute/path/to/agentic-governance` with the real path.

## 3. Verify

Ask ChatGPT/Codex to list the governance tools. You should see `list_domains`,
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

- The MCP server uses **stdio transport** by default. If your OpenAI client only
  supports remote (HTTP/SSE) transport, you may need to run the server with a
  transport adapter — see [Other MCP clients](other-mcp-clients.md).
- Verdicts append to `runs/verdicts.jsonl` (gitignored).

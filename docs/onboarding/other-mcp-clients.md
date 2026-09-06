# Onboarding: Other MCP clients

The agentic-governance MCP server is transport-agnostic. Any client that supports the
[Model Context Protocol](https://modelcontextprotocol.io) can wire it in. This page
covers the general pattern and the clients not given a dedicated guide.

## The universal pattern

Every MCP client wires a server the same way: you give it a **command** and **args**
that launch the server. For this framework that is always:

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

Replace `/absolute/path/to/agentic-governance` with the real path. The server speaks
**stdio** by default.

## Known MCP clients

From the [MCP client list](https://modelcontextprotocol.info/docs/clients/), the
following support MCP **tools** (which is all this server needs):

| Client | Notes |
|---|---|
| Claude Desktop App | Full MCP support |
| Claude Code | See [claude-code.md](claude-code.md) |
| Cursor | See [cursor.md](cursor.md) |
| OpenClaw | See [openclaw.md](openclaw.md) |
| ChatGPT / Codex | See [chatgpt-codex.md](chatgpt-codex.md) |
| Hermes | See [hermes.md](hermes.md) |
| Cline | Tools + resources |
| Continue | Full MCP support |
| GitHub Copilot | Via Copilot-MCP |
| Goose | Tools |
| Roo Code | Tools + resources |
| Windsurf | Tools |
| Zed | Prompts |
| VS Code (MCP extension) | Tools + resources |
| LibreChat | Tools for agents |
| mcp-agent | Tools + connection management |

## If your client only supports remote (HTTP/SSE) transport

The server defaults to stdio. To expose it over HTTP/SSE, run it with a transport
adapter (e.g. `mcp-proxy` or the FastMCP HTTP transport) and point your client at the
resulting URL. The tool set is identical.

## Verify

After wiring, ask your agent to list the governance tools. You should see
`list_domains`, `run_review`, `check_veto`, `get_constitution`, `get_standard`,
`get_agent`, `list_agents`, `list_skills`, `record_verdict`, `query_verdicts`,
`framework_status`, and the setup wizard tools (`setup_wizard_start`,
`setup_wizard_answer`).

## Run a governed review

```
Use the governance server to run a review of this work in the engineer domain:
<your work>
```

## Adopt your agent (BYOA)

Run the setup wizard to declare your roster and reconcile existing instructions. See
[BYOA](byoa.md) for the full walkthrough.

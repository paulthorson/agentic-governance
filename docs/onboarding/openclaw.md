# Onboarding: OpenClaw

Wire the agentic-governance MCP server into **OpenClaw** so your OpenClaw agents run
governed reviews.

## Prerequisites

- [OpenClaw](https://openclaw.ai) installed
- [uv](https://docs.astral.sh/uv/) installed
- The repo cloned (see [README](../README.md#quick-start-any-system))

## 1. Install the MCP server

```bash
cd agentic-governance/mcp
uv sync
```

## 2. Wire it into OpenClaw

Add the server to `openclaw.json` under `mcp.servers`:

```json
{
  "mcp": {
    "servers": {
      "governance": {
        "command": "uv",
        "args": ["--directory", "/absolute/path/to/agentic-governance/mcp", "run", "adversarial-mcp"]
      }
    }
  }
}
```

> Replace `/absolute/path/to/agentic-governance` with the real path.

## 3. Verify

Restart OpenClaw, then ask it to list the governance tools. You should see
`list_domains`, `run_review`, `check_veto`, `get_constitution`, and the rest.

## 4. Run a governed review

```
Use the governance server to run a review of this work in the engineer domain:
<your work>
```

## 5. Adopt your agent (BYOA)

Run the setup wizard to declare your roster and reconcile existing instructions. See
[BYOA](byoa.md) for the full walkthrough.

## Notes

- The MCP server uses **stdio transport**, which OpenClaw supports.
- Verdicts append to `runs/verdicts.jsonl` (gitignored).
- Studio OpenClaw anonymized scars / pin process locks (Standing AG SoT):
  [`projects/openclaw/`](../../projects/openclaw/).

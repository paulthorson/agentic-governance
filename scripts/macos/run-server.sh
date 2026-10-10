#!/bin/bash
# launchd entry point for the hardened MCP server (ADR-0013). Runs as the
# service user. Reads the bearer token from config/ (mode 600) so it never
# appears in the world-readable LaunchDaemon plist.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
export ADVERSARIAL_ROOT="$ROOT"
export PYTHONPATH="$ROOT/mcp"
MCP_AUTH_TOKEN="$(cat "$ROOT/config/mcp_auth_token")"
export MCP_AUTH_TOKEN
# A shared HTTP server must never inherit one agent's identity or approval.
unset AG_AGENT_TOKEN AG_APPROVAL AG_APPROVAL_TOKEN
exec "$ROOT/.venv/bin/python" -m adversarial_mcp.server \
  --transport streamable-http --host 127.0.0.1 --port "${AG_PORT:-8765}"

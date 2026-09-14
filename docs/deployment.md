# Deploying the MCP server remotely

The adversarial MCP server can run over stdio (local, the default) or over HTTP
for remote deployments. This page covers the production deployment path.

## Local (stdio) — default

```bash
cd mcp
uv run adversarial-mcp # stdio transport (default for MCP clients)
```

## Remote (streamable HTTP)

```bash
cd mcp
MCP_AUTH_TOKEN=<token> MCP_RATE_LIMIT=60 \
  uv run adversarial-mcp --transport streamable-http --port 8000 --mount-path /mcp
```

- `MCP_AUTH_TOKEN` — when set, every HTTP request must carry
  `Authorization: Bearer <token>` (401 otherwise).
- `MCP_RATE_LIMIT` — requests per minute per IP (429 over the limit).
- `--mount-path` — the HTTP path the MCP endpoint is served at (default `/mcp`).

## Production hardening

The bearer token + rate limit are a lightweight gate. For a production remote
deployment, put the server behind a reverse proxy or API gateway:

### Option A — Reverse proxy (recommended)

Run the server on a private interface (e.g. `127.0.0.1:8000`) and put it behind
a reverse proxy (nginx, Caddy, or a cloud load balancer) that terminates TLS
and enforces mTLS:

```nginx
# nginx example — TLS + client cert (mTLS)
server {
    listen 443 ssl;
    server_name mcp.example.com;
    ssl_certificate     /etc/ssl/mcp.crt;
    ssl_certificate_key /etc/ssl/mcp.key;
    ssl_client_certificate /etc/ssl/ca.crt;   # client CA
    ssl_verify_client on;                       # require a client cert

    location /mcp {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }
}
```

### Option B — API gateway

Put the server behind a managed API gateway (AWS API Gateway, Cloudflare, etc.)
that handles auth (API keys, OAuth), rate limiting, and TLS termination. The
gateway forwards to the server's HTTP endpoint.

## Client wiring

Point your MCP client at the remote endpoint. For a streamable-http server with
bearer auth, the client sends the token in the `Authorization` header. See
[`docs/onboarding/`](onboarding/) for per-framework wiring.

## Security notes

- The bearer token is a shared secret; rotate it and store it in a secret
  manager, not in the repo.
- mTLS (Option A) is the strongest auth for machine-to-machine; use it when the
  client supports client certificates.
- The server binds `127.0.0.1` by default for HTTP. LAN exposure requires an
  explicit `--host 0.0.0.0` (prints a warning). Prefer loopback behind a proxy.
- Verdicts append to `runs/verdicts.jsonl` (gitignored) — real review history
  is never committed.

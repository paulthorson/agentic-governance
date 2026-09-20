# Security Policy

## Reporting a vulnerability

This is an unpaid personal project. If you find a security issue, do **not** open a
public issue.

Contact: **security@agenticgovernance.app**

You can also report privately via GitHub: open a
[private vulnerability report](https://github.com/paulthorson/agentic-governance/security/advisories/new)
on this repository.

Please include: a description of the issue, the affected path, a minimal
reproduction, and suggested impact.

## Operator responsibility

You run the agents, the model provider account, the network, and the secrets.
This repository does not replace provider billing caps, OS firewalls, or human
review. See [`docs/capability-report.md`](docs/capability-report.md).

**This software does not provide a safety guarantee.**

## Security model (honest)

These are design goals and process rules. Only some have code gates today
([capability report §12.8](docs/capability-report.md#128-code-vs-instruction-controls-summary)).

1. **Blind-review isolation (instruction).** Advocates are instructed not to
   receive the worker’s rationale. There is **no** runtime wall that makes that
   impossible if a caller pastes rationale into a tool.
2. **Human-only veto clearing (process).** Constitutions say only a human clears
   a veto. Files remain writable; discipline is procedural.
3. **Append-only records (process).** Decision records should be appended, not
   rewritten. Ordinary filesystem writes are still possible.
4. **No secret exfiltration (instruction + operator hygiene).** Do not commit
   credentials. Secrets belong in the operator environment.
5. **Prompt-injection resistance (review checks / skills).** Skills and reviews
   flag override attempts; this is not a complete defense.

### Code gates that do exist

| Gate | Behavior | Cite |
|---|---|---|
| Spend (framework units) | Gated MCP reviews refuse at configured numeric cap | capability report §12.1 |
| Network permission | Messaging egress only if `allow`; unknown/deny = no egress | §12.3 |
| Approval checkpoints | Listed subprocess/outbound/outside-write sites refuse without `AG_APPROVAL=1`, `AG_APPROVAL_TOKEN`+`runs/approval.token`, or `runs/approval.ok` | §12.2 |
| HTTP bind | Default `127.0.0.1`; LAN requires explicit `--host` | §12.3 |

### Unchecked (operator must assume open)

- Agent runtimes and tools **not** calling the gated scripts/MCP entrypoints
- Dashboard admin is localhost Host only — remote identity login removed ([§7.2–7.4](docs/capability-report.md#126-secrets-dashboard-site))
- Model-provider token and dollar spend
- Absolute paths the operator points outside the repo when a helper does not gate them
- Blind-review / veto / append-only as technical impossibilities (they are not)

## Secret handling

- Never commit `.env`, `*.pem`, or credential files. `.gitignore` excludes common patterns.
- `dashboard/.env.example` ships **empty** `AUTH_*` placeholders ([§7.1](docs/capability-report.md#71-history--credentials)).
- Rotate any token you place in `MCP_AUTH_TOKEN` or alert webhooks.

## Supported surface

Markdown harnesses/constitutions + MCP server tools + helper scripts. Treat remote
HTTP MCP as hostile-network exposure unless you terminate TLS and auth in front of
loopback ([`docs/deployment.md`](docs/deployment.md)).

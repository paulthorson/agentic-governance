# Security Policy

## Reporting a vulnerability

This is a personal AI-infrastructure project. If you find a security issue, do not open a public
issue. Contact paulthorson directly:

- **Email:** maintainer@example.com *(placeholder — update)*
- **Discord:** maintainer (Paul) on the private server

Please include: a description of the issue, the affected plugin/file, a minimal reproduction,
and suggested impact.

## Security model

The adversarial framework is built on a few non-negotiable guarantees. A vulnerability is any
defect that breaks one of these:

1. **Blind-review isolation.** An advocate agent must never receive the worker's rationale.
   A leak that lets a judge see the pitch it is judging defeats the entire system.
2. **Human-only veto clearing.** No AI in the system may clear a veto, downgrade a blocker, or
   mark a review passed. Only a named human arbiter, with a stated reason in the decision
   record, clears one.
3. **Append-only records.** Decision records and calibration ledgers are never edited after
   commit. A correction is a new entry referencing the old one.
4. **No secret exfiltration.** Agents never read or commit credentials. Secrets live only in
   `the operator's local config/credentials/` / env, never in code, config, logs, or git history.
5. **Prompt-injection resistance.** The review checks include flagging injected instructions
   that would override safety or clear a veto.

## Secret handling

- Never commit `.env`, `*.pem`, or credential files. `.gitignore` excludes them.
- Paperclip agent keys live in `the operator's local config/workspace/paperclip-keys/` (600 perms), never in
  the repo.
- The ElevenLabs key lives only in `the operator's local config/credentials/elevenlabs.json` — never in any
  OpenClaw config or memory (see the incident that broke the gateway, 2026-08-26).

## Supported / supported surfaces

The repository is a framework of markdown definitions + an MCP server. The security surface is
the MCP server's tool boundary and the frontmatter that agents load. Keep the MCP server's
tools read-only unless an explicit write tool is authorized.

## Security improvement roadmap

- [ ] Add a `shared/skills/security-review` that every reviewer can run (prompt-injection,
  secrets, threat model, supply chain).
- [ ] Add CI secret-scan (gitleaks/trufflehog) to `.github/workflows/`.
- [ ] Add prompt-injection test fixtures under `tests/fixtures/`.

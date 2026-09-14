# Initiative evidence — initiative-11-governed-extension-platform

Shipped 2026-09-13. Veto's governed extension platform: third-party extensions
run under a manifest-declared capability model, a default-deny sandbox, a
reusable policy kit, a one-template developer scaffold, Ed25519-signed packages
with publisher-key pinning, and a four-gate curated registry. Extensions must
prove what they access and cannot bypass confirmation, policy, governance, or
audit behavior.

## Scope

- `initiatives/i11/`: `manifest/` (closed capability vocabulary + published
  `MANIFEST_SCHEMA.json`), `sandbox/` (capability broker, deep-frozen
  manifests, HMAC-bound single-use confirmation tokens, fs/net sandboxes,
  hash-chained audit), `policy_kit/` (10 checks + 14 adversarial attacks),
  `scaffold/template.py` (manifest, entrypoint, tests, docs, web card,
  wizard step, CLI/MCP snippets, retro), `signing/` (Ed25519 packages,
  pinning, upgrade review, revocation), `registry/` (compatibility/security
  automated gates, ux/governance human gates),
  `reference/role-radar-digest/` (self-built reference extension, signed),
  README, `integration_notes.md`, `contracts_needed.md`
- `crew.py`: extension host singleton + `extension` CLI command + 7 MCP tools
  (confirmation-token minting is deliberately NOT an MCP tool);
  `mcp-config.json` gains `VETO_EXTENSIONS_DIR`
- 6 test modules, 68 tests, all green; 14/14 adversarial attacks blocked
- Exact deferred wiring for `cli.py`/`server.py`/`webui.py`/`dashboard.py`
  specified in `integration_notes.md` — none of those files edited (owned by
  the integration sweep)

## Governance

- Ticket `muse/2026-09-13/roadmap-exec/init-11/core` (security): first review
  returned **KICK_BACK** — the blind review demonstrated 5 working bypasses:
  (1) `ctx._host` traversal allowed self-minting confirmation tokens;
  (2) mutable context scopes shared with host checks allowed scope escalation;
  (3) mutable action metadata allowed `confirm-required`→`read` downgrade;
  (4) unbanned `initiatives` imports exposed the host secret for token forgery;
  (5) unbanned `os`/`pathlib`/`open()` bypassed the filesystem sandbox and PII
  redaction. All five fixed (token-dispatch broker in a safe-globals module,
  deep-frozen manifests with enforcement reading the frozen copy, extended
  import bans, bare `open()` as a hard violation) and re-verified — re-review
  **ALLOW**.
- Ticket `muse/2026-09-13/roadmap-exec/init-11/platform` (qa): **ALLOW** —
  scaffold generates all 8 surfaces and the scaffolded extension passes the
  full policy suite; signing was upgraded HMAC→Ed25519 during review with
  registry publisher-pubkey pinning; install pinning + upgrade review +
  append-only revocation verified; registry gates correctly block install
  until all four pass.
- 0 structural vetos. Both verdicts carry the depth-2 isolation caveat (reviews
  executed by the coordinator with framework adversary prompts applied to the
  work product only); a genuinely independent re-review is flagged to the
  program coordinator before these are treated as fully cleared.

## Metrics

- New tests: 68 (manifest 12, sandbox 24, adversarial 14 subtests, signing/registry 13, scaffold, crew)
- Full product suite at ship: 1963 total, 0 failures after this initiative's
  own `test_crew` assertion fix (stale vs the new `extension` CLI command),
  8 skipped
- Adversarial: 14/14 attacks blocked by the builder-run suite
- Commit pushed to product main same session

## Assumptions and degradation (from contracts_needed.md)

- Initiative 09 provider contracts and Initiative 10 packaging assumed to land
  as described; Initiative 11 degrades cleanly if they change (documented
  fallback rules: fail closed on unknown capabilities, warn-only on missing
  governance adapter, disabled publishing without the packaging contract)
- Extension-developer demand assumed; scaffold value demonstrated by the
  self-built reference extension (role-radar-digest: read-only, local drafts,
  notification proposals)

## Residual risk (disclosed in README threat model)

- In-process execution retains an introspection residual (`__globals__` /
  dunder paths); the honest design closes every plain-attribute path and names
  the compensating controls: registry human review reads the code (the AST
  scan is a tripwire, the review is the control), signatures, and audit.
- Out-of-process execution is the roadmap's hardening step; this platform is
  the enforcement point, not the final isolation boundary.

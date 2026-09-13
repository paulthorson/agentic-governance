# Initiative evidence — design-system-monorepo

Shipped 2026-09-13. Veto's design system fully codified into a private monorepo
(`@veto/tokens`, `@veto/web`, `@veto/terminal`), wired into the marketing site,
local web dashboard, and terminal dashboard.

## Scope

- `@veto/tokens`: 88 tokens, semantic/component/tone tiers, 7 tests
- `@veto/web`: 12 component CSS modules, zero radius, stepped motion, reduced-motion support
- `@veto/terminal`: `theme.json` + `veto_theme.py`, 25 tests, real usage in `dashboard.py`
- Live `preview/index.html`; DECISIONS.md, MAPPING.md, usage/migration/versioning docs
- Sync script: copy → byte verification → manifest, refuses corruption

## Governance

- Ticket: `muse/2026-09-13/design-system-monorepo`
- **7/7 review domains ALLOW** (fresh reviewers, append-only verdicts)
- UX track: user flows, JTBD job stories, explicit research validation — first-class
  review inputs, not an appendix

## Metrics

- 57 worker subagents — largest coordinated run to date
- Veto suite at ship: 955 passed, 0 failures, 8 skipped

## Caveats (disclosed)

- Raw survey files were lost to a `/tmp` wipe mid-session (disclosed in DECISIONS.md);
  durable-inputs rule adopted: review inputs live under `~/workspace`, never `/tmp`.
- Verification was source/test/build/byte-identity; no browser-rendered screenshots.

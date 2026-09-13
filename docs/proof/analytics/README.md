# Analytics — evergreen

Current as of 2026-09-13. This file is always the latest: update it in place as
new data lands. Superseded versions are kept in `archive/`.

## Review verdicts (cumulative)

| Verdict | Count |
|---|---|
| ALLOW / SHIP | 36 |
| KICK_BACK (rework required) | 32 |
| Review rounds opened | 64 |

- 8 governed tickets across 2026-09-12 → 2026-09-13.
- KICK_BACK rate ≈ 47% of decided verdicts: the adversarial loop fires in practice,
  not just in theory. Every KICK_BACK returned to the builder with findings and
  was re-reviewed by a fresh reviewer before shipping.
- Veto overrides: 0 — no human veto clearance was needed; builders cleared every
  finding through rework.

## Velocity (selected runs)

| Run | Agents | Outcome |
|---|---|---|
| Veto design-system monorepo (tokens, 3 platform packages, docs, app wiring) | 57 workers | 7/7 review domains ALLOW, shipped + pushed same session |
| Annual roadmap P0 scope restoration (24-page plan, full review loop) | ~20 workers across 3 rounds | 4/4 seats ALLOW after one critic KICK_BACK (5 findings, all resolved) |
| Veto phone access (LAN serve, token auth, setup wizard, responsive pass) | ~12 workers | 3/3 reviews ALLOW, 955 tests green |

## Quality

- Veto test suite: **955 passed, 0 failures, 8 skipped** (2026-09-13).
- Design-system packages: 88 design tokens + component CSS modules + terminal theme,
  all with passing test suites; sync script byte-verifies every publish.

## Machine-readable

`archive/` holds the dated JSON snapshots alongside each superseded Markdown version.

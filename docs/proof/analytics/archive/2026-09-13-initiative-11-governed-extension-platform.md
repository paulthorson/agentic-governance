# Analytics — evergreen

Current as of 2026-09-13 (refreshed by the Initiative 05
application-studio run). This file is always the latest: update it in place as
new data lands. Superseded versions are kept in `archive/`.

## Review verdicts (cumulative)

| Verdict | Count |
|---|---|
| ALLOW / SHIP | 56 |
| KICK_BACK (rework required) | 32 |
| Review rounds opened | 94 |

- 24 governed tickets across 2026-09-12 → 2026-09-13.
- KICK_BACK rate ≈ 36% of decided verdicts: the adversarial loop fires in practice,
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
| Veto Initiative 07 mentor matching & warm paths (consent handshake, safety, session kit, warm-path drafts) | 1 coordinator (depth-limited, no subagent spawn) | 6/6 review tickets ALLOW, 82 new tests green, shipped + pushed same session |
| Veto outcome-min-v0 capture (Initiative 01: event schema, append-only store, migration contract, coverage gate) | 1 coordinator (depth-limited, no subagent spawn) | 1/1 reviews ALLOW (9 findings fixed pre-verdict), 58 new tests green, shipped + pushed same session |
| Veto application studio (Initiative 05: versioned resumes, evidence library, ATS check, diff, packet, earned feedback) | 1 coordinator, 5 review rounds | 5/5 reviews ALLOW, 90 new tests green, shipped same session |

## Quality

- Veto test suite: **1760 total, 5 failed, 0 errors, 8 skipped** (2026-09-13, latest full-tree run). The 5 failures are confined to other teams' in-flight uncommitted modules (test_crew, test_i04_schemas, test_i04_share_card, test_i06_ai_lab); Initiative 05's 90 tests all green.
- Design-system packages: 88 design tokens + component CSS modules + terminal theme,
  all with passing test suites; sync script byte-verifies every publish.

## Machine-readable

`archive/` holds the dated JSON snapshots alongside each superseded Markdown version.

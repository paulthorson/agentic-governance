# Analytics — evergreen

Current as of 2026-09-13 (updated by the Initiative 01 outcomes-capture run;
Initiative 09 connector-reliability evidence row added).
This file is always the latest: update it in place as new data lands.
Superseded versions are kept in `archive/`.

## Review verdicts (cumulative)

| Verdict | Count |
|---|---|
| ALLOW / SHIP | 80 |
| KICK_BACK (rework required) | 26 |
| Review rounds opened | 130 |

- Counts recomputed from the append-only verdict log (governance-tools runs,
  2026-09-13): every recorded verdict row, ALLOW/SHIP/PASS counted as ALLOW.
  KICK_BACK counts cannot decrease under append-only, so the log is the source
  of truth — this replaces earlier per-round subsets that are not reproducible
  from the log.
- KICK_BACK rate ≈ 25% of decided verdicts: the adversarial loop fires in practice,
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
| Veto Initiative 09 connector reliability & coverage (contract kit, ATS deepening, session rescue, channels, calendar, scorecard) | 1 coordinator (depth-limited, no subagent spawn) | 7/7 review tickets ALLOW, 105 new tests green, shipped + pushed same session |

## Quality

- Veto test suite: **1602 total, 2 failed, 0 errors, 8 skipped** (2026-09-13,
  Initiative 01 outcomes-capture run). The 2 failures are confined to other
  teams' in-flight uncommitted modules (test_crew: stale assertion vs another
  team's `extension` CLI command; test_skill_gaps: passes standalone and with
  all capture modules combined — ordering interaction elsewhere). Initiative 01's
  58 tests all green; see its EVIDENCE.md for details.
- Initiative 09 added 105 tests, all green (7 adapter tests exercise Initiative 03's contract when it is in-tree and skip gracefully otherwise). Full-tree run at Initiative 09 ship: 1492 tests; failures confined to other teams' in-flight uncommitted work (`test_contribute`, `test_crew`, `test_ext_sandbox` — files outside Initiative 09's scope), flagged not touched.
- Design-system packages: 88 design tokens + component CSS modules + terminal theme,
  all with passing test suites; sync script byte-verifies every publish.

## Machine-readable

`archive/` holds the dated JSON snapshots alongside each superseded Markdown version.

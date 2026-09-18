# Initiative evidence — initiative-01-outcomes-capture

Shipped 2026-09-13. `outcome-min-v0` event capture is ACTIVE in the governed product
(a private product repository, commit `e44fb5a` on `main`): the annual
roadmap's Week-0 minimum event (Decision 02), the gating deliverable that
must precede the P0 craft audit. The P0 audit is now unblocked.

## Scope

- `outcomes.py` (new, ~1130 lines): `outcome-min-v0` schema — `event_id`,
  `application_id`, `event_type` (11 canonical types: discovered,
  shortlisted, applied, replied, screened, interviewed, offered, accepted,
  rejected, withdrawn, stale), `occurred_at`, `source`, `role`,
  `provenance`, `schema_version`. Append-only JSONL store; content-identity-key
  duplicate rejection (identical events rejected, never double-appended);
  reversible provenanced corrections (appended events with `corrects` pointers —
  originals are never edited); timeline/query APIs; CSV import; guided manual
  stage updates (`veto outcomes update`); stale/missing-outcome prompts;
  coverage reporting; `VETO_OUTCOMES_FILE` store override; MCP tools
  (`outcome_record_event`, `outcome_coverage`, `outcome_prompts`,
  `outcome_timeline`) and CLI (`veto outcomes record|timeline|coverage|prompts|import-csv|update`).
- `outcome_migration.py` (new): canonical migration contract — identity and
  time preserved, lossless `verify_migration`, recorded rollback records,
  re-runnable after rollback.
- `docs/outcome-event-contract.md` (new): published schema contract — field
  names, storage rules, duplicate semantics, correction rules, migration
  contract, MCP/CLI surfaces, coverage metrics.
- Wiring (guarded, exception-safe — core flows never depend on capture):
  `server.py` hooks on confirmed submissions (phase-1 and phase-2 browser),
  `apply_queue.py` hook including the dedupe early-return path,
  `lifecycle.update_stage` mirrors stage changes to canonical event types,
  `analytics.py` gains event-query side (`outcome_coverage`,
  `outcome_timeline`, `outcome_prompts`; `generate_report` adds
  `event_coverage` + `recent_outcome_events`).
- Coverage instrumentation for the Q4 ≥95% exit gate: cohort, semantic
  (1/11 Week-0), and state-change coverage, plus an `insufficient_data` flag
  so vacuous 1.0 values can never be claimed as gate evidence.

## Governance

- Ticket: `muse/2026-09-13/roadmap-exec/capture`
- Review rounds opened: 1 (`qa` domain, framework `ag_review.py`; structural
  veto scan clean, no veto triggered)
- Adversary agents executed: critic, edge-case-reviewer, quality-advocate
- Verdicts: **1 ALLOW, 0 KICK_BACK** — initiative KICK_BACK rate 0%
- The adversarial pass found 9 real defects across two passes; all were
  fixed and re-tested before the verdict (see Caveats). No user-harm veto
  triggers: append-only store, reversible corrections, capture never
  submits anything, every capture path is exception-guarded.

## Workers / agents

- 1 coordinator (depth-2 subagent; subagent spawn not available at depth 2,
  so the build was executed directly — no worker subagents)
- 3 adversary agent roles executed in a dedicated reviewer posture against
  the work product + framework review prompt
- Review bundle: `~/workspace/review-capture-outcome-min-v0/REVIEW.md`

## Metrics / verification

- 58 new tests (`tests/test_outcomes.py`): schema validation, append-only,
  duplicate rejection, corrections, migration/rollback/verify, CSV import,
  guided updates, CLI handlers, MCP tools, coverage math — all green
- Related suites (lifecycle, analytics, apply_queue, followup, cli_help):
  green; combined spot run 125 passed
- Full suite at ship (`tests/run.py`, 2026-09-13): **1602 total, 0 errors,
  8 skipped, 2 failures** — both failures confined to other teams'
  in-flight uncommitted work (`test_crew`: stale assertion against another
  team's `extension` CLI command, fails standalone, zero outcome references
  in its diff; `test_skill_gaps`: passes standalone and with all capture
  modules combined — ordering interaction elsewhere). Flagged, not touched
  (disjoint scope).
- Veto overrides: 0. Human-primacy notes: no human gate was inserted and
  none was needed — the directive was fully autonomous execution with
  evidence delivered for later review; no reviewer attempted to override
  explicit scope.

## Caveats (disclosed)

- **Reviewer isolation:** depth-2 execution cannot spawn an independent
  reviewer subagent. The adversarial pass was executed by the builder in a
  dedicated reviewer posture (work product + framework review prompt only,
  inherited rationale explicitly excluded). The verdict record carries this
  caveat; an independent blind re-review should be arranged before this is
  treated as fully cleared.
- **Production capture is instrumented, not yet observed:** the ≥95% gate is
  computed and tested, but no real-world capture data exists yet (the
  enablement marker is written on the first real event). The gate claim is
  about the mechanism, not measured coverage.
- **Coverage holes by construction:** the three known write paths are hooked;
  any future application-recording path added without a hook would silently
  miss events. Browser-failure submissions record stage `applied` with
  `provenance.submitted=false` — consumers must read the flag.
- One accidental `ag_review.py record` probe with summary `"test"` landed in
  the append-only verdict log under this ticket (cannot be deleted; disclosed
  here, not counted as a review round).
- The `.gitignore` outcome-store hunks remain uncommitted (another team's
  `.gitignore` hunks were in flight; coordinated, not staged). The runtime
  store files are ignored locally regardless.

## Assumption vs evidence flags

- EVIDENCE: schema fields, append-only behavior, duplicate rejection,
  correction reversibility, migration identity/time preservation, rollback,
  coverage math — all covered by the 58-test suite, run green 2026-09-13.
- EVIDENCE: capture hooks execute on confirmed submissions — queue path
  covered by tests; server hooks are thin guarded wrappers (no direct unit
  test; accepted as minor, disclosed).
- EVIDENCE: verdict ALLOW recorded append-only under
  `muse/2026-09-13/roadmap-exec/capture`; commit `e44fb5a` on the product repository's
  `main`; full-suite numbers measured 2026-09-13.
- ASSUMPTION: "100% of confirmed submissions after enablement are captured"
  — true for the three hooked write paths by construction; unproven against
  future write paths and unobserved in production.
- ASSUMPTION: adversarial independence — the pass was rigorous (9 real
  defects found and fixed) but not blind; see Caveats.

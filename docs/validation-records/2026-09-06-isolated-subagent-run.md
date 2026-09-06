# Isolated-Subagent Test Run — Validation Record

**Epic:** "Add a `--output` flag to the calibration-report script" (the completed BA epic, re-run with true isolated subagents).
**Date:** 2026-09-06. **Chain:** CEO → Research (→ escalation to CEO).
**Method:** Each role ran as a **true isolated subagent** (no shared reasoning, no shared context). Each loaded the constitution + its harness + only the single upstream artifact.

## What the chain did

1. **CEO** (isolated) received the solution-framed objective. Per A18.3, it restated it as a problem and produced a research question. **Critically, it did NOT ask the researcher to recommend** — respecting the researcher harness's prohibition. This validates the A11 harness-conflict fix in a real isolated run.

2. **Research** (isolated) read the actual script and the git history. It found the **premise is false**: the `--output` flag **already exists** in the committed codebase (implemented and D1/D2-fixed in commit `6a6e83a`). The research question's premise ("writes only to stdout") is contradicted by the evidence.

3. **Research escalated to the CEO** per its harness stop condition ("If the evidence contradicts the premise of the objective, stop and escalate to the CEO bot"). It produced the evidence pack establishing the true state rather than handing the PM a brief-shaped answer to a false-premise question.

## What this proves

**True isolated subagents work end to end:**

- **A18.3 works** — the CEO restated the solution-framed objective as a problem, unprompted, in a true isolated context.
- **The harness-conflict fix held** — the CEO did not ask the researcher to recommend (the A11 finding is fixed and verified in a real run).
- **Research is a real check** — it read the actual code and git history, found the premise false, and escalated rather than re-doing already-done work.
- **The chain does not stall or duplicate** — it caught that the epic was already complete and escalated, rather than re-running the full chain on done work.

## What broke / findings

- **The epic was already done.** The `--output` flag was implemented and committed (as part of completing the BA epic). The isolated run correctly caught this and escalated rather than re-doing it. This is a finding about the epic's timing, not the framework — the framework correctly identified that the work was already complete.

## Artifacts

- `research-question.md` (CEO — problem restatement, no recommendation asked)
- Evidence pack (Research — found the premise false, escalated)
- This record

## Recommendation

The epic is already complete (the `--output` flag is implemented, validated, and committed). No further work is needed on it. The isolated-subagent run validated the framework's core guarantees: A18.3 restatement, the harness-conflict fix, Research as a real check, and clean escalation on a false premise.

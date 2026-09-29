# ADR-0008: Continuous Learning Loop

- **Status:** Proposed
- **Date:** 2026-09-24
- **Supersedes:** _(none)_

## Context

The framework records its mistakes well — retrospectives, the calibration
ledger, daily improvement reports — but recording is write-heavy and
read-light. Nothing forces the next piece of work to consult past lessons
before starting, so the same failure classes recur across verdicts, each
treated as a new surprise. Lessons live as prose; prevention needs
enforcement.

## Decision

Adopt the Continuous Learning Loop (`docs/learning-loop.md`):

- A canonical failure-class registry (`docs/learning-loop-registry.md`).
  One entry per recurring failure pattern, never per incident, never per
  person.
- Retrospectives tag failure-class ids; each tag increments the class's
  occurrence count. Counting is a required retrospective step.
- Graduation rungs: 1st occurrence → written convention; 2nd → mandatory
  pre-flight checklist item injected into matching briefs (automatic);
  3rd → fail-closed gate in review prompts, QA sensors, or automated
  scripts (requires maintainer approval).
- Machine-checkable classes skip to scripted gates. Checks that run beat
  lessons that must be recalled.
- Seat-neutral by design: any team or harness generating briefs from this
  framework performs the same pre-flight registry read.

## Consequences

Positive: recurrence becomes a measured signal instead of anecdote; the
calibration ledger gains an aggregated consumer; prevention strengthens
automatically with each repeat; adopting teams share one mechanism.

Negative: retrospectives gain one required field; the registry needs
curation; rung-3 gates add review strictness that must be maintained
(stale gates are worse than none — the maintainer must prune).

Trade-off: rung-3 graduation requires maintainer approval rather than
being fully automatic, because gates change fail-closed behavior. The
recurrence count is the evidence that makes approval routine.

## Alternatives considered

- **Heavier reviewer prompts listing every past lesson.** Rejected: prompt
  bloat; reviewers skim; no recurrence signal.
- **Fully automatic gate creation.** Rejected: gates change what the
  framework refuses to pass — that decision stays with the maintainer.
- **Per-team learning systems.** Rejected: fragments the signal; the
  framework's value is the shared, compounding record.

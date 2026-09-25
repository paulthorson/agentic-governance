# Continuous Learning Loop

## TL;DR

Governance gets smarter when a repeated mistake automatically becomes harder
to repeat. This document defines a closed loop: every failure is recorded
against a canonical failure class, recurrences are counted, and at fixed
thresholds the lesson graduates from advice to checklist to enforced gate.
No lesson depends on anyone remembering it.

## The problem

Review systems are good at catching a mistake once. They are bad at
preventing the same mistake twice, because lessons are usually recorded as
prose that nobody is forced to read before the next piece of work. The
result is recurrence: the same failure classes appear in verdict after
verdict, each treated as a new surprise.

This loop fixes that by making recurrence itself the trigger for stronger
containment.

## The loop

```
Record → Count → Graduate → Enforce
```

1. **Record.** When a failure occurs, the retrospective tags it with a
   failure-class id (see the registry). If no class fits, a new one is
   opened using `docs/templates/failure-class.md`.
2. **Count.** Each tagged occurrence increments the class's occurrence
   count. Counting is a required step of the retrospective, not an
   optional annotation.
3. **Graduate.** When the count crosses a threshold, the class moves up
   one rung (see below). Graduation to checklist level is automatic;
   graduation to gate level requires maintainer approval, because gates
   change fail-closed behavior.
4. **Enforce.** At the gate rung, the lesson is a check that runs — a
   review-prompt item, a QA sensor, or an automated script. It cannot be
   skipped by forgetting.

## The failure-class registry

The registry (`docs/learning-loop-registry.md`) is the single canonical
list of failure classes. One class per recurring failure pattern — not per
incident. Each entry carries:

- **id** — stable, e.g. `FC-001`
- **title** — short name
- **description** — what the failure looks like, in plain language
- **work types** — tags matching it to the kinds of work it affects
   (e.g. `build`, `deploy`, `review`, `docs`)
- **occurrences** — running count of tagged retrospectives
- **rung** — current containment level (1, 2, or 3)
- **containment** — where the current rung lives (which brief template,
   checklist, review prompt, or script)

## Graduation rungs

| Rung | Name       | Trigger              | Form |
|------|------------|----------------------|------|
| 1    | Convention | 1st occurrence       | Written guidance in the relevant brief template or operator notes. Advisory. |
| 2    | Checklist  | 2nd occurrence       | Mandatory pre-flight item injected into briefs for matching work types. A coordinator or reviewer confirms it; work does not start until it is addressed. |
| 3    | Gate       | 3rd occurrence + maintainer approval | Fail-closed check: a review-prompt item, QA sensor, or automated script. Work cannot pass review while the gate is open. |

Rules:

- A class never moves down a rung. Containment only strengthens.
- Rung 3 requires maintainer approval because it changes what the
   framework refuses to pass. The recurrence count is the evidence the
   maintainer reviews — approval should be routine when the count is real.
- If a failure class is machine-checkable (a script can detect it), it
   should skip directly to a scripted gate at rung 3. Prefer checks that
   run over lessons that must be recalled.

## Pre-flight injection

Brief generation is where prevention happens. Before work starts, the
brief author reads the registry and injects every rung-2 checklist item
whose work-type tags match the planned work. The items travel with the
brief — the builder answers them, the reviewer verifies them.

This is deliberately seat-neutral: any seat, team, or harness that
generates briefs from this framework performs the same step and gets the
same protection.

## Recurrence counting

Counting happens inside the retrospective, which is already a required
step when work ships. The retrospective template gains one field:

```
failure-classes: FC-001, FC-004
```

The coordinator (or whoever writes the retrospective) updates the
occurrence counts in the registry in the same commit as the
retrospective. Counts are per class, never per person — this is a
learning tool, not a blame tool.

The calibration ledger remains the audit trail of individual verdicts;
the registry is the aggregated signal. A class with a climbing count is
the framework telling the maintainer where the system is weakest.

## Hook points

This loop plugs into existing machinery without modifying it here:

- **Brief templates** — add the pre-flight registry read as a generation
   step (rung 2 enforcement point).
- **Review prompts** — rung-3 gates land as fail-closed items.
- **QA sensors** — machine-checkable classes become sensors.
- **Improve reports** — the periodic improvement review reads the
   registry and reports which classes climbed, which graduated, and
   which gates were added.

Each adopting team wires these hooks into its own harnesses. The
framework defines the loop; the team owns the wiring.

## Maintainer role

The maintainer curates the registry, approves rung-3 gates, and reviews
the registry during the periodic improvement cycle. Day-to-day operation
— tagging, counting, rung-1/2 graduation — needs no approval and should
not wait for any.

## What this is not

- Not a blame system. Counts attach to failure patterns, not people.
- Not a second verdict log. Verdicts stay in the calibration ledger;
   the registry aggregates.
- Not a constitution change. This is a process rule. Failure classes
   that reveal a missing law are proposed through the normal lawmaking
   path; the registry is the evidence for the proposal.

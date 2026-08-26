---
description: Run only the blind adversary review against an existing engineering change, diff, or design
argument-hint: "<path to a diff, change description, architecture, or decision record>"
---

# /adversary-eng-review

Review $ARGUMENTS without generating anything.

1. Read `references/constitution.md` and `references/engineering-standard.md`.
2. Build `facts.md` from the submitted change following Step 3 of
   `skills/adversarial-engineer/SKILL.md`. Strip every trace of rationale.
3. Spawn `critic`, `ops-advocate`, and `reliability-reviewer` in parallel with the Agent tool.
   The Critic gets the full submission. The Ops Advocate gets `facts.md` only. Reliability
   Reviewer gets the change and runbook without rationale.
4. Paste all three verdicts verbatim.
5. Route per Step 5. An active veto stops the run and goes to the human arbiter.

Generate nothing. Fix nothing. This command reports.

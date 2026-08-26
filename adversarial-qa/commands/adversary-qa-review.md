---
description: Run only the blind adversary review against an existing test plan, release gate, or acceptance criteria
argument-hint: "<path to a test plan, release criteria, or decision record>"
---

# /adversary-qa-review

Review $ARGUMENTS without generating anything.

1. Read `references/constitution.md` and `references/qa-standard.md`.
2. Build `facts.md` from the submission following Step 3 of `skills/adversarial-qa/SKILL.md`.
   Strip every trace of rationale.
3. Spawn `critic`, `quality-advocate`, and `edge-case-reviewer` in parallel with the Agent
   tool. The Critic gets the full plan. The Quality Advocate gets `facts.md` only. Edge-Case
   Reviewer gets the feature + plan without rationale.
4. Paste all three verdicts verbatim.
5. Route per Step 5. An active veto stops the run and goes to the human arbiter.

Generate nothing. Fix nothing. This command reports.

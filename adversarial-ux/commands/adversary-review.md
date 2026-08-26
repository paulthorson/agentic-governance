---
description: Run only the blind adversary review against an existing design or flow
argument-hint: "<path to a design, flow description, or decision record>"
---

# /adversary-review

Review $ARGUMENTS without generating anything.

1. Read `references/constitution.md` and `references/design.md`.
2. Build `facts.md` from the submitted design following Step 3 of
   `skills/adversarial-ux/SKILL.md`. Strip every trace of rationale.
3. Spawn `critic`, `cx-advocate`, and `evaluative-uxr` in parallel with the Agent tool. The
   Critic gets the full submission. The Advocate gets `facts.md` only. Evaluative UXR gets the
   flow without rationale.
4. Paste all three verdicts verbatim.
5. Route per Step 5. An active veto stops the run and goes to the human arbiter.

Generate nothing. Fix nothing. This command reports.

---
description: Run only the blind evidence review against an existing synthesis or research output
argument-hint: "<path to a synthesis, research output, or decision record>"
---

# /adversary-research-review

Review $ARGUMENTS without generating anything.

1. Read `references/constitution.md` and `references/research-standard.md`.
2. Build `facts.md` from the submission following Step 3 of
   `skills/adversarial-researcher/SKILL.md`. Strip every trace of narrative.
3. Spawn `critic`, `evidence-advocate`, and `context-reviewer` in parallel with the Agent tool.
   The Critic gets the full output + sources. The Evidence Advocate gets `facts.md` only.
   Context Reviewer gets the synthesis without narrative.
4. Paste all three verdicts verbatim.
5. Route per Step 5. An active veto stops the run and goes to the human arbiter.

Generate nothing. Fix nothing. This command reports.

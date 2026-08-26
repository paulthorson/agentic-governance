---
description: Run the universal adversarial review against an existing artifact
argument-hint: "<path to a decision, plan, design, change, or claim>"
---

# /universal-review

Review $ARGUMENTS without generating anything.

1. Read `references/constitution.md` and `references/review-standard.md`.
2. Prepare the submission per Step 1 of `skills/adversarial-universal/SKILL.md`.
3. Spawn `universal-adversary` with the Agent tool, handing it the full submission.
4. Paste the verdict verbatim.
5. Route per Step 3. An active veto stops the run and goes to the human arbiter.

Generate nothing. Fix nothing. This command reports.

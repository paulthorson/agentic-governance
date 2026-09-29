---
name: adversarial-privacy
description: The worker skill for the adversarial-privacy loop. Orchestrates a governed review: the privacy-adversary agent reviews blind, the constitution gates, and only a human clears a veto.
---

# Adversarial Data & Privacy — Worker Skill

This is the orchestration loop for reviewing privacy work. It mirrors the
adversarial-ux loop: a worker produces, the adversary reviews blind, the
constitution gates, and only a human clears a veto.

## The loop

1. **Gather.** Read the work under review plus the constitution and standard.
2. **Adversary review.** Spawn the `privacy-adversary` agent. Give it the work, the
   constitution, and the standard. It reviews blind — it does not see the
   worker's rationale.
3. **Verdict.** The adversary returns KICK_BACK or ALLOW with findings.
4. **Gate.** If the verdict is KICK_BACK with a BLOCKER or a veto, the work
   returns to the worker to fix and resubmit. Only a human clears a veto.
5. **Record.** Append the verdict to `references/calibration-ledger.md`.

## Stateless skills

- `data-collection-audit`, `consent-check`, `retention-bound`, `subject-rights-check`, `transfer-lawfulness`.

## Rules

- The adversary never grades its own work.
- The record is append-only.
- Only a human clears a veto.

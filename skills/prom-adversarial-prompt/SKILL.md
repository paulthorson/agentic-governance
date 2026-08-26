---
name: prom-adversarial-prompt
description: The worker skill for the adversarial-prompt loop. Orchestrates a governed review of an instruction set: the prompt-adversary agent reviews blind, the constitution gates, and only a human clears a veto. Use when an instruction set (AGENTS.md, system prompt, skill, plugin manifest) needs an adversarial pass.
---

# Adversarial Prompt — Worker Skill

This is the orchestration loop for reviewing an instruction set. It mirrors
the adversarial-ux loop: a worker produces, the adversary reviews blind, the
constitution gates, and only a human clears a veto.

## The loop

1. **Gather.** Read the instruction set under review (AGENTS.md, system
   prompt, SKILL.md, plugin.json, or any combination) plus the constitution
   and standard.
2. **Adversary review.** Spawn the `prompt-adversary` agent. Give it the
   instruction set, the constitution, and the standard. It reviews blind —
   it does not see the worker's rationale.
3. **Verdict.** The adversary returns KICK_BACK or ALLOW with findings.
4. **Gate.** If the verdict is KICK_BACK with a BLOCKER or a veto, the work
   returns to the worker to fix and resubmit. Only a human clears a veto.
5. **Record.** Append the verdict to `references/calibration-ledger.md`.

## Stateless skills

- `prompt-injection-scan` — scan for injected instructions.
- `instruction-drift-check` — compare against the constitution.
- `safety-override-scan` — flag weakened safety guarantees.

## Rules

- The adversary never grades its own work.
- The record is append-only.
- Only a human clears a veto.

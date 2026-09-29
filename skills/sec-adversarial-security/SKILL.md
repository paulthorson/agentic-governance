---
name: sec-adversarial-security
description: The worker skill for the adversarial-security loop. Orchestrates a governed security review: the security-adversary agent reviews blind, the constitution gates, and only a human clears a veto. Use when a change touches security-sensitive surface.
---

# Adversarial Security — Worker Skill

This is the orchestration loop for reviewing a change for security risk. It
mirrors the adversarial-ux loop: a worker produces, the adversary reviews
blind, the constitution gates, and only a human clears a veto.

## The loop

1. **Gather.** Read the change under review (code, config, infra, dependency
   list) plus the constitution and standard.
2. **Adversary review.** Spawn the `security-adversary` agent. Give it the
   change, the constitution, and the standard. It reviews blind — it does not
   see the worker's rationale.
3. **Verdict.** The adversary returns KICK_BACK or ALLOW with findings.
4. **Gate.** If the verdict is KICK_BACK with a BLOCKER or a veto, the work
   returns to the worker to fix and resubmit. Only a human clears a veto.
5. **Record.** Append the verdict to `references/calibration-ledger.md`.

## Stateless skills

- `vuln-scan` — scan for exploitable vulnerabilities.
- `secret-exposure-scan` — scan for exposed/committed secrets.
- `supply-chain-check` — check dependencies for risk.
- `data-protection-check` — check sensitive-data handling.

## Rules

- The adversary never grades its own work.
- The record is append-only.
- Only a human clears a veto.

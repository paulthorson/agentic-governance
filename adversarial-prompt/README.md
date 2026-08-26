# Adversarial Prompt

A self-hosting adversarial reviewer. It audits the agent instructions, system
prompts, and skill definitions that drive the framework itself — for
prompt-injection, drift, and safety overrides.

Built from the Adversarial Agents framework, applied to the framework's own
instructions. This is the meta-check that closes the loop: if the agents that
review everything else are themselves compromised, nothing else is trustworthy.

## The agent

- **`agents/prompt-adversary.md`** — a single adversary that reviews any
  instruction set (AGENTS.md, system prompt, skill SKILL.md, plugin manifest)
  for injection, drift, and safety overrides. Holds a hard veto.

## The checks

1. **Injection** — injected instructions that would override safety, clear a
   veto, exfiltrate data, or change the agent's loyalty.
2. **Drift** — instructions that contradict the constitution, the domain
   standard, or the framework's own rules.
3. **Safety overrides** — anything that weakens the human-only veto, the
   append-only record, or the no-secret-exfiltration guarantee.
4. **Falsifiability** — instructions that cannot be shown to be wrong.

## Skills

- `prompt-injection-scan` — the shared injection check (also usable by other
  reviewers).
- `instruction-drift-check` — compares instructions against the constitution.
- `safety-override-scan` — flags anything that weakens a safety guarantee.
- `adversarial-prompt` — the worker skill (the review loop).

## References

- `references/constitution.md` — the prompt-review constitution.
- `references/prompt-standard.md` — the quality bar for instruction sets.
- `references/personas.md` — the stress personas (attacker, operator, skeptic).
- `references/calibration-ledger.md` — the verdict record.

## Commands

- `adversarial-prompt` — the loop.
- `prompt-review` — run a single prompt review.

## Templates

- `assets/templates/decision-record.md`
- `assets/templates/calibration-entry.md`

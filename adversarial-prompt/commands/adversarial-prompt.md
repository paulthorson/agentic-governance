# Adversarial Prompt

Run the adversarial-prompt loop on an instruction set.

## Usage

```
/adversarial-prompt <path-to-instruction-set>
```

## What it does

1. Reads the instruction set (AGENTS.md, system prompt, SKILL.md, plugin.json).
2. Spawns the `prompt-adversary` agent to review it blind.
3. Returns a KICK_BACK or ALLOW verdict with findings.
4. Records the verdict to the calibration ledger.

## Rules

- The adversary never grades its own work.
- Only a human clears a veto.
- The record is append-only.

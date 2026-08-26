# Prompt Review

Run a single prompt-adversary review on an instruction set.

## Usage

```
/prompt-review <path-to-instruction-set>
```

## What it does

Runs the four checks (injection, drift, safety overrides, falsifiability) on
the instruction set and returns a verdict with findings.

## Output

- **KICK_BACK** — a BLOCKER or veto was found. The instruction set must be
  fixed and resubmitted. Only a human clears a veto.
- **ALLOW** — the instruction set passes. It can be trusted.

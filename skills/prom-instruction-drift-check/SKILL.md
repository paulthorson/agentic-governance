---
name: prom-instruction-drift-check
description: Stateless skill. Compares an instruction set against the framework's constitution and domain standard to detect drift — instructions that contradict the governing rules or weaken the quality bar. Returns drift findings with severity.
---

# Instruction-Drift Check

Compare an instruction set against the framework's constitution and the
domain standard. Drift is any instruction that contradicts the governing rules
or weakens the quality bar.

## What to look for

1. **Constitutional contradiction** — an instruction that contradicts a
   constitutional rule (e.g. "you may clear a blocker if the author explains a
   deadline" contradicts the human-only veto).
2. **Standard contradiction** — an instruction that contradicts the domain
   standard's quality bar.
3. **Internal inconsistency** — two instructions that contradict each other.
4. **Silent weakening** — an instruction that weakens a rule without stating
   it (e.g. a veto that can be downgraded by the author).

## Method

1. Read the instruction set, the constitution, and the standard.
2. For each instruction, ask: does this contradict a constitutional rule or the
   standard? If yes, it is a drift finding.
3. Check for internal contradictions between instructions.
4. Look for silent weakenings — instructions that erode a guarantee without
   naming the trade-off.

## Output

```
## Drift findings
- <the instruction> | Contradicts: <constitution rule / standard> | Severity: BLOCKER/CONCERN/NOTE
  What would clear it: <the specific change>
```

A BLOCKER drift (direct constitutional contradiction) is a veto: only a human
clears it.

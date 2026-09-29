---
name: complexity-analysis
description: Map cyclomatic, coupling, and state-space hotspots in a proposed change, without a verdict, so the Critic can check maintainability against facts.
argument-hint: "<the change or diff>"
---

# Complexity Analysis

Produce a hotspot inventory. Input in, artifact out. No verdict on whether the code is good.

## Output

1. **Cyclomatic hotspots** — functions/branches with high decision density.
2. **Coupling hotspots** — modules with many or hidden dependencies.
3. **State-space hotspots** — code with many reachable states, where a state transition could
   be missed.
4. **Testability signal** — where the structure makes testing hard, with the reason.
5. **What could not be measured** — code you could not inspect, named.

```
## COMPLEXITY ANALYSIS

| Kind | Location | What is dense | Why it matters | Test gap |
|---|---|---|---|---|

### State transitions
- <state machine or stateful paths, and whether every state has an exit>

### Not measurable
- <what you could not measure, and why>
```

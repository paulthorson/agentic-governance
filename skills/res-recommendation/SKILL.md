---
name: res-recommendation
description: Produce a recommendation that states its claim, its evidence, and the confidence it earns, without overstating.
argument-hint: "<the synthesis and the decision>"
---

# Recommendation

Pure artifact. No verdict beyond what the evidence supports.

## Output

1. **The decision** this informs (Rule 4).
2. **The recommendation** — the claim, plainly.
3. **The evidence** — what supports it, with sources.
4. **Confidence** — high / medium / low, and why it is not higher.
5. **What would raise confidence** — the evidence that would firm it up.
6. **The counter-case** — what would argue the other way, from the same evidence.

```
## RECOMMENDATION

### Decision this informs
- <decision>

### Recommendation
- <claim, plainly>

### Evidence
- <what supports it, sourced>

### Confidence
- <high/medium/low> — <why not higher>

### What would raise it
- <evidence that would firm it up>

### Counter-case from the evidence
- <what argues the other way>
```

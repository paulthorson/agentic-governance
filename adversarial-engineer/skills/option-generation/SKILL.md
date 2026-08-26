---
name: option-generation
description: Generate at least two distinct implementation options for an engineering problem, each with a "trades away X to get Y" sentence, without picking one.
argument-hint: "<the problem and constraints>"
---

# Option Generation

Produce a set of genuine options. Input in, artifact out. No pick.

## Rules

- Options must differ in **what they optimize** (Rule 2): speed vs correctness, simplicity vs
  capacity, low latency vs low cost, small surface vs features.
- Each option carries a trade-off sentence: "This option trades away X to get Y."
- If two options have the same X and the same Y, they are one option. Say so.
- Three layouts of one idea are not three options.

## Output

```
## OPTIONS

| Option | What it optimizes | Trades away | To get | Rough cost | Risk |
|---|---|---|---|---|---|
| A | <dimension> | <X> | <Y> | <est> | <high/med/low> |
| B | <dimension> | <X> | <Y> | <est> | <high/med/low> |
| C (if any) | <dimension> | <X> | <Y> | <est> | <high/med/low> |

### Why these differ (not variations)
- <for each pair, the differing optimization>

### Constraint tension (Rule 3)
- <which option is fastest/cheapest, and what it gives up — flagged for the human gate>
```

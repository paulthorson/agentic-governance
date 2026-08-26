---
name: qa-acceptance-criteria-parse
description: Turn acceptance criteria into testable conditions, naming the ambiguous ones so they are not silently treated as testable.
argument-hint: "<the acceptance criteria>"
---

# Acceptance Criteria Parse

Produce a testable-criteria artifact. No verdict on the product.

## Output

1. **Testable criteria** — each restated as an observable condition: "when <action>, then
   <observable result>, under <condition>".
2. **Ambiguous criteria** — phrases like "works well", "feels fast", "user-friendly", named as
   untestable and flagged for a human to reword.
3. **Missing criteria** — failure, empty, boundary, and irreversible states not covered by any
   criterion, named.

```
## TESTABLE CRITERIA

| # | Criterion (testable) | Observable result | Condition |
|---|---|---|---|

### Ambiguous (not testable)
- <phrase> → <suggested reword>

### Missing coverage
- <failure/boundary/irreversible path with no criterion>
```

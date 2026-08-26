---
name: regression-map
description: Map what a change could break that already worked, so the plan covers regressions, not just the new feature.
argument-hint: "<the change>"
---

# Regression Map

Pure inventory. No verdict.

## Output

1. **Affected existing behavior** — features, flows, and integrations the change touches.
2. **Dependencies** — things that consume or are consumed by the change.
3. **Regression risk** — per existing behavior: what could silently break.
4. **Suggested regression coverage** — what to test that already worked.

```
## REGRESSION MAP

| Existing behavior | Touched by change? | Could break if | Regression test? |
|---|---|---|---|

### Dependencies
- <consumers and providers, or "none">
```

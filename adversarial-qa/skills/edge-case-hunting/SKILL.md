---
name: edge-case-hunting
description: Enumerate the unusual inputs, states, and paths most likely to hide a defect, without a verdict.
argument-hint: "<the feature>"
---

# Edge-Case Hunting

Pure inventory. No verdict.

## Output

1. **Unusual inputs** — empty, maximum, unicode, extremely long, malformed, duplicated.
2. **Unusual states** — first load, expired session, two tabs, backgrounded, mid-flow timeout,
   re-entry.
3. **Race conditions** — double submission, concurrent edits, async ordering.
4. **Platform variance** — keyboard/screen-reader, reduced motion, small targets (for UI).

```
## EDGE CASES

| Kind | Input/state | What could break | Covered? |
|---|---|---|---|

### Races
- <double-submit / concurrent paths, or "none identified">
```

---
name: desk-research
description: State what is already known about a question, with the gaps named, without a verdict.
argument-hint: "<the question>"
---

# Desk Research

Pure inventory. No verdict.

## Output

1. **What is known** — findings with their sources (what, where, when, type).
2. **What is assumed** — beliefs with no source, named as assumptions.
3. **Gaps** — what nobody has established, and why it matters.
4. **Sources consulted** — the list, with type and date.
5. **Not researched** — avenues you did not pursue, named.

```
## DESK RESEARCH

### Known (sourced)
- <finding> — <source | type | date>

### Assumed (unsourced, labeled)
- <assumption>

### Gaps
- <gap | why it matters>

### Sources consulted
- <list>

### Not researched
- <what you did not cover>
```

## `RESEARCH_BEFORE_ENHANCE` (Rule 2 A)

For UI enhancement work: named sensor `cite-real-screens` is fail-closed. Required artifact
`docs/epics/<slug>/evidence.md` (or stills index) must list real-screen source URLs and what
the pixels show **before** PM hands brief to UX / before first story. Soft / deferred Look gate
is REJECTED. When the pack hits adversarial UX, `ADV_COMP_CRITIQUE` also applies (jury opens
screens; comps are not gospel). Scar SoT (docs only):
`projects/_standing/scars/research-before-enhance.md`.

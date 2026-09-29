---
name: eng-constraint-elicitation
description: Elicit the non-negotiable constraints on an engineering change (performance, budget, stack, ops, security) and their owners, so a fast-path can never silently win.
argument-hint: "<the change>"
---

# Constraint Elicitation

Produce a constraint list. Input in, artifact out. No verdict on whether the change is feasible.

## Output

1. **Non-negotiables** — for each: the constraint, who owns it, and how it would be verified.
   Categories: performance, budget/cost, stack/compatibility, operations/uptime, security,
   compliance.
2. **Soft constraints** — things that can bend, and who can bend them.
3. **Unowned constraints** — constraints with no named owner, flagged as such.

```
## CONSTRAINTS

| # | Constraint | Category | Owner | Violated if | Negotiable? |
|---|---|---|---|---|---|
| C1 | <constraint> | <cat> | <owner> | <condition> | no / yes |

### Unowned / unstated
- <constraints implied but not owned, or "none">

### Cost / schedule pressures (Rule 3)
- <any pressure to ship faster or cheaper, and who applies it, or "none stated">
```

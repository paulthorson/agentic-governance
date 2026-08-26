---
name: univ-ethical-harm-check
description: Stateless skill. Checks a change for ethical and broader-harm risk beyond user-harm — bias, manipulation, deception, environmental or societal impact. Returns ethical findings with severity.
---

# Ethical / Harm Check

Check a change for ethical and broader-harm risk beyond direct user-harm. This
is the shared check that any reviewer can run — not just the universal
adversary.

## What to look for

1. **Bias** — a change that disadvantages a group (race, gender, age, ability,
   class) without justification.
2. **Manipulation** — dark patterns, deceptive defaults, or coercion.
3. **Deception** — a change that misleads users or stakeholders.
4. **Societal impact** — a change with broad negative externalities.
5. **Environmental impact** — a change with significant resource or energy
   cost.

## Method

1. Read the change in full.
2. Identify who is affected, directly and indirectly.
3. Check for bias, manipulation, deception, and broad externalities.
4. Assign severity based on the reach and reversibility of the harm.

## Output

```
## Ethical findings
- <the issue> | Affected: <who is harmed> | Severity: BLOCKER/CONCERN/NOTE
  What would clear it: <the specific change>
```

A BLOCKER ethical finding (irrecoverable or broad harm) is a veto: only a human
clears it.

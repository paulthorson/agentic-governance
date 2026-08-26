---
name: comp-audit-trail-check
description: Stateless skill. Checks whether there is a record of decisions Returns findings with severity.
---

# Audit Trail Check

Checks whether there is a record of decisions This is the shared check that any reviewer can run.

## Method

1. Read the work in full.
2. Apply the check to the work.
3. Assign severity (BLOCKER/CONCERN/NOTE) to each finding.

## Output

```
## Findings
- <finding> | Severity: BLOCKER/CONCERN/NOTE | What would clear it
```

A BLOCKER finding is a veto: only a human clears it.

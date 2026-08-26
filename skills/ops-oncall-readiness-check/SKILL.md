---
name: ops-oncall-readiness-check
description: Stateless skill. Checks whether an operator can diagnose and fix it under pressure Returns findings with severity.
---

# Oncall Readiness Check

Checks whether an operator can diagnose and fix it under pressure This is the shared check that any reviewer can run.

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

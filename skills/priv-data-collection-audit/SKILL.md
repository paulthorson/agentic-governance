---
name: priv-data-collection-audit
description: Stateless skill. Audits what personal data is collected and whether it is necessary Returns findings with severity.
---

# Data Collection Audit

Audits what personal data is collected and whether it is necessary This is the shared check that any reviewer can run.

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

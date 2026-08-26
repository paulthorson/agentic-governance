---
name: univ-risk-scan
description: Rank the failure modes of a proposal by likelihood and irrecoverability, without a verdict.
argument-hint: "<the proposal>"
---

# Risk Scan

Pure inventory. No verdict.

## Output

1. **Failure modes** — each with likelihood (high/med/low) and irrecoverability (yes/no).
2. **Irrecoverable** — anything that cannot be undone, flagged for the human gate (Rule 1).
3. **Silent failures** — where the system or party would not know it went wrong.

```
## RISK SCAN

| Failure mode | Likelihood | Impact | Irrecoverable? | Detected how |
|---|---|---|---|---|

### Irrecoverable
- <item> | <what cannot be undone>

### Silent
- <failure with no detection path>
```

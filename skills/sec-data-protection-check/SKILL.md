---
name: sec-data-protection-check
description: Stateless skill. Checks sensitive-data handling — encryption at rest and in transit, retention bounds, insecure transmission. Returns data-protection findings with severity.
---

# Data-Protection Check

Check how a change handles sensitive data. This is the shared check that any
reviewer can run — not just the security-adversary.

## What to look for

1. **Unencrypted at rest** — sensitive data (PII, credentials, financial)
   stored in plaintext.
2. **Unencrypted in transit** — sensitive data transmitted without TLS or
   equivalent.
3. **Over-retention** — sensitive data kept longer than needed.
4. **Insecure handling** — sensitive data logged, copied, or exposed
   unnecessarily.

## Method

1. Read the change in full.
2. Identify where sensitive data is stored, transmitted, and retained.
3. Check for encryption at rest and in transit, and bounded retention.

## Output

```
## Data-protection findings
- <the data> | Risk: <unencrypted/over-retained/insecure transit> | Severity: BLOCKER/CONCERN/NOTE
  What would clear it: <encrypt / bound retention / secure transit>
```

A BLOCKER data-protection finding (sensitive data exposed) is a veto: only a
human clears it.

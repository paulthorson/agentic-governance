---
name: sec-secret-exposure-scan
description: Stateless skill. Scans a change for exposed or committed secrets — credentials, keys, tokens, passwords in code, config, logs, or git history. Returns secret findings with severity.
---

# Secret-Exposure Scan

Scan a change for exposed or committed secrets. This is the shared check that
any reviewer can run — not just the security-adversary.

## What to look for

1. **Hardcoded secrets** — credentials, keys, tokens, passwords in code.
2. **Plaintext config secrets** — secrets in config files without a
   SecretRef / env-var indirection.
3. **Log exposure** — secrets written to logs or output.
4. **Git history** — secrets committed in past commits.

## Method

1. Read the change in full (code, config, logs, and git history if available).
2. Look for secret patterns: `api_key`, `secret`, `token`, `password`,
   `BEGIN PRIVATE KEY`, long base64/hex strings, `AKIA` (AWS), `sk-` (OpenAI),
   etc.
3. Look for secrets in config that should be env-var or SecretRef indirection.
4. Check git history for committed secrets.

## Output

```
## Secret findings
- <the secret> | Location: <code/config/log/history> | Severity: BLOCKER/CONCERN/NOTE
  What would clear it: <rotate + remove + scrub history>
```

A BLOCKER secret exposure is a veto: only a human clears it.

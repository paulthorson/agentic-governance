---
name: security-review
description: Produce security findings against a stated baseline, with what was not checkable, without a verdict on overall security posture.
argument-hint: "<the change and the security baseline>"
---

# Security Review

Produce a findings inventory. Input in, artifact out. No overall verdict (the Critic and Ops
Advocate grade).

## Output

1. **Findings** — each with severity (CRITICAL | HIGH | MEDIUM | LOW | INFO), where, and what
   to check.
2. **Secrets** — anywhere a secret could be present (code, config, logs, git history), named.
3. **Boundary validation** — every untrusted input and whether it is validated.
4. **Not checkable** — what the baseline does not cover (no security baseline, no SAST, no
   dependency audit), named.

```
## SECURITY REVIEW

| # | Severity | Finding | Where | Fix |
|---|---|---|---|---|

### Secret scan
- <what was checked and what was found, or "none">

### Boundary inputs
| Input | Source | Validated? | Where |
|---|---|---|---|

### Not checkable
- <no baseline, no tooling, no access — say so>
```

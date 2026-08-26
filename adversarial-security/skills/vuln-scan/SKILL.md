---
name: vuln-scan
description: Stateless skill. Scans a change for exploitable vulnerabilities — injection, RCE, privilege escalation, auth bypass, insecure deserialization. Returns vulnerability findings with severity.
---

# Vulnerability Scan

Scan a change for exploitable vulnerabilities. This is the shared check that
any reviewer can run — not just the security-adversary.

## What to look for

1. **Injection** — SQL, command, template, or prompt injection. Untrusted
   input reaching a dangerous code path.
2. **Remote code execution** — untrusted input reaching a code path that
   executes it.
3. **Privilege escalation** — a path from low to high privilege.
4. **Auth bypass** — a way around authentication or authorization.
5. **Insecure deserialization** — untrusted data deserialized unsafely.

## Method

1. Read the change in full.
2. Trace untrusted input (user input, network, files, env) to where it is
   used. If it reaches a dangerous sink (query, command, eval, deserialize,
   auth check), it is a finding.
3. Look for missing input validation, missing auth checks, and unsafe
   deserialization.

## Output

```
## Vulnerability findings
- <the flaw> | Attack path: <how it is exploited> | Severity: BLOCKER/CONCERN/NOTE
  What would clear it: <the specific fix>
```

A BLOCKER vulnerability is a veto: only a human clears it.

---
name: sec-supply-chain-check
description: Stateless skill. Checks a dependency tree for supply-chain risk — unverified sources, floating versions, known CVEs, untrusted registries. Returns supply-chain findings with severity.
---

# Supply-Chain Check

Check a dependency tree for supply-chain risk. This is the shared check that
any reviewer can run — not just the security-adversary.

## What to look for

1. **Unverified sources** — dependencies from unmaintained or unknown
   registries, mirrors, or direct URLs.
2. **Floating versions** — `latest`, `*`, or unpinned ranges (floating = risk).
3. **Known CVEs** — dependencies with known critical vulnerabilities.
4. **Untrusted provenance** — packages with no maintainer, no audit, or
   suspicious publish history.

## Method

1. Read the dependency list (package.json, requirements.txt, go.mod, SBOM,
   etc.).
2. For each dependency, check: source, version pinning, known CVEs, and
   provenance.
3. Flag floating versions and untrusted sources.

## Output

```
## Supply-chain findings
- <the dependency> | Risk: <CVE/unverified/floating/untrusted> | Severity: BLOCKER/CONCERN/NOTE
  What would clear it: <pin version / switch source / update>
```

A BLOCKER supply-chain finding (critical CVE or untrusted source) is a veto:
only a human clears it.

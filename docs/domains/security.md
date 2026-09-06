# Security Domain — deep dive

**Plugin:** `adversarial-security/` · **Veto:** vulnerabilities, secret exposure, supply chain

## What it reviews

Code, config, infrastructure, and dependencies for security risk. A dedicated
security reviewer (previously folded into Engineer).

## Adversary agents

| Agent | Role |
|---|---|
| `security-adversary` | The single reviewer — audits for vulnerabilities, secret exposure, supply-chain risk, and data protection |

## The checks

- **Vulnerability scan** — known vulnerabilities in the change?
- **Secret exposure scan** — any credentials/keys leaked?
- **Supply-chain check** — dependencies, SBOM, provenance?
- **Data-protection check** — is sensitive data handled safely?

## Skills

`sec-vuln-scan`, `sec-secret-exposure-scan`, `sec-supply-chain-check`,
`sec-data-protection-check`, `sec-adversarial-security` (worker).

## Constitution / veto

The security constitution gates on **vulnerabilities, secret exposure, and
supply-chain risk** — a change that introduces any of these is kicked back. Only
a human clears a veto.

## How to use

```
Use the governance server to run a review of this change in the security domain:
<your change>
```

## See also

- [[Domains]] · [[Architecture]] · [[Constitution]]

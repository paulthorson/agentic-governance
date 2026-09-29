# Security Standard

The quality bar for a change to pass security adversarial review.

## Required inputs

A change must carry, or reference, each of these. A missing input is a finding
(UNVERIFIABLE for the checks it would support).

| Input | Purpose | Supports check |
|-------|---------|-----------------|
| `code` / `diff` | The change under review | Vulnerability, secrets |
| `config` | The configuration surface | Secrets, data protection |
| `dependencies` / `SBOM` | The dependency tree | Supply chain |
| `deployment` / `infra` | The deployment surface | Data protection, exposure |

## Quality bar

1. **No exploitable vulnerabilities.** No injection, RCE, privilege
   escalation, auth bypass, or insecure deserialization.
2. **No secrets.** No credentials, keys, tokens, or passwords in code, config,
   logs, or git history.
3. **Trusted, pinned dependencies.** Every dependency from a trusted source,
   pinned to a known-good version, no known critical CVEs.
4. **Protected data.** Sensitive data encrypted at rest and in transit,
   retained only as long as needed.
5. **Complete.** No required input is missing or UNVERIFIABLE without a stated
   reason.

## Severity mapping

- **BLOCKER** — exploitable vulnerability, exposed secret, critical-CVE
  dependency, or sensitive-data exposure.
- **CONCERN** — real but recoverable, or a hardening worth naming.
- **NOTE** — would fix if free.

## Veto conditions

- An exploitable vulnerability (injection, RCE, privilege escalation, auth
  bypass).
- A secret exposed or committed.
- A dependency with a known critical CVE or from an untrusted source.
- Sensitive data exposed or mishandled.

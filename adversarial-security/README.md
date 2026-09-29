# Adversarial Security

A dedicated security adversarial reviewer. It audits code, configuration,
infrastructure, and dependencies for vulnerabilities, secret exposure, and
supply-chain risk — with a hard veto that only a human can clear.

Built from the Adversarial Agents framework, applied to security. This is a
standalone reviewer (security was previously folded into the Engineer domain)
so security gets its own constitution, standard, and veto.

## The agent

- **`agents/security-adversary.md`** — a single adversary that reviews any
  change for security risk. Holds a hard veto for vulnerabilities, secret
  exposure, and supply-chain risk.

## The checks

1. **Vulnerability** — exploitable flaws (injection, RCE, privilege
   escalation, auth bypass).
2. **Secret exposure** — credentials, keys, tokens in code, config, logs, or
   git history.
3. **Supply chain** — dependency risk, unverified sources, known CVEs.
4. **Data protection** — sensitive data handling, encryption, retention.

## Skills

- `vuln-scan` — the vulnerability check.
- `secret-exposure-scan` — the secret/credential check.
- `supply-chain-check` — the dependency/SBOM check.
- `data-protection-check` — the sensitive-data check.
- `adversarial-security` — the worker skill (the review loop).

## References

- `references/constitution.md` — the security-review constitution.
- `references/security-standard.md` — the security quality bar.
- `references/personas.md` — the stress personas (attacker, operator, skeptic).
- `references/calibration-ledger.md` — the verdict record.

## Commands

- `adversarial-security` — the loop.
- `security-review` — run a single security review.

## Templates

- `assets/templates/decision-record.md`
- `assets/templates/calibration-entry.md`

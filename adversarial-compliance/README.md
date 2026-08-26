# Adversarial Compliance

A dedicated compliance adversarial reviewer. Audits work against regulatory gates and policy requirements, with a hard veto that only a human can clear.

Built from the Adversarial Agents framework, applied to compliance.

## The agent

- **`agents/compliance-adversary.md`** — a single adversary that reviews compliance work.
  Holds a hard veto.

## The checks

1. **Regulatory gate** — does the work meet the applicable regulatory requirements.
2. **Policy alignment** — does the work align with stated policy.
3. **Evidence** — is there evidence the work is compliant.
4. **Audit trail** — is there a record of what was decided and why.
5. **Exposure** — what is the liability if the work is non-compliant.

## Skills

- `regulatory-gate-check` — Checks the work against applicable regulatory requirements.
- `policy-alignment-check` — Checks the work against stated policy.
- `compliance-evidence` — Checks whether there is evidence the work is compliant.
- `audit-trail-check` — Checks whether there is a record of decisions.
- `liability-scan` — Scans for liability exposure if non-compliant.
- `adversarial-compliance` — the worker skill (the review loop).

## References

- `references/constitution.md` — the compliance-review constitution.
- `references/compliance-standard.md` — the compliance quality bar.
- `references/personas.md` — the stress personas.
- `references/calibration-ledger.md` — the verdict record.

## Commands

- `adversarial-compliance` — the loop.
- `compliance-review` — run a single review.

## Templates

- `assets/templates/decision-record.md`
- `assets/templates/calibration-entry.md`

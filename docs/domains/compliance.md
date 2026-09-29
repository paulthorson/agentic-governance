# Compliance Domain — deep dive

**Plugin:** `adversarial-compliance/` · **Veto:** regulatory/policy violation, no evidence

## What it reviews

Regulatory and policy gates. A compliance reviewer that audits work against
regulatory requirements, policy alignment, evidence, audit trail, and liability.

## Adversary agents

| Agent | Role |
|---|---|
| `compliance-adversary` | The single reviewer — audits regulatory gates, policy alignment, evidence, audit trail, and liability |

## The checks

- **Regulatory-gate check** — does the change meet applicable regulations?
- **Policy-alignment check** — does it align with declared policy?
- **Compliance evidence** — is there evidence of compliance?
- **Audit-trail check** — is the decision traceable?
- **Liability scan** — does it create liability?

## Skills

`comp-regulatory-gate-check`, `comp-policy-alignment-check`,
`comp-compliance-evidence`, `comp-audit-trail-check`, `comp-liability-scan`,
`comp-adversarial-compliance` (worker).

## Constitution / veto

The compliance constitution gates on **regulatory/policy violation and missing
evidence** — a change that violates a regulation or policy, or lacks evidence
of compliance, is kicked back. Only a human clears a veto.

## How to use

```
Use the governance server to run a review of this change in the compliance domain:
<your change>
```

## See also

- [[Domains]] · [[Architecture]] · [[Constitution]]

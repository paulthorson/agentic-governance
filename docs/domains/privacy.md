# Privacy Domain — deep dive

**Plugin:** `adversarial-privacy/` · **Veto:** unlawful collection, no consent, unbounded retention

## What it reviews

Data handling, retention, consent, and subject rights. A GDPR/CCPA data-privacy
reviewer.

## Adversary agents

| Agent | Role |
|---|---|
| `privacy-adversary` | The single reviewer — audits data collection, consent, retention, subject rights, and cross-border transfer |

## The checks

- **Data-collection audit** — is data collected lawfully and minimally?
- **Consent check** — is consent obtained and documented?
- **Retention bound** — is data retained only as long as needed?
- **Subject-rights check** — can users access/delete their data?
- **Transfer lawfulness** — are cross-border transfers lawful?

## Skills

`priv-data-collection-audit`, `priv-consent-check`, `priv-retention-bound`,
`priv-subject-rights-check`, `priv-transfer-lawfulness`,
`priv-adversarial-privacy` (worker).

## Constitution / veto

The privacy constitution gates on **unlawful collection, no consent, and
unbounded retention** — a change that violates any of these is kicked back. Only
a human clears a veto.

## How to use

```
Use the governance server to run a review of this data handling in the privacy domain:
<your change>
```

## See also

- [[Domains]] · [[Architecture]] · [[Constitution]]

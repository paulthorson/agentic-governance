# Adversarial Data & Privacy

A dedicated data-privacy adversarial reviewer. Audits data handling, retention, and consent for GDPR/CCPA risk, with a hard veto that only a human can clear.

Built from the Adversarial Agents framework, applied to privacy.

## The agent

- **`agents/privacy-adversary.md`** — a single adversary that reviews privacy work.
  Holds a hard veto.

## The checks

1. **Data collection** — what personal data is collected and is it necessary.
2. **Consent** — is consent obtained and revocable.
3. **Retention** — is data retained only as long as needed.
4. **Data subject rights** — can users access, correct, or delete their data.
5. **Cross-border transfer** — is data transferred lawfully.

## Skills

- `data-collection-audit` — Audits what personal data is collected and whether it is necessary.
- `consent-check` — Checks whether consent is obtained, specific, and revocable.
- `retention-bound` — Checks whether data retention is bounded and justified.
- `subject-rights-check` — Checks whether users can access, correct, or delete their data.
- `transfer-lawfulness` — Checks whether cross-border data transfers are lawful.
- `adversarial-privacy` — the worker skill (the review loop).

## References

- `references/constitution.md` — the privacy-review constitution.
- `references/privacy-standard.md` — the privacy quality bar.
- `references/personas.md` — the stress personas.
- `references/calibration-ledger.md` — the verdict record.

## Commands

- `adversarial-privacy` — the loop.
- `privacy-review` — run a single review.

## Templates

- `assets/templates/decision-record.md`
- `assets/templates/calibration-entry.md`

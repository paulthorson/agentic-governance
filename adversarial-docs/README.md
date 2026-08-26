# Adversarial Documentation

A dedicated documentation adversarial reviewer. Audits docs, AGENTS files, and knowledge bases for accuracy, completeness, and usability, with a hard veto that only a human can clear.

Built from the Adversarial Agents framework, applied to docs.

## The agent

- **`agents/docs-adversary.md`** — a single adversary that reviews docs work.
  Holds a hard veto.

## The checks

1. **Accuracy** — is the documentation factually correct.
2. **Completeness** — is the documentation complete and current.
3. **Usability** — can a reader act on the documentation.
4. **Consistency** — is the documentation consistent with the system.
5. **Discoverability** — can a reader find what they need.

## Skills

- `doc-accuracy-check` — Checks whether documentation is factually correct.
- `doc-completeness-check` — Checks whether documentation is complete and current.
- `doc-usability-check` — Checks whether a reader can act on the documentation.
- `doc-consistency-check` — Checks whether documentation is consistent with the system.
- `doc-discoverability-check` — Checks whether a reader can find what they need.
- `adversarial-docs` — the worker skill (the review loop).

## References

- `references/constitution.md` — the docs-review constitution.
- `references/docs-standard.md` — the docs quality bar.
- `references/personas.md` — the stress personas.
- `references/calibration-ledger.md` — the verdict record.

## Commands

- `adversarial-docs` — the loop.
- `docs-review` — run a single review.

## Templates

- `assets/templates/decision-record.md`
- `assets/templates/calibration-entry.md`

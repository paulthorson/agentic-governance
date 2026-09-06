# Docs Domain — deep dive

**Plugin:** `adversarial-docs/` · **Veto:** wrong/missing/misleading docs

## What it reviews

Documentation, AGENTS files, and knowledge bases. A documentation reviewer that
audits accuracy, completeness, usability, consistency, and discoverability.

## Adversary agents

| Agent | Role |
|---|---|
| `docs-adversary` | The single reviewer — audits accuracy, completeness, usability, consistency, and discoverability |

## The checks

- **Doc-accuracy check** — is the documentation correct?
- **Doc-completeness check** — is anything missing?
- **Doc-usability check** — can a reader actually use it?
- **Doc-consistency check** — does it contradict other docs?
- **Doc-discoverability check** — can it be found?

## Skills

`doc-doc-accuracy-check`, `doc-doc-completeness-check`, `doc-doc-usability-check`,
`doc-doc-consistency-check`, `doc-doc-discoverability-check`,
`doc-adversarial-docs` (worker).

## Constitution / veto

The docs constitution gates on **wrong, missing, or misleading documentation** —
docs that mislead or omit critical information are kicked back. Only a human
clears a veto.

## How to use

```
Use the governance server to run a review of this documentation in the docs domain:
<your docs>
```

## See also

- [[Domains]] · [[Architecture]] · [[Constitution]]

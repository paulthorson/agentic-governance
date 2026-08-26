# Contributing

Thanks for helping build the Adversarial Agents framework. This is a small, personal project,
but if you're here, you care about making reviews rigorous and reproducible — that's the
spirit.

## Ground rules

1. **Preserve the blind-review isolation.** Never let a judge see the worker's rationale. This
   is the system's core invariant. A "helpful" context leak is a regression.
2. **Never clear a veto via an edit.** Constitutions and calibration ledgers are human-edited
   only. An agent proposes; a human applies.
3. **Keep records append-only.** Decision records are never rewritten.
4. **Namespacing + frontmatter.** New agents/skills must be domain-prefixed and carry a
   matching `name:` frontmatter field.
5. **Reuse `shared/`.** Add cross-cutting checks to `shared/skills/`, not per-plugin copies.
6. **Run the validator.** Before committing, run `scripts/validate.py` (or the CI workflow)
   and make sure it passes: frontmatter present + matching, naming unique, structure valid,
   cross-references resolve.

## Workflow

1. Fork / branch.
2. Make your change (a plugin, a shared check, a doc, an MCP tool, a test fixture).
3. Add or update tests under `tests/`.
4. Update `docs/` + the relevant ADR if you changed structure or behavior.
5. Run `scripts/validate.py`.
6. Update `CHANGELOG.md` under "Unreleased".
7. Open a PR with a clear description of the change and why.

## What makes a good contribution

- **A new domain plugin** (e.g. security, compliance): copy `adversarial-qa` as the template,
  give it a constitution + standard + advocate-with-veto + personas + calibration ledger, wire
  it into the consolidation map and docs.
- **A new cross-cutting check**: add it to `shared/skills/`, reference it from the reviewers
  that should run it, add a test fixture.
- **An MCP tool**: keep it read-only unless explicitly a write tool; document it in
  `docs/mcp.md`; add a unit test.
- **A fix to the loop**: update the ADR and explain the trade-off you changed.

## Getting help

Open an issue, or ping Paul (maintainer on Discord). If you found a security issue, use
`SECURITY.md` and do not open a public issue.

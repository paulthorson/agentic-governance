# Contributing

Thanks for helping with Agentic Governance. This is an unpaid personal project.
Care about rigorous, reproducible review — that is the spirit.

## Developer Certificate of Origin (DCO)

All commits must be signed off:

```bash
git commit -s
```

By signing off, you certify the Developer Certificate of Origin
(https://developercertificate.org/): you have the right to submit the
contribution under the project’s Apache-2.0 license.

## Ground rules

1. **Preserve blind-review isolation in artifacts.** Do not put worker rationale
   into `facts.md` or other judge-facing packets (`AGENTS.md`).
2. **Never clear a veto by editing a constitution or calibration ledger to force
   a pass.** Humans clear vetoes in decision records.
3. **Keep records append-only** (process): corrections are new entries.
4. **Namespacing + frontmatter.** New flat agents/skills must be domain-prefixed
   with matching `name:` frontmatter.
5. **Reuse `shared/`** for cross-cutting checks instead of duplicating per plugin.
6. **Plugin folders are source of truth.** After plugin edits, run
   `scripts/consolidate-adversarial.py` when regenerating flat layers.
7. **Do not invent enforcement.** If code does not refuse, docs must say advisory
   ([`docs/capability-report.md`](docs/capability-report.md)).
8. **Run validators.** `python3 scripts/validate.py` and `python3 -m pytest tests/ -q`.

## Workflow

1. Fork / branch from `main`.
2. Make a focused change.
3. Add or update tests under `tests/` (especially `tests/test_published_claims.py`
   if you change a published claim).
4. Update `docs/capability-report.md` when behavior changes.
5. Update `CHANGELOG.md` under Unreleased when appropriate.
6. Open a PR with `git commit -s` on each commit.

## What makes a good contribution

- A new domain plugin (copy `adversarial-qa`), wired through consolidation + docs
- A cross-cutting check in `shared/skills/`
- An MCP tool that stays honest about what it enforces
- Fixes that replace fake “enforcement” language with real gates or advisory text

## Security issues

Use [`SECURITY.md`](SECURITY.md). Do not open a public issue for vulnerabilities.

# Continuous improve reports

Daily markdown reports for Agentic Governance (AG) continuous improvement.
These are the public, plain-English record of what shipped, what we learned,
and which KPIs we can actually defend.

## Why this path exists

Governance only improves if improvement is visible and honest. Each day gets
one report under `docs/improve/YYYY-MM-DD.md`. The public dashboard (see
`dashboard/`) reads these files and surfaces them alongside the changelog and
a contribute CTA.

## How to write a report

1. Copy [`_template.md`](./_template.md).
2. Name the file `YYYY-MM-DD.md` for the calendar day the work covers.
3. Fill every section in plain English. Prefer short bullets over narrative.
4. Link related CHANGELOG entries and PRs when they exist.
5. Commit the report with the work it describes (or the next morning’s digest).

## KPI rules (non-negotiable)

**Never invent numbers.**

| Allowed | Not allowed |
|---|---|
| **Measured** — taken from a tool, ledger, CI, token bill, or timer with a named source | Round numbers guessed to “look complete” |
| **Method-estimated** — derived by a stated method (formula, sample, range) with the method written next to the number | Vague claims (“~faster”, “lots less tokens”) without a number *or* a method |
| **Unknown / baseline** — say so explicitly when there is no measurement yet | Filling KPI cells with placeholders that look like real data |

If a KPI is blank on a baseline day, leave it blank or write `not measured yet`.
Do not backfill fake history later.

### KPI fields we track

- **Tokens** — prompt/completion/total for AG runs, with source (e.g. provider bill, engine log).
- **Cycle time** — time from work start to allowed/merged (or veto cleared), with definition stated.
- **Retros** — count and links for post-epic retros actually held.
- **AG PRs** — PRs opened/merged that change governance itself (this repo).
- **Money** — optional. Only include when spend is attributed and sourced.

## Feedback and invites

- **Limen / engine feedback** — note what was sent upstream (issue, PR, message) so engine friction is not lost in chat.
- **Open contribution invites** — name concrete asks for outsiders (docs, harnesses, adapters), not generic “PRs welcome.”

## Related paths

- Template: [`_template.md`](./_template.md)
- Changelog: [`../../CHANGELOG.md`](../../CHANGELOG.md)
- Public dashboard: [`../../dashboard/`](../../dashboard/) (UI SoT = Meta Astryx)
- Admin (Google SSO): [`../../dashboard/`](../../dashboard/) `/admin/*` — see dashboard README for Vercel env + OAuth
- Traction gates: [`../../data/traction.json`](../../data/traction.json) — widgets stay hidden until Cos/Paul set measured values ≥ `minVisible`

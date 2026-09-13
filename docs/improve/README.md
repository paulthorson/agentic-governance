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

## Standing AG self-audit (`SELF_AUDIT_LOOP`)

**Draft SoT until Cos ACCEPT merge — not live / not effective until ACCEPT.** Soft “we
should…”, wiki tip, or scar-without-unpaid = **REJECTED**. SoT lives in
[`harnesses/chief-of-staff.md`](../../harnesses/chief-of-staff.md). **No new Auditor
persona.** Adv challenges Cos ACCEPT on that write (Adv does not write the unpaid plan).

**CoE ownership (Paul/Cos LOCK):** Teams file retros (feed) → Agentic Governance (framework
PM) drafts the named unpaid SoT/plan from retro+audit → Adv challenges the plan (does not
write it) → Cos ACCEPT → Teams absorb. Project PMs do **not** own harness writes.

When live, each Cos 6pm ET improve digest cycle must record **BOTH**:

1. A checklist vs live scars/locks (stills / `token_source` / retros / `LIVE_SOT` /
   `SURFACE_GATE` / Critic stamp), and
2. ≥1 named unpaid improve/SoT item (`id` + owner + metric) **OR** explicit `AUDIT_CLEAR`
   with evidence — drafted by AG (framework PM / CoE), not Adv, not a project PM.

Nag-only digests FAIL. This loop is an addition on the daily digest + `RETRO_BEFORE_CLOSE`,
not a replacement. Scope: AG harness + Cos improve / self-heal — not OpenClaw briefs. P0: no
secrets/keys/emails/PII/host paths in digest artifacts; no invented tokens.

## Related paths

- Template: [`_template.md`](./_template.md)
- Changelog: [`../../CHANGELOG.md`](../../CHANGELOG.md)
- Public dashboard: [`../../dashboard/`](../../dashboard/) (UI SoT = Meta Astryx)
- Admin (Google SSO): [`../../dashboard/`](../../dashboard/) `/admin/*` — see dashboard README for Vercel env + OAuth
- Traction gates: [`../../data/traction.json`](../../data/traction.json) — widgets stay hidden until Cos/Paul set measured values ≥ `minVisible`
- Cos harness SoT (`SELF_AUDIT_LOOP`): [`../../harnesses/chief-of-staff.md`](../../harnesses/chief-of-staff.md)

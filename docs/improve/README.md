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

### Draft lock: `TOKEN_SOURCE_OR_BLANK` (not live / not effective until Cos ACCEPT merge)

- **Id:** `TOKEN_SOURCE_OR_BLANK`
- **Slot:** Critic Check 1 Tokens + `adversarial-ux/references/design.md` `token_source` / this
  improve-digest path.
- **FAIL:** Check 1 PASSes while `token_source` UNSET; improve/report numbers lack a named
  source; tokens invented; blank treated as measured = FAIL.
- **Sensor:** Named source in the KPI table **or** explicit **BLANK** / `not measured yet`.
  Soft / tip / wiki-scar-only ≠ sensor.
- **Stack:** Does not invent a token feed or replace `RESEARCH_BEFORE_ENHANCE`.
- **Scope:** AG improve digests + product UX Critic Check 1; **not** OpenClaw.
- **Metric:** Improve reports with invented or blank-as-measured tokens = **fail closed**.
- **P0:** No secrets/keys/emails/PII/host paths in AG git.

| Allowed | Not allowed |
|---|---|
| **Measured** — taken from a tool, ledger, CI, token bill, or timer with a **named source** | Round numbers guessed to “look complete” |
| **Method-estimated** — derived by a stated method (formula, sample, range) with the method written next to the number | Vague claims (“~faster”, “lots less tokens”) without a number *or* a method |
| **BLANK / unknown / baseline** — say so explicitly (`BLANK`, `not measured yet`) when there is no measurement yet | Filling KPI cells with placeholders that look like real data; treating blank as measured |

If a KPI is blank on a baseline day, leave it blank, write `BLANK`, or write `not measured yet`.
Do not backfill fake history later. Token rows without a named source must be labeled **BLANK**.

### KPI fields we track

- **Tokens** — prompt/completion/total for AG runs, with **named source** (e.g. provider bill, engine log) **or** label **BLANK**. Invented or blank-as-measured = FAIL under `TOKEN_SOURCE_OR_BLANK` (draft until Cos ACCEPT).
- **Cycle time** — time from work start to allowed/merged (or veto cleared), with definition stated.
- **Retros** — count and links for post-epic retros actually held (`projects/<team>/retros/` under `RETRO_BEFORE_CLOSE`, draft until Cos ACCEPT).
- **AG PRs** — PRs opened/merged that change governance itself (this repo). Cite merged SHA when claiming live SoT (`LIVE_SOT_MERGED_SHA`, draft until Cos ACCEPT).
- **Money** — optional. Only include when spend is attributed and sourced.

## Feedback and invites

- **Limen / engine feedback** — note what was sent upstream (issue, PR, message) so engine friction is not lost in chat.
- **Open contribution invites** — name concrete asks for outsiders (docs, harnesses, adapters), not generic “PRs welcome.”

## Standing AG self-audit (`SELF_AUDIT_LOOP`)

**Draft SoT until Cos ACCEPT merge — not live / not effective until ACCEPT.** Soft “we
should…”, wiki tip, or scar-without-unpaid = **REJECTED**. SoT lives in
[`harnesses/chief-of-staff.md`](../../harnesses/chief-of-staff.md). **No new sidebar
persona.**

**Cos CoE ownership (operator/Cos LOCK; Adv confirm):** Team triad retro (feed) → AG seat drafts
named unpaid SoT/plan (`id` / owner / metric / AC; project PMs ≠ AG constitution) → Adv
challenges (does **not** author; `CRITIC_SEPARATE_STAMP`) → Cos ACCEPT → teams absorb next
ship. Sensor remains unpaid item or `AUDIT_CLEAR`.

When live, each Cos 6pm ET improve digest cycle must record **BOTH**:

1. A checklist vs live scars/locks (stills / `token_source` / retros / `LIVE_SOT` /
   `SURFACE_GATE` / Critic stamp), and
2. ≥1 named unpaid improve/SoT item (`id` + owner + metric + AC) **OR** explicit
   `AUDIT_CLEAR` with evidence — drafted by the AG seat, not authored by Adv, not written by
   a project PM into AG constitution/harness.

Nag-only digests FAIL. This loop is an addition on the daily digest + `RETRO_BEFORE_CLOSE`,
not a replacement. Scope: AG harness + Cos improve / self-heal — not OpenClaw briefs. P0: no
secrets/keys/emails/PII/host paths in digest artifacts; no invented tokens.

## Related paths

- Template: [`_template.md`](./_template.md)
- Changelog: [`../../CHANGELOG.md`](../../CHANGELOG.md)
- Public dashboard: [`../../dashboard/`](../../dashboard/) (UI SoT = declared product design system)
- Admin (Google SSO): [`../../dashboard/`](../../dashboard/) `/admin/*` — see dashboard README for Vercel env + OAuth
- Traction gates: [`../../data/traction.json`](../../data/traction.json) — widgets stay hidden until Cos/operator set measured values ≥ `minVisible`
- Cos harness SoT (`SELF_AUDIT_LOOP`): [`../../harnesses/chief-of-staff.md`](../../harnesses/chief-of-staff.md)
- Initiative epic (Anonymous Improve Feedback — PRD / feeds this digest): [`../initiatives/anonymous-improve-feedback.md`](../initiatives/anonymous-improve-feedback.md)

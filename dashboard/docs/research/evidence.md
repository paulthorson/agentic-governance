# ADV_COMP evidence — Public AG dashboard (`/`)

**Gate:** `RESEARCH_BEFORE_ENHANCE` + `ADV_COMP_CRITIQUE` 
**Cos GO:** 2026-09-13 — public dashboard FAIL on look; Research evidence SoT before Check 7/8 or Eng UI. 
**Ownership:** AG Research owns this pack. AG UX owns Check 7 (flows/JTBD) and Check 8 (stills) after — not in this PR. 
**Live surface audited:** https://agentic-governance-three.vercel.app 
**Scope:** ADV_COMP evidence for the public marketing+ops face only (not OpenClaw briefs, not admin SSO, not Check 7/8 artifacts).

---

## 1. Job / surface

Public `/` must read as a best-in-class ops/marketing face for Agentic Governance — KPI card system, real data viz, designed empty/baseline states — without inventing traction numbers or dumping internal Cos/improve MD as the hero.

---

## 2. Our current `/` holes (live copy audit)

Audited live copy on Cos GO day. No invented metrics.

- **Limp KPI tiles** — Mixed "Baseline" labels and raw counts (e.g. Gains `4`, Retros `2`, merged PRs `2`) without a consistent card chrome, sparklines, or secondary method line hierarchy.
- **Sparse chart** — "Improve trends (measured points only)" shows few measured points; null-day gaps read as broken rather than intentional product nulls.
- **Daily improve MD dump as hero** — Full dated `docs/improve/*.md` reports (Shipped / Gains / KPIs / Open invites) dominate the fold. Internal Cos/launch copy appears on the public face: "Cos unlocks", private-repo marketing aside, "Private today → public Vercel deploy is ready; flip repo/site visibility when Cos unlocks launch."
- **Traction gated correctly (keep)** — "5 metrics gated below threshold" is honest and must stay. Empty/baseline states for unpaid metrics are **not** designed as product (Baseline text only; no illustration, recovery path, or intentional null chrome).

---

## 3. Per-comp cite table (Mobbin — Adv must open these URLs)

| Comp | Mobbin | What pixels show | Strong | Delta vs our live `/` | Keep / adopt / do-not-copy |
| --- | --- | --- | --- | --- | --- |
| **Stripe Dashboard overview** | [Your overview KPI grid](https://mobbin.com/screens/673e89af-fe9e-4ab9-ac27-435dedf21888) | "Your overview" with Payments progress, Gross volume sparkline, New customers, Failed payments list, Top customers — modular KPI card grid. | Consistent card chrome; primary number + trend sparkline; secondary lists under the fold of the overview. | Our tiles are label+number without card system or sparklines; no secondary "method" line. | **Adopt** card chrome + sparkline vocabulary. **Do not copy** editable add/remove widget soup on a public marketing face. |
| **Stripe (also usable)** | [Radar / monitoring density](https://mobbin.com/screens/02176a39-e453-4570-af73-6af00fbe681b) | KPI percentage row + Manual reviews empty chart with intact axes + zeroed outcome table + "in good standing" status cards. | Designed zero: axes, tables, and status remain; 0 does not look broken. | Our Baseline tiles drop scaffolding; empty chart gaps feel accidental. | **Adopt** intact chart scaffolding for unpaid/zero. **Do not copy** fraud-ops density or editable programme chrome for public `/`. |
| **Vercel Analytics** | [Web Analytics low-volume](https://mobbin.com/screens/900542f7-c157-4445-8f88-d79dca719c7a) | Dark chrome; Visitors / Page Views / Bounce KPI row; primary line chart; Pages + Referrers tables. Hierarchy stays clear even with low counts (e.g. ~13 visitors). | KPI row → hero chart → detail tables; low counts still read as product. | Our sparse chart lacks companion tables and empty narrative; MD dump competes with KPIs. | **Adopt** KPI→chart→tables hierarchy and calm low-volume treatment. **Do not copy** assuming chart alone carries sparse days. |
| **Linear (Insights analog)** | [Project Overview + Progress rail](https://mobbin.com/screens/e88b6bd7-3d4b-4e1e-8cd7-a9d2a6852795) | Latest Update card + right-rail Progress (Scope / Started / Completed) + burn chart. | Narrative update is a **card**, not a full MD dump; progress KPIs sit in a rail with a small burn viz. | Our hero is full improve MD; progress is not summarized as product chrome. | **Adopt** Latest-Update-as-card + Progress rail pattern for improve health. **Note:** dedicated Linear Insights product screens were sparse in Mobbin; these are the closest Linear ops/insights analogs. |
| **Linear (timeline analog)** | [Timeline + milestones rail](https://mobbin.com/screens/c1cc22aa-69de-468c-b200-cf80f05ac1c7) | Timeline view with right-rail milestones / progress. | Ops density without turning the page into a report archive. | We surface full report bodies instead of timeline/milestone summary. | **Adopt** secondary rail for milestones/progress. **Do not copy** workspace-logged-in chrome as the public marketing shell. |
| **Mixpanel empty** | [Select Event or Cohort](https://mobbin.com/screens/bef3e439-48d3-42de-9b9d-d8f6eb6ff2cd) | Designed empty: illustration + "Select an Event or Cohort to get started" + next-step links (Insights Basics / Examples). | Empty is a product moment with recovery links. | Our unpaid metrics show "Baseline" text only. | **Adopt** illustration + next-step recovery for unpaid/baseline. **Do not copy** logged-in query-builder assumptions on public `/`. |
| **Amplitude empty** | [No data matches](https://mobbin.com/screens/1c4908e9-c1e6-4ed7-97f2-a757099c5462) | "Oops! No data matches…" with recovery guidance. | Honest no-match + how to recover. | Baseline lacks recovery narrative. | **Adopt** recovery copy pattern. **Do not copy** query-builder empty UX as public marketing IA. |
| **Mixpanel board empty** | [Add to Board / Use a Template](https://mobbin.com/screens/194a56e8-d5e0-4349-8353-cf7a6cc25bbf) | Board empty with Add to Board / Use a Template cards. | Empty filled with constructive next actions, not blank chrome. | Traction-gated section has no designed empty product path. | **Adopt** template/next-action cards for gated traction. **Do not copy** board-editor affordances on marketing `/`. |
| **Amplitude home** | [KPI cards + templates](https://mobbin.com/screens/7ebf30d2-b1ea-4c85-b123-76f4347ba357) | Home with KPI cards (+ deltas), primary chart, template gallery, structured empty tables. | Product face even at low volume; templates as designed baseline filler. | No template/gallery or consistent KPI chrome; MD hero instead. | **Adopt** KPI card system + template/next-step gallery beneath measured KPIs. **Do not copy** inventing visitors/revenue to fill charts. |
| **Better Stack (Datadog equal)** | [Reporting Overview](https://mobbin.com/screens/d4ecfb68-a860-41f6-9dc4-93f1b027c7c9) | Hero incident chart, KPI row (Incidents / MTTR / MTTA), detail table. Ops density without scaffolding. | Hero is a **chart**, not a document dump; KPIs + table reinforce. | Our hero is improve MD; chart is secondary and sparse. | **Adopt** chart-as-hero + KPI row + detail table. **Do not copy** dark internal ops chrome wholesale for public marketing. **Note:** Datadog itself not in Mobbin catalog; Cos allowed Datadog-equal. |
| **Neon (Datadog equal)** | [Monitoring — Endpoint inactive](https://mobbin.com/screens/a140f8f1-d12e-407f-81c8-e06186ce5350) | Monitoring with diagonal hatch for "Endpoint inactive" — honest designed empty. | Null/inactive is a **designed pattern** (hatch), not missing pixels. | Our chart gaps look accidental; Baseline is text-only. | **Adopt** intentional null patterning (hatch / labeled inactive). **Do not copy** inventing filled series. |
| **Cloudflare Workers** | [Workers Overview](https://mobbin.com/screens/c2a81c26-677d-43c2-8f93-3fad6513e3bd) | Requests / Errors / CPU KPI cards with sparklines + architecture diagram + next-steps rail. | KPI+sparkline card system; zero Errors still looks intentional; next-steps fill density. | Our KPIs lack sparklines and next-step rail; architecture of AG is buried under MD. | **Adopt** sparkline KPI cards + next-steps rail. **Do not copy** full infra console IA for a marketing+ops face. |

### Linear Insights note (explicit)

Dedicated Linear **Insights** product screens were sparse in Mobbin at pull time. The two Linear cites above are the closest **ops / progress / insights analogs** (project Overview + Progress rail; timeline + milestones). Adv should open those URLs and treat them as analogs, not as the Insights product surface itself.

---

## 4. our-hole

- Hero is report dump not product face — full daily improve MD (Shipped/Gains/Open invites) owns the fold.
- KPI tiles lack consistent card chrome, sparklines, and a source/method secondary line.
- Chart gaps look broken rather than intentional nulls (no hatch/labeled inactive pattern).
- Internal Cos / unlock / private-repo copy on the public marketing surface.
- No designed empty for unpaid/baseline metrics (Baseline text only; traction gate is correct but empty UX is not productized).

---

## 5. competitor-hole

- Stripe overview can feel widget-soup / editable clutter — fine for logged-in ops, wrong for public marketing.
- Vercel Analytics low-volume still looks sparse (single spike) — chart alone is not enough without empty narrative.
- Mixpanel / Amplitude empty states assume a logged-in query builder — not a public marketing visitor.
- Better Stack dark ops chrome may be too internal for a public marketing face.
- Linear project pages are workspace-logged-in, not public marketing.

---

## 6. do-not-copy

- Editable dashboard soup (Stripe add/remove widgets) on public marketing `/`.
- Fake filled charts or invented visitors / revenue / token / money numbers.
- Dumping full MD reports as the fold hero.
- Internal launch language ("Cos unlocks", private-repo asides) on the public face.
- Component-gallery Astryx demos without product IA (Meta Astryx is UI SoT; the page must still be a product face, not a kit demo).

---

## 7. Motion / delight (evidence for UX Check 8 — not Eng yet)

Observed from opened comps; AG UX translates into Check 8 stills. No Eng motion in this PR.

| Intent | Evidence cue | Mobbin cite | Adopt / do-not-copy |
| --- | --- | --- | --- |
| Presence on load | KPI cards and chart scaffolding appear as a composed product face even at zero/low volume — hierarchy reads before numbers do. | [Stripe overview](https://mobbin.com/screens/673e89af-fe9e-4ab9-ac27-435dedf21888), [Amplitude home](https://mobbin.com/screens/7ebf30d2-b1ea-4c85-b123-76f4347ba357) | **Adopt** staged reveal of card chrome → chart → secondary rail. **Do not copy** bounce/glow noise or fake count-up to invented totals. |
| Honest null delight | Diagonal hatch / labeled inactive and illustrated empty with next-step links turn absence into a designed moment. | [Neon inactive hatch](https://mobbin.com/screens/a140f8f1-d12e-407f-81c8-e06186ce5350), [Mixpanel empty](https://mobbin.com/screens/bef3e439-48d3-42de-9b9d-d8f6eb6ff2cd) | **Adopt** hatch or labeled inactive for unpaid/baseline; illustration + recovery links. **Do not copy** query-builder empty as public marketing. |
| Ops pulse without hype | Sparklines and small burn charts give temporal pulse without requiring hero animation or invented series. | [Cloudflare Workers](https://mobbin.com/screens/c2a81c26-677d-43c2-8f93-3fad6513e3bd), [Linear Progress rail](https://mobbin.com/screens/e88b6bd7-3d4b-4e1e-8cd7-a9d2a6852795) | **Adopt** quiet sparkline/burn motion tied to measured points only. **Do not copy** editable widget rearranging as delight. |
| Low-volume calm | Dark/light analytics chrome keeps KPI→chart→tables readable when counts are tiny (~13 visitors). | [Vercel Analytics](https://mobbin.com/screens/900542f7-c157-4445-8f88-d79dca719c7a) | **Adopt** calm hierarchy that does not apologize for low volume. **Do not copy** filling gaps to look “alive.” |

---

## 8. Keep / adopt for Meta Astryx product face (not component demo)

**Keep (locked honesty):**

- Traction gate via `data/traction.json` — hide below-threshold metrics; never invent.
- Measured-points-only improve trends — null days stay gaps (but must look intentional).
- Primary CTA toward Get AG / GitHub (public distribution), once Cos clears public marketing copy.
- UI implementation SoT remains Meta Astryx (`@astryxdesign/core` + theme-neutral) — after Check 8 stills + Adv PASS.

**Adopt (from comps, product IA):**

- KPI **card system**: label, primary value, secondary method/source line, optional sparkline (Stripe / Cloudflare / Amplitude).
- Hierarchy: brand + one job headline → KPI cards → primary chart → secondary tables/rails → CTA (Vercel Analytics / Better Stack / Cloudflare).
- Designed empty/baseline: illustration or hatch + recovery next steps (Mixpanel / Amplitude / Neon).
- Improve narrative as **Latest Update card** + Progress rail, not full MD dump; full reports collapse or live on `/reports` (Linear analog).
- Next-steps / template-style cards under gated traction (Mixpanel board empty / Amplitude templates) — without inventing metrics.

---

## 9. Constraints locked by Cos (2026-09-13)

- No invented KPI / token / money / visitor / revenue numbers.
- Public `/` = marketing + ops face (not admin, not Studio PII, not OpenClaw brief chrome).
- Daily improve: collapse on `/` or move to `/reports` — not fold hero dump.
- Strip internal launch copy from public marketing ("Cos unlocks", private-repo asides).
- UI SoT: Meta Astryx — Eng implements only after AG UX Check 8 `VISUAL_STEP_STILLS` → Adv PASS → stills to Cos.
- This PR is **Research intake only** (`evidence.md`). AG UX owns Check 7/8 next. **Not live Eng UI yet.**

---

## Acceptance record (Research)

| Field | Value |
| --- | --- |
| Received | Cos GO 2026-09-13: FAIL on look for public `/`; ADV_COMP evidence SoT before Check 7/8 or Eng |
| Well-formed? | Yes — job, live holes, opened Mobbin cites, our-hole / competitor-hole / do-not-copy, motion/delight, keep/adopt, Cos constraints |
| Proceed? | Yes — handoff to AG UX for Check 7 (flows/JTBD) then Check 8 stills; no UX artifacts in this PR |

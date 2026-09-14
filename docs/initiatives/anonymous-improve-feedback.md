# Initiative epic — Anonymous Improve Feedback

**Plain-English name:** Anonymous Improve Feedback 
**Type:** Initiative epic plan (PRD / flows) — **not** Eng implementation 
**Status:** Paul LOCK 2026-09-14 — bake anonymous improve telemetry into the Agentic Governance product 
**Owner seat:** AG Product / UX (+ Research for consent HCI); Cos ACCEPT for craft; Eng HOLD until sequenced gates clear 
**Review:** Cos craft first on this tip — **do not ping Adv** unless Cos asks

---

## One-line promise

Agentic Governance is **free**. The tradeoff is that operators share **anonymous basics** that help improve the framework. Richer diagnostic logs stay **opt-in**. Never secrets, tokens, PII, absolute paths, or private operator data.

---

## Paul / Cos locks (bake into this epic)

### Value exchange (Cos ADD LOCK from Paul — first-class product promise)

- AG stays **free**.
- **Anonymous basics are on by default** — that is the privacy-respecting tradeoff that funds continuous improve.
- **Richer diagnostic logs remain opt-in.**
- Phrase publicly in plain English on **Get AG / download**: free because operators share anonymous improve signals.
- Still **no secrets / PII** (and the rest of the privacy floor below).

### Brand voice (Cos ADD LOCK from Paul — AG site Brand Voice)

- Brand beat: **“Worker bees need to feed the hive.”**
- Use on **Get AG** + **consent** as headline / voice for the free tradeoff (anonymous basics that improve the framework).
- Public chrome stays **plain English**. Metaphor is OK as headline/voice — **not** harness jargon, not a mascot layer.
- Still: basics default on · richer logs opt-in · no secrets/PII.

### ADMIN TWIN (related product framing — Paul LOCK)

- `/admin` = **same look and craft** as the public living board (type, space, graph language).
- Sensitive numbers and ops sit **behind that door**.
- **One product, two doors** (public board vs admin) — not a cheap separate back office.
- Cite filled UX Canvas SoT [`docs/initiatives/ag-website-ux-canvas.md`](./ag-website-ux-canvas.md) — LIVE [#50](https://github.com/paulthorson/agentic-governance/pull/50) @ `6b24c4bc` (gate named [#48](https://github.com/paulthorson/agentic-governance/pull/48) @ `e9b4827`).

### Privacy floor (existing P0 — non-negotiable)

| Layer | Default | Rule |
|---|---|---|
| Anonymous basics | **ON** | High-level usage / health signals only — **no identity** |
| Richer diagnostic logs | **OPT-IN** | Never silently escalate |
| Secrets / tokens / PII / absolute host paths / private operator data | **NEVER** | Existing P0 — FAIL closed |

---

## Problem

Operators run AG (and visit the living board / Get AG path) without a governed, privacy-safe way to send improve signals back into the product. Today, bugs and ideas die in chat or never leave the operator’s machine. Without anonymous basics, Cos’s improve loop and daily digest cannot measure what is actually helping — and without a clear consent story, any telemetry risks feeling like surveillance.

We need a productized **Anonymous Improve Feedback** path that:

1. Keeps AG free via an honest value exchange,
2. Defaults to anonymous basics (not richer logs),
3. Makes off-switches and “what basics means” obvious in plain English,
4. Feeds only **measured** improve signals into the living board / Cos daily AG digest.

---

## Outcomes

1. **Value exchange is public and plain.** Get AG / download states: free because operators share anonymous improve signals. Brand beat (“Worker bees need to feed the hive.”) may headline; chrome stays plain English.
2. **Privacy floor holds.** Anonymous basics default on; richer logs opt-in only; zero secrets/tokens/PII/absolute paths/product sauce in payloads or AG git artifacts.
3. **Four lanes ship as product surfaces** (in-product + site CTAs where noted) — not ad-hoc chat dumps.
4. **Signals feed the improve loop** (living board + Cos daily AG digest) as **measured-only** events — BLANK / hatch when unpaid; never invent counts.
5. **Consent UX is research-backed** (HCI) before stories / Check 7 / pixels: clear off-switch; plain-English definition of “basics.” Research pack LIVE [#53](https://github.com/paulthorson/agentic-governance/pull/53) @ `eaa2efa2`.
6. **Admin twin framing preserved:** public board and `/admin` remain one product, two doors; improve telemetry never becomes a reason to ship a cheap separate admin look.

---

## Lanes (1–4)

| # | Lane | Default | Surfaces | What it is |
|---|---|---|---|---|
| 1 | **Anonymous basics** | **ON** | Product runtime + Get AG / consent copy | High-level usage / health signals that help improve the framework — **no identity** |
| 2 | **Bug reports** | Explicit submit | In-product + site CTA | Operator-filed bug reports into the improve intake |
| 3 | **Improvement ideas** | Explicit submit | In-product + site CTA | Operator-filed ideas into the improve intake |
| 4 | **Richer diagnostic logs** | **OPT-IN only** | Explicit consent control | Deeper diagnostics — never on by default; never secrets/PII |

**Destination for all lanes:** improve loop → living board → Cos daily AG digest — **measured only** (`docs/improve/`, public board honesty rules).

---

## Sequencing under Initiative

Eng does **not** start pixels until Cos craft + **Paul yes** on `#39` look. This epic is **PRD / flows first**. Cos craft before Adv.

| Order | Gate | Note |
|---|---|---|
| 0 | **UX Canvas** | After Brand & Design Setup. Gothelf [Lean UX Canvas v2](https://jeffgothelf.com/blog/leanuxcanvas-v2/) boxes 1–8 filled for AG website. Gate named [#48](https://github.com/paulthorson/agentic-governance/pull/48) @ `e9b4827`. **Filled initiative SoT LIVE** [#50](https://github.com/paulthorson/agentic-governance/pull/50) @ `6b24c4bc` — [`ag-website-ux-canvas.md`](./ag-website-ux-canvas.md) (ADMIN TWIN included). |
| 1 | **Research HCI — consent UX** | Clear off-switch; what “basics” means in plain English; layered consent. Pack LIVE [#53](https://github.com/paulthorson/agentic-governance/pull/53) @ `eaa2efa2` — [`dashboard/docs/research/anonymous-improve-consent-2026-09-14.md`](../../dashboard/docs/research/anonymous-improve-consent-2026-09-14.md). Stacks on `RESEARCH_HCI` + `RESEARCH_BEFORE_ENHANCE`. |
| 2 | **Stories / flows** | JTBD + Mermaid flows for lanes 1–4 + Get AG / consent / off-switch (next unpaid after this PRD). |
| 3 | **UX Check 7** | When stories exist — entry / success / error / empty / exits. |
| 4 | **Check 8 stills / Eng** | **HOLD** until Cos craft + Paul yes on `#39` look. No Eng pixels from this epic alone. |

Initiative sequence reminder (LIVE named gates): Research Scope → hunt → Brand & Design Setup → **UX Canvas** → Check 7/8 stills / Eng.

---

## Product framing (public)

**Get AG / download (plain English):** 
Agentic Governance is free because operators share anonymous improve signals that help the framework get better. You can turn basics off. Richer diagnostic logs are optional and off until you opt in. We never collect secrets, tokens, or personal data.

**Brand beat (headline / voice — OK):** 
“Worker bees need to feed the hive.”

**Not for public chrome:** harness ids, scoreboard jargon, ROLE dumps, “measured SoT” as marketing.

---

## Acceptance sketch (PRD / flows — this tip)

This tip is accepted as the Initiative epic plan when:

- [x] Plain-English name **Anonymous Improve Feedback** is recorded.
- [x] Value exchange is a **first-class product promise** (free ↔ anonymous basics default on; richer logs opt-in).
- [x] Brand beat **“Worker bees need to feed the hive.”** is noted for Get AG + consent / AG site Brand Voice.
- [x] Privacy floor (basics on / richer opt-in / never secrets·PII·paths·sauce) is explicit.
- [x] Lanes **1–4** are named with defaults and destinations.
- [x] Destination = improve loop / living board / Cos daily digest — **measured only**.
- [x] Sequencing cites UX Canvas filled SoT **#50 @ `6b24c4bc`** (gate **#48 @ `e9b4827`**), Research HCI consent pack **#53 @ `eaa2efa2`**, Check 7 when stories exist, Eng HOLD pending Cos craft + Paul yes on `#39` look.
- [x] ADMIN TWIN framing is noted (one product, two doors).
- [x] Problem, outcomes, open questions, acceptance sketch, and non-goals are present.
- [ ] Cos craft review of this PRD tip (**do not ping Adv** unless Cos asks).
- [ ] Next unpaid: stories / flows → Check 7 → stills/Eng per sequence (out of scope for this tip).

---

## Open questions

1. Exact field set for **anonymous basics** (event names / aggregates) — Research pack proposes; Privacy must confirm without identity leakage ([#53](https://github.com/paulthorson/agentic-governance/pull/53) @ `eaa2efa2`).
2. Where the **off-switch** lives (install wizard, runtime setting, Get AG page, all three?) — HCI consent pack teaches; UX composes after Cos craft.
3. Bug / idea CTA destination (GitHub issue templates vs in-app intake vs both) — Product + Cos.
4. How lane events appear on the **living board** (anonymized aggregates only on public; richer ops behind `/admin` twin?) — keep ADMIN TWIN honesty.
5. Retention window for basics vs opt-in richer logs — Privacy adversary.
6. Whether “basics on by default” needs a one-time first-run acknowledgment vs silent default + always-visible off-switch — HCI pack layered-consent guidance; Cos may rename.
7. Cross-surface copy: in-product vs site Get AG — same promise, different length; Brand beat placement rules.

---

## Non-goals (this epic / this tip)

- Eng implementation, pixels, schemas, collectors, or dashboard `/src` changes.
- Reopening or amending `#39` look stills / craft tip (Eng HOLD; Paul yes required separately).
- Inventing UX Canvas boxes or skipping the Gothelf v2 filled canvas SoT ([#50](https://github.com/paulthorson/agentic-governance/pull/50) @ `6b24c4bc`).
- Identity-bearing analytics, account graphs, or marketing attribution pixels.
- Collecting secrets, tokens, emails, PII, absolute host paths, or private operator data “for debugging.”
- Turning richer logs on by default, or dark-patterning the off-switch.
- Making `/admin` a separate visual product (violates ADMIN TWIN).
- Invented KPIs on the living board or Cos digest (measured-only / BLANK).
- Non-product surfaces outside the AG public board + admin twin.
- Adv review unless Cos asks (Cos craft before Adv).

---

## Related cites

| Cite | Why |
|---|---|
| [#50](https://github.com/paulthorson/agentic-governance/pull/50) @ `6b24c4bc` | AG website filled UX Canvas initiative SoT (+ ADMIN TWIN) |
| [#48](https://github.com/paulthorson/agentic-governance/pull/48) @ `e9b4827` | UX Canvas named LIVE gate (separate after Brand & Design Setup) |
| [#53](https://github.com/paulthorson/agentic-governance/pull/53) @ `eaa2efa2` | Anonymous Improve consent HCI Research pack |
| [`docs/initiatives/ag-website-ux-canvas.md`](./ag-website-ux-canvas.md) | Filled Gothelf v2 boxes 1–8 for AG website |
| [`dashboard/docs/research/anonymous-improve-consent-2026-09-14.md`](../../dashboard/docs/research/anonymous-improve-consent-2026-09-14.md) | Consent UX Research SoT for this epic |
| [#46](https://github.com/paulthorson/agentic-governance/pull/46) @ `cdf1c41` | Brand & Design Setup + Research Scope docs |
| [#45](https://github.com/paulthorson/agentic-governance/pull/45) @ `ead012f` | `DESIGN_SYSTEM_FIRST` LIVE |
| [`docs/improve/`](../improve/) | Cos daily AG digest / improve loop destination |
| [`dashboard/README.md`](../../dashboard/README.md) | Public `/` + `/admin/*` twin surfaces |

---

## Changelog pointer

See `CHANGELOG.md` → `[Unreleased]` → Added: Initiative epic plan **Anonymous Improve Feedback**.

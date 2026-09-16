# Center of Excellence (operating model)

Plain-English write-up of how Agentic Governance improves the standing standard from real work.

**Cos HOLD ACCEPT / Adv `COE_README_SOT`.** README and this page must name all seven checklist items below. Soft or marketing-only CoE copy that omits them = **FAIL**.

**Status of this page.** Describes the **operating model**. It does **not** invent a new bot or persona, and it does **not** silently amend the constitution.

`SELF_AUDIT_LOOP` is **LIVE** — Cos ACCEPT merged [#18](https://github.com/paulthorson/agentic-governance/pull/18) @ `5c10194`.

`RETRO_BEFORE_CLOSE` is **LIVE** — Cos ACCEPT merged [#17](https://github.com/paulthorson/agentic-governance/pull/17) @ `bd3afa5`.

---

## 1. What — framework CoE, not a delivery team

A **framework CoE**: standing standard + feedback from shipped work.

- **Not** a delivery team, not a new org-chart box, not a new sidebar persona, not a separate bot.
- The standard lives in this repo: constitution, harnesses, adversary checks, ledger.
- The feed is real work: teams ship, file triad retros, and those retros drive unpaid SoT/plans.
- Improvement is mechanical: named unpaid items with `id` / owner / metric / AC — not vibes or tips.

---

## 2. Who — Cos + AG + Adv; no new bot

No new bot. Three existing seats own the CoE loop. **Project PMs are not constitution owners.**

| Seat | Job |
|---|---|
| **Cos** | ACCEPT funnel. Only Cos ACCEPT merge makes SoT live. Does not invent policy or clear human-only vetoes. |
| **AG seat** | Framework PM for this repo. Drafts the named unpaid SoT/plan. Project PMs do **not** write AG constitution. |
| **Adv** | Challenges the plan. Does **not** author it. |

**Teams are members**, not owners of the framework write. They:

1. Ship under the **live** standard (merged Cos ACCEPT SHAs only).
2. File **triad retros** (well / didn’t / improve) into AG git as the CoE feed.
3. Absorb the next ship after Cos ACCEPT — do not run unmerged intake as law.

---

## 3. Loop

```
triad retro
    →  AG unpaid SoT/plan (id / owner / metric / AC)
    →  Adv challenge (does not author)
    →  Cos ACCEPT
    →  teams absorb
```

Negative operator feedback Cos receives is Cos-owned improve input (`COS_FEEDBACK_TO_IMPROVE` **LIVE** [#87](https://github.com/paulthorson/agentic-governance/pull/87) @ `2ab4b17`): same-day anonymize → improve epic/story → Cos → PM → (UX if craft) → Eng → QA; Adv on gates. Not chat-only. All-teams temp improve-inbox feed + Cos promote (`COS_IMPROVE_INBOX`, draft until Cos ACCEPT of AG #89) amends that LIVE lock — [#88](https://github.com/paulthorson/agentic-governance/issues/88) is the temp container pattern, not a sibling SoT path.
---

## 4. Fail-closed middle — `SELF_AUDIT_LOOP` LIVE (unpaid item or `AUDIT_CLEAR`)

`SELF_AUDIT_LOOP` is the fail-closed middle of the CoE loop: each audit cycle must produce a **named unpaid SoT/improve item** **or** explicit **`AUDIT_CLEAR`** with evidence. Nag-only digests (no unpaid item and no `AUDIT_CLEAR`) = **FAIL**.

**Status: LIVE.** Cos ACCEPT merged [#18](https://github.com/paulthorson/agentic-governance/pull/18) @ `5c10194`. Teams execute it.

`RETRO_BEFORE_CLOSE` is the close-gate twin (epic CLOSED / next-pack GO requires a triad retro in AG git).

**Status: LIVE.** Cos ACCEPT merged [#17](https://github.com/paulthorson/agentic-governance/pull/17) @ `bd3afa5`. Teams execute it.

---

## 7. Fail-closed locks LIVE

Both CoE fail-closed locks are merged law:

| Lock | Status | Merged |
|---|---|---|
| `SELF_AUDIT_LOOP` | **LIVE** | [#18](https://github.com/paulthorson/agentic-governance/pull/18) @ `5c10194` |
| `RETRO_BEFORE_CLOSE` | **LIVE** | [#17](https://github.com/paulthorson/agentic-governance/pull/17) @ `bd3afa5` |

---

## Already LIVE (cite merged SHAs)

Cite the merged SHA when claiming SoT:

| Lock / check | Status | What | Merged |
|---|---|---|---|
| `SELF_AUDIT_LOOP` | **LIVE** | Fail-closed AG self-audit → unpaid SoT/improve item or `AUDIT_CLEAR` | [#18](https://github.com/paulthorson/agentic-governance/pull/18) @ `5c10194` |
| `RETRO_BEFORE_CLOSE` | **LIVE** | Epic CLOSED / next-pack GO requires triad retro in AG git | [#17](https://github.com/paulthorson/agentic-governance/pull/17) @ `bd3afa5` |
| **Check 7** | **LIVE** | UX→Eng gate: Mermaid `userflows.md` + `jtbd.md` + Research cite (or explicit `NO_RESEARCH` → human). Stacked on `RESEARCH_BEFORE_ENHANCE`. | [#14](https://github.com/paulthorson/agentic-governance/pull/14) @ `36deb0e` |
| **Check 8** / `VISUAL_STEP_STILLS` | **LIVE** | Product UX visual step-stills sensor (mobile + desktop) graded at Critic. | [#15](https://github.com/paulthorson/agentic-governance/pull/15) @ `d61f4c1` |
| `RESEARCH_BEFORE_ENHANCE` | **LIVE** | Cite-real-screens before brief/stories; `evidence.md` sensor | [#10](https://github.com/paulthorson/agentic-governance/pull/10) @ `bd63566` |
| `RESEARCH_HCI` | **LIVE** | Master's HCI craft bar for all product Research seats. Fundamentals THEN opened comps; `evidence.md` must cite HCI + opened screens or FAIL UX handoff. Stacks on `RESEARCH_BEFORE_ENHANCE`. | [#38](https://github.com/paulthorson/agentic-governance/pull/38) @ `214ed5b` |
| `DESIGN_AGENCY_BAR` | **LIVE** | Cos LOCK operator top-agency craft bar for all product UX seats. Restraint / hierarchy / type / space / micro-interaction; Cos craft FAIL before Adv for spectacle-as-craft. Sensor: craft brief + written craft defense on stills PR. Alias `SPECTACLE_NOT_CRAFT` superseded. | [#43](https://github.com/paulthorson/agentic-governance/pull/43) @ `7e9e0b6` |
| `DESIGN_SYSTEM_FIRST` (**Brand & Design Setup**) | **LIVE** | Cos LOCK operator — Design/Experience/Branding paramount; DS is FIRST Initiative deliverable. **Research Scope** (Q1–Q8) before comps hunt. Fresh **diverse** business-model-matched comps per project; FAIL fixed AG comps (Pentagram/500/AXM) as all-teams default / copy-paste; cites state model-fit + diversity (not one peer); cites internal-only. **Next gate after Brand & Design Setup:** **UX Canvas** (Gothelf Lean UX Canvas v2 boxes 1–8 as-is — [Gothelf external SoT](https://jeffgothelf.com/blog/leanuxcanvas-v2/); **separate** gate, **not** an alias). Sequence: Research Scope → comps → Brand & Design Setup → UX Canvas → then screens / Check 7/8 stills / Eng. Template: `adversarial-ux/assets/templates/design-system.md`. Brand & Design Setup docs [#46](https://github.com/paulthorson/agentic-governance/pull/46) @ `cdf1c41`. UX Canvas name [#48](https://github.com/paulthorson/agentic-governance/pull/48) @ `e9b4827`. Standing Eng-handoff sensor: Check 9 / `INITIATIVE_START_SEQUENCE` (**LIVE** [#64](https://github.com/paulthorson/agentic-governance/pull/64) @ `a9a4327`). | [#45](https://github.com/paulthorson/agentic-governance/pull/45) @ `ead012f` |
| **Check 9** / `INITIATIVE_START_SEQUENCE` (**Initiative start sequence**) | **LIVE** | Fail-closed before Eng handoff. Sensor: missing Research Scope (Q1–Q8) OR Brand & Design Setup / Cos-signed `design-system.md` OR UX Canvas (Gothelf Lean UX Canvas v2 boxes 1–8) = **FAIL**. Do not treat a narrative pass as acceptance. **Who stamps:** QA + Cos. Adv challenges / names SoT — does not replace QA+Cos stamp. Scope: product UX Initiatives only — **not** OpenClaw. Stacks on LIVE `DESIGN_SYSTEM_FIRST` [#45](https://github.com/paulthorson/agentic-governance/pull/45) @ `ead012f` + UX Canvas name [#48](https://github.com/paulthorson/agentic-governance/pull/48) @ `e9b4827` + Check 7 + Check 8 — addition, not replacement. Supersedes draft [#49](https://github.com/paulthorson/agentic-governance/pull/49). SoT: `harnesses/qa.md` (+ UX/Research harness pointers). | [#64](https://github.com/paulthorson/agentic-governance/pull/64) @ `a9a4327` |
| **Cos memory template** (`docs/templates/cos-memory/`) | **LIVE** | Private structured memory store for Cos operators. **operator+Cos clarified store = private git** (their operator memory). **Framework:** part of AG **install/setup when Cos is seated** (wizard ASK after roster — **not** deferred README-only) — Cos prompts **private_git OR local_folder**; do **not** force one mode; wizard **must call** seating hook `mcp/adversarial_mcp/cos_memory_setup.py` (`scripts/cos_memory_setup.py` CLI stub); scaffolds `config/cos-memory/`. Skeleton SoT: `docs/templates/cos-memory/`. Separate from public AG product surface. See `docs/onboarding/cos-seating.md`. | [#64](https://github.com/paulthorson/agentic-governance/pull/64) @ `a9a4327` |
| **Check 10** / `RELEASE_COMPLIANCE` | **LIVE** | **Cos checklist** after material framework changes — **NOT** fail-closed merge gate / stop-the-presses. Unpaid cleanup: (a) legal/terms (**operator human-only**; agents **NEVER** draft/revise legal; Apache-2.0 + LICENSE govern); (b) marketing site copy drift; (c) README/git claim sync. **Who stamps:** Cos stamp; **operator on novel legal**. Cos flags operator; Cos does not draft legal. Scope: AG framework / product release path — **not** OpenClaw (unless `SURFACE_GATE_MATRIX`). Does **not** soften Check 9 fail-closed. Cos memory install ASK remains. SoT: `harnesses/chief-of-staff.md`. Pays Cos HOLD / Adv HOLE unpaid on tip `be550d9`. | [#64](https://github.com/paulthorson/agentic-governance/pull/64) @ `a9a4327` |
| `AI_SLOP_COPY_FAIL` | **LIVE** | operator LOCK 2026-09-15 **ALL PRODUCTS.** AI-slop / synthetic brochure copy on **visitor-facing or user-facing product surfaces** = **FAIL**. **Bar:** Human / Substack / Direct founder voice only. **Ban examples — not exhaustive (Brand Voice judgment):** delve, unlock, elevate, seamless, robust, leverage, empower, journey, revolutionize, cutting-edge; **twin-attribute cadence**. **Stack:** on `DESIGN_AGENCY_BAR` (**LIVE** [#43](https://github.com/paulthorson/agentic-governance/pull/43) @ `7e9e0b6`) + Brand Voice / `DESIGN_SYSTEM_FIRST` — addition, not replacement. **Who stamps:** Cos craft FAIL before Adv; UX Critic grades; QA stop on ship / Look / visual pack gates. Adv challenges / names SoT — does not replace Cos/UX/QA stamp. **Metric (fail closed):** visitor/user-facing surfaces shipping AI-slop = **fail closed**. Do not treat a narrative pass as acceptance. **Scope:** all product UX — **not** OpenClaw. **P0:** no secrets/keys/emails/PII/host paths. SoT: `harnesses/ux.md` (primary) + `harnesses/qa.md` + `harnesses/chief-of-staff.md`. | [#69](https://github.com/paulthorson/agentic-governance/pull/69) @ `859eafa3` |
| `COS_CRITICAL_THINKING` | **LIVE** | Fail-closed (**fleet**): before Cos routes any ask — think through; clarify unclear asks with the human operator (never assume); challenge soft claims; do not invent SoT; unsure → return to PM. Do not treat a narrative pass as acceptance. Stacks `COS_FEEDBACK_TO_IMPROVE` **LIVE** [#87](https://github.com/paulthorson/agentic-governance/pull/87) @ `2ab4b17` (+ `COS_IMPROVE_INBOX` amend draft AG #89). Cite fold [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#79](https://github.com/paulthorson/agentic-governance/pull/79) LIVE @ `cbc4b5b` + [#89](https://github.com/paulthorson/agentic-governance/issues/89). | [#80](https://github.com/paulthorson/agentic-governance/pull/80) @ `e75d3b0` |
| `COS_FEEDBACK_TO_IMPROVE` | **LIVE** | Fail-closed (**fleet**): every negative operator feedback / process scar Cos receives is Cos-owned improve input — not chat-only. Same-day anonymize → improve epic/story; queue Cos → PM → (UX if craft) → Eng → QA; Adv on gates; daily Cos improve pass; missing story for recorded scar = **fail closed**. Human ping only for decisions only the human can make. Do not treat a narrative pass as acceptance. **Addendum:** `COS_IMPROVE_INBOX` (draft AG #89) — all-teams temp improve-inbox feed + Cos promote ≤4h; [#88](https://github.com/paulthorson/agentic-governance/issues/88) = temp container pattern only (not a sibling SoT lock). | [#87](https://github.com/paulthorson/agentic-governance/pull/87) @ `2ab4b17` |

Check 7 / Check 8 scope: product UX surfaces. **Not** OpenClaw briefs. Check 9 / `INITIATIVE_START_SEQUENCE` is **LIVE** [#64](https://github.com/paulthorson/agentic-governance/pull/64) @ `a9a4327`: product UX Initiatives only — **not** OpenClaw; **fail-closed** before Eng handoff. Check 10 / `RELEASE_COMPLIANCE` is **LIVE** [#64](https://github.com/paulthorson/agentic-governance/pull/64) @ `a9a4327`: Cos checklist after material framework changes — **NOT** fail-closed by default; AG framework / product release path — **not** OpenClaw briefs (unless already under `SURFACE_GATE_MATRIX`). Cos memory install ASK (`private_git` OR `local_folder` at Cos seating) is **LIVE** via the same merge. `AI_SLOP_COPY_FAIL` is **LIVE** [#69](https://github.com/paulthorson/agentic-governance/pull/69) @ `859eafa3`: visitor/user-facing product surfaces only — **not** OpenClaw.

---

## Draft intake (not LIVE until Cos ACCEPT)

| Lock / check | Status | What | Note |
|---|---|---|---|
| `COS_IMPROVE_INBOX` | **DRAFT** — not live until Cos ACCEPT of AG #89 (`LIVE_SOT_MERGED_SHA`). Adv must re-NAME this PR before LIVE. Amends `COS_FEEDBACK_TO_IMPROVE` **LIVE** [#87](https://github.com/paulthorson/agentic-governance/pull/87) @ `2ab4b17`. | Fail-closed (**fleet**) addendum: (1) **Temp container:** all seated AG teams feed anonymized scars into shared **improve-inbox** (GitHub label `improve-inbox`; standing inbox [#88](https://github.com/paulthorson/agentic-governance/issues/88) tracks the pattern — **temp container only, not a competing SoT sibling lock**). (2) **Who feeds:** Cos, Product Manager, User Experience, Engineer, Quality, Research, Adversary, and product team leads — **not** Cos-only. (3) **Shape:** anonymized problem + optional fix direction + seat/product code only (no personal names/emails/secrets). (4) **Cos promote:** same day / every Cos improve pass (≤4h): promote each unpaid inbox item into improve epic/story with **requirements + acceptance criteria**, then clear the inbox item. Stacks `COS_FEEDBACK_TO_IMPROVE` metric (fail closed). (5) **Human:** does not babysit inbox or wording; ping only for legal/spend/publish/phone look. Do not treat a narrative pass as acceptance. Soft CONCERN absorb: one path only — amends #87 LIVE; do not invent a second improve path or PM/Eng/QA harness extras. | SoT: Cos harness + cos-memory locks. Cite [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#89](https://github.com/paulthorson/agentic-governance/issues/89) + [#80](https://github.com/paulthorson/agentic-governance/pull/80) LIVE @ `e75d3b0` + [#79](https://github.com/paulthorson/agentic-governance/pull/79) LIVE @ `cbc4b5b`. Temp container: [#88](https://github.com/paulthorson/agentic-governance/issues/88). |
| `COS_FEEDBACK_TO_IMPROVE` | **LIVE** — [#87](https://github.com/paulthorson/agentic-governance/pull/87) @ `2ab4b17`; cite fold AG #89 (`COS_IMPROVE_INBOX` amend draft). | Fail-closed (**fleet**): every negative operator feedback / “we’re not doing something right” / process scar Cos receives is Cos-owned improve input — **not** chat-only. **Same day (Cos):** anonymize into a universal improve item (any operator / any product); strip personal names, emails, product brand kits, and project-specific marketing craft from framework SoT. **Shape:** improve epic when thematic/recurring; else story with problem (anonymized) / requirements / AC / metric (fail closed) where applicable. **Queue:** AG backlog (issue + label / improve path); route **Cos → Product Manager → (UX if craft) → Engineer → Quality**; **Adversary** challenges gates before LIVE. **Daily:** Cos improve pass mines Cos thread + fleet scars; unpaid improve story required per unpaid negative-feedback scar. **Human ping:** only for decisions only the human can make (legal, spend, publish, phone look on a product face). Process wording / tip prose / queue hygiene = Cos+team — **not** human review. **Metric (fail closed):** negative operator feedback recorded in Cos memory / day log with **no** anonymized improve epic/story queued same day = **fail closed**. Do not treat a narrative pass as acceptance. **Addendum:** `COS_IMPROVE_INBOX` (draft AG #89) — all-teams temp improve-inbox; [#88](https://github.com/paulthorson/agentic-governance/issues/88) = temp container pattern only. | SoT: Cos harness + cos-memory locks. Cite [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#80](https://github.com/paulthorson/agentic-governance/pull/80) LIVE @ `e75d3b0` (`COS_CRITICAL_THINKING`) + [#79](https://github.com/paulthorson/agentic-governance/pull/79) LIVE @ `cbc4b5b` (`COS_OPERATOR_LOOK_GATE` / Advercase marketing-only) + [#89](https://github.com/paulthorson/agentic-governance/issues/89). |
| `COS_FLEET_LOOK_GATE` | **DRAFT** — not live until Cos ACCEPT of AG #78 (`LIVE_SOT_MERGED_SHA`). Adv must re-NAME this PR before LIVE. | Fail-closed Cos Look / Ready for **any** product tip Cos surfaces (**fleet**). Required: (1) Phone / live-face SoT for **that** product (tip gif/webm/stills alone ≠ Ready); (2) Unpaid polish named HOLD ; (3) Product-specific craft (fonts, instruments, brand marks) on **that project’s brief only** — not Cos universal. **Not** Advercase fleet Ready. Advercase / Process Instrument / marketing live-face stay under `COS_OPERATOR_LOOK_GATE` + `MARKETING_LIVE_FACE_NONREG` + #79 LIVE @ `cbc4b5b`. **Metric (fail closed):** Cos Look / Ready while phone/live-face unpaid for that product, or tip stills alone as Ready, or unpaid polish silent, or product craft as Cos universal = **fail closed**. Do not treat a narrative pass as acceptance. | SoT: Cos harness + cos-memory locks. Cite [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#80](https://github.com/paulthorson/agentic-governance/pull/80) LIVE @ `e75d3b0` + [#79](https://github.com/paulthorson/agentic-governance/pull/79) LIVE @ `cbc4b5b` + [#89](https://github.com/paulthorson/agentic-governance/issues/89). |
| `COS_CRITICAL_THINKING` | **LIVE** — [#80](https://github.com/paulthorson/agentic-governance/pull/80) @ `e75d3b0`; cite fold AG #89. | Fail-closed (**fleet**): before Cos routes any ask — (1) think through the ask; (2) if unclear, clarify with the **human operator** before routing (never assume); (3) challenge soft claims (fake “approved” copy, tip screenshots as Ready, guessed clocks); do not invent SoT or fill gaps with guesses; unsure → return to PM. **Metric (fail closed):** Cos routes on an assumed SoT / guessed ETA / tip-screenshot Ready = **fail closed**. Do not treat a narrative pass as acceptance. Stacks `COS_FEEDBACK_TO_IMPROVE` **LIVE** [#87](https://github.com/paulthorson/agentic-governance/pull/87) @ `2ab4b17` (+ `COS_IMPROVE_INBOX` amend draft AG #89). | SoT: Cos harness + cos-memory locks. Cite [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#80](https://github.com/paulthorson/agentic-governance/pull/80) LIVE @ `e75d3b0` + [#79](https://github.com/paulthorson/agentic-governance/pull/79) LIVE @ `cbc4b5b` + [#89](https://github.com/paulthorson/agentic-governance/issues/89). |
| `COS_OPERATOR_LOOK_GATE` | **LIVE** marketing face — [#79](https://github.com/paulthorson/agentic-governance/pull/79) @ `cbc4b5b`; cite fold AG #89. | Fail-closed Cos checklist before operator LOOK on **AG marketing**. Required: (1) Phone SoT PASS (operator phone or Cos phone-as-proxy **named**; tip gif/webm/stills alone = FAIL ACCEPT; stacks site #12 scar); (2) Desktop live-face nonreg vs live `https://www.agenticgovernance.app` (grid craft + Process Instrument / big brain moving; cite live URL + tip SHA); (3) **Advercase / brand webfont** live **OR** HOLD + operator GO — **AG marketing only**; other products Advercase **N/A** (cannot read as fleet Ready); (4) Unpaid chrome listed HOLD ; (5) Single brief frozen — interrupt-amend resets Ready unpaid. Cos craft FAIL before Adv. **Metric (fail closed):** operator LOOK while any item unpaid = **fail closed**. Advercase / Process Instrument / brand webfont Ready applied as unpaid on a **non-marketing** product tip = **fail closed**. Do not treat a narrative pass as acceptance. **Scope:** AG marketing face only — **not** fleet / **not** `COS_FLEET_LOOK_GATE`. Stacks `MARKETING_LIVE_FACE_NONREG`. | SoT: `harnesses/chief-of-staff.md` + `docs/templates/cos-memory/locks.md`. Cite [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#80](https://github.com/paulthorson/agentic-governance/pull/80) LIVE @ `e75d3b0` + [#79](https://github.com/paulthorson/agentic-governance/pull/79) LIVE @ `cbc4b5b` + [#89](https://github.com/paulthorson/agentic-governance/issues/89). Do not cite #77 alone as Advercase scope SoT. |
| `COS_ONE_BRIEF_PER_TIP` | **LIVE** [#76](https://github.com/paulthorson/agentic-governance/pull/76) @ `9b1b8c3`; cite fold AG #89. | Fail-closed (**fleet**): one non-negotiable brief per cloud tip / PR tip. Stacking seats+chrome+font+brain mid-run = **FAIL**. New scope = new tip **or** Cos re-PARK + Ready reset. **Scope:** all product / marketing tips Cos surfaces or commands — not marketing-only. Stacks `COS_OPERATOR_LOOK_GATE` item 5 + `COS_FLEET_LOOK_GATE` + `COS_CHAIN_NO_SHORTCUT`. Do not treat a narrative pass as acceptance. | SoT: Cos harness + cos-memory locks. Cite [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#80](https://github.com/paulthorson/agentic-governance/pull/80) LIVE @ `e75d3b0` + [#79](https://github.com/paulthorson/agentic-governance/pull/79) LIVE @ `cbc4b5b` + [#89](https://github.com/paulthorson/agentic-governance/issues/89). |
| `COS_READY_MEANS` | **LIVE** [#76](https://github.com/paulthorson/agentic-governance/pull/76) @ `9b1b8c3`; Advercase clause [#79](https://github.com/paulthorson/agentic-governance/pull/79) LIVE @ `cbc4b5b`; cite fold AG #89. | Fail-closed (**fleet**): **Ready** = `COS_OPERATOR_LOOK_GATE` checklist stamped PASS on AG marketing, **or** `COS_FLEET_LOOK_GATE` stamped PASS for other products. **Not** Ready: UX tip stills alone; Eng “cooked”/CI green alone; Adv docs name-check alone (for marketing look); PR “” while HOLD operator phone unpaid; PR “” while stand-in **Advercase / brand webfont** unpaid on an **AG marketing** tip. Stand-in fonts / Advercase / Process Instrument Ready = **AG marketing only** — **not** fleet Ready; other products Advercase **N/A**. **Metric (fail closed):** Ready from stills/CI/Adv-docs-alone/unpaid HOLD phone = **fail closed**; Advercase/webfont Ready applied unpaid on **non-marketing** tip = **fail closed**. Do not treat a narrative pass as acceptance. Stacks `MARKETING_LIVE_FACE_NONREG`. | SoT: Cos harness + cos-memory locks. Cite [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#80](https://github.com/paulthorson/agentic-governance/pull/80) LIVE @ `e75d3b0` + [#79](https://github.com/paulthorson/agentic-governance/pull/79) LIVE @ `cbc4b5b` + [#89](https://github.com/paulthorson/agentic-governance/issues/89). |
| `MARKETING_LIVE_FACE_NONREG` | **LIVE** marketing face — [#79](https://github.com/paulthorson/agentic-governance/pull/79) @ `cbc4b5b`; cite fold AG #89. | Fail-closed: AG marketing tips that change seats/chrome/persona must prove desktop live-face nonreg (grid craft + Process Instrument / big brain) vs live face, **or HOLD Eng** until restore. **Hole 1:** desktop prove is **after** phone SoT, not instead — desktop prove while phone SoT unpaid = **fail closed**; tip stills / desktop-only cannot clear phone SoT; cite site #12 scar. **#79 LIVE:** Advercase / brand webfont / Process Instrument Ready stacks here + `COS_OPERATOR_LOOK_GATE` item 3 — **AG marketing only**; other products Advercase **N/A**; Advercase/webfont Ready unpaid on non-marketing tip = **fail closed**. Do not treat a narrative pass as acceptance. Stacks living-mesh + `DESIGN_AGENCY_BAR` + phone-SoT + `COS_OPERATOR_LOOK_GATE` items 2–3. **Scope:** AG marketing face — **not** fleet / **not** `COS_FLEET_LOOK_GATE`. | SoT: Cos harness + cos-memory locks. Cite [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#80](https://github.com/paulthorson/agentic-governance/pull/80) LIVE @ `e75d3b0` + [#79](https://github.com/paulthorson/agentic-governance/pull/79) LIVE @ `cbc4b5b` + [#89](https://github.com/paulthorson/agentic-governance/issues/89). Do not cite #77 alone as Advercase scope SoT. |
| `COS_CHAIN_NO_SHORTCUT` | **LIVE** [#76](https://github.com/paulthorson/agentic-governance/pull/76) @ `9b1b8c3`; cite fold AG #89. | Fail-closed (**fleet**): commands travel **Cos → PM → UX → Eng → QA**. No Cos→Eng direct interrupt / stacked GO mid-tip. Emergency Eng stop only with named reason + Ready reset unpaid. **Metric (fail closed):** Cos→Eng direct GO while PM/UX unpaid = **fail closed**. **Scope:** chain + one-brief + Ready + `COS_FLEET_LOOK_GATE` + `COS_CRITICAL_THINKING` + `COS_FEEDBACK_TO_IMPROVE` = fleet; look-gate + nonreg = AG marketing face (#79 LIVE). **QA verify:** before operator LOOK, QA confirms (written) (a) checklist/Ready stamped PASS (`COS_OPERATOR_LOOK_GATE` on AG marketing or `COS_FLEET_LOOK_GATE` for other products) and (b) no Cos→Eng direct interrupt unpaid. Operator LOOK without that QA line = **fail closed**. Do not treat a narrative pass as acceptance. Operator LOCK 2026-09-16. | SoT: Cos harness + cos-memory locks. Cite [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#80](https://github.com/paulthorson/agentic-governance/pull/80) LIVE @ `e75d3b0` + [#79](https://github.com/paulthorson/agentic-governance/pull/79) LIVE @ `cbc4b5b` + [#89](https://github.com/paulthorson/agentic-governance/issues/89). |
| _(harness drafts)_ | — | Draft locks for `SURFACE_GATE_MATRIX`, `CRITIC_SEPARATE_STAMP`, `TOKEN_SOURCE_OR_BLANK`, `LIVE_SOT_MERGED_SHA` remain harness draft intake until Cos ACCEPT. | See harnesses. |

---

## 5. P0 — no secrets

No secrets, keys, emails, PII, absolute host paths, or private operator data in AG git. No invented tokens.

---

## 6. Soft / marketing-only = FAIL

Tips, vibes, chat-only retros, wiki scars without an unpaid item, open/draft PRs treated as live SoT, or a marketing CoE blurb missing owners / loop / fail-closed middle — **FAIL** under `COE_README_SOT`. Soft “we should…” language is **rejected**.

Fail-closed middle must cite `SELF_AUDIT_LOOP` as **LIVE** Cos ACCEPT [#18](https://github.com/paulthorson/agentic-governance/pull/18) @ `5c10194` (unpaid item or `AUDIT_CLEAR`).

`RETRO_BEFORE_CLOSE` must cite **LIVE** Cos ACCEPT [#17](https://github.com/paulthorson/agentic-governance/pull/17) @ `bd3afa5`.

---

## See also

- README CoE section (same seven checklist items)
- [`docs/improve/`](improve/) — daily Cos/AG improve digests
- [`docs/templates/cos-memory/`](templates/cos-memory/) — **LIVE** Cos operator private memory template (locks/episodes; not public product surface) — Cos ACCEPT [#64](https://github.com/paulthorson/agentic-governance/pull/64) @ `a9a4327`
- [`docs/agentic-governance-spec.md`](agentic-governance-spec.md) — ratified framework
- Triad retros under `projects/<team>/retros/`

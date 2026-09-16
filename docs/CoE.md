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

Negative operator feedback Cos receives is Cos-owned improve input (`COS_FEEDBACK_TO_IMPROVE` **LIVE** [#87](https://github.com/paulthorson/agentic-governance/pull/87) @ `2ab4b17`): same-day anonymize → improve epic/story → Cos → PM → (UX if craft) → Eng → QA; Adv on gates. Not chat-only. All-teams temp improve-inbox feed + Cos promote (`COS_IMPROVE_INBOX` **LIVE** [#98](https://github.com/paulthorson/agentic-governance/pull/98) @ `fe27c4b`) amends that LIVE lock — [#88](https://github.com/paulthorson/agentic-governance/issues/88) is the temp container pattern, not a sibling SoT path. Optical/pack/CI gate scars (AG #91 pack — draft until Cos ACCEPT): fail-closed sensors before CLOSED/GO/Ready; human gate only for phone Look / legal / spend / publish.
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
| `COS_CRITICAL_THINKING` | **LIVE** | Fail-closed (**fleet**): before Cos routes any ask — think through; clarify unclear asks with the human operator (never assume); challenge soft claims; do not invent SoT; unsure → return to PM. Do not treat a narrative pass as acceptance. Stacks `COS_FEEDBACK_TO_IMPROVE` **LIVE** [#87](https://github.com/paulthorson/agentic-governance/pull/87) @ `2ab4b17` + `COS_IMPROVE_INBOX` **LIVE** [#98](https://github.com/paulthorson/agentic-governance/pull/98) @ `fe27c4b`. Cite fold [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#98](https://github.com/paulthorson/agentic-governance/pull/98) LIVE @ `fe27c4b` + [#91](https://github.com/paulthorson/agentic-governance/issues/91)–[#97](https://github.com/paulthorson/agentic-governance/issues/97). | [#80](https://github.com/paulthorson/agentic-governance/pull/80) @ `e75d3b0` |
| `COS_FEEDBACK_TO_IMPROVE` | **LIVE** | Fail-closed (**fleet**): every negative operator feedback / process scar Cos receives is Cos-owned improve input — not chat-only. Same-day anonymize → improve epic/story; queue Cos → PM → (UX if craft) → Eng → QA; Adv on gates; daily Cos improve pass; missing story for recorded scar = **fail closed**. Human ping only for decisions only the human can make. Do not treat a narrative pass as acceptance. **Addendum:** `COS_IMPROVE_INBOX` **LIVE** [#98](https://github.com/paulthorson/agentic-governance/pull/98) @ `fe27c4b` — all-teams temp improve-inbox feed + Cos promote ≤4h; [#88](https://github.com/paulthorson/agentic-governance/issues/88) = temp container pattern only (not a sibling SoT lock). | [#87](https://github.com/paulthorson/agentic-governance/pull/87) @ `2ab4b17` |
| `COS_IMPROVE_INBOX` | **LIVE** | Fail-closed (**fleet**) addendum to `COS_FEEDBACK_TO_IMPROVE`: all seated AG teams feed anonymized scars into shared **improve-inbox** (label `improve-inbox`; standing inbox [#88](https://github.com/paulthorson/agentic-governance/issues/88) = temp container pattern only — not a competing SoT sibling). Cos promote same day / ≤4h into improve epic/story with requirements + AC. Do not treat a narrative pass as acceptance. | [#98](https://github.com/paulthorson/agentic-governance/pull/98) @ `fe27c4b` |

Check 7 / Check 8 scope: product UX surfaces. **Not** OpenClaw briefs. Check 9 / `INITIATIVE_START_SEQUENCE` is **LIVE** [#64](https://github.com/paulthorson/agentic-governance/pull/64) @ `a9a4327`: product UX Initiatives only — **not** OpenClaw; **fail-closed** before Eng handoff. Check 10 / `RELEASE_COMPLIANCE` is **LIVE** [#64](https://github.com/paulthorson/agentic-governance/pull/64) @ `a9a4327`: Cos checklist after material framework changes — **NOT** fail-closed by default; AG framework / product release path — **not** OpenClaw briefs (unless already under `SURFACE_GATE_MATRIX`). Cos memory install ASK (`private_git` OR `local_folder` at Cos seating) is **LIVE** via the same merge. `AI_SLOP_COPY_FAIL` is **LIVE** [#69](https://github.com/paulthorson/agentic-governance/pull/69) @ `859eafa3`: visitor/user-facing product surfaces only — **not** OpenClaw.

---

## Draft intake (not LIVE until Cos ACCEPT)

| Lock / check | Status | What | Note |
|---|---|---|---|
| `SHIP_WITHOUT_SENSOR` | **DRAFT** — not live until Cos ACCEPT of AG #92 (`LIVE_SOT_MERGED_SHA`). Adv must re-NAME this PR before LIVE. Parent [#91](https://github.com/paulthorson/agentic-governance/issues/91). | Fail-closed (**fleet** / G2 plugin seat): Upload/Install ≠ CLOSED. Done-when = Hub stills PASS + **named Look line** as durable PR/tip artifact (not chat). Pack GO requires named Look line durable path. Do not treat a narrative pass as acceptance. **Metric (fail closed):** Upload or Install alone stamps CLOSED while Hub stills or Look score unpaid = **fail closed**. | SoT: Cos harness + cos-memory locks. Cite [#92](https://github.com/paulthorson/agentic-governance/issues/92) + Check 8 / `VISUAL_STEP_STILLS` (**LIVE** [#15](https://github.com/paulthorson/agentic-governance/pull/15) @ `d61f4c1`) + `COS_FLEET_LOOK_GATE` / `COS_OPERATOR_LOOK_GATE` + [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#98](https://github.com/paulthorson/agentic-governance/pull/98) LIVE @ `fe27c4b`. |
| `DOCS_PASS_NE_PACK_GO` | **DRAFT** — not live until Cos ACCEPT of AG #93. Parent [#91](https://github.com/paulthorson/agentic-governance/issues/91). | Fail-closed (**fleet** / G2 plugin seat): Check 7 / Eng-handoff PASS ≠ Cos pack GO. Pack GO is a separate Cos named durable stamp on tip/PR before Eng packs. Do not treat a narrative pass as acceptance. **Metric (fail closed):** Check 7 PASS alone unlocks pack GO = **fail closed**. | SoT: Cos harness + cos-memory locks. Cite [#93](https://github.com/paulthorson/agentic-governance/issues/93) + Check 7 (**LIVE** [#14](https://github.com/paulthorson/agentic-governance/pull/14) @ `36deb0e`) + `COS_CHAIN_NO_SHORTCUT` + [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#98](https://github.com/paulthorson/agentic-governance/pull/98) LIVE @ `fe27c4b`. |
| `VERBAL_PASS_NE_OPTICAL` | **DRAFT** — not live until Cos ACCEPT of AG #94. Parent [#91](https://github.com/paulthorson/agentic-governance/issues/91). | Fail-closed (**fleet** / G2 plugin seat): Optical CLOSE = Cos-routed stills + Look score (durable) **or** named operator phone Look PASS after Cos checklist (human-only exception). Verbal KEEP ≠ optical CLOSE. Tip gif/webm/stills alone ≠ phone. Do not treat a narrative pass as acceptance. **Metric (fail closed):** Verbal alone stamps optical CLOSE = **fail closed**. | SoT: Cos harness + cos-memory locks. Cite [#94](https://github.com/paulthorson/agentic-governance/issues/94) + `VISUAL_STEP_STILLS` (**LIVE** [#15](https://github.com/paulthorson/agentic-governance/pull/15) @ `d61f4c1`) + `COS_OPERATOR_LOOK_GATE` / `COS_FLEET_LOOK_GATE` + [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#98](https://github.com/paulthorson/agentic-governance/pull/98) LIVE @ `fe27c4b`. |
| `CI_EMPTY_NE_MERGE_GATE` | **DRAFT** — not live until Cos ACCEPT of AG #95. Parent [#91](https://github.com/paulthorson/agentic-governance/issues/91). | Fail-closed (**fleet**): empty / none status-check rollup ≠ / merge Ready. Alternate gate: Adv re-NAMES PASS **and** Cos ACCEPT with explicit empty-CI acknowledgment **or** human merge GO — Adv PASS alone ≠ sole soft green. Prefer minimal required check job on docs tips when feasible (follow-on; not blocker). Do not treat a narrative pass as acceptance. **Metric (fail closed):** Empty CI rollup treated as / merge Ready = **fail closed**. | SoT: Cos harness + cos-memory locks. Cite [#95](https://github.com/paulthorson/agentic-governance/issues/95) + [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#98](https://github.com/paulthorson/agentic-governance/pull/98) LIVE @ `fe27c4b`. |
| `CRITIC_SEAT_THRASH` / `CRITIC_SEPARATE_STAMP` | **DRAFT** — not live until Cos ACCEPT of AG #96. Parent [#91](https://github.com/paulthorson/agentic-governance/issues/91). | Fail-closed (**fleet**): Critic = harness **role** (grades UX/craft); Adv ≠ Critic. After Adv PASS on docs/SoT, Cos ACCEPT may proceed without Critic dual-wait unless Critic is seated on the brief. Draft stamp: `CRITIC_SEPARATE_STAMP` — Critic grades ≠ collapse into Adv. Do not treat a narrative pass as acceptance. **Metric (fail closed):** Cos/Eng wait on Critic seat after Adv PASS while Critic is **not** seated = **fail closed**. | SoT: Cos harness + cos-memory locks. Cite [#96](https://github.com/paulthorson/agentic-governance/issues/96) + `CRITIC_SEPARATE_STAMP` + [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#98](https://github.com/paulthorson/agentic-governance/pull/98) LIVE @ `fe27c4b`. Soft CONCERN #96 cite-fold absorb. |
| `CHAT_LOCK_NE_DURABLE_FOLD` | **DRAFT** — not live until Cos ACCEPT of AG #97. Parent [#91](https://github.com/paulthorson/agentic-governance/issues/91). | Fail-closed (**fleet** / G2 plugin seat): process locks in chat unpaid until same-day durable fold (harness / cos-memory / learnings — file path named). Chat KEEP ≠ durable fold. Do not treat a narrative pass as acceptance. **Metric (fail closed):** Chat-only lock with no durable fold by next Cos improve pass (≤4h) = **fail closed**. | SoT: Cos harness + cos-memory locks. Cite [#97](https://github.com/paulthorson/agentic-governance/issues/97) + [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#98](https://github.com/paulthorson/agentic-governance/pull/98) LIVE @ `fe27c4b`. |
| Pack #91 metric | **DRAFT** — not live until Cos ACCEPT of AG #91 pack. | Pack-level: unpaid inbox scar OR unpaid promote OR unpaid Eng land after Adv PASS while scar open = **fail closed**. Cos-locked path: fail-closed sensors before CLOSED/GO/Ready; human gate only for phone Look / legal / spend / publish. Named stamp / Look line = durable artifact only. Seat code: **G2 plugin seat**. Do not treat a narrative pass as acceptance. Soft CONCERN H body/label sync **PAID**. | Cite [#91](https://github.com/paulthorson/agentic-governance/issues/91)–[#97](https://github.com/paulthorson/agentic-governance/issues/97) + [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#98](https://github.com/paulthorson/agentic-governance/pull/98) LIVE @ `fe27c4b` + Check 7/8 + `VISUAL_STEP_STILLS` + `COS_OPERATOR_LOOK_GATE` / `COS_FLEET_LOOK_GATE`. |
| `COS_IMPROVE_INBOX` | **LIVE** — [#98](https://github.com/paulthorson/agentic-governance/pull/98) @ `fe27c4b`; cite fold AG #91. | Fail-closed (**fleet**) addendum to `COS_FEEDBACK_TO_IMPROVE` LIVE #87: all-teams temp improve-inbox feed + Cos promote ≤4h; [#88](https://github.com/paulthorson/agentic-governance/issues/88) = temp container pattern only (not a sibling SoT lock). Do not treat a narrative pass as acceptance. | SoT: Cos harness + cos-memory locks. Cite [#98](https://github.com/paulthorson/agentic-governance/pull/98) LIVE @ `fe27c4b` + [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#91](https://github.com/paulthorson/agentic-governance/issues/91)–[#97](https://github.com/paulthorson/agentic-governance/issues/97). |
| `COS_FEEDBACK_TO_IMPROVE` | **LIVE** — [#87](https://github.com/paulthorson/agentic-governance/pull/87) @ `2ab4b17`; cite fold AG #91 (+ `COS_IMPROVE_INBOX` LIVE #98). | Fail-closed (**fleet**): every negative operator feedback / process scar Cos receives is Cos-owned improve input — **not** chat-only. Same-day anonymize → improve epic/story; queue Cos → PM → (UX if craft) → Eng → QA; Adv on gates; daily Cos improve pass. Do not treat a narrative pass as acceptance. | SoT: Cos harness + cos-memory locks. Cite [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#98](https://github.com/paulthorson/agentic-governance/pull/98) LIVE @ `fe27c4b` + [#91](https://github.com/paulthorson/agentic-governance/issues/91)–[#97](https://github.com/paulthorson/agentic-governance/issues/97). |
| `COS_FLEET_LOOK_GATE` | **DRAFT** — not live until Cos ACCEPT of AG #78 (`LIVE_SOT_MERGED_SHA`). Cite fold AG #91. | Fail-closed Cos Look / Ready for **any** product tip Cos surfaces (**fleet**). Required: (1) Phone / live-face SoT for **that** product (tip gif/webm/stills alone ≠ Ready); (2) Unpaid polish named HOLD ; (3) Product-specific craft on **that project’s brief only**. Do not treat a narrative pass as acceptance. | SoT: Cos harness + cos-memory locks. Cite [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#98](https://github.com/paulthorson/agentic-governance/pull/98) LIVE @ `fe27c4b` + [#91](https://github.com/paulthorson/agentic-governance/issues/91)–[#97](https://github.com/paulthorson/agentic-governance/issues/97). |
| `COS_CRITICAL_THINKING` | **LIVE** — [#80](https://github.com/paulthorson/agentic-governance/pull/80) @ `e75d3b0`; cite fold AG #91. | Fail-closed (**fleet**): before Cos routes any ask — think through; clarify unclear asks with the human operator; challenge soft claims; do not invent SoT; unsure → return to PM. Do not treat a narrative pass as acceptance. Stacks `COS_FEEDBACK_TO_IMPROVE` LIVE #87 + `COS_IMPROVE_INBOX` LIVE #98. | SoT: Cos harness + cos-memory locks. Cite [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#98](https://github.com/paulthorson/agentic-governance/pull/98) LIVE @ `fe27c4b` + [#91](https://github.com/paulthorson/agentic-governance/issues/91)–[#97](https://github.com/paulthorson/agentic-governance/issues/97). |
| `COS_OPERATOR_LOOK_GATE` | **LIVE** marketing face — [#79](https://github.com/paulthorson/agentic-governance/pull/79) @ `cbc4b5b`; cite fold AG #91. | Fail-closed Cos checklist before operator LOOK on **AG marketing**. Phone SoT PASS; desktop live-face nonreg; Advercase/webfont or HOLD+operator GO (AG marketing only); unpaid chrome listed; single brief frozen. Do not treat a narrative pass as acceptance. **Not** fleet / **not** `COS_FLEET_LOOK_GATE`. | SoT: Cos harness + cos-memory locks. Cite [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#98](https://github.com/paulthorson/agentic-governance/pull/98) LIVE @ `fe27c4b` + [#91](https://github.com/paulthorson/agentic-governance/issues/91)–[#97](https://github.com/paulthorson/agentic-governance/issues/97). |
| `COS_ONE_BRIEF_PER_TIP` | **LIVE** [#76](https://github.com/paulthorson/agentic-governance/pull/76) @ `9b1b8c3`; cite fold AG #91. | Fail-closed (**fleet**): one non-negotiable brief per cloud tip / PR tip. Do not treat a narrative pass as acceptance. | SoT: Cos harness + cos-memory locks. Cite [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#98](https://github.com/paulthorson/agentic-governance/pull/98) LIVE @ `fe27c4b` + [#91](https://github.com/paulthorson/agentic-governance/issues/91)–[#97](https://github.com/paulthorson/agentic-governance/issues/97). |
| `COS_READY_MEANS` | **LIVE** [#76](https://github.com/paulthorson/agentic-governance/pull/76) @ `9b1b8c3`; Advercase clause [#79](https://github.com/paulthorson/agentic-governance/pull/79) LIVE @ `cbc4b5b`; cite fold AG #91. | Fail-closed (**fleet**): Ready = `COS_OPERATOR_LOOK_GATE` on AG marketing **or** `COS_FLEET_LOOK_GATE` for other products. Do not treat a narrative pass as acceptance. | SoT: Cos harness + cos-memory locks. Cite [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#98](https://github.com/paulthorson/agentic-governance/pull/98) LIVE @ `fe27c4b` + [#91](https://github.com/paulthorson/agentic-governance/issues/91)–[#97](https://github.com/paulthorson/agentic-governance/issues/97). |
| `MARKETING_LIVE_FACE_NONREG` | **LIVE** marketing face — [#79](https://github.com/paulthorson/agentic-governance/pull/79) @ `cbc4b5b`; cite fold AG #91. | Fail-closed: AG marketing tips that change seats/chrome/persona must prove desktop live-face nonreg vs live face, **or HOLD Eng**. Do not treat a narrative pass as acceptance. **Not** fleet / **not** `COS_FLEET_LOOK_GATE`. | SoT: Cos harness + cos-memory locks. Cite [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#98](https://github.com/paulthorson/agentic-governance/pull/98) LIVE @ `fe27c4b` + [#91](https://github.com/paulthorson/agentic-governance/issues/91)–[#97](https://github.com/paulthorson/agentic-governance/issues/97). |
| `COS_CHAIN_NO_SHORTCUT` | **LIVE** [#76](https://github.com/paulthorson/agentic-governance/pull/76) @ `9b1b8c3`; cite fold AG #91. | Fail-closed (**fleet**): Cos → PM → UX → Eng → QA. No Cos→Eng direct interrupt / stacked GO mid-tip. Do not treat a narrative pass as acceptance. | SoT: Cos harness + cos-memory locks. Cite [#87](https://github.com/paulthorson/agentic-governance/pull/87) LIVE @ `2ab4b17` + [#98](https://github.com/paulthorson/agentic-governance/pull/98) LIVE @ `fe27c4b` + [#91](https://github.com/paulthorson/agentic-governance/issues/91)–[#97](https://github.com/paulthorson/agentic-governance/issues/97). |
| _(harness drafts)_ | — | Draft locks for `SURFACE_GATE_MATRIX`, `CRITIC_SEPARATE_STAMP` (also paid via AG #96 pack fold), `TOKEN_SOURCE_OR_BLANK`, `LIVE_SOT_MERGED_SHA` remain harness draft intake until Cos ACCEPT. | See harnesses. |

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

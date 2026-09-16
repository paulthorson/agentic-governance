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
| `DESIGN_AGENCY_BAR` | **LIVE** | Cos LOCK Paul top-agency craft bar for all product UX seats. Restraint / hierarchy / type / space / micro-interaction; Cos craft FAIL before Adv for spectacle-as-craft. Sensor: craft brief + written craft defense on stills PR. Alias `SPECTACLE_NOT_CRAFT` superseded. | [#43](https://github.com/paulthorson/agentic-governance/pull/43) @ `7e9e0b6` |
| `DESIGN_SYSTEM_FIRST` (**Brand & Design Setup**) | **LIVE** | Cos LOCK Paul — Design/Experience/Branding paramount; DS is FIRST Initiative deliverable. **Research Scope** (Q1–Q8) before comps hunt. Fresh **diverse** business-model-matched comps per project; FAIL fixed AG comps (Pentagram/500/AXM) as all-teams default / copy-paste; cites state model-fit + diversity (not one peer); cites internal-only. **Next gate after Brand & Design Setup:** **UX Canvas** (Gothelf Lean UX Canvas v2 boxes 1–8 as-is — [Gothelf external SoT](https://jeffgothelf.com/blog/leanuxcanvas-v2/); **separate** gate, **not** an alias). Sequence: Research Scope → comps → Brand & Design Setup → UX Canvas → then screens / Check 7/8 stills / Eng. Template: `adversarial-ux/assets/templates/design-system.md`. Brand & Design Setup docs [#46](https://github.com/paulthorson/agentic-governance/pull/46) @ `cdf1c41`. UX Canvas name [#48](https://github.com/paulthorson/agentic-governance/pull/48) @ `e9b4827`. Standing Eng-handoff sensor: Check 9 / `INITIATIVE_START_SEQUENCE` (**LIVE** [#64](https://github.com/paulthorson/agentic-governance/pull/64) @ `a9a4327`). | [#45](https://github.com/paulthorson/agentic-governance/pull/45) @ `ead012f` |
| **Check 9** / `INITIATIVE_START_SEQUENCE` (**Initiative start sequence**) | **LIVE** | Fail-closed before Eng handoff. Sensor: missing Research Scope (Q1–Q8) OR Brand & Design Setup / Cos-signed `design-system.md` OR UX Canvas (Gothelf Lean UX Canvas v2 boxes 1–8) = **FAIL**. Do not treat a narrative pass as acceptance. **Who stamps:** QA + Cos. Adv challenges / names SoT — does not replace QA+Cos stamp. Scope: product UX Initiatives only — **not** OpenClaw. Stacks on LIVE `DESIGN_SYSTEM_FIRST` [#45](https://github.com/paulthorson/agentic-governance/pull/45) @ `ead012f` + UX Canvas name [#48](https://github.com/paulthorson/agentic-governance/pull/48) @ `e9b4827` + Check 7 + Check 8 — addition, not replacement. Supersedes draft [#49](https://github.com/paulthorson/agentic-governance/pull/49). SoT: `harnesses/qa.md` (+ UX/Research harness pointers). | [#64](https://github.com/paulthorson/agentic-governance/pull/64) @ `a9a4327` |
| **Cos memory template** (`docs/templates/cos-memory/`) | **LIVE** | Private structured memory store for Cos operators. **Paul+Cos clarified store = private git** (their operator memory). **Framework:** part of AG **install/setup when Cos is seated** (wizard ASK after roster — **not** deferred README-only) — Cos prompts **private_git OR local_folder**; do **not** force one mode; wizard **must call** seating hook `mcp/adversarial_mcp/cos_memory_setup.py` (`scripts/cos_memory_setup.py` CLI stub); scaffolds `config/cos-memory/`. Skeleton SoT: `docs/templates/cos-memory/`. Separate from public AG product surface. See `docs/onboarding/cos-seating.md`. | [#64](https://github.com/paulthorson/agentic-governance/pull/64) @ `a9a4327` |
| **Check 10** / `RELEASE_COMPLIANCE` | **LIVE** | **Cos checklist** after material framework changes — **NOT** fail-closed merge gate / stop-the-presses. Unpaid cleanup: (a) legal/terms (**Paul human-only**; agents **NEVER** draft/revise legal; Apache-2.0 + LICENSE govern); (b) marketing site copy drift; (c) README/git claim sync. **Who stamps:** Cos stamp; **Paul on novel legal**. Cos flags Paul; Cos does not draft legal. Scope: AG framework / product release path — **not** OpenClaw (unless `SURFACE_GATE_MATRIX`). Does **not** soften Check 9 fail-closed. Cos memory install ASK remains. SoT: `harnesses/chief-of-staff.md`. Pays Cos HOLD / Adv HOLE unpaid on tip `be550d9`. | [#64](https://github.com/paulthorson/agentic-governance/pull/64) @ `a9a4327` |
| `AI_SLOP_COPY_FAIL` | **LIVE** | Paul LOCK 2026-09-15 **ALL PRODUCTS.** AI-slop / synthetic brochure copy on **visitor-facing or user-facing product surfaces** = **FAIL**. **Bar:** Human / Substack / Direct founder voice only. **Ban examples — not exhaustive (Brand Voice judgment):** delve, unlock, elevate, seamless, robust, leverage, empower, journey, revolutionize, cutting-edge; **twin-attribute cadence**. **Stack:** on `DESIGN_AGENCY_BAR` (**LIVE** [#43](https://github.com/paulthorson/agentic-governance/pull/43) @ `7e9e0b6`) + Brand Voice / `DESIGN_SYSTEM_FIRST` — addition, not replacement. **Who stamps:** Cos craft FAIL before Adv; UX Critic grades; QA stop on ship / Look / visual pack gates. Adv challenges / names SoT — does not replace Cos/UX/QA stamp. **Metric (fail closed):** visitor/user-facing surfaces shipping AI-slop = **fail closed**. Do not treat a narrative pass as acceptance. **Scope:** all product UX — **not** OpenClaw. **P0:** no secrets/keys/emails/PII/host paths. SoT: `harnesses/ux.md` (primary) + `harnesses/qa.md` + `harnesses/chief-of-staff.md`. | [#69](https://github.com/paulthorson/agentic-governance/pull/69) @ `859eafa3` |

Check 7 / Check 8 scope: product UX surfaces. **Not** OpenClaw briefs. Check 9 / `INITIATIVE_START_SEQUENCE` is **LIVE** [#64](https://github.com/paulthorson/agentic-governance/pull/64) @ `a9a4327`: product UX Initiatives only — **not** OpenClaw; **fail-closed** before Eng handoff. Check 10 / `RELEASE_COMPLIANCE` is **LIVE** [#64](https://github.com/paulthorson/agentic-governance/pull/64) @ `a9a4327`: Cos checklist after material framework changes — **NOT** fail-closed by default; AG framework / product release path — **not** OpenClaw briefs (unless already under `SURFACE_GATE_MATRIX`). Cos memory install ASK (`private_git` OR `local_folder` at Cos seating) is **LIVE** via the same merge. `AI_SLOP_COPY_FAIL` is **LIVE** [#69](https://github.com/paulthorson/agentic-governance/pull/69) @ `859eafa3`: visitor/user-facing product surfaces only — **not** OpenClaw.

---

## Draft intake (not LIVE until Cos ACCEPT)

| Lock / check | Status | What | Note |
|---|---|---|---|
| `COS_PAUL_LOOK_GATE` | **DRAFT** — not live / not effective until Cos ACCEPT merge (`LIVE_SOT_MERGED_SHA`). Adv must re-NAME this PR before LIVE. | Fail-closed Cos checklist before Paul LOOK on **AG marketing**. Required: (1) Phone SoT PASS (Paul phone or Cos phone-as-proxy **named**; tip gif/webm/stills alone = FAIL ACCEPT; stacks site #12 scar); (2) Desktop live-face nonreg vs live `https://www.agenticgovernance.app` (grid craft + Process Instrument / big brain moving; cite live URL + tip SHA); (3) Named brand webfont live **OR** HOLD + Paul GO; (4) Unpaid chrome listed HOLD ; (5) Single brief frozen — interrupt-amend resets Ready unpaid. Cos craft FAIL before Adv. **Metric (fail closed):** Paul LOOK while any item unpaid = **fail closed**. Do not treat a narrative pass as acceptance. **Scope:** AG marketing face only. | SoT: `harnesses/chief-of-staff.md` + `docs/templates/cos-memory/locks.md`. Cite [#75](https://github.com/paulthorson/agentic-governance/issues/75) Cos draft + Cos amend. |
| `COS_ONE_BRIEF_PER_TIP` | **DRAFT** — not live until Cos ACCEPT. Adv re-NAMES before LIVE. | Fail-closed: one non-negotiable brief per cloud tip / PR tip. Stacking seats+chrome+font+brain mid-run = **FAIL**. New scope = new tip **or** Cos re-PARK + Ready reset. **Scope (hole 2):** all product / marketing tips Cos surfaces or commands — not marketing-only. Stacks `COS_PAUL_LOOK_GATE` item 5 + `COS_CHAIN_NO_SHORTCUT`. Do not treat a narrative pass as acceptance. | SoT: Cos harness + cos-memory locks. [#75](https://github.com/paulthorson/agentic-governance/issues/75). |
| `COS_READY_MEANS` | **DRAFT** — not live until Cos ACCEPT. Adv re-NAMES before LIVE. | Fail-closed: **Ready** = `COS_PAUL_LOOK_GATE` checklist stamped PASS (written to Eng+UX+Adv before Paul LOOK) or product-equivalent where marketing locks N/A. **Not** Ready: UX tip stills alone; Eng “cooked”/CI green alone; Adv docs name-check alone (for marketing look); PR “” while HOLD Paul phone + stand-in fonts unpaid. **Scope (hole 2):** fleet Cos Ready — all product / marketing tips. Do not treat a narrative pass as acceptance. | SoT: Cos harness + cos-memory locks. [#75](https://github.com/paulthorson/agentic-governance/issues/75). |
| `MARKETING_LIVE_FACE_NONREG` | **DRAFT** — not live until Cos ACCEPT. Adv re-NAMES before LIVE. | Fail-closed: AG marketing tips that change seats/chrome/persona must prove desktop live-face nonreg (grid craft + Process Instrument / big brain) vs live face, **or HOLD Eng** until restore. **Hole 1:** desktop prove is **after** phone SoT, not instead — desktop prove while phone SoT unpaid = **fail closed**; tip stills / desktop-only cannot clear phone SoT; cite site #12 scar. Stacks living-mesh + `DESIGN_AGENCY_BAR` + phone-SoT + `COS_PAUL_LOOK_GATE` item 2. **Scope:** AG marketing face. Do not treat a narrative pass as acceptance. | SoT: Cos harness + cos-memory locks. [#75](https://github.com/paulthorson/agentic-governance/issues/75). |
| `COS_CHAIN_NO_SHORTCUT` | **DRAFT** — not live until Cos ACCEPT. Adv re-NAMES before LIVE. | Fail-closed: commands travel **Cos → PM → UX → Eng → QA**. No Cos→Eng direct interrupt / stacked GO mid-tip. Emergency Eng stop only with named reason + Ready reset unpaid. **Metric (fail closed):** Cos→Eng direct GO while PM/UX unpaid = **fail closed**. **Scope (hole 2):** chain + one-brief + Ready = all product tips; look-gate + nonreg = AG marketing face. **QA verify (hole 3):** before Paul LOOK, QA confirms (written) (a) checklist/Ready stamped PASS and (b) no Cos→Eng direct interrupt unpaid. Paul LOOK without that QA line = **fail closed**. Do not treat a narrative pass as acceptance. Paul LOCK 2026-09-16. | SoT: Cos harness + cos-memory locks. [#75](https://github.com/paulthorson/agentic-governance/issues/75). |
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

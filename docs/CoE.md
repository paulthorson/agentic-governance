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
| `DESIGN_SYSTEM_FIRST` (**Brand & Design Setup**) | **LIVE** | Cos LOCK Paul — Design/Experience/Branding paramount; DS is FIRST Initiative deliverable. **Research Scope** (Q1–Q8) before comps hunt. Fresh **diverse** business-model-matched comps per project; FAIL fixed AG comps (Pentagram/500/AXM) as all-teams default / copy-paste; cites state model-fit + diversity (not one peer); cites internal-only. **Next gate after Brand & Design Setup:** **UX Canvas** (Gothelf Lean UX Canvas v2 boxes 1–8 as-is — [Gothelf external SoT](https://jeffgothelf.com/blog/leanuxcanvas-v2/); **separate** gate, **not** an alias). Sequence: Research Scope → comps → Brand & Design Setup → UX Canvas → then screens / Check 7/8 stills / Eng. Template: `adversarial-ux/assets/templates/design-system.md`. Brand & Design Setup docs [#46](https://github.com/paulthorson/agentic-governance/pull/46) @ `cdf1c41`. UX Canvas name [#48](https://github.com/paulthorson/agentic-governance/pull/48) @ `e9b4827`. Standing Eng-handoff sensor: Check 9 / `INITIATIVE_START_SEQUENCE` (draft — see Draft intake). | [#45](https://github.com/paulthorson/agentic-governance/pull/45) @ `ead012f` |

Check 7 / Check 8 scope: product UX surfaces. **Not** OpenClaw briefs. Check 9 / `INITIATIVE_START_SEQUENCE` (when LIVE): product UX Initiatives only — **not** OpenClaw; **fail-closed** before Eng handoff. Check 10 / `RELEASE_COMPLIANCE` (when LIVE): Cos checklist after material framework changes — **NOT** fail-closed by default; AG framework / product release path — **not** OpenClaw briefs (unless already under `SURFACE_GATE_MATRIX`).

---

## Draft intake (not LIVE until Cos ACCEPT)

| Lock / check | Status | What | Note |
|---|---|---|---|
| **Check 9** / `INITIATIVE_START_SEQUENCE` (**Initiative start sequence**) | **DRAFT** — not live / not effective until Cos ACCEPT merge (`LIVE_SOT_MERGED_SHA`) | **Check:** Check 9 / `INITIATIVE_START_SEQUENCE` (fail-closed before Eng handoff). **Sensor:** missing cite of Research Scope (Q1–Q8) OR Brand & Design Setup / Cos-signed `design-system.md` OR UX Canvas (Gothelf Lean UX Canvas v2 boxes 1–8) = **FAIL**. Do not treat a narrative pass as acceptance. **Metric (fail closed):** Eng handoffs missing Research Scope cite, signed Brand & Design Setup, or UX Canvas (boxes 1–8) = **fail closed**. Do not treat a narrative pass as acceptance. **Scope:** product UX Initiatives only — **not** OpenClaw. **Who stamps:** QA + Cos. Adv challenges / names SoT — does not replace QA+Cos stamp. Sequence: Research Scope → comps → Brand & Design Setup → UX Canvas → then screens. Stacks on LIVE `DESIGN_SYSTEM_FIRST` [#45](https://github.com/paulthorson/agentic-governance/pull/45) @ `ead012f` + UX Canvas name [#48](https://github.com/paulthorson/agentic-governance/pull/48) @ `e9b4827` + Check 7 + Check 8 (`VISUAL_STEP_STILLS`) — addition, not replacement. Supersedes draft [#49](https://github.com/paulthorson/agentic-governance/pull/49). P0: no secrets/keys/emails/PII/host paths. | SoT: `harnesses/qa.md` (+ UX/Research harness pointers). Check 9 free on main (no collision with Checks 7–8). |
| **Cos memory template** (`docs/templates/cos-memory/`) | **DRAFT** — not live until Cos ACCEPT of this tip | Private structured memory store for Cos operators. **Paul+Cos clarified store = private git** (their operator memory). **Framework:** part of AG **install/setup when Cos is seated** (wizard ASK after roster — **not** deferred README-only) — Cos prompts **private_git OR local_folder**; do **not** force one mode; wizard **must call** seating hook `mcp/adversarial_mcp/cos_memory_setup.py` (`scripts/cos_memory_setup.py` CLI stub); scaffolds `config/cos-memory/`. Skeleton SoT remains `docs/templates/cos-memory/`. Cos↔human locks/episodes, not chat-only. **Separate from public AG product surface.** Adv may name SoT later. P0: no secrets/keys/emails/PII/host paths. | SoT: wizard + seating hook + Cos harness + template. See `docs/onboarding/cos-seating.md`. |
| **`RELEASE_COMPLIANCE`** (Check 10) | **DRAFT** — not live until Cos ACCEPT (`LIVE_SOT_MERGED_SHA`). **Pays Cos HOLD / Adv HOLE** unpaid on tip `be550d9`. | **Check:** Check 10 / `RELEASE_COMPLIANCE`. **Sensor/shape:** Cos checklist after material framework changes — **NOT** fail-closed merge gate / stop-the-presses. Cos surfaces unpaid cleanup: (a) legal/terms (**Paul human-only**; agents **NEVER** draft/revise legal; Apache-2.0 + LICENSE govern); (b) marketing site copy drift; (c) README/git claim sync. Review categories (not auto merge blockers): claims · telemetry · install promises · auth · license · public marketing face · data collection. **Who stamps:** **Cos stamp**; **Paul on novel legal**. Cos **flags Paul**; Cos does **not** draft legal. **Metric (fail closed):** Material framework-change cycles where Cos skips checklist = **fail closed**; agent-drafted legal = **fail closed**. **Scope:** AG framework / product release path — **not** OpenClaw (unless `SURFACE_GATE_MATRIX`). Does **not** soften Check 9 fail-closed. Cos memory install ASK remains. P0: no secrets/PII/host paths; no invented legal. | SoT: `harnesses/chief-of-staff.md` (+ CoE). |
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
- [`docs/templates/cos-memory/`](templates/cos-memory/) — **DRAFT** Cos operator private memory template (locks/episodes; not public product surface)
- [`docs/agentic-governance-spec.md`](agentic-governance-spec.md) — ratified framework
- Triad retros under `projects/<team>/retros/`

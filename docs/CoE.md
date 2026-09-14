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
| `DESIGN_SYSTEM_FIRST` (**Brand & Design Setup**) | **LIVE** | Cos LOCK Paul — Design/Experience/Branding paramount; DS is FIRST Initiative deliverable. **Research Scope** (Q1–Q8) before comps hunt. Fresh **diverse** business-model-matched comps per project; FAIL fixed AG comps (Pentagram/500/AXM) as all-teams default / copy-paste; cites state model-fit + diversity (not one peer); cites internal-only. Template: `adversarial-ux/assets/templates/design-system.md`. | [#45](https://github.com/paulthorson/agentic-governance/pull/45) @ `ead012f` |

Check 7 / Check 8 scope: product UX surfaces. **Not** OpenClaw briefs.

---

## Draft intake (not LIVE until Cos ACCEPT)

| Lock / check | Status | What | Note |
|---|---|---|---|
| _(none currently)_ | — | Draft locks for `SURFACE_GATE_MATRIX`, `CRITIC_SEPARATE_STAMP`, `TOKEN_SOURCE_OR_BLANK`, `LIVE_SOT_MERGED_SHA` remain harness draft intake until Cos ACCEPT. | See harnesses. |

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
- [`docs/agentic-governance-spec.md`](agentic-governance-spec.md) — ratified framework
- Triad retros under `projects/<team>/retros/`

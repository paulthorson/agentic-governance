---
name: res-desk-research
description: State what is already known about a question, with the gaps named, without a verdict.
argument-hint: "<the question>"
---

# Desk Research

Pure inventory. No verdict.

## Output

1. **What is known** — findings with their sources (what, where, when, type).
2. **What is assumed** — beliefs with no source, named as assumptions.
3. **Gaps** — what nobody has established, and why it matters.
4. **Sources consulted** — the list, with type and date.
5. **Not researched** — avenues you did not pursue, named.

```
## DESK RESEARCH

### Known (sourced)
- <finding> — <source | type | date>

### Assumed (unsourced, labeled)
- <assumption>

### Gaps
- <gap | why it matters>

### Sources consulted
- <list>

### Not researched
- <what you did not cover>
```

## `RESEARCH_BEFORE_ENHANCE` (Rule 2 A)

For UI enhancement work: named sensor `cite-real-screens` is fail-closed. Required artifact
`docs/epics/<slug>/evidence.md` (or stills index) must list real-screen source URLs and what
the pixels show **before** PM hands brief to UX / before first story. Soft / deferred Look gate
is REJECTED. When the pack hits adversarial UX, `ADV_COMP_CRITIQUE` also applies (jury opens
screens; comps are not gospel). Scar SoT (docs only):
`projects/_standing/scars/research-before-enhance.md`.

## `RESEARCH_HCI` (draft SoT until Cos ACCEPT — stacks on `RESEARCH_BEFORE_ENHANCE`)

**Not live / not effective until Cos ACCEPT.** Soft / deferred / tip-only = REJECTED. For
product UX Research packs (every product Research seat — **not** OpenClaw): after cite-real-screens,
`evidence.md` (or equivalent) must also cite HCI fundamentals (type, space, hierarchy,
gestalt, info-viz, Fitts / Hick / Jakob) with craft analysis **THEN** opened expert comps
(Obsidian graph first among equals when graph/splash is relevant). Screenshot collecting
without craft analysis = FAIL UX handoff. Metric: fail closed. Adv must name `RESEARCH_HCI`
before Cos ACCEPT. Harness SoT: `harnesses/researcher.md`.

## `DESIGN_SYSTEM_FIRST` (draft SoT until Cos ACCEPT — stacks on `DESIGN_AGENCY_BAR` + `RESEARCH_HCI` + `RESEARCH_BEFORE_ENHANCE` + Check 7/8)

**Not live / not effective until Cos ACCEPT.** Soft / deferred / tip-only = REJECTED.
**Design, Experience, and Branding are paramount**; engineering follows signed craft. For
product Initiatives (every product UX + Research seat — **not** OpenClaw): design system is the
FIRST deliverable before any web / UI pixels / stills / screens. Research + UX collaborate;
Initiative packet must include Cos-signed `design-system.md` (tokens / type / space / motion
/ brand / do-not + Experience principles + **Brand Voice** [tone, lexicon, headline patterns,
narrative drill-down] + **Audience/promise** + **Information-design rules** [measured-only;
marks stay marks] + Research cite) before Check 7 / Check 8 stills / Eng handoff. FAIL:
pixels without signed DS; Research or UX solo-shipping Initiative look; completeness stills
without a system; Eng-led chrome before craft; missing Brand Voice / Audience/promise /
Experience principles / info-design. Agency brain stacks `DESIGN_AGENCY_BAR` permanently
(not a splash tip). Metric: fail closed. Adv must name `DESIGN_SYSTEM_FIRST` before Cos ACCEPT.
Cite DESIGN_AGENCY_BAR **#43** @ `7e9e0b6`; RESEARCH_HCI **#38** @ `214ed5b`. Template:
`adversarial-ux/assets/templates/design-system.md`. Harness SoT: `harnesses/researcher.md` +
`harnesses/ux.md`.

# Scar — Research before enhance (Rule 2 A + adversary comp critique)

**Project:** Standing AG (cross-project) 
**Filed:** 2026-09-12 (Standing AG — anonymized process lock) 
**Status:** CLOSED (constitution sensors live; soft gate B rejected) 
**Kind:** process lock / UX + Research hard gate 
**Lock name:** `RESEARCH_BEFORE_ENHANCE` (Rule 2 A) + `ADV_COMP_CRITIQUE` 
**Check / sensor:** `cite-real-screens` (Rule 2 A) + `adv-comp-critique` (jury) — fail-closed; **a scar/wiki page is not the gate** 
**Required artifact:** `docs/epics/<slug>/evidence.md` (or stills index) — real-screen source URLs + what the pixels show — **before** PM hands brief to UX / before first story 
**Metric:** enhancement packs without cited real-screen evidence = **0** (hold) 
**Secondary:** `evidence.md` present before first story = **required** 
**Scope:** product UX / Research + adversarial UX jury (explicitly **not** OpenClaw morning-brief gate; not Eng-only bugs with no UI)

## Symptom

Enhancement briefs, draft stories, and packs could proceed without a cited real-screen artifact
in the epic. Soft "do comps at Look" deferred the gate. Jury review could rubber-stamp comps
without opening pixels, or treat big-app patterns as gospel (including copying competitor gaps).

## Root cause

Cite-real-screens was treated as optional color or a Look-phase soft gate, not a Rule 2 A hard
precondition. Sensors were not named in the constitution / jury agents; a docs page alone does
not fail-close.

## Fix (process lock — keep named)

### Rule 2 A — `RESEARCH_BEFORE_ENHANCE` (hard gate; soft gate B REJECTED)

1. **No** `brief.md`, stories, or pack without a cited real-screen artifact **already in the
   epic**. Draft stories without cites are **forbidden**, not deferred to Look.
2. Research (or UX if no Research seat) pulls real competitor / analog screens, cites each,
   analyzes what the UIs do / strengths / deltas vs current UI.
3. **Required artifact:** `docs/epics/<slug>/evidence.md` (or stills index) listing real-screen
   source URLs and what the pixels show — **before** PM → UX brief handoff and **before** first
   story.
4. Learnings → project knowledge base; stripped PII-free retro → this AG repo.
5. **Named sensor `cite-real-screens`:** fail-closed. Missing cites → Adv FAIL; Cos / QA / CEO
   reject.

### `ADV_COMP_CRITIQUE` (jury)

1. Critic, CX-Quality Advocate, and Evaluative UXR **open** the cited screens (operator's
   already-connected screenshot library / MCP). Not a rubber stamp that comps exist.
2. Cite-or-fail: worker actually opened real pixels.
3. Criticize **our** UI using those screens.
4. Criticize **competitor** screens — file do-not-copy gaps; comps are not gospel.
5. **Jury artifact (required before Pack / Look):** opened screen IDs or URLs (no secrets,
   keys, emails, or host paths) **and** ≥1 hole in **our** UI **and** ≥1 hole in a
   **competitor** screen **and** one do-not-copy gap.
6. **Named sensor `adv-comp-critique`:** Pack / Look path — Adv FAIL + Cos / QA / CEO reject if
   cites missing, **or** jury has no opened-screen cites, **or** jury artifact omits our-hole /
   competitor-hole / do-not-copy, **or** comps treated as uncriticizable.

## AG implication (Adv gate)

Any later AG change that restores a soft/deferred Look gate for cites, lets UX / Research skip
`evidence.md` before brief/stories, lets the jury PASS without opening cited screens / without
critiquing comps, or stores secrets in this repo → Adv **FAIL** before Cos→human ACCEPT.

## What went well

- Cos LOCK after Adv challenge: Rule 2 A hard; soft gate B rejected by name
- Named sensors in constitution (UX + Research) and adversarial-ux jury agents
- Required artifact path named (`docs/epics/<slug>/evidence.md`)

## What didn't

- Soft "comps at Look" would have kept draft stories cite-free
- Scar-only documentation is not a fail-closed sensor

## What to improve (unpaid — do not drop)

- Product harnesses enforce `evidence.md` existence before brief handoff (sensor, not wiki)
- Dated PII-free AG retros per pack that exercised the lock

## P0 boundary

This repo is public. Do **not** file: API keys, screenshot-library / MCP tokens or keys,
account emails, PII, absolute host paths, private operator data, or product credentials. You may
say "use the operator's already-connected screenshot library / MCP" without naming vendor
secrets or how to log in.

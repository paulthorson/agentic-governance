# Research before enhance

**Status:** Closed — 2026-09-12. Constitution sensors are live. A deferred
Look-phase gate is rejected.

**What this practice is for:** Stop a product UX or Research pack from moving
into briefs or stories without cited real-screen evidence.

**When it applies:** Before a Product Manager hands a brief to User Experience,
and before the first story is written. Applies to product UX, Research, and
the adversarial UX jury. Does not apply to engineering-only bugs with no UI,
or to external-runtime morning briefs.

**Recorded:** 2026-09-12

**Lock name:** `RESEARCH_BEFORE_ENHANCE` (Rule 2 A) + `ADV_COMP_CRITIQUE`

**Sensors:** `cite-real-screens` (Rule 2 A) and `adv-comp-critique` (jury) —
fail-closed. A documentation page is not the gate.

**Required evidence:** `docs/epics/<slug>/evidence.md` (or a stills index)
listing real-screen source URLs and what those pixels show.

**Miss:** Any enhancement pack, brief, or story set that proceeds without that
cited real-screen artifact already in the epic.

## What failed

Enhancement briefs, draft stories, and packs could proceed without a cited
real-screen artifact in the epic. A deferred “do comps at Look” rule left
draft stories without cites. Jury review could pass competitor screens without
opening the pixels, or treat large-app patterns as required — including
copying competitor gaps.

## What the gate requires

### Rule 2 A — `RESEARCH_BEFORE_ENHANCE`

Hard gate. A deferred Look-phase gate is rejected.

1. No `brief.md`, stories, or pack without a cited real-screen artifact
   already in the epic. Draft stories without cites are forbidden, not
   deferred to Look.
2. Research (or User Experience if there is no Research seat) pulls real
   competitor or analog screens, cites each one, and records what those UIs
   do, their strengths, and the deltas versus the current UI.
3. Required artifact: `docs/epics/<slug>/evidence.md` (or a stills index)
   listing real-screen source URLs and what the pixels show — before the
   Product Manager hands the brief to User Experience, and before the first
   story.
4. Learnings go to the project knowledge base. A personal-data-free
   retrospective may be recorded in this repository.
5. Named sensor `cite-real-screens`: fail-closed. Missing cites are an
   Adversary fail. Chief of Staff, Quality, and Chief Executive reject.

### `ADV_COMP_CRITIQUE` (jury)

1. Critic, CX-Quality Advocate, and Evaluative UXR open the cited screens
   through the operator’s already-connected screenshot library or MCP.
   Existence of a comps list is not enough.
2. Cite-or-fail: the worker actually opened real pixels.
3. Critique our UI using those screens.
4. Critique competitor screens — file do-not-copy gaps. Comps are not
   required patterns.
5. Jury artifact (required before Pack or Look): opened screen IDs or URLs
   (no secrets, keys, emails, or host paths) **and** at least one hole in
   our UI **and** at least one hole in a competitor screen **and** one
   do-not-copy gap.
6. Named sensor `adv-comp-critique`: Pack or Look path — Adversary fail, and
   Chief of Staff, Quality, and Chief Executive reject, if cites are missing,
   the jury has no opened-screen cites, the jury artifact omits our-hole /
   competitor-hole / do-not-copy, or comps are treated as uncriticizable.

## Framework implication

Any later change that restores a deferred Look gate for cites, lets User
Experience or Research skip `evidence.md` before brief or stories, lets the
jury pass without opening cited screens or critiquing comps, or stores
secrets in this repository is an Adversary fail before Chief of Staff
acceptance.

## Still required

- Product harnesses must enforce that `evidence.md` exists before brief
  handoff (a sensor, not a wiki page).
- Dated, personal-data-free retrospectives for each pack that exercised the
  lock.

## Public-tree boundary

This repository is public. Do not commit credentials or personal data. You
may say “use the operator’s already-connected screenshot library / MCP”
without naming vendor secrets or how to log in.

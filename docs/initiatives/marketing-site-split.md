# Epic — Marketing site split (EXTRACT PRD)

Status: **tip for Cos ACCEPT / MUST-merge** (operator LOCK 2026-09-14; Cos craft PASS
on content with stay-vs-move OPEN Q → LOCK). Docs / Class A ops plan only — not look,
not pixels, not Research.

**operator LOCK — repo name (exact):**
[`paulthorson/agentic-governance-site`](https://github.com/paulthorson/agentic-governance-site)

**Related initiative SoT (look / UX, separate track):**
[`ag-website-ux-canvas.md`](ag-website-ux-canvas.md) — screens still gated; **never**
absorb #39 / #26 look into this extract epic.

**Related (Anonymous Improve product epic, separate):**
[`anonymous-improve-feedback.md`](anonymous-improve-feedback.md) — this split epic only
locks **which git** owns public UX vs measured corpus (below); it does not rewrite that
PRD.

## Problem

`paulthorson/agentic-governance` currently carries both (1) the product/framework
people download and (2) the public marketing / living-board surface under
`dashboard/` is the **LOCALHOST** improve app only (Tip B #124). Public marketing face = `agentic-governance-site` / https://www.agenticgovernance.app. Framework must **not** bind Vercel project `agentic-governance`.

That conflates faces:

- Clone / download of AG looks like (or ships beside) a marketing site.
- Marketing deploy is wired to the framework git, so process docs, proof hubs, and
 look PRs fight the same tree.
- Get AG / download CTA risk pointing at the wrong git once a marketing-only repo
 exists.
- Analytics / measured board feeds belong to the framework loop; the marketing
 surface should **consume** them read-only, not own the framework.

## Outcomes (operator LOCK — SPLIT tracks)

1. **New git for MARKETING WEBSITE only** —
 [`paulthorson/agentic-governance-site`](https://github.com/paulthorson/agentic-governance-site)
 (created; name locked). Extract the `dashboard/` public marketing surface from
 `agentic-governance` into that repo.
2. **`paulthorson/agentic-governance` remains the product/framework** people
 download — **no** marketing site as the download face.
3. **Vercel project for the marketing-site repo is on the CRITICAL PATH** (Cos/operator
 LOCK) — create / bind a Vercel project to
 https://github.com/paulthorson/agentic-governance-site as Class A ops **now**.
 **Do NOT wait** on look stills (**#39 / #26**). Rewire / successor of current
 marketing deploy (**agentic-governance-site** Vercel) is the critical path;
 conflict cleanup for open docs tips **#42 / #35 / #34 / #49** GO on a **separate**
 track — not this PRD’s merge payload.
4. **Get AG / download CTA URL** →
 `https://github.com/paulthorson/agentic-governance` (or release assets) — **NOT**
 the marketing repo. Settled release posture: **no acceptance gate**;
 Apache-2.0 LICENSE is the only use governor ([redacted] Get AG files removed).
5. **Marketing site PULLS** analytics / measured board feeds **FROM** the AG git
 (or a published feed from AG) — **read-only consume**; marketing git does **not**
 contain the framework.

## Critical path — Vercel project (Class A; not gated on look)

| Step | Owner | Lock |
|---|---|---|
| Create / bind Vercel project to https://github.com/paulthorson/agentic-governance-site | Cos (Class A ops) | **CRITICAL PATH** of this site-split epic |
| **Do NOT wait** on #39 / #26 look stills / pixels | Eng + Cos | Look ≠ deploy path |
| When Vercel project is up → **Cos notifies operator** (domain setup) | Cos → operator | Cos owns operator notify; operator owns domain setup after notify |
| Keep marketing deploy on agentic-governance-site Vercel (framework detached) | Cos / Eng Class A | Same critical path; still not blocked on look |

## Class A vs Class B merge rule (cite)

| Class | What | Merge rule |
|---|---|---|
| **Class A** | Process / docs / extract + **Vercel project create/rewire** ops | May plan and (after Cos ACCEPT of this PRD) execute **without** waiting on marketing look. Marketing look ≠ process. Vercel project creation is **critical path**. |
| **Class B** | Marketing look / stills / pixels (`dashboard` craft, Check 7/8 stills) | **Eng HOLD** pixels on **#39** until operator yes. **Never** #39 / #26 look on this extract tip. Look/stills move with the site repo **once split**, still under operator craft gate — **not** a gate on Vercel project create. |

- **Process/docs stay in AG git** (this epic lives here as Class A SoT).
- **Research not required** for the repo split.
- **Cos ACCEPT** this extract PRD, then execute (including Vercel project on critical path).
- **Eng** may **plan** extract + Vercel project/rewire as **Class A ops** now; may not ship
 look pixels via #39/#26.

## Stay-vs-move LOCKs (Cos craft PASS — was OPEN Q)

Cos craft PASS on content; operator/Cos LOCK these three (no longer open):

| # | Topic | LOCK |
|---|---|---|
| L1 | **Admin twin** | **Admin twin UI moves** with the marketing-site repo — **one product, two doors** (public board + `/admin` craft together). **AG owns** measured data / feeds the twin reads. |
| L2 | **Anonymous Improve** | **Public UX / consent** lives on the marketing-site (+ in-product later). **Measured improve corpus stays in AG git.** |
| L3 | **Living board** | **Living board UI moves** with the marketing-site repo. **Feed publisher stays on AG**; site **read-only consumes** the feed. |

## Move / stay sketch (per LOCKs above)

### Move → `paulthorson/agentic-governance-site`

- Public marketing surface today under AG `dashboard/` (app shell, public `/`,
 marketing chrome, Get AG CTA wiring target).
- **Admin twin UI** (`/admin`) — same craft as public board; one product, two doors
 (L1).
- **Anonymous Improve public UX / consent** surface (L2); in-product later is a
 product track, not a reason to keep public UX in AG git.
- **Living board UI** (L3).
- Look / stills / visual QA packs that are **marketing-site craft** — move with the
 site repo **once split** (still Class B / operator craft gate; not executed by this
 PRD; **never** #39 / #26 on this tip).
- Vercel project bound to site repo (**critical path** create/rewire; includes
 public face on **agentic-governance-site**.

### Stay → `paulthorson/agentic-governance`

- Framework / product download surface (README, harnesses, agents, skills, MCP,
 constitutions, domains).
- Process / docs / CoE / improve / proof / initiatives (including **this** epic).
- **Measured data / feeds** for admin twin (L1) — AG owns; marketing UI consumes.
- **Measured improve corpus** (L2) — AG owns.
- **Living board feed publisher** (L3) — AG owns; marketing **read-only consume**.
- Release assets / tags for Get AG.

## Acceptance sketch (Cos ACCEPT → execute)

Cos ACCEPT / MUST-merge of **this** tip means the extract PRD is SoT (including
stay-vs-move LOCKs). Execute tracks (separate PRs / ops) then prove:

| # | Acceptance check |
|---|---|
| A1 | Marketing git exists at exact URL
 https://github.com/paulthorson/agentic-governance-site and holds the extracted
 public marketing surface (framework code **not** vendored into it). |
| A2 | `paulthorson/agentic-governance` download face is framework-first — marketing
 site is **not** the clone/download primary face. |
| A3 | **CRITICAL PATH:** Vercel project exists for
 https://github.com/paulthorson/agentic-governance-site (create and/or rewire of
 **agentic-governance-site**). Class A ops — **not** blocked on
 #39/#26 look stills. |
| A3a | **Cos notifies operator** when that Vercel project is up so operator can do **domain
 setup**. Cos owns the notify; notify is part of critical-path completion. |
| A4 | Get AG / download CTA resolves to
 `https://github.com/paulthorson/agentic-governance` or AG release assets — **not**
 `agentic-governance-site`. Settled posture: **no acceptance gate**; Apache-2.0
 LICENSE only (Get AGs removed). |
| A5 | Marketing site consumes analytics / measured board feeds from AG (or published
 AG feed) **read-only**; no framework tree inside marketing git. |
| A6 | Process/docs remain in AG git; look/stills that move do so under Class B / operator
 craft rules (Eng HOLD #39 until operator yes) — look remains **off** the Vercel
 critical path. |
| A7 | Stay-vs-move LOCKs held: admin twin UI + living board UI + Anonymous Improve
 public UX/consent on site repo; AG owns measured data/feeds, improve corpus, and
 feed publisher. |

**Separate GO (not this PRD’s merge payload):** conflict cleanup for open tips
**#42 / #35 / #34 / #49** — Class A hygiene track; may proceed when Cos schedules;
must not pull in **#39 / #26** look. Vercel project create/rewire itself is **on**
this epic’s critical path (not deferred to look).

## Non-goals

- No #39 / #26 look, stills, or pixel Eng GO from this epic.
- No Research pack required for the split itself.
- No rename of `paulthorson/agentic-governance-site` (name locked).
- No moving process/docs/CoE/improve/proof/initiatives / measured corpora into the
 marketing git.
- No pointing Get AG at the marketing repo.
- No shipping framework harnesses/agents inside the marketing git.
- No treating conflict cleanup #42/#35/#34/#49 as blocked on this tip’s wording —
 they GO separately when Cos says.
- No gating Vercel project creation on #39 / #26 look stills.
- No rewriting [`anonymous-improve-feedback.md`](anonymous-improve-feedback.md)
 product lanes here — only the git ownership LOCK (L2).

## Ownership / next

| Role | Action |
|---|---|
| **Cos** | ACCEPT / MUST-merge this extract PRD tip when CI green + MERGEABLE → execute critical path (extract + **Vercel project create/rewire** Class A). **Notify operator** when Vercel project is up (domain setup). |
| **operator** | Domain setup after Cos notify that Vercel project for agentic-governance-site is up. |
| **Eng** | Plan extract + Vercel project/rewire as Class A ops (**not** gated on look); **HOLD** #39 pixels until operator yes. |
| **UX** | Look/stills follow site repo after split; never via this tip; never #39/#26 here; never block Vercel critical path. |
| **Research** | Not required for repo split. |
| **Adv** | Challenge only if this tip smuggles look, moves measured corpora/process into marketing git, or re-gates Vercel create on #39/#26. |

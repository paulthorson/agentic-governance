# Changelog

All notable changes to the Adversarial Agents framework.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **OpenClaw ocuclaw-owner-guard scar SoT** (docs only; `OCUCLAW_OWNER_GUARD`;
 `scripts/ocuclaw-owner-guard` + cron every 2 min; bare ocuclaw / even-ai keys
 remapped each tick; `defaultAgent` stays `main`; zero `openclaw.json` hand-edits
 = **0** hold) at `projects/openclaw/scars/ocuclaw-owner-guard.md`. CLOSED harness
 scar for bare session keys rejected under `agents.ownership=explicit` (no
 explicit owner). Scope: OpenClaw Studio OcuClaw / relay sessions only — **not**
 product UX Check 7 / Check 8 / Check 9. Closes residual named unpaid in
 question-wait-guard [#66](https://github.com/paulthorson/agentic-governance/pull/66).
 Draft until Cos ACCEPT after Adv (`LIVE_SOT_MERGED_SHA`). P0: no secrets/tokens,
 emails, Discord channel names, absolute host home paths, Notion workspace IDs,
 cron UUIDs, or private operator data.
- **OpenClaw question-wait-guard scar SoT** (docs only; `QUESTION_WAIT_GUARD`;
 question-wait-guard script + cron every 2 min; main session `blocked_tool_call`
 hangs ≥120s without auto-abort = **0** hold) at
 `projects/openclaw/scars/question-wait-guard.md`. CLOSED harness scar for
 `agent:main:main` hung on masked-token / secret `question.waitAnswer` (default
 15m timeout too long). Scope: OpenClaw Studio session ops only — **not** product
 UX Check 7 / Check 8. Draft until Cos ACCEPT after Adv (`LIVE_SOT_MERGED_SHA`).
 P0: no secrets/tokens, emails, Discord channel names, absolute host home paths,
 Notion workspace IDs, or private operator data.
- **OpenClaw gateway single-owner + stale-install recycle scar SoT** (docs only;
 `GATEWAY_SINGLE_OWNER` + `STALE_INSTALL_RECYCLE`; gateway-health-guard–style
 scheduled sensor; competing gateway process count = **0** hold while LaunchAgent
 loaded) at
 `projects/openclaw/scars/gateway-single-owner-stale-install-recycle.md`. CLOSED
 harness scar for dual-owner recycle races + install-changed `UNAVAILABLE` under a
 long-lived PID. Scope: OpenClaw Studio gateway ops only — **not** product UX
 Check 7 / Check 8. Draft until Cos ACCEPT after Adv (`LIVE_SOT_MERGED_SHA`).
 P0: no secrets/tokens, emails, Discord channel names, absolute host home paths
 (LaunchAgent label OK), or private operator data.
- **Check 9 / `INITIATIVE_START_SEQUENCE` (Paul LOCK Cos plain 2026-09-15 — now LIVE via [#64](https://github.com/paulthorson/agentic-governance/pull/64) @ `a9a4327`):**
 Standing QA check (same family as Check 7 / Check 8 visual stills) — **fail-closed before Eng
 handoff**. Plain name: **Initiative start sequence**. Sequence **must** run before screens:
 **Research Scope → comps → Brand & Design Setup → UX Canvas** (Gothelf Lean UX Canvas v2 boxes
 1–8) → **then screens**. Sensor: missing cite of Research Scope (Q1–Q8) OR Brand & Design Setup /
 Cos-signed `design-system.md` OR UX Canvas (boxes 1–8) at Eng handoff = **FAIL**. Do not treat a narrative pass as acceptance
 rejected. **Who stamps:** QA + Cos. Adv challenges / names SoT — does not replace QA+Cos stamp.
 Stacks on LIVE `DESIGN_SYSTEM_FIRST` [#45](https://github.com/paulthorson/agentic-governance/pull/45)
 @ `ead012f` + UX Canvas name [#48](https://github.com/paulthorson/agentic-governance/pull/48) @
 `e9b4827` + Check 7 + Check 8 (`VISUAL_STEP_STILLS`) — addition, not replacement. Scope: product
 UX Initiatives only — **not** OpenClaw. Check 9 free on main (no collision). Supersedes draft
 [#49](https://github.com/paulthorson/agentic-governance/pull/49) (Gothelf without check id).
 **Metric (fail closed):** Eng handoffs missing Research Scope cite, signed Brand & Design Setup, or
 UX Canvas (boxes 1–8) = **fail closed**. Do not treat a narrative pass as acceptance. SoT: `harnesses/qa.md` + UX/Research
 harness + CoE Already LIVE.
- **Cos memory template (Paul LOCK Cos enhancement — now LIVE via [#64](https://github.com/paulthorson/agentic-governance/pull/64) @ `a9a4327`):** Baked-in operator
 template at `docs/templates/cos-memory/` for a **private** structured memory store.
 **Paul+Cos clarified store = private git** (their operator memory). **Framework:** part of AG
 **install/setup when Chief of Staff is seated** — **not** a deferred README-only step. Wizard ASK
 after roster (`mcp/adversarial_mcp/setup_wizard.py`); finalize **must call** seating hook
 `mcp/adversarial_mcp/cos_memory_setup.py` (`scripts/cos_memory_setup.py` CLI stub) —
 Cos prompts `private_git` OR `local_folder` (do **not** force one); scaffolds `config/cos-memory/`;
 writes mode/label to `config/setup.md` + Cos persona. Cos harness stop if seated without mode.
 Docs: `docs/onboarding/cos-seating.md` + README Install. Cos↔human locks/episodes, not chat-only.
 **Separate from public AG product surface.** Adv may name SoT later. P0: no secrets/keys/emails/PII/host
 paths. Folded into the same Class A tip as Check 9 (no second PR).
- **`RELEASE_COMPLIANCE` (now LIVE via [#64](https://github.com/paulthorson/agentic-governance/pull/64) @ `a9a4327`):**
 **Check:** Check 10 / `RELEASE_COMPLIANCE`. **Sensor/shape:** Cos checklist after material
 framework changes — **NOT** fail-closed merge gate / stop-the-presses. Unpaid cleanup:
 (a) legal/terms (**Paul human-only**; agents **NEVER** draft/revise legal; Apache-2.0 + LICENSE
 govern); (b) marketing site copy drift; (c) README/git claim sync. Review categories (not auto
 merge blockers): claims · telemetry · install promises · auth · license · public marketing face ·
 data collection. **Who stamps:** Cos stamp; **Paul on novel legal**. Cos flags Paul; Cos does not
 draft legal. **Metric (fail closed):** skipped Cos checklist after material framework change = **fail closed**; agent-drafted legal = **fail closed**. **Scope:** AG framework / product release path — not
 OpenClaw (unless `SURFACE_GATE_MATRIX`). Check 9 stays fail-closed; Cos memory install ASK stays.
 SoT: `harnesses/chief-of-staff.md` + CoE Already LIVE.

- **Get AG (historical — file later removed):** Fuller LICENSE text authored on tip [#60](https://github.com/paulthorson/agentic-governance/pull/60); path was `` (**removed** on release hardening).
- **Eng extract execute status (Class A companion):** After Eng plan [#56](https://github.com/paulthorson/agentic-governance/pull/56) **Cos ACCEPT MERGED LIVE** @ `e7bb36e` — extract execute **GO** (site-repo extract continues **in parallel**). Site face → `paulthorson/agentic-governance-site`; this repo remains feed/corpus publisher + framework download. Path: `docs/initiatives/marketing-site-extract-execute.md`. Settled Get AG posture supersedes prior acceptance-gate HOLD (see Removed).

- **Get AG (historical — file later removed).** Cos LOCK with Paul 2026-09-14. Path was `` (**removed** on release hardening; see Removed above).
- **Eng extract plan (Class A ops): Marketing site split.** Companion to PRODUCT epic
 [#55](https://github.com/paulthorson/agentic-governance/pull/55) @ `19e451f` (**MERGED LIVE**) —
 `docs/initiatives/marketing-site-split.md` (do not overwrite). Path:
 `docs/initiatives/marketing-site-extract-plan.md`. Cos OPEN Q LOCKs folded: admin twin UI,
 Anonymous Improve public UX, living board UI → `agentic-governance-site`; AG owns
 feeds/corpus/publisher (site read-only pull). Vercel project `agentic-governance-site`
 already created + Git-linked. Get AG CTA → AG git only. **PLAN ONLY** — Eng HOLD look
 pixels until Paul yes. Cos ACCEPT + MUST-merge this Eng plan when CI green; Eng execute
 after this plan MERGED.
- **Marketing site split (extract epic PRD — MERGED LIVE [#55](https://github.com/paulthorson/agentic-governance/pull/55) @ `19e451f`):** Paul
 LOCK 2026-09-14 + Cos craft PASS — extract public marketing/`dashboard` surface into
 locked repo [`paulthorson/agentic-governance-site`](https://github.com/paulthorson/agentic-governance-site);
 AG stays framework download face; **Vercel project create CRITICAL PATH** (do **not**
 wait on #39/#26); Cos owns Paul notify when Vercel is up (domain setup); stay-vs-move
 LOCKs: admin twin UI + living board UI + Anonymous Improve public UX/consent move with
 site; AG owns measured data/feeds, improve corpus, feed publisher (read-only consume);
 Get AG CTA → AG git; conflict cleanup #42/#35/#34/#49 GO separately; Class A ≠ Class B
 look — never #39/#26. Path: `docs/initiatives/marketing-site-split.md` (+ index).
- **Initiative epic plan: Anonymous Improve Feedback (PRD / flows — Eng HOLD).** Paul LOCK
 2026-09-14 bake anonymous improve telemetry into the AG product. **Value exchange:** AG is
 free because operators share anonymous basics (default on); richer diagnostic logs remain
 opt-in. **Brand beat:** “Worker bees need to feed the hive.” (Get AG + consent headline/voice;
 chrome stays plain English). Privacy floor: never secrets/tokens/PII/absolute paths/product
 sauce. Lanes 1–4 (basics / bugs / ideas / richer opt-in) feed improve loop / living board /
 Cos daily digest — measured only. Sequencing: after UX Canvas filled SoT [#50](https://github.com/paulthorson/agentic-governance/pull/50)
 @ `6b24c4bc` (gate named [#48](https://github.com/paulthorson/agentic-governance/pull/48) @
 `e9b4827`) → Research HCI consent pack [#53](https://github.com/paulthorson/agentic-governance/pull/53)
 @ `eaa2efa2` → Check 7 when stories exist → Eng pixels only after Cos craft + Paul yes on #39
 look. ADMIN TWIN framing noted. Path: `docs/initiatives/anonymous-improve-feedback.md` (+
 index README).
- **AG website UX Canvas (initiative SoT):** Filled Gothelf Lean UX Canvas v2 for the AG
 marketing/website initiative — Cos LOCK with Paul 2026-09-14; screens gated after this
 canvas. Includes admin twin definition (one product, two doors). Path:
 `docs/initiatives/ag-website-ux-canvas.md`. Pointer from `adversarial-ux/README.md`
 Initiative sequence. **Not** the constitution Gothelf box-definitions tip. LIVE via
 [#50](https://github.com/paulthorson/agentic-governance/pull/50) @ `6b24c4bc`.

- **SoT: `DESIGN_SYSTEM_FIRST` (Brand & Design Setup) — LIVE via `#45` / `ead012f`.** Cos
 LOCK Paul — **Design, Experience, and Branding are paramount** (not optional polish after
 Eng; design system + Experience + Branding lead Initiative; **engineering follows signed
 craft**). Design system is the **FIRST Initiative deliverable** for **every product UX +
 Research seat** (AG, Ladders, [redacted product], Even Weather / EW, EvenCursor, Dungeon, JEEP, and
 future) — **not OpenClaw.** **Bar / order:** bake DS before any web / UI pixels / stills /
 screens; Research + UX collaborate; Cos signoff in early Initiative. Agency design thinking
 (restraint, hierarchy, type, space, one strong quiet option) is **permanent UX brain** —
 stacks `DESIGN_AGENCY_BAR`; not a one-off splash tip. **Required `design-system.md`
 sections:** tokens / type / space / motion / brand / do-not + **Experience principles** +
 **Brand Voice** (tone, lexicon — words we use/never use — headline patterns, narrative
 drill-down voice; name Brand Voice explicitly) + **Audience/promise** +
 **Information-design rules** (measured-only; marks stay marks) + Research cite. Template:
 `adversarial-ux/assets/templates/design-system.md`. **Stack:** addition on
 `DESIGN_AGENCY_BAR` + `RESEARCH_HCI` + `RESEARCH_BEFORE_ENHANCE` (Rule 2 A) + Critic Check 7
 + Check 8 (`VISUAL_STEP_STILLS`, **LIVE** via `#15` / `d61f4c1`) — **not** a replacement.
 **FAIL:** shipping screens/stills/web without signed `design-system.md`; Research or UX
 solo-shipping Initiative look; completeness stills without a system; Eng-led chrome before
 signed craft; missing Experience principles / Brand Voice / Audience/promise / info-design;
 invented/blank-as-measured; marks-as-decoration. **Sensor (fail-closed):** Initiative packet
 includes complete `design-system.md` (not tokens/type/space/motion/do-not only) + Research
 cite; Cos signoff stamp before Check 7 / Check 8 stills / Eng handoff. **Metric (fail closed):**
 pixels shipped without DS signoff = **0**. Soft / deferred / tip / wiki-scar-only =
 **REJECTED**. **HOLD ACCEPT until Adv names the check** (`DESIGN_SYSTEM_FIRST`) then Cos
 ACCEPT merge. Do **not** mark LIVE until Cos ACCEPT MERGED SHA. Cite prior locks:
 DESIGN_AGENCY_BAR **#43** @ `7e9e0b6`; RESEARCH_HCI **#38** @ `214ed5b`. **P0:** no
 secrets/keys/emails/PII/host paths. Out of scope: inventing a token feed; filling a concrete
 product Initiative `design-system.md`; OpenClaw briefs; amending prior stills PNGs. SoT:
 `harnesses/ux.md` + `harnesses/researcher.md`; template; adversarial-ux /
 adversarial-researcher critic tables + Adv pointers + flat `agents/*` copies; skill
 pointers; CoE + spec Section 5.0 / 5.2 index pointers.

- **Draft SoT: `DESIGN_AGENCY_BAR` — not live / not effective until Cos ACCEPT merge.** Cos
 LOCK Paul agency craft bar for **every product UX seat** (AG, Ladders, [redacted product], Even
 Weather / EW, EvenCursor, Dungeon, JEEP, and future) — **product UX stills / public marketing
 faces only; not OpenClaw briefs.** **Bar:** design as if from a top agency — restraint,
 hierarchy, type, space, micro-interaction; prefer **one strong quiet option** (Apple / Linear
 restraint SoT) over stacking effects. **Stack:** addition on `RESEARCH_HCI` +
 `RESEARCH_BEFORE_ENHANCE` (Rule 2 A) + Check 7 + Check 8 (`VISUAL_STEP_STILLS`, **LIVE** via
 `#15` / `d61f4c1`) — **not** a replacement; does not reopen Check 8. **FAIL (Cos craft before
 Adv):** cheesy effects; spectacle as craft (particle beads / marble pulses / confetti /
 glow-as-craft / cheesy “alive”); wallpaper rain over labels; jargon scoreboards; checklist
 stills without agency-level composition; stacking effects to prove “alive.” **Do-not-copy
 (named LIVE prohibition content):** particle beads / marble pulses / cheesy “alive” as status
 — scar AG **#39** tip `9b1bba2` pulse craft FAIL; correct = faint white colorization **within**
 the thin line. Cite RESEARCH_HCI **#38** @ `214ed5b`. **Sensor (fail-closed):** craft brief
 (restraint SoT + what NOT to do) before stills; stills PR must include **written craft
 defense** (why clean; what rejected as cheesy). **Metric (fail closed):** Cos craft FAIL holds for
 listed spectacle patterns = **0**. Soft / deferred / tip / wiki-scar-only = **REJECTED**.
 **HOLD ACCEPT until Adv names the check** (`DESIGN_AGENCY_BAR`) then Cos ACCEPT merge. Do
 **not** mark LIVE until Cos ACCEPT MERGED SHA. Superseded alias `SPECTACLE_NOT_CRAFT` —
 absorb FAIL conditions under this id; do not ship a competing lock. **P0:** no
 secrets/keys/emails/PII/host paths. Out of scope: dashboard pixel implementation; amending
 #39 stills PNGs. SoT: `harnesses/ux.md`; adversarial-ux critic + CX / Evaluative pointers +
 flat `agents/ux-*` copies; adversarial-ux skill pointer; CoE + spec Section 5.2 index
 pointers.

- **Draft SoT: `RESEARCH_HCI` — not live / not effective until Cos ACCEPT merge.** Master's
 HCI craft bar for **every product Research seat** (AG, Ladders, [redacted product], Even Weather /
 EW, EvenCursor, Dungeon, and future product Research seats) — **Product UX Research only;
 not OpenClaw briefs; not AG-dashboard-only.** **Stack:** addition on
 `RESEARCH_BEFORE_ENHANCE` (Rule 2 A) — **not** a replacement; cite-real-screens still
 required. **Bar:** fundamentals **THEN** opened comps — type, space, hierarchy, gestalt,
 info-viz, Fitts / Hick / Jakob with craft analysis; expert comps opened and cited (for
 graph/splash work, Obsidian graph is first among equals when relevant); pack must **teach
 UX** senior-director composition. **FAIL:** screenshot collecting / completeness pack
 without craft analysis — no narrative pass. **Sensor (fail-closed):** `evidence.md` (or
 equivalent) must cite HCI fundamentals + opened screens, or **FAIL UX handoff**. **Metric
 (fail closed):** packs that hand off without that craft analysis = **0**. Soft / deferred / tip /
 wiki-scar-only = **REJECTED**. **HOLD ACCEPT until Adv names the check** (`RESEARCH_HCI`)
 then Cos ACCEPT merge. **P0:** no secrets/keys/emails/PII/host paths; no invented KPI
 numbers. Out of scope for this SoT write: dashboard look/stills pixels; Obsidian splash pack
 amendments. SoT: `harnesses/researcher.md`; adversarial-researcher critic Check 6 + Adv
 pointers (evidence-advocate / context-reviewer) + flat `agents/res-*` copies; desk-research
 / adversarial-researcher skill pointers; CoE + spec Section 5.0 index pointers.

- **Draft SoT: `SELF_AUDIT_LOOP` — not live / not effective until Cos ACCEPT merge.** Cos 6pm
 ET improve digest + AG standing self-audit routine (not a product UX Critic Check number; **no
 new sidebar persona**). **Cos CoE ownership (Paul/Cos LOCK; Adv confirm):** Team triad
 retro (feed) → AG seat drafts named unpaid SoT/plan (`id` / owner / metric / AC; project
 PMs ≠ AG constitution) → Adv challenges (does **not** author; `CRITIC_SEPARATE_STAMP`) →
 Cos ACCEPT → teams absorb next ship. Sensor remains unpaid item or `AUDIT_CLEAR`.
 **One-line FAIL:** FAIL if the periodic AG self-audit only nags (missing stills, `UNSET`
 `token_source`, missing retros, draft-as-law, wrong-surface gates) without opening a
 fail-closed named unpaid SoT/improve item; Paul/Cos having to hand-list meta-gaps = FAIL of
 this loop. **Why retro-only insufficient:** `RETRO_BEFORE_CLOSE` is post-epic/team-scoped —
 cannot catch standing AG gate drift between epics; digest-without-unpaid = nag theater.
 **Sensor (fail-closed):** each audit cycle produces BOTH (1) checklist vs live scars/locks
 (stills / `token_source` / retros / `LIVE_SOT` / `SURFACE_GATE` / Critic stamp) and (2) ≥1
 named unpaid improve/SoT item (`id` + owner + metric + AC) OR explicit `AUDIT_CLEAR` with
 evidence — drafted by the AG seat. Soft “we should…” / wiki tip / scar-without-unpaid =
 **REJECTED**. **Stack:** addition on daily improve digest + `RETRO_BEFORE_CLOSE` — not a
 replacement; audits the other five locks (`CRITIC_SEPARATE_STAMP`, `TOKEN_SOURCE_OR_BLANK`,
 `RETRO_BEFORE_CLOSE`, `LIVE_SOT_MERGED_SHA`, `SURFACE_GATE_MATRIX`) once SoT-live — this PR
 does **not** define those five. **Scope:** AG harness + Cos improve digest / self-heal —
 **not** OpenClaw briefs. **Metrics (fail closed):** Cos/Paul hand-recommended AG meta-gaps the
 last audit should have fail-closed = **0**; nag-only cycles (no unpaid item and no
 `AUDIT_CLEAR`) = **0**. **P0:** no secrets/keys/emails/PII/host paths in AG git or digest
 artifacts; no invented tokens. Soft / deferred / tip / wiki-scar-only = REJECTED. SoT:
 `harnesses/chief-of-staff.md`; digest pointer `docs/improve/README.md`; light Adv challenge
 pointer on universal-adversary.

- **Draft SoT: five Adv-named locks — not live / not effective until Cos ACCEPT merge.**
 Soft / deferred / tip / wiki-scar-only = **REJECTED**. P0: no secrets/keys/emails/PII/host
 paths in AG git. **HOLD ACCEPT until Adv PASS.** Exactly these five Adv-named locks. No
 invented tokens. No fan-out language. Check 8 / `VISUAL_STEP_STILLS` is already **LIVE** on
 main via `#15` / `d61f4c1` — this PR only cross-references stacks; does **not** reopen or
 rewrite Check 8.
 1. **`CRITIC_SEPARATE_STAMP`** — Slot: UX Critic output + adversarial-ux workflow (parallel
 QA Critic when QA gates); stamp-isolation over Checks 7–8 (**not** a new Check number).
 FAIL: Checks 7–8 lack a distinct Critic-labeled verdict artifact/run separate from Adv;
 silent dual-hat = FAIL. Sensor: Critic template filed as **CRITIC** (isolated); if no
 Critic bot, Adv runs critic.md second pass labeled CRITIC — not folded into ADV prose.
 Stack: Check 7 + Check 8 + `ADV_COMP_CRITIQUE` (Critic grades; Adv challenges). Scope:
 product UX jury; all product teams; not OpenClaw. Metric: Adv-only stamps on Checks 7–8
 = **fail closed**.
 2. **`TOKEN_SOURCE_OR_BLANK`** — Slot: Critic Check 1 + `design.md` `token_source` /
 improve-digest path. FAIL: Check 1 PASS while UNSET; invented tokens; blank-as-measured.
 Sensor: Check 1 = UNVERIFIABLE (never PASS) when UNSET; digests cite named source or
 **BLANK**. Stack: on Check 1 / design.md — does not invent token feed or replace
 `RESEARCH_BEFORE_ENHANCE`. Scope: AG improve digests + product UX Check 1; not OpenClaw.
 Metric: invented or blank-as-measured token reports = **fail closed**.
 3. **`RETRO_BEFORE_CLOSE`** — Slot: Cos/CEO close gate (not a Critic Check). FAIL: epic
 CLOSED / next-pack GO without triad retro in AG git. Sensor:
 `projects/<team>/retros/<epic-or-date>.md` (well / didn't / improve); tip/scar/wiki ≠
 sensor. Stack: after ship/close; does not replace Check 7/8 / `RESEARCH_BEFORE_ENHANCE`.
 Scope: all product teams; OpenClaw keeps scars (do not force product retro path). Metric:
 Cos-closed epics missing retro = **fail closed**.
 4. **`LIVE_SOT_MERGED_SHA`** — Slot: Studio→AG→Cos ACCEPT + Adv challenge. FAIL: treating
 intake / open PR / draft / muse as live Paul LOCK; only Cos ACCEPT + merged SHA is live
 (precedent `#13` intake ≠ SoT). Sensor: cite merged SHA/PR; draft headers say not live /
 not effective until Cos ACCEPT merge. Stack: liveness only — does not replace Check 7/8 /
 `RESEARCH_BEFORE_ENHANCE` content. Scope: AG harness writes + all product teams + OpenClaw
 ops citing AG law. Metric: teams executing unmerged intake as SoT = **fail closed**.
 5. **`SURFACE_GATE_MATRIX`** — Slot: Scope lines in ux/qa harnesses, Critic Checks 6/7/8,
 OpenClaw brief docs. FAIL: product-UX gates on OpenClaw briefs, or omitted on product
 surfaces. Matrix: Product UX = `RESEARCH_BEFORE_ENHANCE` + Check 7 + Check 8 +
 `ADV_COMP_CRITIQUE`; OpenClaw = `MORNING_BRIEF_CITE_OR_BLANK` only. Sensor: named Scope
 lines; wrong-surface FAIL explicit. Stack: binds existing stacks — replaces none. Scope:
 all teams. Metric: OpenClaw briefs failed for missing userflows/stills = **fail closed**.
 SoT: `harnesses/ux.md`, `harnesses/qa.md`, `harnesses/ceo.md`, `harnesses/chief-of-staff.md`;
 adversarial-ux/qa critics + flat copies; `design.md`; improve README/template; workflow
 skills; OpenClaw README + morning-brief scar cross-ref; Ladders retros README pointer.

- **Draft SoT: `VISUAL_STEP_STILLS` (Critic Check 8) — not live / not effective until Cos
 ACCEPT merge.** Fail-closed visual step-stills sensor for product UX ship / Look / visual
 pack gates. Sensor: `docs/epics/<slug>/qa/visual-stills/` + index
 `docs/epics/<slug>/qa/visual-qa.md` with per-step **mobile and desktop** screenshots (scar
 page ≠ sensor). QA owns sensor; UX Critic Check 8 grades presence + named FAIL bullets;
 QA Critic verifies sensor before gate; Adv opens best-in-class comps and files ≥1 OUR hole
 + ≥1 COMP hole + do-not-copy (theme-on-CTA-row, dynamic-banner CLS) — comps ≠ gospel.
 **Stack:** addition on `RESEARCH_BEFORE_ENHANCE` (Rule 2 A) + Critic Check 7 +
 `ADV_COMP_CRITIQUE` — not a replacement. **Metrics (fail closed):** visual QA packs / ship gates
 without step stills (mobile+desktop) = **0**; marketing/dashboard layout-shift Highs
 (primary CTA wrap, chrome colliding with CTA, theme control stealing CTA row) = **0**.
 **Scope:** product UX surfaces only (marketing + app chrome); **all** product UX teams
 (Ladders, Even Weather, [redacted product], Dungeon, JEEP, EvenCursor, Nearby Places, G2, and any
 other product UX team) — **not** OpenClaw briefs. **P0:** no secrets/keys/emails/PII/host
 paths in AG git. **Named FAIL (no etc.):** CLS/layout (CTA wrap/shift when theme/chrome
 loads; reserved-space missing for theme control; dynamic banner pushes hero CTA); Fitts
 (CTA shrinks/splits; theme toggle in CTA cluster); Hick (>1 competing primary in same thumb
 zone without hierarchy); Jakob (mobile↔desktop chrome inconsistency without documented
 exception); Miller (NOTE only unless stills show unlabeled overflow chrome crowding the
 step). Soft / deferred / tip / wiki-scar-only = REJECTED. SoT: `harnesses/qa.md`;
 adversarial-ux critic Check 8 + flat `agents/ux-critic.md`; adversarial-qa critic sensor
 check + flat `agents/qa-critic.md`; light Adv pointers (cx-advocate / evaluative-uxr /
 quality-advocate).

- **UX harness lock: Mermaid userflows + JTBD before Eng handoff (Cos ACCEPT B).**
 Named Critic Check 7 at UX→Eng gate: require `userflows.md` (Mermaid: entry, success,
 key error/empty, exits) + `jtbd.md` + Research cite, **or** explicit `NO_RESEARCH` →
 escalate to human (do not invent). Check 7 is **stacked on `RESEARCH_BEFORE_ENHANCE`**,
 not a replacement. Metric: UX epics missing those at Critic = **fail closed**. Scope:
 product UX epics only — **not** OpenClaw briefs. P0: no PII/secrets in AG git. Stop
 conditions for missing/misaligned artifacts; CX Advocate + Evaluative UXR treat Mermaid
 flows as the flow under review and note when not checked vs research. SoT:
 `harnesses/ux.md`; adversarial-ux critic/advocates + flat `agents/ux-*` copies.
 (Unrelated to PR #13 intake.)

- **`RESEARCH_BEFORE_ENHANCE` (Rule 2 A) + `ADV_COMP_CRITIQUE` standing lock** — hard gate
 (soft / deferred Look gate REJECTED). Named sensors `cite-real-screens` +
 `adv-comp-critique` fail-closed (a scar/wiki page is not the gate). Required artifact
 `docs/epics/<slug>/evidence.md` (or stills index) with real-screen source URLs + what the
 pixels show, before PM→UX brief / before first story. Jury (Critic, CX Advocate, Evaluative
 UXR) must open cited screens; **jury artifact before Pack/Look** must name opened screen IDs
 or URLs (no secrets/keys/emails/host paths) **and** ≥1 hole in our UI **and** ≥1 hole in a
 competitor screen **and** one do-not-copy gap — Pack/Look FAIL if no opened-screen cites.
 Comps are not gospel. Metric: enhancement packs without cited real-screen evidence = fail closed.
 Scope: product UX/Research + adversarial UX jury (not OpenClaw morning-brief). SoT:
 `constitution/domains/ux.md`, `constitution/domains/researcher.md`,
 `projects/_standing/scars/research-before-enhance.md`, adversarial-ux agents + desk-research
 pointers. P0: no keys, tokens, emails, PII, absolute host paths, or private operator data.
- **OpenClaw morning-brief cite-or-blank scar SoT** (docs only;
 `MORNING_BRIEF_CITE_OR_BLANK` Rule 2 A; `validate-brief-grounding.py`
 fail-closed before Discord) at
 `projects/openclaw/scars/morning-brief-cite-or-blank.md`. CLOSED harness scar
 for invented meetings after KICK_BACK+rewrite; OpenClaw morning briefs only.
- **OpenClaw bridge-guard false-clobber scar SoT** (docs only; structural vs
 content check named) at
 `projects/openclaw/scars/bridge-guard-false-clobber.md`.
- **Dashboard public + admin split.** Same Vercel deploy (`dashboard/`): public
 marketing at `/` (KPI strip, Get AG CTA, traction gated by
 `data/traction.json`); admin at `/admin/*` behind Auth.js v5 Google SSO with
 allowlist (`noreply address` + optional `ADMIN_EMAILS`). Admin shows
 honest Baseline / unpaid token placeholders, cycle-time tables, improve
 report detail, raw traction (including below `minVisible`), and anonymized
 scar index — never invents live token/$ numbers; no Studio PII.
- **OpenClaw pin-enforce scar SoT** at
 `projects/openclaw/scars/pin-enforce-version-drift.md` (docs only; Cos
 canonicalizes on OpenClaw Eng’s draft, not Bridge paste). CLOSED harness scar
 for silent downgrade via nightly `npm update -g openclaw` vs pin; documents
 the pin-enforce process lock only — no framework-policy invention beyond that
 lock.
- **Continuous improve reporting path.** Daily markdown reports live under
 `docs/improve/` (README with KPI rules, `_template.md`, dated stubs). KPIs
 must be measured or method-estimated — never invented. A public Next.js
 marketing dashboard under `dashboard/` (UI SoT = Meta Astryx:
 `@astryxdesign/core` + `theme-neutral`) puts KPI strip/charts first, a loud
 Get AG CTA second, then changelog/contribute. Traction widgets are fully
 wired but gated by `data/traction.json` `minVisible` thresholds (hidden on
 launch). Vercel-ready; Cos/Paul must make the marketing surface public.

- **Chief of Staff (Cos) for multi-team mode.** Setup wizard asks whether the
 operator will run more than one project/team at once; if yes, a Cos roster
 row is required. Cos is the human funnel: only Cos surfaces decisions to the
 human; Cos owns the Section 13 morning queue in multi-team mode; Cos triages
 P0/P1 and enforces the daytime escalate; Cos watches governance and
 drafts amendment proposals (human still gates the constitution). Single-team
 mode unchanged: CEO → human for the morning queue. Harness:
 `harnesses/chief-of-staff.md`. Spec/comms/wizard deltas as recorded in the
 Cos proposal.
- **Cos escalation behavior is wizard-configured, not hardcoded.** Two new
 setup-wizard questions: quiet-hours P0 behavior (`interrupt` to break through
 via messaging, or `defer` to queue at the head until quiet hours end) and the
 daytime escalate SLA in hours (default 4). Both land in `config/setup.md`.
 Operator's own quiet hours stay in local config; nothing personal ships in
 the build.
- **Vanilla handoff (ADR-0006, ADR-0007).** The framework is now environment-agnostic —
 adopters take the constitution + harnesses as a loadable contract (no repo mirror).
 First real-team adoption: Ladders Grok Bot (2026-09-06).
- **Watchdog data-source abstraction (ADR-0007).** `stuck-review-watchdog.py` now
 supports `--source paperclip` (default), `--source file --issues-file <path>` (JSON
 file or stdin), and `--source none` (disabled until an in_review backend exists).
 `collect_stuck` logic unchanged; backward-compatible.
- **Setup wizard data-source questions.** The wizard now asks where in_review issues
 and the verdict ledger live (`issue_source`, `issues_file`, `verdict_log`) and writes
 them to `config/setup.md`, so the watchdog + telemetry are configured at setup time.
- **Config-file fallback in watchdog + telemetry.** Both scripts read the data-source
 config from `config/setup.md` when CLI flags / env are not set.
- **Local ticket/story system (`scripts/ticket.py`).** A built-in, file-based ticket
 base so a vanilla install works with NO external tracker (no Paperclip, no GitHub,
 no Linear). Create work items, track review state, record verdicts. Writes
 `runs/in_review.json` (feeds the watchdog) and `runs/verdicts.jsonl` (feeds
 telemetry), so the whole loop runs out of the box.
- **Wizard questions rewritten in plain language.** Every setup question now reads
 clearly to someone who doesn't know the framework (no jargon like "in_review",
 "verdict ledger", "epic", "autonomy ladder"). The wizard also auto-creates the
 default data files (`runs/in_review.json`, `runs/verdicts.jsonl`).

- `docs/spec-addendum-01.md` — Addendum 01 (Reversibility, Autonomy, Budgets, and Audit), ratified, committed into the repo so the repo copy is canonical and the Downloads copy is dead. Amends Sections 5, 6, 9, 10, 11, 13, 14 of `docs/agentic-governance-spec.md`. A9 and A10 are recorded open problems (not implemented).
- `docs/agentic-governance-spec.md`: added **Section 10.7 Reversibility as the approval line** (A1) — finish reversible work, stage and stop irreversible work; precedence over vetoes/mandatory escalation; adversarial agents unchanged.
- `docs/agentic-governance-spec.md`: added **Section 10.8 The autonomy ladder** (A2) — Levels 0-4, promotion earned on evidence, automatic demotion, config for starting level and clean runs per promotion.
- `docs/agentic-governance-spec.md`: added **Section 10.9 Declared retry budgets** (A3) — target/count/gap/escalation declared before work; bot does not set its own budget; repeated exhaustion is a rule problem.
- `docs/agentic-governance-spec.md`: added **Section 10.10 Cost attribution** (A7) — spend recorded per bot, not only per epic; unattributed spend marked rather than invented.
- `docs/agentic-governance-spec.md`: added **Section 10.11 Failure domains** (A13) — every node has a declared failure policy; never hide missing work; distinguish stalled from failed.
- `docs/agentic-governance-spec.md`: added **Section 10.12 Gates belong in architecture where architecture allows it** (A14) — three protection levels (unreachable/intercepted/instructed); config records which level applies per irreversible action class.
- `docs/agentic-governance-spec.md`: added **Section 13.5 Routine audit** (A4) — weekly receipt, three questions, verifier kill rate per adversary/role, bot is not sole judge of its own history.
- `docs/agentic-governance-spec.md`: **corrected Section 9.4** (A5) — the read-only persona line is documentation, not enforcement; the adversarial commit check is the real control; genuine isolation requires separate credentials.
- `docs/agentic-governance-spec.md`: added **Section 9.6 Config validation** (A8) — wizard validates before writing and refuses on contradictions; validation runs on every run; unvalidatable values stated as such. (Section 9.5, A6 BYOA, is deferred to a later pass.)
- `docs/agentic-governance-spec.md`: added to **Section 14** — **End-to-end validation before further extension** (A11, adoption prerequisite) and **When not to invoke the chain** (A15, adoption note).
- `harnesses/researcher.md`: created the **Research role harness** (A12.3) from the nine-section skeleton — establishes what is true before anyone plans against it; evidence pack to PM; bounded discovery loop; permitted plugins `universal`, `prompt`, `docs`, `researcher`.
- `docs/agentic-governance-spec.md`: added **Section 5.0 Research Harness** (A12) ahead of the PM harness — why the chain needs it, where it sits (CEO → Research → PM → UX → engineer → QA → CEO), the harness, bounded discovery loop, reduce-before-reasoning, degrade visibly, amendments, adversaries already exist.
- `docs/agentic-governance-spec.md`: applied the **A12.7 amendments** — Section 5.1 PM brief fields 3 & 4 must cite a finding from the evidence pack; Section 6 adds the Research edge (Research receives from CEO bot, hands to PM); Section 11 moves `researcher` to the Research role and UX loses read-only researcher access.
- `mcp/adversarial_mcp/setup_wizard.py`: added the **Addendum 01 config questions** (unanswered, operator answers through the wizard) — autonomy starting level + clean runs per promotion (A2), retry count + escalation on exhaustion (A3), audit cadence (A4), research discovery bounds (rounds without findings, round budget) (A12.4), and irreversible-action protection level per class (A14). Written to `config/setup.md`. A6 (BYOA) is deferred to a later pass.
- `docs/agentic-governance-spec.md`: Section 14 now points to `docs/spec-addendum-01.md` for the two recorded open problems (A9 ledger structure/growth, A10 rollback) — named, not resolved.
- `docs/spec-addendum-01.md`: recorded **A16, a third open problem** — harness bodies are duplicated between the spec and the harness files, no precedence rule exists, and the fix is either a precedence rule or generating one from the other. Recorded, not solved.
- `docs/spec-addendum-01.md`: recorded **A17, a fourth open problem** — this repo has no project repo, so every real change targets the governance repo, which bots cannot write; the read-only rule (9.4) and the engineer's obligation (5.3) cannot both hold for governance-repo work. Options: a separate project repo, an exception path with a human applying the change, or scoping the framework to exclude self-modification. Recorded, not solved.
- `docs/spec-addendum-01.md`: added **A18, a decided section** (not an open problem) — (1) acceptance rules need an artifact: every role that can reject upstream work records its acceptance decision (what it received, whether well-formed, why it proceeded despite a defect); (2) adversarial review covers intake, not only output: the Critic checks whether each role received input its harness permits and rejected if not; (3) the CEO harness amendment: turning an objective into a research question means restating a solution-framed objective as a problem, passing it through verbatim is not scoping (applies to Section 10 and A12.2).
- `harnesses/ceo.md` and `docs/agentic-governance-spec.md` (Section 10 + A12.2): amended per A18.3 — the CEO scopes research questions by restating a solution-framed objective as a problem.
- **A18.1 acceptance records** (Phase 1): every role that can reject upstream work now records its acceptance decision in the artifact it produces — what it received, whether it was well-formed against its inputs rule, and if it proceeded despite a defect, why. Added to Research (`evidence.md`), PM (`brief.md`), UX (`rationale.md`), engineer (`notes.md`), QA (`results.md`), and the CEO (calibration ledger, on QA's report). Updated in **both** copies (harnesses/*.md and inline in the spec) and kept byte-identical — 12 places touched (6 roles × 2 copies). The spec's Section 10 CEO harness previously lacked the "Required artifact format" section the harness file has; it was added to match (a pre-existing A16 divergence, not fixed beyond this section).
- `docs/spec-addendum-01.md`: added **A19, a decided boundary rule** — the Section 7 carve-out protects an adversarial agent's identity, not its check list. Identity is what the agent is and what it may never do; a check is what it verifies. Adding/removing/amending a check is procedure (permitted); changing what the agent is, may never do, or its authority to block is identity (forbidden). An amendment requiring rewording the identity section is not procedure.
- **A18.2 intake conformance** (Phase 2): added a fifth check (intake conformance) to all eight Critic files (4 plugin + 4 flat) — reads the acceptance record and asks whether the role received input its harness permits and, if not, whether it rejected. Same mechanical shape as the existing four checks. Flat bodies kept identical to plugin (only `name:` frontmatter differs). Identity sections untouched in all 8 (boundary rule satisfied).
- **Governance setup wizard** (`mcp/adversarial_mcp/setup_wizard.py`): conversational, exposed through the MCP server as `setup_wizard_start` / `setup_wizard_answer` (Section 9.3). Asks the operator's 13 questions natively with labeled options where bounded, writes `config/setup.md` and `config/roster.md`, and generates one persona block per roster row into `config/personas/` (Section 9.4 template). Re-runnable; absent/incomplete config is the unknown state, never defaulted. Built untested per operator instruction (interactive tooling down).
- `docs/agentic-governance-spec.md` — the ratified work order (`agent-harnesses.md`) committed into the repo (including the Section 7 constitutional-content carve-out). From this commit forward the repo copy is canonical; the Downloads copy is dead.
- **Agentic governance restructure** (governance-restructure branch) per ratified `agent-harnesses.md` work order:
 - Repo renamed `adversarial-agents` → `agentic-governance` (GitHub redirect from old name).
 - Governance layout: `constitution/`, `harnesses/`, `ledger/`, `config/`.
 - Five role harness files: `harnesses/pm.md`, `harnesses/ux.md`, `harnesses/engineer.md`, `harnesses/qa.md`, `harnesses/ceo.md` — using the Section 4 skeleton and Sections 5/10 content, with Section 11 plugin allowlists cross-referenced.
 - `config/roster.md` — empty roster table (Section 9.2 columns).
 - `ledger/queue.md` — human queue (Section 13).
 - `docs/communication.md` — communication rules (Section 6).
 - `docs/commit-discipline.md` — commit discipline (Section 8).
 - Constitution relocated `docs/Constitution.md` → `constitution/constitution.md`; calibration ledger `docs/Calibration.md` → `ledger/calibration-ledger.md` (git mv, history preserved); inbound reference in `docs/adr/0004-hard-vetoes.md` updated.
 - `docs/` retained as the in-repo wiki (no separate `wiki/` folder).
- Foundation for GitHub publication: LICENSE (MIT), SECURITY.md, CONTRIBUTING.md,
 AGENTS.md (repo operating rules), CHANGELOG.md, .gitignore.
- AUDIT.md — enterprise gap analysis + roadmap.
- CI validation workflow (`scripts/validate.py` + GitHub Actions) — lints frontmatter,
 checks naming uniqueness, validates structure and cross-references.

### Changed
- **Class A honesty flip — Check 9 / Check 10 / Cos memory LIVE after Cos ACCEPT [#64](https://github.com/paulthorson/agentic-governance/pull/64) @ `a9a4327`:** CoE Draft intake
 still listed Check 9 / `INITIATIVE_START_SEQUENCE`, Check 10 / `RELEASE_COMPLIANCE`, and Cos
 memory install ASK as Draft after Cos ACCEPT MERGED. Flip those rows to CoE Already LIVE citing
 `#64` @ `a9a4327`. Drop stale “draft until Cos ACCEPT” labels on related harness / template /
 index / spec pointers already on main. **Check 9 stays fail-closed** before Eng handoff.
 **Check 10 stays Cos checklist** — **NOT** fail-closed / stop-the-presses. Cos memory ASK
 (`private_git` OR `local_folder` at Cos seating) stays. No new checks invented. P0: no secrets.
- **UX Canvas contents honesty (Paul LOCK — absorb Gothelf; kill “contents TBD”):** **UX Canvas** =
 Jeff Gothelf [Lean UX Canvas V2](https://jeffgothelf.com/blog/leanuxcanvas-v2/) boxes **1–8 as-is**
 (external SoT for box definitions). Boxes: (1) Business problem statement (2) Business outcomes
 (3) Users (4) User outcomes and benefits (5) Solutions (6) Hypotheses (7) What’s the most
 important thing we need to learn first? (8) What’s the least amount of work to learn the next
 most important thing? Touched paths drop “contents TBD”; standing Check 9 owns Eng-handoff
 fail-closed. Absorb under LIVE UX Canvas name [#48](https://github.com/paulthorson/agentic-governance/pull/48)
 @ `e9b4827` / `DESIGN_SYSTEM_FIRST` [#45](https://github.com/paulthorson/agentic-governance/pull/45)
 @ `ead012f`.

- **Get AG Adv CONCERN amend (historical — files later removed):** Pay Adv CONCERNs on tip [#60](https://github.com/paulthorson/agentic-governance/pull/60) @ `86e98081` without absorbing unpaid counsel work. Paths were ``, `` (**removed** on release hardening; see Removed above).

- **LICENSE MIT → Apache-2.0 (Class A):** Replace root `LICENSE` with standard Apache License 2.0 text; Copyright (c) 2026 paulthorson (match prior copyright style). README license badge + Governance mention → **Apache-2.0** (public framework license for fork / remix / contribute).
- **Get AG — Paul LOCKs amend (historical — file later removed):** Amend that was applied to `` (**removed** on release hardening).
- **Adv CONCERN absorb (AG website UX Canvas SoT — unpaid from merged [#50](https://github.com/paulthorson/agentic-governance/pull/50) @ `6b24c4b`):** Amend
 `docs/initiatives/ag-website-ux-canvas.md` without inventing product policy: (1) cite
 Cos-signed Brand & Design Setup / design-system packet (Sage instrument brand;
 Advercase + Geist; Process Instrument in the Void hybrid; Direct founder voice) + Eng
 HOLD look/pixels until Cos craft + Paul yes on stills; screens only after this canvas;
 (2) Box 2 metric + direction per outcome (honest directions, no fake percentages);
 (3) Box 5 solutions as genuine options with one trade line each; (4) Box 3 users + Box 6
 hypotheses marked Cos-owned with Paul 2026-09-14 — Research Scope provenance unpaid.
 `adversarial-ux/README.md` Initiative LIVE pointer drops stale “contents TBD” and points
 at the filled SoT. No Brand & Design Setup constitution rewrite; no look/stills (#39/#26).

- **UX Canvas named next gate (Paul/Cos LOCK — no new check id):** **UX Canvas** is the
 **separate** next Initiative gate **after** Brand & Design Setup — **not** an alias of Brand
 & Design Setup. Sequence: Research Scope → hunt → Brand & Design Setup → **UX Canvas**
 (before screens; contents TBD) → Check 7/8 stills / Eng. Name the gate only; do not invent
 canvas contents or a new Critic Check. Absorb into harness + design-system sensor + CoE/spec
 pointers under LIVE `DESIGN_SYSTEM_FIRST` [#45](https://github.com/paulthorson/agentic-governance/pull/45)
 @ `ead012f` + Brand & Design Setup docs [#46](https://github.com/paulthorson/agentic-governance/pull/46)
 @ `cdf1c41`.
- **Adv CONCERN absorb (`DESIGN_SYSTEM_FIRST` / Brand & Design Setup — no new check id):**
 Research cites must be **diverse** + **business-model-matched per project**; **FAIL** fixed AG
 comps (Pentagram/500/AXM) as all-teams default / copy-paste across teams; sensor requires cites
 that **state why this set matches this product’s model** and **why it is diverse** (not one
 peer); name walkthrough **Brand & Design Setup** once in harness heading. Also: **Research
 Scope** (Paul LOCK plain-English) Q1–Q8 wizard before comps hunt — no new check id.
- **LIVE tidy:** `DESIGN_SYSTEM_FIRST` (**LIVE** `#45` / `ead012f`), `DESIGN_AGENCY_BAR`
 (**LIVE** `#43` / `7e9e0b6`), `RESEARCH_HCI` (**LIVE** `#38` / `214ed5b`) — remove stale
 “draft until Cos ACCEPT” labels; move to CoE Already LIVE.
- **`DESIGN_SYSTEM_FIRST` plain-English name (Paul LOCK):** **Brand & Design Setup** — early
 Initiative Cos walkthrough. Map that human/agent name onto the check in `harnesses/ux.md`,
 `adversarial-ux/assets/templates/design-system.md`, CoE + Critic table rows. Check id
 unchanged (`DESIGN_SYSTEM_FIRST`).
- **`DESIGN_SYSTEM_FIRST` / Brand & Design Setup — fresh comps (Paul LOCK):** Research gathers
 a **FRESH diverse** comps set for **each** project’s Brand & Design Setup, **matched to that
 project’s business model**. Do **not** treat Pentagram / 500 / AXM as an all-teams default
 (AG-site-specific). Comp cites **internal only** (never public chrome). Absorbed into
 `harnesses/ux.md` + `harnesses/researcher.md`, design-system template, CoE + Critic rows.
 Check id unchanged (`DESIGN_SYSTEM_FIRST`).

- `docs/adr/0004-hard-vetoes.md`: references updated to `constitution/constitution.md` and `constitution/vetoes.md`.
- `mcp/adversarial_mcp/server.py`: `get_constitution` reads `constitution/domains/<domain>.md`; `REPO_ROOT` now resolves relative to `server.py` (rename/clone-anywhere safe); `get_standard` fixed via glob of exactly one standard file per plugin (was reading nonexistent `references/standard.md` and silently returning empty for all 12 domains since the MCP server shipped 2026-08-26).
- `mcp/adversarial_mcp/server.py`: `run_review` and `record_verdict` now tag verdict-log records with a `source` field (`app` by default; tests pass `source="smoke_test"`); `query_verdicts` gained a `source` filter so test/automation records can be excluded from the real-review log (runs/verdicts.jsonl).
- `mcp/adversarial_mcp/setup_wizard.py`: fixed a bug where the roster never completed — `_is_repeated_pending` compared the `__DONE__` sentinel as a list slice when it is stored as a string, so the roster looped forever and the wizard never finalized. Now compares the stored string correctly; verified end-to-end (writes `config/setup.md`, `config/roster.md`, and one persona block per roster row).
- `scripts/smoke_test_mcp.py`: hardens the MCP smoke test — (1) wired into CI (`.github/workflows/validate.yml` `tests` job); (2) under a Python without `mcp` it now prints a clear message naming the interpreter to use and exits non-zero instead of a raw `ModuleNotFoundError`; (3) `run_review` in the per-domain loop now passes `source="smoke_test"` so its records are filterable, and `query_verdicts` is checked for errors only (an empty verdict history is a valid state).
- `harnesses/ceo.md`: removed the restriction "Read access across everything belongs to the adversarial agents, not to the CEO" from the Inputs section — not in the spec, and the CEO reads the constitution, harness, config, and ledger by definition. The adversarial agents' read access is stated in Section 12 without a counterpart denial here.
- **Migration brief (Section 7):** added carve-out — Phase 3 does not touch `references/constitution.md` in any plugin (constitutional content, not capability).
- **Spec correction:** the Section 4 skeleton lists eight harness sections, but every harness carries a ninth — the Section 11 plugin allowlist. The allowlist is legitimately part of a harness; the spec (not the harnesses) is wrong. Noted for spec fix.

### Removed
- **[redacted] Get AG (Paul LOCK release):** Deleted ``, ``, and empty `docs/legal/`. Settled posture: free/open source Apache-2.0; **no acceptance gate**; LICENSE is the only use governor. **No replacement** Terms/privacy/warranty text. Cross-links in docs/initiatives, `docs/README.md`, dashboard README, and capability report §12.7 updated accordingly.

### Fixed
- `docs/spec-addendum-01.md` — **A16 self-contradiction caught and fixed.** A decision about where validation records live was recorded as DECIDED in `docs/proposals/a17-validation-record-home.md` while §A17 still said "Not decided. Do not implement." — two copies of a governance rule disagreeing, with no precedence rule. This is exactly the A16 open problem, occurring inside the file where A16 is written down. The fix renumbered the validation-record decision as **A20** (decided, distinct from A17), kept A17 open on its actual subject (no project repo for governance-repo work), renamed the proposal file to `a20-validation-record-home.md`, and recorded the occurrence in the A16 section as evidence the duplication problem is real and already biting.

### Moved
- `docs/Constitution.md` → `constitution/constitution.md` (git rename).
- `docs/Calibration.md` → `ledger/calibration-ledger.md` (git rename).
- `docs/Vetoes.md` → `constitution/vetoes.md` (git rename). The veto principle is now stated once, in `constitution.md` Rule 1; `vetoes.md` points to Rule 1 and keeps only its unique operational content (domain table, mechanism, mechanical enforcement, rationale). Inbound references updated.
- 12 per-domain constitutions `adversarial-<domain>/references/constitution.md` → `constitution/domains/<domain>.md` (git rename, no rule text changed). Constitutional content moved out of capability folders; `get_constitution` repointed to the new path and verified for all 12 domains.

## [0.1.1] — 2026-09-11

### Added
- **Ladders epic retrospectives as SoT** under `projects/ladders/retros/`
 (Paul LOCK 2026-09-11). Filed triad retros for `migration-drift-gate` and
 `marketing-landing` (went well / didn't / improve only). Optional mirrors
 elsewhere OK later; this tree is canonical. Docs only — no framework-policy
 change.

## [0.1.0] — 2026-08-26

### Added
- Five adversarial domain plugins:
 - `adversarial-ux` — user experience (critic, cx-advocate, evaluative-uxr; 10 skills)
 - `adversarial-engineer` — engineering (critic, ops-advocate, reliability-reviewer; 9 skills)
 - `adversarial-qa` — testing/release (critic, quality-advocate, edge-case-reviewer; 8 skills)
 - `adversarial-researcher` — research/evidence (critic, evidence-advocate, context-reviewer; 8 skills)
 - `adversarial-universal` — catch-all (universal-adversary; 6 skills)
- Each plugin: constitution, domain standard, personas, calibration ledger, decision-record
 + calibration-entry templates, commands.
- Consolidated flat layer: 13 namespaced agents + 45 namespaced skills.
- Cursor + Claude Code wiring (agents + skills symlinks).
- Paperclip wiring: 5 adversarial agents + mandatory-review rule in 8 domain agents.

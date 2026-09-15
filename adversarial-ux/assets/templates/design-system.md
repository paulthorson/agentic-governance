# Brand & Design Setup — Initiative packet (`DESIGN_SYSTEM_FIRST`)

**LIVE** — Cos ACCEPT merged [#45](https://github.com/paulthorson/agentic-governance/pull/45)
@ `ead012f`. Soft / deferred / tip / wiki-scar-only = **REJECTED**. Cos LOCK Paul. Check id:
`DESIGN_SYSTEM_FIRST`.

Copy this template into the Initiative packet as `design-system.md`. Research × UX fill it
together. Complete **Research Scope** (Q1–Q8) **before** the comps hunt. **Cos signs Brand &
Design Setup** before any web/UI pixels, stills, or screens. Next gate after Brand & Design
Setup: **UX Canvas** (Gothelf Lean UX Canvas v2 boxes 1–8 as-is — [Gothelf external SoT](https://jeffgothelf.com/blog/leanuxcanvas-v2/);
before screens — **separate** gate, **not** an alias of Brand & Design Setup). Then screens /
Check 7/8 stills / Eng. Standing Eng-handoff sensor: Check 9 / `INITIATIVE_START_SEQUENCE`
(**LIVE** [#64](https://github.com/paulthorson/agentic-governance/pull/64) @ `a9a4327`; **QA + Cos** stamp). Engineering follows signed craft — not the
reverse. Cite [#64](https://github.com/paulthorson/agentic-governance/pull/64) @ `a9a4327` + [#48](https://github.com/paulthorson/agentic-governance/pull/48) @ `e9b4827` +
[#46](https://github.com/paulthorson/agentic-governance/pull/46) @ `cdf1c41` +
[#45](https://github.com/paulthorson/agentic-governance/pull/45) @ `ead012f`.

**Paramount:** Design, Experience, and Branding are paramount — not optional polish after Eng.
Design system + Experience + Branding **lead** Initiative; engineering follows signed craft.

**Fresh comps (Paul LOCK — Research owns):** Research cites must be **diverse** and
**business-model-matched per project**. Gather a **FRESH** set for **this** project — **not**
one peer, **not** a fixed AG comps list copy-pasted across teams. Do **not** reuse
Pentagram / 500 / AXM as an all-teams default — those were **AG-site-specific**. Comp cites
are **internal only** (never public chrome). Cites must **state why this set matches this
product’s business model** and **why the set is diverse**.

**Stack:** `DESIGN_AGENCY_BAR` (**LIVE** `#43` / `7e9e0b6`) + `RESEARCH_HCI` (**LIVE** `#38` /
`214ed5b`) + `RESEARCH_BEFORE_ENHANCE` + Check 7 + Check 8 + Check 9 /
`INITIATIVE_START_SEQUENCE` (**LIVE** `#64` / `a9a4327`) — addition, not replacement.
Agency design thinking (`DESIGN_AGENCY_BAR`) remains the permanent UX brain for every product
UX seat.

**P0:** No secrets, keys, emails, PII, or absolute host paths.

```yaml
initiative: UNSET
cos_signed: no
cos_signed_at: UNSET
research_cite: UNSET
research_scope_complete: no
ux_owners: []
research_owners: []
```

---

## 0. Research Scope (required — before comps hunt)

Plain-English name: **Research Scope**. Folded into `DESIGN_SYSTEM_FIRST` (no new check id).
Missing answers = FAIL. Copy-pasting another team’s Scope = FAIL.

| # | Question | Answer |
|---|---|---|
| Q1 | Business model | |
| Q2 | Category | |
| Q3 | Audience | |
| Q4 | Offer / promise | |
| Q5 | Craft bar (what good looks like) | |
| Q6 | Anti-patterns | |
| Q7 | How many comps + diversity bar | |
| Q8 | Where to look (if blank, Research suggests: Mobbin, live sites, apps, …) | |

---

## 1. Tokens

Named color, radius, elevation (and related) tokens. No raw values in later stills/specs
without a token name.

| Token | Value / ref | Notes |
|---|---|---|
| | | |

## 2. Type

Type scale, weights, line-height, and usage rules.

| Role | Token | Notes |
|---|---|---|
| | | |

## 3. Space

Spacing scale and layout rhythm.

| Token | Value / ref | Notes |
|---|---|---|
| | | |

## 4. Motion

Duration, easing, and when motion is allowed vs quiet.

| Token | Value / ref | Notes |
|---|---|---|
| | | |

## 5. Brand / do-not

Brand marks, palette intent, and named **do-not** (spectacle patterns, wrong chrome, etc.).

- Brand marks / lockups:
- Do-not (named prohibitions):

## 6. Experience principles (required)

Interaction, hierarchy, and journey principles that lead Initiative craft. Missing = FAIL
under `DESIGN_SYSTEM_FIRST`.

- Principle 1:
- Principle 2:
- Principle 3:
- Anti-principles (what Experience must not become):

## 7. Brand Voice (required)

Tone, vocabulary (**lexicon**), headline patterns, and narrative drill-down voice. Name
**Brand Voice** explicitly. Missing this section = FAIL under `DESIGN_SYSTEM_FIRST`.

### Tone
- What we sound like:
- What we never sound like:

### Lexicon — words we use
-

### Lexicon — words we never use
- (Initiative-specific)
- **Standing ban (`AI_SLOP_COPY_FAIL` — draft until Cos ACCEPT):** examples — not exhaustive
  (Brand Voice judgment) — delve, unlock, elevate, seamless, robust, leverage, empower,
  journey, revolutionize, cutting-edge; twin-attribute cadence; synthetic brochure / AI-slop
  pitch. **Bar:** Human / Substack / Direct founder voice only on visitor/user-facing product
  surfaces. Metric: visitor/user-facing surfaces shipping AI-slop = **fail closed**. Stacks
  `DESIGN_AGENCY_BAR`. Not OpenClaw.

### Headline patterns
- Pattern A:
- Pattern B:
- Anti-patterns:

### Narrative drill-down voice
How copy deepens from splash → section → detail without changing character:

-

## 8. Audience / promise (required)

Who this Initiative speaks to, and the promise we keep. Missing = FAIL.

- Primary audience:
- Secondary audience (if any):
- Promise (one sentence):
- Out of promise / not for:

## 9. Information-design rules (required)

**Measured-only; marks stay marks.** Missing or violated = FAIL.

- **Measured-only:** Numbers, KPIs, and claims in UI/copy cite a measured source or are labeled
  **BLANK** / not measured. No invented metrics. No blank-as-measured.
- **Marks stay marks:** Brand marks, status marks, and data marks keep their defined meaning;
  do not restyle marks into decoration, spectacle, or ambiguous chrome.
- Other info-design rules for this Initiative:

| Rule | Held when | FAIL when |
|---|---|---|
| Measured-only | Cited source or BLANK | Invented / blank-as-measured |
| Marks stay marks | Mark meaning unchanged | Mark used as decoration / spectacle |

## 10. Research cite (required)

Path or ID of the Research pack that co-authored this system (HCI / evidence). Solo UX or
solo Research look = FAIL.

- Research cite:
- Research × UX collab note:

## 11. Fresh comps (required — Research owns)

**FRESH diverse** comps for **this** project, matched to **this** project’s business model.
**Not** one peer. **Not** fixed AG comps (Pentagram / 500 / AXM) as all-teams default or
copy-paste across teams. Cites are **internal only** — never public chrome.

- Business model (one line):
- **Why this set matches this product’s model** (required):
- **Why this set is diverse** (required — not one peer):
- Comps (diverse; opened + craft-read):

| Comp | URL / ID (internal) | Business-model fit | Diversity role | Craft note |
|---|---|---|---|---|
| | | | | |

- Not AG-site default / not copy-paste across teams (Pentagram / 500 / AXM): **held**
- Cites internal-only (not public chrome): **held**
- Research Scope complete before hunt: **held**

## Cos stamp

- Cos ACCEPT of this Brand & Design Setup `design-system.md`: **yes | no**
- Next gate after this stamp: **UX Canvas** (Gothelf Lean UX Canvas v2 boxes 1–8; before screens — not an alias)
- Then screens / Check 7/8 stills / Eng (Check 9 / `INITIATIVE_START_SEQUENCE` fail-closes Eng handoff — **LIVE** [#64](https://github.com/paulthorson/agentic-governance/pull/64) @ `a9a4327`; QA + Cos stamp)
- Stamp note:

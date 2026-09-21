# Design Standard

The token and pattern layer the Critic checks against. This file ships with placeholders. Replace
them with the real design system before the Critic's compliance check means anything.

Until this file is filled in, the Critic reports token compliance as **UNVERIFIABLE** rather than
passing it. Do not let an unfilled file read as a pass.

### Draft lock: `TOKEN_SOURCE_OR_BLANK` (not live / not effective until Cos ACCEPT merge)

Soft / deferred / tip / wiki-scar-only = **REJECTED**.

- **Id:** `TOKEN_SOURCE_OR_BLANK`
- **Slot:** Critic Check 1 Tokens + this file's `token_source` / improve-digest path.
- **FAIL:** Check 1 PASSes while `token_source` UNSET; improve/report numbers lack a named
  source; tokens invented; blank treated as measured = FAIL.
- **Sensor:** `token_source` below; Check 1 = **UNVERIFIABLE** (never PASS) when UNSET; digests
  cite a named source or label **BLANK**.
- **Stack:** On Check 1 / this file — does not invent a token feed or replace
  `RESEARCH_BEFORE_ENHANCE`.
- **Scope:** AG improve digests + product UX Critic Check 1; **not** OpenClaw.
- **Metric:** Improve reports with invented or blank-as-measured tokens = **fail closed**.
- **P0:** Keep private operator data out of AG git.

---

## How to point this at a real system

Pick one and delete the rest:

- **Local repo.** Set `token_source` below to a **repo-relative** path, for example
  `packages/tokens/tokens.json`. Agents read that file directly. Do not commit absolute host
  paths.
- **Figma.** Set `token_source` to a Figma file URL and use the Figma MCP tools
  (`get_variable_defs`, `get_design_context`) to pull variables at run time.
- **Inline.** Paste the token table into this file and set `token_source: inline`.
- **Blank / unset.** Leave `token_source: UNSET`. Check 1 stays **UNVERIFIABLE** — never PASS.
  Improve digests must label token KPIs **BLANK** (not measured), never invent numbers.

```yaml
token_source: UNSET
design_system_name: UNSET
last_verified: UNSET
```

`token_source: UNSET` is the honest blank. It is **not** a measured token feed.
---

## Token categories the Critic checks

For each category, the Critic verifies that the submitted design names tokens rather than raw
values, and that every named token exists in the source.

| Category | Example token names | Fails when |
|---|---|---|
| Color | `color.text.primary`, `color.surface.raised` | Raw hex appears in a spec |
| Type | `type.body.md`, `type.heading.lg` | Font size given in px with no token |
| Space | `space.100`, `space.400` | Arbitrary margins, one-off gaps |
| Radius | `radius.sm`, `radius.pill` | Mixed radii inside one component group |
| Elevation | `elevation.raised`, `elevation.overlay` | Shadow values written by hand |
| Motion | `motion.duration.fast`, `motion.ease.standard` | Durations invented per component |

---

## Component rules

1. Use an existing component before proposing a new one. A proposed new component needs a line
   in the decision record saying which existing component was rejected and why.
2. A variant that exists in the system is used as-is. Visual tweaks to a system component are a
   Critic flag.
3. Every interactive element declares its states: default, hover, focus, active, disabled,
   loading, error, empty.

## Accessibility floor

These are not aspirations. A miss is a Critic flag, and a miss in an irreversible flow is an
Advocate blocker.

- Text contrast meets WCAG 2.2 AA: 4.5:1 body, 3:1 for large text and UI boundaries.
- Every interactive element is reachable and operable by keyboard, in a visible order that
  matches the visual order.
- Focus is always visible and never removed without a replacement that meets contrast.
- Target size is at least 24 by 24 CSS pixels, with spacing when smaller than 44.
- Color is never the only carrier of meaning.
- Every input has a programmatic label. Errors are announced, not only colored.
- Motion respects `prefers-reduced-motion`.

## Content rules

- No "please" in UI copy. No exclamation points.
- Error text says what happened and what to do next, in that order.
- Buttons name the action they perform. "Submit" and "Continue" are flags when a specific verb
  exists.
- Numbers, dates, and currency follow one format across the flow.

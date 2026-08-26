# Design Standard

The token and pattern layer the Critic checks against. This file ships with placeholders. Replace
them with the real design system before the Critic's compliance check means anything.

Until this file is filled in, the Critic reports token compliance as **UNVERIFIABLE** rather than
passing it. Do not let an unfilled file read as a pass.

---

## How to point this at a real system

Pick one and delete the rest:

- **Local repo.** Set `token_source` below to a path, for example
  `packages/tokens/tokens.json`. Agents read that file directly.
- **Figma.** Set `token_source` to a Figma file URL and use the Figma MCP tools
  (`get_variable_defs`, `get_design_context`) to pull variables at run time.
- **Inline.** Paste the token table into this file and set `token_source: inline`.

```yaml
token_source: UNSET
design_system_name: UNSET
last_verified: UNSET
```

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

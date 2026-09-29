# BYODS: Bring Your Own Design System

**BYODS** is the setup wizard's design-system step. After BYOA adoption, the
wizard records your visual foundation so new projects can start building
immediately instead of designing from scratch.

## The core idea

Most operators either have a design system already, want a proven codified
one, or have nothing and need a starting point. The wizard covers all three:

1. **i-have-a-link** — paste a link to your design system repo or docs.
   The wizard validates it looks like a URL and records it.
2. **choose-predefined** — pick a codified design system to start building
   immediately. Astryx (Meta's open-source, agent-ready system with MCP
   tooling for agentic IDEs) is the recommended default when agents author
   the UI. Also offered: Google Material Design, IBM Carbon, Adobe Spectrum,
   Atlassian Design System, Shopify Polaris, GitHub Primer.
3. **build-custom** — the wizard walks through the pieces with you:
   - **Fonts** — primary and secondary, from free Google Font
     recommendations (Inter, Roboto, Space Grotesk, …), or name your own
     with `custom`.
   - **Colors** — primary, secondary, tertiary as hex codes. No brand
     colors defined? Answer `help` and the wizard offers curated,
     contrast-checked starter palettes (every primary is text-safe at
     ≥ 4.5:1 on white, WCAG AA).
   - **Data-viz colors** — a color-vision-deficiency-safe (CVD) palette is
     recommended: Okabe–Ito, the standard colorblind-safe set. Or paste
     your own comma-separated hex codes.
   - **Brand voice** — six example styles (direct-founder, warm-expert,
     playful-challenger, minimal-luxury, technical-precision,
     community-coach), or `i-have-one-already`: paste sample text now, or
     type `later` and the wizard asks for it at the first project kickoff.
4. **skip** — no design system recorded.

## The color picker

The framework is conversational, so the "picker" is data the operator's
agent renders natively: the `design_system_palettes` MCP tool returns the
starter palettes, the CVD-safe viz set, font recommendations, brand voice
styles, and predefined systems as structured JSON. A client may render a
native color wheel and pass the chosen hex back through
`setup_wizard_answer()`; the wizard validates hex codes and records them.

## Default vs per-project

At the end of the section the wizard asks about scope:

- **default** — the recorded system (written to `config/design-system.md`)
  is what every new project starts from. Fast development: agents read it
  at kickoff (persona blocks point at it) instead of designing from zero.
- **per-project** — the BYODS questions are re-run at each project kickoff,
  case by case.

## Detail tokens: quick setup vs define-each

A custom build continues past voice with the rest of the codified tokens.
First the wizard asks: **quick** (recommended values, no further questions)
or **define-each** (walk through every token)?

| Token | Recommended (quick) | Define-each |
|---|---|---|
| Neutrals (bg/surface/text/muted/border) | Cool gray ramp | Pick warm-gray, true-neutral, or paste 5 hexes |
| Dark mode | Auto — light + dark ramps | light-only, dark-only, or paste 5 dark hexes |
| Corner radius | Rounded — 8px | sharp, pill, or custom (e.g. 6px) |
| Icon set | Lucide | Material Symbols, Heroicons, or custom |
| Logo / brand assets | — | link, `later` (kickoff), or `none` |
| Type scale | 12/14/16/20/24/32/48px | custom pixel list |
| Spacing grid | 8pt grid | 4pt grid or custom |
| Shadows / elevation | subtle | none, pronounced, or custom |
| Motion | subtle, 150–250ms ease-out, honors prefers-reduced-motion | none, expressive, or custom |
| Breakpoints | 640/768/1024/1280px | custom pixel list |

## Machine-readable tokens

Every build also writes `config/design-tokens.json` — W3C-DTCG-flavored
`$value`/`$type` tokens (colors, fonts, radius, spacing, shadows, motion,
breakpoints, icons, logo, brand voice) so agents and build tooling can
import the system directly instead of parsing prose. Link/predefined
sources write a reference entry pointing at the external system.

A per-project kickoff may always override the default: initiative-level
craft gates (`DESIGN_SYSTEM_FIRST`, Check 7/8, Cos stamp) still apply, and
the initiative packet's `design-system.md` wins for that project.

## Honest limits

The framework **records** the design system as config; it does **not**
pixel-enforce it in code. There is no automated check that a shipped UI
matches the recorded tokens — that is what the initiative-level craft
gates and human review are for. See
[`docs/capability-report.md`](../capability-report.md).

# AGENTS.md

Project-specific guidance for AI coding agents.

> **Localhost dashboard only** — UI SoT for this app is its declared design system in `package.json`. Not fleet / framework law.

<!-- LOCALHOST-UI-KIT:START -->
Localhost dashboard UI kit (declared in package.json) · components via configured CLI
CLI: run every command as `npx ui-kit <cmd>` (shown below as `ui-kit.`).

SETUP (once, in your app entry e.g. main.tsx) — without these, components render unstyled:
  import "<ui-kit>/reset.css";  /* actual package path in package.json */
  import "<ui-kit>/kit.css";  /* actual package path in package.json */

WORKFLOW — discover, don't guess. Before writing UI:
1. `ui-kit build "<idea>"` — START HERE: returns a kit (closest [page] + [block]s + [component]s). No args = full playbook.
2. `ui-kit template <name> [--skeleton]` — scaffold the [page]/[block]s it named, or study their layout. Templates are reference code.
3. `ui-kit component <Name>` — props + examples for every component you use.

RULES:
- No <div> — components do all layout/spacing, page frame included.
- Frame first: read `ui-kit docs layout` before writing any page or screen — page frame, region widths, breakpoint behavior.
- Dense data = rows (Table, List/Item), never Card-wrapped list items; Card is for standalone widgets. Status = StatusDot/Token; Badge = counts only.
- Custom styling: component props first; else style/className with tokens — var(--color-*|--spacing-*|--radius-*). No raw hex/px. (No StyleX/Tailwind compiler here — don't use xstyle/utility classes.)
- Tokens for every value (`ui-kit docs tokens`). Brand/accent belongs in the theme (`ui-kit theme list` / `theme add <slug>`, or `ui-kit theme template` for a custom one) — never override --color-* in :root.
- SELF-CHECK before you finish: re-read the file and replace any raw <div>/<span> layout, imported.css/@apply, or hardcoded value (#hex, 16px) with the component or a token (var(--color-*|--spacing-*|…)). If unsure a component/prop exists, run `ui-kit component <Name>` / `ui-kit search "<thing>"`; don't hand-roll CSS.

MORE CLI:
  search "<query>"   find any component / hook / doc / template / block
  component --list   163 components by category
  template --list    page + block recipes
  docs <topic>       browser-support, cli-integrations, color, elevation, getting-started, icons, illustrations, internationalization, layout, migration, motion, principles, shadcn-compatibility, shape, spacing, styling-libraries, styling, theme, tokens, typography, working-with-ai
  swizzle <Name>     eject component source for deep customization
  upgrade --apply    run after any UI kit or integration dependency bump
<!-- LOCALHOST-UI-KIT:END -->

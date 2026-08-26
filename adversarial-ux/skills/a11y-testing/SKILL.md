---
name: a11y-testing
description: Audit a design, flow, or implemented interface against WCAG 2.2 AA and report conformance findings with the specific success criterion, the location, and the remedy. Use in the adversarial-ux Develop phase before adversary review, and whenever someone asks about accessibility, WCAG, screen readers, keyboard navigation, contrast, or an a11y audit. Produces findings mapped to criteria, and clearly separates what was checked from what only a real assistive-technology run can confirm.
---

# Accessibility Testing

A pure function. Interface or spec in, conformance findings out. Every finding names a success
criterion, a location, and a remedy.

## Scope honesty, first

Say up front what kind of check this is:

- **Spec review**: reading a design description. Catches missing labels, missing states,
  contrast values given in the spec, keyboard paths that were never defined.
- **Code review**: reading markup. Catches semantics, roles, names, focus management.
- **Live run**: driving a real page. Catches actual tab order, actual announcements.

A spec review cannot confirm what a screen reader says. Never report a spec review as a
conformance pass. Report criteria the input could not cover under **Not checkable here**.

## Checklist, WCAG 2.2 AA

**Perceivable**
- 1.1.1 Non-text content has a text alternative; decorative images are hidden from AT
- 1.3.1 Structure is programmatic: headings, lists, tables, form groups
- 1.3.5 Inputs declare autocomplete purpose where applicable
- 1.4.3 Text contrast 4.5:1, large text 3:1
- 1.4.11 UI component and graphical object contrast 3:1
- 1.4.10 Reflow at 320 CSS px with no two-dimensional scrolling
- 1.4.12 Text spacing adjustable without loss of content

**Operable**
- 2.1.1 Everything operable by keyboard; 2.1.2 no keyboard trap
- 2.4.3 Focus order matches meaning; 2.4.7 focus visible
- 2.4.11 Focused element not entirely obscured by sticky content
- 2.5.7 Dragging has a single-pointer alternative
- 2.5.8 Target size at least 24 by 24 CSS px, or spaced

**Understandable**
- 3.2.2 No change of context on input alone
- 3.3.1 Errors identified in text; 3.3.2 labels and instructions present
- 3.3.3 Error suggestion offered; 3.3.7 no redundant entry
- 3.3.8 Accessible authentication: no cognitive function test without an alternative

**Robust**
- 4.1.2 Name, role, value exposed for every custom control
- 4.1.3 Status messages announced without focus change

## Output

```markdown
# Accessibility Findings: <subject>

## Check type
<spec review | code review | live run>, covering <what was available>

## Findings
| # | Criterion | Level | Severity | Location | Issue | Remedy |
|---|---|---|---|---|---|---|
| 1 | 1.4.3 | AA | blocker | <where> | <what fails, with values> | <specific fix> |

## Blockers
- <finding that prevents task completion for an AT user>

## Not checkable here
| Criterion | Why | What would check it |
|---|---|---|

## Passed
- <criteria verified, with how they were verified>
```

## Rules

- Cite the criterion number every time. "Bad contrast" without 1.4.3 and the measured ratio is
  not a finding.
- Give measured values where the input supplies them and say "not stated" where it does not.
  Never estimate a contrast ratio from a color name.
- A barrier that makes a task impossible is a blocker, not a concern, and gets referred to the
  CX-Quality Advocate.
- Never write "fully accessible" or "WCAG compliant". Report what was checked and what passed.

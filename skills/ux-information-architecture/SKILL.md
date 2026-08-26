---
name: ux-information-architecture
description: Produce the structure under a design: content inventory, grouping model, labels, navigation, and URL or route scheme, with the alternatives that were rejected. Use in the adversarial-ux Develop phase before any screen layout work, and whenever someone asks about navigation, taxonomy, menu structure, labeling, or where something should live. Produces a structure artifact with labeled trade-offs, never a screen design.
---

# Information Architecture

A pure function. Content and tasks in, structure out. No visual design, no layout, no component
choices.

## Method

1. **Inventory.** List every content type, object, and task in scope. Note volume: how many of
   each will exist at year one, and at year five.
2. **Find the organizing principle.** Try at least three, then pick and say why:
   - By object type
   - By task or job
   - By lifecycle stage
   - By audience
   - By frequency of use
3. **Group.** Build the hierarchy. Keep breadth over depth where scanning matters, depth over
   breadth where the vocabulary is well known to the audience.
4. **Label.** Use the words the user uses, taken from research where research exists. Where it
   does not, mark each label as unvalidated and say what test would validate it.
5. **Route.** Define the navigation model and the URL or route scheme. Say what is deep-linkable
   and what is not.
6. **Test the structure** against real questions: pick five things a user would look for and walk
   the path to each. Count the decisions on the way.

## Output

```markdown
# Information Architecture: <scope>

## Inventory
| Object / content | Volume year 1 | Volume year 5 | Owner |
|---|---|---|---|

## Organizing principle
Chosen: <principle>, because <reason>
Rejected: <principle>, because <reason>

## Structure
- Level 1
  - Level 2
    - Level 3

## Labels
| Label | Source | Validated |
|---|---|---|
| <label> | <research quote, existing product, invented> | yes / no, <test that would validate> |

## Navigation model
<primary, secondary, utility; what persists, what is contextual>

## Routes
| Path | Object | Deep-linkable | Auth required |
|---|---|---|---|

## Findability walkthrough
| A user looking for. | Path | Decisions on the way |
|---|---|---|

## Trade-off
This structure trades away <X> to get <Y>.

## Breaks when
- <the growth or content case that invalidates this structure>
```

## Rules

- Never invent a label from product vocabulary when a user word exists in the research.
- Every unvalidated label is marked. A tidy structure built on guessed labels is a guess with
  good posture.
- The "breaks when" section is required. Structures fail at scale and the failure point belongs
  in the record.
- No layout, no components, no visual hierarchy. Different skill.

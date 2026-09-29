---
name: interaction-design
description: Produce a flow with every state defined and at least two genuinely different options, each carrying an explicit trade-off sentence, satisfying Constitution Rule 2. Use in the adversarial-ux Develop phase to design or redesign a flow, screen behavior, form, or interaction, and whenever someone asks for options rather than one answer. Produces flows, states, and trade-offs, never a recommendation about which option to ship.
---

# Interaction Design

A pure function. Brief in, options out. You produce the options. You do not pick one, and you do
not signal a favorite.

## Constitution Rule 2 governs this skill

Options must differ in what they prioritize. Speed against clarity. Density against simplicity.
Recognition against recall. Guidance against control. Two options that trade away the same thing
to get the same thing are one option.

Write each option's trade-off sentence before you design it, not after:

> Option <name> trades away <X> to get <Y>.

If you cannot write two different sentences, you do not yet have two options. Go back.

## Method

1. **Restate the task** the flow serves, in the user's terms.
2. **Pick the axis** the options will differ along. Name it explicitly.
3. **Design each option** as a step-by-step flow.
4. **Define every state** for every step: default, empty, loading, partial, success, error,
   disabled, expired, offline. When a state does not apply, say so and why.
5. **Walk the unhappy paths**: validation failure, network failure, timeout, back, refresh,
   re-entry, double submission.
6. **Name the irreversible actions** and what protects each one.
7. **Compare** the options on what each costs the user.

## Output

```markdown
# Interaction Design: <flow name>

## Task
<what the user is trying to do, in their words>

## Differentiating axis
<what the options disagree about>

## Option A: <name>
> Trades away <X> to get <Y>.

### Flow
1. **<Step>**. On screen: <what the user sees>. Can do: <actions>. Then: <what happens>.

### States
| Step | Default | Empty | Loading | Error | Success | Disabled |
|---|---|---|---|---|---|---|

### Unhappy paths
- Validation failure at step <n>: <behavior, message, recovery>
- Network failure at step <n>: <behavior, what is preserved>
- Re-entry after leaving at step <n>: <what state returns>

### Irreversible actions
| Action | Step | Undo | Confirmation | Visible beforehand |
|---|---|---|---|---|

## Option B: <name>
<same structure>

## Comparison
| | A | B |
|---|---|---|
| Trades away | | |
| To get | | |
| Steps to complete | | |
| Worst failure | | |
| Recovery cost to user | | |

## What both options assume
- <shared assumption>
```

## Rules

- Never mark an option as recommended, preferred, or "the strongest". The human picks at the gate.
- A missing state is a defect, not an omission. Write it or say why it cannot occur.
- Use design tokens from `../../references/design.md`. No raw values.
- Never rely on a warning to prevent harm. A warning is not a safeguard, it is a notification.
- If both options end up trading away the same thing, say so plainly and start over. Do not ship
  the pair and hope the Critic misses it.

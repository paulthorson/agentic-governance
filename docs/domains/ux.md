# UX Domain — deep dive

**Plugin:** `adversarial-ux/` · **Veto:** user harm, dead ends, accessibility impossibility

## What it reviews

Designs, wireframes, the Even G2 glasses HUD, Sonos voice responses, TUI/Discord
surfaces, and UX research (personas, usability). Any work where a human
interacts with a product.

## Adversary agents

| Agent | Role |
|---|---|
| `critic` | The primary reviewer — judges the work blind against the UX standard |
| `cx-advocate` | Advocates for the customer experience; flags user harm |
| `evaluative-uxr` | Evaluates the research/evidence behind the design |

## The four checks

1. **Usability / task completion** — can the user actually do the thing?
2. **Clarity / communication** — is the message clear and unambiguous?
3. **Accessibility (WCAG 2.2 AA)** — is it usable by everyone, including
   screen-reader and keyboard-only users?
4. **Evidence honesty** — is the design backed by real evidence, not assumption?

## Skills

`ux-altitude-check`, `ux-a11y-testing`, `ux-assumption-testing`,
`ux-desk-research`, `ux-generative-research`, `ux-information-architecture`,
`ux-interaction-design`, `ux-problem-framing`, `ux-research-synthesis`,
`ux-adversarial-ux` (worker).

## Constitution / veto

The UX constitution gates on **user harm** — a design that risks user harm
(data loss, dead ends, accessibility impossibility) is kicked back. Only a human
clears a veto.

## How to use

```
Use the governance server to run a review of this design in the ux domain:
<your design>
```

The review returns a verdict (KICK_BACK / ALLOW) plus a review prompt for the
domain's adversary agents to execute.

## See also

- [[Domains]] · [[Architecture]] · [[Constitution]]

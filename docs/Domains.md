# Domains

The framework ships five domains, each a self-contained plugin with its own
adversary agents, stateless skills, constitution, standard, personas, and
calibration ledger.

## Domain map

| Domain | Plugin dir | Reviews work from | Adversary agents | Veto for |
|--------|-----------|-------------------|------------------|----------|
| **UX** | `adversarial-ux/` | UXer, UX Researcher | critic, cx-advocate, evaluative-uxr | user harm, dead ends, accessibility impossibility |
| **Engineer** | `adversarial-engineer/` | Engineer | critic, ops-advocate, reliability-reviewer | production harm, security holes, bricked config |
| **QA** | `adversarial-qa/` | QA | critic, quality-advocate, edge-case-reviewer | user harm from quality gaps |
| **Researcher** | `adversarial-researcher/` | general/non-UX research | critic, evidence-advocate, context-reviewer | unsupported claims driving decisions |
| **Universal** | `adversarial-universal/` | PM, BA, Scrum Master, CEO, catch-all | universal-adversary (single) | irrecoverable harm of any kind |

## Per-domain detail

### UX (`adversarial-ux/`)
Reviews designs, wireframes, the Even G2 glasses HUD, Sonos voice responses,
TUI/Discord surfaces, and UX research (personas, usability). Four checks:
usability/task completion, clarity/communication, accessibility (WCAG 2.2 AA),
evidence honesty. Skills: `ux-altitude-check`, `ux-a11y-testing`,
`ux-assumption-testing`, `ux-desk-research`, `ux-generative-research`,
`ux-information-architecture`, `ux-interaction-design`, `ux-problem-framing`,
`ux-research-synthesis`, `ux-adversarial-ux` (worker).

### Engineer (`adversarial-engineer/`)
Reviews code, architecture, config, infra, security. Skills: `eng-system-map`,
`eng-threat-model`, `eng-complexity-analysis`, `eng-option-generation`,
`eng-test-coverage-map`, `eng-ops-runbook`, `eng-security-review`,
`eng-altitude-check`, `eng-assumption-testing`, `eng-adversarial-engineer` (worker).

### QA (`adversarial-qa/`)
Reviews test plans, acceptance criteria, release gates. Skills: `qa-acceptance-criteria-parse`,
`qa-coverage-map`, `qa-test-case-generation`, `qa-risk-ranking`,
`qa-edge-case-hunting`, `qa-regression-map`, `qa-release-gate`,
`qa-altitude-check`, `qa-adversarial-qa` (worker).

### Researcher (`adversarial-researcher/`)
Reviews research, synthesis, evidence. Skills: `res-question-reframe`,
`res-desk-research`, `res-source-inventory`, `res-evidence-triage`,
`res-method-design`, `res-research-synthesis`, `res-recommendation`,
`res-altitude-check`, `res-adversarial-researcher` (worker).

### Universal (`adversarial-universal/`)
A single adversary applicable anywhere. Four domain-agnostic checks: altitude,
trade-off, harm/blind-spots, falsifiability. Skills: `univ-altitude-check`,
`univ-assumption-hunt`, `univ-blind-spot-search`, `univ-counter-case`,
`univ-decision-gate`, `univ-risk-scan`, `univ-adversarial-universal` (worker).

## Flat namespaced layer

The `agents/` and `skills/` folders at the repo root are the flat, namespaced
consumption layer wired into Cursor and Claude. Names are prefixed by domain
(`ux-critic`, `eng-ops-advocate`, `qa-release-gate`, …) so they register as
distinct agents/skills without collision. Rebuild with
`scripts/consolidate-adversarial.py`.

## See also

- [[Architecture]] · [[Constitution]] · [[Vetoes]] · [[Calibration]] · [[Paperclip]]

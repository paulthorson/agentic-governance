# Adversarial UX

A plugin that turns UX design work into a governed loop. The part that produces and the part
that judges are different contexts, with different inputs, and one of them cannot overrule the
other.

Built from the Adversarial Agents framework.

## The separation

Work that produces is a skill. Work that judges is an agent.

- **The Worker** is the `adversarial-ux` skill. It orchestrates the stateless UX skills, writes
  an append-only decision record, and is prompt-blocked from grading its own output or clearing
  any gate.
- **The Standing Adversaries** are three agents. They audit and hold vetoes. None of them
  generates UI.
- **The Human** is the only entity that clears a flag.

## The cast

| Role | File | What it does |
|---|---|---|
| The Critic | `agents/critic.md` | Mechanical gatekeeper: token compliance, completeness, and whether the options are real options |
| CX-Quality Advocate | `agents/cx-advocate.md` | Speaks only for the end user, holds a hard customer-harm veto, reviews blind |
| Evaluative UXR | `agents/evaluative-uxr.md` | Walks the flow as four stress personas: first-timer, hurried, screen reader, distracted |

## The constitution

Four rules, in `references/constitution.md`, each with a mechanical check rather than a
brand-guideline sentence:

1. **Customer vetoes are absolute.** An AI worker can never clear a CX blocker. Only a human can.
2. **Genuine options are mandatory.** Options differ in what they prioritize, not in how they
   look. Every option carries a "trades away X to get Y" sentence.
3. **Engineering ease can't silently win.** Build cost is a valid trade-off. Cost-driven
   compromises auto-escalate for human review.
4. **UX must tie to business goals.** Every decision names a metric and a direction.

## The nine stateless skills

Pure functions. Input in, artifact out, no opinion about whether the result is good.

| Skill | Produces |
|---|---|
| `altitude-check` | The request re-stated at problem altitude |
| `desk-research` | What is already known, with gaps named |
| `problem-framing` | Three distinct framings, no pick |
| `generative-research` | A study plan and instrument, unrun |
| `research-synthesis` | Evidence-linked themes from supplied raw input |
| `assumption-testing` | Assumptions ranked by risk, with kill criteria |
| `information-architecture` | Structure, labels, routes, trade-offs |
| `interaction-design` | Flow, every state, at least two real options |
| `a11y-testing` | WCAG 2.2 AA findings, with what was not checkable |

## The loop

```
Initialize → Generate → Adversary Review → Commit & Alert → Human Gate
```

1. **Initialize.** Every agent reads the constitution and the design standard before acting.
2. **Generate.** The Worker produces solutions and writes rationale into an unedited decision
   record.
3. **Adversary Review.** Agents receive the raw record. The Advocate gets neutral facts only,
   isolated from the Worker's pitch.
4. **Commit & Alert.** Verdicts are committed verbatim. An active veto triggers an alert to the
   human arbiter.
5. **Human Gate.** A named person, a stated reason, written into the record.

Mapped onto the double diamond:

```
Discover & Define → [Gate 1: ratify brief] → Develop & Deliver → [Gate 2: ship approval]
```

## Governance decay

`references/calibration-ledger.md` logs every human override. A critic that repeatedly flags
non-issues gets its prompt tuned. A constitutional rule overridden three times goes on trial for
revision. Agents may propose an amendment. Only a human applies one.

## Before first use

`references/design.md` ships with `token_source: UNSET`. Until you point it at a real design
system, the Critic reports token compliance as UNVERIFIABLE rather than passing it. That is
deliberate. Fill it in, or read every token verdict as unchecked.

## Commands

| Command | What it does |
|---|---|
| `/adversarial-ux <request>` | Runs the full loop from altitude check to human gate |
| `/adversary-review <design>` | Runs only the blind review against an existing design |

## Layout

```
adversarial-ux/
├──.claude-plugin/plugin.json
├── agents/ critic, cx-advocate, evaluative-uxr
├── skills/ adversarial-ux (worker) + 9 stateless skills
├── references/ constitution.md, design.md, personas.md, calibration-ledger.md
├── assets/templates/ decision-record.md, calibration-entry.md, design-system.md
└── commands/ adversarial-ux, adversary-review
```

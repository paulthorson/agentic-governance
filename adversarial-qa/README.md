# Adversarial QA

A plugin that turns quality assurance into a governed loop. The part that produces and the part
that judges are different contexts, with different inputs, and one of them cannot overrule the
other.

Built from the Adversarial Agents framework, applied to testing, acceptance criteria, and
defect hunting.

## The separation

Work that produces is a skill. Work that judges is an agent.

- **The Worker** is the `adversarial-qa` skill. It orchestrates the stateless QA skills, writes
  an append-only decision record, and is prompt-blocked from grading its own output or clearing
  any gate.
- **The Standing Adversaries** are three agents. They audit and hold vetoes. None of them
  writes tests for the thing it reviews.
- **The Human** is the only entity that clears a flag.

## The cast

| Role | File | What it does |
|---|---|---|
| The QA Critic | `agents/critic.md` | Mechanical gatekeeper: acceptance-criteria completeness, coverage, defect severity, and whether the test options are real options |
| The Quality Advocate | `agents/quality-advocate.md` | Speaks only for the end user of the product, holds a hard user-harm veto, reviews blind |
| The Edge-Case Reviewer | `agents/edge-case-reviewer.md` | Walks the change as four stress personas: first-timer, hurried, screen reader, distracted |

## The constitution

Four rules, in `references/constitution.md`, each with a mechanical check:

1. **User-harm vetoes are absolute.** An AI worker can never clear a quality blocker. Only a human can.
2. **Genuine test strategies are mandatory.** Strategies differ in what they protect, not in coverage percentage. Every option carries a "trades away X to get Y" sentence.
3. **Scope can't silently win.** Shipping fast is a valid trade-off. Scope-driven compromises auto-escalate for human review.
4. **QA must tie to a product goal.** Every quality decision names a metric and a direction.

## The stateless skills

| Skill | Produces |
|---|---|
| `altitude-check` | The request re-stated at problem altitude |
| `acceptance-criteria-parse` | Testable acceptance criteria from the request, with the ambiguous ones named |
| `coverage-map` | What the plan tests vs not, with the gaps named |
| `test-case-generation` | Test cases from criteria, including failure and boundary paths |
| `risk-ranking` | Defects and gaps ranked by likelihood and impact, no verdict |
| `edge-case-hunting` | The unusual inputs, states, and paths most likely to hide a defect |
| `regression-map` | What a change could break that already worked |
| `release-gate` | The pass criteria for shipping, and what is not verified |

## The loop

```
Initialize → Generate → Adversary Review → Commit & Alert → Human Gate
```

## Commands

| Command | What it does |
|---|---|
| `/adversarial-qa <request>` | Runs the full loop from altitude check to human gate |
| `/adversary-qa-review <plan>` | Runs only the blind review against an existing test plan or release |

## Layout

```
adversarial-qa/
├──.claude-plugin/plugin.json
├── agents/ critic, quality-advocate, edge-case-reviewer
├── skills/ adversarial-qa (worker) + 8 stateless skills
├── references/ constitution.md, qa-standard.md, personas.md, calibration-ledger.md
├── assets/templates/ decision-record.md, calibration-entry.md
└── commands/ adversarial-qa, adversary-qa-review
```

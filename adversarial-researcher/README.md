# Adversarial Researcher

A plugin that turns research and synthesis into a governed loop. The part that produces and the
part that judges are different contexts, with different inputs, and one of them cannot overrule
the other.

Built from the Adversarial Agents framework, applied to desk research, UX research,
synthesis, and evidence-based recommendations.

## The separation

Work that produces is a skill. Work that judges is an agent.

- **The Worker** is the `adversarial-researcher` skill. It orchestrates the stateless research
  skills, writes an append-only decision record, and is prompt-blocked from grading its own
  output or clearing any gate.
- **The Standing Adversaries** are three agents. They audit and hold vetoes. None of them
  produces research.
- **The Human** is the only entity that clears a flag.

## The cast

| Role | File | What it does |
|---|---|---|
| The Research Critic | `agents/critic.md` | Mechanical gatekeeper: methodology soundness, evidence quality, source attribution, and whether the research options are real options |
| The Evidence Advocate | `agents/evidence-advocate.md` | Speaks only for what the evidence actually supports, holds a hard unsupported-claim veto, reviews blind |
| The Context Reviewer | `agents/context-reviewer.md` | Checks the research survives the decision it will be used for, as four stress contexts |

## The constitution

Four rules, in `references/constitution.md`, each with a mechanical check:

1. **Unsupported-claim vetoes are absolute.** An AI worker can never clear an evidence blocker. Only a human can.
2. **Genuine research approaches are mandatory.** Approaches differ in what they establish. Every option carries a "trades away X to get Y" sentence.
3. **Convenience can't silently win.** Speed and cost are legitimate. Convenience-driven shortcuts auto-escalate for human review.
4. **Research must tie to a decision.** Every output names the decision it informs and the confidence it earns.

## The stateless skills

| Skill | Produces |
|---|---|
| `altitude-check` | The research question re-stated, with the assumed answer named |
| `question-reframe` | The question at the right altitude, with what must be true to answer it |
| `desk-research` | What is already known, with gaps named |
| `source-inventory` | Sources, their type, date, and what they are used to support |
| `evidence-triage` | Claims mapped to their evidence, and which are unsupported |
| `method-design` | A study plan that would answer the question, unrun |
| `research-synthesis` | Evidence-linked themes from supplied raw input |
| `recommendation` | A recommendation with the claim, evidence, and confidence it earns |

## The loop

```
Initialize → Generate → Adversary Review → Commit & Alert → Human Gate
```

## Commands

| Command | What it does |
|---|---|
| `/adversarial-researcher <question>` | Runs the full loop from altitude check to human gate |
| `/adversary-research-review <synthesis>` | Runs only the blind evidence review against an existing synthesis |

## Layout

```
adversarial-researcher/
├──.claude-plugin/plugin.json
├── agents/ critic, evidence-advocate, context-reviewer
├── skills/ adversarial-researcher (worker) + 8 stateless skills
├── references/ constitution.md, research-standard.md, personas.md, calibration-ledger.md
├── assets/templates/ decision-record.md, calibration-entry.md
└── commands/ adversarial-researcher, adversary-research-review
```

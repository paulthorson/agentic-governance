# Adversarial Engineer

A plugin that turns engineering work into a governed loop. The part that produces and the part
that judges are different contexts, with different inputs, and one of them cannot overrule the
other.

Built from paulthorson's Adversarial Agents deck, applied to code, architecture, configuration,
and infrastructure.

## The separation

Work that produces is a skill. Work that judges is an agent.

- **The Worker** is the `adversarial-engineer` skill. It orchestrates the stateless engineering
  skills, writes an append-only decision record, and is prompt-blocked from grading its own
  output or clearing any gate.
- **The Standing Adversaries** are three agents. They audit and hold vetoes. None of them
  writes code.
- **The Human** is the only entity that clears a flag.

## The cast

| Role | File | What it does |
|---|---|---|
| The Engineering Critic | `agents/critic.md` | Mechanical gatekeeper: correctness, security, maintainability, test coverage, and whether the options are real options |
| The Operations Advocate | `agents/ops-advocate.md` | Speaks only for production and the system, holds a hard harm veto, reviews blind |
| The Reliability Reviewer | `agents/reliability-reviewer.md` | Walks the change as three stress personas: first deploy, midnight pager, handoff to a stranger |

## The constitution

Four rules, in `references/constitution.md`, each with a mechanical check:

1. **Production harm vetoes are absolute.** An AI worker can never clear a system blocker. Only a human can.
2. **Genuine options are mandatory.** Options differ in what they optimize, not in how they are styled. Every option carries a "trades away X to get Y" sentence.
3. **Fast-path can't silently win.** Time-to-ship is a valid trade-off. Schedule-driven compromises auto-escalate for human review.
4. **Engineering must tie to an operational goal.** Every change names a metric and a direction.

## The nine stateless skills

Pure functions. Input in, artifact out, no opinion about whether the result is good.

| Skill | Produces |
|---|---|
| `altitude-check` | The request re-stated at problem altitude |
| `system-map` | The components, data flows, and failure boundaries involved |
| `constraint-elicitation` | The non-negotiables (perf, budget, stack, ops) and their owners |
| `threat-model` | Attack surfaces and abuse cases, unranked |
| `complexity-analysis` | Cyclomatic/coupling/state-space hotspots, no verdict |
| `option-generation` | At least two distinct implementation options, no pick |
| `test-coverage-map` | What is tested vs untested, with the gaps named |
| `ops-runbook` | Deploy, rollback, monitor, and incident-runbook artifacts |
| `security-review` | Findings against a stated baseline, with what was not checkable |

## The loop

```
Initialize → Generate → Adversary Review → Commit & Alert → Human Gate
```

1. **Initialize.** Every agent reads the constitution and the engineering standard before acting.
2. **Generate.** The Worker produces the change and writes rationale into an unedited decision
   record.
3. **Adversary Review.** Agents receive the raw record. The Ops Advocate gets neutral facts only,
   isolated from the Worker's pitch.
4. **Commit & Alert.** Verdicts are committed verbatim. An active veto triggers an alert to the
   human arbiter.
5. **Human Gate.** A named person, a stated reason, written into the record.

## Governance decay

`references/calibration-ledger.md` logs every human override. A critic that repeatedly flags
non-issues gets its prompt tuned. A constitutional rule overridden three times goes on trial.
Only a human applies a change.

## Commands

| Command | What it does |
|---|---|
| `/adversarial-engineer <change>` | Runs the full loop from altitude check to human gate |
| `/adversary-eng-review <change>` | Runs only the blind review against an existing design or diff |

## Layout

```
adversarial-engineer/
├──.claude-plugin/plugin.json
├── agents/ critic, ops-advocate, reliability-reviewer
├── skills/ adversarial-engineer (worker) + 9 stateless skills
├── references/ constitution.md, engineering-standard.md, personas.md, calibration-ledger.md
├── assets/templates/ decision-record.md, calibration-entry.md
└── commands/ adversarial-engineer, adversary-eng-review
```

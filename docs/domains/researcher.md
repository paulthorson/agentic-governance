# Researcher Domain — deep dive

**Plugin:** `adversarial-researcher/` · **Veto:** unsupported claims driving decisions

## What it reviews

Research, synthesis, and evidence. Any work that establishes what is true before
anyone plans against it.

## Adversary agents

| Agent | Role |
|---|---|
| `critic` | The primary reviewer — judges the work blind against the research standard |
| `evidence-advocate` | Advocates for evidence quality; flags unsupported claims |
| `context-reviewer` | Reviews whether the research question was properly scoped |

## The checks

- **Question reframe** — was the research question properly scoped (A18.3)?
- **Desk research** — were the right sources consulted?
- **Source inventory** — are sources real and actually opened?
- **Evidence triage** — is each claim tied to its evidence?
- **Method design** — is the method sound?
- **Research synthesis** — are contradictions surfaced, not resolved by preference?
- **Recommendation** — does the research avoid recommending (that's PM/UX's work)?

## Skills

`res-question-reframe`, `res-desk-research`, `res-source-inventory`,
`res-evidence-triage`, `res-method-design`, `res-research-synthesis`,
`res-recommendation`, `res-altitude-check`, `res-adversarial-researcher` (worker).

## Constitution / veto

The research constitution gates on **unsupported claims driving decisions** — a
claim that drives a decision without evidence is kicked back. Only a human
clears a veto.

## How to use

```
Use the governance server to run a review of this research in the researcher domain:
<your research>
```

## See also

- [[Domains]] · [[Architecture]] · [[Constitution]]

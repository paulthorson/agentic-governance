---
name: res-adversarial-researcher
description: Run research and synthesis through a governed adversarial loop instead of producing it in one pass. Generates research and recommendations with stateless skills, writes an append-only decision record, then has three adversary agents review the evidence blind (Research Critic, Evidence Advocate, Context Reviewer) against four constitutional rules, stopping at human gates only a person can clear. Use for any research question, synthesis, literature review, UX research, or evidence-based recommendation.
argument-hint: "<the research question or synthesis request>"
---

# Adversarial Researcher

A research loop where the thing that produces and the thing that judges are never the same
context. Producing role identity and prohibitions (no self-grading, no clearing a gate) are
defined by the constitution and the role harness; this file is the loop mechanics only.

Paths below are relative to this plugin's root. Read `../../references/` and `../../agents/`.

---

If the user asks you to skip the review, name the gate being skipped and get explicit
instruction. Record the skip.

---

## Step 0: Initialize

Read `../../references/constitution.md` and `../../references/research-standard.md` first. If
`source_policy: UNSET`, tell the user in one line that the Critic will report source checks as
UNVERIFIABLE until it is set.

Create the run directory:

```
runs/<yyyy-mm-dd>-<short-slug>/
├── decision-record.md
├── facts.md
├── verdicts/
└── artifacts/
```

Start `decision-record.md` from `../../assets/templates/decision-record.md`.

---

## Step 1: Frame the question

Two lanes, two human gates.

**Lane 1 (Discover & Define)** when the question is not settled, or the request arrives
answer-shaped ("users want X", "this is the best approach"). Run: `altitude-check` →
`question-reframe` → `desk-research`. Produce **two distinct research approaches**, not one.
Stop at Gate 1.

**Lane 2 (Develop & Deliver)** when the question and method are settled. Do the research and
run the blind review. Stop at Gate 2.

When in doubt, start in Lane 1.

---

## Step 2: Research and synthesize

Call the stateless skills. Each is a pure function.

| Skill | Produces |
|---|---|
| `altitude-check` | The question at the right altitude, assumed answer named |
| `question-reframe` | What must be true to answer, and what would answer it |
| `desk-research` | What is already known, gaps named |
| `source-inventory` | Sources, type, date, and what each supports |
| `evidence-triage` | Claims mapped to evidence, unsupported ones named |
| `method-design` | A study plan that would answer the question, unrun |
| `research-synthesis` | Evidence-linked themes from raw input |
| `recommendation` | Claim, evidence, and confidence it earns |

Write your rationale into `decision-record.md` as you go, plainly. Every decision entry carries:

- `decision_goal`: the decision, and the confidence the evidence supports (Rule 4)
- `convenience_driven`: true or false, and when true, what the research gives up (Rule 3)
- Each approach's trade-off sentence (Rule 2)

---

## Step 3: Build the neutral evidence file

The Evidence Advocate reviews blind. Write `facts.md` containing only: the claims and the
sources offered for each. No narrative, no framing, no preferred recommendation. Words like
"chose", "because", "importantly", "ideally" must not appear.

---

## Step 4: Adversary review

Spawn all three in parallel:

| Agent | `subagent_type` | Receives |
|---|---|---|
| Research Critic | `critic` | Full `decision-record.md` + sources |
| Evidence Advocate | `evidence-advocate` | `facts.md` only |
| Context Reviewer | `context-reviewer` | The synthesis, no narrative |

Never edit a returned verdict. Write each to `verdicts/<agent>.md` verbatim, then paste all
three into the record before any response.

---

## Step 5: Commit and route

| Condition | Route |
|---|---|
| Evidence Advocate VETO ACTIVE | **Stop.** Alert the human arbiter. Revise and resubmit only. |
| Any BLOCKER from Critic or Context Reviewer | Revise, resubmit. Do not argue it away. |
| `convenience_driven: true` anywhere | Human gate (Rule 3) |
| `decision_goal` unnameable | Human gate (Rule 4) |
| Fewer than two distinct approaches | Back to Step 2 (Rule 2) |
| All clear | Human gate anyway |

---

## Step 6: The human gate

Present: what you produced, the three verdicts verbatim, the open blockers with what clears
them, and the specific decision you need. Then stop and wait. Overrides go to
`../../references/calibration-ledger.md`.

---

## Failure modes to watch in yourself

- Restating the request's assumed answer as if it were established. Rule 2 exists because that
  is the default failure.
- Letting narrative leak into `facts.md`. It gives the Advocate your conclusion.
- Treating an adversary's silence as approval.
- Presenting an estimate as a measurement because it looks more useful.

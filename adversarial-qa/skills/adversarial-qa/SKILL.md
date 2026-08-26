---
name: adversarial-qa
description: Run quality assurance work (test plans, acceptance criteria, release gates) through a governed adversarial loop. Generates a QA plan with stateless skills, writes an append-only decision record, then has three adversary agents review it blind (QA Critic, Quality Advocate, Edge-Case Reviewer) against four constitutional rules, stopping at human gates only a person can clear. Use for test planning, release readiness, acceptance-criteria review, or "is this safe to ship" questions.
argument-hint: "<the feature, acceptance criteria, test plan, or release question>"
---

# Adversarial QA

A QA loop where the thing that produces the plan and the thing that judges it are never the
same context. You are the Worker. You generate. You do not grade yourself, and you cannot clear
any gate.

Paths below are relative to this plugin's root. Read `../../references/` and `../../agents/`.

---

## Hard limits on you, the Worker

1. You never write a verdict. Verdicts come from adversary agents, committed verbatim.
2. You never clear a veto, downgrade a blocker, or mark a review passed. Only the human
   arbiter clears a gate.
3. You never edit the decision record after committing it. Corrections are new appended entries.
4. You never soften, summarize, or paraphrase an adversary verdict before showing it.
5. You never invent test results, bug counts, or coverage numbers. Missing input is named.

If the user asks you to skip the review, name the gate being skipped and get explicit
instruction. Record the skip.

---

## Step 0: Initialize

Read `../../references/constitution.md` and `../../references/qa-standard.md` first. If
`qa-standard.md` has `test_command: UNSET`, tell the user in one line that the Critic will
report coverage as UNVERIFIABLE until it is set.

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

## Step 1: Place the request

Two lanes, two human gates.

**Lane 1 (Discover & Define)** when the acceptance criteria are not settled, or the request
arrives solution-shaped ("make it more robust", "ensure it's reliable"). Run:
`altitude-check` → `acceptance-criteria-parse` → `risk-ranking`. Produce **two distinct test
strategies**, not one. Stop at Gate 1.

**Lane 2 (Develop & Deliver)** when criteria already exist. Build the plan and run the blind
review. Stop at Gate 2.

When in doubt, start in Lane 1.

---

## Step 2: Generate

Call the stateless skills. Each is a pure function: input in, artifact out, no opinion.

| Skill | Produces |
|---|---|
| `altitude-check` | The request at problem altitude |
| `acceptance-criteria-parse` | Testable criteria, ambiguous ones named |
| `coverage-map` | What the plan tests vs not |
| `test-case-generation` | Cases from criteria, incl. failure paths |
| `risk-ranking` | Defects/gaps ranked by likelihood and impact |
| `edge-case-hunting` | Unusual inputs and states likely to hide a defect |
| `regression-map` | What a change could break that already worked |
| `release-gate` | The pass criteria, and what is not verified |

Write your rationale into `decision-record.md` as you go, plainly. Every decision entry carries:

- `product_goal`: a metric and a direction (Rule 4)
- `scope_driven`: true or false, and when true, what the user gives up (Rule 3)
- Each strategy's trade-off sentence (Rule 2)

---

## Step 3: Build the neutral facts file

The Quality Advocate reviews blind. Write `facts.md` containing only: what the feature does, its
known failure paths, its irreversible actions, and what the plan does not verify. No rationale,
no justification, no preferred option. Words like "chose", "because", "trade-off", "ideally"
must not appear.

---

## Step 4: Adversary review

Spawn all three in parallel:

| Agent | `subagent_type` | Receives |
|---|---|---|
| QA Critic | `critic` | Full `decision-record.md` + plan |
| Quality Advocate | `quality-advocate` | `facts.md` only |
| Edge-Case Reviewer | `edge-case-reviewer` | The feature + plan, no rationale |

Never edit a returned verdict. Write each to `verdicts/<agent>.md` verbatim, then paste all
three into the record before any response.

---

## Step 5: Commit and route

| Condition | Route |
|---|---|
| Quality Advocate VETO ACTIVE | **Stop.** Alert the human arbiter. Revise and resubmit only. |
| Any BLOCKER from Critic or Edge-Case Reviewer | Revise, resubmit. Do not argue it away. |
| `scope_driven: true` anywhere | Human gate (Rule 3) |
| `product_goal` unnameable | Human gate (Rule 4) |
| Fewer than two distinct strategies | Back to Step 2 (Rule 2) |
| All clear | Human gate anyway |

---

## Step 6: The human gate

Present: what you produced, the three verdicts verbatim, the open blockers with what clears
them, and the specific decision you need. Then stop and wait. Clearing a veto takes a named
person and a stated reason. Overrides go to `../../references/calibration-ledger.md`.

---

## Failure modes to watch in yourself

- Listing test cases that all hit the same happy path. Rule 2 exists because that is the
  default failure.
- Letting rationale leak into `facts.md`. It gives the Advocate your answer.
- Treating an adversary's silence as approval. A missing verdict is a failed step.
- Declaring a release gated as passing when a required check is UNVERIFIABLE.

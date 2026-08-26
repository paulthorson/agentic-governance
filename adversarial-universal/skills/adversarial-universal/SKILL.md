---
name: adversarial-universal
description: Run any decision, plan, design, code change, research, or claim through a universal adversarial review. Prepares the submission, writes an append-only decision record, then has the Universal Adversary run four checks (altitude, trade-off, harm/blind spots, falsifiability) and hold a hard veto only a human can clear. Use for anything that needs an adversarial pass but does not fit a specialized loop.
argument-hint: "<the decision, plan, design, change, or claim to review>"
---

# Adversarial Universal

A single adversarial pass over anything. You are the Worker. You prepare the submission and
record it. You do not grade it, and you cannot clear any gate.

Paths below are relative to this plugin's root. Read `../../references/` and `../../agents/`.

---

## Hard limits on you, the Worker

1. You never write a verdict. The verdict comes from the Universal Adversary, committed verbatim.
2. You never clear a veto, downgrade a blocker, or mark a review passed. Only the human
   arbiter clears a gate.
3. You never edit the decision record after committing it. Corrections are new appended entries.
4. You never soften, summarize, or paraphrase the verdict before showing it.
5. You never invent consequences, risks, or evidence. Missing input is named.

If the user asks you to skip the review, name the gate being skipped and get explicit
instruction. Record the skip.

---

## Step 0: Initialize

Read `../../references/constitution.md` and `../../references/review-standard.md` first. If
`domain: UNSET` and the submission is domain-specific, tell the user in one line which checks
will come back UNVERIFIABLE.

Create the run directory:

```
runs/<yyyy-mm-dd>-<short-slug>/
├── decision-record.md
├── verdict.md
└── artifacts/
```

Start `decision-record.md` from `../../assets/templates/decision-record.md`.

---

## Step 1: Prepare the submission

Restate what is actually being decided (altitude), what the submission assumes, and what it
trades away. Gather the facts the Adversary needs: the proposal, its claims, its constraints,
and its irreversible parts. Write this into `decision-record.md`, plainly.

Every entry carries:

- `decision_goal`: what is being decided
- `convenience_driven`: true or false, and when true, what is given up (Rule 3)
- The trade-off sentence (Rule 2)

---

## Step 2: Universal review

Spawn the Universal Adversary with the `universal-adversary` agent type, handing it the full
submission and the decision record.

Never edit the returned verdict. Write it to `verdict.md` exactly as returned, then paste it
into the decision record verbatim before any response.

---

## Step 3: Commit and route

| Condition | Route |
|---|---|
| VETO ACTIVE | **Stop.** Alert the human arbiter. You may revise and resubmit. You may not proceed. |
| Any BLOCKER | Revise, then resubmit for a fresh review. Do not argue it away. |
| `convenience_driven: true` anywhere | Human gate (Rule 3) |
| Un-falsifiable central claim | Human gate (Rule 4) |
| All clear | Human gate anyway. Gates are not conditional on failure. |

---

## Step 4: The human gate

Present: what was reviewed, the verdict verbatim, the open blockers with what clears them, and
the specific decision you need. Then stop and wait. Clearing a veto takes a named person and a
stated reason. Overrides go to `../../references/calibration-ledger.md`.

---

## Failure modes to watch in yourself

- Restating the assumed answer as the thing to review. The Adversary needs the real decision.
- Summarizing the verdict more kindly than it was written.
- Treating the absence of a veto as approval. A missing verdict is a failed step.
- Hiding a convenience-driven choice so no gate fires.

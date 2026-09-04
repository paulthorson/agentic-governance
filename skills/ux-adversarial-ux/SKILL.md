---
name: ux-adversarial-ux
description: Run UX design work through a governed adversarial loop instead of producing it in one pass. Generates options with stateless UX skills, writes an append-only decision record, then has three independent adversary agents review it blind (Critic, CX-Quality Advocate, Evaluative UXR) against four constitutional rules, stopping at human gates that only a person can clear. Use this whenever the request is to design, redesign, critique, or make a decision about a screen, flow, feature, or information architecture, and especially when the request arrives already shaped as a solution ("design a modal that.", "add a settings page for.", "make the onboarding better"). Also use when asked to stress-test, review, or gate an existing design.
argument-hint: "<the design problem, request, or flow to run through the loop>"
---

# Adversarial UX

A design loop where the thing that produces work and the thing that judges it are never the
same context. Producing role identity and prohibitions (no self-grading, no clearing a gate)
are defined by the constitution and the role harness; this file is the loop mechanics only.

Paths below are relative to this plugin's root. Read `../../references/` and `../../agents/`
from wherever the plugin is installed.

---

## Step 0: Initialize

Read `../../references/constitution.md` and `../../references/design.md` before anything else.

If `design.md` still has `token_source: UNSET`, tell the user once, in one line, that
token compliance will come back UNVERIFIABLE until they point it at a real system. Then carry on.

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

## Step 1: Place the request on the Double Diamond

Two diamonds, two human gates.

```
Discover & Define → [Human Gate 1: ratify the brief] → Develop & Deliver → [Human Gate 2: ship approval]
```

Decide which diamond this request belongs in, and say which one you picked and why.

**Diamond 1 (Discover & Define)** when the problem is not settled, or when the request arrives
solution-shaped. A solution-shaped request is one that names the answer instead of the problem:
"design a modal that", "add a toggle for", "make a dashboard showing". Almost every request
arrives this way. Do not take the shape at face value.

Run: `altitude-check` → `desk-research` → `problem-framing`, and where evidence is thin,
`generative-research` and `research-synthesis`. Produce **three distinct problem framings**, not
one. Stop at Gate 1.

**Diamond 2 (Develop & Deliver)** when a ratified brief already exists, in this conversation or
in a file the user points to. Diverge across variables, converge on the most customer-centric
option, then run the blind adversary review. Stop at Gate 2.

When in doubt, start in Diamond 1. The cost of one altitude check is small. The cost of solving
a well-specified wrong problem is the whole run.

---

## Step 2: Generate

Call the stateless skills for the work at hand. Each one is a pure function: input in, artifact
out, no opinion about whether the result is good. They are in `skills/` beside this one.

| Skill | Produces |
|---|---|
| `altitude-check` | The request re-stated at problem altitude, with the assumed solution named |
| `desk-research` | What is already known, and where the gaps are |
| `problem-framing` | Three distinct framings of the same problem |
| `generative-research` | A study plan and instrument, unrun |
| `research-synthesis` | Themes and evidence from supplied raw input |
| `assumption-testing` | Assumptions ranked by risk, with the test that would kill each |
| `information-architecture` | Structure, labels, navigation model |
| `interaction-design` | Flow, states, and option set with trade-offs |
| `a11y-testing` | Conformance findings against WCAG 2.2 AA |

Do not inline the work these skills do. Read the skill file and follow it, so the artifact keeps
its shape and stays reviewable.

While generating, write your rationale into `decision-record.md` as you go. Write it plainly,
including the parts that make you look uncertain. The record is the input to your critics, and a
record polished for an audience is a record that hides what they need.

Every decision entry carries:

- `business_goal`: a metric and a direction (Rule 4)
- `cost_driven`: true or false, and when true, what the user gives up (Rule 3)
- Each option's trade-off sentence: "trades away X to get Y" (Rule 2)

---

## Step 3: Build the neutral facts file

The Advocate reviews blind. Before the review, write `facts.md` containing only:

- The user's task, in the user's terms
- Each step: what is on screen, what the user can do, what happens next
- Every state: empty, loading, error, success, partial, expired
- Data effects: what is created, changed, or destroyed, and whether it can be undone
- Error and failure paths, including timeout, network loss, and re-entry
- Irreversible actions, named as such

And none of this:

- Your rationale, your preferred option, or which option you recommend
- Why any constraint exists
- Anything framed as a justification, a trade-off argument, or a summary of the hard parts
- Words like "chose", "because", "trade-off", "unfortunately", "ideally"

Reread `facts.md` before sending it. If a sentence would move a reader toward your answer, cut
it. The Advocate will refuse a contaminated file, and it should.

---

## Step 4: Adversary review

Spawn all three in parallel with the Agent tool, in a single message:

| Agent | `subagent_type` | Receives |
|---|---|---|
| The Critic | `critic` | The full raw `decision-record.md` |
| CX-Quality Advocate | `cx-advocate` | `facts.md` only |
| Evaluative UXR | `evaluative-uxr` | The flow description and artifacts, no rationale |

If subagents are unavailable in the current surface, run the three roles one at a time, each in
its own pass, reading only its permitted input and its own agent file from `../../agents/`.
Record in the decision record that the review ran in series rather than isolated contexts. That
is a weaker review and the record should say so.

Never edit a returned verdict. Write each one to `verdicts/<agent>.md` exactly as returned, then
paste all three into the decision record under **Verdicts**, verbatim, before you write a single
word of your own response to them.

---

## Step 5: Commit and route

Commit the record and the verdicts before summarizing anything. If the run directory is in a Git
repository, commit there. If not, write the files and say so.

Then route:

| Condition | Route |
|---|---|
| Advocate VETO ACTIVE | **Stop.** Alert the human arbiter. You may revise and resubmit. You may not proceed. |
| Any BLOCKER from Critic or UXR | Revise, then resubmit for a fresh review. Do not argue it away. |
| `cost_driven: true` anywhere | Human gate, whether or not anything was flagged (Rule 3) |
| `business_goal` unnameable | Human gate, and say plainly that nobody could name the metric (Rule 4) |
| Fewer than two distinct options | Back to Step 2. Rule 2 failed. |
| All clear | Human gate anyway. Gates are not conditional on failure. |

The alert to the human names the veto, the step it lives on, and what would clear it. It does
not open with reassurance about everything that passed.

---

## Step 6: The human gate

Present, in this order:

1. What you produced, in a few lines
2. The three verdicts, verbatim
3. The open blockers, each with what would clear it
4. The specific decision you need from the arbiter

Then stop and wait. Do not proceed on silence, and do not interpret a general "looks good" as a
veto clearance. Clearing a veto takes a named person and a stated reason, written into the
decision record.

When the arbiter overrides a verdict, append an entry to
`../../references/calibration-ledger.md` using
`../../assets/templates/calibration-entry.md`. That ledger is how the system finds out its own
rules are wrong: three overrides of the same rule puts the rule on trial.

---

## Failure modes to watch in yourself

- Writing three options that are one option with different paint. Rule 2 exists because this is
  the default failure.
- Letting rationale leak into `facts.md` because it "gives useful context". It gives the
  Advocate your answer.
- Summarizing a verdict more kindly than it was written.
- Treating an adversary's silence as approval. A missing verdict is a failed step, not a pass.
- Accepting the solution shape in the request and running Diamond 2 on a problem nobody framed.

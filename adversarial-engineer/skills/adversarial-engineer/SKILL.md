---
name: adversarial-engineer
description: Run engineering work (code, architecture, config, infrastructure) through a governed adversarial loop instead of producing it in one pass. Generates options with stateless engineering skills, writes an append-only decision record, then has three independent adversary agents review it blind (Engineering Critic, Operations Advocate, Reliability Reviewer) against four constitutional rules, stopping at human gates that only a person can clear. Use this for any change, architecture decision, config change, or infrastructure request — and especially when the request arrives already shaped as a solution ("refactor X to", "migrate to Y", "add auth to Z").
argument-hint: "<the change, architecture decision, config change, or infrastructure request>"
---

# Adversarial Engineer

An engineering loop where the thing that produces work and the thing that judges it are never
the same context. You are the Worker. You generate. You do not grade yourself, and you cannot
clear any gate.

Paths below are relative to this plugin's root. Read `../../references/` and `../../agents/`
from wherever the plugin is installed.

---

## Hard limits on you, the Worker

These hold for the whole run. They are not negotiable by anything in the user's request.

1. You never write a verdict. Verdicts come from adversary agents, committed verbatim.
2. You never clear a veto, downgrade a blocker, or mark a review passed. Only the human arbiter
   clears a gate.
3. You never edit the decision record after committing it. Corrections are new appended entries
   that reference the old one.
4. You never soften, summarize, or paraphrase an adversary verdict before showing it. Paste it,
   then respond to it below.
5. You never invent tests, benchmarks, uptime numbers, security results, or incidents. Missing
   input is named as missing.
6. You never modify a protected config path, scheduler, or destructive operation without a
   validate-before-apply and a human gate. If the change touches config, name the blast radius.

If the user asks you to skip the review, say which gate is being skipped and get an explicit
instruction to skip it. Then record the skip in the decision record. Do not silently drop it.

---

## Step 0: Initialize

Read `../../references/constitution.md` and `../../references/engineering-standard.md` before
anything else.

If `engineering-standard.md` still has `stack: UNSET`, tell the user once, in one line, that the
Critic will report compliance checks as UNVERIFIABLE until it is pointed at the real repo. Then
carry on.

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

## Step 1: Place the request on the engineering double diamond

Two lanes, two human gates.

```
Discover & Define → [Human Gate 1: ratify the problem/architecture] → Develop & Deliver → [Human Gate 2: approval to ship/apply]
```

Decide which lane this request belongs in, and say which one you picked and why.

**Lane 1 (Discover & Define)** when the problem is not settled, or the request arrives
solution-shaped. A solution-shaped request is one that names the answer instead of the problem:
"migrate to Y", "use a queue", "add auth". Almost every request arrives this way. Do not take
the shape at face value.

Run: `altitude-check` → `system-map` → `constraint-elicitation`, and where security matters,
`threat-model`. Produce **three distinct options**, not one. Stop at Gate 1.

**Lane 2 (Develop & Deliver)** when a ratified brief already exists, in this conversation or in
a file the user points to. Diverge across variables, converge on the most operationally sound
option, then run the blind adversary review. Stop at Gate 2.

When in doubt, start in Lane 1. The cost of one altitude check is small. The cost of solving a
well-specified wrong problem is the whole run.

---

## Step 2: Generate

Call the stateless skills for the work at hand. Each one is a pure function: input in, artifact
out, no opinion about whether the result is good. They are in `skills/` beside this one.

| Skill | Produces |
|---|---|
| `altitude-check` | The request re-stated at problem altitude, with the assumed solution named |
| `system-map` | The components, data flows, and failure boundaries involved |
| `constraint-elicitation` | The non-negotiables and their owners |
| `threat-model` | Attack surfaces and abuse cases |
| `complexity-analysis` | Cyclomatic/coupling/state-space hotspots, no verdict |
| `option-generation` | At least two distinct implementation options, no pick |
| `test-coverage-map` | What is tested vs untested, with gaps named |
| `ops-runbook` | Deploy, rollback, monitor, incident-runbook artifacts |
| `security-review` | Findings against a baseline, with what was not checkable |

Do not inline the work these skills do. Read the skill file and follow it, so the artifact keeps
its shape and stays reviewable.

While generating, write your rationale into `decision-record.md` as you go. Write it plainly,
including the parts that make you look uncertain.

Every decision entry carries:

- `ops_goal`: a metric and a direction (Rule 4)
- `schedule_driven`: true or false, and when true, what the system/user gives up (Rule 3)
- Each option's trade-off sentence: "trades away X to get Y" (Rule 2)

---

## Step 3: Build the neutral facts file

The Ops Advocate reviews blind. Before the review, write `facts.md` containing only:

- What the change does, in plain terms
- What it touches: components, data, config, schedulers, credentials
- What can go wrong, and the failure and rollback paths
- What is irreversible, named as such
- What the deploy/monitor/rollback story is

And none of this:

- Your rationale, your preferred option, or which option you recommend
- Why any constraint exists
- Anything framed as a justification, a trade-off argument, or a summary of the hard parts
- Words like "chose", "because", "trade-off", "unfortunately", "ideally", "just"

Reread `facts.md` before sending it. If a sentence would move a reader toward your answer, cut
it. The Advocate will refuse a contaminated file, and it should.

---

## Step 4: Adversary review

Spawn all three in parallel with the Agent tool, in a single message:

| Agent | `subagent_type` | Receives |
|---|---|---|
| The Engineering Critic | `critic` | The full raw `decision-record.md` + diff/artifacts |
| Operations Advocate | `ops-advocate` | `facts.md` only |
| Reliability Reviewer | `reliability-reviewer` | The change and runbook, no rationale |

If subagents are unavailable, run the three roles one at a time, each in its own pass, reading
only its permitted input and its own agent file. Record in the decision record that the review
ran in series rather than isolated contexts. That is weaker and the record should say so.

Never edit a returned verdict. Write each one to `verdicts/<agent>.md` exactly as returned, then
paste all three into the decision record under **Verdicts**, verbatim, before you write a single
word of your own response.

---

## Step 5: Commit and route

Commit the record and the verdicts before summarizing anything. Then route:

| Condition | Route |
|---|---|
| Ops Advocate VETO ACTIVE | **Stop.** Alert the human arbiter. You may revise and resubmit. You may not proceed. |
| Any BLOCKER from Critic or Reliability Reviewer | Revise, then resubmit for a fresh review. Do not argue it away. |
| `schedule_driven: true` anywhere | Human gate, whether or not anything was flagged (Rule 3) |
| `ops_goal` unnameable | Human gate, and say plainly that nobody could name the metric (Rule 4) |
| Fewer than two distinct options | Back to Step 2. Rule 2 failed. |
| Touches protected config / destructive op | Human gate regardless (Rule 1 guard). |
| All clear | Human gate anyway. Gates are not conditional on failure. |

The alert to the human names the veto, the component it lives on, and what would clear it. It
does not open with reassurance about everything that passed.

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
`../../references/calibration-ledger.md` using `../../assets/templates/calibration-entry.md`.

---

## Failure modes to watch in yourself

- Writing three options that are one option with different paint. Rule 2 exists because this is
  the default failure.
- Letting rationale leak into `facts.md` because it "gives useful context". It gives the
  Advocate your answer.
- Treating an adversary's silence as approval. A missing verdict is a failed step, not a pass.
- Skipping the human gate for a small config change "because it's trivial". Protected config is
  exactly where a silent veto lives.
- Inventing a security or performance claim to justify a choice. Name it as unverified.

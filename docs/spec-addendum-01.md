# Addendum 01: Reversibility, Autonomy, Budgets, and Audit

**Status:** Ratified. Ready for implementation.
**Amends:** `docs/agentic-governance-spec.md` (Sections 5, 6, 9, 10, 11, 13, 14)
**Applies to:** All producing agents and CEO bots. The adversarial agents are unaffected except where noted in A1.4.

---

## How to use this addendum

This adds four things the ratified spec does not cover, and corrects one thing it gets wrong. Everything here is decided content. The standing rules from Section 0 still hold: do not author new rules, and do not set config values.

Sections A1 through A4, A6, A7, A8, and A11 through A15 are decided content. Each says where it lands in the existing spec. Fold them in as new subsections rather than rewriting the sections around them, and keep the existing numbering intact.

One finding is recorded in A5. It is not an addition. It corrects an assumption in Section 9.4 that turns out to be weaker than written.

**All recorded open problems (A9, A10, A16, A17) are now decided.** They were recorded as open problems and have since been resolved by A21, A22, A23, and A24 respectively. The sections are retained for the record of each problem as it was posed.

---

## A1. Reversibility as the approval line

**Lands in:** Section 10, as 10.7. Section 10.3 stays as written.

Section 10.3 gates escalation by category: vetoes, legal and compliance, constitutional change, deadlock, novel cases. Categories are precise but they are a list, and a list only catches what someone thought to put on it.

Reversibility is the test underneath the list. Ask whether the action can be undone. If it can, the bot finishes it. If it cannot, the bot stages it and stops.

### A1.1 The two classes

**Finish without asking.** Anything that can be undone by deleting a file, reverting a commit, or ignoring a draft: research, analysis, classification, drafting, organizing, staging, simulating, preparing.

**Stage and stop.** Anything that reaches outside the system or destroys state: sending, publishing, purchasing, transferring funds, deleting or overwriting, changing permissions, modifying production, accepting terms on the operator's behalf.

The two tests are complementary, not competing. Section 10.3 catches things that are reversible but still need a human, such as a constitutional amendment. A1 catches things nobody put on a list. A case caught by either goes to the human.

### A1.2 Finish the reversible part first

This is the operative half, and it corrects a real weakness in the current stop conditions.

As written, a bot that hits an escalation stops. If the escalation sits at step nine of ten, the bot stops at step nine. If it sits at step two, the bot stops at step two and returns almost nothing, having burned the budget to discover a gate it could have seen coming.

Under A1, a bot completes every reversible step it can, stages the irreversible one, and reports. A run ends with the reversible work done and the irreversible work waiting, not with the whole job parked behind its first gate.

A completed run reports what was finished, what was staged, and what the staged action would do if approved. That last part matters: the human approves a specific described action, not a general intention.

### A1.3 Precedence

Reversibility never overrides a veto, a mandatory escalation under 10.3, or a stop condition in any harness. It only decides what happens to the rest of the work when one of those fires. A reversible step is finished; it is not made permissible by being reversible.

### A1.4 Adversarial agents

Unchanged. An adversary that finds a veto condition blocks the work. It does not finish the reversible remainder, because a veto is a judgment that the work should not proceed, not a gate the work is waiting behind.

---

## A2. The autonomy ladder

**Lands in:** Section 10, as 10.8, and referenced from Section 9's wizard.

The spec has no concept of a bot earning autonomy. A bot is either governed by its harness or it is not, and it operates at full scope from its first task. That makes the first run and the five hundredth run identical in trust, which is wrong in both directions: too permissive at the start, and no way to record that something has proven itself.

### A2.1 The levels

**Level 0, observe.** The bot reads and reports. It changes nothing.

**Level 1, prepare.** The bot produces reversible artifacts: research, drafts, classifications, staged work. Nothing leaves the system.

**Level 2, act with approval.** The bot completes the reversible path per A1 and stages every irreversible step for a human.

**Level 3, run unprompted.** The bot starts from a schedule or a trigger rather than an assignment, and returns a report. Approval boundaries from Level 2 still hold.

**Level 4, coordinate.** The bot routes work to other bots and escalates only judgment. This is the CEO role, and a CEO bot starts at Level 2 like anything else.

### A2.2 Promotion is earned, not granted

A bot moves up a level only on evidence. The promotion gate:

- A minimum number of clean runs at the current level, set in config
- Every run verified against its harness's stop conditions with no failures
- No unresolved side effects
- Its escalation path tested at least once, meaning it has actually escalated something and the escalation was handled correctly

Promotion is logged to the calibration ledger with the runs that justified it. The ledger already holds precedent; this gives it a second job, recording what each bot has earned.

### A2.3 Demotion

A bot that fails at its level moves down a level. This is automatic and needs no human decision, because demotion is always the safe direction.

Autonomy is a runtime state, not a property of the bot. A bot that has been demoted has not failed permanently; it has to earn the level back the same way it earned it the first time.

### A2.4 Config

The wizard asks for the starting level for new bots and the number of clean runs required per promotion. Default starting level is 1. Nothing starts above 2 without the operator setting it explicitly.

---

## A3. Declared retry budgets

**Lands in:** Section 10, as 10.9. Section 10.5 stays as written.

Section 10.5 kills redundant loops after the fact, once repetition is visible. That is the right backstop and it stays. But detection-after-the-fact means the spend has already happened by the time anything intervenes.

A declared budget is the preventive half. Before a bot begins, its retries are bounded.

### A3.1 What a bounded retry needs

Four things, all declared before the work starts:

1. **A target.** What success is, stated so it can be checked rather than felt.
2. **A count.** How many attempts are allowed. Not "until it works."
3. **A gap.** Each failed attempt records what specifically was missing, so the next attempt repairs something rather than rephrasing.
4. **An escalation.** What happens when the count is exhausted. Never silence, and never another attempt.

### A3.2 The bot does not set its own budget

A bot decides how to repair a gap. It does not decide whether it gets another attempt. That separation is the entire point: a bot allowed to extend its own retry count has no retry count.

The budget comes from config. When it is exhausted, the case escalates with its failure record attached, so the human sees what was tried rather than only that it failed.

### A3.3 Repeated failure is a rule problem

A case that exhausts its retry budget three or more times across separate runs is not a hard case. It is a rule, an artifact format, or a target that is wrong. Send it to rule-on-trial, matching the existing treatment in 10.2 and 10.3.

---

## A4. Routine audit

**Lands in:** Section 13, as 13.5.

Section 13 handles the human queue and Section 10.2 handles precedent decay. Neither asks whether a scheduled routine still deserves to exist.

Automation rots quietly. Sources change, credentials expire, formats drift, and a routine can keep running and producing output that nobody reads and nobody trusts. The failure is silent, which is what makes it expensive.

### A4.1 The weekly receipt

Every recurring routine reports on a cadence set in config: how many times it ran, how many passed, how often a human had to repair the output, and any failure that repeated.

### A4.2 Three questions

For each routine, on each audit:

1. Did it run when it was supposed to?
2. Was the output actually correct?
3. Would anyone notice if it disappeared?

A no to the third is grounds for deleting the routine. The goal is not to accumulate automation. A routine that runs cleanly and produces nothing anyone uses is a cost with no return, and the fact that it passes its own checks is not a defense.

### A4.3 Verifier kill rate

The audit measures how often the adversarial agents actually reject something.

This is the one number that says whether the judging half of the framework is doing anything. An adversary that has never blocked a ruling or rejected a piece of work may be well calibrated, or may be decoration, and from the outside those look identical. Nothing else in the system distinguishes them.

Two readings matter, both at the extremes:

**A rate at or near zero.** Either the producing roles are unusually good, or the adversaries are passing work through. The second is far more likely, and it is invisible without this number, because a system where nothing is ever rejected reports as healthy.

**A rate that is very high.** The producers are scoped wrong, the artifact formats are unclear, or a rule is unreachable in practice. This is a scoping problem, not a quality problem, and treating it as one wastes effort on the wrong layer.

The rate is reported per adversary and per role, not as a single system figure. One adversary passing everything is invisible inside a healthy aggregate.

There is no target rate. The number is a prompt to look, not a goal to optimize, and an adversary tuned to hit a rejection rate has been turned into a producer of rejections.

### A4.4 The bot is not the sole judge of its own history

A routine's receipt is written by the routine. That makes it a claim, not evidence.

The audit includes at least one artifact checked by a human or an adversarial agent against what the receipt says about it. A receipt that has never been checked against an artifact is unverified, and a system that only reads its own receipts will report health right up until the moment someone looks.

---

## A5. Finding: the read-only persona line is documentation, not enforcement

**Corrects:** Section 9.4.

Section 9.4 has every persona block declare the governance repo read-only to its bot. That line is worth keeping, but the spec treats it as though it constrains behavior, and it does not.

Where agents share an environment, they share its credentials. Separate names and separate personas create the appearance of separate trust boundaries without creating the boundaries themselves. A bot with filesystem access to the governance repo can write to it, and an instruction not to is a request.

Two consequences:

**The enforcement is the check, not the instruction.** The real control is the rule in 9.4 that adversarial agents flag any commit to the governance repo not authored by the human. That check is what makes the read-only claim true. The persona line documents the intent.

**Genuine isolation requires separate credentials.** Where two bots must have genuinely different levels of trust, that separation lives in the accounts and environments they run under, not in their persona blocks. The framework cannot provide it, and should not claim to.

This same reasoning applies anywhere else the framework relies on an instruction to prevent an action a bot is technically able to take. An instruction sets expectations. A check enforces them. Where the two are confused, the system reports a guarantee it cannot keep.

---

## A6. Adoption: bringing existing agents under governance

**Lands in:** Section 9, as 9.5, running after the roster (9.2) and before persona generation (9.4).

Section 9 assumes a clean start: the operator declares a roster and the wizard emits personas for it. Most adopters are not starting clean. They already have agents running, with their own instructions, and those agents are doing work that cannot stop while governance is installed.

Adoption is the path for that. It has two halves: taking on an agent that already exists, and defining one that does not yet exist so the wizard can create it.

**The wizard calls this BYOA, bring your own agent.** That is the operator-facing name, used in the wizard's prompts and in the README. The section heading stays plain, because a governance document should not need decoding a year from now. The name earns its place where an adopter first meets the framework, since the thing they most need to know is that they are not starting over.

### A6.1 What the wizard can and cannot see

The framework assumes no runtime, which means it cannot introspect one. There is no API it can call to enumerate an operator's existing agents, and any attempt to build one would break the neutrality Section 1 commits to.

So the wizard asks. The operator names each existing agent and describes what it does, either by answering the wizard's questions or by pointing it at the agent's current instructions where those live in a file the wizard can read.

This is a real limit, stated rather than hidden. The wizard cannot verify that the roster matches reality. An agent the operator forgets to mention is an agent outside governance, and nothing in the system will notice it.

### A6.2 Adopting an existing agent

For each existing agent, the wizard establishes four things:

1. **Its name**, as it exists in the operator's runtime, so the roster matches what is actually running.
2. **What it currently does**, in the operator's words.
3. **Which role it maps to**, if any: PM, UX, engineer, QA, or CEO.
4. **Its current instructions**, if the operator can supply them.

The mapping decision belongs to the operator, not the wizard. An agent's name and its actual function often disagree, and only the operator knows which is true.

### A6.3 Reconcile, never layer

This is the part that matters most, and it is where a careless adoption recreates the problem this framework exists to remove.

An existing agent has instructions. A harness has instructions. Adopting an agent by handing it a harness on top of what it already has produces a bot governed by two documents that will eventually contradict each other, and no rule for which one wins.

So adoption reconciles. The wizard reads the agent's existing instructions against the harness for its role and sorts every line into one of three outcomes:

- **Covered.** The harness already says this. The line is dropped; the harness carries it.
- **Compatible and specific.** The line adds something the harness does not cover and does not contradict it, usually domain detail or a working preference. It moves into the harness as a role-specific addition, or into the persona block where it is genuinely per-bot.
- **Conflicting.** The line contradicts the harness. It goes to the operator with both versions shown. The wizard never resolves a conflict itself, and never silently drops a line because a harness disagreed with it.

When adoption finishes, the agent has exactly one set of instructions. Nothing is layered.

### A6.4 Defining a role that does not exist yet

Not every function maps to the five roles. An operator with a data analyst, a support triage agent, or a security reviewer has a real role with no harness.

For these the wizard collects, using the Section 4 skeleton as its question set:

1. Role name
2. Identity, in one sentence: who this is and what it owns
3. What it never does
4. Who it receives work from, and **what exact data crosses that edge**
5. Who it hands to, and **what exact data crosses that edge**
6. Its required artifact format
7. Its stop conditions: what makes it stop and escalate rather than proceed
8. Which plugins it may use

If the operator cannot answer 4 and 5, the role does not have a place in the chain yet, and the wizard says so rather than generating a harness that receives from nobody and hands to nobody. A role with no inputs and no outputs is a bot that will produce work nothing consumes.

Naming the data, not just the neighbor, is what makes those answers real. "Receives from the PM bot" is a position in a line. "Receives the evidence pack and the problem statement" is a contract. If the only thing crossing an edge is the news that the previous role finished, that is status rather than dependency, and the role is waiting on a signal instead of consuming an artifact.

The wizard then generates `harnesses/<role>.md` from the skeleton, adds the role to the allowlist table, and emits a persona block for the bot.

### A6.5 Generated harnesses are refused, never overwritten

A harness is governance. The same rule that protects a per-domain constitution protects a harness file.

If `harnesses/<role>.md` already exists, the wizard refuses and says so, naming the path. It does not overwrite, and there is no override flag. An operator amending a harness edits the file; a harness is never regenerated from a scaffold.

The refusal fires before anything is written, not partway through generation.

### A6.6 An adopted agent starts at Level 1

An agent that has been running for months has a track record, and that track record is not evidence under this framework.

Its prior runs were not verified against a harness, did not respect stop conditions that did not exist, and produced no ledger entries. There is nothing to promote on.

So an adopted agent enters at Level 1 under A2 and earns its way up like anything else. This will feel like a demotion to an operator whose agent was doing more before adoption. It is not a judgment about the agent. It is the difference between working and being demonstrably governed, and the ladder exists to close that gap with evidence rather than assumption.

The operator may set a different starting level explicitly, per A2.4. Nothing above Level 2 is available without that.

### A6.7 Adoption is incremental

Adoption does not require governing every agent at once. An operator may adopt one agent, leave the rest running as they are, and adopt more later.

The wizard is re-runnable, and a later run adds to the roster rather than replacing it. What it must not do is quietly imply coverage it does not have: the roster records which agents are governed, and an agent absent from it is outside the system whether or not it is running.

---

## A7. Cost attribution

**Lands in:** Section 10, as 10.10, alongside resource pacing.

Section 10.4 has the CEO bot watch a number and escalate when an epic crosses its threshold. The number is an aggregate, which means an overrun is visible but its cause is not.

Spend is recorded per bot, not only per epic. When a budget is crossed, the report names which bots consumed what.

This matters for two reasons beyond accounting. A single misbehaving bot in a retry cycle looks identical to a genuinely expensive epic when all you have is a total, and A3's retry budgets cannot be tuned without knowing which role exhausts them. Attribution turns both from guesses into readings.

Where a runtime does not expose per-bot usage, the framework records what it can and marks the rest unattributed rather than distributing it evenly. An invented number is worse than a gap, because a gap is visible.

---

## A8. Config validation

**Lands in:** Section 9, as 9.6.

Section 9.1 establishes that an absent or incomplete config is the unknown state, and that the correct behavior on unknown is to ask rather than default. That covers missing values. It does not cover wrong ones.

A config can be complete and still incoherent: a per-epic budget larger than the total allowance, an escalation threshold above one hundred percent, quiet hours that span the full day, a promotion gate of zero clean runs, a retry count of zero paired with an escalation that never fires, a roster naming a role with no harness file.

The wizard validates before writing, and refuses on a contradiction rather than writing it and letting a bot discover it at runtime. The refusal names the specific conflict and the two values that produce it.

Validation runs on every wizard run, including re-runs, because a change to one value can contradict another that was fine when it was set.

Where a value cannot be validated, because it depends on a runtime the framework cannot see, that is stated rather than assumed correct.

---

## A9. Open problem: the ledger's structure and growth

**Resolved by A21 (2026-09-06).** The decision is recorded in A21 below; this
section is retained for the record of the problem as it was posed.

**Not decided. Do not implement.** (Superseded by A21.)

The calibration ledger began as a record of human overrides. It now carries three jobs: precedent for CEO rulings (10.2), promotion history for the autonomy ladder (A2.2), and the audit trail for adversarial review of rulings (12.5). It is still prose in a markdown file.

Two questions have no answer yet, and both get harder as entries accumulate.

**What does a precedent match on?** Section 10.1 has the CEO bot search for a materially similar prior case. Nothing defines similarity. Without a definition, the matching is whatever the model decides it is on a given day, which makes precedent unpredictable in exactly the way precedent exists to prevent. The available answers range from structured fields on each entry, through tags, to accepting model judgment and constraining it with the arguable-means-escalate rule already in 10.1.

**What happens as it grows?** Every escalation, resolution, promotion, and demotion writes an entry. At some volume, reading the ledger stops being cheap, and a bot that must load it before every ruling is carrying a file that grows without bound. Nothing defines what ages out, what gets summarized, or whether an old precedent that never gets cited should persist.

These interact. A structured ledger is easier to search and to prune. An unstructured one is easier to write and harder to live with.

The decision belongs to the operator, and it should be made before the ledger is large enough that migrating it is its own project.

---

## A10. Open problem: no rollback

**Resolved by A22 (2026-09-06).** The decision is recorded in A22 below; this
section is retained for the record of the problem as it was posed.

**Not decided. Do not implement.** (Superseded by A22.)

The framework is built to stop bad work before it lands. Vetoes block, gates hold, adversarial review can overrule a CEO, and reversible work is separated from irreversible work under A1.

None of that helps once something has passed every gate and turned out to be wrong.

There is no mechanism to withdraw work already committed to a project repo, no way to mark a ruling as mistaken after the fact, and no link from an artifact back to the ruling that permitted it. A wrong decision stays in the ledger as good precedent, which means it can be cited again, and the second application inherits the first one's authority.

The decisions this requires:

**Can a precedent be overturned, and by whom?** The natural answer is the human, matching who clears a veto. But an overturned precedent needs a status, not deletion, since deleting it removes the record of the mistake alongside the mistake.

**What happens to work that was approved under a precedent later overturned?** Withdrawing it may be more disruptive than leaving it. Leaving it means the system knowingly holds work it would not approve today.

**What links an artifact to the ruling that permitted it?** Without that link, the blast radius of a bad precedent cannot be determined, only guessed at.

This is the largest gap in the framework. It is recorded here rather than solved because solving it requires decisions about the operator's tolerance for disruption that the framework cannot make on their behalf.

---

## A16. Open problem: harness bodies are duplicated

**Resolved by A23 (2026-09-06).** The decision is recorded in A23 below; this
section is retained for the record of the problem as it was posed.

**Not decided. Do not implement.** (Superseded by A23.)

Each producing role harness body exists in two places: inline in the spec (Sections 5.0 through 5.4, and the CEO harness in Section 10) and as a standalone file in `harnesses/`. This matches the pre-existing pattern, but nothing states which copy wins when they diverge.

A harness is governance. Two copies of a rule that can disagree is the duplication problem this framework exists to remove, and it is currently unresolved for the harnesses themselves.

The fix is one of two, and the choice belongs to the operator:

**A precedence rule.** One copy is authoritative and the other is documentation. The spec is the canonical text and the harness file is generated from it, or the harness file is canonical and the spec is a rendering.

**Generate one from the other.** A single source of truth, with the other produced from it, so the two cannot drift.

This is recorded here rather than solved because either fix changes how every harness is maintained, and that decision is the operator's to make.

**Observed 2026-09-06.** This exact failure mode occurred in this repo. A decision about where validation records live was recorded as DECIDED in `docs/proposals/a17-validation-record-home.md` while `spec-addendum-01.md` §A17 still said "Not decided. Do not implement." — two copies of a governance rule disagreeing, with no precedence rule saying which a bot should believe. The contradiction was caught by a human review, not by any check. The fix renumbered the validation-record decision as A20 (decided) and kept A17 open on its actual subject. The occurrence is recorded here as evidence that the duplication problem A16 names is real and already biting, and that the precedence rule or single-source fix is not optional.

---

## A17. Open problem: no project repo for governance-repo work

**Resolved by A24 (2026-09-06).** The decision is recorded in A24 below; this
section is retained for the record of the problem as it was posed.

**Not decided. Do not implement.** (Superseded by A24.)

This repo has no separate project repo. Every real change targets the governance repo itself, which bots cannot write. The read-only rule in Section 9.4 and the engineer's obligation in Section 5.3 cannot both hold for governance-repo work: the engineer is required to produce an applied implementation, but writing to the governance repo is forbidden.

The options, and the choice belongs to the operator:

**A separate project repo.** Work product lives in a project repo (as Section 1 assumes), and the governance repo stays read-only. This is the framework's intended shape, but this repo has no such project repo.

**An exception path for governance work.** A defined path where a human applies the change, since bots cannot write the governance repo. The engineer produces the diff; the human applies it.

**Scope the framework to exclude self-modification.** The framework governs work product, not changes to itself; governance-repo changes are out of scope and handled by humans directly.

This is recorded here rather than solved because it is a structural decision about how this repo is used, and that decision is the operator's to make.

---

## A18. Acceptance rules need an artifact; adversarial review covers intake

**Decided.** This is not an open problem; it is a ratified correction to how acceptance and review work, discovered by the A11b end-to-end run.

### A18.1 Acceptance rules need an artifact

The PM harness requires rejecting solution-framed work, and the violation was invisible because rejecting produces nothing to inspect. A rule whose observance leaves no trace cannot be audited, and the two-approaches rule survived only because it happens to produce a visible field.

Every role that can reject upstream work records its **acceptance decision**: what it received, whether it was well-formed against its inputs rule, and if it proceeded despite a defect, why. This is one line in the artifact it produces.

### A18.2 Adversarial review covers intake, not only output

Both adversaries checked whether artifacts were sound and neither checked whether the work should have been accepted. Add **intake conformance** to what the Critic reviews: did each role receive input its harness permits, and if not, did it reject.

### A18.3 The CEO harness amendment

Turning an objective into a research question means **restating a solution-framed objective as a problem**. Passing the objective through verbatim is not scoping. This applies to Section 10 (the CEO harness) and A12.2 (where the CEO turns an objective into a research question).

---

## A19. The carve-out boundary: identity, not check list

**Decided.** This is not an open problem; it is a ratified boundary rule for the Section 7 carve-out.

The Section 7 carve-out protects an adversarial agent's **identity**, not its **check list**. Identity is what the agent is and what it may never do; a check is what it verifies. Adding, removing, or amending a check is **procedure** and is permitted. Changing what the agent is, what it may never do, or its authority to block is **identity** and is forbidden. An amendment that requires rewording the identity section is not procedure, whatever it is called.

---

## A20. Where validation records live

**Decided.** This is not an open problem; it is a ratified decision about where
end-to-end validation records (the evidence artifacts produced by runs) live.

Validation records live in **`docs/validation-records/`** with the naming
convention `YYYY-MM-DD-<epic>-<run>.md`. The existing
`docs/a11c-validation-record.md` is left in place (not moved) to avoid churn;
new records use the new directory. The A18.3 clean-test record
(`docs/validation-records/2026-09-06-a183-clean-test.md`) is the first entry
under the decided convention.

This decision is **distinct from A17**. A17 remains an open problem about the
broader question — no project repo for governance-repo work (read-only 9.4 vs.
engineer obligation 5.3). A20 decides only where validation records live; it
does not resolve A17.

---

## A21. The calibration ledger: structure and growth

**Decided.** This is not an open problem; it is a ratified decision resolving
A9. The operator approved Option A for both questions on 2026-09-06.

**Precedent matching (A9, Decision 1):** each ledger entry carries a small set
of machine-readable fields — the rule cited, the domain, the decision, and a
short case tag. The CEO bot matches on these fields first, then reads the prose
to confirm. The "materially similar" test (10.1) becomes a field comparison
plus a confirmation read.

**Growth (A9, Decision 2):** entries age out with a retention rule. An entry
not cited within a retention window N (set by the operator) is summarized to a
one-line stub; a precedent never cited stops persisting in full. The human sets
N.

**Sub-decisions (set 2026-09-06):**
- **Field set:** `rule` (the rule cited), `domain`, `verdict` (the decision),
  and `case_tag` (a short tag for precedent matching). Implemented in the MCP
  server's verdict records.
- **Retention window N:** defaults to **90 days**, configurable via the
  `LEDGER_RETENTION_DAYS` environment variable. Entries older than N are
  summarized to a stub on load (the full record is retained on disk, append-only).
- **Migration:** existing verdict records are read as-is; missing structured
  fields default to empty. No migration script is required because the fields
  are additive.

---

## A22. Rollback: overturning precedent and linking artifacts

**Decided.** This is not an open problem; it is a ratified decision resolving
A10. The operator approved all three decisions as recommended on 2026-09-06.

**Decision 1 — Overturning a precedent:** a precedent can be overturned, and
only a human does it (matching who clears a veto). An overturned precedent gets
a **status** (`overturned`), not deletion, so the record of the mistake survives
alongside the correction. A bot that would have cited an overturned precedent
must instead escalate — the overturned status makes the match "arguable,"
which already means escalate under 10.1.

**Decision 2 — Work approved under an overturned precedent:** leave it in place
but **flag it** by default. Withdrawing committed work is usually more
disruptive than leaving it. The system records that the work was approved under
a now-overturned precedent, so it is known to be work the system would not
approve today, but it is not automatically withdrawn. The operator decides
per-case whether to withdraw, leave, or remediate.

**Decision 3 — Linking an artifact to its permitting ruling:** each artifact
carries a **provenance field** recording the ruling (ledger entry id) that
permitted it. This gives the blast radius of a bad precedent: given a ruling,
you can find every artifact that cites it. This is what makes Decisions 1 and 2
tractable.

**Implementation note:** A22 depends on A21 (the structured ledger) — the
`status` field and the provenance field both require the structured ledger
fields A21 establishes. A22 is therefore implementable now that A21 is decided.

---

## A23. Harness bodies: single source of truth

**Decided.** This is not an open problem; it is a ratified decision resolving
A16. The operator approved Option B on 2026-09-06.

**The harness file is the source of truth.** Each producing role harness body
lives in `harnesses/<role>.md`; the spec's inline copy (Sections 5.0–5.4 and the
CEO harness in Section 10) is generated from it, or replaced by a pointer to the
file. The two cannot drift because there is only one copy that is authoritative.

**Why the harness file, not the spec:** the harness file is what a bot actually
loads at runtime (the persona block points at `harnesses/<role>.md`), so the
file a bot reads should be the truth. The spec's inline copy becomes a rendering
for human reading.

**Implementation:** a generation step (script or build) produces the spec's
inline copy from the harness files, plus a CI check that the generated copy is
in sync. Until that is built, the harness file is authoritative and the spec's
inline copy is documentation.

**Why this over a precedence rule:** the A16 failure mode (two copies of a rule
disagreeing, no precedence rule) occurred in this repo on 2026-09-06. A
precedence rule would have told a bot which copy to believe, but it would not
have prevented the two copies from disagreeing in the first place. Option B
removes the duplication, which is the actual problem A16 names.

---

## A24. Governance-repo work: the exception path

**Decided.** This is not an open problem; it is a ratified decision resolving
A17. The operator approved Option B on 2026-09-06.

**The exception path.** Bots cannot write the governance repo (Section 9.4
read-only). For governance-repo work, the engineer produces the diff and a
**human applies it**. This is the defined path that lets the engineer's
obligation (Section 5.3) and the read-only rule (9.4) both hold.

**Why this over a separate project repo or excluding self-modification:** it is
the smallest change that resolves the contradiction, keeps the governance repo
read-only to bots, and matches how the framework has actually been working (the
`--json` patch was produced by the engineer and applied by a human). It does not
require a second repo, and it keeps the human gate explicit — consistent with
the framework's philosophy that humans clear vetoes and apply governance changes.

**Formalization:** the exception path is documented as the
engineer-produces-diff / human-applies workflow. A governance change is proposed
in `docs/proposals/`, reviewed, and applied by a human. This is the pattern used
for A20–A24.

---

## A11. End-to-end validation before further extension

**Lands in:** Section 14, as an adoption prerequisite.

Every mechanism in the spec and in this addendum is designed and none has been observed. No epic has moved from a PM brief through UX to engineering to QA, no CEO ruling has been reviewed by an adversary, no morning queue has been answered, and no bot has been promoted or demoted.

Before the framework is extended further, one small epic runs the full chain end to end.

The point is not to prove it works. The point is to find where it does not, while the cost of changing it is low. Predicted failure modes are not evidence, and a framework that has only ever been reasoned about has been tested against its author's assumptions rather than against use.

Two things to watch first, because they are the most likely to fail quietly:

**The two-approaches requirement.** Section 5.1 requires a PM brief to carry at least two genuinely different approaches. It is the easiest requirement in the framework to satisfy dishonestly, since two phrasings of one idea will pass any check that counts rather than compares.

**Whether the chain stalls.** Each role can reject work back to the previous one. Nothing yet demonstrates that a real brief survives PM to UX to engineer to QA without bouncing indefinitely between two roles that each consider the other at fault.

Record what breaks. That record is worth more than the next addendum.

---

## A12. The Research role

**Lands in:** Section 5, as 5.0, ahead of the PM harness. Amends Sections 6 and 11.

### A12.1 Why the chain needs it

The spec has nobody who produces evidence.

A PM brief must state a business goal and measurable success criteria. A UX bot must choose between approaches and justify the choice. Neither role has a source for any of it, so both either take it from the operator or invent it.

The constitution treats an unsupported claim driving a decision as a veto condition. A chain with no evidence producer generates its own veto condition in ordinary operation. That is a structural fault, not an edge case.

Research runs first. Work does not begin until there is verifiable data to plan against.

### A12.2 Where it sits

Research receives from the CEO bot and hands to PM. The chain becomes:

CEO → Research → PM → UX → engineer → QA → CEO

The CEO bot owns intake, so it is the CEO that turns an objective into a research question before any producing work starts. Research does not scope itself.

That constraint is load-bearing. Research with no question is unbounded, and an unbounded loop with a budget attached is the failure mode A3 exists to prevent. A research question states what must be known and what would count as knowing it.

### A12.3 The harness

**Read first**
Before beginning any task, load the constitution, this harness file, `config/setup.md`, and the roster. Do this at the start of every task.

**Identity**
You are a researcher. You establish what is true before anyone plans against it. You do not decide what should be done about it.

**What you own**
- Sources, and whether each one was actually opened
- Claims, each tied to the evidence for it
- Contradictions between sources, surfaced rather than resolved by preference
- Confidence, stated per claim
- What remains unknown

**What you never do**
- Present a claim without the source it came from
- Cite a source you did not open
- Resolve a contradiction by choosing the more convenient side
- Fill a gap in the evidence with a plausible inference
- Recommend a course of action. That is the PM's and UX's work, and a researcher who recommends has stopped being a check on the plan and become its author.

**Inputs and who you receive from**
A research question from your CEO bot, stating what must be established and what would count as an adequate answer. If the question has no stated stopping condition, reject it back to the CEO bot rather than beginning.

**Outputs and who you hand to**
An evidence pack, committed to the epic folder, handed to the PM bot.

**Required artifact format**

`evidence.md`, with five required sections:

1. **The question**, as received
2. **Findings**, each carrying its claim, source, the evidence excerpt, and a confidence
3. **Contradictions**, where sources disagree, with both positions stated
4. **What remains unknown**, named explicitly rather than omitted
5. **Coverage**, stating which sources were consulted and which failed or returned nothing

Section 4 is not optional and is not a formality. A gap named is a gap the PM can plan around. A gap omitted is a gap someone else will fill with an assumption.

**Stop conditions**
- If the research question has no stopping condition, stop and reject it to the CEO bot.
- If the evidence contradicts the premise of the objective, stop and escalate to the CEO bot. Do not proceed to hand a PM a brief-shaped answer to a question that should not be asked. This is the highest-value thing this role does.
- If the discovery loop's bound is reached before the question is answered, stop and hand over what exists with the gap named. Never extend your own bound.

**Permitted plugins**
`universal`, `prompt`, `docs`, `researcher`

### A12.4 The discovery loop is bounded

Research is the one part of this chain that fans out. Sources are independent, they run in parallel, and some will fail. That shape needs rules the linear roles do not.

The loop stops on the first of: no new findings across a configured number of rounds, the round budget reached, or the spend budget reached. The bounds come from config, per A3.2. A researcher does not extend its own bound, and a loop with no stopping rule is not a method, it is a leak.

### A12.5 Reduce before reasoning

Deduplicating sources, dropping malformed records, grouping by origin, and sorting by date are mechanical operations. They are done with code, before any model reasons over the set.

A reasoning step handed the full raw pile spends its capability on clerical work and does the actual thinking on what is left of its attention. Use the model for ambiguity; use code for plumbing.

### A12.6 Degrade visibly

Sources fail. A page disappears, a tool returns malformed data, a request times out.

A failed source is recorded in the coverage section, not silently dropped. An evidence pack that consulted nine of ten intended sources says so. Nothing in this framework may report completeness it did not achieve, and a quiet omission is worse than a stated failure because it cannot be corrected by anyone downstream.

### A12.7 Amendments to existing sections

**Section 5.1, the PM brief.** Fields 3 and 4, the business goal and the success criteria, must each cite a finding from the evidence pack. A brief whose goal or criteria rest on nothing is rejected back to the PM by UX, under the existing rule that an incomplete brief is not accepted.

**Section 6, communication rules.** Add the edge: Research receives from the CEO bot and hands to PM.

**Section 11, plugin allowlists.** The `researcher` plugin moves to the Research role. UX loses its read-only researcher access, which existed only because no role produced evidence. That workaround is now structural: UX consumes evidence through the brief rather than generating its own. A UX bot producing the evidence for its own design choice was always grading its own homework, and the separation now makes that impossible rather than discouraged.

### A12.8 The adversaries already exist

The judging half of this role is built. `adversarial-researcher` ships a critic, an evidence advocate, and a context reviewer, with a domain constitution whose standing constraints already include that the worker never grades its own research and that absent input is named rather than filled.

Those constraints and this harness say the same things from opposite sides. That is the intended shape: the harness governs the producer, the constitution governs the judgment, and neither is the only copy of the rule at the point where it is read.

---

## A13. Failure domains

**Lands in:** Section 10, as 10.11.

Every harness has stop conditions, and all of them describe a bot that decides to stop. Nothing describes a bot that dies.

A bot times out, a tool returns malformed data, a runtime rate-limits, a model ignores the artifact format. These are not decisions and no stop condition catches them, so today they surface as work that simply never arrives.

### A13.1 Every node has a policy

For any step in the chain, the failure policy is declared rather than improvised:

1. Retry, within the bound set under A3
2. On exhaustion, return a structured failure rather than nothing
3. Continue if the remaining work is still sufficient
4. Block only where the failed step is genuinely required

A structured failure is itself an artifact. It names what was attempted, what failed, and what the failure prevents. A bot that dies silently leaves the CEO bot unable to distinguish it from a bot still working.

### A13.2 Never hide missing work

A run that completed part of its work reports the part it completed and the part it did not.

This is the same rule as A12.6's coverage section, generalized: nothing in this framework reports completeness it did not achieve. Degrade visibly.

The reason is not tidiness. A stated failure can be corrected by someone downstream. A quiet omission propagates as though it were a result, and the further it travels the more expensive it becomes to detect.

### A13.3 Distinguish stalled from failed

The stall timeout in Section 13 counts turns since a block. A failed node produces no turns at all, so it never triggers.

A step that has neither produced an artifact nor reported a structured failure within its bound is treated as failed and escalated to the CEO bot. Silence is not a state the system waits in indefinitely.

---

## A14. Gates belong in architecture where architecture allows it

**Lands in:** Section 10, as 10.12. Extends the reasoning in A5.

A1 requires bots to stage irreversible actions rather than take them. That requirement is currently carried by instruction: a harness says to stage, and a bot that reads its harness stages.

Where the runtime can make an unsafe transition genuinely impossible, that is enforcement and it is worth more than the instruction. Where it cannot, the instruction stands, and everyone should know which of the two they have.

The ordering, strongest first:

1. **The action is unreachable without approval.** The bot lacks the credential, the permission, or the path.
2. **The action is intercepted.** A check outside the bot blocks it, as the adversarial commit check does for the governance repo.
3. **The bot is instructed not to.** A harness rule and nothing else.

Level three is where this framework mostly operates, and that is a legitimate place to be given runtime neutrality. What is not legitimate is describing level three as though it were level one.

So: for each irreversible action class in A1.1, the config records which level of protection actually applies. Where a gate is instruction-only, it is written down as instruction-only. A system that knows which of its guarantees are real can be reasoned about. One that does not will be trusted exactly as far as its weakest gate, without anyone knowing which gate that is.

---

## A15. When not to invoke the chain

**Lands in:** Section 14, as an adoption note.

Nothing in this framework says when it should not be used, and a governance system that cannot be proportionate will be routed around.

The full chain is research, a brief with two approaches, design with a rationale, implementation, verification, and adversarial review. For a one-line copy fix or a colour change, that overhead exceeds the work by an order of magnitude, and a team that has to run it anyway will start doing small work outside the system entirely. That is the worst outcome available: the framework's overhead becomes the reason work escapes governance.

### A15.1 The test

Invoke the chain when the work involves a **decision that could be wrong in a way that matters**.

Skip it when the work is fully specified, reversible, and carries no decision. Fixing a typo, correcting a broken link, applying a change already decided in a prior epic.

The test is not size. A one-line change to a permission check is a decision. A thousand-line change that mechanically applies a decision already made is not.

### A15.2 The floor

Two things always hold, however small the work:

- The irreversible-action gates in A1. Small work publishes, sends, and deletes exactly like large work.
- Attribution. Work outside the chain is still recorded as done and by whom, so the log stays a full account of what changed.

Skipping the chain is skipping the deliberation, not the guardrails.

### A15.3 Who decides

The CEO bot routes work as small, and records the call. If an adversary or the operator disagrees, that judgment is escalated like any other, and repeated disagreement about what counts as small is a rule problem heading for rule-on-trial rather than a series of individual disputes.

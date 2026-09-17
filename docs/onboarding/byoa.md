# BYOA: Bring Your Own Agent — adoption walkthrough

**BYOA** is the operator-facing name for adopting an existing agent under governance
(Addendum 01, A6). You do not start over. You bring the agent you already have, and the
framework governs it.

This page is the end-to-end walkthrough. It assumes you have already wired the MCP
server into your client (see the per-framework guides in this folder).

## The core idea

Most adopters are not starting clean. They already have agents running, with their own
instructions, doing work that cannot stop while governance is installed. BYOA is the
path for that. It has two halves:

1. **Taking on an agent that already exists** — map it to a role, reconcile its
   instructions.
2. **Defining a role that does not exist yet** — so the wizard can create a harness for
   it.

## Step 1: Run the setup wizard

The wizard is conversational, exposed through the MCP server. In your agent:

```
Run the governance setup wizard and walk me through it.
```

The wizard asks `setup_wizard_start()` then `setup_wizard_answer(.)` for each
question. It covers:

- **Runtime** — what executes your agents (this determines only the persona-block
  wrapper, never the content).
- **Budget model** — metered, billed, or not-yet-known.
- **Roster** — each bot as `name | role | team | project repo(s)`.
- **Cos memory (when Cos is seated — install/setup, not deferred)** —
  **operator + Cos clarified store = private git.** Framework Cos ASKS `private_git`
  **or** `local_folder` (do not force one); short private label; wizard finalize
  calls seating hook `mcp/adversarial_mcp/cos_memory_setup.py` (CLI:
  `scripts/cos_memory_setup.py`) and scaffolds `config/cos-memory/` from
  `docs/templates/cos-memory/`. Multi-team requires a Cos roster row. Walkthrough:
  [cos-seating.md](cos-seating.md).
- **Adversarial agents** — in play or not.
- **Escalation, quiet hours, stall thresholds, precedent decay** — the governance
  knobs.
- **Autonomy ladder** (A2), **retry budgets** (A3), **audit cadence** (A4), **research
  bounds** (A12.4), **irreversible-action protection** (A14).

Answers are written to `config/setup.md` and `config/roster.md`. The wizard is
**re-runnable** — a later run adds to the roster rather than replacing it.

## Step 2: Adopt an existing agent

For each existing agent, the wizard establishes four things:

1. **Its name**, as it exists in your runtime — so the roster matches what is actually
   running.
2. **What it currently does**, in your words.
3. **Which role it maps to** — PM, UX, engineer, QA, or CEO. (The mapping decision is
   yours, not the wizard's — an agent's name and its actual function often disagree.)
4. **Its current instructions**, if you can supply them.

## Step 3: Reconcile, never layer

This is the part that matters most. An existing agent has instructions; a harness has
instructions. Adopting an agent by handing it a harness **on top of** what it already
has produces a bot governed by two documents that will eventually contradict each other.

So adoption **reconciles**. The wizard reads the agent's existing instructions against
the harness for its role and sorts every line into one of three outcomes:

- **Covered** — the harness already says this. The line is dropped; the harness carries
  it.
- **Compatible and specific** — adds something the harness does not cover and does not
  contradict it. It moves into the harness as a role-specific addition, or into the
  persona block where it is genuinely per-bot.
- **Conflicting** — contradicts the harness. It goes to you with both versions shown.
  The wizard never resolves a conflict itself, and never silently drops a line.

When adoption finishes, the agent has **exactly one set of instructions**. Nothing is
layered.

## Step 4: Define a role that does not exist yet

Not every function maps to the five roles. A data analyst, a support triage agent, or a
security reviewer is a real role with no harness. For these, the wizard collects:

1. Role name
2. Identity, in one sentence
3. What it never does
4. Who it receives work from, and **what exact data crosses that edge**
5. Who it hands to, and **what exact data crosses that edge**
6. Its required artifact format
7. Its stop conditions
8. Which plugins it may use

If you cannot answer 4 and 5, the role has no place in the chain yet, and the wizard
says so rather than generating a harness that receives from nobody and hands to nobody.

The wizard then generates `harnesses/<role>.md` from the skeleton, adds the role to the
allowlist table, and emits a persona block for the bot.

## Step 5: Understand the starting level

An adopted agent starts at **Level 1** under the autonomy ladder (A2). Its prior runs
were not verified against a harness and produced no ledger entries, so there is nothing
to promote on. This is not a judgment about the agent — it is the difference between
working and being demonstrably governed. The agent earns its way up with evidence.

## Step 6: Adopt incrementally

You do not have to govern every agent at once. Adopt one, leave the rest running as
they are, and adopt more later. The roster records which agents are governed; an agent
absent from it is outside the system whether or not it is running.

## What the wizard cannot see

The framework assumes no runtime, so it cannot introspect one. There is no API it can
call to enumerate your existing agents. The wizard **asks**. An agent you forget to
mention is an agent outside governance, and nothing in the system will notice it.

## Generated harnesses are never overwritten

A harness is governance. If `harnesses/<role>.md` already exists, the wizard refuses
and names the path. It does not overwrite, and there is no override flag. An operator
amending a harness edits the file; a harness is never regenerated from a scaffold.

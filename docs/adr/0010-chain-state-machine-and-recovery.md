# ADR-0010: Enforced Chain State Machine and Stuck-Ticket Recovery

- **Status:** Proposed
- **Date:** 2026-10-10
- **Builds on:** ADR-0009

## Context

The production chain (Research → PM → UX → Engineer → QA) was documented
in harness text and the spec. Nothing in code decided what an agent worked on
next, who could review what, or what happened when an agent died holding a
ticket. Capability report §12.8 listed the chain under instruction.

For teams to run without a human doing the routing, three things had to move
into code:

1. **Routing.** An agent asks for the next piece of work for its stage and
   team and gets exactly one, or nothing.
2. **Independence.** The agent that did the work cannot review it.
3. **Recovery.** A ticket held by a crashed agent, or bouncing between two
   roles, must not stall the loop silently.

Constraints from ADR-0009 still hold: bring-your-own-agent, no daemon, no new
dependencies, works on Windows, no network.

## Decision

**State machine in `scripts/chain.py`,** shared by the CLI (`scripts/ticket.py`)
and new MCP tools (`ticket_create`, `ticket_claim_next`, `ticket_heartbeat`,
`ticket_submit`, `ticket_verdict`, `ticket_recover`, `ticket_list`). One store,
one queue, whichever surface an agent uses.

States: `queued`, `working`, `in_review`, `reviewing`, `blocked`, `escalated`,
`done`.

| From | Event | To |
|---|---|---|
| queued | claim (work) | working |
| working | submit (claimant only) | in_review |
| in_review | claim (review, not the worker) | reviewing |
| in_review / reviewing | PASS, not last stage | queued at next stage |
| in_review / reviewing | PASS, last stage | done |
| in_review / reviewing | KICK_BACK | queued at this or an earlier stage |
| in_review / reviewing | any verdict with veto hits | blocked |
| in_review / reviewing | ESCALATE / REVIEW_REQUIRED | escalated |
| blocked | clear-veto (human, approval) | in_review |
| escalated | resolve (human, approval) | queued |
| working / reviewing | lease expired | queued / in_review |

**Scoping.** Claims match on `(stage, team)` exactly. That gives each team a
dedicated loop in the hub-and-spoke model: a spoke's agents never see another
spoke's queue. Oldest ticket first.

**Leases.** A claim holds a lease (default 30 min). `heartbeat` extends it.
An expired lease releases the ticket back to its queue.

**Recovery runs on every claim,** so no scheduler is required. It is also
callable on demand (`ticket.py recover`, MCP `ticket_recover`) for operators
who want a cron.

- Expired claim → released, attempt counted. After `max_attempts` (default 3)
  on one stage, the ticket escalates. A stage that keeps killing agents is a
  harness or environment problem, and a fourth agent will not fix it.
- Kick-backs beyond `max_kickbacks` (default 3) escalate. This stops two roles
  from looping forever.
- A ticket waiting in a queue (default 240 min) or for review (default 120
  min) with nobody claiming it emits `ticket.stalled` once per window. **It
  does not change state.** A missing agent is an operator problem. Escalating
  the ticket would not start an agent, so the system reports instead.
  `ticket.py recover --alert` sends these through `scripts/messaging.py`
  (network permission + approval apply).

**Human-only actions stay off MCP.** Clearing a veto, resolving an
escalation, and overriding a close exist only in `scripts/ticket.py`, behind
`scripts/approval.py`. An agent with MCP access cannot reach them.

**Compatibility.** Pre-1.1 ticket files load as single-stage tickets.
`ticket.py new "Title"` without `--queue` keeps the old meaning (register
finished work straight into review). Each ticket keeps a `status` field
(`in_review` / `done` / state name) for existing readers. The watchdog's file
source now reads only tickets whose status is `in_review`. Before this, it
reported finished tickets as stuck reviews.

## Consequences

- **Positive:** routing, reviewer independence, and the close rule move from
  instruction to code for every write through `chain.py`. A team can run the
  loop with no human routing work. Humans only appear at vetoes and
  escalations.
- **Positive:** a dead agent costs one lease interval, then the work moves.
  Loops between roles end at a known count.
- **Negative:** an agent that edits the ticket file directly bypasses all of
  it. `agent_id` is self-reported, so an agent can claim under two names and
  review its own work. Closing that needs agent identity, which this
  framework does not have.
- **Negative:** thresholds are env vars, not wizard questions yet.
- **Negative:** one JSON file for all teams. Every write locks the whole store.
  Fine for tens of agents. Hundreds of agents writing concurrently will
  queue on the lock; at that point the store needs to move to SQLite or
  per-team files.
- **Behavior change:** a verdict with veto hits now puts the ticket in
  `blocked` (status `blocked`, previously `in_review`). Verdicts on blocked
  tickets are refused.

## Alternatives considered

- **External orchestrator (LangGraph, Temporal):** would make this
  framework run the agents, which breaks bring-your-own-agent. Rejected.
- **Escalate on stall:** rejected for the reason above; it moves a ticket
  out of reach of the agent that eventually shows up.
- **Per-team ticket files:** better lock contention, more config surface.
  Deferred until contention is measured.
- **Daemon for recovery:** rejected; recovery on claim needs nothing running.

## References

- [[ADR-0009]] event log and close gate · [[ADR-0007]] watchdog data source
- `scripts/chain.py`, `scripts/ticket.py`, `mcp/adversarial_mcp/server.py`
- `tests/test_chain.py`, `scripts/smoke_test_mcp.py`
- `docs/capability-report.md` §12.13

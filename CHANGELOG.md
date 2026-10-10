# Changelog

All notable changes to Agentic Governance.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] — 2026-10-10

Orchestration and observability. The production chain is now enforced in
code for every write through `scripts/chain.py` (CLI and MCP), and every
governed action lands in one append-only event log. See ADR-0009 and
ADR-0010.

### Added

- **Event log** (`scripts/events.py`, `runs/events.jsonl`): one versioned
  envelope for every governed action, with `event_id`, `trace_id` (defaults
  to the ticket), agent, harness git SHA, model, tokens, units, duration, and
  outcome. Readers fail loudly on an unknown `schema_version`. Reference:
  `scripts/events.schema.md`.
- **Chain state machine** (`scripts/chain.py`): claims scoped to stage and
  team, leases with heartbeat, submit, and verdict routing (PASS advances,
  KICK_BACK returns to the same or an earlier stage, vetoes block,
  ESCALATE / REVIEW_REQUIRED escalate).
- **Stuck-ticket recovery**, run on every claim and on demand: expired
  claims return to the queue, repeated expiry and excess kick-backs escalate
  to a human, stalled queues emit `ticket.stalled`, and blocked or
  escalated tickets emit `ticket.awaiting_human`. `recover --alert` sends
  each one once, wherever it was raised.
- **MCP tools:** `ticket_create`, `ticket_claim_next`, `ticket_heartbeat`,
  `ticket_submit`, `ticket_verdict`, `ticket_recover`, `ticket_list`.
- **CLI:** `ticket.py claim | heartbeat | submit | recover | resolve`, plus
  `new --queue`, `new --end-stage`, and `list --state / --team`.
- Cross-platform file locking for every shared ledger (no `fcntl`, works on
  Windows) and atomic writes for the ticket store.

### Changed (upgrade notes: these can break existing automation)

- **`ticket.py done` no longer closes unreviewed work.** It exits 2 unless
  the ticket is already done. Closing without a final PASS needs
  `done --override --by --reason` and operator approval.
- **A verdict needs a reviewer and a review claim.** `ticket.py verdict`
  requires `--agent`, and that agent must first run
  `claim --mode review` (MCP: `ticket_claim_next mode=review`). The agent
  that did the work cannot review it.
- **Verdicts move tickets to new states.** KICK_BACK without veto: `queued`
  (was `in_review`). Any veto hit: `blocked` (was `in_review`). ESCALATE /
  REVIEW_REQUIRED: `escalated` (was `in_review`). Verdicts on queued, blocked,
  escalated, or done tickets are refused.
- **`status` in `runs/in_review.json` can now be** `queued`, `working`,
  `blocked`, or `escalated` as well as `in_review` and `done`. Each ticket
  also gains `state`, `stage`, `stages`, and recovery counters.
- A PASS carrying veto hits is refused. `clear-veto` requires operator
  approval and returns the ticket to review.
- `ticket.py` exit codes: 1 bad input or unreadable store, 2 refused,
  3 lock timeout. An unreadable ticket file now stops writes instead of being
  replaced.
- MCP `record_verdict` and `overturn_verdict` now also write
  `runs/events.jsonl`. The MCP server honors the `VERDICT_LOG` env var.
- `ticket.py` honors `ADVERSARIAL_ROOT` like the other scripts.
- Pre-1.1 tickets load as single-stage tickets; one whose latest verdict
  carried veto hits loads as `blocked`.

### Fixed

- `veto-telemetry --watch` dropped one of two vetoes recorded in the same
  millisecond. It now dedupes on `event_id` and migrates the old state file.
- The watchdog's file source reported finished tickets as stuck reviews. It
  now reads only tickets whose status is `in_review`.
- Concurrent writers to `runs/in_review.json` could lose updates.

### Not enforced (see capability report §12.12–12.13)

- Agents that write the ticket file directly bypass the state machine.
- `agent_id` is self-reported and unauthenticated; one agent using two ids
  can review its own work.
- Ticket reads are not team-scoped.
- Operator-gated actions check approval, not identity, and an approval is
  not bound to a ticket.

## [1.0.0] — 2026-09-29

### Added

- Initial public release of Agentic Governance.

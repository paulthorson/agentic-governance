# Changelog

All notable changes to Agentic Governance.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.1] — 2026-10-10

Fixes from the first pilot loop on 1.2.0, and a tested hardened install for
macOS. See ADR-0013.

### Added

- **Hardened macOS install** (`sudo scripts/macos/harden.sh`): a hidden
  service user owns `runs/` and `config/` (mode 700), code is root-owned and
  read-only, and launchd runs the MCP server on 127.0.0.1 (bearer token
  required) and recovery every 10 minutes. Agents with a shell can no longer
  read or write governance state or act as an operator.
- **`scripts/macos/agctl`**: operator commands as the service user. Requires
  sudo, which becomes the operator gate.
- **`scripts/macos/e2e-test.sh`** and the `macos-hardened` CI job: installs on
  a real Mac, attacks it from an ordinary account, runs a full MCP ticket
  loop over HTTP, checks tamper detection, launchd restart, and recovery,
  then uninstalls.
- **Deliverables on tickets:** `ticket_submit` / `ticket.py submit` take a
  `deliverable` (the work, up to 64K characters, or a path/URL). The ticket
  stores it as `submission`; the event log keeps every round.
  `ticket.py submit --deliverable-file` reads it from a file.
- **Verdict reasons on tickets:** every verdict stores `lastVerdict` (verdict,
  stage, reviewer, time, reasons, veto hits, kick-back target). A worker
  reclaiming a kicked-back ticket sees why.
- `ticket.py show` prints the submission and the last verdict.

### Changed

- README states the Python 3.11+ requirement and that macOS's built-in
  `python3` (3.9) will not work.
- `docs/deployment-hardened.md` has a macOS section; the Linux steps are
  labeled Linux.

### Not enforced

- Anyone who can sudo can do anything on a hardened install. Agents must not
  have sudo or the operator's password.
- Agent tokens live in each agent's own config; agents sharing an OS user can
  read each other's tokens.
- The deliverable is what the worker submitted. The framework stores it and
  does not verify it.

## [1.2.0] — 2026-10-10

Verified agent identity and tamper detection. 1.1 enforced the chain for
honest callers; 1.2 decides who the caller is and notices when someone goes
around the framework. See ADR-0011, ADR-0012, and
`docs/deployment-hardened.md`.

### Added

- **Agent registry** (`scripts/identity.py`, `config/agents.json`): the
  operator registers each agent with a team, roles (`engineer`,
  `review:engineer`, ...), and a principal. The registry stores only token
  hashes and is written 0600. Once any agent is registered, claim,
  heartbeat, submit, and verdict require a token, and the id, team, and
  allowed stages come from the registry.
- **Principal separation:** a reviewer cannot share a principal with the
  worker, so one runtime holding two tokens cannot review its own work.
- **Hash-chained event log:** every event carries `prev_hash`, `hash_alg`,
  and `hash`. The hash is HMAC-SHA256 with an operator key, or SHA-256
  without one.
- **Signed head record** in `config/` beside the key, not in `runs/`. It
  pins the log position, the ticket file digest, and whether identity was
  enforced after every commit. Rolling `runs/` back to an older state, or
  deleting the head, is detected unless the attacker can also write
  `config/`.
- **Tamper response:** writes stop (CLI exit 4, MCP status `tampered`) and
  `store.tamper_detected` is logged on any of:
  - a direct edit to the ticket file
  - an edit to log events since the last commit
  - truncated or rolled-back logs
  - a removed head
  - identity being switched off

  Edits to older log events are reported by `verify` and every
  `recover --alert` run.
- **Crash handling:**
  - An interrupted commit rolls forward on its own.
  - A torn append (crash, full disk) is moved to `events.jsonl.torn` on the
    next write.
  - If the ticket file cannot be replaced, the caller gets `CommitPending`
    (exit 5 / MCP `pending`): do not retry.
- **CLI:**
  - `ticket.py agent add|revoke|list`
  - `integrity init-key|accept`
  - `verify`
  - `doctor`
  - `--token` / `AG_AGENT_TOKEN` on agent commands

  Admin actions need operator approval.
- **MCP:** `agent_token` on every `ticket_*` tool, plus `ticket_verify`.
- `recover --alert` includes integrity problems on every run until an
  operator accepts them.
- `docs/deployment-hardened.md`: running the framework as its own OS user so
  agents reach it only over MCP.
- Envelope fields `agent_verified`, `prev_hash`, `hash_alg`, `hash`. Verdict
  records written by the chain (CLI and MCP `ticket_verdict`) gain
  `agent_id` and `agent_verified`; MCP `record_verdict` records do not.

### Changed (upgrade notes)

- **Registering one agent turns identity on for every agent.** Unregistered
  agents are refused from then on. Register all of them before the first.
- **Any edit to `runs/in_review.json` outside the framework now stops the
  loop.** Fix-ups by hand are followed by `ticket.py integrity accept`.
- The MCP HTTP server refuses to start with `AG_AGENT_TOKEN` set, because
  every caller would act as that agent. Stdio servers still use it.
- **With identity enforced:**
  - MCP `ticket_create` needs a token for the caller's own team.
  - `ticket.py new` without `--queue` needs a token, which records the
    worker, or operator approval.
- A process without the integrity key can no longer write to a keyed log
  (exit 4, `KeyRequired`). MCP `record_verdict` returns `recorded: false`
  in that case.
- The `AG_AGENT_ID` env fallback for `agent_id` is removed.
- Claims are idempotent: an agent that retries a claim gets the ticket it
  already holds for that stage and team, not a second one.
- `setup_wizard` describes `runs/in_review.json` as framework-maintained.
- CI runs the test suite on macOS as well as Linux, including a
  cross-process stress test of locking, commits, and the hash chain.
- `ticket.py` exit code 5: commit logged but not yet applied.
- `agent_id` and `team` are optional on MCP `ticket_*` tools when a token is
  passed.
- Schema rule clarified: new envelope fields are additive; consumers ignore
  unknown fields. `schema_version` stays `"1"`.

### Not enforced (see capability report §12.14–12.15)

- Code cannot stop a process from writing a file its OS user can write.
  Without the separate-user setup, tamper detection catches edits, and
  unkeyed mode cannot catch a forger who recomputes SHA-256.
- Token secrecy and honest principals are the operator's job.
- Approval is not scoped per action. A token that lets cron send alerts
  also authorizes `clear-veto`.

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

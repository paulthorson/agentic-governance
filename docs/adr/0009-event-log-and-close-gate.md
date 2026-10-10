# ADR-0009: Append-Only Event Log and Ticket Close Gate

- **Status:** Proposed
- **Date:** 2026-10-10

## Context

The framework had observability fragments but no shared record:
`runs/verdicts.jsonl` (verdicts only), `runs/in_review.json` (current ticket
state, rewritten whole), and `veto-telemetry.py` / the watchdog reading them.
Four problems came out of a code read:

1. **Review could be skipped.** `ticket.py done <id>` marked any ticket done
   with no verdict, so an agent could close work that never went through
   review.
2. **Lost updates.** `in_review.json` was a read-modify-write with no lock.
   Two agents writing at once could drop a ticket or a status change. One
   team rarely hits this; hub-and-spoke with several teams will.
3. **Dropped veto alerts.** `veto-telemetry --watch` deduped on the
   millisecond `ts`. Two vetoes recorded in the same millisecond produced one
   alert.
4. **No join keys.** Records carried no event id, trace id, agent, harness
   version, model, tokens, or duration. Questions like "did the veto rate
   change after a harness edit?" could not be answered from the data.

This is also the first step toward moving the documented chain
(Research → PM → UX → Engineer → QA → CEO) from instruction to code. A state
machine needs an event record underneath it first.

The framework is bring-your-own-agent and public. Whatever is added must work
on Linux, macOS, and Windows, add no dependencies to the base install, and
make no network calls.

## Decision

**1. One append-only event log with a versioned envelope.**
`scripts/events.py` writes `runs/events.jsonl`. Every record uses the same
envelope (`schema_version`, `event_id`, `ts`, `ts_iso`, `kind`, `trace_id`,
`ticket`, `role`, `agent_id`, `harness_sha`, `constitution_version`, `model`,
`tokens_in`, `tokens_out`, `framework_units`, `duration_ms`, `outcome`,
`data`). Optional fields are always present and null when unknown. The
envelope is a public contract, documented in `scripts/events.schema.md`.
Readers raise on an unknown `schema_version` rather than mis-parse.

`trace_id` defaults to the ticket id, so every event for one ticket groups
without the caller tracking anything. `harness_sha` is read from `.git` files
directly, never through a subprocess, so it never hits an approval-gated
call site.

**2. Cross-platform file locking.** Every writer to a shared ledger takes a
sibling `<file>.lock` created with `O_CREAT | O_EXCL`. `fcntl` was rejected
because it does not exist on Windows. Locks older than 30 seconds are
treated as abandoned and broken. `in_review.json` is written atomically via
temp file + `os.replace`.

**3. Close gate in `ticket.py` (code, not instruction).**
- A ticket closes through a recorded PASS verdict.
- `done` refuses unless the latest verdict is PASS.
- A PASS carrying veto hits is refused.
- A veto opens on the ticket and blocks PASS until `clear-veto` runs.
  `clear-veto` requires operator approval (`scripts/approval.py`) and records
  who cleared it and why.
- `done --override` exists for real emergencies. It requires operator
  approval plus `--by` and `--reason`, and is recorded as an override.
- Every refusal is written to the event log as
  `ticket.transition_refused`, so bypass attempts are visible.

**4. Veto dedupe on `event_id`.** Verdict records now carry the `event_id` of
their event. Telemetry dedupes on it, falls back to a composite key for
pre-1.1 records, and migrates the old state file so an upgrade does not
re-alert old vetoes.

**5. Dual-write for compatibility.** `verdicts.jsonl` and `in_review.json`
keep their existing shapes so the watchdog, telemetry, dashboard, and any
operator shims keep working. In 1.1 they are written alongside the event
log. Deriving them from the event log is deferred.

## Consequences

- **Positive:** review can no longer be skipped through `ticket.py`.
  Concurrent writers through these scripts do not lose updates. Every vetoed
  verdict alerts. The data now supports per-edge cycle time, kick-back rate,
  veto rate per harness SHA, and cost per ticket once agents report tokens.
- **Positive:** no new dependencies, no network, works on Windows.
- **Negative:** the gate only covers writes that go through `ticket.py` and
  the MCP server. An agent that edits `runs/in_review.json` by hand is
  outside it. The capability report says so.
- **Negative:** `agent_id`, `model`, and token fields are self-reported by
  the caller and unauthenticated.
- **Negative:** dual-write means two records can disagree if a process dies
  between writes. The event log is the record of truth when they do.
- **Negative:** a lock-break race exists. If two waiters both see a stale
  lock in the same instant, one can remove the other's fresh lock. With a
  30-second threshold and millisecond critical sections this needs a crashed
  writer plus two waiters racing. Accepted for 1.1.
- **Behavior change:** `ticket.py done` on a ticket without PASS now exits
  2 instead of closing it. Any automation that relied on the old behavior
  breaks, on purpose.

## Alternatives considered

- **`fcntl` / `msvcrt` locking:** two code paths, and `fcntl` advisory locks
  behave differently on network filesystems. Rejected for the O_EXCL lock
  file.
- **A third-party lock library (e.g. `filelock`):** solid, but adds a
  dependency to the base install. Rejected for now; can be revisited.
- **SQLite as the event store:** gives transactions for free, but the logs
  stop being greppable text and every existing consumer needs rewriting.
  Rejected for 1.1.
- **Derive `verdicts.jsonl` and `in_review.json` from events now:** cleaner,
  but changes every consumer in one release. Deferred.
- **Ship OpenTelemetry export in this change:** deferred to an optional extra
  behind `network_permission=allow`, since export is egress.

## Next steps (not in this ADR)

1. Enforced chain state machine in the MCP server (`claim_next`, `submit`,
   `transition`) with KICK_BACK routing to the previous role.
2. Derive the compatibility views from the event log.
3. Optional OTel exporter, gated as egress.
4. Flip the watchdog default source from `paperclip` to `file` for public
   installs.

## References

- [[ADR-0007]] watchdog data source · [[ADR-0008]] continuous learning loop
- `scripts/events.py`, `scripts/events.schema.md`, `scripts/ticket.py`,
  `scripts/veto-telemetry.py`, `mcp/adversarial_mcp/server.py`
- `tests/test_events.py`, `tests/test_ticket.py`
- `docs/capability-report.md` §12.12

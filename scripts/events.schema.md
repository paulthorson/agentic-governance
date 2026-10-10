# Event log: envelope schema (version 1)

The stable reference for `runs/events.jsonl`, written by `scripts/events.py`
(ADR-0009). A consumer (dashboard, exporter, adapter) can implement against
this document without reading the source.

## Format

- One JSON object per line, UTF-8, append-only.
- Writers hold `runs/events.jsonl.lock` while appending, so lines never
  interleave.
- Malformed lines can appear after a crash mid-write. Readers skip them
  (the reference reader warns on stderr).

## Versioning

Every record carries `schema_version`. The current version is `"1"`. A
consumer that sees a version it does not recognize **MUST** fail loudly
rather than mis-parse. The reference reader raises `UnknownSchemaVersion`.

Adding a new `kind`, a new key inside `data`, or a new envelope field is not
a version change; consumers **MUST** ignore fields they do not know.
Removing, renaming, or retyping an envelope field is. Events written before
1.2 lack the 1.2 fields below.

## Envelope

Every field is always present. Optional fields are `null` when unknown.
Field order is stable.

| Field | Type | Description |
|---|---|---|
| `schema_version` | string | `"1"` |
| `event_id` | string | 32-char hex UUID4. Unique per event. Use this as the dedupe key. |
| `ts` | integer | Unix epoch milliseconds (UTC). |
| `ts_iso` | string | Same instant, ISO 8601 UTC. |
| `kind` | string | Event type. See below. |
| `trace_id` | string | Groups related events. Defaults to the ticket id; falls back to `event_id`. |
| `ticket` | string \| null | Ticket identifier (`T-12`). |
| `role` | string \| null | Chain stage or adversary domain the event concerns. |
| `agent_id` | string \| null | Self-reported by the caller. **Not authenticated.** Falls back to env `AG_AGENT_ID`. |
| `harness_sha` | string \| null | Git commit of the framework checkout, read from `.git` (env `AG_HARNESS_SHA` overrides). |
| `constitution_version` | string \| null | From env `AG_CONSTITUTION_VERSION`. |
| `model` | string \| null | Model that produced the work, if the caller reports it. |
| `tokens_in` | integer \| null | Caller-reported. |
| `tokens_out` | integer \| null | Caller-reported. |
| `framework_units` | number \| null | Framework spend units, if the caller reports them. |
| `duration_ms` | integer \| null | Caller-reported. |
| `outcome` | string \| null | Short result: a verdict, the resulting state, or `refused`. |
| `data` | object | Kind-specific detail. Never null. Ticket events committed since 1.2 carry `state_digest` (SHA-256 of the ticket file after the commit). |
| `agent_verified` | boolean | *1.2+.* True when `agent_id` came from a registry token (ADR-0011). False means self-reported. |
| `prev_hash` | string | *1.2+.* `hash` of the previous chained event; 64 zeros for the first. |
| `hash_alg` | string | *1.2+.* `hmac-sha256` (operator key) or `sha256` (no key). |
| `hash` | string | *1.2+.* `H(prev_hash + canonical JSON of this event without hash)`, canonical = sorted keys, `(",", ":")` separators, UTF-8. Verify with `ticket.py verify` (ADR-0012). |

## Kinds emitted (1.1 and 1.2)

| Kind | Emitted by | `outcome` | Notable `data` keys |
|---|---|---|---|
| `ticket.created` | chain | `queued` / `in_review` | `title`, `team`, `stages` |
| `ticket.claimed` | chain | `working` / `reviewing` | `mode`, `lease_minutes` |
| `ticket.heartbeat` | chain | current state | |
| `ticket.submitted` | chain | `in_review` | `summary` |
| `ticket.verdict` | chain | verdict | `veto_hits`, `summary`, `domain` |
| `ticket.advanced` | chain | `queued` | `from_stage`, `to_stage` |
| `ticket.kicked_back` | chain | `queued` | `from_stage`, `to_stage`, `kickbacks` |
| `ticket.blocked` | chain | `blocked` | `veto_hits` |
| `ticket.veto_cleared` | chain (human) | `in_review` | `cleared_by`, `reason` |
| `ticket.escalated` | chain | `escalated` | `reason` |
| `ticket.resolved` | chain (human) | `queued` | `by`, `reason`, `to_stage` |
| `ticket.closed` | chain | `done` | `via` (`verdict` / `override`), `by`, `reason` |
| `ticket.lease_expired` | recovery | `released` | `mode`, `attempt` |
| `ticket.stalled` | recovery | `stalled` | `waiting_for`, `minutes`, `message` |
| `ticket.awaiting_human` | recovery | `blocked` / `escalated` | `reason`, `message` |
| `ticket.transition_refused` | chain / CLI | `refused` | `transition`, `reason` |
| `verdict.recorded` | MCP `record_verdict` | verdict | `summary`, `rule`, `case_tag`, `source` |
| `verdict.overturned` | MCP `overturn_verdict` | `overturned` | `reason` |
| `store.committed` | chain | `saved` | `state_digest` (a commit with no other event) |
| `store.tamper_detected` | chain | `refused` | `reason` |
| `store.integrity_accepted` | `ticket.py integrity accept` | `accepted` | `by`, `reason`, `problem`, `log_problems`, `state_digest` |
| `store.integrity_keyed` | `ticket.py integrity init-key` | `keyed` | `state_digest` |
| `agent.registered` | `ticket.py agent add` | `registered` | `team`, `roles`, `principal` |
| `agent.revoked` | `ticket.py agent revoke` | `revoked` | |

## Example

```json
{"schema_version": "1", "event_id": "9f1c2e7a4b5d4c6e8f0a1b2c3d4e5f60", "ts": 1791640800000, "ts_iso": "2026-10-10T13:20:00+00:00", "kind": "ticket.kicked_back", "trace_id": "T-12", "ticket": "T-12", "role": "pm", "agent_id": "ux-critic", "harness_sha": "e57e8f3db07d9caf44b99ea057fe6002c5cf95e6", "constitution_version": null, "model": null, "tokens_in": null, "tokens_out": null, "framework_units": null, "duration_ms": null, "outcome": "queued", "data": {"from_stage": "ux", "to_stage": "pm", "kickbacks": 1}}
```

## Compatibility views

`runs/verdicts.jsonl` and `runs/in_review.json` keep their pre-1.1 shapes.
Ticket transitions write their events first and then save the ticket file,
both under the ticket lock, and each event's `ts` is the transition time.
Verdict records now include `event_id`. If a process dies between the event
write and the save, the log holds a transition the ticket file lacks; the
reverse cannot happen through `scripts/chain.py`.

# Calibration

The calibration ledger is the framework's memory of its own verdicts. Every
review outcome is recorded so the system is auditable and improvable.

## What gets recorded

Each domain ships a `references/calibration-ledger.md` template. The MCP
server appends structured verdict records to `runs/verdicts.jsonl` (gitignored
— real review history never gets committed):

```json
{
  "kind": "verdict",
  "domain": "engineer",
  "verdict": "KICK_BACK",
  "summary": "API key exposed in logs — security hole",
  "ticket": "THO-123",
  "ts": 1780000000000
}
```

## Why it matters

1. **Auditability** — every kick-back and allow is traceable to a ticket and a
   reason. No silent decisions.
2. **Calibration** — over time, the ledger reveals whether the adversaries are
   too strict (everything kicked back) or too lax (vetoes missed). The
   framework can be tuned against its own history.
3. **Improvement** — recurring veto hits point to systemic gaps in the
   producers' work, which is the real signal the framework exists to surface.

## Querying

The MCP `query_verdicts(domain, limit)` tool returns recent verdicts. The
`framework_status` tool reports the verdict log size.

## See also

- [[Architecture]] · [[Vetoes]] · [[MCP]] · [[Tooling]]

## 2026-09-06 — First real-team adoption (Ladders Grok Bot) — dry-run lesson

**Case:** First handoff of the framework to a real, pre-existing team (Ladders: CEO/PM/UX/Eng/QA, no Researcher), relayed via Openclaw Bridge.

**Finding (calibration):** Three adoption requirements surfaced that the framework did not anticipate:
1. Adopters take harness + constitution as a **loadable contract**, not a repo mirror — harnesses must be standalone-loadable (no repo-relative refs).
2. A **Researcher role must exist** on every adopting roster — without it, the evidence gate is skipped and the CEO is overloaded.
3. **Telemetry/watchdog are per-team responsibilities** — each adopting team runs its own, against its own alert channel; the framework host (Grimdor) does not run checks for other teams.

**Decision:** Recorded as ADR-0006. Ladders to spin up a Grok Research agent; Ladders to own its own telemetry/watchdog from the Grok side.

**Citation:** ADR-0006 · relayed 2026-09-06 via Openclaw Bridge.

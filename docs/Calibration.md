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

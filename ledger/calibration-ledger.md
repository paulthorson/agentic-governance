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

## 2026-09-06 — First real-team adoption (first adopting team / first product-seat adopter) — dry-run lesson

**Case:** First handoff of the framework to a real, pre-existing team (first adopting team: CEO/PM/UX/Eng/QA, no Researcher), relayed via product-seat bridge.

**Finding (calibration):** Three adoption requirements surfaced that the framework did not anticipate:
1. Adopters take harness + constitution as a **loadable contract**, not a repo mirror — harnesses must be standalone-loadable (no repo-relative refs).
2. A **Researcher role must exist** on every adopting roster — without it, the evidence gate is skipped and the CEO is overloaded.
3. **Telemetry/watchdog are per-team responsibilities** — each adopting team runs its own, against its own alert channel; the framework host does not run checks for other teams.

**Decision:** Recorded as ADR-0006. First adopting team to spin up a Research agent; first adopting team to own its own telemetry/watchdog from the product-seat side.

**Citation:** ADR-0006 · relayed 2026-09-06 via product-seat bridge.

## 2026-09-06 — First adopting team data-source decision (Paperclip coupling)

**Case:** First adopting team confirmed their issue/verdict store: GitHub PRs + epic markdown, no `in_review` ticket store, no Paperclip.

**Finding (calibration):** The stuck-review-watchdog is Paperclip-native and does not drop into a non-Paperclip team; veto-telemetry is file-based and portable. The framework's logic is portable, but the watchdog's data source must be abstracted for vanilla handoff.

**Decision (first adopting team, 2026-09-06):** telemetry ON (first-adopting-team-scoped verdicts log, alerts to product-seat chat for now); watchdog OFF until first adopting team has an in_review backend (GitHub PR review state or file ledger in epic folder); no Paperclip on first adopting team; veto-class issues escalate to the operator in chat until then.

**Action:** abstract the watchdog data source (ADR-0007).

**Citation:** ADR-0006 D4 · relayed 2026-09-06 via product-seat bridge.

## 2026-09-06 — Watchdog data-source abstraction (ADR-0007)

**Case:** First adopting team does not use Paperclip; the stuck-review-watchdog was Paperclip-native and could not drop in.

**Finding (calibration):** the watchdog's logic (staleness, dedupe, alerting) is portable; only its data source was coupled. The framework must be vanilla-handoffable.

**Decision:** abstract the watchdog data source. `--source paperclip` (default, unchanged) or `--source file --issues-file <path>` (JSON file or stdin). Any team's store adapts by emitting the issue shape. `collect_stuck` unchanged.

**Action:** implemented in `scripts/stuck-review-watchdog.py`; recorded as ADR-0007.

**Citation:** ADR-0007 · 2026-09-06.

## 2026-09-14 — COUNSEL_GATE

**Case:** A production-facing acceptance path shipped without a recorded human counsel clearance.

**Finding:** Draft legal artifacts are not production SoT until a named human records clearance.

**Decision:** Record `COUNSEL_GATE` as a scar. Apache-2.0 LICENSE is the only use governor. No acceptance gate.

**Citation:** 2026-09-14.

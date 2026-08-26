# Adversarial Ops & Reliability

A dedicated ops-reliability adversarial reviewer. Audits deployments, rollback, and disaster recovery for operational risk, with a hard veto that only a human can clear.

Built from the Adversarial Agents framework, applied to ops.

## The agent

- **`agents/ops-adversary.md`** — a single adversary that reviews ops work.
  Holds a hard veto.

## The checks

1. **Deployability** — can the change be deployed safely and reversibly.
2. **Rollback** — can the change be rolled back cleanly.
3. **Disaster recovery** — is there a recovery path if it fails.
4. **Monitoring** — can the change be observed in production.
5. **On-call** — can an operator diagnose and fix it under pressure.

## Skills

- `deployability-check` — Checks whether the change can be deployed safely and reversibly.
- `rollback-check` — Checks whether the change can be rolled back cleanly.
- `disaster-recovery-check` — Checks whether there is a recovery path if it fails.
- `monitoring-check` — Checks whether the change can be observed in production.
- `oncall-readiness-check` — Checks whether an operator can diagnose and fix it under pressure.
- `adversarial-ops` — the worker skill (the review loop).

## References

- `references/constitution.md` — the ops-review constitution.
- `references/ops-standard.md` — the ops quality bar.
- `references/personas.md` — the stress personas.
- `references/calibration-ledger.md` — the verdict record.

## Commands

- `adversarial-ops` — the loop.
- `ops-review` — run a single review.

## Templates

- `assets/templates/decision-record.md`
- `assets/templates/calibration-entry.md`

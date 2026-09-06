# Ops Domain — deep dive

**Plugin:** `adversarial-ops/` · **Veto:** irreversible deployment, no rollback, no DR

## What it reviews

Deployment, rollback, and disaster recovery. An ops/reliability reviewer that
audits deployability, rollback, DR, monitoring, and on-call readiness.

## Adversary agents

| Agent | Role |
|---|---|
| `ops-adversary` | The single reviewer — audits deployability, rollback, DR, monitoring, and on-call readiness |

## The checks

- **Deployability check** — can this be deployed safely?
- **Rollback check** — can it be rolled back if it fails?
- **Disaster-recovery check** — is there a DR plan?
- **Monitoring check** — will failures be detected?
- **On-call readiness** — can an operator respond?

## Skills

`ops-deployability-check`, `ops-rollback-check`, `ops-disaster-recovery-check`,
`ops-monitoring-check`, `ops-oncall-readiness-check`, `ops-adversarial-ops` (worker).

## Constitution / veto

The ops constitution gates on **irreversible deployment, no rollback, and no
DR** — a change that cannot be rolled back or recovered is kicked back. Only a
human clears a veto.

## How to use

```
Use the governance server to run a review of this deployment in the ops domain:
<your change>
```

## See also

- [[Domains]] · [[Architecture]] · [[Constitution]]

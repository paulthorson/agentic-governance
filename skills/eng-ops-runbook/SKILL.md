---
name: eng-ops-runbook
description: Produce deploy, rollback, monitor, and incident-runbook artifacts for an engineering change, so the Reliability Reviewer and Ops Advocate can check them.
argument-hint: "<the change>"
---

# Ops Runbook

Produce operational artifacts. Input in, artifact out. No verdict.

## Output

1. **Deploy** — the exact steps, in order, and what a half-success looks like.
2. **Rollback** — the exact steps to undo, and what is lost if rolled back.
3. **Monitor** — the specific signals (alerts, dashboards, logs) to watch, and what each
   abnormal value means.
4. **Incident path** — the first actions a paged operator takes.
5. **Irreversible actions** — named, with their guard.
6. **Unknowns** — steps you could not write because the ops contract is not defined.

```
## OPS RUNBOOK

### Deploy
- <steps, and the first signal of silent failure>

### Rollback
- <steps | what is lost on rollback>

### Monitor
| Signal | Tool/where | Normal | Abnormal means |
|---|---|---|---|

### Incident (first 5 minutes)
- <what the paged operator does>

### Irreversible
- <action | fence/guard | blast radius>

### Cannot write yet
- <deploy tool unset, no monitoring stack,.>
```

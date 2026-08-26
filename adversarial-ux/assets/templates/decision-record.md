# Decision Record: <run title>

Run ID: <yyyy-mm-dd-slug>
Diamond: <Discover & Define | Develop & Deliver>
Started: <timestamp>
Human arbiter: <name>

**This file is append-only.** Nothing above a committed line is edited. A correction is a new
entry that references the entry it corrects.

---

## 1. Request

> <the request, verbatim>

Solution shape assumed by the request: <what it presumed, or "none">

## 2. Artifacts produced

| Skill | Artifact | Path |
|---|---|---|

## 3. Decisions

### D1: <decision>
- **Chose.** <what>
- **Over.** <alternatives, each with its trade-off sentence>
- **Because.** <rationale, written plainly, including what is uncertain>
- **business_goal.** <metric and direction>
- **cost_driven.** <true | false>. If true: user gives up <X>, team saves <Y>
- **Confidence.** <high | medium | low>. <What would raise it>
- **Unknown at decision time.** <what nobody knew>

## 4. Options presented

| Option | Trades away | To get |
|---|---|---|

## 5. Neutral facts issued to the Advocate

Path: `facts.md`
Contamination self-check performed: <yes | no>

## 6. Verdicts

Pasted verbatim, before any response from the worker.

### Critic
```
<verbatim>
```

### CX-Quality Advocate
```
<verbatim>
```

### Evaluative UXR
```
<verbatim>
```

Review isolation: <parallel subagents | run in series, weaker>

## 7. Worker response to verdicts

For each finding: accepted and revised, or disputed with reasoning. The worker may not mark
anything cleared.

| Finding | Response | Status |
|---|---|---|
| <id> | <revision made, or dispute> | open / revised / awaiting human |

## 8. Gate

Gate: <1 | 2>
Routed because: <veto active | blocker open | cost_driven true | business_goal unnameable | scheduled gate>

### Human decision
- Arbiter: <name>
- Date: <date>
- Decision: <approved | rejected | approved with override>
- Reason: <stated reason>
- Vetoes cleared: <which, and on what basis, or "none">

## 9. Skips

| What was skipped | Instructed by | Recorded at |
|---|---|---|

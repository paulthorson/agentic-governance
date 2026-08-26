# Decision Record: <QA run title>

Run ID: <yyyy-mm-dd-slug>
Lane: <Discover & Define | Develop & Deliver>
Started: <timestamp>
Human arbiter: <name>

**This file is append-only.** Nothing above a committed line is edited.

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
- **Because.** <rationale, plainly>
- **product_goal.** <metric and direction>
- **scope_driven.** <true | false>. If true: user gives up <X>, team ships faster by <Y>
- **Confidence.** <high | medium | low>
- **Unknown at decision time.** <what nobody knew>

## 4. Test strategies considered

| Strategy | Trades away | To get |
|---|---|---|

## 5. Neutral facts issued to the Quality Advocate

Path: `facts.md`
Contamination self-check performed: <yes | no>

## 6. Verdicts

Pasted verbatim, before any response from the worker.

### Critic
```
<verbatim>
```

### Quality Advocate
```
<verbatim>
```

### Edge-Case Reviewer
```
<verbatim>
```

Review isolation: <parallel subagents | run in series, weaker>

## 7. Worker response to verdicts

| Finding | Response | Status |
|---|---|---|
| <id> | <revision made, or dispute> | open / revised / awaiting human |

## 8. Gate

Gate: <1 | 2>
Routed because: <veto active | blocker open | scope_driven true | product_goal unnameable | scheduled gate>

### Human decision
- Arbiter: <name>
- Date: <date>
- Decision: <approved | rejected | approved with override>
- Reason: <stated reason>
- Vetoes cleared: <which, and on what basis, or "none">

## 9. Skips

| What was skipped | Instructed by | Recorded at |
|---|---|---|

# Compliance Standard

The quality bar for compliance work to pass adversarial review.

## Required inputs

A piece of compliance work must carry, or reference, each of these. A missing
input is a finding (UNVERIFIABLE for the checks it would support).

| Input | Purpose | Supports check |
|-------|---------|-----------------|
| `work` | The compliance artifact under review | All checks |
| `alternatives` | What the work trades away | Rule 2 |
| `convenience_driven` | Whether the fast path silently won | Rule 3 |
| `falsifiability` | What would show each claim false | Rule 4 |

## Quality bar

1. **No irrecoverable harm.** No compliance outcome that cannot be undone.
2. **Genuine alternatives.** The work names what it trades away.
3. **No silent fast path.** The easy option that changes the outcome is stated.
4. **Falsifiable.** Each central claim names what would show it false.
5. **Complete.** No required input is missing or UNVERIFIABLE without a stated
   reason.

## Severity mapping

- **BLOCKER** — irrecoverable harm, or a claim that drives action with no
  support.
- **CONCERN** — real but recoverable, or a blind spot worth naming.
- **NOTE** — would fix if free.

## Veto conditions

- regulatory violation, policy violation, no evidence of compliance, no audit trail.

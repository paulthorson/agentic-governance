# QA Standard

The baseline the QA Critic checks against. Ships with placeholders. Fill in the real test
commands, environments, and coverage targets before the Critic's checks mean anything.

```yaml
test_command: UNSET # e.g. pnpm test
e2e_command: UNSET # e.g. playwright test
lint_command: UNSET
coverage_threshold: UNSET # e.g. unit >= 80%, critical paths 100%
environments: UNSET # e.g. local, staging, prod
last_verified: UNSET
```

## The four checks the Critic runs

### Check 1: Acceptance criteria are testable
- Every acceptance criterion maps to an observable, verifiable condition. No "works well",
  "feels fast", "user-friendly".
- Criteria that cannot be tested are named as such, not silently treated as testable.

### Check 2: Coverage is real, not numeric
- Critical and irreversible paths are covered (or the gap is named with a reason).
- Failure, boundary, empty, and error states are covered, not just the happy path.
- If a coverage number is claimed, it is backed by a command that produces it. Otherwise the
  check is UNVERIFIABLE.

### Check 3: Defect severity is honest
- Blockers are true blockers (unrecoverable harm or complete task failure), not style nits.
- Severity is not inflated to look thorough, and not deflated to keep a release on schedule.
- A finding that blocks a release says what must change to unblock it.

### Check 4: Reversibility and release readiness
- Any feature that can cause unrecoverable harm has a regression test or a named gap.
- The release gate lists what is verified and what is explicitly not verified.
- No release is gated as passing when a required check is UNVERIFIABLE.

## If a check is UNVERIFIABLE
Report UNVERIFIABLE and say why. Never report an unverifiable check as a pass.

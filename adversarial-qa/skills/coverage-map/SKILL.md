---
name: coverage-map
description: Map what a test plan tests versus not, naming the gaps, without a verdict on whether coverage is adequate.
argument-hint: "<the plan and feature>"
---

# Coverage Map

Pure inventory. No verdict.

## Output

1. **Covered** — paths with a test, and what the test asserts.
2. **Untested** — paths with no test, and why it matters.
3. **Happy-path only** — places where only the success path is covered and failure/empty/error
   states are not.
4. **Untestable** — paths that cannot be tested as written, named.
5. **Not checkable** — no test command configured, say so.

```
## COVERAGE MAP

| Path/behavior | Test? | What it asserts | Gap if untested |
|---|---|---|---|

### Failure-path coverage
- <which failure paths are tested, which are not>

### Not checkable
- <test_command unset, no tests found — say so>
```

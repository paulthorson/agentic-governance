---
name: eng-test-coverage-map
description: Map what is tested versus untested in a proposed change, naming the gaps, without a verdict on whether coverage is good enough.
argument-hint: "<the change and its tests>"
---

# Test Coverage Map

Produce a coverage inventory. Input in, artifact out. No verdict.

## Output

1. **Covered** — paths with a test, and what the test asserts.
2. **Untested** — paths with no test, and why that matters.
3. **Untestable** — paths that cannot be tested as written (structure or missing seam), named.
4. **Failure-path coverage** — whether error/async/empty states are tested.
5. **What could not be checked** — e.g. no test command configured.

```
## TEST COVERAGE MAP

| Path/behavior | Test? | What it asserts | Gap if untested |
|---|---|---|---|

### Failure paths
- <which error/async paths are tested, which are not>

### Not checkable
- <test command unset, no tests found, code not inspectable — say so>
```

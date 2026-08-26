---
name: test-case-generation
description: Generate test cases from acceptance criteria, including failure, boundary, and empty paths, without a verdict.
argument-hint: "<the criteria>"
---

# Test Case Generation

Pure artifact. No verdict.

## Output

1. **Happy-path cases** — from each testable criterion.
2. **Boundary cases** — edge values, max lengths, off-by-one, empty input.
3. **Failure-path cases** — validation failure, timeout, network loss, back/refresh, re-entry,
   double submission.
4. **Irreversible-action cases** — with an assertion that the confirmation and recovery path
   behave correctly.
5. **Accessibility cases** — screen-reader, keyboard-only, focus visibility (when the product
   is a UI).

```
## TEST CASES

| ID | Given | When | Then | Type |
|---|---|---|---|---|

### Irreversible-action cases
- <cases covering confirmation, undo, recovery>

### Accessibility cases
- <cases, or "not applicable / not stated">
```

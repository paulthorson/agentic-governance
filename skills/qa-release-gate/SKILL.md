---
name: qa-release-gate
description: State the pass criteria for shipping a release, and what is explicitly not verified, without a verdict.
argument-hint: "<the release>"
---

# Release Gate

Pure artifact. No verdict.

## Output

1. **Required checks** — each pass criterion, and the command/evidence that verifies it.
2. **Verified** — what has actually been confirmed, with the evidence.
3. **Not verified** — what is explicitly unconfirmed and why, named as such (never implied).
4. **Irreversible scope** — anything in this release that can cause unrecoverable harm and is
   routed to the human gate.

```
## RELEASE GATE

| Required check | Verifies | Evidence | Verified? |
|---|---|---|---|

### Not verified (named)
- <check | why | what would verify it>

### Irreversible scope
- <item | harm | routed to human gate?>
```

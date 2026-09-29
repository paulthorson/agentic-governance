# Proposal: A20 — where validation records live

**Status:** DECIDED — Option A approved by operator on 2026-09-06.
**Date:** 2026-09-06
**Related:** A11c validation record. (This is a distinct decision from A17, which
remains open on its own subject — no project repo for governance-repo work.)

## The problem

The A11c run surfaced a concrete instance of an unresolved question: the validation
record — the only evidence an adversarial check can fail — had no defined home. We
pragmatically placed it at `docs/a11c-validation-record.md`, but that was an ad-hoc
choice, not a decided rule.

## The decision needed

Where do validation records (the evidence artifacts produced by end-to-end runs)
live, and how are they named?

## Options

### Option A — `docs/validation-records/` (recommended)

A dedicated directory under `docs/` for run evidence.

- **Pros:** Co-locates evidence with the spec and addenda it validates; simple;
  discoverable; no new tooling.
- **Cons:** `docs/` is currently a mix of reference and evidence; needs a naming
  convention to stay tidy.
- **Naming:** `docs/validation-records/YYYY-MM-DD-<epic>-<run>.md`, e.g.
  `2026-09-05-watchdog-json-a11c.md`.

### Option B — `evidence/` at repo root

A top-level directory parallel to `docs/`, `scripts/`, `harnesses/`.

- **Pros:** Clean separation of evidence from reference docs; scales if evidence
  volume grows.
- **Cons:** New top-level dir; the structure validator (`scripts/validate.py`)
  may need updating to allow it.

### Option C — keep the ad-hoc `docs/<name>.md` pattern

No new rule; each record placed where it seems fit.

- **Pros:** No change.
- **Cons:** Exactly the ambiguity this decision is trying to resolve; records
  scatter and become undiscoverable.

## Recommendation

**Option A** — `docs/validation-records/` with a dated, epic-scoped naming
convention. It is the smallest change that gives validation records a stable,
discoverable home, and it keeps evidence next to the spec it validates. The
existing `docs/a11c-validation-record.md` would move into the new directory as
the first entry.

## Decision (2026-09-06)

**Option A approved by the operator.** Validation records live in
`docs/validation-records/` with the naming convention
`YYYY-MM-DD-<epic>-<run>.md`. The existing `docs/a11c-validation-record.md` is
left in place (not moved) to avoid churn; new records use the new directory.
The A18.3 clean-test record (`docs/validation-records/2026-09-06-a183-clean-test.md`)
is the first entry under the decided convention.

This decision is recorded as **A20** in `docs/spec-addendum-01.md`. It does not
resolve A17, which remains open on its own subject.

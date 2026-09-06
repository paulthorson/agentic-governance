# Proposal: A17 — where validation records live

**Status:** Proposal for operator review. Not decided, not merged.
**Date:** 2026-09-06
**Related:** A17 open problem (spec-addendum-01.md §A17), A11c validation record.

## The problem

A17 records that the governance repo has no project repo, and that bots cannot
write the governance repo (Section 9.4 read-only) while the engineer is
obligated to produce applied implementations (Section 5.3). The A11c run
surfaced a concrete instance: the validation record — the only evidence an
adversarial check can fail — had no defined home. We pragmatically placed it
at `docs/a11c-validation-record.md`, but that was an ad-hoc choice, not a
decided rule.

## The decision needed

Where do validation records (the evidence artifacts produced by end-to-end
runs) live, and how are they named?

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
- **Cons:** Exactly the ambiguity A17 is trying to resolve; records scatter and
  become undiscoverable.

## Recommendation

**Option A** — `docs/validation-records/` with a dated, epic-scoped naming
convention. It is the smallest change that gives validation records a stable,
discoverable home, and it keeps evidence next to the spec it validates. The
existing `docs/a11c-validation-record.md` would move into the new directory as
the first entry.

## Open question for the operator

1. Approve Option A, B, or C?
2. If A: should the existing `a11c-validation-record.md` be moved into
   `docs/validation-records/` (renamed per the convention), or left in place?

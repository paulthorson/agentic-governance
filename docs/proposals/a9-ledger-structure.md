# Proposal: A9 — the calibration ledger's structure and growth

**Status:** DECIDED — Option A for both questions, approved by operator
on 2026-09-06. Recorded as **A21** in spec-addendum-01.md.
**Date:** 2026-09-06
**Related:** A9 open problem (spec-addendum-01.md §A9), now resolved by A21.

## The problem

The calibration ledger does three jobs — precedent for CEO rulings (10.2),
promotion history for the autonomy ladder (A2.2), and the audit trail for
adversarial review of rulings (12.5) — but it is prose in a markdown file. Two
questions have no answer: what a precedent matches on, and what happens as the
ledger grows.

## Decision 1: What does a precedent match on?

Three options, from most to least structured:

### Option A — Structured fields on each entry (recommended)

Each ledger entry carries a small set of machine-readable fields: the rule
cited, the domain, the decision, and a short "case" tag. The CEO bot matches on
these fields first, then reads the prose to confirm.

- **Pros:** Predictable matching; searchable; prunable; the "materially similar"
  test becomes a field comparison plus a confirmation read.
- **Cons:** Requires a schema change to the ledger and a migration of existing
  entries; writers must fill the fields.

### Option B — Tags only

Each entry carries free-form tags; matching is on tag overlap, with the
arguable-means-escalate rule (10.1) as the backstop.

- **Pros:** Lighter than full fields; less migration.
- **Cons:** Tags are only as consistent as the writer; still leaves "materially
  similar" partly to model judgment.

### Option C — Accept model judgment, constrained

Keep prose entries; matching is whatever the model decides, constrained by the
existing "arguable means escalate" rule.

- **Pros:** No change; simplest.
- **Cons:** Exactly the unpredictability precedent exists to prevent; no
  improvement.

## Decision 2: What happens as the ledger grows?

### Option A — Age-out with a retention rule (recommended)

Define what ages out: an entry not cited within N days is summarized to a
one-line stub (or archived), and a precedent that is never cited stops
persisting in full. The human sets N.

- **Pros:** Bounded growth; old-but-relevant precedent survives as a stub.
- **Cons:** Needs a summarization/archival mechanism; a stub loses detail.

### Option B — Summarize, never delete

Old entries are summarized into a digest; nothing is removed.

- **Pros:** Full history preserved.
- **Cons:** The digest itself grows; the "load before every ruling" cost
  persists.

### Option C — No growth policy

Leave it; the ledger grows without bound.

- **Pros:** No change.
- **Cons:** The load-before-every-ruling cost grows unbounded; the exact failure
  A9 names.

## Recommendation

**Decision 1: Option A** (structured fields) — it makes precedent predictable
and is the only option that also makes pruning tractable. **Decision 2: Option
A** (age-out with retention) — bounded growth with a human-set retention window.

These interact: a structured ledger is easier to search and to prune, which is
why both lean structured.

## Open questions for the operator

1. Approve Decision 1 (precedent matching) — A, B, or C?
2. Approve Decision 2 (growth) — A, B, or C?
3. If structured fields: what is the exact field set, and who migrates existing
   entries?
4. If age-out: what is the retention window N?

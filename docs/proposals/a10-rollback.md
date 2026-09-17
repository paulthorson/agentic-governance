# Proposal: A10 — rollback (decision framework)

**Status:** DECIDED — all three decisions as recommended, approved by operator
on 2026-09-06. Recorded as **A22** in spec-addendum-01.md.
**Date:** 2026-09-06
**Related:** A10 open problem (spec-addendum-01.md §A10), now resolved by A22.

## The problem

The framework stops bad work before it lands (vetoes, gates, adversarial
review, A1 reversibility). None of that helps once something has passed every
gate and turned out to be wrong. There is no mechanism to withdraw committed
work, no way to mark a ruling as mistaken after the fact, and no link from an
artifact back to the ruling that permitted it. A wrong decision stays in the
ledger as good precedent and can be cited again.

## The three decisions

### Decision 1: Can a precedent be overturned, and by whom?

**Recommended: yes, by the human** — matching who clears a veto. An overturned
precedent gets a **status** (e.g., `overturned`), not deletion, so the record of
the mistake survives alongside the correction.

- The human marks a ruling `overturned` with a reason and a date.
- The ledger keeps the entry but flags it so it is no longer citable as
  precedent.
- A bot that would have cited it must instead escalate (the overturned status
  makes the match "arguable," which already means escalate under 10.1).

### Decision 2: What happens to work approved under an overturned precedent?

**Recommended: leave it in place, but flag it.** Withdrawing committed work is
usually more disruptive than leaving it. The system records that the work was
approved under a precedent now overturned, so it is known to be work the system
would not approve today — but it is not automatically withdrawn.

- The operator decides per-case whether to withdraw, leave, or remediate.
- The default is leave-and-flag, because automatic withdrawal risks more harm
  than it prevents.

### Decision 3: What links an artifact to the ruling that permitted it?

**Recommended: a provenance field on the artifact.** Each artifact records the
ruling (ledger entry id) that permitted it. This gives the blast radius of a bad
precedent: given a ruling, you can find every artifact that cites it.

- This is the piece that makes Decisions 1 and 2 tractable — without the link,
  you cannot know what an overturned precedent affected.

## What this requires

- A `status` field on ledger entries (active / overturned).
- A provenance field on artifacts linking back to the permitting ruling.
- A human-facing action to overturn a ruling.
- A query to find all artifacts citing a given ruling.

## Open questions for the operator

1. Approve Decision 1 (human overturns, status not deletion)?
2. Approve Decision 2 (leave-and-flag by default, operator decides per-case)?
3. Approve Decision 3 (provenance field linking artifact to ruling)?
4. Is this the right scope, or should rollback be deferred until the ledger
   (A9) is structured — since provenance and status both depend on ledger
   structure?

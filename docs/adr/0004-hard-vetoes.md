# ADR-0004: Hard Vetoes, Human-Only Clearing

- **Status:** Accepted
- **Date:** 2026-08-26

## Context

Some harms are not recoverable: a leaked credential, a bricked config, a
fabricated user driving a product decision, a dead end for a screen-reader
user. If an AI can clear these, the framework's safety guarantee is hollow.

## Decision

Adversary agents hold **hard vetoes** for irrecoverable harm. A veto kicks the
work back; **only a human arbiter clears it**, with a stated reason in the
decision record. No AI may clear a veto, downgrade a blocker, or mark a review
passed.

## Consequences

- **Positive:** Irrecoverable harm is stopped, not negotiated. The human gate
  is real.
- **Negative:** Requires a human to be available to clear legitimate vetoes.

## Alternatives considered

- **AI can clear vetoes with justification** — rejected: an AI can always
  justify its own decision.

## References

- `constitution/vetoes.md`
- `constitution/constitution.md`

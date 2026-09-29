# ADR-0001: The Governed Adversarial Review Loop

- **Status:** Accepted
- **Date:** 2026-08-26

## Context

Every piece of work (code, design, research, decision, message) needs review
before it proceeds. Traditional review is advisory — a reviewer comments, the
author decides. For an AI-agent system, advisory review is too weak: an agent
can argue away a blocker or proceed with a note that it was considered.

## Decision

Adopt a **governed adversarial review loop**: every ticket goes to `in_review`,
a domain-matched adversary agent reviews it blind, and either kicks it back
(with findings) or allows it. Adversaries hold **hard vetoes** for
irrecoverable harm; only a human clears a veto. The loop is governed by a
constitution, not by style-guide taste.

## Consequences

- **Positive:** Irrecoverable harm (data loss, security holes, user harm,
  unsupported claims) is stopped, not just flagged. The system is auditable
  via the calibration ledger.
- **Negative:** Adds a review step to every ticket. Requires adversary agents
  to be available (mitigated by the stuck-review watchdog).

## Alternatives considered

- **Advisory review only** — rejected: too weak for an AI-agent system.
- **No review** — rejected: no safety net.

## References

- `docs/Architecture.md`

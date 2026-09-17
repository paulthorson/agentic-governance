# Learning 2026-09-13 — Builders never get the last word

## What happened

Across every 2026-09-13 workstream (phone access, design-system monorepo, roadmap
restoration), the builder's own "looks done" was never accepted. Each workstream
ran a separate verification pass with independent evidence: screenshots, command
transcripts, test runs, byte-identity checks.

## Learning

Adversarial review is a role with a name, not a vibe. The reviewer's job is to
reject, and the loop isn't done until they sign off with zero open issues. The
KICK_BACK rate (≈47% of decided verdicts on 2026-09-12/13) shows the loop fires
in practice.

## What changed

Framework rule: KICK_BACK returns work to the builder for rework and re-review
with a FRESH reviewer. Builders never clear blockers; only the human (operator)
clears a veto via `overturn_verdict`.

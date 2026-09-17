# Learning — adversarial review at the subagent depth limit

Date: 2026-09-13. Run: Veto Initiative 07 (mentor matching & warm paths),
`muse/2026-09-13/roadmap-exec/init-07-*`.

## What happened

The Initiative 07 build coordinator ran at runtime depth 2/2 with
`can_spawn=no`: no subagents could be spawned, so the framework's normal
pattern — builder ships, independent blind reviewer judges — was
impossible to staff. The coordinator executed the build directly as six
sequential workstreams, then ran the framework's `run_review` for each
workstream (structural veto scan + the domain's real adversary prompts:
critic, edge-case-reviewer, quality-advocate) and performed the
adversarial review itself, work-product-only, against those prompts.

## What we learned

Adversarial self-review under the framework's prompts still finds real
defects — 8 across 3 workstreams, including a TTL enforced by nothing (no
background sweeper existed), capacity never consumed on consent, blocked
actors still surfacing in discovery, audit withdrawals misattributed to
the wrong actor, and a CLI flag default that silently recorded "decline".
The prompts, not the reviewer's independence, did most of the finding;
independence mostly prices in the things self-review rationalizes away.

But self-review cannot satisfy the framework's blind-isolation invariant,
and recording ALLOW verdicts from it without disclosure would launder the
provenance. The honest move is to record the verdicts with the isolation
caveat stated in the summary itself, and to route the existing human gate
(the roadmap's pre-pilot "operator + independent framework reviewer must pass
the consent/abuse suite") as the backstop that restores blind review
before any real users are involved.

## What changed

- All six Initiative 07 verdicts carry an explicit reviewer-isolation
  caveat in their recorded summaries; the EVIDENCE.md discloses it under
  Caveats and names the pre-pilot human gate as the corrective.
- Pattern for future depth-limited runs: run `run_review`, apply the
  adversary prompts to the work product alone, fix findings, re-verify,
  record with caveat, and never present a self-reviewed ALLOW as
  equivalent to a blind-reviewed one.

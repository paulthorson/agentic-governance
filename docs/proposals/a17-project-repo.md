# Proposal: A17 — no project repo for governance-repo work

**Status:** DECIDED — Option B (exception path), approved by operator
on 2026-09-06. Recorded as **A24** in spec-addendum-01.md.
**Date:** 2026-09-06
**Related:** A17 open problem (spec-addendum-01.md §A17), now resolved by A24.
Distinct from A20 (where validation records live), which is decided.

## The problem

This repo has no separate project repo. Every real change targets the governance
repo itself, which bots cannot write. The read-only rule (Section 9.4) and the
engineer's obligation (Section 5.3) cannot both hold for governance-repo work:
the engineer is required to produce an applied implementation, but writing to
the governance repo is forbidden.

## The options

### Option A — A separate project repo

Work product lives in a project repo (as Section 1 assumes), and the governance
repo stays read-only. This is the framework's intended shape, but this repo has
no such project repo.

- **Pros:** Matches the framework's design; bots can write freely to the project
  repo; governance repo stays protected.
- **Cons:** Requires creating and maintaining a second repo; work product is
  split across two repos.

### Option B — An exception path for governance work (recommended)

A defined path where a human applies the change, since bots cannot write the
governance repo. The engineer produces the diff; the human applies it.

- **Pros:** No new repo; keeps the governance repo read-only to bots; the human
  gate is explicit and matches the framework's philosophy (humans clear vetoes,
  humans apply governance changes).
- **Cons:** Every governance change needs a human to apply it; slower for
  routine changes. This is the path we have effectively been using (the
  `--json` patch was produced by the engineer and applied by a human).

### Option C — Scope the framework to exclude self-modification

The framework governs work product, not changes to itself; governance-repo
changes are out of scope and handled by humans directly.

- **Pros:** Cleanest conceptually; removes the contradiction entirely.
- **Cons:** The framework no longer governs its own evolution; a governance
  change is not itself governed, which is a real gap.

## Recommendation

**Option B** — the exception path. It is the smallest change that resolves the
contradiction, keeps the governance repo read-only to bots, and matches how we
have actually been working (engineer produces a diff, human applies it). It
does not require a second repo, and it keeps the human gate explicit.

Option A is the framework's intended long-term shape if you want a project repo;
Option C is the cleanest conceptually but removes governance from the framework's
own evolution.

## Open questions for the operator

1. Approve Option A, B, or C?
2. If B: should the exception path be documented as a formal procedure (e.g., a
   `docs/proposals/` + human-apply workflow), or left as the informal
   engineer-produces-diff / human-applies pattern?

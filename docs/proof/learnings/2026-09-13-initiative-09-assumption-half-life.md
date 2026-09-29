# 2026-09-13 — Assumption flags have a half-life; declarative copies of enforcement numbers are invented metrics

Two findings from Initiative 09's adversarial review, both worth carrying
into every future build.

## 1. Re-verify assumed-absent dependencies right before writing parallel code

Initiative 09 began with a documented assumption: "Initiative 03's
provider-health contract is not published yet." A coordinator grep at build
start confirmed it — and then the 03 team's file appeared in-tree mid-build.
The parallel health interface was already written before the stale
assumption was caught in review. The fix (rewriting as an adapter over 03's
contract) was cheap only because the review caught it the same day.

**Rule:** a grep at build start is not enough. Re-verify an
assumed-absent dependency at the moment before you write the parallel
implementation. The check costs minutes; the second write path costs a
migration.

## 2. If enforcement doesn't use the number, the UI must not show it

The first version of the provider contract kit declared per-provider daily
budgets in its own table. The numbers looked reasonable — and were fiction:
`compliance.py` enforces tier-based budgets (official 1000 / scraping 40),
so the scorecard would have displayed "budget used / total" against totals
nothing enforces. A declarative copy of an enforcement number is an invented
metric by another name.

**Rule:** display numbers must be derived from the enforcing module as the
single source of truth, not mirrored in a second table that can drift. The
conformance suite now asserts the displayed budget equals the enforced one —
the honesty guarantee is a test, not a convention.

## 3. (Reinforcing, from the same ship) Shared-tree pushes need a protocol

Two coordinators committing to one repo on one VM collided twice in an
hour: a `git commit --amend` landed on the wrong HEAD after a concurrent
reset, and a rebase swept one file into another team's commit. Both were
recovered because every step was verifiable (`git reflog`, `git show`,
test runs on the merged tree) — but the recovery cost an hour. Parallel
builders on a shared tree should push through isolated worktrees or
per-team branches and merge, never amend/reset a moving HEAD.

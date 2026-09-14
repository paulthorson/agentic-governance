# Approval must be content-pinned and self-invalidating

2026-09-13 — from the Initiative 05 application-studio build
(`muse/2026-09-13/roadmap-exec/init-05/ws4`, engineer domain, ALLOW).

## What happened

The application packet's approval was first designed as a status flag:
checklist passes → `status = "approved"`. The framework's reliability
reviewer asked what happens when content changes *after* approval — a
reviewer marks one more diff item reviewed, or a refresh surfaces a new
blocker. The flag would have kept blessing content that no longer
matched what was reviewed.

## What we learned

A sticky "approved" flag that survives content edits is a dishonest
receipt. Approval must pin the exact content it blesses (here, a
SHA-256 over the packet body) and invalidate itself on any review-state
edit or any newly surfaced checklist blocker — reverting to draft and
dropping the approval stamps. Re-checking the checklist on every state
change is cheap; trusting a stale flag is how unreviewed content ships.

## What changed

`packet.approve_packet()` requires zero pending checklist items and
pins `content_sha256`; `mark_change_reviewed()` and
`refresh_checklist()` both call `_clear_approval()` whenever the
reviewed content or its check results change. Two regression tests
lock the behavior: re-marking a change after approval reverts to
draft, and a refresh that surfaces a new blocker reverts to draft.

## Where it generalizes

Any governed "approved" state — packets, designs, plans, releases —
should be a function of (content hash × check results), never a flag
set once. If the inputs can change without the flag noticing, the flag
is decoration.

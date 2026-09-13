# Learning — publishing to an evergreen file with parallel teams (2026-09-13)

## What happened

Twelve teams publish proof to one evergreen file
(`docs/proof/analytics/README.md`) on separate branches. During the
Initiative 01 publish, the file changed under the publisher three times in
~20 minutes: another team's version landed between the archive step and the
edit step (silently discarding the first edit), a second team's in-flight
archive files sat untracked in the same checkout, and a sibling agent
committed their Initiative 05 proof onto Initiative 01's branch in the shared
working tree. The publisher recovered by: verifying every edit after
applying it (never assuming the file was unchanged), moving the branch-collided
commit onto its owner's branch ref, resetting the initiative branch to
`origin/main`, and rebuilding the commit in an isolated `git worktree`.

## What we learned

1. Archive-first is not enough when the archive itself races: verify the file
   is byte-identical before and after your edit, or diff it. A silent
   overwrite looks exactly like success.
2. One shared checkout for N parallel publishers is a collision machine.
   Isolated worktrees (one per initiative branch) remove the entire class of
   working-tree fights — including the worst one: a commit landing on the
   wrong branch.
3. Branch-name discipline is load-bearing: `<slug>`-namespaced branches only
   work if every publisher double-checks which branch is checked out before
   committing. The fix for a mis-landed commit is cheap (`branch -f` the
   owner's branch to the commit, reset yours) — but only if you inspect
   `git log` on your branch before pushing.
4. Keep evergreen edits small and additive (one velocity row + refreshed
   counts/date). On rebase conflicts, keep main's version and re-apply —
   redoing a small edit is expected, not a failure.

## What changed

Initiative 01's proof published cleanly from an isolated worktree on
`muse/proof-initiative-01-outcomes-capture-2026-09-13`, based on the latest
`main`, with the Initiative 05 commit re-homed to its owner's branch.

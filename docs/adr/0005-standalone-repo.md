# ADR-0005: Standalone Git Repo

- **Status:** Accepted
- **Date:** 2026-08-26

## Context

`~/adversarial-agents` was initially a subdirectory of a git repo rooted at the
home directory (`~/.git`, created Aug 20, tracking only a stray README, remote
pointing at an unrelated repo). `git status` showed the entire home directory
as untracked — including credentials, `.bash_history`, `.claude/`, `.cursor/`.
Committing from there would have tried to track the whole home directory.

## Decision

Initialize a **standalone git repo** inside `~/adversarial-agents/` (nested
repo — the inner `.git` is authoritative for everything under it). The home
`.git` is left untouched. The standalone repo is pushed to
`github.com/paulthorson/adversarial-agents`.

## Consequences

- **Positive:** The repo is clean and self-contained. No risk of committing
  the home directory. History scrubbed of personal info.
- **Negative:** None significant.

## Alternatives considered

- **Delete the home `.git`** — rejected: not ours to remove, and harmless
  once the inner repo exists.

## References

- `README.md`

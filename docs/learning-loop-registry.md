# Failure-Class Registry

The canonical list of recurring failure patterns. Counts attach to
patterns, never to people. See `docs/learning-loop.md` for the loop and
`docs/templates/failure-class.md` to open a new class.

> The classes below are **illustrative examples** of the format, drawn
> from failure patterns common to governed agent work. They ship with
> zero occurrences. Adopting teams replace them with their own observed
> classes or promote these by tagging real retrospectives.

---

## FC-001: producer-verifies-own-work

- **Title:** Producer verifies own work
- **Description:** The agent or team that built something also performs
  the final verification of it, and defects the builder is blind to pass
  through.
- **Work types:** `build`, `review`
- **First seen:** —
- **Occurrences:** 0
- **Rung:** 1
- **Containment:** Convention: verification must be performed by a party
  that did not produce the work, with independent evidence.
- **Gate ref:** —

---

## FC-002: ship-claimed-without-live-check

- **Title:** Shipped claimed without a live check
- **Description:** Work is reported as live or complete based on a
  successful push or deploy step, without fetching the live surface and
  confirming the new output is actually being served.
- **Work types:** `deploy`, `release`
- **First seen:** —
- **Occurrences:** 0
- **Rung:** 1
- **Containment:** Convention: "pushed" is not "live" — every rollout
  ends with a post-production check against the real URL.
- **Gate ref:** —

---

## FC-003: secret-or-identifier-in-repo

- **Title:** Secret or personal identifier committed to a repository
- **Description:** Credentials, tokens, personal names, contact details,
  or other identifying information end up in committed content —
  code, docs, comments, or history.
- **Work types:** `build`, `docs`, `release`
- **First seen:** —
- **Occurrences:** 0
- **Rung:** 1
- **Containment:** Convention: grep for identifiers and secret keywords
  before every push; machine-checkable — candidate for a scripted gate.
- **Gate ref:** —

---

## FC-004: brief-without-evidence-links

- **Title:** Brief or report without evidence links
- **Description:** A status report, handoff, or decision brief makes
  claims without linking the underlying evidence (files, commits,
  screenshots, logs), forcing the reader to take assertions on trust.
- **Work types:** `briefing`, `review`
- **First seen:** —
- **Occurrences:** 0
- **Rung:** 1
- **Containment:** Convention: every claim a reader will act on carries
  its evidence link.
- **Gate ref:** —

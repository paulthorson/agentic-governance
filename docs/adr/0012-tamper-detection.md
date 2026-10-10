# ADR-0012: Tamper Detection for the Ticket Store and Event Log

- **Status:** Accepted
- **Date:** 2026-10-10
- **Builds on:** ADR-0009, ADR-0010

## Context

The chain is enforced for writes that go through `scripts/chain.py`. An agent
that edits `runs/in_review.json` directly skips all of it. It could mark a
ticket done, clear a veto, or rewrite history in `runs/events.jsonl`.

The constraint that shapes everything below: **code cannot stop a process
from writing a file that its OS user can write.** If agents and the
framework run as the same user, the only in-code option is detection.
Prevention needs OS separation, which an operator sets up and the framework
can check for but not create.

## Decision

**1. Hash-chained event log.** Every event carries `prev_hash`, `hash_alg`,
and `hash`, where `hash = H(prev_hash || canonical_json(event))`. H is
HMAC-SHA256 with the operator's integrity key (`config/integrity.key` or
`AG_INTEGRITY_KEY`), or SHA-256 if no key is configured. Editing, inserting,
deleting, or reordering events breaks the chain. Once a keyed event appears,
an unkeyed one after it is reported as a downgrade. Leading pre-1.2 events
without hashes are allowed.

**2. Signed head record** kept beside the key in `config/`, **not** in
`runs/` (`config/<store>-<hash>.integrity.json`). After each commit it
records:

- the log byte offset
- the hash of the event ending there
- the SHA-256 of the ticket file
- whether agent identity was enforced

It carries a MAC under the key. This catches what a chain alone cannot:
deleting the newest events, and editing the ticket file.

Keeping the head out of `runs/` matters. If it lived beside the files it
protects, anyone who can write `runs/` could delete it, or restore an older
genuinely signed copy together with older ticket and log files. That rolls
state back with no forgery at all. With the head in `config/`, that
rollback needs write access to `config/`.

If a head record is missing while the log anywhere holds committed ticket
state, that is tampering. The whole log is scanned, so a junk last line
cannot make a committed log look fresh. If the head says identity was
enforced and the registry is now missing or empty, that is also tampering.

**3. Commit order:** write temp file, write events stamped with the new
`state_digest`, replace the ticket file, write the head. On every load:

| Ticket file matches | Result |
|---|---|
| Latest committed digest | OK |
| Neither, but the temp file matches the latest digest in the log | Interrupted commit; roll forward |
| Anything else | `TamperDetected` |

Events after the head are re-verified on every load.

**Crash handling.**

- Once the events are written, the commit stands. If the replace keeps
  failing, the caller gets `CommitPending` (CLI exit 5, MCP status
  `pending`), which means do not retry. Windows sharing violations are
  retried first.
- An append cut short by a crash or a full disk leaves a line with no
  newline. The next append moves that fragment to `events.jsonl.torn`.
  Readers never treat an unterminated line as committed.
- A process without the key refuses to extend a keyed log instead of
  appending a downgrade that would halt every honest writer.

**4. On tampering, all writes stop.** Claims, submits, verdicts, and
recovery are refused (CLI exit 4, MCP status `tampered`). A
`store.tamper_detected` event is logged. `recover --alert` sends integrity
problems every run until an operator acts. To resume:

- `ticket.py verify` shows what broke.
- `ticket.py integrity accept --by --reason` (operator approval) re-baselines
  to the current state. It records the problem, who accepted it, and why.
  Historical chain breaks stay visible as "accepted earlier" and never
  disappear. An accepted problem names the line and a digest of its bytes,
  so a later edit to the same line is a new, unaccepted problem.

**5. Keying.** `ticket.py integrity init-key` (operator approval) creates a
0600 key. It runs only after a clean `verify` (or accepted problems) and
applies any pending commit first. Then it re-signs the head. Keyed
installs refuse to load if the key goes missing or the head is unkeyed.

**6. `ticket.py doctor`** reports what is enforced on this install:

- registry present
- key present
- key and registry permissions
- runs/ directory writability
- log and store verification

It always prints that same-user writes cannot be prevented in code.

## Consequences

- **Positive:** a hand edit of the ticket store, or of log events written
  since the last commit, is caught on the next write. The loop stops
  instead of continuing on forged state. An edit to older log events is
  caught by `ticket.py verify`, which `recover --alert` runs every time.
- **Positive:** a crash mid-commit recovers on its own.
- **Negative, unkeyed mode:** anyone who can write the files can recompute
  SHA-256. Unkeyed mode catches accidents and naive edits, not a deliberate
  forger.
- **Negative, keyed mode on one OS user:** agents can read the key file,
  forge, and rewrite the head. The key and the `config/` head help only
  when agents cannot read or write `config/` (`docs/deployment-hardened.md`).
- **Negative, unkeyed mode:** the head in `config/` still blocks rollback by
  someone limited to `runs/`, but anyone who can write `config/` can
  recompute everything.
- **Negative:** `verify` reads the whole log. Loads only read events after
  the last commit.
- **Negative:** the verdict view (`runs/verdicts.jsonl`) is not covered;
  the event log is the record that counts.

## Alternatives considered

- **Append-only file attributes (`chattr +a`):** Linux-only and needs root.
  Documented as an optional hardening step.
- **Store in SQLite with triggers:** same-user processes can still edit the
  database. No gain over a signed head.
- **Ship a daemon running as its own user:** this is the real fix. It
  changes how agents connect, so it stays an operator choice, with a guide.

## References

- [[ADR-0009]] · [[ADR-0010]] · [[ADR-0011]] · `scripts/integrity.py` ·
  `scripts/chain.py` `Store.check_integrity` ·
  `tests/test_identity_integrity.py` · capability report §12.15 ·
  `docs/deployment-hardened.md`

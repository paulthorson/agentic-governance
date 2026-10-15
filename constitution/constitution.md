# Constitution

The constitution is the governing law of the framework. Each domain has its
own at `constitution/domains/<domain>.md`. Every adversary reads its domain's
file before acting, and no agent may edit one.

## What is enforced by code, and what is not

Rule 1 has two code gates: a word-match tripwire on submissions, and a veto
clear that only a human can approve.

- The review tools in the MCP server scan a submission against a fixed list
  of the domain's veto terms and patterns and return `KICK_BACK` on a match
  (`run_review`, `run_review_deep`). The scan matches words, not meaning. A
  submission that does damage without using any listed term or pattern
  passes the scan with `REVIEW_REQUIRED`, and spotting the harm is then the
  adversary's job. The scan is a tripwire, not a detector.
- Clearing a veto on a ticket requires an operator approval that the agent
  runtime cannot supply (`ticket.py clear-veto`, behind `approval.py`). This
  gate holds no matter how the veto was raised.

Rules 2 through 4 are instructions. The adversary applies them in its review,
the verdict is recorded, and the calibration ledger audits the overrides.
Nothing in the code refuses a submission for failing Rule 2, 3, or 4. The
capability report (`docs/capability-report.md`, section 12.8) lists the same
split and is the authority if this page and the report ever disagree.

## The pattern most domains follow

Ten of the twelve domain constitutions share one shape:

1. **A harm veto is absolute.** The domain names the harm it guards against
   (production harm, user harm, unsupported claims, irrecoverable harm, and so
   on). An AI worker can never clear the veto; a named human does, with a
   reason, and the clearing is logged.
2. **Genuine alternatives are mandatory.** A proposal names what it trades
   away. Fewer than two surviving options goes back to the worker.
3. **The fast path can't silently win.** Convenience, scope, engineering ease,
   or whatever the domain's shortcut is may win, but only when it is named
   and chosen on the record.
4. **Claims tie to something checkable.** Either the claim names what would
   falsify it (compliance, docs, ops, privacy, product, universal) or the work
   ties to a stated goal or decision (engineer, QA, researcher, UX).

Two domains depart from the pattern because their subject is a different kind
of risk. **Security** keeps the veto and replaces rules 2 through 4 with
concrete prohibitions: secrets never ship, dependencies are trusted or pinned,
sensitive data is protected. **Prompt** reviews instruction sets rather than
work products: the set must be self-consistent, safety guarantees are not
negotiable, and instructions must name what would violate them.

Each domain file also carries standing constraints that apply to every
review: the reviewer never grades its own work, the record is append-only, no
invented consequences, uncertainty is labeled, and no personal information in
work products.

## Amendment procedure

One procedure, stated in every domain file and repeated here so the two
cannot drift:

- Every human override of a rule is logged in that domain's calibration
  ledger (`adversarial-<domain>/references/calibration-ledger.md`).
- Three overrides of one rule puts the rule on trial.
- Only a human edits a constitution file. The edit is reviewed by the
  domain's adversary before it merges, like any other change to this
  repository.

## Per-domain constitutions

The MCP `get_constitution(domain)` tool returns the live text of
`constitution/domains/<domain>.md`.

## See also

- [[Architecture]] · [[Vetoes]] · [[Calibration]] · [[Domains]]

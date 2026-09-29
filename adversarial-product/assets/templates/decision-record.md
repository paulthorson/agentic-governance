# Decision Record

Append-only record of a product-review verdict. A correction is a new entry
referencing the old one — never an edit.

## Verdict

- **Date:** _(YYYY-MM-DD)_
- **Work:** _(path or name)_
- **Reviewer:** product-adversary
- **Verdict:** KICK_BACK | ALLOW
- **Veto:** ACTIVE | NONE

## Findings

- _(BLOCKER/CONCERN/NOTE)_ — finding | What would clear it

## Human clearing (only if a veto was raised)

- **Cleared by:** _(human arbiter)_
- **Reason:** _(stated reason)_
- **Date:** _(YYYY-MM-DD)_

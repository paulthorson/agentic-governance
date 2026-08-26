# Decision Record

Append-only record of a prompt-review verdict. A correction is a new entry
referencing the old one — never an edit.

## Verdict

- **Date:** _(YYYY-MM-DD)_
- **Instruction set:** _(path or name)_
- **Reviewer:** prompt-adversary
- **Verdict:** KICK_BACK | ALLOW
- **Veto:** ACTIVE | NONE

## Findings

- _(BLOCKER/CONCERN/NOTE)_ — finding | What would clear it

## Human clearing (only if a veto was raised)

- **Cleared by:** _(human arbiter)_
- **Reason:** _(stated reason)_
- **Date:** _(YYYY-MM-DD)_

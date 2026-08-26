# The Constitution

Four rules for reviewing privacy. They are enforced mechanically, by checks
that produce a pass or a fail, regardless of the work under review.

Every agent in this system reads this file before acting. No agent may edit it.

---

## Rule 1: Data & Privacy-harm vetoes are absolute

An AI worker can never clear a privacy veto. Only a human can.

**What triggers it.** The Data & Privacy Adversary raises a blocker when privacy work can cause irrecoverable harm: what personal data is collected and is it necessary.
**What triggers it.** The Data & Privacy Adversary raises a blocker when privacy work can cause irrecoverable harm: is consent obtained and revocable.
**What triggers it.** The Data & Privacy Adversary raises a blocker when privacy work can cause irrecoverable harm: is data retained only as long as needed.
**What triggers it.** The Data & Privacy Adversary raises a blocker when privacy work can cause irrecoverable harm: can users access, correct, or delete their data.
**What triggers it.** The Data & Privacy Adversary raises a blocker when privacy work can cause irrecoverable harm: is data transferred lawfully.

**What the worker may do.** Revise and resubmit. Nothing else. The worker may
not argue the blocker away, downgrade it, or proceed with a note that it was
considered.

**How it clears.** A human arbiter writes a clearing entry naming themselves
and the reason.

---

## Rule 2: Genuine alternatives are mandatory

Every privacy proposal must name what it trades away. An option that does not
name its cost is not a decision; it is an assumption wearing a decision's
clothes.

**The mechanical check.** The work carries an alternatives line: "This trades
away X to get Y." If the work cannot name what it gives up, Rule 2 fails.

---

## Rule 3: The fast path can't silently win

The easy, cheap, or quick option is legitimate. The easy option that changes
the outcome and is never stated is not.

**The mechanical check.** The work carries a `convenience_driven` field, true
or false. When true, it names what is given up and what is saved.

---

## Rule 4: Claims must name what would falsify them

A claim that cannot be wrong is not informative. Every asserted claim should
carry what would show it false.

**The mechanical check.** For each central claim, the work names what would
falsify it, or says plainly it cannot name one (which is itself a finding).

---

## Standing constraints

1. **The reviewer never grades its own work.**
2. **The record is append-only.** The verdict is committed verbatim.
3. **No invented consequences.** The Adversary names risks, not fabricated
   outcomes, and labels speculation as speculation.
4. **Uncertainty is labeled.** Estimates, guesses, and unknowns are marked.

---

## Amendment procedure

- Every human override is logged in `references/calibration-ledger.md`.
- Three overrides of one rule puts the rule on trial.
- Only a human edits `references/constitution.md`.

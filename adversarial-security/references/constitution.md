# The Constitution

Four rules for reviewing security. They are enforced mechanically, by checks
that produce a pass or a fail, regardless of the change under review.

Every agent in this system reads this file before acting. No agent may edit it.

---

## Rule 1: Security-harm vetoes are absolute

An AI worker can never clear a security veto. Only a human can.

**What triggers it.** The Security Adversary raises a blocker when a change
can cause irrecoverable security harm: an exploitable vulnerability, an
exposed or committed secret, a dependency with a known critical CVE or from
an untrusted source, or sensitive data exposed or mishandled.

**What the worker may do.** Revise and resubmit. Nothing else. The worker may
not argue the blocker away, downgrade it, or proceed with a note that it was
considered.

**How it clears.** A human arbiter writes a clearing entry naming themselves
and the reason.

---

## Rule 2: Secrets never ship

No credential, key, token, or password may appear in code, config, logs, or
git history. A secret that ships is a veto.

**The mechanical check.** The change is scanned for secrets in code, config,
logs, and history. A hit fails Rule 2.

---

## Rule 3: Dependencies are trusted or pinned

Every dependency must be from a trusted source and pinned to a known-good
version. A floating version or an untrusted source is a finding.

**The mechanical check.** The dependency list is checked for source and
version pinning. A known critical CVE fails Rule 3.

---

## Rule 4: Sensitive data is protected

Sensitive data (PII, credentials, financial) must be encrypted at rest and in
transit, and retained only as long as needed.

**The mechanical check.** The change is checked for unencrypted sensitive
data, over-retention, and insecure transit. A failure is a finding.

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

# Validation Record — Real Epic Through the Governance Chain

**Epic:** "Add a `--output` flag to the calibration-report script so operators can write the report to a file instead of only stdout."
**Date:** 2026-09-06. **Chain:** CEO → Research → PM → UX → Engineer → QA.
**Method:** Each role loaded the constitution + its harness + only the single upstream artifact, and produced its required artifact. Work done in `/tmp/ba-test-run/`; the governance repo (`~/adversarial-agents`) was **not modified** (read-only to bots). The engineer produced a diff (not applied); QA applied the diff to a copy in `/tmp` and ran real tests.

**Context:** This is the real-write-path counterpart to the prior A11 false-premise epic (`--dry-run`). Unlike A11, this epic's premise is genuine — the script has no write path today, so adding one is a real change.

---

## What each role produced

| Role | Input (only) | Artifact | Location |
|---|---|---|---|
| **CEO** | Objective | Research question (restated objective as problem per A18.3, with stopping condition) | `epic/ceo-research-question.md` |
| **Research** | Research question | `evidence.md` (5 required sections + acceptance record) | `epic/evidence.md` |
| **PM** | evidence.md | `brief.md` (5 required fields, 2 genuinely different approaches) | `epic/brief.md` |
| **UX** | brief.md | `stories.md` (standard template) + `rationale.md` | `epic/stories/` |
| **Engineer** | stories | `implementation.diff` + `notes.md` (3 sections) | `epic/implementation/` |
| **QA** | story + notes | `test-plan.md` + `results.md` (1:1 vs ACs) | `epic/qa/` |
| **CEO (accept)** | QA report | Acceptance decision (A18.1) | `epic/ceo-acceptance.md` |

---

## Did the chain complete or stall/escalate?

**The chain completed all six roles and produced a genuine QA verdict — but it did NOT reach clean acceptance.** QA found **two real defects** and the CEO routed a rework loop back to the engineer. This is the framework working as designed: it caught real defects in a real implementation rather than rubber-stamping.

- **No stall** — no infinite bounce between roles, no loop-kill needed.
- **No escalation to the human** — the defects are ordinary implementation defects (not a customer-harm veto, not legal/compliance/privacy, not a novel no-precedent case). The CEO routed rework, which is within its authority.
- **The chain is currently in a rework loop** (engineer → QA), which is the correct state given the defects found.

---

## What broke — the findings (this is the point)

### F1. The engineer's diff was not a cleanly-appliable patch (REAL defect in the deliverable)
The `implementation.diff` had **incorrect hunk-header line counts on both hunks**:
- Hunk 1: `@@ -1,13 +1,14 @@` but the content is 13 original / 18 new (5 added lines). Should be `+1,18`.
- Hunk 2: `@@ -78,6 +79,7 @@` but the content spans ~20+ original lines. The header undercounts badly.

`patch` rejected the diff as malformed. QA had to reconstruct the patched file by hand to test the intended implementation. **A governance framework whose engineer role produces non-applicable diffs is a real gap** — the diff is the engineer's primary deliverable, and it must be machine-applicable to be reviewable/testable. This is the single most important finding.

### F2. QA found a real functional defect: file output missing trailing newline (D1)
`emit()` uses `Path.write_text(text)`, which writes exactly the joined string with **no trailing newline**, whereas `print()` appends one. Result: `--output report.txt` is **not byte-identical to stdout** (AC1 FAIL), and `--json --output report.json` has the same trailing-newline difference (AC2 caveat). The story's AC1 requires the file content to match stdout. **Real defect, caught by QA.**

### F3. QA confirmed the engineer's flagged gap: no atomic-write guarantee (D2)
`Path.write_text` opens with `'w'`, which **truncates the target before writing**. A mid-write failure (disk full, quota) leaves a truncated/partial file. The story's AC5 requires "no partial/corrupt file left behind." The engineer **honestly flagged** this in `notes.md` rather than claiming compliance; QA confirmed it is a real, unaddressed defect. **The flag-and-verify loop worked** — the engineer's honesty was validated, not hidden.

### F4. The subagent-isolation constraint (methodological finding)
The task instructed spawning **isolated subagents** per role. I am at subagent depth 1/1 and **cannot spawn further subagents**, so I ran each role myself with strict context isolation (harness + constitution + single upstream artifact only). This preserved the *information* isolation (each role saw only its upstream artifact) but not *reasoning* isolation (one model produced all artifacts). The prior A11 record used true isolated subagents. **This is a limitation of the test harness, not the governance framework** — but it means the "no shared reasoning" guarantee was weaker than intended. A real deployment must spawn true isolated subagents.

### F5. Minor: trailing-slash path edge case
`--output target.txt/` (trailing slash) silently wrote to `target.txt` (the slash was normalized). Not a defect per the story, but an unhandled edge case worth noting.

### F6. Minor: `--output -` (stdout sentinel) not handled
The engineer flagged this as ambiguous in the design; the story did not authorize a `-` sentinel. `--output -` would create a file literally named `-`. Not a defect, but a design gap the story left open.

---

## What worked (the framework's strengths, confirmed in a real run)

- **A18.3 (CEO restates solution as problem):** The CEO restated the solution-framed objective ("add a `--output` flag") as a problem ("operators need a durable, discoverable way to persist the report"), unprompted. Verified again in a full chain.
- **Research is a real check:** The researcher read the actual script and established the no-write-path baseline, named the gap (operator need unproven; shell redirection may suffice), and did **not** recommend a course of action (respecting its harness prohibition).
- **PM produced two genuinely different approaches:** Approach A (code change) vs Approach B (documentation change) — mechanically distinguishable, not variations of the same idea.
- **UX recorded its rationale in writing:** `rationale.md` explicitly states it chose Approach A *not* because it is easier to build (it is harder) but because it solves the problem — the engineering-ease rule's "fingerprints" mechanism worked.
- **Engineer flagged rather than hid:** The engineer surfaced the AC5 partial-write gap in `notes.md` instead of silently claiming compliance.
- **QA verified against the story, not the implementation:** QA tested the story's ACs (not the engineer's claims), found D1 and D2, and reported **up to the CEO** (not back to the engineer), per the routing rule.
- **The chain did not stall:** It reached a clean, correct state (rework loop) with real defects surfaced.

---

## Final recommendation

1. **Fix the engineer harness / diff requirement (highest priority).** The engineer's diff must be machine-applicable (correct hunk headers, verifiable with `patch --dry-run` or `git apply --check`). Add this as a mechanical check. This is the biggest breakage found.
2. **Fix the two implementation defects** (D1: add trailing newline to file output; D2: write to temp file + atomic rename, or otherwise guarantee no partial file) and re-run QA.
3. **Address the design gaps** the engineer flagged: define `--output -` semantics and trailing-slash handling, or explicitly reject them.
4. **For future test runs:** use true isolated subagents (the depth-1/1 constraint here weakened the "no shared reasoning" guarantee). The framework itself is sound; the isolation was a test-harness limitation.
5. **The epic itself is valid and worth completing.** Unlike the A11 false-premise epic, this one has a genuine write path and a real operator need (durable, discoverable report persistence). It should proceed through the rework loop to acceptance.

**Bottom line:** The governance chain **works end to end on a real epic** — it caught two genuine defects in a real implementation, routed rework correctly, and never stalled or fabricated work. The one structural breakage is the engineer role's non-applicable diff, which should be fixed in the harness.

---

## Follow-up (2026-09-06, later): D1 and D2 fixed

The two implementation defects found by QA were fixed in `scripts/calibration-report.py`:

- **D1 (missing trailing newline):** the report is now built as a string with a
  trailing newline and emitted via a single `emit()` helper; file output is
  byte-identical to stdout (verified with `diff`).
- **D2 (no atomic-write guarantee):** the file is written to a temp file in the
  target directory then atomically renamed (`os.replace`), so a mid-write
  failure never leaves a partial file. Missing-directory and unwritable-path
  errors give a clear message and non-zero exit. Verified: no temp files left
  behind, JSON output valid.

The `--output` flag is now implemented with both defects resolved. The epic is
ready to re-run through QA to acceptance.

# Workstream 3 — Process records and rule status

**Status:** proposed. Nothing here is implemented or in force. Any registry or schema named below is a **decision option** (D2), not a decision. The records that exist today (`docs/CoE.md`, the files under `harnesses/`, `ledger/calibration-ledger.md`, `constitution/`) remain the authoritative record until a recorded decision changes that. 
**Audience:** agent (seats that execute). 
**Reviewed at:** `main @ a0a79ef`. 
**Owners:** Chief of Staff owns rule status and any status change; only a recorded acceptance changes a status. Engineer owns checks, fixtures, and templates. Quality owns the seeded-defect matrix and records results. Adversary challenges every status change and every check and may not stamp. 
**Layers:** the requirements below are layer A once reviewed by the owning roles; decision D2 is layer A. All stories are layer B and open only after the operator accepts the Workstream 0 requirements. 
**Depends on:** nothing. **Enables:** Workstream 2 (path and link checks), Workstream 4 (status vocabulary).

## Rule

A process claim is either backed by a check that fails on a seeded defect, or it is written as advisory. A rule has exactly one recorded status wherever it is cited. Records that are meant to be append-only are protected by a check, not by convention.

## Problem (verifiable at `a0a79ef`)

**Status is inconsistent between places, and this plan does not say which place is right.**
- `docs/CoE.md`: the row for `OPERATOR_FACING_GIT_PLAIN_ENGLISH` records its status as **draft**, pending acceptance. A sibling row on the same page refers to the same rule as in force and cites a merge. The rule's recorded status in its own row is draft; the sibling reference is the inconsistency. Resolving it is a Chief of Staff decision, not something this plan decides.
- `AI_SLOP_COPY_FAIL`: `docs/CoE.md` lists it in the table of accepted rules with a merge reference; `harnesses/chief-of-staff.md` describes it as draft pending acceptance. The two pages disagree.
- The same rule text is restated across `docs/CoE.md`, `harnesses/chief-of-staff.md`, `harnesses/ux.md`, `harnesses/qa.md`, and `harnesses/engineer.md`, and the copies differ in wording and detail.
- Merge references cited next to a status are prose; no check confirms that a cited commit exists on `main`.
- `docs/improve/2026-09-20.md` already lists status drift between `docs/CoE.md` and the role files as open work.

**CI steps that cannot fail.**
- `.github/workflows/validate.yml` contains a step named for frontmatter and link integrity whose install command swallows its own failure and whose inline script never exits non-zero.
- `CONTRIBUTING.md` rule 7 states that documentation must not claim enforcement that code does not perform. The step's name makes such a claim.

**Records protected by convention only.**
- `AGENTS.md` rule 3 states that decision records are append-only. No check rejects an edit to an existing entry in `ledger/calibration-ledger.md`.
- `.gitignore` re-includes a key-file pattern under plugin agent folders with no recorded reason; the related test checks only that the exclusion pattern is present.

**Intake and queue have no documented shape.**
- `.github/` contains only `workflows/`; there is no issue or pull-request template. `harnesses/chief-of-staff.md` describes improvement intake as a label plus a standing issue and requires same-day anonymization, but no checklist artifact exists for the person filing.
- `ledger/queue.md` describes the decision-ready shape for items that reach a human and contains no example entry.

## Requirements

1. Every governance rule identifier cited on a public page has exactly one recorded status, and every citation agrees with it. Where the record lives is decision D2; until decided, the existing pages are the record.
2. A status changes only by a recorded acceptance from the Chief of Staff, with the Adversary's challenge recorded. No check, script, or migration changes a status.
3. Every status that cites a commit cites one that exists on `main`.
4. Every CI step has a seeded-defect fixture on which it fails and a clean fixture on which it passes. A step without such a fixture is removed, and any documentation that named it is corrected.
5. Every check runs from one program that a contributor can run locally; no check logic lives inline in a workflow file.
6. Append-only records are protected: a change that modifies or removes an existing entry fails a check. Corrections are new entries that cite the entry they correct.
7. Every rule identifier used in a record resolves to a recorded rule.
8. Improvement intake has a template with an anonymization checklist the filer completes. Until Workstream 0 establishes a content check, the checklist is self-attested and the Chief of Staff's promotion step re-reads it.
9. The human decision queue has one placeholder example in the documented shape, and new entries are checked against that shape.
10. Negations of secret-file patterns in `.gitignore` carry a recorded reason or are removed.

## Stories

### 3.S1 — Rule status consistency (decision D2 open)

**Deliverable.** A consistency check across the pages that record rule status; a list of every current disagreement for the Chief of Staff to resolve one by one; and, only if D2 selects option (a), a registry file with a schema. Any migration copies statuses as recorded and marks disagreements as `conflict`; it changes nothing. 
**Acceptance criteria.**
- [ ] A check extracts every rule identifier and status from the recording pages and fails when one identifier has more than one status; it passes on a fixture with agreeing pages and fails on a fixture with a disagreement.
- [ ] A check fails when a status cites a commit that is not an ancestor of `main`.
- [ ] Every disagreement present at `a0a79ef` is listed in the pull request; each is resolved by a separate recorded acceptance from the Chief of Staff with the Adversary's challenge recorded; none is resolved by a script.
- [ ] If D2 selects option (a): the schema names status values, sensor kind (`code` or `process`), the paths where the rule is recorded, and the acceptance reference; the initial file is generated from the existing pages and diffed against them; it contains no status that differs from the pages except entries marked `conflict`.
- [ ] Documentation that describes a rule as fail-closed also states whether its sensor is code or process, consistent with `docs/capability-report.md`.
**Risks / exclusions / rollback.** Risk: the check reads a cross-reference as a status claim — mitigation: the check distinguishes a rule's own row from mentions of it elsewhere and reports the two separately. Exclusion: this story never changes a status. Rollback: remove the check; the pages are as they were; if a registry was created, delete it — the pages remain the record. 
**Done / miss.** Done when the consistency check passes on `main` and every disagreement has a recorded resolution. Miss when a status changes without a recorded acceptance. Quality detects; Engineer may not stamp; Chief of Staff may not stamp its own acceptance.

### 3.S2 — CI proof harness

**Deliverable.** A fixtures directory with one seeded-defect fixture and one clean fixture per CI step; a self-test that runs every step against its fixtures; removal of any step that cannot fail; correction of the tooling page to list the steps that exist. 
**Acceptance criteria.**
- [ ] For every step in the validation workflow, the self-test runs the step's program on its seeded-defect fixture and asserts a non-zero exit, and on its clean fixture and asserts zero.
- [ ] The step named for frontmatter and link integrity is removed or replaced by a program that fails on its fixture.
- [ ] The workflow file contains no command that swallows its own failure and no inline script.
- [ ] `docs/Tooling.md` lists exactly the jobs and steps in the workflow (test compares names).
- [ ] The self-test runs in CI on every change to the workflow file or the fixtures.
- [ ] `.gitignore` negations of secret-file patterns carry a reason comment; a test fails on a negation without one.
**Risks / exclusions / rollback.** Risk: a fixture is written to pass trivially — mitigation: the Adversary reviews each fixture pair against the step's stated purpose. Exclusion: the secrets scan is not replaced. Rollback: revert; existing steps keep running as before. 
**Done / miss.** Done when every step fails on its fixture and passes clean. Miss when a step exists without a fixture. Quality detects; Engineer may not stamp.

### 3.S3 — Append-only records

**Deliverable.** An entry template for the calibration ledger; a helper that appends a formatted entry; a check that rejects edits to existing entries. 
**Acceptance criteria.**
- [ ] A template defines the entry shape (date, identifier or title, case, finding, decision, citation).
- [ ] A pull request that modifies or removes text inside an existing ledger entry fails the check; a pull request that only appends passes (both as fixtures).
- [ ] The append helper refuses an entry with an empty field and refuses a rule identifier that does not resolve to a recorded rule.
- [ ] A correction is a new entry that cites the entry it corrects; the check does not accept an in-place edit labelled as a correction.
**Risks / exclusions / rollback.** Risk: the check blocks whitespace or formatting repairs — mitigation: the check normalises whitespace before comparing. Exclusion: files other than the ledger and decision records. Rollback: disable the check job; entries are unaffected. 
**Done / miss.** Done when both fixtures behave as specified in CI. Miss when an existing entry changes in place. Quality detects; Engineer may not stamp.

### 3.S4 — Improvement intake with anonymization checklist

**Deliverable.** An issue template for improvement intake and a pull-request template; both open with a bottom line a stranger can decide from. 
**Acceptance criteria.**
- [ ] The issue template has these fields: bottom line (one sentence); what happened (facts only); what should be true instead; evidence as repository paths or commands; an anonymization checklist the filer completes (no personal names, no contact details, no private product names or paths, no credentials); the filing role.
- [ ] The template applies the intake label; the label, not a specific issue, is the intake container. Retiring any existing container issue is a recorded Chief of Staff decision taken after the template is in use.
- [ ] The pull-request template has a bottom-line section first, a list of changed paths with their declared audience, and a place for any exception approvals; a check fails a pull request whose bottom-line section is empty.
- [ ] `docs/improve/README.md` has a human-facing "How to file" section that explains intake and promotion in plain words and links the glossary.
- [ ] The checklist is self-attested until Workstream 0 establishes a content check; the template states that dependency.
**Risks / exclusions / rollback.** Risk: filers tick the checklist without reading — mitigation: the Chief of Staff's promotion step re-reads the body and returns the item if the checklist is untrue. Exclusion: no in-product feedback collector. Rollback: remove the templates; the label continues to work. 
**Done / miss.** Done when both templates exist and the bottom-line check fails on an empty fixture. Miss when intake can be filed without the checklist. Quality detects; Product Manager may not stamp.

### 3.S5 — Decision-ready human queue

**Deliverable.** One placeholder example in `ledger/queue.md` in the shape the file already documents; a shape check for new entries. 
**Acceptance criteria.**
- [ ] `ledger/queue.md` contains one example with all five parts the file names: a one-line question, labelled answer options, a free-response option, what is blocked, and why it reached the queue; all names are placeholders.
- [ ] A check fails on a fixture entry missing any of the five parts and passes on the example.
- [ ] The example contains no real project, team, or person name.
**Risks / exclusions / rollback.** Risk: the example is mistaken for a live item — mitigation: it is labelled as an example in its heading. Exclusion: no change to how items reach the queue. Rollback: remove the example and check. 
**Done / miss.** Done when the example and the check are in place. Miss when a real entry lands without the five parts. Quality detects; Chief of Staff may not stamp.

## Fail conditions (rejected outright)

- A status changed by a script, a migration, or any seat other than the Chief of Staff with a recorded acceptance.
- A registry or schema described as the record before decision D2 is taken.
- A CI step without a seeded-defect fixture.
- A workflow command that swallows its own failure.
- An in-place edit to an append-only record.
- Intake filed without the anonymization checklist.

## Falsification (Adversary)

| Claim | Procedure | Expected |
|---|---|---|
| One status per rule | Write a second, different status for a rule on any recording page; run the check | Fails, naming the identifier and both statuses |
| Cross-references are not statuses | Mention an accepted rule from another rule's row; run the check | Reported as a cross-reference, not as a second status |
| Commits are real | Cite a commit that is not on `main` next to a status | Fails |
| Nothing changed silently | Read the change history of the recording pages for status changes | Every change has a recorded acceptance |
| Every step bites | Run the self-test | Every step fails on its fixture and passes clean |
| Append-only holds | Open a pull request editing an existing ledger entry | Check fails, naming the entry |
| Intake is shaped | File an intake with the checklist incomplete | Template rejects submission |
| Queue is shaped | Add a queue entry missing one part | Check fails |

# Workstream 0 — Public-page content check — CANDIDATE

**Status: CANDIDATE — operator Look FAIL on PRD v2.1; failure reasons are unnamed and must not be inferred.**

This workstream has no accepted name or identifier. It is referred to here only as the public-page content check. Nothing in this file is decided: the surfaces a check would cover, the classes of content, the mechanism, how exceptions are handled, the sequencing, and the approval model are all open until the operator records a decision. This file describes how to reach that decision (layer A) and how to prove whatever is decided (layer B).

**Audience:** agent (seats that execute). 
**Reviewed at:** `main @ a0a79ef`. 
**Owners:** Operator decides requirements. Chief of Staff prepares the requirements draft and carries the operator's decision into the record. Engineer builds the proof only from recorded requirements. Quality runs fixtures and records results. Adversary challenges at each step and may not stamp. 
**Layers:** story 0.S1 is layer A (requirements and decision; closes without build). Stories 0.S2 and 0.S3 are layer B and open only after the operator's decision line reads `accepted`. 
**Depends on:** nothing. **Enables:** layer B of every other workstream.

## Rule

No public-page content check is built, enabled, or described as in force until the operator has recorded a decision on its requirements. A check built from inferred requirements is rejected.

## Problem (verifiable at `a0a79ef`)

1. CI runs a structure validator, a harness single-source check, the test suite, an MCP smoke test, and a secrets scan (`.github/workflows/validate.yml`). No step evaluates the content of public pages against any content rule.
2. The rules that exist for public-page content are recorded as process, not code: the `COUNSEL_GATE` entry in `ledger/calibration-ledger.md` records a decision and nothing checks it; the release-compliance checklist in `harnesses/chief-of-staff.md` states that it is a checklist and not a merge gate; the visitor-face and vanilla rules in `harnesses/qa.md` name Quality judgment as the sensor.
3. `docs/capability-report.md` sections 12.7–12.8 distinguish code controls from instruction controls. Every control over public-page content is on the instruction side.
4. A prior requirements document for this check (PRD v2.1) did not pass operator review. The reasons are not recorded in this repository. **They are unknown to this plan and must not be reconstructed from the repository, from its history, or from any other source.**

## What this workstream does not decide

These are questions for the requirements decision (story 0.S1). Listing them is not an answer to any of them.

- Which paths count as public-facing.
- Which classes of content are out of bounds, and whether that list is fixed or extensible.
- Whether the check blocks a merge or only reports.
- How an exception is requested, who may approve one, and whether any class of exception is reserved to the operator.
- Whether the check runs only in CI, also locally, or both.
- Who owns the check after it exists, and how its requirements change.
- Whether the check may print the content it matched, or only the location and rule.
- What the check, and this workstream, are called.

## Requirements

1. The requirements are written as a new draft. The draft carries nothing forward from PRD v2.1 by assumption; anything reused is reused because the operator says so in the decision line.
2. Each requirement in the draft has an identifier and a statement that a fixture can test.
3. The operator's decision is recorded by the operator, in the operator's words, in the requirements document or in the pull request that carries it. Agents do not write, paraphrase, or infer that line.
4. (Layer B) A proof exists for every accepted requirement: at least one seeded-defect fixture that must fail and one clean fixture that must pass.
5. (Layer B) The check runs from one code path wherever it runs. Check logic copied inline into a workflow file is rejected.
6. (Layer B) The check is introduced in report-only mode first. The result of the report-only run on `main` is recorded as reported; it is a measurement, not a target. The operator decides when and whether the check becomes blocking.
7. (Layer B) Making the check required is a repository setting the operator changes; it is recorded as done in the pull request, not assumed.

## Stories

### 0.S1 — Requirements decision (layer A)

**Problem.** There is no accepted requirements record for the check. The earlier version was not accepted and its reasons are unrecorded. 
**Deliverable.** A requirements draft at a location named in the pull request, containing: purpose; the open questions above, each with the operator's answer once given; numbered testable requirements; the operator's decision line. 
**Acceptance criteria.**
- [ ] The draft exists at the location named in the pull request and is linked from this file.
- [ ] Every open question above has an answer field; a question without an answer is marked `undecided`, never filled in by an agent.
- [ ] Every requirement has an identifier and a testable statement.
- [ ] The document contains an operator decision line (`accepted`, `returned`, or `rejected`) written by the operator; no agent-written text is placed in that line.
- [ ] The document contains no statement about why PRD v2.1 did not pass.
**Risks / exclusions / rollback.** Risk: an agent drafts or paraphrases the decision line — check: the line's author is recorded as the operator in the pull request. Exclusion: no check code, fixtures, or CI changes in this story. Rollback: withdraw the draft; nothing else changes. 
**Done / miss.** Done when the decision line reads `accepted`. Miss when any requirement is treated as decided without that line. Quality detects; Chief of Staff and Engineer may not stamp.

### 0.S2 — Proof design from decided requirements (layer B)

**Problem.** A check without seeded defects cannot show that it works; a check built before requirements are accepted encodes guesses. 
**Deliverable.** For each accepted requirement: a seeded-defect fixture, a clean fixture, and a check that runs the same way locally and in CI. Whether the check may print matched content follows the operator's answer to that open question. 
**Acceptance criteria.**
- [ ] Story 0.S1 is done before any check code is written; the pull request that adds the check links the accepted requirements document.
- [ ] For every accepted requirement identifier there is at least one seeded-defect fixture; running the check on it exits non-zero and names the requirement identifier.
- [ ] Running the check on the clean fixture exits zero with no findings.
- [ ] The CI workflow calls the same program a contributor runs locally; no check logic lives inline in the workflow file.
- [ ] The check's output on seeded fixtures conforms to the operator's decision about printing matched content.
- [ ] If an exception mechanism was accepted, it has its own seeded fixture: an exception that violates the accepted approval rule makes the check fail.
**Risks / exclusions / rollback.** Risk: fixtures themselves carry out-of-bounds content — check: fixtures use placeholder text and pass whatever content rule the operator accepted for fixture files. Exclusion: the check is not made required in this story. Rollback: remove the check and fixtures; no page content depends on them. 
**Done / miss.** Done when all fixtures behave as specified in CI. Miss when a requirement has no fixture, or a fixture passes when it should fail. Quality detects; Engineer may not stamp.

### 0.S3 — Controlled rollout (layer B)

**Problem.** A new blocking check applied to an existing tree either blocks all work or forces exceptions written in haste. 
**Deliverable.** A report-only run on `main`, a recorded measurement, and a recorded operator decision before blocking mode. 
**Acceptance criteria.**
- [ ] The check runs in report-only mode on `main` and on pull requests; its findings are recorded in the pull request as reported, without editing the numbers.
- [ ] Findings on `main` are resolved by editing the flagged content or by an accepted exception under the accepted approval rule; no requirement is weakened to make findings disappear.
- [ ] The operator records a second decision line before the check is made blocking.
- [ ] The repository setting that makes the check required is recorded as done in the pull request by the person who changed it.
- [ ] After blocking mode, a pull request that reintroduces any seeded defect cannot be merged.
**Risks / exclusions / rollback.** Risk: blocking mode stalls unrelated work — mitigation: report-only period first, with the measured findings visible before the operator decides. Exclusion: this story never edits a requirement. Rollback: the operator returns the check to report-only by reversing the repository setting; the check and fixtures remain. 
**Done / miss.** Done when blocking mode is on and a seeded-defect pull request is refused. Miss when blocking is enabled without the operator's decision line, or when a finding is closed by changing a requirement. Quality detects; Chief of Staff may not stamp the operator's decision.

## Fail conditions (rejected outright)

- A check built from requirements the operator has not accepted.
- Any text, in any file, that states or implies why PRD v2.1 did not pass.
- A name, identifier, category, mechanism, allowlist, or approval rule presented as decided before the decision line exists.
- Check logic copied inline into a workflow file.
- A requirement changed to make an existing finding disappear.
- Blocking mode enabled without a recorded operator decision.

## Falsification (Adversary)

| Claim | Procedure | Expected |
|---|---|---|
| Nothing is decided here | Read this file for any name, category, allowlist, or mechanism stated as fact | None found |
| Requirements precede code | Compare the merge order of the requirements document and the check | Requirements accepted first |
| Seeded defects fail | Run the check on each seeded fixture | Non-zero exit; requirement identifier named |
| Clean passes | Run the check on the clean fixture | Zero exit; no findings |
| One code path | Search the workflow file for inline check logic | None |
| Rollout was controlled | Read the pull request for the report-only measurement and the operator's decision lines | Present, in order |
| v2.1 reasons not inferred | Search this workstream's files and pull request for any stated reason | None |

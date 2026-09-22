# Workstream 4 — Localhost framework dashboard UX

**Status:** proposed. Plan only: no implementation, no visual design, no schema in this pull request. 
**Audience:** agent (seats that execute). 
**Reviewed at:** `main @ a0a79ef`. 
**Owners:** Product Manager owns the purpose statement and human copy. User Experience owns the state contracts, the information architecture, the accessibility configuration, and the stills review. Engineer owns the fixtures mode, the feed filter, the clean build, and the CI jobs. Quality owns the screen-by-state matrix and records results. Chief of Staff decides the design reference (decision D6). Adversary challenges and may not stamp. 
**Layers:** the requirements below are layer A once reviewed by the owning roles; decisions D5 and D6 are layer A. All stories are layer B and open only after the operator accepts the Workstream 0 requirements. 
**Depends on:** Workstream 2 (report feed, decision D5) and Workstream 3 (status vocabulary). **Enables:** nothing downstream.

## Scope boundary

This workstream covers only the optional local dashboard under `dashboard/`, which runs on the operator's machine. The public marketing site, its visual "instrument" feature, and its typography readiness work live in another repository and are **not** touched, referenced as a design source, or gated by anything here.

## Rule

The dashboard shows only what a local file says, says where it came from, and says so plainly when the file is missing, empty, unmeasured, or unreadable. It never writes to the framework's records and never runs anywhere but the operator's machine. Its visual states are proven with stills captured from the running local application at the tip under review; mock frames and design-file exports are not proof.

## Problem (verifiable at `a0a79ef`)

1. `dashboard/README.md` opens with working notes (holds and issue references) before saying what the application is for. The repository README states the dashboard is not required to use the framework; the dashboard's own page does not lead with that.
2. `dashboard/docs/ux/look.md`, `dashboard/docs/ux/design-system.md`, and related notes describe a design direction for a public marketing surface, while `dashboard/README.md` states that the public face lives in a different repository. The local application has no design reference of its own.
3. `dashboard/scripts/sync-improve.mjs` copies every markdown file at the top level of `docs/improve/` into the application's content, including the folder's README, the template, and the operations changelog.
4. No screen states what it shows when its source file is missing, empty, unmeasured, or unreadable. The report parser recognises some non-numeric labels as unmeasured; the vocabulary `docs/improve/README.md` requires for unmeasured values is not covered by a test.
5. `.github/workflows/validate.yml` has no job that builds the dashboard, and no accessibility check runs anywhere in CI.
6. `dashboard/src/middleware.ts` and `dashboard/src/lib/admin-access.ts` restrict administrative screens to local hosts, with a unit test; there is no request-level test of that boundary.
7. `dashboard/package.json` declares several dependencies with version ranges rather than exact pins.
8. `dashboard/docs/ux/README.md` links a folder that does not exist.

## Requirements

1. The dashboard's first page states its purpose, that it is optional, that it runs only on the operator's machine, and that it reads local files and writes none of the framework's records.
2. Every screen has a state contract with four states — empty, not measured, measured, error — each with the copy it shows and the source it names. A value is never shown without its source.
3. A fixtures mode renders every screen in every state deterministically from placeholder data, for tests and for review.
4. Each declared state is proven by a still captured from the running local application at the tip under review. The capture method is recorded on the installer's product brief, not in this repository; no capture tool is named here.
5. The dashboard reads only the human-facing part of the improve record, as decided in D5. Templates, folder READMEs, operations changelogs, and agent logs never enter its content.
6. An automated accessibility check runs in CI over every screen in every state, and the build fails on any finding the check reports. Which rules the check enforces is configured in the repository by the User Experience owner; this plan does not set a severity floor. Keyboard operation and a reduced-motion preference are honoured.
7. The dashboard builds from a clean clone in CI with exact dependency pins.
8. The local-only boundary is proven at the request level, and no code path writes to `runs/`, `ledger/`, or `config/`.
9. The dashboard's design reference is its own documentation (decision D6); notes that describe another surface are marked as such.

## Open question (not a story)

Whether the dashboard should also show the review loop itself — verdict flow by domain from the local verdict log, open vetoes, stale reviews — rather than only report values and traction. This is a User Experience and Chief of Staff decision on scope. If taken, it inherits requirements 2, 3, 4, 6, and 8 unchanged.

## Stories

### 4.S1 — Purpose statement and local, read-only boundary

**Deliverable.** `dashboard/README.md` as a human page; a request-level boundary test; a static write-path test. 
**Acceptance criteria.**
- [ ] `dashboard/README.md` opens with purpose, optional status, local-only rule, and data sources; it contains no issue references or hold notes; it passes the Workstream 2 human-page checks.
- [ ] Working notes formerly at the top of the README live in an `audience: agent` file or in the installation's private store (decision D4); the pull request records which.
- [ ] A request-level test sends an administrative-screen request with a non-local host header and asserts a redirect to the public page; with a local host header it asserts success.
- [ ] A static test asserts no code under `dashboard/src` writes to `runs/`, `ledger/`, or `config/`.
- [ ] A static test asserts no third-party analytics or telemetry code is present under `dashboard/src`, keeping `docs/capability-report.md` section 7.4 true by test.
**Risks / exclusions / rollback.** Risk: the boundary test passes against a mocked server but not the real one — check: the test drives the built application. Exclusion: no change to how the local host gate is implemented. Rollback: revert; documentation and tests only. 
**Done / miss.** Done when the README passes and both tests pass. Miss when any write path or external call exists. Quality detects; Engineer may not stamp.

### 4.S2 — State contracts, fixtures mode, and live stills

**Deliverable.** A state contract per screen in the dashboard's own design reference document; a fixtures mode; a screen-by-state test; a still of the running local application for each screen in each state. 
**Acceptance criteria.**
- [ ] The design reference document lists every screen and, for each, the copy and named source for empty, not measured, measured, and error states.
- [ ] Fixtures mode loads placeholder data for each state from a fixtures directory; placeholder names only; fixtures mode is off unless explicitly enabled, and a test asserts the default build contains no fixture data.
- [ ] A test renders every screen in every state and asserts the contract copy is present; in empty and not-measured states it asserts no numeric value is shown other than a date.
- [ ] Parsing of report values recognises every label the improve README defines for an unmeasured value and treats each as unmeasured (unit tests per label).
- [ ] The error state names the file that could not be read and does not show stale values from a previous read.
- [ ] For every screen and state, a still captured from the running local application at the tip under review is attached to the pull request; a still of a mock frame, a design file, or a different tip is rejected; the capture method is not named in the repository.
**Risks / exclusions / rollback.** Risk: stills are taken from an older tip — check: each still is labelled with the tip's commit and the Quality role compares. Exclusion: no visual design changes. Rollback: revert; fixtures and tests only. 
**Done / miss.** Done when the matrix test passes and every state has a live still. Miss when any screen shows a number without a source, invents a value for an unmeasured cell, or is proven only by a mock. Quality detects; User Experience may not stamp.

### 4.S3 — Human-facing report feed only

**Deliverable.** A feed filter in the sync; a test that seeds excluded kinds. 
**Acceptance criteria.**
- [ ] The sync copies only the human-facing part of the improve record per the D5 option recorded: under (a) the human report files; under (b) the human summary section of each day's file; under (c) nothing from the improve record. It never copies the folder README, the template, the operations changelog, agent logs, or intake notes.
- [ ] A test places one file of each excluded kind in a temporary source and asserts none appears in the application's content.
- [ ] A test seeds process shorthand into an agent-facing part of the record and asserts it does not appear in any rendered screen.
- [ ] Until D5 is recorded, the sync is limited to the date-named report files that exist today, and that limitation is stated in the sync's own documentation comment.
**Risks / exclusions / rollback.** Risk: option (b) section parsing breaks on a malformed file — check: a malformed fixture produces the error state, not partial content. Exclusion: no change to how reports are written. Rollback: revert the filter; the prior copy-all behaviour returns and the problem statement above applies again. 
**Done / miss.** Done when the exclusion test passes. Miss when any non-human content appears in the application's content. Quality detects; Engineer may not stamp.

### 4.S4 — Accessibility proof

**Deliverable.** An automated accessibility check in CI over the screen-by-state matrix, configured in the repository by the User Experience owner; keyboard and reduced-motion tests. 
**Acceptance criteria.**
- [ ] The accessibility check runs in CI against every screen in every fixture state and the build fails on any finding the check reports; the check's configuration file is in the repository and names the User Experience role as its owner.
- [ ] Every interactive element is reachable and operable by keyboard; focus is visible (test).
- [ ] With the reduced-motion preference set, no continuous animation runs (test toggles the preference and asserts no running animation).
- [ ] The dashboard's documentation states the accessibility standard the check is configured against, taken from the check's configuration rather than written by hand.
**Risks / exclusions / rollback.** Risk: the configuration is loosened to make the build pass — mitigation: changes to the configuration file require the User Experience owner's recorded approval in the pull request, and the Adversary challenges each change. Exclusion: manual assistive-technology testing is not claimed. Rollback: disable the job; the configuration file remains for the next attempt. 
**Done / miss.** Done when the CI check is green over the full matrix under the recorded configuration. Miss when a finding is present or an animation ignores the preference. Quality detects; User Experience may not stamp.

### 4.S5 — Clean-clone build and dependency posture

**Deliverable.** A CI job that installs and builds the dashboard from a clean clone; exact dependency pins; corrected links and dispositions in the dashboard's documentation. 
**Acceptance criteria.**
- [ ] A CI job runs the documented dashboard install and build commands on a clean machine image with no cache and exits zero.
- [ ] Every dependency in `dashboard/package.json` is pinned to an exact version; a test fails on a range specifier.
- [ ] The licence note for native dependencies in `docs/capability-report.md` remains and is linked from `dashboard/README.md`.
- [ ] The link check reports none broken under `dashboard/docs/`.
- [ ] The design notes that describe another surface begin with a disposition line saying so, per decision D6, and the dashboard's own design reference document is named as the source for this application.
**Risks / exclusions / rollback.** Risk: exact pins block security updates — mitigation: the pin test allows a pin change when the lockfile changes with it in the same pull request. Exclusion: no dependency is added or removed by this story. Rollback: revert; the build job is removed and the prior manifest returns. 
**Done / miss.** Done when the build job is green and the pin test passes. Miss when the build needs a manual step not in the documentation. Quality detects; Engineer may not stamp.

## Fail conditions (rejected outright)

- A value shown without a named source.
- A number invented for an unmeasured cell.
- Any write to `runs/`, `ledger/`, or `config/` from the dashboard.
- Any non-human-facing part of the improve record in the dashboard's content.
- A screen without a defined empty, not-measured, and error state.
- A state proven by a mock frame or design file instead of a still of the running local application at the tip.
- A capture tool or method named in this repository.
- A dependency range instead of an exact pin.
- Any reference to the public marketing site's features as a design source or gate for this application.

## Falsification (Adversary)

| Claim | Procedure | Expected |
|---|---|---|
| Honest states | Run fixtures mode in each state; visit every screen | Contract copy present; no unsourced value |
| Proven live | Compare each still's labelled tip to the pull request tip | Equal for every still |
| Read-only | Static write-path test | No write path |
| Only human-facing content flows | Seed each excluded kind; run the sync | None appear in content |
| Accessibility check bites | Introduce a known accessibility defect in a fixture; run the check | Build fails |
| Reduced motion honoured | Toggle the preference; sample animations | None running |
| Clean clone builds | Fresh image; documented commands | Exit zero |
| Local-only | Request with a non-local host header | Redirect to the public page |
| Own design reference | Read the first line of the other-surface design notes | Disposition line present |

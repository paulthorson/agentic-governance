# Initiative — making the framework ready for a new installer

**Draft plan — awaiting review. Nothing in this plan is implemented, approved, or in force. Do not merge.**

This page is for people: installers, operators, and contributors deciding whether this work is worth doing. It comes from reading this repository at `main @ a0a79ef` the way a newcomer would. The detailed plan for the roles that would do the work is in the five workstream files linked at the end.

## 1. Bottom line

- **What this is.** A plan to make the framework trustworthy for someone who has never seen it: install it, believe what its pages say, reuse its role definitions, and read its optional local dashboard without being misled.
- **What works today.** The engine. Following the install steps starts the server, the structure validator passes, and the test suite passes at `a0a79ef`.
- **What does not yet.** The pages and files around the engine. Rules about what may appear on public pages (the files a visitor or installer reads) are applied by people rereading diffs, not by a check. Documentation names tools that are not in the repository and states counts that do not match it. The role instruction files other teams are meant to reuse carry one installation's working state. The local dashboard has no stated behaviour for empty or unmeasured data.
- **What this plan proposes.** Five workstreams that replace hand-applied rules with checks that fail on a seeded defect (a deliberately planted fault that proves a check can fail). The public-page content check is a **candidate only**: an earlier version of its requirements did not pass operator review, the reasons were not recorded, and this plan does not guess them.
- **What happens next.** Nothing is built until decisions are recorded. The operator decides the requirements for the public-page content check; the Chief of Staff (the framework role that carries decisions between the human operator and the other roles) records the remaining decisions in section 6. Only after the operator accepts the content-check requirements does build work begin in any workstream.

## 2. Why this matters

A governance framework is judged on what a newcomer does in the first hour: install it, believe what it says about itself, and reuse its role definitions without inheriting someone else's backlog. At `a0a79ef` each of those has a gap that only a careful human reader would catch.

The framework's own capability report separates controls that are code from controls that are instructions (`docs/capability-report.md`, sections 12.7–12.8). Every control over public-page content, documentation accuracy, and rule status sits on the instruction side today. This plan moves the ones that can be checked mechanically to the code side and says plainly which ones cannot.

## 3. Outcomes

Each outcome either holds on `main` or it does not.

1. **Public-page content check (candidate).** Requirements are decided and recorded with the operator. If accepted, a check built from those requirements fails on a seeded defect and passes on a clean fixture, and it runs in report-only mode until the operator decides it should block.
2. **Install and first-run proof.** The documented install path completes in a clean environment in CI. Verification never writes into an installer's working records.
3. **Documentation truth.** Every path, command, and count in the documentation matches the repository. Links resolve. Every public page says who it is for.
4. **Reusable role files.** Role instruction files contain the sections the framework's own skeleton requires, load on their own, and carry no repository ticket references or installation-specific working state.
5. **Process records and rule status.** Each governance rule has one recorded status wherever it is cited. Every CI step fails on a seeded defect or is removed. Append-only records are protected by a check. Intake and the human decision queue have documented, placeholder-safe shapes.
6. **Localhost framework dashboard.** The optional local dashboard states what each screen shows when data is empty, not measured, measured, or unreadable; never shows a value without a named source; reads only the human report; passes an automated accessibility check in CI; and builds from a clean clone. Its states are proven with stills of the running local application, not mock-ups.

## 4. Scope and non-goals

**In scope:** this repository only — install and onboarding pages, documentation, role instruction files, governance records and CI, and the optional local dashboard under `dashboard/`.

**Not in scope:**

- Any other repository. Where a file here points at one, the pointer is fixed here and nothing is edited there.
- The public marketing site and everything on it, including its visual "instrument" feature and its typography readiness work. Those live in another repository and this initiative does not touch them.
- Changing the constitution's rules or any domain veto. Those follow the amendment procedure in `constitution/constitution.md`.
- Drafting, revising, or interpreting legal text. Agents do not author legal language.
- Implementing anything in this pull request. This is a plan.
- Visual design of the local dashboard. Its workstream covers behaviour, honesty, and accessibility.
- Inferring why the earlier public-page requirements did not pass review.
- Changing repository history.

## 5. Workstreams

### Workstream 0 — Public-page content check (candidate)

*Problem.* CI runs a structure validator, tests, and a secrets scan; nothing evaluates what public pages say. The rules that exist for this are recorded as process, in the ledger and in role instruction files. An earlier requirements version for this check did not pass operator review, and the reasons were not recorded. 
*Done looks like.* Requirements decided with the operator and recorded in the operator's words. If accepted: a check that fails on seeded defects and passes clean, rolled out report-only first, blocking only on the operator's decision. 
*Plan:* [`epic-0-public-page-proof-candidate.md`](./epic-0-public-page-proof-candidate.md)

### Workstream 1 — Install and first-run proof

*Problem.* The install page lists prerequisites without versions and hands off to "your agent host" without linking the guides that exist. The server starts silently. Installing dependencies on a clean clone modifies a tracked file. The documented verification writes test records into the same files the framework treats as the installation's decision history (`scripts/smoke_test_mcp.py`). 
*Done looks like.* A CI job runs the documented install on a clean machine and passes; the working tree is clean afterwards; a newcomer can confirm a healthy install without connecting an agent; verification is isolated; every host guide has the same steps. 
*Plan:* [`epic-1-install-and-onboarding-proof.md`](./epic-1-install-and-onboarding-proof.md)

### Workstream 2 — Documentation and reusable role files

*Problem.* Several pages reference a script and a directory that do not exist. Pages say the framework ships five domains; the validator reports twelve plugin folders. One page says the repository is private. No page states whether it is for people or for agents, and the daily improve reports read as agent logs despite being described as a plain-English record. Role instruction files contain repository ticket references and working state, although the framework's own adoption record says they must load standalone (`docs/adr/0006-first-real-team-adoption.md`). 
*Done looks like.* Referenced paths exist; links resolve; counts are generated from the tree; every page declares its audience; role files have the required sections, load standalone, and carry no ticket references or local state. 
*Plan:* [`epic-2-documentation-and-reusable-role-surfaces.md`](./epic-2-documentation-and-reusable-role-surfaces.md)

### Workstream 3 — Process records and rule status

*Problem.* Rule status is written in prose in several places, and the places disagree: on one page a rule's own row says draft while a sibling row refers to it as in force. A CI step named for link and frontmatter integrity cannot fail. Append-only records rely on convention. The human decision queue has no example entry, and there is no intake template. 
*Done looks like.* Every rule has one consistent recorded status; every CI step has a seeded-defect fixture; append-only records are protected; intake and queue shapes are documented with placeholders. Whether status moves into a single registry is a decision, not a given. 
*Plan:* [`epic-3-process-evidence-and-status-consistency.md`](./epic-3-process-evidence-and-status-consistency.md)

### Workstream 4 — Localhost framework dashboard UX

*Problem.* The dashboard's page opens with working notes rather than saying what it is for. Its design notes describe a different, public surface. Its report sync copies every markdown file in the improve folder, including templates. No screen defines what it shows when data is empty, unmeasured, or unreadable. No accessibility check or clean build runs in CI. 
*Done looks like.* Purpose and local, read-only boundary stated; per-screen state contracts proven with stills of the running local application; only human reports flow in; accessibility check and clean build in CI; no value without a source. 
*Plan:* [`epic-4-localhost-dashboard-ux.md`](./epic-4-localhost-dashboard-ux.md)

## 6. Sequence and unresolved decisions

**Sequence.** Decisions come before builds. Workstream 0 begins with a requirements decision, not code. Build work in every workstream waits for the operator's acceptance of those requirements (see section 7, layer B). Once open, Workstreams 1 and 3 establish the proof pattern (seeded defect plus clean fixture) that the others reuse; Workstream 2 uses the path and link checks from Workstream 3; Workstream 4 depends on the report decision (D5) and on Workstream 3's status vocabulary.

**Decisions this plan needs and does not make.** Each row lists the genuine options with what each gives up, so the decider can choose. Where a default is named, it applies only if no decision is recorded.

| # | Decision | Options and what each gives up | Who decides | Default if undecided |
|---|---|---|---|---|
| D1 | Requirements for the public-page content check: what it covers, how exceptions are approved, whether it blocks or reports, who owns it. | Open. The earlier requirements version did not pass review; reasons unrecorded. No option is pre-selected here. | Operator, with the Chief of Staff | No check is built. Workstream 0 stays at the requirements step. |
| D2 | Where rule status is recorded. | **(a)** One registry file with a schema — one place to read, but a migration and a new file to keep in step with the pages. **(b)** Keep status on the existing pages and add a check that fails when two places disagree — no migration, but status stays spread across pages. | Chief of Staff; Adversary may challenge | (b). Existing records stay authoritative. |
| D3 | Tooling that documentation references but the repository lacks. | **(a)** Build it — pages become true, at the cost of new code to maintain. **(b)** Remove the references — pages become true today, and contributors lose a described workflow that never existed. | Product Manager | (b). |
| D4 | Where installation-specific working state goes when removed from role files. | **(a)** The framework's private memory template (`docs/templates/cos-memory/`) — designed for it, but per-installation setup is required. **(b)** An agent-facing file in this repository — simpler, but the state stays public. | Chief of Staff | Moved out of the public role files; destination named per item in the pull request. |
| D5 | How the daily improve record serves people and agents, and what the dashboard reads. | **(a)** Two files per day: a human report and an agent log; the dashboard reads the human report. Clear audiences, but two files to keep aligned and more daily writing. **(b)** One file per day with a human summary first and an agent section after; the dashboard reads only the summary section. One file, but the sync must parse sections and the plain-language bar is harder to hold. **(c)** Keep the current single record and stop feeding the dashboard from it; the dashboard shows only values from the measured traction file. No daily writing change, but the dashboard loses the daily narrative. | Chief of Staff and Product Manager | No change to the record. The dashboard sync stays limited to the date-named report files that exist today. |
| D6 | Which design reference the local dashboard follows. | **(a)** Its own, written for a local operator tool — fits its purpose, but is new work. **(b)** The reference in its current notes, written for a public marketing surface — exists already, but describes a different audience and surface. | User Experience with the Chief of Staff | (a), recorded in the dashboard's documentation. |

## 7. Initiative acceptance

Acceptance has two layers. Layer A can close without any build. Layer B opens only after the operator has accepted the Workstream 0 requirements; no item in layer B is a condition for closing layer A.

**Layer A — recorded requirements and decisions**

- [ ] D1 has an operator decision line (`accepted`, `returned`, or `rejected`), written by the operator.
- [ ] D2–D6 each have a recorded decision, or are explicitly recorded as deferred with the default applying.
- [ ] The Workstream 0 requirements document exists, every requirement in it is testable, and it contains no statement about why the earlier version did not pass.
- [ ] Each of Workstreams 1–4 has its requirements list reviewed by its owning roles, with the review recorded in the pull request.
- [ ] No status is stamped for any rule, check, or workstream by this layer.

**Layer B — build, blocking CI, and ship gates** (opens only after D1 reads `accepted`)

- [ ] Workstream 0: check exists; every seeded defect fails; clean fixture passes; a report-only run is recorded; blocking mode is enabled only after a second recorded operator decision.
- [ ] Workstream 1: clean-environment CI job passes; working tree clean after dependency install; verification leaves `runs/` unchanged; every onboarding guide has the same section headings in the same order.
- [ ] Workstream 2: every referenced path exists; link check reports none broken; generated facts match the tree; every public page declares its audience; role files pass the required-sections, no-ticket-reference, and standalone-load checks.
- [ ] Workstream 3: status consistency check passes; every CI step has a seeded-defect fixture and fails on it; append-only check rejects an edit to an existing record; intake template and queue example exist and pass the shape check.
- [ ] Workstream 4: every screen renders in each declared state without an unsourced value, proven with stills of the running local application at the tip; only human reports are synced; the accessibility check passes; the clean-clone build passes.
- [ ] No box is checked by the role that did the work; the Quality role records each result, and the Adversary (the framework's reviewing role) records its challenge per workstream.

## 8. Link to agent plan

The agent-facing files carry requirements, stories, acceptance criteria, owners, risks, and fail conditions:

- [`epic-0-public-page-proof-candidate.md`](./epic-0-public-page-proof-candidate.md)
- [`epic-1-install-and-onboarding-proof.md`](./epic-1-install-and-onboarding-proof.md)
- [`epic-2-documentation-and-reusable-role-surfaces.md`](./epic-2-documentation-and-reusable-role-surfaces.md)
- [`epic-3-process-evidence-and-status-consistency.md`](./epic-3-process-evidence-and-status-consistency.md)
- [`epic-4-localhost-dashboard-ux.md`](./epic-4-localhost-dashboard-ux.md)

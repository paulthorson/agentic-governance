# Workstream 1 — Install and first-run proof

**Status:** proposed. Nothing here is implemented or in force. 
**Audience:** agent (seats that execute). 
**Reviewed at:** `main @ a0a79ef`. 
**Owners:** Product Manager owns the install page wording. Engineer owns the server's start and self-check behaviour, dependency declarations, verification isolation, and the CI job. Quality owns fixtures and records results. User Experience owns the structure of the install page. Adversary challenges and may not stamp. 
**Layers:** the requirements below are layer A once reviewed by the owning roles. All stories are layer B and open only after the operator accepts the Workstream 0 requirements. 
**Depends on:** nothing. **Enables:** Workstream 4 (clean-build pattern), Workstream 3 (fixture pattern).

## Rule

The install path a newcomer follows is the path CI executes. If the documented steps and the CI job differ, the documentation is wrong until they match.

## Problem (verifiable at `a0a79ef`)

1. `README.md`, "Install (framework)": prerequisites are listed without versions; the "connect the server to your agent" step says wiring depends on the host and does not link the per-host guides under `docs/onboarding/`.
2. `mcp/adversarial_mcp/server.py`, `main()`: the server writes nothing on a successful start over the default transport and nothing on a clean exit. A newcomer cannot tell a working start from a hung one.
3. `mcp/pyproject.toml` and `mcp/uv.lock` record different versions for the package itself. Installing dependencies from a clean clone modifies the lockfile, so the first documented command leaves the working tree modified.
4. `CONTRIBUTING.md`, "Run validators": the test command requires a test runner that the package manifest does not declare. The CI workflow installs it with a separate ad-hoc command.
5. `scripts/smoke_test_mcp.py` runs review tools against the repository root; those tools append records to `runs/`. Running the documented verification therefore writes test records into the files the framework treats as the installation's decision history.
6. `docs/onboarding/cursor.md` references a script that does not exist, and its relative links to the repository README take two different forms.
7. `docs/Home.md`, "Quick start": states the repository is private.

## Requirements

1. One canonical install page. Every other page that describes installation links to it rather than restating it.
2. Prerequisites state the minimum versions the repository itself declares.
3. A newcomer can tell that the server started and can confirm a healthy install without connecting an agent host. Diagnostic output never goes to the protocol stream.
4. Installing dependencies from a clean clone leaves the working tree unmodified.
5. Verification never writes to the installation's `runs/` directory.
6. The test command is declared once, in the package manifest, and the contributor guide and the CI workflow use the identical command.
7. A CI job executes the documented install on a clean machine image from the repository's own instructions. The image is the one the workflow declares; adding platforms is an Engineer decision recorded in the workflow, not a requirement here.
8. Every per-host onboarding guide has the same section headings in the same order.
9. The setup wizard can be previewed without an agent host: every question, its options, and where the answer is written, without writing anything.

## Stories

### 1.S1 — Canonical install page and troubleshooting

**Deliverable.** The README install section as the single path, linking every per-host guide; a troubleshooting page under the onboarding docs with entries in the shape *symptom → cause → fix → cite*. 
**Acceptance criteria.**
- [ ] Every guide under `docs/onboarding/` is linked from the README install section; every link in that section resolves.
- [ ] Prerequisite versions on the install page match the values the repository declares in its package manifest.
- [ ] No public page states that the repository is private.
- [ ] Every troubleshooting entry cites a repository path and contains no transcript or narrative.
- [ ] No other page restates the install steps; they link to the README section.
**Risks / exclusions / rollback.** Risk: a guide restates steps and drifts — check: the link test fails on a page that repeats the install commands. Exclusion: no change to the wizard or to server behaviour. Rollback: revert; documentation only. 
**Done / miss.** Done when the link check and the version check pass. Miss when a page restates steps or a link fails. Quality detects; Product Manager may not stamp.

### 1.S2 — Clean-environment proof

**Deliverable.** A start and exit signal on the diagnostic stream; a self-check a newcomer can run without a host; a consistent lockfile; a CI job that runs the documented install on a clean machine image. 
**Acceptance criteria.**
- [ ] Starting the server over the default transport writes one line to the diagnostic stream on start and one on clean exit; with input closed immediately, the protocol stream carries zero bytes (test).
- [ ] A newcomer can run a self-check without an agent host; it exits zero on a healthy tree and non-zero otherwise, and it reports the installed version.
- [ ] After the documented dependency-install command on a clean clone, the working tree shows no modified files.
- [ ] A CI step fails when the lockfile and the package manifest disagree.
- [ ] A CI job on the clean machine image the workflow declares installs from the README instructions, runs the self-check, and runs the repository's structure validator; all exit zero; no cached dependencies are used on the first step.
**Risks / exclusions / rollback.** Risk: the start line reaches the protocol stream and breaks hosts — check: the zero-byte test. Exclusion: transports other than the default are unchanged. Rollback: revert the commit; no data or configuration migrates. 
**Done / miss.** Done when the job is green. Miss when any step passes only with a manual pre-step not in the README. Quality detects; Engineer may not stamp.

### 1.S3 — Isolated verification and declared test dependencies

**Deliverable.** Smoke test and self-check that run against an isolated location; the test runner declared as a development dependency; one test command everywhere. 
**Acceptance criteria.**
- [ ] With a sentinel line placed in each file under `runs/`, running the smoke test and the self-check leaves every file byte-identical (test).
- [ ] The framework's status tool does not count verification records against the installation's recorded usage.
- [ ] The package manifest declares the test runner as a development dependency.
- [ ] The contributor guide and the CI workflow contain the identical test command (test compares both).
- [ ] The ad-hoc install line for the test runner is removed from the workflow.
**Risks / exclusions / rollback.** Risk: isolation is bypassed by an environment variable — check: the sentinel test runs with and without the variable set. Exclusion: no change to how real reviews record verdicts. Rollback: revert; existing `runs/` files are untouched either way. 
**Done / miss.** Done when the sentinel test passes and the two commands match. Miss when verification writes to `runs/` under any invocation. Quality detects; Engineer may not stamp.

### 1.S4 — Onboarding parity

**Deliverable.** Every guide under `docs/onboarding/` shares the same section headings in the same order: install, connect, verify, run a governed review, adopt an existing agent. 
**Acceptance criteria.**
- [ ] A test lists the level-two headings of every onboarding guide and asserts they are identical in order.
- [ ] No onboarding guide references a path that does not exist in the repository.
- [ ] Every relative link under `docs/onboarding/` resolves.
- [ ] Each guide's verify section links the troubleshooting page.
**Risks / exclusions / rollback.** Risk: a host-specific step has no place in the shared order — mitigation: host-specific notes go under the guide's own connect section, not a new heading. Exclusion: no new host guides. Rollback: revert; documentation only. 
**Done / miss.** Done when the heading test and link check pass. Miss when any guide diverges. Quality detects; Product Manager may not stamp.

### 1.S5 — Wizard preview without a host

**Deliverable.** A way to print every setup-wizard question in order with its identifier, options, and destination, without writing; and a non-interactive mode that writes the wizard's output to a caller-chosen directory from an answers file. 
**Acceptance criteria.**
- [ ] Running the preview with no arguments writes nothing to disk (working tree unchanged; no `config/` created).
- [ ] The preview lists every question in the wizard's flow in the order the wizard asks them (test compares to the wizard's own question list).
- [ ] Non-interactive mode writes only to the directory given; it refuses to write into `config/` unless that directory is named explicitly.
- [ ] An example output under the onboarding docs uses placeholder names only.
- [ ] The adoption walkthrough states that the preview does not inspect any runtime.
**Risks / exclusions / rollback.** Risk: preview and wizard flows diverge — check: the comparison test. Exclusion: no new wizard questions. Rollback: remove the preview; the wizard is unchanged. 
**Done / miss.** Done when the preview matches the wizard's flow and writes nothing by default. Miss when it writes to `config/` implicitly. Quality detects; Engineer may not stamp.

## Fail conditions (rejected outright)

- An install step that works only with knowledge not on the install page.
- A verification command that writes to `runs/`.
- A test command that exists in one place but not the other.
- A CI job that installs from anything other than the repository's own instructions.
- An onboarding guide with a different section order.

## Falsification (Adversary)

| Claim | Procedure | Expected |
|---|---|---|
| Install path is the CI path | Compare the README commands with the CI job steps | Same commands |
| Tree stays clean | Run the documented dependency install on a clean clone; list modified files | None |
| Protocol stream is clean | Start the server with input closed; count bytes on the protocol stream | Zero |
| Verification is isolated | Sentinel test | Files unchanged |
| One test command | Compare the two strings | Equal |
| Guides are parallel | Heading test | Pass |
| Preview writes nothing | Run the preview; list modified and new files | None |

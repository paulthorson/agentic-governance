# Workstream 2 — Documentation and reusable role files

**Status:** proposed. Nothing here is implemented or in force. 
**Audience:** agent (seats that execute). 
**Reviewed at:** `main @ a0a79ef`. 
**Owners:** Product Manager owns the human-facing layer and the audience classification. Engineer owns the documentation tests, the link check, and the role-file lint. Chief of Staff owns the destination of any working state removed from role files (decision D4). Quality runs the checks and records results. Adversary challenges and may not stamp. 
**Layers:** the requirements below are layer A once reviewed by the owning roles. All stories are layer B and open only after the operator accepts the Workstream 0 requirements. 
**Depends on:** Workstream 3 (fixture pattern, link and path checks). **Enables:** Workstream 4 (report feed, per decision D5).

## Rule

A public page states only what the repository contains. A path that does not exist, a count that does not match the tree, a rule described as stronger than the code makes it, or a role file that only one installation can load is a defect, and a check must catch it before merge.

## Problem (verifiable at `a0a79ef`)

**Referenced things that do not exist.**
- `AGENTS.md`, `CONTRIBUTING.md`, `docs/Tooling.md`, `docs/Home.md`, `docs/README.md`, and `docs/onboarding/cursor.md` reference a consolidation script under `scripts/` and a `shared/skills/` directory. Neither is in the repository.
- `docs/README.md`, `constitution/constitution.md`, and `constitution/vetoes.md` link wiki-style to pages named Governance, Constitution, Vetoes, and Calibration. No file with those names exists under `docs/`.

**Facts that do not match the tree.**
- `docs/Domains.md`, `docs/Tooling.md`, and `docs/README.md` say the framework ships five domains. The structure validator reports twelve plugin folders, and the table in `docs/Domains.md` itself lists twelve.
- `constitution/vetoes.md` lists veto conditions for five domains. `constitution/domains/` contains twelve files.
- `constitution/constitution.md` describes the constitution as enforced mechanically and points to a per-plugin `references/constitution.md`. `README.md`, `SECURITY.md`, and `docs/capability-report.md` describe instruction and process controls with a small number of code gates, and the validator looks for domain constitutions under `constitution/domains/`.
- `docs/Roadmap.md` states agent, skill, tool, and test counts that differ from what the validator and test suite report.
- `docs/Home.md` says the repository is private.

**Audience is not declared.**
- No page states whether it is for people or for agents. `docs/improve/README.md` describes the daily reports as a plain-English public record; `docs/improve/2026-09-20.md` is written in process shorthand. `dashboard/README.md` opens with working notes. `docs/CoE.md` is titled as a plain-English write-up and consists mainly of rule tables.
- `docs/pre-merge-review.md` embeds full copies of `README.md`, `SECURITY.md`, `CONTRIBUTING.md`, and `docs/capability-report.md`, so those copies drift from the files they copy.
- `docs/quarantine/AUDIT.md` and the files under `docs/proposals/` carry no marker saying whether they are current, historical, or superseded.

**Role files are not reusable as shipped.**
- The files under `harnesses/` contain repository ticket references and installation-specific working state (holds, per-item merge instructions, references to other repositories' issues). `docs/adr/0006-first-real-team-adoption.md` records the lesson that role files must be standalone-loadable with no repository-relative references. The setup wizard carries its own harness skeleton that defines the sections a role file needs. A private memory template for operator-local state exists at `docs/templates/cos-memory/`.

## Requirements

1. Every repository path referenced from a public page exists. Every relative link and every wiki-style link resolves to a file.
2. Counts and enumerations on public pages are generated from the tree or omitted. A page never states a count by hand.
3. `constitution/vetoes.md` covers every file in `constitution/domains/`. `constitution/constitution.md` describes enforcement in the same terms as `docs/capability-report.md` and points at the paths the validator uses. The four rules and the veto conditions themselves are not changed by this workstream.
4. Every public markdown file declares its audience (`human`, `agent`, or `bridge`) in frontmatter. Human pages meet the bar in `skills/doc-framework-technical-writing/SKILL.md`. Agent pages are exempt from the human bar but not from the path, link, and audience checks.
5. The daily improve record follows the option chosen in decision D5. Whichever option is chosen, the part the dashboard reads is declared `human`, and the plain-language bar applies to it.
6. Every role file under `harnesses/` contains the sections in the wizard's harness skeleton, contains no repository ticket references, contains no installation-specific working state, and loads standalone: copied alone into an empty directory, every path it references is either present there or declared as external.
7. Working state removed from a role file is not deleted silently. Each removed block is listed in the pull request with its destination kind (per decision D4). The content of private destinations is never reproduced in the public repository.
8. Every file that is a working record rather than documentation begins with a disposition line: `current`, `historical`, or `superseded by <path>`. No page embeds a full copy of another tracked file.

## Stories

### 2.S1 — Referenced paths exist and links resolve

**Deliverable.** A documentation test that extracts repository paths from public pages and asserts existence; a link check for relative and wiki-style links; both in CI; the absent references resolved per decision D3. 
**Acceptance criteria.**
- [ ] The path test fails on a fixture page that references a non-existent file or directory and passes on `main`.
- [ ] The link check fails on a fixture with one broken relative link and one wiki-style link to a missing page, and reports none on `main`.
- [ ] Decision D3 is recorded in the pull request per referenced item (built, or reference removed); `AGENTS.md` and `CONTRIBUTING.md` describe the flat `agents/` and `skills/` layers as the tree and validator actually handle them.
- [ ] Wiki-style links either point to files that exist or are converted to file links; the choice is applied consistently across `docs/`.
- [ ] External links are not fetched by CI.
**Risks / exclusions / rollback.** Risk: the path test flags illustrative paths in examples — mitigation: a marked example block is exempt, and the exemption is itself tested. Exclusion: external link health. Rollback: revert; documentation and tests only. 
**Done / miss.** Done when both checks pass on `main` and fail on their fixtures. Miss when a page references an absent path. Quality detects; Product Manager may not stamp.

### 2.S2 — Generated facts match the tree

**Deliverable.** A generated facts block (domains, plugin folders, agents, skills, tools) used wherever a count appears; a vetoes-coverage test; the constitution's description of enforcement aligned with the capability report; repository-visibility statements corrected. 
**Acceptance criteria.**
- [ ] A test fails on any hand-written count of domains, agents, skills, tools, or tests on a public page outside a marked generated block.
- [ ] CI fails when a committed generated block differs from the generator's output.
- [ ] A test asserts one row in `constitution/vetoes.md` for every file in `constitution/domains/`.
- [ ] `constitution/constitution.md` describes enforcement in terms consistent with `docs/capability-report.md` sections 12.7–12.8 and points at `constitution/domains/`; a diff test shows the four rules unchanged.
- [ ] No public page states that the repository is private.
- [ ] `docs/Roadmap.md` contains no hand-written counts.
**Risks / exclusions / rollback.** Risk: the generator and the validator disagree on what counts as a plugin — check: the generator reads the same folder list the validator reads. Exclusion: no change to rule text or veto conditions. Rollback: revert; generated blocks return to their prior text. 
**Done / miss.** Done when all tests pass on `main`. Miss when any count is hand-written or any domain lacks a veto row. Quality detects; Product Manager may not stamp.

### 2.S3 — Audience declared; human pages meet the writing bar; improve record per decision D5

**Deliverable.** `audience` frontmatter on every public markdown file; a check that human pages open with a bottom-line section and use no internal term that a glossary page does not define; the improve record shaped per the D5 option chosen. 
**Acceptance criteria.**
- [ ] Every public markdown file declares `audience`; a file without it fails the check; unknown values fail.
- [ ] Every `audience: human` page opens with a section that states what the page is and who it is for (test on the first heading after the title).
- [ ] A glossary page defines each internal term used on human pages; a human page using a term not in the glossary fails the check; agent pages are exempt.
- [ ] The improve record follows the D5 option recorded in the pull request. Under option (a), each day has a human report and an agent log with audiences declared. Under option (b), each day's file is declared `bridge`, its human summary comes first, and the sync reads only that section. Under option (c), the record is declared `agent` and the dashboard does not read it. In every option, prior records are left unchanged.
- [ ] `dashboard/README.md` and `docs/CoE.md` are declared `human` and pass the human-page checks; their rule detail moves to agent-facing files or to the status record chosen in Workstream 3.
**Risks / exclusions / rollback.** Risk: the glossary becomes a place to legitimise jargon — mitigation: the Product Manager approves each glossary entry in the pull request. Exclusion: no change to role-file content (story 2.S4). Rollback: remove the frontmatter and checks; pages are unchanged otherwise. 
**Done / miss.** Done when every public page declares an audience and every human page passes. Miss when a human page needs an insider to read it. Quality detects; Product Manager may not stamp.

### 2.S4 — Reusable role files

**Deliverable.** Each role file under `harnesses/` reduced to the role contract; a role-file lint in CI; a standalone-load test; a migration table in the pull request for every removed block. 
**Acceptance criteria.**
- [ ] Every role file contains every section of the wizard's harness skeleton, in order (test compares headings to the skeleton the wizard itself uses).
- [ ] No role file contains a repository ticket or pull-request reference, a hold instruction, or a per-item merge instruction (lint; fixture fails).
- [ ] No role file names a third-party agent runtime, vendor, or agency; engine-specific notes live under the onboarding or engine documentation.
- [ ] Standalone load: with the role files copied alone into an empty directory, every relative path referenced either exists there or is listed in the file as external; the test passes.
- [ ] Rules that remain framework law are referenced by identifier plus a one-sentence "who stamps"; each identifier resolves in the status record chosen in Workstream 3.
- [ ] The pull request lists every removed block with a destination kind; no removed block's content appears anywhere in the public repository afterwards, except where the destination is a framework record.
- [ ] The existing harness single-source check still passes, and wizard persona generation still resolves every role file it cites (existing tests pass).
**Risks / exclusions / rollback.** Risk: a rule that is genuinely framework law is removed as working state — mitigation: the Chief of Staff classifies each block before removal and the Adversary challenges the table. Exclusion: no change to which roles exist or to the production chain. Rollback: restore the prior role files from history; the migration table records what was moved and where. 
**Done / miss.** Done when lint and standalone-load pass on `main`. Miss when a role file carries working state or a ticket reference. Quality detects; Chief of Staff may not stamp its own migration table.

### 2.S5 — Working records carry a disposition; no embedded copies

**Deliverable.** Disposition lines on working records; `docs/pre-merge-review.md` reduced to an index of links. 
**Acceptance criteria.**
- [ ] Every file under `docs/quarantine/` and `docs/proposals/`, and `docs/pre-merge-review.md`, begins with a disposition line (`current`, `historical`, or `superseded by <path>`); a test asserts it.
- [ ] No public page contains a fenced block that reproduces the full content of another tracked file (test compares fenced blocks against tracked files).
- [ ] The link check reports none broken in the reduced review pack.
**Risks / exclusions / rollback.** Risk: a record marked historical is still the only place a fact lives — check: the Product Manager confirms each fact has a current home before the marker is added. Exclusion: files are not deleted in this story. Rollback: revert; documentation only. 
**Done / miss.** Done when the disposition and embed tests pass. Miss when a working record reads as current documentation. Quality detects; Product Manager may not stamp.

## Fail conditions (rejected outright)

- A public page that references a path absent from the tree.
- A hand-written count.
- A rule described as enforced by code when `docs/capability-report.md` records it as instruction.
- A role file that a second installation cannot load unchanged.
- A removed block whose destination is not recorded, or whose private content is reproduced in the public repository.
- A change to the four constitutional rules or any veto condition under this workstream.

## Falsification (Adversary)

| Claim | Procedure | Expected |
|---|---|---|
| Paths exist | Reference a non-existent file on a public page; run the test | Fails, naming the path |
| Links resolve | Add one broken relative link and one wiki-style link to a missing page | Two named failures |
| Facts are generated | Hand-write a domain count outside a generated block | Fails |
| Vetoes cover every domain | Add a fixture domain file; run the test | Fails until a row exists |
| Law unchanged | Diff the four rules and veto conditions against `a0a79ef` | No change |
| Audience declared | Remove frontmatter from one public page | Fails |
| Role files reusable | Copy the role files alone to an empty directory; run lint and standalone-load | Pass |
| Nothing dropped silently | Compare removed blocks to the migration table | Every block has a destination |

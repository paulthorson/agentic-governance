# Changelog

All notable changes to the Adversarial Agents framework.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **UX harness lock: Mermaid userflows + JTBD before Eng handoff (Cos ACCEPT B).**
  Named Critic Check 7 at UX→Eng gate: require `userflows.md` (Mermaid: entry, success,
  key error/empty, exits) + `jtbd.md` + Research cite, **or** explicit `NO_RESEARCH` →
  escalate to human (do not invent). Check 7 is **stacked on `RESEARCH_BEFORE_ENHANCE`**,
  not a replacement. Metric: UX epics missing those at Critic = **fail closed**. Scope:
  product UX epics only — **not** OpenClaw briefs. P0: no PII/secrets in AG git. Stop
  conditions for missing/misaligned artifacts; CX Advocate + Evaluative UXR treat Mermaid
  flows as the flow under review and note when not checked vs research. SoT:
  `harnesses/ux.md`; adversarial-ux critic/advocates + flat `agents/ux-*` copies.
  (Unrelated to PR #13 intake.)

- **`RESEARCH_BEFORE_ENHANCE` (Rule 2 A) + `ADV_COMP_CRITIQUE` standing lock** — hard gate
  (soft / deferred Look gate REJECTED). Named sensors `cite-real-screens` +
  `adv-comp-critique` fail-closed (a scar/wiki page is not the gate). Required artifact
  `docs/epics/<slug>/evidence.md` (or stills index) with real-screen source URLs + what the
  pixels show, before PM→UX brief / before first story. Jury (Critic, CX Advocate, Evaluative
  UXR) must open cited screens; **jury artifact before Pack/Look** must name opened screen IDs
  or URLs (no secrets/keys/emails/host paths) **and** ≥1 hole in our UI **and** ≥1 hole in a
  competitor screen **and** one do-not-copy gap — Pack/Look FAIL if no opened-screen cites.
  Comps are not gospel. Metric: enhancement packs without cited real-screen evidence = fail closed.
  Scope: product UX/Research + adversarial UX jury (not OpenClaw morning-brief). SoT:
  `constitution/domains/ux.md`, `constitution/domains/researcher.md`,
  `projects/_standing/scars/research-before-enhance.md`, adversarial-ux agents + desk-research
  pointers. P0: no keys, tokens, emails, PII, absolute host paths, or private operator data.
- **OpenClaw morning-brief cite-or-blank scar SoT** (docs only;
  `MORNING_BRIEF_CITE_OR_BLANK` Rule 2 A; `validate-brief-grounding.py`
  fail-closed before Discord) at
  `projects/openclaw/scars/morning-brief-cite-or-blank.md`. CLOSED harness scar
  for invented meetings after KICK_BACK+rewrite; OpenClaw morning briefs only.
- **OpenClaw bridge-guard false-clobber scar SoT** (docs only; structural vs
  content check named) at
  `projects/openclaw/scars/bridge-guard-false-clobber.md`.
- **Dashboard public + admin split.** Same Vercel deploy (`dashboard/`): public
  marketing at `/` (KPI strip, Get AG CTA, traction gated by
  `data/traction.json`); admin at `/admin/*` behind Auth.js v5 Google SSO with
  allowlist (`noreply address` + optional `ADMIN_EMAILS`). Admin shows
  honest Baseline / unpaid token placeholders, cycle-time tables, improve
  report detail, raw traction (including below `minVisible`), and anonymized
  scar index — never invents live token/$ numbers; no Studio PII.
- **OpenClaw pin-enforce scar SoT** at
  `projects/openclaw/scars/pin-enforce-version-drift.md` (docs only; Cos
  canonicalizes on OpenClaw Eng’s draft, not Bridge paste). CLOSED harness scar
  for silent downgrade via nightly `npm update -g openclaw` vs pin; documents
  the pin-enforce process lock only — no framework-policy invention beyond that
  lock.
- **Continuous improve reporting path.** Daily markdown reports live under
  `docs/improve/` (README with KPI rules, `_template.md`, dated stubs). KPIs
  must be measured or method-estimated — never invented. A public Next.js
  marketing dashboard under `dashboard/` (UI SoT = Meta Astryx:
  `@astryxdesign/core` + `theme-neutral`) puts KPI strip/charts first, a loud
  Get AG CTA second, then changelog/contribute. Traction widgets are fully
  wired but gated by `data/traction.json` `minVisible` thresholds (hidden on
  launch). Vercel-ready; Cos/Paul must make the marketing surface public.

- **Chief of Staff (Cos) for multi-team mode.** Setup wizard asks whether the
  operator will run more than one project/team at once; if yes, a Cos roster
  row is required. Cos is the human funnel: only Cos surfaces decisions to the
  human; Cos owns the Section 13 morning queue in multi-team mode; Cos triages
  P0/P1 and enforces the daytime escalate; Cos watches governance and
  drafts amendment proposals (human still gates the constitution). Single-team
  mode unchanged: CEO → human for the morning queue. Harness:
  `harnesses/chief-of-staff.md`. Spec/comms/wizard deltas as recorded in the
  Cos proposal.
- **Cos escalation behavior is wizard-configured, not hardcoded.** Two new
  setup-wizard questions: quiet-hours P0 behavior (`interrupt` to break through
  via messaging, or `defer` to queue at the head until quiet hours end) and the
  daytime escalate SLA in hours (default 4). Both land in `config/setup.md`.
  Operator's own quiet hours stay in local config; nothing personal ships in
  the build.
- **Vanilla handoff (ADR-0006, ADR-0007).** The framework is now environment-agnostic —
  adopters take the constitution + harnesses as a loadable contract (no repo mirror).
  First real-team adoption: Ladders Grok Bot (2026-09-06).
- **Watchdog data-source abstraction (ADR-0007).** `stuck-review-watchdog.py` now
  supports `--source paperclip` (default), `--source file --issues-file <path>` (JSON
  file or stdin), and `--source none` (disabled until an in_review backend exists).
  `collect_stuck` logic unchanged; backward-compatible.
- **Setup wizard data-source questions.** The wizard now asks where in_review issues
  and the verdict ledger live (`issue_source`, `issues_file`, `verdict_log`) and writes
  them to `config/setup.md`, so the watchdog + telemetry are configured at setup time.
- **Config-file fallback in watchdog + telemetry.** Both scripts read the data-source
  config from `config/setup.md` when CLI flags / env are not set.
- **Local ticket/story system (`scripts/ticket.py`).** A built-in, file-based ticket
  base so a vanilla install works with NO external tracker (no Paperclip, no GitHub,
  no Linear). Create work items, track review state, record verdicts. Writes
  `runs/in_review.json` (feeds the watchdog) and `runs/verdicts.jsonl` (feeds
  telemetry), so the whole loop runs out of the box.
- **Wizard questions rewritten in plain language.** Every setup question now reads
  clearly to someone who doesn't know the framework (no jargon like "in_review",
  "verdict ledger", "epic", "autonomy ladder"). The wizard also auto-creates the
  default data files (`runs/in_review.json`, `runs/verdicts.jsonl`).

### Fixed
- `docs/spec-addendum-01.md` — **A16 self-contradiction caught and fixed.** A decision about where validation records live was recorded as DECIDED in `docs/proposals/a17-validation-record-home.md` while §A17 still said "Not decided. Do not implement." — two copies of a governance rule disagreeing, with no precedence rule. This is exactly the A16 open problem, occurring inside the file where A16 is written down. The fix renumbered the validation-record decision as **A20** (decided, distinct from A17), kept A17 open on its actual subject (no project repo for governance-repo work), renamed the proposal file to `a20-validation-record-home.md`, and recorded the occurrence in the A16 section as evidence the duplication problem is real and already biting.

### Added
- `docs/spec-addendum-01.md` — Addendum 01 (Reversibility, Autonomy, Budgets, and Audit), ratified, committed into the repo so the repo copy is canonical and the Downloads copy is dead. Amends Sections 5, 6, 9, 10, 11, 13, 14 of `docs/agentic-governance-spec.md`. A9 and A10 are recorded open problems (not implemented).
- `docs/agentic-governance-spec.md`: added **Section 10.7 Reversibility as the approval line** (A1) — finish reversible work, stage and stop irreversible work; precedence over vetoes/mandatory escalation; adversarial agents unchanged.
- `docs/agentic-governance-spec.md`: added **Section 10.8 The autonomy ladder** (A2) — Levels 0-4, promotion earned on evidence, automatic demotion, config for starting level and clean runs per promotion.
- `docs/agentic-governance-spec.md`: added **Section 10.9 Declared retry budgets** (A3) — target/count/gap/escalation declared before work; bot does not set its own budget; repeated exhaustion is a rule problem.
- `docs/agentic-governance-spec.md`: added **Section 10.10 Cost attribution** (A7) — spend recorded per bot, not only per epic; unattributed spend marked rather than invented.
- `docs/agentic-governance-spec.md`: added **Section 10.11 Failure domains** (A13) — every node has a declared failure policy; never hide missing work; distinguish stalled from failed.
- `docs/agentic-governance-spec.md`: added **Section 10.12 Gates belong in architecture where architecture allows it** (A14) — three protection levels (unreachable/intercepted/instructed); config records which level applies per irreversible action class.
- `docs/agentic-governance-spec.md`: added **Section 13.5 Routine audit** (A4) — weekly receipt, three questions, verifier kill rate per adversary/role, bot is not sole judge of its own history.
- `docs/agentic-governance-spec.md`: **corrected Section 9.4** (A5) — the read-only persona line is documentation, not enforcement; the adversarial commit check is the real control; genuine isolation requires separate credentials.
- `docs/agentic-governance-spec.md`: added **Section 9.6 Config validation** (A8) — wizard validates before writing and refuses on contradictions; validation runs on every run; unvalidatable values stated as such. (Section 9.5, A6 BYOA, is deferred to a later pass.)
- `docs/agentic-governance-spec.md`: added to **Section 14** — **End-to-end validation before further extension** (A11, adoption prerequisite) and **When not to invoke the chain** (A15, adoption note).
- `harnesses/researcher.md`: created the **Research role harness** (A12.3) from the nine-section skeleton — establishes what is true before anyone plans against it; evidence pack to PM; bounded discovery loop; permitted plugins `universal`, `prompt`, `docs`, `researcher`.
- `docs/agentic-governance-spec.md`: added **Section 5.0 Research Harness** (A12) ahead of the PM harness — why the chain needs it, where it sits (CEO → Research → PM → UX → engineer → QA → CEO), the harness, bounded discovery loop, reduce-before-reasoning, degrade visibly, amendments, adversaries already exist.
- `docs/agentic-governance-spec.md`: applied the **A12.7 amendments** — Section 5.1 PM brief fields 3 & 4 must cite a finding from the evidence pack; Section 6 adds the Research edge (Research receives from CEO bot, hands to PM); Section 11 moves `researcher` to the Research role and UX loses read-only researcher access.
- `mcp/adversarial_mcp/setup_wizard.py`: added the **Addendum 01 config questions** (unanswered, operator answers through the wizard) — autonomy starting level + clean runs per promotion (A2), retry count + escalation on exhaustion (A3), audit cadence (A4), research discovery bounds (rounds without findings, round budget) (A12.4), and irreversible-action protection level per class (A14). Written to `config/setup.md`. A6 (BYOA) is deferred to a later pass.
- `docs/agentic-governance-spec.md`: Section 14 now points to `docs/spec-addendum-01.md` for the two recorded open problems (A9 ledger structure/growth, A10 rollback) — named, not resolved.
- `docs/spec-addendum-01.md`: recorded **A16, a third open problem** — harness bodies are duplicated between the spec and the harness files, no precedence rule exists, and the fix is either a precedence rule or generating one from the other. Recorded, not solved.
- `docs/spec-addendum-01.md`: recorded **A17, a fourth open problem** — this repo has no project repo, so every real change targets the governance repo, which bots cannot write; the read-only rule (9.4) and the engineer's obligation (5.3) cannot both hold for governance-repo work. Options: a separate project repo, an exception path with a human applying the change, or scoping the framework to exclude self-modification. Recorded, not solved.
- `docs/spec-addendum-01.md`: added **A18, a decided section** (not an open problem) — (1) acceptance rules need an artifact: every role that can reject upstream work records its acceptance decision (what it received, whether well-formed, why it proceeded despite a defect); (2) adversarial review covers intake, not only output: the Critic checks whether each role received input its harness permits and rejected if not; (3) the CEO harness amendment: turning an objective into a research question means restating a solution-framed objective as a problem, passing it through verbatim is not scoping (applies to Section 10 and A12.2).
- `harnesses/ceo.md` and `docs/agentic-governance-spec.md` (Section 10 + A12.2): amended per A18.3 — the CEO scopes research questions by restating a solution-framed objective as a problem.
- **A18.1 acceptance records** (Phase 1): every role that can reject upstream work now records its acceptance decision in the artifact it produces — what it received, whether it was well-formed against its inputs rule, and if it proceeded despite a defect, why. Added to Research (`evidence.md`), PM (`brief.md`), UX (`rationale.md`), engineer (`notes.md`), QA (`results.md`), and the CEO (calibration ledger, on QA's report). Updated in **both** copies (harnesses/*.md and inline in the spec) and kept byte-identical — 12 places touched (6 roles × 2 copies). The spec's Section 10 CEO harness previously lacked the "Required artifact format" section the harness file has; it was added to match (a pre-existing A16 divergence, not fixed beyond this section).
- `docs/spec-addendum-01.md`: added **A19, a decided boundary rule** — the Section 7 carve-out protects an adversarial agent's identity, not its check list. Identity is what the agent is and what it may never do; a check is what it verifies. Adding/removing/amending a check is procedure (permitted); changing what the agent is, may never do, or its authority to block is identity (forbidden). An amendment requiring rewording the identity section is not procedure.
- **A18.2 intake conformance** (Phase 2): added a fifth check (intake conformance) to all eight Critic files (4 plugin + 4 flat) — reads the acceptance record and asks whether the role received input its harness permits and, if not, whether it rejected. Same mechanical shape as the existing four checks. Flat bodies kept identical to plugin (only `name:` frontmatter differs). Identity sections untouched in all 8 (boundary rule satisfied).
- **Governance setup wizard** (`mcp/adversarial_mcp/setup_wizard.py`): conversational, exposed through the MCP server as `setup_wizard_start` / `setup_wizard_answer` (Section 9.3). Asks the operator's 13 questions natively with labeled options where bounded, writes `config/setup.md` and `config/roster.md`, and generates one persona block per roster row into `config/personas/` (Section 9.4 template). Re-runnable; absent/incomplete config is the unknown state, never defaulted. Built untested per operator instruction (interactive tooling down).
- `docs/agentic-governance-spec.md` — the ratified work order (`agent-harnesses.md`) committed into the repo (including the Section 7 constitutional-content carve-out). From this commit forward the repo copy is canonical; the Downloads copy is dead.
- **Agentic governance restructure** (governance-restructure branch) per ratified `agent-harnesses.md` work order:
  - Repo renamed `adversarial-agents` → `agentic-governance` (GitHub redirect from old name).
  - Governance layout: `constitution/`, `harnesses/`, `ledger/`, `config/`.
  - Five role harness files: `harnesses/pm.md`, `harnesses/ux.md`, `harnesses/engineer.md`, `harnesses/qa.md`, `harnesses/ceo.md` — using the Section 4 skeleton and Sections 5/10 content, with Section 11 plugin allowlists cross-referenced.
  - `config/roster.md` — empty roster table (Section 9.2 columns).
  - `ledger/queue.md` — human queue (Section 13).
  - `docs/communication.md` — communication rules (Section 6).
  - `docs/commit-discipline.md` — commit discipline (Section 8).
  - Constitution relocated `docs/Constitution.md` → `constitution/constitution.md`; calibration ledger `docs/Calibration.md` → `ledger/calibration-ledger.md` (git mv, history preserved); inbound reference in `docs/adr/0004-hard-vetoes.md` updated.
  - `docs/` retained as the in-repo wiki (no separate `wiki/` folder).
- Foundation for GitHub publication: LICENSE (MIT), SECURITY.md, CONTRIBUTING.md,
  AGENTS.md (repo operating rules), CHANGELOG.md, .gitignore.
- AUDIT.md — enterprise gap analysis + roadmap.
- CI validation workflow (`scripts/validate.py` + GitHub Actions) — lints frontmatter,
  checks naming uniqueness, validates structure and cross-references.

### Moved
- `docs/Constitution.md` → `constitution/constitution.md` (git rename).
- `docs/Calibration.md` → `ledger/calibration-ledger.md` (git rename).
- `docs/Vetoes.md` → `constitution/vetoes.md` (git rename). The veto principle is now stated once, in `constitution.md` Rule 1; `vetoes.md` points to Rule 1 and keeps only its unique operational content (domain table, mechanism, mechanical enforcement, rationale). Inbound references updated.
- 12 per-domain constitutions `adversarial-<domain>/references/constitution.md` → `constitution/domains/<domain>.md` (git rename, no rule text changed). Constitutional content moved out of capability folders; `get_constitution` repointed to the new path and verified for all 12 domains.

### Changed
- `docs/adr/0004-hard-vetoes.md`: references updated to `constitution/constitution.md` and `constitution/vetoes.md`.
- `mcp/adversarial_mcp/server.py`: `get_constitution` reads `constitution/domains/<domain>.md`; `REPO_ROOT` now resolves relative to `server.py` (rename/clone-anywhere safe); `get_standard` fixed via glob of exactly one standard file per plugin (was reading nonexistent `references/standard.md` and silently returning empty for all 12 domains since the MCP server shipped 2026-08-26).
- `mcp/adversarial_mcp/server.py`: `run_review` and `record_verdict` now tag verdict-log records with a `source` field (`app` by default; tests pass `source="smoke_test"`); `query_verdicts` gained a `source` filter so test/automation records can be excluded from the real-review log (runs/verdicts.jsonl).
- `mcp/adversarial_mcp/setup_wizard.py`: fixed a bug where the roster never completed — `_is_repeated_pending` compared the `__DONE__` sentinel as a list slice when it is stored as a string, so the roster looped forever and the wizard never finalized. Now compares the stored string correctly; verified end-to-end (writes `config/setup.md`, `config/roster.md`, and one persona block per roster row).
- `scripts/smoke_test_mcp.py`: hardens the MCP smoke test — (1) wired into CI (`.github/workflows/validate.yml` `tests` job); (2) under a Python without `mcp` it now prints a clear message naming the interpreter to use and exits non-zero instead of a raw `ModuleNotFoundError`; (3) `run_review` in the per-domain loop now passes `source="smoke_test"` so its records are filterable, and `query_verdicts` is checked for errors only (an empty verdict history is a valid state).
- `harnesses/ceo.md`: removed the restriction "Read access across everything belongs to the adversarial agents, not to the CEO" from the Inputs section — not in the spec, and the CEO reads the constitution, harness, config, and ledger by definition. The adversarial agents' read access is stated in Section 12 without a counterpart denial here.
- **Migration brief (Section 7):** added carve-out — Phase 3 does not touch `references/constitution.md` in any plugin (constitutional content, not capability).
- **Spec correction:** the Section 4 skeleton lists eight harness sections, but every harness carries a ninth — the Section 11 plugin allowlist. The allowlist is legitimately part of a harness; the spec (not the harnesses) is wrong. Noted for spec fix.

## [0.1.1] — 2026-09-11

### Added
- **Ladders epic retrospectives as SoT** under `projects/ladders/retros/`
  (Paul LOCK 2026-09-11). Filed triad retros for `migration-drift-gate` and
  `marketing-landing` (went well / didn't / improve only). Optional mirrors
  elsewhere OK later; this tree is canonical. Docs only — no framework-policy
  change.

## [0.1.0] — 2026-08-26

### Added
- Five adversarial domain plugins:
  - `adversarial-ux` — user experience (critic, cx-advocate, evaluative-uxr; 10 skills)
  - `adversarial-engineer` — engineering (critic, ops-advocate, reliability-reviewer; 9 skills)
  - `adversarial-qa` — testing/release (critic, quality-advocate, edge-case-reviewer; 8 skills)
  - `adversarial-researcher` — research/evidence (critic, evidence-advocate, context-reviewer; 8 skills)
  - `adversarial-universal` — catch-all (universal-adversary; 6 skills)
- Each plugin: constitution, domain standard, personas, calibration ledger, decision-record
  + calibration-entry templates, commands.
- Consolidated flat layer: 13 namespaced agents + 45 namespaced skills.
- Cursor + Claude Code wiring (agents + skills symlinks).
- Paperclip wiring: 5 adversarial agents + mandatory-review rule in 8 domain agents.

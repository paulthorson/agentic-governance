# Changelog

All notable changes to the Adversarial Agents framework.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
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
- `harnesses/ceo.md`: removed the restriction "Read access across everything belongs to the adversarial agents, not to the CEO" from the Inputs section — not in the spec, and the CEO reads the constitution, harness, config, and ledger by definition. The adversarial agents' read access is stated in Section 12 without a counterpart denial here.
- **Migration brief (Section 7):** added carve-out — Phase 3 does not touch `references/constitution.md` in any plugin (constitutional content, not capability).
- **Spec correction:** the Section 4 skeleton lists eight harness sections, but every harness carries a ninth — the Section 11 plugin allowlist. The allowlist is legitimately part of a harness; the spec (not the harnesses) is wrong. Noted for spec fix.

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

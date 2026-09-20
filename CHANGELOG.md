# Changelog

All notable changes to Agentic Governance.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Product-facing notes for human visitors. Agent/ops scar and SoT narrative that
formerly lived here is archived at
[`docs/improve/changelog-ops-unreleased.md`](docs/improve/changelog-ops-unreleased.md).

### Added

- Framework technical writing skill for public git docs
  (`skills/doc-framework-technical-writing/`).
- External side-effect go-gate: messaging egress only when network permission
  allows, with a documented Quality check path.
- Chief of Staff memory seating at install when Cos is on the roster
  (`docs/onboarding/cos-seating.md`, wizard ASK + scaffold).
- Continuous improve reporting under `docs/improve/` (daily digests the
  optional localhost dashboard can surface).
- Localhost `dashboard/` app for operator/dev — not required to use the
  framework; marketing face lives in the separate site repo.
- Governance setup wizard via MCP (`setup_wizard_start` /
  `setup_wizard_answer`) writing roster and persona config.
- Local file-based ticket/story helper (`scripts/ticket.py`).

### Changed

- Localhost dashboard admin uses a localhost Host gate only; remote identity
  login is removed (fail closed off-box).
- Root README Install section rewritten as a stranger-facing clone → MCP →
  wizard guide (no private-repo HOLD voice; Cos seating detail linked from
  onboarding docs).
- Root license is Apache License 2.0 (see `LICENSE` and `NOTICE`).
- Setup wizard questions rewritten in plain language; data-source and network
  permission questions included.
- Framework restructure: shared `constitution/` + `harnesses/` + MCP engine
  alongside domain plugins.

### Fixed

- MCP `get_standard` / `get_constitution` path resolution for domain plugins.
- Setup wizard roster completion so finalize can write config.

### Removed

- [redacted] Get AG/outline documents. Settled posture: free/open
  source under Apache-2.0; LICENSE is the only use governor.

## [0.1.1] — 2026-09-11

### Added
- **Product-seat epic retrospectives as SoT** (path on product brief — OUT of
  AG framework repo; was under `projects/ladders/retros/` — tree removed from
  tip). Operator LOCK 2026-09-11. Filed triad retros for `migration-drift-gate` and
  `marketing-landing` (went well / didn't / improve only). Optional mirrors
  elsewhere OK later. Docs only — no framework-policy
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

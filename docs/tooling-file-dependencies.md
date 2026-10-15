# Tooling File Dependencies

Inventory of every file path the tooling reads at runtime, and which tool
depends on it. Purpose: **read-before-strip**. During the Phase 3 migration,
if the migration would move or remove content from a file on this list, flag
it and stop rather than executing. Discovering breakages one at a time is the
expensive way.

Paths are relative to the repo root unless absolute. Verified against the
current tree on `governance-restructure` (2026-09-04).

---

## MCP server — `mcp/adversarial_mcp/server.py`

All reads go through `_read()` (returns `""` on missing) unless noted. `REPO_ROOT`
resolves from the file's own location; `DOMAIN_DIR[domain] = REPO_ROOT/adversarial-<domain>`.

| Path read | Reader | Depends on it | Notes |
|---|---|---|---|
| `constitution/domains/<domain>.md` | `_constitution(domain)` | `get_constitution`, `run_review`, `run_review_deep` | Relocated here from the per-plugin `references/` folder before 1.0. **Do not strip.**
| `adversarial-<domain>/references/*.md` (the single standard file) | `_standard(domain)` (glob, excludes `calibration-ledger.md`/`personas.md`) | `get_standard`, `run_review_deep` | Domain-specific names (`qa-standard.md`, `design.md`, …). Exactly-one-match enforced.
| `adversarial-<domain>/references/personas.md` | `_personas(domain)` | (review context) | 
| `adversarial-<domain>/references/calibration-ledger.md` | `_ledger(domain)` | (ledger read) | 
| `adversarial-<domain>/agents/*.md` | `_agents_for(domain)` | `list_agents`, `get_agent`, `run_review`, `run_review_deep`, `framework_status` | **Capability + identity live here.** Migration target — strip identity, keep capability.
| `adversarial-<domain>/skills/*/SKILL.md` | `_skills_for(domain)` | `list_skills`, `framework_status` | **Capability + identity live here.** Migration target.
| `runs/verdicts.jsonl` | `_append_verdict`, `_load_verdicts` | `record_verdict`, `query_verdicts`, `framework_status` | Append-only verdict log (gitignored).
| `config/wizard-state.json` | `setup_wizard` module | `setup_wizard_start`, `setup_wizard_answer` | Wizard resumability; absent = unknown state.
| `config/setup.md`, `config/roster.md`, `config/personas/*.md` | `setup_wizard` module | written on wizard completion | Read by bots (persona blocks point to them); not read by server.py directly.

## Scripts — `scripts/`

| Path read | Script | Depends on it | Notes |
|---|---|---|---|
| `runs/verdicts.jsonl` | `calibration-report.py` | Calibration report | Same log as MCP.
| `runs/stuck-watchdog.json` | `stuck-review-watchdog.py` | Stuck-review state | `STUCK_STATE_FILE` override.
| company ticket dirs | `stuck-review-watchdog.py` | Watchdog | Reads external ticket dirs.
| Every plugin: `agents/*.md`, `skills/*/SKILL.md`, `references/` (`calibration-ledger.md`, `personas.md`), `assets/templates/`, `commands/`; `constitution/domains/<domain>.md`; flat `agents/` + `skills/` | `validate.py` | CI structure validation | Reads the per-domain constitution from `constitution/domains/` and fails on any file that still names the retired per-plugin path. Hardcoded default `--root <framework-root>`.

## Write-only (not reads) — noted for awareness

- `scripts/gen-plugin.py` — scaffolds new plugins. Writes the new domain's constitution to `constitution/domains/<domain>.md` and only the standard to the plugin's `references/`, so it does not recreate the duplicate-constitution pattern.
- `scripts/consolidate-adversarial.py` — regenerates the flat `agents/` + `skills/` layer from the plugins. `--check` (run in CI) fails on drift.

---

## Read-before-strip flags (stop-and-check before migrating these)

1. **`validate.py`** reads `constitution/domains/<domain>.md` (fixed; it used to require the retired per-plugin copy). It is a consumer, not migrated content.
2. `adversarial-<domain>/agents/*.md` and `skills/*/SKILL.md` are read **and** are migration targets. Stripping must remove only identity lines, never capability — otherwise `_agents_for`/`_skills_for` and `list_agents`/`list_skills`/`run_review`/`run_review_deep`/`framework_status` lose content.
3. `constitution/domains/*.md` and the per-plugin standard files are constitutional content — on the carve-out, not migration targets.

*Companion: `docs/agentic-governance-spec.md`, Section 7 (migration brief) + the constitutional-content carve-out.*

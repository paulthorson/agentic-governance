# Tooling

The scripts and CI that keep the framework from decaying.

## `scripts/validate.py`

The structure validator. Checks:

- All 5 plugin folders exist with the required skeleton (agents/, skills/,
  references/, commands/, assets/templates/).
- Every agent and skill has valid frontmatter.
- Flat-layer names are namespaced by domain (no collisions).
- References files (constitution, standard, personas, calibration-ledger)
  exist per plugin.

Run locally:

```bash
python3 scripts/validate.py
```

## CI workflow (`.github/workflows/validate.yml`)

Runs on push to `main` and pull requests:

1. **Structure validation** — `python3 scripts/validate.py --root.`
2. **Secret scan** — `gitleaks` (blocks accidental credential commits)

## `scripts/consolidate-adversarial.py`

Rebuilds the flat namespaced `agents/` and `skills/` layers from the plugin
folders: adds the domain prefix to each `name:` and re-points relative paths
so they resolve from the flat location. Writes nothing outside the repo.
Idempotent. Run after editing any plugin:

```bash
python3 scripts/consolidate-adversarial.py          # rebuild
python3 scripts/consolidate-adversarial.py --check  # CI: fail on drift
```

## `scripts/check-doc-refs.py`

Checks every tracked markdown file for paths that point at nothing: `scripts/`
mentions that do not exist, `../` harness paths that do not resolve, relative
links to missing files, and any use of the retired per-plugin constitution
path. Runs in CI on every PR.

```bash
python3 scripts/check-doc-refs.py
```

## `scripts/stuck-review-watchdog.py`

Detects `in_review` tickets that have been sitting without a verdict past the
staleness threshold (default 120 min) — the assigned adversary is down, paused,
or stalled. Alerts via Discord with dedupe state. Wired into a 30-min cron.

```bash
python3 scripts/stuck-review-watchdog.py --stale-minutes 120 --dry-run
```

## `scripts/gen-plugin.py`

Generates a new adversarial plugin from a spec (domain, prefix, agent name,
checks, skills, veto keywords, personas). Reusable — creates the full plugin
structure mirroring the existing plugins. Used to build the security, privacy,
compliance, and product plugins.

```bash
python3 scripts/gen-plugin.py <domain> <prefix> <agent> --title. --desc. \
  --checks "." --skills "." --veto "." --personas "."
```

## `mcp/`

The MCP server (see [[MCP]]). Managed with `uv`; pinned to `mcp<2`.

## See also

- [[Architecture]] · [[Calibration]] · [[MCP]] · [[Roadmap]]

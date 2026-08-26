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
folders and re-symlinks them into Cursor (`~/.cursor/`) and Claude
(`~/.claude/`). Idempotent. Run after editing any plugin:

```bash
python3 scripts/consolidate-adversarial.py
```

## `mcp/`

The MCP server (see [[MCP]]). Managed with `uv`; pinned to `mcp<2`.

## See also

- [[Architecture]] · [[Calibration]] · [[MCP]] · [[Roadmap]]

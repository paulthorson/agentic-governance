# Adversarial Agents

Consolidated root for all the assistant adversarial agents and skills. Referenceable from both
**Cursor** and **Claude Code** for agents and skills.

## What's here

Five adversarial frameworks, each a self-contained plugin folder plus a flat, namespaced
consumption layer:

| Plugin | Domain | Reviews | Veto |
|---|---|---|---|
| `adversarial-ux` | User experience (designs, HUD, voice, personas) | UXer, UX Researcher | User harm |
| `adversarial-engineer` | Engineering (code, architecture, config, infra) | Engineer | Production harm |
| `adversarial-qa` | Testing, acceptance criteria, release gates | QA | User harm |
| `adversarial-researcher` | Research, synthesis, evidence | general research | Unsupported claims |
| `adversarial-universal` | Catch-all (any domain) | PM, BA, Scrum, CEO, anything | Irrecoverable harm |

## Structure

```
~/adversarial-agents/
├── <plugin>/ # self-contained plugin (agents/, skills/, references/, commands/)
├── agents/ # FLAT namespaced agents, e.g. eng-critic.md, ux-cx-advocate.md
└── skills/ # FLAT namespaced skills, e.g. eng-system-map/, ux-altitude-check/
```

Namespacing (`eng-`, `qa-`, `res-`, `ux-`, `univ-`) prevents collisions between domains — every
plugin has a `critic` and an `altitude-check`, so the flat layer disambiguates them.

## Reference into Cursor

Agents and skills are already symlinked into:

- `~/.cursor/agents/` → `eng-critic.md`, `ux-cx-advocate.md`,. (13 agents)
- `~/.cursor/skills/` → `eng-system-map/`, `ux-altitude-check/`,. (45 skills)

Cursor picks these up automatically from `.cursor/agents` and `.cursor/skills`.

## Reference into Claude

Agents and skills are already symlinked into:

- `~/.claude/agents/` → the 13 namespaced agent files
- `~/.claude/skills/` → the 45 namespaced skill folders

Claude Code loads agents from `~/.claude/agents/*.md` and skills from `~/.claude/skills/*/SKILL.md`.

## Re-wiring after edits

The plugin folders under `~/adversarial-agents/<plugin>/` are the source of truth. If you edit
them, the flat `agents/` and `skills/` copies (and the Cursor/Claude symlinks) point at the
namespaced copies, not the plugin originals — so to propagate an edit, re-run:

```
python3 /tmp/consolidate-adversarial.py
```

(or the canonical script at `the operator's local config/workspace/scripts/consolidate-adversarial.py` if you
moved it there). This rebuilds the flat layer from the plugin folders and re-symlinks into
Cursor and Claude.

## Each plugin's internal layout (mirrors adversarial-ux)

```
<plugin>/
├──.claude-plugin/plugin.json
├── agents/ the standing adversary agents (with YAML frontmatter)
├── skills/ the worker skill + stateless skills (each a SKILL.md)
├── references/ constitution.md, <domain>-standard.md, personas.md, calibration-ledger.md
├── assets/templates/ decision-record.md, calibration-entry.md
└── commands/ the loop + review commands
```

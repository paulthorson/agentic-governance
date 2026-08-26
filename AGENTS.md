# AGENTS.md — Operating Instructions for Any Agent in This Repo

This file tells agents (and humans) how to work correctly inside the Adversarial Agents repo.
Read it before making changes.

## What this repo is

A set of **governed adversarial review frameworks**. Each plugin folder is a self-contained
loop: a worker skill produces work, adversary agents judge it blind, a constitution gates it,
and only a human clears a veto. The same loop is exposed to Cursor, Claude Code, Paperclip, and
(via the MCP server) any MCP-capable client.

## Ground rules for agents working here

1. **Never break the blind-review isolation.** The advocate agents must review neutral facts
   only — never the worker's rationale. Do not "helpfully" leak the worker's pitch into a
   `facts.md`. That is the single most important invariant in the whole system.
2. **Never edit a constitution or a calibration ledger to clear a veto.** Only a human edits
   `references/constitution.md`. Vetoes are cleared by a named human arbiter, written into the
   decision record.
3. **Keep the record append-only.** `decision-record.md` is never edited after commit;
   corrections are new appended entries referencing the old one.
4. **Namespacing is required.** Every agent and skill in the flat `agents/` and `skills/`
   layers is prefixed with its domain (`ux-`, `eng-`, `qa-`, `res-`, `univ-`). Do not create
   un-namespaced files — they would collide (every plugin has a `critic` and `altitude-check`).
5. **Frontmatter is the contract.** Every agent `.md` and every `SKILL.md` must carry a
   `name:` frontmatter field that matches its namespaced filename/skill. Cursor and Claude
   register agents/skills from this. A mismatched `name:` means the agent won't load.
6. **The plugin folders are the source of truth.** `~/adversarial-agents/<plugin>/` holds the
   canonical content. The flat `agents/` + `skills/` are generated copies. After editing a
   plugin, re-run `scripts/consolidate-adversarial.py` to rebuild + re-symlink into Cursor and
   Claude.
7. **Cross-domain checks come from `shared/`.** Prompt-injection, security, privacy,
   supply-chain, performance, and accessibility checks live in `shared/skills/` and are
   referenced by reviewers, not duplicated per plugin.
8. **Wiki + ADRs are authoritative.** Architecture decisions are recorded in `docs/adr/`.
   Read the relevant ADR before changing structure.

## The 5 canonical domains

| Domain | Plugin | Agents | Veto |
|---|---|---|---|
| UX | `adversarial-ux` | critic, cx-advocate, evaluative-uxr | user harm |
| Engineering | `adversarial-engineer` | critic, ops-advocate, reliability-reviewer | production harm |
| QA | `adversarial-qa` | critic, quality-advocate, edge-case-reviewer | user harm |
| Research | `adversarial-researcher` | critic, evidence-advocate, context-reviewer | unsupported claims |
| Universal | `adversarial-universal` | universal-adversary | irrecoverable harm |

## Adding a new domain

1. Copy the pattern from an existing plugin (`adversarial-qa` is the cleanest template).
2. Give it a constitution, a standard, 2–3 agents (one is the veto-holding advocate), personas,
   a calibration ledger, a decision-record template, commands, and at least the core skills.
3. Reuse `shared/skills/` for cross-cutting checks instead of duplicating.
4. Add the domain prefix to the consolidation map and re-run `consolidate-adversarial.py`.
5. Add a `docs/` page and an ADR for the new domain.
6. Wire it into Paperclip (routing) if it should participate in the mandatory-review loop.

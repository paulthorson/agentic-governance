# Cos memory store (operator template)

**Status:** **LIVE** — Cos ACCEPT merged [#64](https://github.com/paulthorson/agentic-governance/pull/64) @ `a9a4327`. Soft / tip-only use as AG law = **REJECTED**. Install ASK at Cos seating remains `private_git` OR `local_folder` (do not force one).

## Purpose

Give Cos operators a **private structured memory store** for Cos↔human locks and episodes — not only chat context. Copy this folder into private storage you control. Fill it as you work. It is a baked-in operator template, not a product feature.

## Paul + Cos clarified store

**Paul+Cos operator memory = private git.** That is the clarified store for Paul and Cos themselves (versioned private repo — not public AG product surface).

This is a **clarification of Paul+Cos’s own store**, not a framework-wide forced default for every install.

## Framework setup flow (ASK at Cos seating — not deferred)

**Part of AG install/setup when Chief of Staff is seated — not a later optional README-only step.**

The conversational setup wizard (`mcp/adversarial_mcp/setup_wizard.py`, MCP tools `setup_wizard_start` / `setup_wizard_answer`) asks Cos memory mode **immediately after the roster** whenever a `cos` row is present. Finalize **must call** the seating hook [`mcp/adversarial_mcp/cos_memory_setup.py`](../../mcp/adversarial_mcp/cos_memory_setup.py) `apply_at_cos_seating` (CLI stub: [`scripts/cos_memory_setup.py`](../../scripts/cos_memory_setup.py)). Answers land in `config/setup.md`; skeleton is scaffolded to `config/cos-memory/` (gitignored). This template remains the skeleton SoT.

See also: [`docs/onboarding/cos-seating.md`](../onboarding/cos-seating.md).

At seating, **framework Cos ASKS the operator** which path to use. The skeleton supports **either**. **Do not** force one option in the framework template or wizard.

| Path | Wizard option | When |
|---|---|---|
| **A — Private git repo** | `private_git` | Operator wants versioned history / sync (same shape as Paul+Cos clarified store) |
| **B — Local folder** | `local_folder` | On-machine install; operator wants a simple private directory |

Record the chosen path in `profile.md` / `STORAGE_MODE.md` (mode + non-secret label only — **no** absolute host paths, emails, or tokens).

## Private ≠ public

| This template | Public AG product surface |
|---|---|
| Cos operator working memory | Marketing site, dashboard chrome, Get AG, living board |
| Private git (Paul+Cos clarified) **or** operator-chosen private git / local folder | `paulthorson/agentic-governance` public tree / site repo |
| Locks, episodes, Cos↔human decisions | Public product copy, screens, stills |

**Do not** commit a filled memory store into public AG git. Ship only this empty template under `docs/templates/cos-memory/`. Filled stores stay private.

## How to use — Path A (private git)

1. Create or open a **private** git repo (not the public AG product repo).
2. Copy this template directory into that repo (or use the seating scaffold from `config/cos-memory/`).
3. Commit skeleton files; append locks/episodes as usual.
4. Point Cos at the private repo (operator notes only — not public product docs).

## How to use — Path B (local folder)

1. Create a **local** private folder on the machine (on-machine install).
2. Copy this template directory into that folder (or keep the seating scaffold under `config/cos-memory/`).
3. Edit skeletons in place; no git required.
4. Point Cos at the folder via operator notes (relative/private label only — **no** absolute host paths in public AG).

## Shared rules (both paths)

1. Keep filenames stable (`profile.md`, `locks.md`, `log.md`, `log/`) so Cos can find them.
2. Append; do not rewrite history of accepted locks without a new dated entry.
3. Soft / tip-only as AG law = **REJECTED**. Template remains **DRAFT** until Cos ACCEPT of the shipping tip.

## What belongs

- Standing Cos operator **profile / prefs** (`profile.md`) — including chosen storage mode (A or B)
- **Paul/Cos LOCKs** with date + plain text (`locks.md`)
- **Episodes** — Cos↔human decisions, ACCEPT/HOLD outcomes, named SoT lines (`log.md` and/or `log/`)

## What does NOT belong

- Public product chrome, marketing copy, or Class B look/stills
- Secrets, API keys, tokens, passwords
- Emails, account names, or other PII dumps
- Absolute host paths
- private operator data
- A framework-forced “must use git” or “must use local” rule (Paul+Cos clarified store ≠ force-all-operators)

**P0:** Examples in this template stay scrubbed. Soft “put everything in memory” = **REJECTED**.

## Skeleton map

| File | Role |
|---|---|
| `profile.md` | Standing Cos operator profile / prefs + storage mode (A or B) |
| `locks.md` | Paul/Cos LOCKs — date + plain text |
| `log.md` | Append-only episode index / short log |
| `log/` | Optional dated episode files (`YYYY-MM-DD-slug.md`) |

Adv may name a check/lock id later. Until Cos ACCEPT, treat this as draft template only.

# Scar — OpenClaw silent version drift (pin-enforce)

**Project:** OpenClaw 
**Filed:** 2026-09-11 (Standing AG — anonymized process lock) 
**Status:** CLOSED 
**Kind:** harness scar / runtime pin lock 
**Artifacts (local, not in this repo):** pin file under OpenClaw config pins dir; pin-enforce script; periodic LaunchAgent enforcer 

## Symptom

Overnight the global OpenClaw package drifted below the declared pin (example: `2026.9.3` → `2026.9.2`). Runtime state stayed on a newer schema while the CLI build supported an older one → `SqliteSchemaVersionError` on next CLI/TUI touch. Gateway process could keep an in-memory older-good version, so the failure looked intermittent / “silent” until a fresh CLI path hit the DB.

## Root cause

A nightly “system & OpenClaw update” job still ran package-manager global update (`npm update -g openclaw`), fighting the declared version pin. Pin without enforcement (and with an updater that ignores it) is not a lock.

## Fix (process lock — keep named)

1. **Nightly no longer package-updates OpenClaw.** Update job calls pin-enforce only; intentional upgrades are explicit Eng work, not cron drift.
2. **Pin file** records `MIN_VERSION` (locked example: `2026.9.3` / schema 16).
3. **Periodic enforcer** (LaunchAgent ~every 30m) checks installed version vs pin and restores/alerts on drift — not wait-for-morning.

## AG implication (Adv gate)

Any AG framework/process change that **assumes pin-stable OpenClaw** without **naming this lock and check** → Adv **FAIL**. Evidence that the scar is CLOSED does not waive naming the control in the proposal.

## What went well

- Fast restore to pinned version once drift was seen
- Root cause traced to updater-vs-pin, not “DB clobber”
- Standing AG allowlist path for anonymized scars/locks (no private operator data dump)

## What didn't

- Declared pin without killing the updater = false safety
- Overnight silent drift; discovery lagged until CLI error
- Legacy nightly script outlived the pin decision

## What to improve

- Treat **pin + enforcer + no-auto-update** as one three-part lock (document all three)
- Any future OpenClaw version bump: Eng changes pin intentionally; cron never invents upgrades
- AG proposals that depend on Studio OpenClaw stability must cite this scar/lock before Cos→human ACCEPT

## P0 boundary (do not re-break)

Do **not** file into agentic-governance: PII, secrets/tokens, private config, machine identifiers, or private operator data paths beyond the anonymized process names above.

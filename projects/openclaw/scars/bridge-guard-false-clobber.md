# Scar — Bridge-guard false clobber (Claude config byte drift)

**Project:** OpenClaw 
**Filed:** 2026-09-11 (Standing AG — anonymized process lock) 
**Status:** CLOSED 
**Kind:** harness scar / guard false-positive 
**Studio cite:** hash `b7bf3b5ea310ffaf` 

## Symptom

Periodic bridge guard (~every 5m) Discord-alerted “config clobber” and restored **all** watched files after the desktop MCP host rewrote its MCP config. Bridge runtime `.mjs` were unchanged; handshake still succeeded. Repeated false alarms same day and prior day.

## Root cause

Guard treated **whole-file byte equality** of the desktop MCP config vs a stale known-good snapshot as a clobber signal. Any rewrite of sibling servers / preferences flipped a shared “changed” flag, then restore-all rewrote bridge `.mjs` too. Byte-exact config snapshots ≠ structural health of the one bridge MCP entry.

## Fix (process lock — keep named)

1. **Per-file `.mjs` restore** — only restore bridge `.mjs` that actually differ from known-good; never cascade from desktop MCP config drift.
2. **Structural check only** for desktop MCP config — require `mcpServers["openclaw-bridge"]` present with non-empty command and args whose path ends in the bridge `server.mjs`. Ignore sibling servers and other top-level keys. No whole-file byte compare as alert/restore trigger.
3. **Surgical repair** — if the bridge entry is missing/broken, merge-replace **only** that entry from a small entry template (command/args shape; no secret env). Preserve other MCP servers.
4. **Known-good refresh** — refresh `.mjs` known-good after intentional Eng edits + handshake OK; optional full desktop-config snapshot refresh after structural PASS (does not gate alerts). Authoritative expected entry is the entry template, not the full desktop config file.
5. **Discord policy** — alert on real `.mjs` drift, bridge-entry repair failure, or handshake ≥2 consecutive fails. **No** Discord for desktop-config byte drift when the bridge entry structurally PASSes.

## AG implication (Adv gate)

Any AG process lock that assumes **byte-exact config snapshots** without a **structural vs content** distinction → Adv **FAIL** before Cos→human ACCEPT. Cite this scar.

## What went well

- Handshake strike logic already avoided auth false positives
- Fix verified live: `.mjs` OK + structural entry OK + handshake OK on subsequent guard runs

## What didn't

- Shared changed-flag + restore-all coupled unrelated files
- Stale full-file known-good fought a living desktop config

## What to improve

- Guards that watch multi-tenant config files must name the **entry** they protect, not the whole blob
- Separate “snapshot for last-resort restore” from “oracle for alerts”

## P0 boundary

Do **not** file into agentic-governance: secrets/tokens, usernames, absolute host paths, machine ids, channel ids, or private operator data beyond anonymized process names above.

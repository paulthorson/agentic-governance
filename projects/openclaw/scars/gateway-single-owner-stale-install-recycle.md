# Scar — Gateway single-owner + stale-install recycle

**Project:** OpenClaw 
**Filed:** 2026-09-15 (Standing AG — anonymized process lock) 
**Status:** CLOSED (Studio gate live; residual unpaid below) 
**Kind:** harness scar / gateway ops self-heal 
**Family:** Standing AG self-heal (pin-enforce / bridge-guard / cite-or-blank) 
**Lock names:** `GATEWAY_SINGLE_OWNER` + `STALE_INSTALL_RECYCLE` 
**Check / sensor:** gateway-health-guard–style cron (scheduled) — fail-closed before Discord/alert 
**Metric:** competing gateway process count = **0** (hold) while LaunchAgent loaded 
**Scope:** OpenClaw Studio gateway ops only (explicitly **not** product UX Check 7 / Check 8)

## Symptom

Operator send failed with `UNAVAILABLE` — running Gateway could no longer load part of its OpenClaw installation (install changed under a long-lived PID). Recycle attempts spawned a competing gateway run while LaunchAgent still owned the port/state → port in use + another gateway already owns this state directory refusing ready → clients stuck on gateway starting.

## Root cause

1. **Dual owner:** LaunchAgent vs ad-hoc gateway run/restart races.
2. **Stale process:** live PID older than on-disk install after package/plugin updates.
3. **Firefight without fail-closed sensor** → repeated ops mistakes.

## Fix (process lock — keep named; LIVE in Studio)

1. **`GATEWAY_SINGLE_OWNER`** — only LaunchAgent owns Studio gateway; kill competing gateway node processes; never use competing `gateway run` when LaunchAgent is loaded.
2. **`STALE_INSTALL_RECYCLE`** — detect install-changed `UNAVAILABLE` / dist newer than process; one `launchctl kickstart -k` of the LaunchAgent; require prove-handshake PASS; Discord/alert only after **2** handshake fails.
3. **Sensor** — gateway-health-guard–style cron (scheduled). Soft / tip / wiki-scar-only ≠ sensor.

## Done-when / metric

- Competing gateway process count = **0** hold while LaunchAgent loaded.
- After install drift, handshake PASS within one recycle (alert ≤ once per dual-fail).
- Adv **FAIL** if later recycle omits naming LaunchAgent as sole owner.

## AG implication (Adv gate)

Any later AG / OpenClaw ops lock that recycles Studio gateway without naming **`GATEWAY_SINGLE_OWNER`** (LaunchAgent sole owner) + **`STALE_INSTALL_RECYCLE`** + the scheduled sensor → Adv **FAIL** before Cos→human ACCEPT. Evidence that this scar is CLOSED does not waive naming the controls.

## What went well

- Dual-owner race named (LaunchAgent vs ad-hoc) instead of treating “port in use” as noise
- Stale-install recycle tied to handshake prove, not blind restart loops
- Alert deferred until dual handshake fail (noise control)

## What didn't

- Long-lived PID + on-disk install drift produced `UNAVAILABLE` without a fail-closed sensor
- Firefight restarts created a second owner while LaunchAgent still held port/state

## What to improve (unpaid — do not drop)

Bare session keys under explicit ownership need owner mapping without hand-editing gateway JSON (owner-guard script only). **Not** part of this scar’s done-when.

## P0 boundary

Do **not** file into agentic-governance: secrets/tokens, emails, Discord channel names, absolute host home paths that identify a machine user (LaunchAgent label OK), or private operator data beyond the anonymized lock/sensor names above.

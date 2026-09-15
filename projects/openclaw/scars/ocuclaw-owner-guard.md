# Scar — ocuclaw-owner-guard (bare session keys under explicit ownership)

**Project:** OpenClaw 
**Filed:** 2026-09-15 (Standing AG — anonymized process lock) 
**Status:** CLOSED (Studio gate live) 
**Kind:** harness scar / session ops self-heal 
**Family:** Standing AG self-heal (pin-enforce / bridge-guard / cite-or-blank / gateway-single-owner [#65](https://github.com/paulthorson/agentic-governance/pull/65) / question-wait-guard [#66](https://github.com/paulthorson/agentic-governance/pull/66)) 
**Lock name:** `OCUCLAW_OWNER_GUARD` — supersedes unpaid prose id `OCUCLAW_OWNER_PREFIX` (same residual; naming drift closed). `OCUCLAW_OWNER_GUARD` is the only live lock name. 
**Check / sensor:** `scripts/ocuclaw-owner-guard` + OpenClaw cron every 2 min (Studio land-complete 2026-09-15) 
**Metric:** bare ocuclaw / even-ai session keys remapped each cron tick; `defaultAgent` stays `main`; zero `openclaw.json` hand-edits for this fix = **0** hold 
**Scope:** OpenClaw Studio OcuClaw / relay sessions only (explicitly **not** product UX Check 7 / Check 8 / Check 9)

## Symptom

With `agents.ownership=explicit` and multiple agents (`main`, `ba`), bare session keys such as `ocuclaw:even-ai` (and related even-ai forms) are rejected: no explicit owner. Phone / relay UX fails or loops while the gateway stays otherwise healthy.

## Root cause

1. OcuClaw / relay clients historically used bare `ocuclaw:…` keys.
2. Hand-editing gateway JSON to force defaults was forbidden (P0 / dual-run family).
3. Guard script existed but was not on a standing cron → mapping drifted until manual runs.

## Fix (process lock — keep named; LIVE in Studio)

1. **`OCUCLAW_OWNER_GUARD`** — reassert ocuclaw-settings `defaultAgent=main`; map bare session keys matching `ocuclaw:` / `evenai:` / `even-ai:` to `main` in session-agents / display-toggles / stable-prompts; **skip** keys already `agent:`-prefixed.
2. **Sensor** — `scripts/ocuclaw-owner-guard` + cron every 2 min. Soft / tip / wiki-scar-only ≠ sensor.
3. **Hard rule:** NEVER hand-edit `openclaw.json` (schema rejects; dual-run FAIL / config clobber family). Dual-run FAIL. No gateway JSON hand-edit for this.

## Done-when / metric

- Bare ocuclaw / even-ai keys remapped each cron tick = **0** hold.
- ocuclaw-settings `defaultAgent` stays `main`.
- Zero `openclaw.json` hand-edits for this fix.
- Adv **FAIL** if later AG recommends editing `openclaw.json` `agents.entries` defaults instead of naming this guard + scheduled sensor.

## AG implication (Adv gate)

Any later AG / OpenClaw ops lock that treats bare OcuClaw / even-ai session keys under `agents.ownership=explicit` as safe by hand-editing `openclaw.json` `agents.entries` defaults — instead of naming **`OCUCLAW_OWNER_GUARD`** + `scripts/ocuclaw-owner-guard` + the scheduled sensor → Adv **FAIL** before Cos→human ACCEPT. Evidence that this scar is CLOSED does not waive naming the control.

## What went well

- Bare-key rejection named as ownership mapping, not gateway health
- Mapping confined to bare `ocuclaw:` / `evenai:` / `even-ai:` forms; `agent:`-prefixed keys skipped
- Hard rule against `openclaw.json` hand-edit kept (schema / dual-run / clobber family)

## What didn't

- Guard script without standing cron allowed mapping to drift until manual runs
- Firefight / one-shot remap recovered once without a recurring sensor

## What to improve (unpaid — do not drop)

None for this residual — closes the unpaid owner-guard pointer from question-wait-guard ([#66](https://github.com/paulthorson/agentic-governance/pull/66)). Gateway-single-owner ([#65](https://github.com/paulthorson/agentic-governance/pull/65) @ `bb60bb3`) and question-wait-guard ([#66](https://github.com/paulthorson/agentic-governance/pull/66) @ `c70425e`) LIVE separate. **Not** part of those scars’ done-when; this scar pays the residual.

## P0 boundary

Do **not** file into agentic-governance: secrets/tokens, emails, Discord channel names, absolute host home paths that identify a machine user, Notion workspace IDs, cron UUIDs, or private operator data beyond the anonymized lock/sensor names above. Script path may be named as `scripts/ocuclaw-owner-guard` (generic).

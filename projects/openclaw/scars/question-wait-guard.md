# Scar — question-wait-guard (main blocked on secret/question UX)

**Project:** OpenClaw 
**Filed:** 2026-09-15 (Standing AG — anonymized process lock) 
**Status:** CLOSED (Studio gate live; residual paid by [ocuclaw-owner-guard.md](ocuclaw-owner-guard.md)) 
**Kind:** harness scar / session ops self-heal 
**Family:** Standing AG self-heal (pin-enforce / bridge-guard / cite-or-blank / gateway-single-owner [#65](https://github.com/paulthorson/agentic-governance/pull/65)) 
**Lock name:** `QUESTION_WAIT_GUARD` 
**Check / sensor:** question-wait-guard script + cron every 2 min — fail-closed earlier than the default gateway question timeout 
**Metric:** main session `blocked_tool_call` hangs ≥120s without auto-abort = **0** hold 
**Scope:** OpenClaw Studio session `agent:main:main` only (explicitly **not** product UX Check 7 / Check 8)

## Symptom

Operator main session hung repeatedly while a tool wait sat on `question.waitAnswer` — typically a masked-token / secret prompt with no usable timeout UX. Gateway stayed healthy; session showed stalled `blocked_tool_call` for many minutes until manual `chat.abort`. Default gateway question timeout is 15 minutes — too long for the primary interactive session.

## Root cause

1. Secret / human-input tools block the main session indefinitely (or for up to 15m).
2. No fail-closed sensor aborted `blocked_tool_call` early.
3. Firefight aborts recovered once but did not prevent recurrence.

## Fix (process lock — keep named; LIVE in Studio)

1. **`QUESTION_WAIT_GUARD`** — if `agent:main:main` is `state=processing` with `blocked_tool_call` and age ≥ 120s, call `chat.abort` on that session. Alert only on a real abort or after **2** failed abort attempts (not on no-op).
2. **Sensor** — question-wait-guard script + cron every 2 min. Soft / tip / wiki-scar-only ≠ sensor.
3. **Dual-run FAIL.** No gateway JSON hand-edit for this.

## Policy lock (Cos)

Masked-token / secret prompts **MUST NOT** block `agent:main:main`. Use credential file / non-main session / short-timeout UX. Sensor fails closed earlier than the 15m default.

## Done-when / metric

- Main session `blocked_tool_call` hangs ≥120s without auto-abort = **0** hold.
- Alert only on real abort or ×2 abort failure (not on no-op).
- Adv **FAIL** if later AG assumes secret prompts on main are safe without naming this guard + policy.

## AG implication (Adv gate)

Any later AG / OpenClaw ops lock that treats secret / masked-token prompts on `agent:main:main` as safe without naming **`QUESTION_WAIT_GUARD`** + this Cos policy + the scheduled sensor → Adv **FAIL** before Cos→human ACCEPT. Evidence that this scar is CLOSED does not waive naming the control.

## What went well

- Hang named as main-session question wait, not gateway health
- Abort gated at 120s (fail-closed before 15m default)
- Alert deferred until real abort or dual abort failure (noise control)

## What didn't

- Default 15m question timeout left primary interactive session unusable
- Firefight `chat.abort` recovered once without a recurring sensor

## What to improve (unpaid — do not drop)

Bare session keys under explicit ownership need owner mapping without hand-editing gateway JSON (owner-guard script only). Gateway-single-owner scar ([#65](https://github.com/paulthorson/agentic-governance/pull/65)) LIVE separate. **Not** part of this scar’s done-when. Residual paid by [ocuclaw-owner-guard](ocuclaw-owner-guard.md) (`OCUCLAW_OWNER_GUARD`).

## P0 boundary

Do **not** file into agentic-governance: secrets/tokens, emails, Discord channel names, absolute host home paths that identify a machine user, Notion workspace IDs, or private operator data beyond the anonymized lock/sensor names above.

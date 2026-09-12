# Scar — Morning brief cite-or-blank (no invented meetings)

**Project:** OpenClaw 
**Filed:** 2026-09-12 (Standing AG — anonymized process lock) 
**Status:** CLOSED (Studio gate live; follow-ups unpaid below) 
**Kind:** harness scar / Discord ship gate 
**Lock name:** `MORNING_BRIEF_CITE_OR_BLANK` (Rule 2 A) 
**Check / sensor:** `validate-brief-grounding.py` fail-closed before Discord 
**Metric:** invented-meeting count on **shipped** Discord morning briefs = **0** (hold) 
**Scope:** OpenClaw morning briefs only (not other Grimdor reports)

## Symptom

Morning brief pipeline could Discord-ship a full “Meeting Synthesis / Activity” narrative after adversarial **KICK_BACK+rewrite**, even when evidence window had no grounded meetings (example: weekend brief listing multiple timed meetings with `source_meetings: 0`). Term whitelist caught misspellings, not invented meetings. KICK_BACK was treated as ship authority.

## Root cause

Generator prompt demanded verbose meeting sections; grounding was advisory. Adversarial rewrite re-checked Semantica/web deltas, **not** cite-or-blank. Discord summary posted the body without a hard ungrounded-claims gate.

## Fix (process lock — keep named)

1. **Cite or blank** — every meeting / decision / owner / deadline / attendee cites a concrete source id, else blank / `[unknown]`.
2. **Rule 2 A** — cite-or-blank + **re-ground every KICK_BACK rewrite** (order: generate → term check → adversarial → **grounding gate** → Discord).
3. **Sensor** — `validate-brief-grounding.py` fail-closed; on fail Discord only withhold alert, vault kept for review (exit ≠ ship).
4. **No-evidence path** — grounded meeting count 0 → short no-evidence brief; forbid invented Meeting Synthesis / Activity tables.
5. **Prompt** — temperature ≤0.3; no “fill verbose quota by inventing”; frontmatter citations / accurate `source_meetings`.

## AG implication (Adv gate)

Any later AG process lock that assumes morning briefs are **source-true** without naming this lock/check → Adv **FAIL** before Cos→human ACCEPT.

## What went well

- Dry-run sensor: prior invented brief **FAIL-closed** (timed meetings with `source_meetings=0`, no Source citations)
- Gate wired after adversarial so KICK_BACK alone cannot ship

## What didn't

- Prior TCC empty-source abort existed, but invent-with-thin/wrong evidence still shipped
- KICK_BACK+ship was a steady-state failure mode

## What to improve (unpaid — do not drop)

- Unify generator vs term-validator transcript trees (Documents vs home paths)
- Align generator exit-2 TCC/FDA special-case with shell abort path while keeping grounding withhold distinct
- Related Paperclip health deep-dive remains a separate ticket (recover ≠ close); not this scar’s done-when

## P0 boundary

Do **not** file into agentic-governance: secrets/tokens, usernames, absolute host paths, channel ids, or private operator data beyond anonymized lock/sensor names above.

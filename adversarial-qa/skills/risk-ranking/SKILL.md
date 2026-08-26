---
name: risk-ranking
description: Rank defects and coverage gaps by likelihood and impact, without a verdict on overall quality.
argument-hint: "<the gaps and known defects>"
---

# Risk Ranking

Pure inventory. No overall verdict.

## Output

1. **Ranked risks** — each with likelihood (high/med/low), impact (high/med/low), and who it
   harms (user, operator, business).
2. **Irreversible risks** — anything that can cause unrecoverable harm, marked and routed to
   the human gate (Rule 1).
3. **Unrankable** — risks you cannot score because the impact is unknown, named.

```
## RISK RANKING

| Risk | Likelihood | Impact | Harms | Irreversible? |
|---|---|---|---|---|

### Unrankable
- <what you could not score, and why>
```

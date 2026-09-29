# Paperclip

How the framework is wired into the Paperclip agent team.

## Agent roster (13 total)

**Producers** (8) — create work, must route to review:

| Agent | Routes finished work to |
|-------|-------------------------|
| Engineer | Adversarial Engineer |
| QA | Adversarial QA |
| UXer | Adversarial UX |
| UX Researcher | Adversarial UX |
| Product Manager | Adversarial Universal |
| Business Analyst | Adversarial Universal |
| Scrum Master | Adversarial Universal |
| CEO | Adversarial Universal |

**Adversary reviewers** (5) — claim `in_review` tickets, run checks, kick
back or allow:

| Agent | Reviews work from | Veto for |
|-------|-------------------|----------|
| Adversarial Engineer | Engineer | production harm, security holes, bricked config |
| Adversarial QA | QA | user harm from quality gaps |
| Adversarial UX | UXer, UX Researcher | user harm, dead ends, accessibility |
| Adversarial Researcher | general/non-UX research | unsupported claims |
| Adversarial Universal | PM, BA, Scrum Master, CEO, catch-all | irrecoverable harm |

## The mandatory-review rule

Every producer agent's instructions include the same rule:

1. **Never mark a ticket done directly.**
2. When work is complete → move to `in_review` → reassign to the matching
   adversary agent → post a completion comment.
3. The adversary reviewer then either **kicks it back** (→ `in_progress`,
   reassigned to the producer, with findings) or **allows it** (→ done, or
   flags a human gate for cost/schedule/confidence decisions).
4. Producers must **address kick-backs, not argue them away**; only a human
   clears a veto.

## Routing model

**Option A (in use):** the producer explicitly assigns its `in_review`
ticket to the correct adversary agent. Deterministic, no dispatcher.

## Wake mechanism

Paperclip wakes an agent automatically when a ticket is reassigned to it in
`in_review`. The system self-drives: producer finishes → assigns → adversary
wakes → reviews → kicks back or allows.

## See also

- [[Architecture]] · [[Domains]] · [[Vetoes]] · [[Home]]

# Setup

Configured by the conversational setup wizard (Section 9.3). Absent or incomplete config is the unknown state; the CEO bot does not start work on unknown and re-runs the wizard instead.

## Runtime
- openclaw

## Budget model
- metered

### Metered
- allowance per cycle: 1000
- reset cadence: weekly
- headroom reserved for in-flight work: 200

## Per-epic budget
- 300

## Adversarial agents
- in play: in-play

## Project repos
- ~/adversarial-agents (governance repo, read-only to bots); project work in /tmp or a project repo

## Escalation preferences (beyond Section 10.3 mandatory list)
- none beyond the mandatory list in 10.3

## Domain risk
- none declared

## Quiet hours
- 23:00-08:00 America/New_York

## Stall threshold
- 3

## Precedent decay window
- 90d

## Autonomy ladder (A2)
- starting level for new bots: 1
- clean runs required per promotion: 3

## Retry budgets (A3)
- retry count: 3
- escalation on exhaustion: escalate to human

## Routine audit (A4)
- audit cadence: weekly

## Research discovery loop (A12.4)
- rounds without new findings: 3
- round budget: 5

## Irreversible action protection (A14)
- per action class: 2


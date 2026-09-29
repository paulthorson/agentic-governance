# Learning 2026-09-13 — Stalled coordinator recovery

## What happened

The annual-roadmap restoration coordinator went silent for ~8 hours with a
critic KICK_BACK (5 findings) sitting with the builder. Status showed `running`
but the raw state was `pending_init` with no activity — a dead coordinator
masquerading as a live one.

## Learning

1. A coordinator's "running" status is not proof of life — check last-activity age.
2. Recovery is forensic: the dead coordinator's session log still held the 5
   critic findings verbatim, so a fresh coordinator picked up with zero
   re-derivation.
3. The stalled builder had actually applied all 5 findings before dying; the new
   coordinator verified rather than re-did the work. Since verdicts carry no
   timestamps and the document changed under the earlier ALLOWs, it ran spot
   re-confirmations instead of assuming they stood.

## What changed

Recovery pattern: shut down the dead coordinator, extract findings from its
session log, spawn a fresh coordinator with the findings + state, verify-don't-redo,
re-earn verdicts on the final artifact.

# Adversarial Documentation

Run the adversarial-docs loop on work.

## Usage

```
/adversarial-docs <path-to-work>
```

## What it does

1. Reads the work.
2. Spawns the `docs-adversary` agent to review it blind.
3. Returns a KICK_BACK or ALLOW verdict with findings.
4. Records the verdict to the calibration ledger.

## Rules

- The adversary never grades its own work.
- Only a human clears a veto.
- The record is append-only.

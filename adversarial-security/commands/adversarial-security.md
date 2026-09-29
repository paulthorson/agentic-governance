# Adversarial Security

Run the adversarial-security loop on a change.

## Usage

```
/adversarial-security <path-to-change>
```

## What it does

1. Reads the change (code, config, infra, dependency list).
2. Spawns the `security-adversary` agent to review it blind.
3. Returns a KICK_BACK or ALLOW verdict with findings.
4. Records the verdict to the calibration ledger.

## Rules

- The adversary never grades its own work.
- Only a human clears a veto.
- The record is append-only.

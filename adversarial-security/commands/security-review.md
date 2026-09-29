# Security Review

Run a single security-adversary review on a change.

## Usage

```
/security-review <path-to-change>
```

## What it does

Runs the four checks (vulnerability, secret exposure, supply chain, data
protection) on the change and returns a verdict with findings.

## Output

- **KICK_BACK** — a BLOCKER or veto was found. The change must be fixed and
  resubmitted. Only a human clears a veto.
- **ALLOW** — the change passes. It can ship.

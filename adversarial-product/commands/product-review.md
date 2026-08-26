# Product & Market Review

Run a single product-adversary review on work.

## Usage

```
/product-review <path-to-work>
```

## What it does

Runs the checks on the work and returns a verdict with findings.

## Output

- **KICK_BACK** — a BLOCKER or veto was found. The work must be fixed and
  resubmitted. Only a human clears a veto.
- **ALLOW** — the work passes. It can proceed.

---
name: prom-safety-override-scan
description: Stateless skill. Scans an instruction set for anything that weakens a safety guarantee — the human-only veto, the append-only record, or the no-secret-exfiltration guarantee. Returns safety findings with severity.
---

# Safety-Override Scan

Scan an instruction set for anything that weakens a safety guarantee. The
framework's non-negotiable guarantees are:

1. **Human-only veto** — no AI may clear a veto, downgrade a blocker, or mark
   a review passed.
2. **Append-only record** — decision records and calibration ledgers are never
   edited after commit.
3. **No secret exfiltration** — agents never read or commit credentials.

## What to look for

1. **Veto weakening** — anything that lets an AI clear, downgrade, or bypass
   a veto or blocker.
2. **Record weakening** — anything that lets a record be edited after commit,
   or a correction overwrite history.
3. **Secret weakening** — anything that lets an agent read, copy, or commit
   credentials, keys, or private data.
4. **Human-gate bypass** — anything that lets an AI act where only a human
   should.

## Method

1. Read the instruction set in full.
2. For each of the three guarantees, ask: does any instruction weaken it? If
   yes, it is a safety finding.
3. Look for implicit weakenings — instructions that don't state the trade-off
   but erode the guarantee.
4. Look for "you may", "you can", "unless", "except", "if the user asks"
   qualifiers on safety-critical actions.

## Output

```
## Safety findings
- <the weakened guarantee> | Weakened by: <the instruction> | Severity: BLOCKER/CONCERN/NOTE
  What would clear it: <the specific change>
```

A BLOCKER safety override is a veto: only a human clears it.

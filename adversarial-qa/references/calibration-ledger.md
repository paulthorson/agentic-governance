# Calibration Ledger

Every human override of an agent verdict gets an entry here. Nothing else does.

The ledger exists so the system can find out where it is wrong.

1. **An agent that keeps crying wolf.** Repeated `false-positive` overrides on the same kind of
   finding → its prompt gets tuned. Edit the agent file and note the change here.
2. **A rule that keeps losing.** Three overrides of one rule → the rule goes on trial.

Use `assets/templates/calibration-entry.md` for the entry format.

---

## Override tally

| Rule | Overrides | Status |
|---|---|---|
| Rule 1: User-harm vetoes are absolute | 0 | |
| Rule 2: Genuine test strategies are mandatory | 0 | |
| Rule 3: Scope can't silently win | 0 | |
| Rule 4: QA must tie to a product goal | 0 | |

| Agent | False positives | Last prompt tune |
|---|---|---|
| critic | 0 | never |
| quality-advocate | 0 | never |
| edge-case-reviewer | 0 | never |

---

## Entries

<!-- newest first -->

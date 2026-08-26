# Calibration Ledger

Every human override of an agent verdict gets an entry here. Nothing else does.

The ledger exists so the system can find out where it is wrong. Two patterns matter:

1. **An agent that keeps crying wolf.** When one agent produces repeated `false-positive`
   overrides on the same kind of finding, its prompt gets tuned. Edit the agent file in
   `agents/` and note the change here.
2. **A rule that keeps losing.** When the same constitutional rule is overridden three times,
   the rule goes on trial. Open a trial entry naming the three overrides and propose either a
   revision or an explicit carve-out. A human edits `references/constitution.md`. An agent
   never does.

Use `assets/templates/calibration-entry.md` for the entry format.

---

## Override tally

| Rule | Overrides | Status |
|---|---|---|
| Rule 1: Customer vetoes are absolute | 0 | |
| Rule 2: Genuine options are mandatory | 0 | |
| Rule 3: Engineering ease can't silently win | 0 | |
| Rule 4: UX must tie to business goals | 0 | |

| Agent | False positives | Last prompt tune |
|---|---|---|
| critic | 0 | never |
| cx-advocate | 0 | never |
| evaluative-uxr | 0 | never |

---

## Entries

<!-- newest first -->

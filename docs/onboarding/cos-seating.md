# Cos seating — memory store at AG install/setup

**Not a deferred README-only step.** Cos memory choice runs as part of AG install/setup when Chief of Staff is seated.

## When it runs

1. Operator wires MCP and starts the setup wizard (`setup_wizard_start` / `setup_wizard_answer`).
2. Operator lists roster. If a row has role `cos` (Chief of Staff), Cos is seated.
3. **Immediately after roster**, the wizard ASKS Cos memory mode:
   - `private_git` — private git repo
   - `local_folder` — on-machine private folder
4. Wizard finalize **must call** the seating hook `apply_at_cos_seating` in
   [`mcp/adversarial_mcp/cos_memory_setup.py`](../../mcp/adversarial_mcp/cos_memory_setup.py),
   which scaffolds `config/cos-memory/` from [`docs/templates/cos-memory/`](../templates/cos-memory/).

## Clarifications

| Claim | Meaning |
|---|---|
| **Paul+Cos clarified store** | Private git (their operator memory) |
| **Framework Cos ASK** | Operator chooses `private_git` OR `local_folder` — **not forced** to one |
| **Private ≠ public** | Filled memory stays out of public AG product surface |

## Re-run / CLI stub

```bash
python3 scripts/cos_memory_setup.py --show-prompt
python3 scripts/cos_memory_setup.py --mode private_git --label cos-memory-private
python3 scripts/cos_memory_setup.py --mode local_folder --label desk-cos-memory
```

Same hook the wizard calls. Label = short private name only — no host paths, emails, or secrets.

## Related

- Template skeleton: [`docs/templates/cos-memory/`](../templates/cos-memory/)
- Cos harness: [`harnesses/chief-of-staff.md`](../../harnesses/chief-of-staff.md)
- BYOA walkthrough: [`byoa.md`](byoa.md)

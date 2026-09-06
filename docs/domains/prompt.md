# Prompt Domain — deep dive

**Plugin:** `adversarial-prompt/` · **Veto:** safety overrides, injection, drift

## What it reviews

The framework's own instructions — AGENTS.md, system prompts, skills, plugin
manifests. A self-hosting adversary that audits the framework against itself.

## Adversary agents

| Agent | Role |
|---|---|
| `prompt-adversary` | The single reviewer — audits instructions for injection, drift, and safety overrides |

## The checks

- **Prompt-injection scan** — could untrusted content override the instructions?
- **Instruction-drift check** — have the instructions drifted from intent?
- **Safety-override scan** — does anything weaken a safety guarantee?

## Skills

`prom-prompt-injection-scan`, `prom-instruction-drift-check`,
`prom-safety-override-scan`, `prom-adversarial-prompt` (worker).

## Constitution / veto

The prompt constitution gates on **safety overrides, injection, and drift** —
an instruction change that weakens safety or allows injection is kicked back.
Only a human clears a veto.

## How to use

```
Use the governance server to run a review of this instruction change in the prompt domain:
<your instruction change>
```

## See also

- [[Domains]] · [[Architecture]] · [[Constitution]]

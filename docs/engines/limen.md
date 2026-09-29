# Limen — the reference engine

Limen is the **reference engine** for agentic-governance. It is a minimal
one-human-many-agents harness built from files, git, and one CLI. It is optional
— you can bring your own engine (BYOE) — but it is the engine the framework is
tested against.

> **BYOA + BYOE.** Agentic-governance is the harness (constitution, adversarial
> review, vetoes, role harnesses). Limen is the engine (spawns workers, isolates
> worktrees, manages jobs, merges). You bring your own agent (BYOA) and your own
> engine (BYOE); Limen is the recommended default engine.

## Why Limen

- **Cleanest fit.** Files + git + one CLI — exactly the model agentic-governance
  assumes. No tmux, no Postgres, no Rust build.
- **Governance belongs in the harness.** Limen has no baked-in governance, which
  is deliberate — the framework supplies it. An engine that bakes in its own
  governance would conflict with the framework's harnesses.
- **Validated.** Limen's 8 audit bugs were fixed and verified; the fixes passed
  the agentic-governance adversarial review.

See [engine comparison](comparison.md) for the full due-diligence record.

## Install

Limen is a separate project (upstream: `overment/limen`). Install it as a
dependency, not a fork:

```bash
git clone https://github.com/overment/limen.git
cd limen
npm install
npm link
```

Requires macOS or Linux, Node.js 24+, Git, and `pi` on `PATH`.

## Use with agentic-governance

1. **Install Limen** (above).
2. **Run the agentic-governance wizard** and select Limen as your engine.
3. The wizard wires the framework's harnesses + adversarial review into Limen's
   spawn/review/merge flow.

## How the harnesses map to Limen

| Agentic-governance role | Limen role |
|---|---|
| CEO harness | Limen coordinator (routes work, escalates) |
| Engineer / PM / UX / QA harnesses | Limen worker (required artifact format, stop conditions) |
| Adversarial review (critic, constitution, vetoes) | Limen reviewer (spawns a fresh reviewer against a candidate) |
| Acceptance record + veto gate | Limen merge decision (human merges) |

## Bring your own engine (BYOE)

Limen is the default, but not required. If you use Claude Code, Cursor,
Paperclip, or another engine, the framework governs it the same way — the
harnesses and adversarial review are engine-agnostic. The wizard asks which
engine you use and wires the harnesses accordingly.

## See also

- [Engine comparison](comparison.md)
- [BYOA / BYOE onboarding](onboarding/byoa.md)

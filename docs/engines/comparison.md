# Engine comparison — why Limen is the reference engine

Agentic-governance is **BYOA + BYOE**: you bring your own agent (the worker) and
your own engine (the runtime that orchestrates agents). The framework is the
harness — constitution, adversarial review, vetoes, role harnesses. The engine
is pluggable. This page records the due diligence behind choosing **Limen** as
the reference engine.

## The candidates evaluated

| Engine | Model | Governance baked in? | Fit for agentic-governance |
|---|---|---|---|
| **Limen** (`overment/limen`) | Files + git + one CLI | No (deliberate) | **Chosen.** Cleanest fit; governance belongs in the harness, not the engine. |
| **superharness** (`backmeupplz`) | tmux-based orchestration around Claude/OpenCode/Codex | No | Considered. tmux dependency adds fragility; heavier than needed. |
| **majiayu000/harness** | Rust control plane | **Yes** | Considered. The only candidate with governance baked in — but that conflicts with the framework's harnesses (two governance layers). |
| **legio** | Smaller/niche | — | Considered. Too small to be a reference. |
| **ruah** | Smaller/niche | — | Considered. Too small to be a reference. |
| **haru** | Smaller/niche | — | Considered. Too small to be a reference. |

## Why Limen

1. **Cleanest fit.** Files + git + one CLI — exactly the model agentic-governance
   assumes. No tmux, no Postgres, no Rust build. The harnesses map directly onto
   Limen's spawn/review/merge flow.
2. **Governance belongs in the harness, not the engine.** Limen has no baked-in
   governance, which is a feature: the framework supplies it. An engine that
   bakes in its own governance (like majiayu000/harness) would create two
   competing governance layers and conflict with the framework's harnesses.
3. **Validated.** Limen's 8 audit bugs were fixed and verified; the fixes passed
   the agentic-governance adversarial review.

## The key insight

> **Governance lives in the harness, not the engine.** So an engine *without*
> baked-in governance is the right fit — the framework provides the governance,
> and the engine just orchestrates.

This is why Limen (no governance) beats majiayu000/harness (governance baked in)
for this framework: the framework *is* the governance, and a clean, minimal
engine is the best substrate for it.

## Bring your own engine (BYOE)

Limen is the default, not required. If you use Claude Code, Cursor, Paperclip,
or another engine, the framework governs it the same way — the harnesses and
adversarial review are engine-agnostic. The setup wizard asks which engine you
use and wires the harnesses accordingly.

## See also

- [Limen — the reference engine](limen.md)
- [BYOA / BYOE onboarding](onboarding/byoa.md)

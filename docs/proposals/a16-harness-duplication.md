# Proposal: A16 — harness bodies are duplicated

**Status:** Draft for operator review. Not decided.
**Date:** 2026-09-06
**Related:** A16 open problem (spec-addendum-01.md §A16). This is the problem
that just bit us (2026-09-06): a decision recorded as DECIDED in a proposal
while the addendum said "Not decided" — two copies of a rule disagreeing, no
precedence rule.

## The problem

Each producing role harness body exists in two places: inline in the spec
(Sections 5.0–5.4, CEO harness in Section 10) and as a standalone file in
`harnesses/`. Nothing states which copy wins when they diverge. A harness is
governance; two copies of a rule that can disagree is the duplication problem
this framework exists to remove.

## The fix — two options

### Option A — Precedence rule (recommended)

One copy is authoritative; the other is documentation. The **harness file is
canonical** and the spec is a rendering (or the reverse).

- **Pros:** Smallest change; no tooling; immediately resolves the ambiguity.
- **Cons:** Still two copies that can drift; the precedence rule only says which
  wins, it does not prevent divergence.
- **Which copy?** Recommend the **harness file is canonical** — it is what a bot
  actually loads at runtime (the persona block points at `harnesses/<role>.md`),
  so the file a bot reads should be the truth. The spec's inline copy becomes a
  rendering for human reading.

### Option B — Generate one from the other (single source of truth)

A single source of truth, with the other produced from it, so the two cannot
drift.

- **Pros:** Eliminates drift entirely; the A16 failure mode becomes impossible.
- **Cons:** Requires a generation step (a script or build) and a CI check that
  the generated copy is in sync; more upfront work.
- **Which is the source?** Recommend the **harness file is the source**, and the
  spec's inline copy is generated from it (or replaced by a pointer to the file).

## Recommendation

**Option B** — generate one from the other, with the harness file as the source
of truth. The A16 failure mode just occurred in this repo; a precedence rule
(Option A) would have told a bot which copy to believe, but it would not have
prevented the two copies from disagreeing in the first place. Option B removes
the duplication, which is the actual problem A16 names.

If Option B is too much for now, **Option A** (harness file canonical) is the
acceptable interim — it at least resolves which copy a bot should believe.

## Open questions for the operator

1. Approve Option A (precedence) or Option B (generate one from the other)?
2. If B: is the harness file the source, with the spec's inline copy generated
   from it (or replaced by a pointer)?
3. If A: confirm the harness file is canonical and the spec is the rendering.

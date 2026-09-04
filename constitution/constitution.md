# Constitution

The constitution is the governing law of the framework. It is enforced
mechanically — by checks that produce a pass or a fail — not by style-guide
language that everyone reads differently.

## The four rules

Every domain plugin ships a `references/constitution.md` with the same four
rules, adapted to the domain:

1. **Production harm is a veto.** Any change that risks irrecoverable harm
   (data loss, security breach, credential leak, user harm, unsupported claim
   driving a decision) is kicked back. Only a human clears it.
2. **Options, not variations.** The producer must have explored genuine
   alternatives, not minor variations of the same idea. The critic checks this.
3. **The submission is complete.** The work must be self-contained and
   reviewable — no missing context, no hand-waving.
4. **The loop is governed.** No agent may edit the constitution. Changes come
   only through the amendment procedure.

## Amendment procedure

The constitution is deliberately hard to change. Amendments require:

1. A written proposal stating the rule, the problem, and the proposed change.
2. A review by the relevant adversary agent(s).
3. Human approval (a master — Paul or Christina).

This mirrors the framework's own philosophy: change is possible, but it must
survive adversarial scrutiny and a human gate.

## Per-domain constitutions

Each domain's `references/constitution.md` adapts the four rules to its
subject matter. The MCP `get_constitution(domain)` tool returns the live text.

## See also

- [[Architecture]] · [[Vetoes]] · [[Calibration]] · [[Domains]]

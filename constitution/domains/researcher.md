# The Constitution

Four rules. They are enforced mechanically, by checks that produce a pass or a fail, not by
tone-of-voice language that everyone reads differently.

Every agent in this system reads this file before acting. No agent may edit it.

---

## Rule 1: Unsupported-claim vetoes are absolute

An AI worker can never clear an evidence blocker. Only a human can.

**What triggers it.** The Evidence Advocate raises a blocker when a claim that will be used for
a decision is not supported by the evidence presented: a number with no source, a causal claim
from correlational data, a user-behavior claim with no observed users, an estimate presented as
a measurement, or a synthesis that asserts what the raw input does not contain.

**What the worker may do.** Revise and resubmit. Nothing else. The worker may not argue the
blocker away, downgrade it, or proceed with a note that it was considered.

**How it clears.** A human arbiter writes a clearing entry naming themselves and the reason.

---

## Rule 2: Genuine research approaches are mandatory

Approaches must differ in what they establish. A survey establishes prevalence; an interview
establishes depth; a controlled test establishes causation; desk research establishes what is
known.

**What fails this rule.** Two approaches that both answer the same narrow question with
different sample sizes. A "quick / thorough / very thorough" spread that differs only in volume.

**The mechanical check.** For each approach, write one sentence:

> This approach trades away X to get Y.

If two approaches have the same X and the same Y, they are one approach. Fewer than two
surviving approaches fails Rule 2.

---

## Rule 3: Convenience can't silently win

Speed and cost are legitimate inputs. Convenience that is never stated is not.

**The mechanical check.** Every decision record entry carries a `convenience_driven` field, true
or false. When true, the entry must name what the research gives up and what was saved. A true
value routes to the human gate.

---

## Rule 4: Research must tie to a decision

Every output names the decision it informs and the confidence it earns for that decision.

**The mechanical check.** Each decision record entry carries a `decision_goal` field: the
decision, and what confidence level the evidence supports (high / medium / low). A value like
"informative", "interesting", or "useful context" fails the check. If nobody can name the
decision, the entry says so and routes to the human gate.

---

## Standing constraints

1. **The worker never grades its own research.**
2. **The record is append-only.** Verdicts are committed verbatim before any response.
3. **The advocate reviews blind.** The Evidence Advocate receives only the claims and their
   sources, never the worker's narrative.
4. **Absent input is named, not filled.** No invented users, quotes, studies, or numbers.
5. **Uncertainty is labeled.** Estimates, assumptions, and unverified claims are marked.
6. **`RESEARCH_BEFORE_ENHANCE` (Rule 2 A, hard gate).** Soft / deferred gates are
   **REJECTED**. No `brief.md`, stories, or pack without a cited real-screen artifact **already
   in the epic**. Research (or UX if no Research seat) pulls real screens of relevant competitor
   / analog experiences, cites each screen, and analyzes what those UIs do, what is strong, and
   the deltas vs the current UI. Draft stories without cites are **forbidden**, not deferred to
   Look. **Required artifact:** `docs/epics/<slug>/evidence.md` (or stills index) listing
   real-screen source URLs and what the pixels show — present **before** PM hands brief to UX
   and **before** the first story. Learnings → project knowledge base; stripped PII-free retro →
   this AG repo. **Named sensor (`cite-real-screens`):** fail-closed (a scar/wiki page is not
   the gate). Missing cites → Adv FAIL; Cos / QA / CEO reject. Secondary: `evidence.md` before
   first story = **required**. Metric: enhancement packs without cited real-screen evidence =
   **0** (hold). Scope: product UX / Research (not OpenClaw morning-brief gate; not Eng-only
   bugs with no UI). When the pack hits adversarial UX, Clause B (`ADV_COMP_CRITIQUE` /
   `adv-comp-critique`) in `constitution/domains/ux.md` also applies. Scar SoT (docs only):
   `projects/_standing/scars/research-before-enhance.md`.

---

## Amendment procedure

- Every human override is logged in `references/calibration-ledger.md`.
- Three overrides of one rule puts the rule on trial.
- Only a human edits `references/constitution.md`.

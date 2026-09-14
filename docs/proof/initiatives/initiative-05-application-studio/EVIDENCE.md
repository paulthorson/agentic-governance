# Initiative evidence — initiative-05-application-studio

Shipped 2026-09-13 (final close-out committed 21:01 EDT). Veto's Application
Studio: governed resume tailoring with versioned variants, an evidence
library, ATS readiness checks, explained diffs, review-gated application
packets, and earned-success feedback. Every tailored statement traces to
approved evidence; every version restores byte-identically; the packet is
build-only (no submit path exists); delight appears only under
Initiative 00's context gate.

## Scope

- `initiatives/i05/`: contracts, versions, evidence_library, ats_check,
  diff_explain, packet, success_feedback, studio (terminal CLI),
  DECISIONS.md, integration_notes.md
- `tailor.py::tailor_with_provenance()` — additive; existing behavior unchanged
- 7 test files, **137/137 i05 tests green** on the committed tree
- Terminal coverage complete via `studio.py` (15 subcommands); web/phone
  integration specified as exact snippets for the owning teams
  (out of file scope)

## Governance — the real arc (16 verdict records: 12 ALLOW, 4 KICK_BACK)

Tickets: `muse/2026-09-13/roadmap-exec/init-05/ws1`–`ws6`,
`muse/2026-09-13/roadmap-exec/init-05` (epic blind reviews),
`muse/2026-09-14/roadmap-exec/init-05-finalmile`.

1. **First pass (5 ALLOW):** ws1 (contracts + versioned variants), ws2
   (evidence library), ws3 (ATS readiness), ws4 (diff + packet), ws6
   (earned feedback + CLI) — all ALLOW, 0 structural vetos.
2. **Blind epic reviews (3 ALLOW, 2 KICK_BACK):** Epics 4+5 ALLOW, Epic 1
   ALLOW, Epic 6 ALLOW. Epic 2 (evidence library) KICK_BACK — three majors
   against its headline honesty claims. Epic 3 (ATS readiness) KICK_BACK —
   blocker: the `ready` flag overclaimed ATS-readiness for resumes that
   still carried warnings.
3. **Rework + fresh blind re-reviews:** Epic 1 re-review ALLOW (all five
   claimed fixes verified by the reviewer). Epic 3 re-review ALLOW
   (reviewer ran the 24/24 ATS test file). Epic 2 re-review KICK_BACK —
   the three original majors were verified fixed, but the fresh reviewer
   found a new issue → second rework → **round-3 re-review ALLOW**
   (reviewer executed the exact probe).
4. **Final mile (1 KICK_BACK, 1 ALLOW):** the structural veto scanner
   flagged the keyword `downtime` inside synthetic fixture text — a false
   positive, but the loop treats scanner hits as guilty until reviewed.
   Fixture reworded → round-2 blind re-review with a fresh reviewer:
   ALLOW.

Every KICK_BACK returned to the builder with findings and was cleared by
rework plus a fresh blind reviewer — never by editing a verdict, never by
escalation. Veto overrides: 0.

## Metrics

- 16 verdict records across the initiative; KICK_BACK rate 25% — the
  adversarial loop fired in practice, including twice on re-reviews, and
  every finding was closed before ship.
- 137/137 i05 tests green on the committed tree (7 test files).
- Reviewers ran the actual test files and exact probes during re-reviews;
  verdicts cite executed evidence, not code reading.

## Caveats (disclosed)

- **Accepted defect (follow-up F2):** the ats-ready checklist copy
  overclaims — it does not name the blocking warnings. Docs-only fix
  recorded in DECISIONS.md, still open.
- **Review isolation, first pass:** the ws1–ws6 first-pass reviews were
  executed by the build coordinator under blind discipline (work product +
  framework review_prompt only), with the caveat recorded in the verdict
  summaries. All KICK_BACK rounds and the final-mile round-2 were
  genuinely blind with fresh, independent reviewers.
- Built against local contract adapters for Initiatives 01/02/04/00
  (their live contracts had not landed); the swap is a one-line wiring
  change per adapter.
- Web/phone surfaces are integration contracts + snippets, not
  implementations — the owning teams wire them; terminal is fully
  covered today.
- The `.gitignore` hunk for i05 data stores sits outside the
  initiative's listed file scope; flagged for reviewer confirmation.
- No ws5 ticket: diff explanations and the application packet were
  reviewed together as ws4 (they share the review-gate boundary).

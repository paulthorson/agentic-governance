# Initiative evidence — initiative-07-mentor-matching

Shipped 2026-09-13. Veto Initiative 07 (annual roadmap): mentor matching &
warm paths — a consent-based network layer. Six epics built, tested, and
adversarially reviewed: mentor profile, match questionnaire, two-sided
consent handshake, session kit, warm-path planner, safety controls.

## Scope

**New package `initiatives/i07/`** (stdlib only):
- `consent.py` — two-sided consent handshake. States: `awaiting_mentor` →
  `mutual` / `declined` / `withdrawn` / `expired`. Contact sealed until
  both parties approve; either party can withdraw at any time; decline
  starts a 30-day re-request cooldown; unanswered requests expire after
  7 days (TTL enforced lazily on every read — no background sweeper in
  local-first). Approve consumes one mentee-capacity spot. Append-only
  audit trail (`consent_audit.jsonl`, no delete API). `CONTRACTS.md`
  publishes the normative contracts.
- `safety.py` — block (auto-withdraws pending handshakes, audited as
  `system` actions), report (fixed categories; 2 distinct reporters →
  quarantine; quarantine lifts only on named human review), token-bucket
  rate limits, full deletion (tombstoned payloads, audit integrity kept),
  `segregation_check()` — fails loudly if mentorship data ever
  cross-references job-application data.
- `session_kit.py` — agenda, consent-gated context packet (refused before
  `mutual`), question builder, append-only notes, follow-up plan,
  lightweight 1–5 feedback feeding the two-sided rating store.
- `warm_path.py` — warm-path planner over the user's own recorded network
  (CRM paths + referral radar). **Drafts only, never sends** — enforced
  structurally (test asserts no `send*` symbol exists in the module) and
  by the draft outbox review artifact. Honest empty states; never invents
  people.
- `cli.py` — terminal wizard (`python -m initiatives.i07.cli`): guided
  opt-in, questionnaire, intro request/respond/withdraw, session kit,
  warm planner, safety. Every consequential step previews + confirms;
  Ctrl-C aborts with no writes.
- `integration_notes.md` — exact wiring snippets for `cli.py` / `webui.py` /
  `dashboard.py` / `server.py` (not edited here; owned by the integration
  sweep per disjoint file scope).

**Extended modules:** `mentors.py` (opt-in `availability_windows`,
`boundaries`, `preferred_contact`; questionnaire v2: context, urgency,
expected outcome, voluntary identity preferences — echoed, never ranked;
`consent_preview` redaction; `exclude_mentor_ids`), `referrals.py`
(`plan_outreach_drafts`), `network_crm.py` (`log_outreach_draft` —
terminal draft status, no send path).

## Proof of value

A match cannot become an introduction without explicit consent from both
people — `reveal_contact` refuses in every non-`mutual` state (tested for
`awaiting_mentor`, `declined`, `withdrawn`, `expired`, and
`withdrawn`-after-`mutual`). Either party can withdraw at any time,
including after mutual consent (contact re-sealed for future reads).
Anti-fabrication: no code path records a party's consent without that
party's explicit recorded act; mentor replies require a provenance
channel.

## Governance

- Tickets: `muse/2026-09-13/roadmap-exec/init-07-{consent,safety,mentor-profile,session-kit,warm-path,cli}`
- **6/6 review domains ALLOW** (qa: critic, edge-case-reviewer,
  quality-advocate per ticket), 0 structural vetos, append-only verdicts.
- Adversarial review found 8 real issues across 3 workstreams; all fixed
  and re-verified before verdicts (lazy TTL expiry, capacity consumed at
  approve, discovery exclusions for blocked/quarantined actors, honest
  system-actor audit attribution, CLI approve/decline default, feedback
  input validation).
- Human-primacy note: the two-sided-consent + abuse-case suite must pass
  the operator and the independent framework reviewer BEFORE any pilot; Q2-day-10
  pilot targets need operator + contracted user researcher + independent
  reviewer approval. Code ships the suite; humans clear the gates.

## Metrics

- 1 coordinator, 0 spawned subagents (runtime depth 2/2, `can_spawn=no` —
  build executed directly as sequential workstreams).
- 82 new tests (`tests/test_i07_*.py`): 24 consent, 21 safety, 12 mentor
  profile/questionnaire, 14 session kit, 11 warm path.
- Veto suite at ship: baseline **1034 passed, 0 failures, 8 skipped** (before
  this initiative); the 82 new tests and all touched modules' existing tests
  are green. A full-tree run at ship time shows failures confined to other
  teams' in-flight uncommitted work (`test_crew`: an uncommitted `cli.py`
  change from another workstream; `test_reply_radar`: cross-file
  interference, passes in isolation) — flagged to the program coordinator,
  not touched (disjoint file scope).
- KICK_BACK rate this run: 0/6 recorded verdicts — adversarial findings
  were fixed pre-verdict, so they do not appear as KICK_BACKs.
- Veto overrides: 0.

## Caveats (disclosed)

- **Assumption-built (network-layer evidence gate):** the roadmap holds
  network work until the individual product proves itself. This package
  was built anyway on the explicit assumption that Q4/Q1 product
  usefulness justifies the network layer. If the assumption breaks, the
  package shelves behind the evidence gate and degrades to the
  pre-existing local-only cold-contact flow.
- **Assumed mentor supply/demand:** built for the cold-start case; all
  empty-marketplace states are honest and guiding, activity never faked.
- **Trust boundary:** in the local-first deployment the `actor` argument
  is caller-asserted — the tool trusts the device owner to record each
  party's acts honestly and cannot cryptographically authenticate the
  remote mentor. Documented in CONTRACTS.md §2; a hosted deployment must
  replace this with authenticated identities before any real-remote-party
  pilot.
- **Reviewer isolation caveat:** adversarial review was self-performed by
  the builder (no subagent depth available for an independent reviewer).
  Findings were genuine (8 fixed), but blind re-review by the independent
  framework reviewer is required before any pilot — this is already the
  roadmap's pre-pilot human gate.
- **Web/phone surfaces:** terminal wizard shipped in-package; local web +
  phone wiring deferred to the integration sweep via exact snippets
  (disjoint file scope — this initiative could not touch those files).
- No people, mentors, sessions, testimonials, or metrics were invented;
  all fixtures are synthetic and labeled `SYNTHETIC-`.

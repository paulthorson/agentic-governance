# Initiative evidence — initiative-09-connector-reliability

Shipped 2026-09-13. Veto Initiative 09 (annual roadmap): connector reliability
& coverage — every connector declares what it can do, why it may be blocked,
what data it sends, and what needs confirmation; provider health flows through
one store; CAPTCHA/auth/ambiguity becomes a structured pause-and-handoff
instead of a dead end. All six epics built, tested, and adversarially
reviewed: provider contract kit, ATS deepening (official interfaces only),
explicitly selected communication connectors, confirmed calendar handoff,
session rescue, provider reliability scorecard.

## Scope

**New modules:**
- `providers/_contract.py` — the Q2 capability contract: normalized
  `JobPosting`/`JobDetail` schema, terms/robots classification per provider,
  budgets derived from `compliance.py` (single source of truth — the
  scorecard can never display a number enforcement doesn't use),
  `ConnectorManifest` proof-of-value declarations (four required sections),
  and the `conformance_suite` every connector must pass.
- `providers/health_contract.py` — ADAPTER over Initiative 03's
  `provider_health.py` (found in-tree mid-build; the "no contract"
  assumption was stale). Single write path via 03's `record_fetch`;
  reads map 03's `provider_status()` rows onto `HealthSnapshot` through
  one explicit function (`snapshot_from_status`). Local JSONL fallback
  when 03's module is unavailable.
- `providers/scorecard.py` — terminal table + JSON reliability scorecard:
  freshness, error state, last success, capability label, budget,
  cooldown, CAPTCHA state, recovery streak. Providers with no data show
  "no data" — never a fabricated healthy row.
- `providers/session_rescue.py` — detects reCAPTCHA, hCaptcha, Cloudflare
  Turnstile, generic CAPTCHA markers, login/auth walls, and ambiguous
  fields; produces a structured `RescueHandoff` (reason, evidence,
  screenshot path, field summary, guidance, resume token). CAPTCHA is
  never bypassed — the refusal is part of the contract.
- `initiatives/i09/channels/registry.py` — explicit opt-in registry for
  personal email, WhatsApp, Discord, Messenger. Disabled by default; enabling
  requires `confirm=True`; append-only local consent audit. personal email
  delegates to the existing `email_sync`; WhatsApp/Discord/Messenger are
  skill-gated declarations (no transport claimed) — disclosed, not hidden.
- `initiatives/i09/calendar_handoff.py` — side-effect-free interview-prep
  and follow-up drafts; `confirm_and_handoff` refuses without `confirm=True`
  AND refuses confirmed drafts with missing times (no fabricated defaults).
- `initiatives/i09/integration_notes.md` — exact copy-paste wiring snippets
  for `server.py` / `cli.py` / `dashboard.py` / `webui.py` (not edited here;
  owned by the integration sweep per disjoint file scope), plus an explicit
  list of what must NOT be wired yet.

**Extended modules (additive only):** `greenhouse.py`, `lever.py`,
`ashby.py` (official detail enrichment: offices, application questions,
departments/teams, workplace type, remote/date — read-only); `ats_apply.py`
(`describe_apply_path` honesty declarations); `browser_apply.py`,
`easy_apply.py` (rescue checks after load/navigation and before fills and
submits; no fill and no submit proceeds on a flagged page).

## Proof of value

- The Q2 gate is mechanical: `validate_manifest` fails any connector whose
  four proof-of-value sections aren't all non-empty; `conformance_suite`
  checks schema, self-describing ids, terms classification, and
  compliance-derived budgets — 23 contract tests, all green.
- Session rescue holds by construction + test: rescue checks run before
  every fill and every submit; a flagged page returns a handoff, never a
  bypass attempt (17 tests, incl. a wiring test asserting the checks exist
  in the apply paths).
- Channels hold by construction + test: nothing is enabled by default;
  `enable_channel` without `confirm=True` changes nothing and returns the
  manifest for review (13 tests).
- Calendar holds by construction + test: unconfirmed drafts are inert
  dicts; the handoff refuses to execute without confirmation (10 tests).
- Policy suite (18 tests) pins the cross-cutting guarantees: manifest
  completeness, no auto-enable, local-first storage, budget truthfulness,
  rescue-before-submit wiring.

## Governance

- Tickets: `muse/2026-09-13/roadmap-exec/init-09/{provider-contract,ats-connectors,session-rescue,reliability-scorecard,communication-connectors,calendar-handoff,integration-surfaces}`
- **7/7 review domains ALLOW** (qa/engineer), 0 structural vetos, append-only verdicts.
- Adversarial review found 3 real defects, all fixed and re-verified before
  verdicts: (1) a parallel invented budget table mismatching enforcement
  tiers → budgets now derived from `compliance.py`; (2) a duplicated
  robots.txt helper → removed in favor of the canonical one; (3) the stale
  "no 03 contract" assumption → `health_contract.py` rewritten as an
  adapter with the assumption flag flipped to CONFIRMED-with-caveats in
  the module docstring.
- Retro written to `governance/LEDGER.md` at ship time (not reconstructed).

## Metrics

- 1 coordinator, 0 spawned subagents (runtime depth 2/2, `can_spawn=no` —
  build executed directly as sequential workstreams).
- 105 new tests across 7 modules, all green.
- Veto suite at ship: 1492 tests; failures confined to other teams'
  in-flight uncommitted work (`test_contribute`, `test_crew`,
  `test_ext_sandbox` — files outside Initiative 09's scope), flagged to
  the program coordinator, not touched (disjoint file scope; never stashed).
- KICK_BACK rate this run: 0/7 recorded verdicts — adversarial findings
  were fixed pre-verdict, so they do not appear as KICK_BACKs.
- Veto overrides: 0.

## Caveats (disclosed)

- **Initiative 03's contract is in-flight:** `provider_health.py` exists in
  the tree but is uncommitted. The adapter maps its fields explicitly
  (`snapshot_from_status`); if 03 renames fields before shipping, only
  that one function changes. Until 03 commits, the adapter exercises its
  local fallback (7 adapter tests skip gracefully in that state).
- **WhatsApp/Discord/Messenger are declarations, not deliveries:** no
  transport is wired and none is claimed; the registry blocks any send
  path until a skill connects AND the user explicitly enables the channel.
- **Calendar is a confirmed handoff payload, not an executed write:** the
  integration sweep executes it through the calendar skill with the user's
  grant — no direct API write is invented here.
- **Reviewer isolation caveat:** adversarial review was self-performed by
  the builder (no subagent depth available for an independent reviewer).
  Findings were genuine (3 fixed), but blind re-review by an independent
  reviewer should be arranged by the parent before these verdicts are
  treated as fully cleared.
- **Web/phone surfaces:** terminal scorecard shipped in-package; local web
  + phone wiring deferred to the integration sweep via exact snippets
  (disjoint file scope — this initiative could not touch those files).
- **Shared-tree commit collision:** during the push, a concurrent
  coordinator's rebase swept one Initiative 09 test fix
  (`test_scorecard.py` adapter skip) into their commit. The tree was
  verified correct afterward (all 105 tests green on the merged main);
  attribution is imperfect, content is exact.
- No private names, emails, secrets, or absolute paths in this file; all
  fixtures synthetic and labeled `SYNTHETIC-`.

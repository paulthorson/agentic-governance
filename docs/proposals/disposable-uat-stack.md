# Disposable UAT — salvage-only recommended pattern

**Status:** ADOPTED (salvage-only recommended pattern) — 2026-09-18 
**Ship-gate strength:** recommended practice, **not** a required fleet ship gate 
**Skill / constitution:** none — no skill file; constitution untouched 
**Adoption:** opt-in per project; recorded as a decision; reversible 
**Keep path:** `docs/proposals/disposable-uat-stack.md`

## What is adopted

A short sealed-copy pattern for acceptance runs:

1. **Stand up** a disposable local copy of the service and what it needs for that run.
2. **Test** against that copy.
3. **Tear down** everything the run created (including on catchable failures).

Use **fake, sanitized, version-controlled seed data** — never production data.

The builder does **not** grade a hand-tuned laptop. Verification belongs in an environment the builder did not personally tune for a lucky green.

If a project **chooses** recorded stubs, **stale or missing stub recordings fail loud** (hard red). Stubs are not mandated by this adoption.

## What this is not

This adoption is **not** a five-command platform, not a production-identical database mandate, not a two-layer contract-testing platform, not a fleet-wide re-record cadence, and not a required ship gate. Those ideas live only under **NOT ADOPTED** below (historical / rejected platform face).

## Soft notes (salvage face)

When a project opts in, watch for: cache that breaks hermetic runs; seed-before-migrate ordering mistakes (migrate before seed); async/streaming paths left outside the sealed copy; tear-down that leaves local residue or is misused as a long-lived local stack. Name them in the project decision — do not grow this page back into a platform.

## Open questions (operator lock 2026-09-18)

1. Approve as a QA-domain playbook? — **ANSWERED:** yes, as salvage-only recommended QA playbook (not a fleet platform).
2. Placement: standalone docs page, or a section in existing QA-domain docs? — **ANSWERED:** keep at `docs/proposals/disposable-uat-stack.md`.
3. Ship-gate strength: recommended practice, or required gate alongside UAT? — **ANSWERED:** recommended, **not** required.

---

## NOT ADOPTED / historical appendix

> Everything below is **not adopted**. It is retained as readable history of an earlier platform-shaped proposal face (rework 5 / QA adversarial review round 4 era). Do not treat any rule, command contract, cadence, or acceptance checklist here as current guidance.

**Historical status line (superseded):** PROPOSED (rework 5 — addresses QA adversarial review round 4), dated 2026-09-16. 
**Historical related framing:** QA harness ("What you own": test plans, test results); standing rule that user acceptance testing gates every ship.

### Historical problem statement (not adopted as fleet law)

Acceptance tests usually run against whatever environment happens to be
around: a developer's laptop, a shared staging box, a staging database that
has drifted from production. That produces three failure modes the review loop
cannot catch, because adversarial review judges the work, not the room it ran
in:

1. **"Passed locally, failed in staging."** In-memory or lightweight stand-ins
   differ from the production data store in SQL dialect, driver behavior, and
   connection handling. (Assumption, labeled: this locates environment bugs
   where industry experience says they cluster; a project with counter-evidence
   should say so.)
2. **Flaky, non-repeatable runs.** Live external APIs change, rate-limit, or go
   down. Nothing about the run is reproducible six months later, so a past
   green run proves nothing about today's code.
3. **Contaminated state.** One run's leftovers become the next run's fixtures.
   A suite that passes because of residue is not testing the code.

User acceptance testing is a standing ship gate. A gate that runs on a
contaminated, non-repeatable environment is not a gate; it is a ritual.

### Historical five-command platform pattern (not adopted)

One command stands up a developer's own complete, disposable copy of the
service and everything it depends on. A second command runs the full test
suite against it. A third tears it all down. Nothing is shared, nothing is
long-lived, and a fresh clone works on the first try.

Conventional command names (adapt to the project's tooling — the five
lifecycle operations are the contract; the names are conventional, the tools
are the project's choice; never introduce a second language or framework to
satisfy this playbook):

- `stand-up` — start containers, seed data, start stub servers, start service
- `test-contract` — contract tests only (fast feedback)
- `test` — full suite: unit, contract, integration, regression
- `record-stubs` — re-record external API responses from a test environment
  (`record-stubs --verify` probes the test environment and diffs response
  shapes against the recordings; it runs on a schedule, not per-PR)
- `tear-down` — stop and delete everything

CI runs stand-up, then the suite, then tear-down — with teardown on all
catchable failures even when the suite fails (trap / try-finally, never a
bare `&&` chain, which would skip teardown on exactly the runs where residue
matters most).

### Historical "what this buys" framing (not adopted)

This playbook turns the framework's verification from ritual into mechanism.
Today a verdict can cite "all tests green" — a claim about a run nobody can
reproduce. Under this playbook a verdict cites "N/N green in disposable stack
run #200, byte-identical to run #1" — an aspiration with a defined scope,
labeled as such: byte-identical reruns hold for normalized inputs
(recordings, fixtures, seeds). Full run-level determinism would additionally
require seeded RNGs, fixed clocks, normalized logs, and stable ordering —
controls this playbook does not mandate. The claim here is precisely scoped:
what is version-controlled and normalized reruns identically; beyond that
boundary, the playbook promises isolation and repeatability, not
bit-for-bit determinism. The environment is version-controlled,
the stubs are recorded and stamped, the data is seeded from fixtures. That is
evidence, not a claim.

It also gives teeth to "builders never verify their own work." Today that rule
is about who runs the review; this playbook extends it to *where* the review
runs. Verification executes in a disposable environment the builder did not
hand-tune — no lucky local config, no residue from the builder's own
debugging sessions, no "works on my machine." The environment is a neutral
witness.

### Historical adoption framing that made rules ship-gate-required once opted in (not adopted)

This is a **playbook**, not a constitutional requirement. It imposes nothing
on any project until the operator adopts it for that project. Adoption is
per-project, recorded as a decision, and reversible. The constitution is
untouched by this proposal; no new universal "thou shalt" is created.

The rules below are written as "a project that adopts this playbook…".
Where the text says "required," it means required *at that project's ship
gates once adopted* — adopted per project, required at ship gates. A project
that has not adopted the playbook is unaffected by every line below.

Each rule below states its tradeoff in the constitution's mechanical form
("this strategy trades X for Y"), its metric with a direction, and its scope
flag.

**Operator note (2026-09-18):** the salvage adoption above keeps opt-in /
recorded / reversible and constitution-untouched, but does **not** adopt
"required at ship gates once adopted," the five-command contract, or the
rules that follow.

### Historical rule 1 — Lifecycle hermetic and disposable (not adopted as written)

- `stand-up` produces a complete copy of the service **and everything it
  depends on**, owned by that run alone. Two developers' runs never share
  test state — they share the host kernel and container daemon, so volumes,
  networks, and containers are named with the run id; static names are
  forbidden. Run ids are globally unique (UUID), never bare build numbers
  (which CI systems may reuse across re-runs). A run never depends on a long-lived shared environment.
- `tear-down` removes everything the run created on all catchable failures
  (trap / try-finally). It does not cover SIGKILL, CI-runner preemption, or
  OOM-kill — that residual risk is named here, not hidden; the post-teardown
  audit (acceptance criterion 8) is the backstop. After teardown, no
  containers, volumes, stub servers, bound ports, or seeded data remain.
- **Ports:** fixed ports are forbidden. `stand-up` allocates ephemeral
  (OS-assigned) ports and publishes them to the service under test via
  configuration, so concurrent runs on one machine or a shared CI runner
  coexist without collision. The service's listen port must therefore be
  configurable — where a service genuinely requires a fixed port
  (callbacks, startup contracts), the exception is documented at adoption
  and isolation is achieved by other namespacing.
- Acceptance criterion: a fresh clone of the repo, on a machine with the
  documented prerequisites, reaches a green stand-up/test/tear-down on the
  first try.

> This rule trades developer-machine resources and CI minutes for isolation
> and repeatability.
> Metric: fresh-clone first-try green rate, toward 100%; teardown residue
> count, toward 0; concurrent-run interference incidents, toward 0.
> Scope: scope_driven = true. The project gives up runner resources and
> minutes; it ships slower per run but stops shipping environment bugs.
> What the team ships faster: root-causing — reproducible failures debug
> in minutes instead of days.

### Historical rule 2 — Production-identical DB engines in containers (not adopted)

- Run the **same database engine and version production uses**, inside a
  container, started and stopped by the test harness (Testcontainers or the
  stack's equivalent).
- No in-memory or lightweight substitutes. They differ in SQL dialect, driver
  behavior, and connection handling.
- Seed the database from a **small, sanitized, version-controlled snapshot**.
  (Assumption, labeled: a few hundred representative records is enough for
  most projects — size the snapshot to the project's own edge-case history,
  and record the sizing rationale next to the seed.)
- The seed must cover the edge cases that caused past data-layer bugs; the
  snapshot's provenance (what it covers and why) is documented alongside it.
- **Never production data.** Sanitized fixtures only. The mechanical screen
  is a `check-fixtures` lint — a best-effort heuristic (pattern matching
  has known false negatives on free-text fields and novel formats, labeled
  as such) that scans seed snapshots for production hostnames, credential
  patterns, and known PII markers, and fails the build on a hit. Code
  review is the second check, not the only one.
- If the project has no database: the file-store equivalent applies — an
  isolated data directory per run, seeded from version-controlled fixture
  files. The rule is "production-identical storage behavior," not "a
  container for its own sake."
- **Non-containerizable stores:** some production engines cannot run in a
  container (managed-only services). The fallback is explicit, not silent:
  the project documents the closest faithful substitute (vendor emulator or
  nearest self-hostable engine), records the fidelity gap as a known
  limitation, and obtains operator approval for the exception. A project that
  cannot name its gap cannot claim this rule.

> This rule trades CI time and container cost for storage-behavior fidelity.
> Metric: seed coverage of documented past data-layer bugs, toward 100%;
> fixture-sanitization lint violations, toward 0.
> Scope: scope_driven = true. The project gives up the speed and simplicity
> of in-memory substitutes; it gains builds that fail on storage bugs before
> users find them. What the team ships faster: data-layer debugging against
> a faithful store instead of against a substitute that lies.

### Historical rule 3 — Stubs recorded / cadence as fleet law (not adopted)

- Any external API the service calls is replaced locally by a **stub server
  running on localhost** (WireMock, Hoverfly, Mountebank, or the stack-native
  equivalent).
- The service points at the stubs **through configuration, never through code
  changes**. If a base URL is hard-coded, adding the configuration seam is
  part of adopting this playbook.
- Stubs are built by **recording real responses from a test environment**,
  not written by hand. The record pipeline has three mechanical stages:
  1. **Record** — capture live responses.
  2. **Normalize** — replace timestamps, tokens, nonces, signed URLs, and
     any secrets with deterministic placeholders, and serialize canonically
     (sorted keys, fixed float formatting, normalized line endings), so
     re-running `record-stubs` against an unchanged API yields byte-identical
     recordings and identical captures diff clean.
  3. **Verify** — a lint enforces that every endpoint's recording set
     contains at least one success, one error, one slow, and one malformed
     response. Thresholds are project-defined and documented at adoption:
     "slow" means slower than the project's documented latency budget;
     "malformed" means failing the consumer's expected schema (the
     contract) — not merely differing from observed provider quirks. Failure-mode
     coverage is checked, not hoped for.
- Recordings are **committed to the repo**, so any change to them shows up in
  code review.
- **Freshness is a rule, not a hope.** Recorded stubs rot, so every
  recording carries a **captured-at timestamp and the external API's version
  identifier**, stored in the recording file itself. Re-recording is
  **required** on a defined cadence (set at adoption, documented in the
  project — e.g. every 30 days) **and** on any external-API version change.
  Providers without versioning or change announcements leave only the
  cadence trigger: up to one full cadence window of testing against stale
  stubs is a known residual, disclosed here rather than hidden.
  The harness **fails loudly** — hard red build, never a silent skip or an
  amber warning — when a recording is stale (past cadence or version
  mismatch) or missing. A suite that passes against absent stubs is lying;
  this rule makes *silent* staleness impossible.
- Freshness enforcement is split so the per-PR path stays hermetic. Per-PR
  CI checks staleness **without network access** — captured-at stamp versus
  the documented cadence, plus version-identifier match; stale or missing
  means a loud red build. The live probe (`record-stubs --verify` against
  the test environment) runs on a **schedule**, not per-PR: a per-PR live
  probe would reintroduce the external dependency this playbook exists to
  eliminate (sandbox outage → red CI, conflating environment failure with
  code regression). Known gap, acknowledged: between scheduled probes, an
  unannounced provider change is caught only at the next probe or at
  cadence expiry.
- Record/replay covers request-response APIs. Stateful or sessioned
  protocols that require freshness (challenge-response, some OAuth/device
  flows) cannot be replayed with deterministic placeholders: for those, the
  playbook permits reviewed, scripted dynamic stubs instead of recordings.
  The boundary is documented per endpoint; "not written by hand" applies
  where replay is possible.
- **Record targets are allowlisted.** `record-stubs` refuses to record
  against production URLs; the permitted test-environment targets are
  listed in configuration. This is the user-harm guard the playbook would
  otherwise lack: recordings are committed to the repo, so a misconfigured
  record run must be mechanically unable to capture real user data into git
  history. The `check-fixtures`-style lint also scans committed recordings
  for production hostnames and credential patterns.
- **No test environment?** Some providers offer no sandbox, a paid-only
  sandbox, or a test environment that requires production-adjacent
  credentials. The fallback mirrors Rule 2's: hand-authored recordings built
  from the provider's documentation, reviewed like code and labeled as an
  assumption (observed behavior was not captured) — or a documented adoption
  exception with operator approval. A project that cannot name its gap
  cannot claim this rule.
- **Secrets for re-recording** come from the project's existing secret store
  or environment variables — named in the README's contributor onboarding
  ("obtain a test key from <source>, export <VAR>"), never committed, never
  pasted into docs.

> This rule trades recording-maintenance burden for external-dependency
> determinism.
> Metric: stale or missing recordings, toward 0; endpoints missing any
> failure-mode recording, toward 0.
> Scope: scope_driven = false *if* the project already maintains stub or
> test-double infrastructure (assumption, labeled — the "negative net scope"
> claim rests on it). Otherwise scope_driven = true: adoption adds stub
> servers, the three-stage record pipeline, committed recordings, the
> failure-mode lint, and the re-record cadence — new ongoing scope, named
> here so it cannot bypass the human gate.

**Operator note (2026-09-18):** salvage adoption does **not** mandate stubs.
If a project opts into recorded stubs, only the loud-fail-on-stale/missing
behavior is carried onto the adopted face — not the scheduled re-record
cadence as fleet law, not the three-stage pipeline mandate, not failure-mode
lint as fleet law.

### Historical rule 4 — Two-layer contract tests (not adopted)

Two layers, in this order. The order matters: layer 2 without layer 1 is a
tautology.

- **Layer 1 — spec-anchored contracts.** The contract encodes the PROMISED
  interface as defined by the project's spec, epics, and stories — authored
  from the requirements (by hand or from spec tooling), never generated from
  the implementation. Tests assert that the implementation honors the
  promise. This is the layer that says something about *correctness*: the
  contract is an independent statement of what was supposed to be built.
  Where no spec/epics/stories exist as artifacts, the authored-and-reviewed
  contract itself becomes the promise record — but that downgrade is
  explicit and reviewed, never silent, and the adoption record notes the
  weakened evidence grade as a labeled limitation: correctness evidence is
  weaker when the promise originates on the implementation side.
- **Layer 2 — drift detection.** A snapshot of the interface is derived from
  the code on every build and compared against the **base-branch snapshot**
  — the snapshot committed on the branch the change merges into, not a
  snapshot regenerated in the same PR. Snapshot updates themselves land only
  in separately reviewed commits. Without baseline independence, the check
  compares new code against a snapshot derived from that same code — the
  exact tautology condemned above ("proves nothing changed, not that
  anything is correct"). A dependency upgrade that quietly changes
  serialization, routing, or response structure fails the build instead of
  reaching users. This layer says something about *stability*: it catches
  what changed.

Stated explicitly, because the confusion is common: **a contract generated
from code and asserted against the same code proves nothing changed, not
that anything is correct.** Layer 2 alone is a change detector, not a
correctness check. The playbook requires both layers; a project with only
the drift snapshot does not satisfy this rule.

> Layer 1 trades ongoing hand-authoring labor against spec churn for
> correctness evidence — this is the single largest adoption cost in the
> playbook, stated plainly rather than folded into "upkeep."
> Layer 2 trades build time for stability: quiet dependency changes fail
> the build instead of reaching users.
> Metric: spec-anchored contract coverage of promised endpoints, toward
> 100%; post-release shape-drift incidents, toward 0 (measured where
> attribution is possible; the drift-check red-build count is the leading
> proxy).
> Scope: scope_driven = false *if* the project already has contract tests
> or spec tooling (assumption, labeled). Otherwise scope_driven = true:
> hand-authoring layer-1 contracts from requirements is new authoring scope,
> named here so it cannot bypass the human gate.

### Historical rule 5 — Required ship-gate regression before merge (not adopted)

For a project that has adopted this playbook:

- The **complete** test suite runs against the local disposable stack.
- The **same** suite runs in CI as a **required check** on every pull
  request.
- A change that breaks the suite cannot merge.

> This rule trades merge latency for a hard red-suite gate.
> Metric: red-suite merges, toward 0.
> Scope: scope_driven = true. The project gives up the option of merging
> around a red suite; it ships fewer regressions. What the team ships
> faster: incident-free releases — fewer rollbacks, fewer hotfixes.

**Operator note (2026-09-18):** salvage adoption is recommended practice only;
it is **not** a required fleet ship gate and does not mandate a required CI
check once opted in.

### Historical acceptance criteria checklist (not adopted)

A project claims this playbook when all of the following hold. Each criterion
names its independent verifier — the worker never grades its own work.

- [ ] `stand-up`, `test-contract`, `test`, `record-stubs`, `tear-down` exist
      and are documented in the project's README or equivalent.
      Verifier: CI lint that the commands exist and the docs section exists
      — a smoke check only (presence is gameable; the behavioral proof is
      the next criterion).
- [ ] A fresh clone reaches green stand-up/test/tear-down on the first try,
      following only the documented prerequisites. Prerequisites are
      version-pinned in the docs ("install docker" is not a prerequisite;
      "docker >= 24.0" is). "No tribal knowledge" is demonstrated, not
      asserted: the run is performed by a contributor who did not author
      the setup, or by a scheduled CI fresh-clone job (defined cadence,
      e.g. weekly), and the run log is kept.
      Verifier: the second contributor's (or CI job's) run log.
- [ ] The data store is the production engine and version (or the isolated
      file-store equivalent, or an operator-approved documented fallback),
      seeded from a version-controlled sanitized snapshot; the
      `check-fixtures` lint is green.
      Verifier: CI (lint + suite), plus the seed provenance reviewed by the
      PR reviewer — someone other than the seed author.
- [ ] Every external API is stubbed on localhost via configuration only;
      recordings are normalized, committed, carry captured-at/version stamps,
      and pass the failure-mode lint; the re-record cadence is documented;
      `record-stubs --verify` is green on its schedule; a stale or missing
      recording fails the build loudly, never silently.
      Verifier: per-PR CI (lint + stamp/cadence check, no network) and the
      scheduled live-probe job.
- [ ] If `tear-down` itself fails partway (locked volume, wedged
      container), the audit step detects the residue and fails the build;
      remediation is a force-removal retry, then the project's documented
      operator cleanup runbook. Detection without a cleanup path is only
      half a criterion.
      Verifier: CI audit step plus the runbook's existence in the docs.
- [ ] Contract layer 1: contracts encode the promised interface as defined
      by the spec/epics/stories — authored from the requirements, never
      generated from the implementation — and cover every promised endpoint;
      the suite asserts the implementation honors them.
      Verifier: traceability from each contract to its spec/epic/story,
      reviewed by a reviewer other than the contract author (or the
      operator where no second reviewer exists).
- [ ] Contract layer 2: a code-derived interface snapshot is compared on
      every build; drift fails the build.
      Verifier: CI build log showing the drift check ran and passed.
- [ ] CI runs the full suite against the disposable stack as a required
      check; a red suite blocks merge.
      Verifier: the CI platform's required-checks configuration, reviewed
      by the operator.
- [ ] `tear-down` leaves nothing behind: no containers, volumes, stub
      processes, bound ports, or seeded files survive — including after a
      failed test run.
      Verifier: a post-teardown audit step in CI (list containers/volumes/
      processes/ports; fail on residue).

### Historical recommendation / Muse-skill invent (not adopted)

Adopt this as a **QA-domain playbook**: a new docs page under `docs/` (or a
section in the QA-domain material — maintainer's call on placement),
referenced from the QA harness's "What you own" list. This proposal adds no
constitutional rule and amends no constitution, calibration ledger, or
decision record. The engineer produces the playbook text and the reference
diff; the maintainer applies them. (Bots do not write the governance repo;
this proposal is the diff, the maintainer is the hand.)

Consider, as a follow-up decision, making a disposable-stack UAT run part of
the ship gate itself — "nothing ships without UAT on a disposable stack" —
so the acceptance gate the framework already requires runs on an environment
the gate can trust. That decision is scope_driven = true and is routed to the
operator below.

**Operator note (2026-09-18):** no skill file was invented; constitution
untouched; keep path remains this proposals file; ship-gate follow-up was
answered as recommended-not-required.

### Historical open questions (superseded by answers above)

1. Approve as a QA-domain playbook?
2. Placement: standalone docs page, or a section in existing QA-domain docs?
3. Ship-gate strength: recommended practice, or required gate alongside UAT?
   (scope_driven = true — a required gate trades ship velocity for
   environment trust. Metric: environment-attributed post-release incidents,
   down.)

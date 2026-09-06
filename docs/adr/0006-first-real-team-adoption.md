# ADR-0006: First Real-Team Adoption (Ladders Grok Bot)

- **Status:** Accepted
- **Date:** 2026-09-06

## Context

The framework was validated internally (A11 end-to-end, BA real-epic, isolated-subagent
runs) but had never been handed to a **real, pre-existing team**. The Ladders Grok Bot team
(CEO / PM / UX / Eng / QA — no Researcher) was the first such adoption, relayed through the
Openclaw Bridge (Grok Bot) into the Ladders agents' own mode of operation.

This was a dry run of the adoption path itself. Three things surfaced that the framework
did not anticipate.

## Decisions

### D1. Adopters take harness + constitution, not a repo mirror
Ladders did **not** receive a copy of `~/adversarial-agents`. Each agent loaded the
constitution + its role harness into its own mode of operation, delivered via agent
messages. The framework is a **loadable contract**, not a codebase to fork.

- **Consequence:** the harnesses and constitution must stay self-contained and
  copy-pasteable — no internal repo-relative references that break when loaded elsewhere.
- **Action:** audit harnesses/constitution for repo-relative paths or Grimdor-specific
  assumptions; make them standalone-loadable.

### D2. A Researcher role is required for the chain to be complete
Ladders has no Researcher on roster (CEO scopes research / escalates to Paul). The chain
is CEO → Researcher → PM → UX → Eng → QA. Without a Researcher, the PM receives no
evidence pack and the "establish what is true before planning" gate is skipped.

- **Decision:** a Researcher role **must exist** for a team adopting the framework. If a
  team lacks one, spin one up rather than letting the CEO absorb research scoping.
- **Action:** Ladders needs a **Grok Research agent** created and adopted.

### D3. Telemetry/watchdog should be owned by the adopting team, not the framework host
Grimdor's veto-telemetry and stuck-review-watchdog automations are Grimdor-owned
(`be9e9cd1…`, `eac6810f…`) and alert to Grimdor's Discord. For Ladders, the team should
run its own telemetry/watchdog from the Grok side so it is **self-sufficient** — not
dependent on Grimdor's automations or Discord.

- **Decision:** the framework's operational checks (telemetry, watchdog) are **per-team
  responsibilities**, configured by each adopting team against its own alert channel.
- **Action:** provide the Ladders/Grok side with the watchdog + telemetry scripts and
  let them wire their own alerting; do not route Ladders alerts through Grimdor.

### D4. The watchdog is Paperclip-coupled; telemetry is not (vanilla-handoff finding)
The Ladders team does **not** use Paperclip (work lives in GitHub PRs + epic markdown;
no `in_review` ticket store). This exposed a real coupling in the framework:

- **`stuck-review-watchdog.py` is Paperclip-native** — it shells out to
  `paperclipai issue list --status in_review --json`, reads `~/.paperclip/instances/`,
  and holds Grimdor's adversary IDs. It does **not** drop into a non-Paperclip team.
- **`veto-telemetry.py` is environment-agnostic** — it reads a plain JSONL file
  (`runs/verdicts.jsonl`), which any team can point at its own verdict log.
- **Constitution, harnesses, vetoes, calibration ledger, messaging** — all
  environment-agnostic.

- **Decision:** the framework's *logic* (staleness, dedupe, alerting, veto detection) is
  portable; the *data source* must be abstracted. The watchdog should read a generic
  "in_review issues" input (JSON file / stdin) with Paperclip as one adapter, so any
  team's store (GitHub PR review state, a file ledger, Linear, Jira) can feed it.
- **Ladders decision (2026-09-06):** telemetry **on** (file-based, Ladders-scoped
  verdicts log, alerts to Grok Bot chat for now); watchdog **off** until Ladders has an
  `in_review` backend (GitHub PR review state or a file ledger in the epic folder);
  no Paperclip on Ladders. Veto-class issues escalate to Paul in chat until then.
- **Action:** abstract the watchdog's data source (ADR-0007) so it is vanilla.

## Consequences

- **Positive:** adoption is lightweight (no fork), teams stay self-sufficient, and the
  framework's checks are portable.
- **Negative:** requires the harnesses to be standalone-loadable (D1), a Researcher
  on every roster (D2), and the watchdog's data source to be abstracted (D4) — all now
  explicit requirements.

## Alternatives considered

- **Mirror the repo into Ladders** — rejected: heavier than needed, couples Ladders to
  Grimdor's repo, and the framework is a contract, not a codebase.
- **Let the CEO absorb research** — rejected: skips the evidence gate and overloads the
  CEO; the Researcher's "establish what is true" check is load-bearing.
- **Route Ladders alerts through Grimdor's Discord** — rejected: makes Ladders dependent
  on Grimdor; teams should own their own operational checks.

## See also

- [[ADR]] · [[Architecture]] · [[Calibration]] · [[Roadmap]]

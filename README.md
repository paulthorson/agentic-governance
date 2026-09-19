# Agentic Governance

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

This project is free and open source under the [Apache License 2.0](LICENSE). No acceptance of any terms is required to use it. The Apache License is the only thing governing use of the software. See also [NOTICE](NOTICE).

A **bring-your-own-agent (BYOA)** governance **framework**: role harnesses, a directed production chain, constitutions, a calibration ledger, an MCP server, and a setup wizard. You bring agents you already run; the wizard maps them to roles and writes config.

Claims in this file trace to the [`docs/capability-report.md`](docs/capability-report.md); if you find a discrepancy, open an issue.

---

## Governance limits

This project is a set of **instructions, review tools, and a few code gates**. It is not a sandbox, not a compliance certification, and not a guarantee that agents will obey harness text. See [what “governance” does not mean](docs/capability-report.md#127-what-governance-does-not-mean).

## Operational warning

Running AI agents can spend money, exfiltrate data, modify systems, and cause harm. Operators are responsible for provider billing limits, network controls, secrets, and human oversight. **This software does not provide a safety guarantee.**

## Code vs instruction controls

| Kind | Examples (see capability report) |
|---|---|
| **Code** | Framework-unit spend refuse on gated MCP reviews; messaging egress only when `network_permission=allow`; approval checkpoints on listed subprocess/outbound/outside-write sites; MCP HTTP default bind `127.0.0.1` |
| **Instruction / process** | CEO pacing language; blind-review isolation; human-only veto clearing; append-only ledger norms |

Detail: [`docs/capability-report.md` §12.8](docs/capability-report.md#128-code-vs-instruction-controls-summary).

## Independent personal project

This is an independent personal project. It is not a product of, or endorsed by, any employer or cloud vendor unless separately stated by that party in writing.

---

## What you get

| Layer | Job | Evidence |
|---|---|---|
| **Constitution** (`constitution/`) | Written veto rules and domain law | Files in tree |
| **Harnesses** (`harnesses/`) | Role instructions (own / never / stop conditions) | Files in tree |
| **Chain** | Directed edges Research → PM → UX → Engineer → QA → CEO (documented) | Spec + harnesses |
| **Calibration ledger** (`ledger/`) | Precedent records (ordinary files) | Files in tree |
| **Config** (`config/`) | Wizard output: roster, budget units, network permission, alerts | Wizard writes; see capability report §12.1–12.3 |
| **Plugins** (`adversarial-*/`) | Adversary agents and skills | Files in tree |
| **Engine** (`mcp/` + `scripts/`) | MCP tools, wizard, tickets, watchdog, telemetry, messaging | capability report |

Telemetry and alerts are local unless the operator configures a destination; no destination ships configured; nothing is sent to the project author, ever.

**Plugins vs harnesses.** Plugins add adversary capabilities. Harnesses define roles. A plugin must not claim a role.

---

## Who is who (documented roles)

```
HUMAN
│ clears vetoes; applies governance diffs; owns provider billing
│
└── CHIEF OF STAFF (multi-team mode only) — human funnel (instruction)
    └── CEO BOT(s) — route, advise pacing, resolve by ledger precedent (instruction)
        └── RESEARCH → PM → UX → ENGINEER → QA
```

| Role | Owns (harness text) |
|---|---|
| Researcher | Evidence; does not recommend |
| PM | Problem brief with options |
| UX | User stories + rationale |
| Engineer | Code / diffs |
| QA | Test plans / gates |
| CEO | Routing, advisory resource pacing, precedent resolutions |
| Chief of Staff | Multi-team human funnel |

CEO “pacing” is **advisory** unless a gated MCP path refuses under the framework-unit meter ([§12.1](docs/capability-report.md#121-spend)).

---

## Spend (honest limits)

The framework can refuse gated MCP operations when recorded framework-visible units meet a wizard-configured numeric ceiling ([`spend.py`](mcp/adversarial_mcp/spend.py); [§12.1](docs/capability-report.md#121-spend)). This framework cannot see or limit what you spend with your model provider. Set a hard spending cap in your provider's billing console. This cap counts framework units only.

---

## Network and bind

- Wizard asks `network_permission`: `allow` | `deny` | `unknown`. **Unknown = no egress** ([§12.3](docs/capability-report.md#123-network-and-bind)).
- `scripts/messaging.py` delivers alerts only when permission is `allow` (and approval is present).
- MCP HTTP transport defaults to **`127.0.0.1`**. LAN bind requires explicit `--host` and prints a warning ([§12.3](docs/capability-report.md#123-network-and-bind)).

---

## Approval checkpoints

Listed subprocess / outbound / outside-write call sites refuse without `AG_APPROVAL=1`, `AG_APPROVAL_TOKEN` matching `runs/approval.token`, or `runs/approval.ok` ([§12.2](docs/capability-report.md#122-approval-checkpoints)). The operator creates `runs/approval.token`; the framework only reads it. On a successful token match, the framework best-effort `chmod 0600`s the file and prints a stderr warning if that chmod fails ([§12.10](docs/capability-report.md#1210-runsapprovaltoken-write--permissions)). Own-directory framework writes and agent runtimes outside these scripts remain **unchecked**.

---

## Install (framework)

**HOLD — authorized access only.** This GitHub repository is private. Anonymous visitors cannot open or clone it (the public repo URL returns 404). There is no public install path while the repository stays private. Do not treat the clone command below as a working path unless you already have authorized access.

If you have authorized access:

```bash
git clone https://github.com/paulthorson/agentic-governance.git
cd agentic-governance
cd mcp && uv sync && uv run adversarial-mcp # stdio (default)
```

Wire the MCP server into your agent, then run `setup_wizard_start` / `setup_wizard_answer`.

**Cos seating (install/setup — not deferred):** When the roster includes Chief of Staff (`cos`), the wizard **ASKS** Cos memory store mode (`private_git` OR `local_folder` — do not force one) and scaffolds from `docs/templates/cos-memory/` via the seating hook `mcp/adversarial_mcp/cos_memory_setup.py` (CLI stub: `scripts/cos_memory_setup.py`). operator + Cos clarified store = private git. See [`docs/onboarding/cos-seating.md`](docs/onboarding/cos-seating.md).

Onboarding guides: [`docs/onboarding/`](docs/onboarding/).

**Public face vs localhost:** Marketing homepage is [https://www.agenticgovernance.app](https://www.agenticgovernance.app) (site repo). The optional Next.js `dashboard/` app is **localhost-only** for operator/dev — **not required** to use the framework ([§7.3](docs/capability-report.md#73-dashboard-required)), and this framework repo must **not** bind a Vercel project to `dashboard/`.

Historical gap analysis lives under [`docs/quarantine/`](docs/quarantine/) (not live Class A SoT).

---

## Setup wizard (BYOA)

Conversational via MCP tools. Asks runtime, engine, budget model (framework units), roster, **Cos memory (when Cos is seated — install-time ASK)**, adversaries, escalation, quiet hours, autonomy, retries, research bounds, irreversible-action protection level, **network permission**, alert channel, and data-source paths. Writes `config/setup.md`, `config/roster.md`, persona blocks, and (when Cos is seated) `config/cos-memory/`.

**Reconcile, never layer** when adopting existing agents. **Re-runnable.** Agents absent from the roster are outside this framework’s config — the framework cannot introspect arbitrary runtimes.

---

## Adversaries (judges)

Adversaries are instructed to review **blind** (neutral facts, not the worker’s pitch) and to treat customer-harm vetoes as human-cleared only. That isolation is **process/instruction**, not a cryptographic wall ([§12.7](docs/capability-report.md#127-what-governance-does-not-mean)).

Domains ship under `adversarial-*/` (UX, engineer, QA, researcher, universal, prompt, security, privacy, compliance, product, ops, docs). Counts change as plugins are added; trust the tree and `scripts/validate.py`, not a marketing number.

---

## Documentation

| Doc | What |
|---|---|
| [`docs/capability-report.md`](docs/capability-report.md) | **What code actually does** (source of truth for capability claims) |
| [`docs/claim-alignment-plan.md`](docs/claim-alignment-plan.md) | Claim alignment plan |
| [`docs/Home.md`](docs/Home.md) | Wiki entry |
| [`docs/agentic-governance-spec.md`](docs/agentic-governance-spec.md) | Framework spec (includes advisory sections) |
| [`docs/spec-addendum-01.md`](docs/spec-addendum-01.md) | Addendum |
| [`docs/deployment.md`](docs/deployment.md) | Remote MCP |
| [`docs/adr/`](docs/adr/) | Architecture decisions |
| [`SECURITY.md`](SECURITY.md) | Reporting + security model (honest) |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | DCO + contribution rules |

---

## Tooling & CI

- `scripts/validate.py` — structure validator; `git apply --check` on patches requires approval when patches exist
- `.github/workflows/validate.yml` — validate + tests + gitleaks
- `scripts/messaging.py` — alerts (network permission + approval)
- `scripts/approval.py` — approval checkpoints
- `mcp/adversarial_mcp/spend.py` — framework-unit meter

---

## License

[Apache License 2.0](LICENSE). See also [NOTICE](NOTICE).

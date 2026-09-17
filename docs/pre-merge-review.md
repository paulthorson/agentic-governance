# Pre-merge review pack (PR #62)

Author review artifact. PR stays **DRAFT**. Do not merge from this note alone.

Updated for operator LOCK — AG PUBLIC RELEASE EXECUTE (items 2–6). Settled posture is FINAL.

**Final batch (operator LOCK):** §12.9 OLLAMA loopback distinction; README telemetry/approval/`approval.token` clarity + stranger-facing language; `SECURITY.md` contact `security@agenticgovernance.app` + GitHub private reporting; stale `DISCORD_WEBHOOK_URL` docstring fix; calibration proximate-cause sentence. PR remains **DRAFT**.

---

## §1 Findings (items 2–6)

### 2 — Remove Extra use-governor documents documents

| Action | Result |
|---|---|
| Delete `` | **Deleted** |
| Delete `` | **Deleted** |
| Delete `docs/legal/` if empty | **Removed** (directory gone) |
| Replacements | **None** (standing rule) |

**Files that referenced them (and what changed):**

| File | Change |
|---|---|
| `docs/README.md` | Removed Get AG index rows; pointed at capability-report / pre-merge pack |
| `docs/initiatives/README.md` | Removed Terms links; settled posture (no acceptance gate) |
| `docs/initiatives/marketing-site-split.md` | Removed outline link; no acceptance gate |
| `docs/initiatives/marketing-site-extract-plan.md` | Superseded acceptance-gate HOLD; removed outline paths |
| `docs/initiatives/marketing-site-extract-execute.md` | Superseded T&Cs HOLD; removed outline paths |
| `docs/initiatives/anonymous-improve-feedback.md` | Removed outline link; no acceptance gate |
| `dashboard/README.md` | HOLD banner: look pixels only; Terms drafts removed |
| `docs/capability-report.md` §12.7 item 7 | Removed “Get AG docs are separate DRAFT” |
| `CHANGELOG.md` | Added Removed entry; marked prior Terms bullets historical (paths removed) |
| `docs/pre-merge-review.md` | This pack; Item 10 → deleted |

### 3.1 — Telemetry (author-control check)

**Verdict: No data reaches a destination the repository author operates or receives from by default.** Outbound alert destinations are operator-supplied only. Loopback defaults on the operator machine do not change that verdict.

| Question | Answer |
|---|---|
| Default Discord webhook URL in `scripts/messaging.py` (verbatim) | `""` — `ALERT_WEBHOOK_URL = os.environ.get("ALERT_WEBHOOK_URL", "")` at `scripts/messaging.py:41` |
| What `scripts/veto-telemetry.py` sends | On `--watch` (not `--dry-run`): veto alert string via `messaging.send_alert` (domain, verdict, ticket, rule, hits). Without `--watch`: local report/JSON/stdout only |
| Where it sends | Only via `messaging.send_alert` → operator `ALERT_WEBHOOK_URL` and/or `ALERT_COMMAND`, and only if `network_permission=allow` **and** approval present |
| Author-controlled / off-machine default destination? | **None.** `ALERT_*` defaults at `messaging.py:40–43` are all `""` — nothing points outside the operator's machine or to the author |
| Non-empty default in tree (loopback only) | `OLLAMA_URL` → `http://localhost:11434` at `mcp/adversarial_mcp/server.py:433` — operator machine only |

**Non-empty default destination URLs in tree (verbatim):**

| File:line | Default |
|---|---|
| `mcp/adversarial_mcp/server.py:433` | `OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")` — **local loopback only**, not author-operated remote |
| Discord/Slack webhook URL hardcoded as non-empty default | **None found** |

Capability-report **§12.9** is the standing telemetry section. Final-batch rewrite distinguishes (a) no off-machine/author default vs (b) the one loopback default.

### 3.2 — NOTICE / `[BRACKET]` placeholders

`NOTICE` filled by operator: copyright holder named in `NOTICE`, 2026. `SECURITY.md` contact is `security@agenticgovernance.app`. **No** remaining unfilled `[AUTHOR …]` / WILL-BE-SUPPLIED authoring placeholders in shipped release files.

Not counted: wiki `[[.]]`, skill tags, markdown links, Apache LICENSE bracket terms.

### 3.3 — README work-instruction numbering

No `11.1`–`11.4` (or other work-instruction numbering) in README headings. Capability-report § cites elsewhere remain intentional.

### 3.4 — Claim table row 18 / uncertainty markers

`test_gitignore_excludes_env_and_pem` in `tests/test_published_claims.py` asserts `.gitignore` contains `.env` and `*.pem`. Claim table row 18 cites that test. **No** deliverable uncertainty markers (`rewrote?`, TBD-as-status, UNKNOWN-as-deliverable-status) remain in the claim table / this pack / capability-report for this pass. (`UNKNOWN` as a factual capability answer, e.g. network permission option, is intentional.)

### 3.5 — Git identity durability

**Does not survive a fresh VM.** `~/.gitconfig` / process env on one Cloud Agent session do **not** ship with this branch or this repo. Every future session must set identity on the host before committing if specific authorship is required. What would make it survive: durable host/org Cloud Agent environment config outside this repository (not implemented in-repo; no `.gitconfig` in tree).

### 3.6 — Capability report §12.4 rows 5.1 / 5.2

Rewritten: no in-tree identity config; committing agent identity comes from host environment, outside this repository and not controlled by it. Cite: `tests/test_published_claims.py:168–211`.

### 3.7 — Line cites

| Cite | Lines |
|---|---|
| stuck-review-watchdog paperclipai gate | `scripts/stuck-review-watchdog.py:116–121` (`require_approval` at `:119`) |
| calibration-report `emit()` | `scripts/calibration-report.py:100–119` (`require_approval` at `:119`) |
| setup_wizard `network_permission` in WIZARD_FLOW | `mcp/adversarial_mcp/setup_wizard.py:229–233` (`id` at `:230`) |
| 12.4 identity grep | `tests/test_published_claims.py:168–211` |

### 3.8 — `runs/approval.token`

| Question | Answer |
|---|---|
| Who writes it? | **Framework never writes it.** Operator creates. Code reads when `AG_APPROVAL_TOKEN` set (`scripts/approval.py:42–50`) |
| Permissions | Operator umask on create. On read, best-effort `chmod 0o600` if group/world bits set (`approval.py:65–84`) |
| Other local users? | Yes if left group/world-readable until tightened; warn on stderr if chmod fails |

### 3.9 — SECURITY.md + CONTRIBUTING.md

Full current text embedded below (Items 9 / 9b). Eight SECURITY.md line cites for operator review are in that embed.

### 4 — Calibration ledger

| | |
|---|---|
| Path | `ledger/calibration-ledger.md` |
| Entry | `2026-09-14 — COUNSEL_GATE (site [redacted])` |
| Gap named | Instruction-only counsel gate in deleted outline §11.4; `LIVE_SOT_MERGED_SHA` still draft (`harnesses/chief-of-staff.md:178–184`); site PR #3 merged despite HOLD/DRAFT; no AG constitution rule for [redacted] |
| Rule proposed | `COUNSEL_GATE_BEFORE_PROD` — **not implemented** in this PR |

### 5 — Release files

| File | Status |
|---|---|
| `LICENSE` | Apache 2.0 verbatim; no prepended copyright |
| `NOTICE` | NOTICE present, copyright holder named in `NOTICE`, 2026 |
| `CONTRIBUTING.md` | DCO via `git commit -s` documented |
| `README.md` | Near top: free/open source Apache 2.0; no acceptance required; LICENSE only governor |

### 6 — Clean-clone verification

See **§6 Clean-clone** at the end of this pack (filled after stranger-path run).

---

## 5.1 Complete current README.md

~~~~markdown
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

```bash
git clone https://github.com/paulthorson/agentic-governance.git
cd agentic-governance
cd mcp && uv sync && uv run adversarial-mcp # stdio (default)
```

Wire the MCP server into your agent, then run `setup_wizard_start` / `setup_wizard_answer`.

Onboarding guides: [`docs/onboarding/`](docs/onboarding/).

The optional Next.js `dashboard/` app is **not required** to use the framework ([§7.3](docs/capability-report.md#73-dashboard-required)).

---

## Setup wizard (BYOA)

Conversational via MCP tools. Asks runtime, engine, budget model (framework units), roster, adversaries, escalation, quiet hours, autonomy, retries, research bounds, irreversible-action protection level, **network permission**, alert channel, and data-source paths. Writes `config/setup.md`, `config/roster.md`, and persona blocks.

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
~~~~

## 5.2 Complete current docs/capability-report.md

~~~~markdown
# Capability report — Agentic Governance (facts at HEAD of this PR)

Facts only. Citations are `file:line`. Where something is not implemented or not
observable from this repo, the answer is **NO** or **UNKNOWN** — never inferred.

Governing principle applied: text in a spec is guidance; only code that refuses
or gates is enforcement.

---

## 12.1 Spend

| Question | Answer | Cite |
|---|---|---|
| Does any code meter model-provider tokens or dollars? | **NO** | `mcp/adversarial_mcp/spend.py:1–14` (module docstring states limits) |
| Does any code refuse at a configured numeric cap for framework-recorded units? | **YES** | `spend.py:181–198` `refuse_if_over_cap`; wired at `server.py:384–387`, `server.py:492–495` |
| Where is usage recorded? | `runs/spend-ledger.jsonl` | `spend.py:41–44`, `spend.py:130–148` |
| Does the meter see Claude/Cursor/OpenAI billing? | **NO** | `spend.py:7–11`; `spend_status` sets `provider_dollars_metered: False` (`spend.py:210–216`) |
| Wizard tells operator only hard $ limit is provider console? | **YES** | `setup_wizard.py` `SPEND_UNIT_QUALIFIER` on numeric prompts; written under `## Spend honesty` at `setup_wizard.py:404–406` |
| CEO/harness “hard stop” as code enforcement of agent halt? | **NO** — advisory text | `harnesses/ceo.md` Resource pacing (advisory language); agents outside gated MCP entrypoints unchecked |
| Per-bot dollar attribution implemented? | **NO** | Spec/addendum rewritten to say framework-visible units only |

---

## 12.2 Approval checkpoints

| Question | Answer | Cite |
|---|---|---|
| Shared approval helper exists? | **YES** | `scripts/approval.py:87–105` `require_approval` |
| How is approval granted? | `AG_APPROVAL=1`, or `AG_APPROVAL_TOKEN` matching `runs/approval.token`, or `runs/approval.ok` | `approval.py:6–10`, `36–60` |
| `validate.py` `git apply --check` gated? | **YES** when `.diff`/`.patch` files exist | `scripts/validate.py:146–157` |
| Messaging outbound gated by approval? | **YES** (after network allow) | `scripts/messaging.py:146–153` |
| `paperclipai` subprocess gated? | **YES** | `scripts/stuck-review-watchdog.py:116–121` (`require_approval` at `:119`) |
| Ollama `urlopen` gated? | **YES** | `server.py:445–450` |
| Outside-repo `calibration-report --output` gated? | **YES** | `scripts/calibration-report.py:100–119` `emit()` (`require_approval` at `:119`) |
| Own-dir writes (`runs/`, `config/`, plugins) gated? | **NO** | By design — reversible / expected |
| Dashboard Google OAuth gated by this helper? | **NO** — separate deploy surface | `dashboard/src/auth.ts:9–37` |
| Arbitrary agent shells outside these scripts gated? | **NO** | Unchecked |

---

## 12.3 Network and bind

| Question | Answer | Cite |
|---|---|---|
| Wizard asks network permission? | **YES** | `mcp/adversarial_mcp/setup_wizard.py:229–233` (`id: network_permission` at `:230` in `WIZARD_FLOW`) |
| Options | `allow` \| `deny` \| `unknown` | `setup_wizard.py:40` `NETWORK_PERMISSIONS` |
| UNKNOWN / missing → egress? | **NO** (no egress) | `messaging.py:78–80`; `load_network_permission` default `unknown` at `messaging.py:57–58`, `75` |
| Messaging respects permission? | **YES** | `messaging.py:134–141` |
| MCP HTTP default bind | `127.0.0.1` | `server.py:660–662`, `689` |
| LAN bind | Explicit `--host 0.0.0.0` (etc.) + stderr warning | `server.py:681–688` |
| Stdio transport default? | **YES** | `server.py:656–657` |

---

## 12.4 Identity (report-only items)

| Question | Answer | Cite |
|---|---|---|
| 5.1 In-tree configs that SET `user.name` / `user.email` / `GIT_AUTHOR*` / `GIT_COMMITTER*` | **No in-tree identity config exists.** The committing agent's identity comes from its **host environment** (e.g. `~/.gitconfig`, process env), outside this repository and not controlled by it. | Repo-wide grep + `tests/test_published_claims.py:168–211` (`test_no_git_identity_config_uses_non_noreply_email`) |
| 5.2 Changes made in-repo | **None in-tree** — host-side git identity is outside this repository and not controlled by it. Not a repository fix. | Same; durability row below |
| Git identity durability across fresh environments | **Does not survive a fresh Cloud Agent / ephemeral VM.** Setting `~/.gitconfig` (ephemeral host) (or `GIT_AUTHOR_*` / `GIT_COMMITTER_*`) on one session does **not** ship with this branch or this repo. Every future session must set identity on the host before committing if operator / noreply authorship is required. This is **not** fixed by this PR. | Host filesystem only; no `.gitconfig` / identity setter in tree |
| 5.3 Personal allowlist email (historical) | Was in allowlist; **removed** from functional code, tip prose, and git history (placeholder `noreply address` / `ADMIN_EMAILS`) | `admin-access.ts` now env-only; history scrub note |
| Personal phone numbers in tree | **NO** found | Repo-wide grep (no matches) |
| 5.4 Prior personal GitHub username URL | HTTP **404** (2026-09-14 probe); tip + history scrubbed to `prior username` | Read-only `curl -sI`; history scrub note |
| History rewrite / `.mailmap` | **Done** 2026-09-16 (operator GO): `git-filter-repo` on `main` | `docs/history-identity-scrub-2026-09-16.md` |

---

## 12.5 License and dependencies

| Question | Answer | Cite |
|---|---|---|
| LICENSE text | Exact Apache-2.0 from upstream (no prepended copyright line) | `LICENSE` |
| NOTICE | NOTICE present, copyright holder named in `NOTICE`, 2026. | `NOTICE` |
| MCP direct deps | `mcp>=1.0.0,<2`, `pydantic>=2.0` | `mcp/pyproject.toml:6–9` |
| Resolved Python licenses (local metadata) | mcp MIT; pydantic MIT; uvicorn/starlette/httpx BSD-3-Clause; certifi **MPL-2.0**; cryptography Apache-2.0 OR BSD-3-Clause; python-multipart Apache-2.0; typing-extensions PSF-2.0 | `importlib.metadata` after install |
| GPL / AGPL in MCP set | **NO** found | — |
| Dashboard `sharp-libvips*` | **LGPL-3.0-or-later** in lockfile | `dashboard/package-lock.json` (e.g. line 839+) |
| LGPL obligation (sharp / libvips) | Distributing **binaries** that link LGPL libvips may require providing corresponding source / relink rights under LGPL-3.0-or-later. Source-only consumers of this repo who never ship those native binaries are not distributing the LGPL object. **Operator/redistributor must verify** their own distribution form. | Lockfile license field; |

---

## 12.6 Secrets, dashboard, site

### 7.1 History / credentials

| Question | Answer | Cite |
|---|---|---|
| `dashboard/.env.example` AUTH values | Empty placeholders (`AUTH_SECRET=`, `AUTH_GOOGLE_ID=`, `AUTH_GOOGLE_SECRET=`) | `dashboard/.env.example:4–9` |
| Commit that added them | `1bfa1a5` — empty values only | git history |
| Real credentials committed in those env keys | **NO** evidence in example file | Same |
| Admin token pages | Admin UI under `/admin/tokens` shows **placeholder KPI copy** (“Baseline / unpaid”); not live provider tokens | `dashboard/src/components/AdminTokens.tsx` (placeholder posture documented in dashboard README) |

### 7.2 NextAuth Google

| Question | Answer | Cite |
|---|---|---|
| Deployer must supply | `AUTH_SECRET`, `AUTH_GOOGLE_ID`, `AUTH_GOOGLE_SECRET`, and `ADMIN_EMAILS` (Google emails; empty = nobody) | `dashboard/.env.example`; `dashboard/README.md` |
| Default secret in repo | **NO** — empty `AUTH_*` example | `.env.example` |
| Stores what where | Auth.js/NextAuth session cookies on the deployed host (Auth.js defaults); allowlist from `ADMIN_EMAILS` only | `dashboard/src/auth.ts`; `admin-access.ts` |
| Hardcoded allowlist email | **NO** — empty hardcoded list; fail closed | `admin-access.ts` |

### 7.3 Dashboard required?

| Question | Answer | Cite |
|---|---|---|
| Required to run the governance framework (MCP/scripts/harnesses)? | **NO** | Root install path uses `mcp/` + scripts; dashboard is separate Next app |
| Optional marketing/admin face? | **YES** | `dashboard/README.md`; root README marketing-face note |

### 7.4 Deployed site / routes / storage / analytics / clone builds

| Question | Answer | Cite |
|---|---|---|
| In-repo app routes | `/`, `/admin`, `/admin/login`, `/admin/reports`, `/admin/traction`, `/admin/tokens`, `/admin/cycle-time`, `/admin/scars`, `/api/auth/[.nextauth]` | `dashboard/src/app/**` |
| Input | Google OAuth on admin login; public pages render content | `auth.ts`; `app/page.tsx` |
| Storage | Traction/improve content from repo files / synced content; no first-party DB module found in dashboard src for AG data | `dashboard/data/`, `docs/improve` sync script |
| Cookies | Auth.js session cookies when admin SSO used; no custom cookie module found in `dashboard/src` | Grep: no `cookie` hits under `dashboard/src` |
| Analytics (gtag/plausible/segment) | **NO** matches under `dashboard/src` | Grep |
| Clone-build deps that commonly break cold clones | `dashboard` needs `npm install` including the localhost dashboard UI kit packages, `next`, `next-auth`; `prebuild` runs `sync-improve.mjs`. MCP needs `uv`/`pip` for `mcp`+`pydantic`. Native **sharp**/libvips platform packages may fail on unsupported OS/arch. | `dashboard/package.json:7–25`; lockfile sharp entries |

---

## 12.7 What “governance” does **NOT** mean

At HEAD, this repository’s “governance” does **not** mean:

1. A technical sandbox that prevents agents from running arbitrary tools outside these scripts.
2. A meter of real cloud LLM spend or a hard dollar stop inside this repo.
3. A guarantee that vetoes cannot be cleared by editing files (clearing is process + human convention).
4. Blind-review isolation enforced by a runtime wall (advocates are instructed not to see rationale; tools do not cryptographically separate channels).
5. Append-only ledgers enforced by WORM storage (files are ordinary writable files).
6. That installing this repo makes third-party agents safe by default.
7. Legal advice, Terms of Service, warranty, indemnity, or liability coverage beyond what Apache-2.0 LICENSE + NOTICE already state (no separate Terms documents in this repository).
8. That the optional dashboard is part of the control plane for agent spend/network.

Governance **does** mean (what code/docs actually provide): role harnesses and constitutions as instructions; MCP review/veto tooling; wizard-written config; framework-unit spend refuse on gated MCP paths; approval gates on listed call sites; network deny-by-default for messaging egress; loopback HTTP default.

---

## 12.8 Code vs instruction controls (summary)

| Control | Kind | Evidence |
|---|---|---|
| Framework-unit spend refuse | **Code** | `spend.py` + `server.py` gates |
| Messaging egress | **Code** | `messaging.py` network + approval |
| `git apply` in validate | **Code** | `validate.py` + `approval.py` |
| Ollama generate | **Code** | `server.py` approval |
| Uvicorn bind default | **Code** | `server.py:662` |
| CEO pacing / halt language | **Instruction** | harness/spec |
| Blind review / human-only veto clear / append-only | **Instruction + process** | constitutions, SECURITY model text |
| Irreversible-action levels 1–3 from wizard | **Config recorded; not fully enforced for all agent actions** | wizard writes level; only listed script sites checkpointed |

Unchecked (document in SECURITY): dashboard OAuth deploy surface; agent runtimes not calling gated scripts; absolute path writes if operator points config outside repo without hitting a gated helper; model-provider billing.

---

## 12.9 Telemetry and outbound destinations (author-control check)

**Verdict: No data reaches a destination the repository author controls by default.** Outbound alert destinations are **operator-supplied only**. There is **no** non-empty default webhook URL or author-owned endpoint in tree. Loopback defaults on the operator machine do not change that verdict.

| Question | Answer | Cite |
|---|---|---|
| Default Discord / alert webhook URL in `scripts/messaging.py` | **Empty string** `""` — operator must set `ALERT_WEBHOOK_URL` | `scripts/messaging.py:41` (`ALERT_WEBHOOK_URL = os.environ.get("ALERT_WEBHOOK_URL", "")`) |
| Default `ALERT_CHANNEL` / `ALERT_COMMAND` / `ALERT_TO` | All default to `""` | `messaging.py:40–43` |
| What `scripts/veto-telemetry.py` sends | On `--watch` (and not `--dry-run`): a veto alert string via `messaging.send_alert` (domain, verdict, ticket, rule, hits). Without `--watch`, local report/JSON/stdout only — **no** outbound send. | `veto-telemetry.py` (`send_alert` in `--watch` path); gates in `messaging.py` |
| Where it sends | Only through `messaging.send_alert` → operator `ALERT_WEBHOOK_URL` (Discord) and/or `ALERT_COMMAND`, and only if `network_permission=allow` **and** approval present. Env names are messaging/`ALERT_*` (and optional `NETWORK_PERMISSION`). | `veto-telemetry.py` (calls `send_alert`); `messaging.py:126–163`; gates at `:134–153` |
| Non-empty default destination authored into this repo? | **(a)** No default destination points **outside** the operator's machine or **to the author** — `ALERT_*` defaults are all `""`. **(b)** One non-empty default exists: `OLLAMA_URL` → `http://localhost:11434` (`mcp/adversarial_mcp/server.py:433`) — **loopback only**, operator machine. | `messaging.py:40–43`; `server.py:433` |
| Fallback helper path | Optional local helper `REPO_ROOT.parent / ".openclaw/workspace/scripts/post-to-discord.py"` **if that file exists on the operator host** — not shipped in this repo; not an author-controlled remote URL. | `messaging.py:97–108` |

---

## 12.10 `runs/approval.token` (write / permissions)

| Question | Answer | Cite |
|---|---|---|
| Who writes `runs/approval.token`? | **This framework never writes it.** Only the operator creates it. Code **reads** it when `AG_APPROVAL_TOKEN` is set. | `scripts/approval.py:42–50` (read only); no `write`/`open(.,"w")` of `approval.token` in tree |
| Default file permissions | Whatever the operator’s umask / create mode produced. Not set by framework create (there is no create). | Operator host |
| Can other local users read it? | **If** the operator left group/world bits set, yes — until tightened. On successful token match path, `has_approval` calls `_tighten_secret_file` which attempts `chmod 0o600` when group/world bits are present; if chmod fails, warns on stderr that other local users may read the token. | `approval.py:46`, `65–84` |
| World-readable by design? | **No.** Best-effort tighten to `0600` on read; cannot guarantee on foreign-owned / unsupported FS. | Same |
~~~~

---

## 5.3 Claim-to-test table (README / SECURITY / CONTRIBUTING)

Only factual does / does-not / enforces / refuses / defaults / requires claims.
Scope notes (Governance scope note / Operational warning / Code vs instruction /
Independent personal project, unpaid/personal, DCO process text) are listed as
NOTE (not product capability). Work-instruction heading numbers (11.1–11.4)
were stripped from the published README.

| # | Claim (quoted) | Docs file:line | Code file:line | Test |
|---|---|---|---|---|
| 1 | Framework-unit spend refuse on gated MCP reviews | README.md:23,77 | mcp/adversarial_mcp/spend.py:181–198; server.py run_review/run_review_deep gates | test_spend_enforcement_refuses_at_cap; test_spend_status_and_refuse_include_qualifier |
| 2 | messaging egress only when network_permission=allow | README.md:23,83–84 | scripts/messaging.py:78–80,134–141 | test_wizard_unknown_network_permits_no_egress; test_messaging_blocks_without_network_allow_even_if_approved |
| 3 | approval checkpoints on listed sites | README.md:23,91 | scripts/approval.py:87–105; validate/messaging/stuck-review/server/calibration | test_approval_checkpoints_block_without_approval; test_messaging_blocks_without_approval_when_network_allow |
| 4 | MCP HTTP default bind 127.0.0.1 | README.md:25,87 | mcp/adversarial_mcp/server.py:660–662,689 | test_uvicorn_default_bind_is_loopback |
| 5 | Unknown network = no egress | README.md:87 | scripts/messaging.py:57–58,75,78–80 | test_wizard_unknown_network_permits_no_egress |
| 6 | Spend meter cannot see/limit provider $; provider console is hard $ cap; cap = framework units | README.md:81 | spend.py SPEND_UNIT_QUALIFIER; setup_wizard.py SPEND_UNIT_QUALIFIER | test_spend_qualifier_adjacent_on_numeric_wizard_prompts; test_spend_status_and_refuse_include_qualifier |
| 7 | Own-dir writes / outside scripts remain unchecked | README.md:95 | (negative: no gate) documented | scope/negative — no positive gate to regress; left as honest gap |
| 8 | stdio is default MCP transport | README.md:104 | server.py:656–657 | test_stdio_is_default_transport |
| 9 | dashboard not required for framework | README.md:111 | mcp/pyproject.toml; server.py (no dashboard import) | test_dashboard_not_required_by_mcp_package |
| 10 | Wizard asks network_permission allow\|deny\|unknown | README.md:87,117 | setup_wizard.py:230 / NETWORK_PERMISSIONS | test_wizard_unknown_network_permits_no_egress |
| 11 | git apply --check requires approval when patches exist | README.md:149 | scripts/validate.py:146–157 | test_approval_checkpoints_block_without_approval |
| 12 | Apache License 2.0 LICENSE (no prepended copyright) | README.md:159 | LICENSE | test_license_is_apache_without_prepended_copyright |
| 13 | Spend refuse at configured numeric cap | SECURITY.md:46 | spend.py + server.py | test_spend_enforcement_refuses_at_cap |
| 14 | Messaging egress only if allow; unknown/deny = no egress | SECURITY.md:47 | messaging.py | test_wizard_unknown_network_permits_no_egress; test_messaging_blocks_without_network_allow_even_if_approved |
| 15 | Approval checkpoints refuse without approval | SECURITY.md:48 | approval.py | test_approval_checkpoints_block_without_approval |
| 16 | HTTP bind default 127.0.0.1 | SECURITY.md:49 | server.py | test_uvicorn_default_bind_is_loopback |
| 17 | dashboard/.env.example AUTH_* empty placeholders | SECURITY.md:62 | dashboard/.env.example | test_no_shipped_config_contains_real_credential |
| 18 |.gitignore excludes.env / *.pem | SECURITY.md:61 |.gitignore:29–30 | test_gitignore_excludes_env_and_pem |
| 19 | Empty ADMIN_EMAILS = nobody (fail closed); no personal hardcoded allowlist | dashboard README / capability report | admin-access.ts | test_admin_allowlist_empty_is_fail_closed_and_no_personal_default |
| 20 | No personal email in functional config/defaults | (this pack §1.5) | admin-access,.env.example, mcp, scripts, tests,.github | test_no_personal_email_in_functional_config_defaults |
| 21 | Blind-review / human veto / append-only are instruction/process not walls | README.md:26,125; SECURITY.md:30–36 | constitutions (text) | NOTE — rewritten as instruction; no code wall claimed |
| 22 | This software does not provide a safety guarantee | README.md:19; SECURITY.md:23 | N/A scope note | NOTE |
| 23 | Independent personal / unpaid project | README.md:30; SECURITY.md:5; CONTRIBUTING.md:3 | N/A scope note | NOTE |
| 24 | DCO requires git commit -s | CONTRIBUTING.md:8–16 | process | scope/process — not a runtime claim |

### Counts (4.4)

| Metric | Count |
|---|---|
| Total factual capability claims enumerated | 20 (+ 4 scope/process) |
| With automated tests | 19 |
| New tests written this pass | `test_gitignore_excludes_env_and_pem` (row 18); prior pass added 9 methods |
| Claims rewritten (instruction not code) | 1 cluster (blind/veto/append-only already advisory) |
| Claims cut (untraceable product claim) | 0 this pass |
| Uncertainty markers remaining in this deliverable | **None** (`rewrote?` removed; no `???` / unresolved authoring markers in claim table, this pack, or capability-report) |

### Cuts considered

- No additional README product claims cut this pass; prior PR already removed “mechanical governance” / fake hard-stop language.
- Personal email / prior-username tip prose scrubbed to redacted placeholders; full history rewrite completed 2026-09-16 (operator GO) — see `docs/history-identity-scrub-2026-09-16.md`.
- README work-instruction numbers 11.1–11.4 stripped from headings; remaining §12.x / §7.x cites point at capability-report sections (intentional).

---

---

## 5.4 Answers

### 1.1 Allowlist controls / read site / empty behavior

- **Controls:** which Google account emails may `signIn` / pass middleware / admin layouts for `/admin/*`.
- **Read at:** `dashboard/src/lib/admin-access.ts` (`envAdminEmails`, `adminAllowlist`, `isAdminEmail`); called from `dashboard/src/auth.ts`, `middleware.ts`, admin pages.
- **Empty behavior (after fix):** **fail closed — nobody.** Empty/missing `ADMIN_EMAILS` → `[]` → `isAdminEmail` returns false.

### 1.3 Can `paulthorson@users.noreply.github.com` work as Google OAuth login?

**No.** Google OAuth returns a Google account email. `users.noreply.github.com` is not a Google identity. Allowlist therefore ships **without** a hardcoded address; deployer must set `ADMIN_EMAILS` to real Google account email(s). Documented in `dashboard/README.md` and `.env.example`.

### 1.5 Grep lists

**Functional (fixed):**

| Was | Action |
|---|---|
| `dashboard/src/lib/admin-access.ts` hardcoded `noreply address` | Removed; env-only |
| `dashboard/.env.example` `ADMIN_EMAILS=` personal address | Placeholder `you@example.com` |
| `dashboard/README.md` / login page hardcoded references | Rewritten |
| `dashboard/src/app/admin/login/page.tsx` PRIMARY_ADMIN_EMAIL | Removed |

**Incidental prose (tip scrubbed; history rewrite done 2026-09-16):**

| Location | Note |
|---|---|
| `CHANGELOG.md` | Historical allowlist → `ADMIN_EMAILS` / no personal address |
| `docs/claim-alignment-plan.md` | Audit note → redacted placeholders |
| `docs/capability-report.md` | Historical/5.3 / 5.4 notes redacted |
| Prior personal GitHub username / noreply | Tip scrubbed to `prior username` |
| Git commit author history | Not rewritten |

**Phone / home / personal id in functional positions:** none found.

### 2.2 Git identity source (before → after) — durability

| Source | Before | After |
|---|---|---|
| `~/.gitconfig` (ephemeral host) `user.name` | `Cursor Agent` | `operator` (this VM only) |
| `~/.gitconfig` (ephemeral host) `user.email` | `cursoragent@cursor.com` | `paulthorson@users.noreply.github.com` (this VM only) |
| Env `GIT_AUTHOR_*` / `GIT_COMMITTER_*` | unset | may be set for commits in a session |
| In-repo git identity config | none | none |
| CI workflow git identity | none | none |

**Honest durability statement:** The git identity fix lives only on the ephemeral host (`~/.gitconfig` / process env). It does **not** survive a fresh Cloud Agent environment and is **not** fixed by this branch. Every future session must set identity on the host before committing if operator / noreply authorship is required. Capability-report §12.4 records the same. Aligns with 5.1/5.2 rewrite: no in-tree identity config; committing agent identity comes from host environment outside this repository.

### 2.4 Proof commit identity

```
git log -1 --format='%an <%ae> / %cn <%ce>'
operator <operator@users.noreply.github.com> / operator <operator@users.noreply.github.com>
```

(Verified on commits in this pre-merge pass when host config + env were set. Co-authored-by trailer: none observed on these commits.)

---

---

## 5.5 Spend wording before/after (3.4)

| Location | Before | After |
|---|---|---|
| setup_wizard `budget_model` prompt | Partial honesty sentence | Full `SPEND_UNIT_QUALIFIER` adjacent |
| setup_wizard `metered_allowance` / `headroom` / `billed_cap` / `billed_escalation` / `per_epic_budget` | Short “not dollars” or none | Full qualifier in same question |
| setup.md numeric bullets | Honesty section only above | Qualifier bullet immediately under each number + honesty section |
| README Spend section | Three bullets | One paragraph with meter claim **and** full qualifier |
| spec §10.4 | Shorter meter note | Full qualifier next to meter + next to 75% / ceiling bullets |
| harnesses/ceo.md Resource pacing | Shorter note | Full qualifier next to meter + next to threshold/ceiling bullets |
| spend.py alert / SpendCapExceeded / spend_status | Short parenthetical | Full `SPEND_UNIT_QUALIFIER` |
| Dashboard AdminTokens | KPI placeholders (not spend meter) | Unchanged (not a spend-cap surface) |

Qualifier text:

> This framework cannot see or limit what you spend with your model provider. Set a hard spending cap in your provider's billing console. This cap counts framework units only.

---

---

## 5.6 Could not do / why

- Could not make GitHub noreply a Google SSO identity (Google product constraint).
- Tip-scrub PR did not rewrite git history (done later 2026-09-16 under separate operator GO — `docs/history-identity-scrub-2026-09-16.md`).
- Did not mark PR ready or merge (forbidden).
- Did not invent TERMS/PRIVACY or replacement legal text for deleted Get AGs (forbidden).
- Did **not** implement proposed `COUNSEL_GATE_BEFORE_PROD` (human reviews first; lands separately).
- Site-repo acceptance gate cleanup is Cos-owned (out of scope for this AG agent).
- Git identity durability is **not** a durable repo fix (see §1 / 3.5).

---

## Item 8 — `runs/approval.token` write / permissions

See §1 / 3.8 and capability-report **§12.10**.

---

## Item 9 — Full current SECURITY.md

~~~~markdown
# Security Policy

## Reporting a vulnerability

This is an unpaid personal project. If you find a security issue, do **not** open a
public issue.

Contact: **security@agenticgovernance.app**

You can also report privately via GitHub: open a
[private vulnerability report](https://github.com/paulthorson/agentic-governance/security/advisories/new)
on this repository.

Please include: a description of the issue, the affected path, a minimal
reproduction, and suggested impact.

## Operator responsibility

You run the agents, the model provider account, the network, and the secrets.
This repository does not replace provider billing caps, OS firewalls, or human
review. See [`docs/capability-report.md`](docs/capability-report.md).

**This software does not provide a safety guarantee.**

## Security model (honest)

These are design goals and process rules. Only some have code gates today
([capability report §12.8](docs/capability-report.md#128-code-vs-instruction-controls-summary)).

1. **Blind-review isolation (instruction).** Advocates are instructed not to
 receive the worker’s rationale. There is **no** runtime wall that makes that
 impossible if a caller pastes rationale into a tool.
2. **Human-only veto clearing (process).** Constitutions say only a human clears
 a veto. Files remain writable; discipline is procedural.
3. **Append-only records (process).** Decision records should be appended, not
 rewritten. Ordinary filesystem writes are still possible.
4. **No secret exfiltration (instruction + operator hygiene).** Do not commit
 credentials. Secrets belong in the operator environment.
5. **Prompt-injection resistance (review checks / skills).** Skills and reviews
 flag override attempts; this is not a complete defense.

### Code gates that do exist

| Gate | Behavior | Cite |
|---|---|---|
| Spend (framework units) | Gated MCP reviews refuse at configured numeric cap | capability report §12.1 |
| Network permission | Messaging egress only if `allow`; unknown/deny = no egress | §12.3 |
| Approval checkpoints | Listed subprocess/outbound/outside-write sites refuse without `AG_APPROVAL=1`, `AG_APPROVAL_TOKEN`+`runs/approval.token`, or `runs/approval.ok` | §12.2 |
| HTTP bind | Default `127.0.0.1`; LAN requires explicit `--host` | §12.3 |

### Unchecked (operator must assume open)

- Agent runtimes and tools **not** calling the gated scripts/MCP entrypoints
- Dashboard Google OAuth / admin SSO deploy surface ([§7.2–7.4](docs/capability-report.md#126-secrets-dashboard-site))
- Model-provider token and dollar spend
- Absolute paths the operator points outside the repo when a helper does not gate them
- Blind-review / veto / append-only as technical impossibilities (they are not)

## Secret handling

- Never commit `.env`, `*.pem`, or credential files. `.gitignore` excludes common patterns.
- `dashboard/.env.example` ships **empty** `AUTH_*` placeholders ([§7.1](docs/capability-report.md#71-history--credentials)).
- Rotate any token you place in `MCP_AUTH_TOKEN` or alert webhooks.

## Supported surface

Markdown harnesses/constitutions + MCP server tools + helper scripts. Treat remote
HTTP MCP as hostile-network exposure unless you terminate TLS and auth in front of
loopback ([`docs/deployment.md`](docs/deployment.md)).
~~~~

## Item 9b — Full current CONTRIBUTING.md

~~~~markdown
# Contributing

Thanks for helping with Agentic Governance. This is an unpaid personal project.
Care about rigorous, reproducible review — that is the spirit.

## Developer Certificate of Origin (DCO)

All commits must be signed off:

```bash
git commit -s
```

By signing off, you certify the Developer Certificate of Origin
(https://developercertificate.org/): you have the right to submit the
contribution under the project’s Apache-2.0 license.

## Ground rules

1. **Preserve blind-review isolation in artifacts.** Do not put worker rationale
 into `facts.md` or other judge-facing packets (`AGENTS.md`).
2. **Never clear a veto by editing a constitution or calibration ledger to force
 a pass.** Humans clear vetoes in decision records.
3. **Keep records append-only** (process): corrections are new entries.
4. **Namespacing + frontmatter.** New flat agents/skills must be domain-prefixed
 with matching `name:` frontmatter.
5. **Reuse `shared/`** for cross-cutting checks instead of duplicating per plugin.
6. **Plugin folders are source of truth.** After plugin edits, run
 `scripts/consolidate-adversarial.py` when regenerating flat layers.
7. **Do not invent enforcement.** If code does not refuse, docs must say advisory
 ([`docs/capability-report.md`](docs/capability-report.md)).
8. **Run validators.** `python3 scripts/validate.py` and `python3 -m pytest tests/ -q`.

## Workflow

1. Fork / branch from `main`.
2. Make a focused change.
3. Add or update tests under `tests/` (especially `tests/test_published_claims.py`
 if you change a published claim).
4. Update `docs/capability-report.md` when behavior changes.
5. Update `CHANGELOG.md` under Unreleased when appropriate.
6. Open a PR with `git commit -s` on each commit.

## What makes a good contribution

- A new domain plugin (copy `adversarial-qa`), wired through consolidation + docs
- A cross-cutting check in `shared/skills/`
- An MCP tool that stays honest about what it enforces
- Fixes that replace fake “enforcement” language with real gates or advisory text

## Security issues

Use [`SECURITY.md`](SECURITY.md). Do not open a public issue for vulnerabilities.
~~~~

By signing off, you certify the Developer Certificate of Origin
(https://developercertificate.org/): you have the right to submit the
contribution under the project’s Apache-2.0 license.

## Ground rules

1. **Preserve blind-review isolation in artifacts.** Do not put worker rationale
 into `facts.md` or other judge-facing packets (`AGENTS.md`).
2. **Never clear a veto by editing a constitution or calibration ledger to force
 a pass.** Humans clear vetoes in decision records.
3. **Keep records append-only** (process): corrections are new entries.
4. **Namespacing + frontmatter.** New flat agents/skills must be domain-prefixed
 with matching `name:` frontmatter.
5. **Reuse `shared/`** for cross-cutting checks instead of duplicating per plugin.
6. **Plugin folders are source of truth.** After plugin edits, run
 `scripts/consolidate-adversarial.py` when regenerating flat layers.
7. **Do not invent enforcement.** If code does not refuse, docs must say advisory
 ([`docs/capability-report.md`](docs/capability-report.md)).
8. **Run validators.** `python3 scripts/validate.py` and `python3 -m pytest tests/ -q`.

## Workflow

1. Fork / branch from `main`.
2. Make a focused change.
3. Add or update tests under `tests/` (especially `tests/test_published_claims.py`
 if you change a published claim).
4. Update `docs/capability-report.md` when behavior changes.
5. Update `CHANGELOG.md` under Unreleased when appropriate.
6. Open a PR with `git commit -s` on each commit.

## What makes a good contribution

- A new domain plugin (copy `adversarial-qa`), wired through consolidation + docs
- A cross-cutting check in `shared/skills/`
- An MCP tool that stays honest about what it enforces
- Fixes that replace fake “enforcement” language with real gates or advisory text

## Security issues

Use [`SECURITY.md`](SECURITY.md). Do not open a public issue for vulnerabilities.

```

---

## Item 10 — Get AG documents

**DELETED** on this tip (operator LOCK public release). No replacements.

| Former path | Status |
|---|---|
| `` | **Deleted** |
| `` | **Deleted** |
| `docs/legal/` | **Removed** (empty) |

Historical authorship remains in git history (`9b5bcd9`, `86e9808`, `c7bc7bc`, site `[redacted]`). Calibration entry records the draft→deploy gap. Standing rule: do not draft replacement legal language.

NOTICE (current):

```text
Agentic Governance
Copyright 2026 <copyright holder named in NOTICE>

Licensed under the Apache License, Version 2.0.

```

*(Legal party text lives only in `NOTICE` / `LICENSE` — this embed is anonymized for public tip scrub.)*
---

## §6 Clean-clone

Stranger path: `/tmp/ag-stranger-clone-final` (and earlier `/tmp/ag-stranger-clone-*`). Focus: **agentic-governance** only (site clean-clone Cos-owned separately).

| Step | Command | Result |
|---|---|---|
| 1 | `git clone --branch cursor/release-hardening-4904` into new directory | **OK** — tip `12d383c` (remote verified after push) |
| 2a | `cd mcp && uv sync` on host **without** `uv` on PATH | **FAIL (host-only):** `uv: command not found` (exit 127). Not an in-repo blocker — install `uv` (https://docs.astral.sh/uv/) or ensure `~/.local/bin` on PATH |
| 2b | Same after installing `uv` 0.12.13 | **OK** — venv created; `adversarial-mcp` + deps installed |
| 3 | `uv run adversarial-mcp` (stdio; stdin closed) | **OK** — process starts and exits cleanly on EOF (expected for stdio smoke) |
| 4 | `python3 -m pytest tests/ -q` without pytest installed | **FAIL (host-only):** `No module named pytest`. CI installs via `pip install "mcp<2" pytest` (`.github/workflows/validate.yml`) |
| 4b | Same after `pip install --user "mcp<2" pytest` | **OK — 53 passed** |
| 5 | `python3 scripts/validate.py` | **OK — VALIDATION PASSED** (12 plugins / 20 flat agents / 86 flat skills) |

**In-repo blockers found:** none on the documented `cd mcp && uv sync && uv run adversarial-mcp` path once host has `uv`. Pytest is documented via CI / CONTRIBUTING (`python3 -m pytest tests/ -q`), not as a root `uv` extra — host must provide pytest (or follow CI pip line).

**Workspace tip pytest (this agent):** **53 passed**.

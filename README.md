# Agentic Governance

A **bring-your-own-agent (BYOA)** governance framework: role harnesses, a directed production chain, a constitution, a calibration ledger, and a setup wizard — so you can run **any** AI agent (Claude, ChatGPT/Codex, Hermes, Cursor, OpenClaw, or a custom client) under verifiable rules.

You do not start over. You bring the agents you already have. The wizard maps them to roles, reconciles their instructions against the harness (never layers a second rulebook on top), and writes the config your team will actually run.

---

## Why it exists

Most agent setups are governed by vibes: a prompt says "be careful," and nothing checks whether the agent was. This framework makes governance **mechanical** — harness stop conditions, required artifact shapes, a constitution with hard vetoes, and a ledger that turns human answers into precedent.

It is designed to be adopted **incrementally**, one agent at a time, without stopping work that is already running.

---

## How it came to be

1. **Adversarial review plugins** — domain reviewers with blind facts, constitutions, and hard vetoes (UX, engineering, QA, research, plus cross-cutting domains).
2. **Enterprise gap audit** — `AUDIT.md` drove the expansion from review loops into a full governance product.
3. **Harnesses + one master governance repo** — ratified in `docs/agentic-governance-spec.md`: constitution, role harnesses, calibration ledger, config, and in-repo wiki live here; project repos hold work product only. Git handoffs (named bot commits, folder ownership, no sideways writes) are the audit trail.
4. **Governance layout** — constitution, harnesses, ledger, and config landed in one master repo (`agentic-governance` on GitHub).
5. **Setup wizard** — conversational BYOA via the MCP server (`setup_wizard_start` / `setup_wizard_answer`), writing `config/setup.md`, `config/roster.md`, and persona blocks.
6. **Vanilla handoff** — first real-team adoption (Ladders, 2026-09-06): adopters load constitution + harnesses as a **contract**, not a repo fork (ADR-0006). Local tickets + portable watchdog/telemetry so a vanilla install needs no Paperclip (ADR-0007).

The full design lives in [`docs/agentic-governance-spec.md`](docs/agentic-governance-spec.md) and [`docs/spec-addendum-01.md`](docs/spec-addendum-01.md). Start the wiki at [`docs/Home.md`](docs/Home.md).

---

## The framework (what you actually run)

| Layer | Job |
|---|---|
| **Constitution** (`constitution/`) | Governing law and hard vetoes. Deliberately hard to change. |
| **Harnesses** (`harnesses/`) | Who each role is, what it owns, what it never does, inputs/outputs, artifact format, stop conditions. |
| **The chain** | Directed edges only. Research → PM → UX → Engineer → QA → CEO. No sideways traffic. |
| **Calibration ledger** (`ledger/`) | Case law: escalations, resolutions, promotions. CEOs resolve by precedent only — they never invent policy. |
| **Config** (`config/`) | Operator answers from the wizard: roster, budget, quiet hours, autonomy ladder, data sources. |
| **Plugins** (`adversarial-*/`) | Capability packs the harnesses may allowlist. Plugins never assert a role. |
| **Engine** (`mcp/` + `scripts/`) | MCP server, wizard, local tickets, stuck-review watchdog, veto telemetry. |

**Plugins vs harnesses.** Plugins are capability (what a thing can do). Harnesses are role definition (who a bot is). A harness may name which plugins a role may use. A plugin must never claim a role.

**One governance repo.** Every bot on every team reads the same constitution, harnesses, changelog, and ledger. Project repos hold epics and artifacts only — no forked copies of the rules.

---

## Who is who

```
HUMAN (Paul or You)
│ last resort: novel cases, veto clearance, CEO/adversary deadlock,
│ governance amendments, applying framework diffs
│
└── CHIEF OF STAFF (CoS) [multi-team mode only]
    │  the only bot allowed to reach the human
    │  merges + dedupes CEO queues · triages P0/P1 · decision-ready only
    │  daytime window · quiet hours · may NOT bypass its own funnel
    │
    ├── CEO BOT — team A
    ├── CEO BOT — team B
    └── CEO BOT — team C .
        │  resolves escalations by precedent from the Calibration Ledger
        │  never invents policy · may kill redundant loops
        │
        └── THE CHAIN (directed edges only, no sideways traffic)
            │
            RESEARCH ──> PM ──> UX ──> ENGINEER ──> QA ──> back to CEO
              │          │      │        │          │
              │          │      │        │          └─ test plans, gates
              │          │      │        └─ code, diffs
              │          │      └─ user stories, rationale.md
              │          └─ problem brief, 2+ real options
              └─ evidence pack, never recommends

Single-team mode: no CoS. CEO talks to the human directly.
```

### Role harnesses (7)

| Role | Owns |
|---|---|
| **Researcher** | Evidence pack. Establishes what is true. Never recommends. |
| **PM** | Problem brief with **two or more real options**. |
| **UX** | User stories + `rationale.md`. |
| **Engineer** | Code and machine-applicable diffs. |
| **QA** | Test plans and gates. Reports up to the CEO. |
| **CEO** | Routes work, paces spend, accepts QA, resolves by ledger precedent, kills redundant loops. |
| **CoS** | Multi-team only. Human funnel; morning queue; P0/P1 triage. Does not invent policy or clear vetoes. |

Folder ownership is the boundary: each bot writes only in its own epic folder and reads only upstream. Because the work lives in Git, every handoff is a commit by a named bot — an audit trail for the whole line at no extra cost.

---

## Center of Excellence (operating model)

Cos HOLD ACCEPT / Adv `COE_README_SOT` checklist — all seven named here. Soft or marketing-only CoE copy that omits them = **FAIL**.

**1. What.** A **framework CoE**: standing standard + feedback from real work. **Not** a delivery team, not a new org box, not a new bot or sidebar persona. Does **not** amend the constitution by itself.

**2. Who (owners — no new bot).** Cos + AG seat + Adv only. Project PMs are **not** constitution owners.

| Seat | Job |
|---|---|
| **Cos** | ACCEPT funnel. Merges only when Adv challenge clears. Does not invent policy. |
| **AG seat** | Framework PM. Drafts the named unpaid SoT/plan (`id` / owner / metric / AC). Project PMs ≠ AG constitution. |
| **Adv** | Challenges the plan. Does **not** author it. |

**Teams (members).** Ship under the live standard. File triad retros (well / didn’t / improve) as the feed.

**3. Loop.**

```
triad retro → AG unpaid SoT/plan → Adv challenge (does not author) → Cos ACCEPT → teams absorb
```

**4. Fail-closed middle.** `SELF_AUDIT_LOOP` is **LIVE** — Cos ACCEPT merged [#18](https://github.com/paulthorson/agentic-governance/pull/18) @ `5c10194`. Each audit cycle fail-closes to a **named unpaid SoT/improve item** **or** explicit **`AUDIT_CLEAR`** with evidence (nag-only = FAIL).

`RETRO_BEFORE_CLOSE` sits beside it as the close-gate twin — **named, not merged law yet** (still on [#17](https://github.com/paulthorson/agentic-governance/pull/17)).

**7. Not merged law yet — `RETRO_BEFORE_CLOSE` only.** Do **not** claim `RETRO_BEFORE_CLOSE` is live harness/constitution law. SoT still in flight on the five Adv-named locks — [PR #17](https://github.com/paulthorson/agentic-governance/pull/17). **Not live** until Cos ACCEPT merge.

**Already LIVE (cite merged SHAs).**

| Lock / check | Status | Merged |
|---|---|---|
| `SELF_AUDIT_LOOP` | **LIVE** | [#18](https://github.com/paulthorson/agentic-governance/pull/18) @ `5c10194` |
| Critic Check 7 | **LIVE** | [#14](https://github.com/paulthorson/agentic-governance/pull/14) @ `36deb0e` |
| Critic Check 8 / `VISUAL_STEP_STILLS` | **LIVE** | [#15](https://github.com/paulthorson/agentic-governance/pull/15) @ `d61f4c1` |

**5. P0.** No secrets, keys, emails, PII, or absolute host paths in AG git.

**6. Soft/marketing-only = FAIL.** Tips, vibes, chat-only retros, wiki scars without unpaid items, or a marketing CoE blurb missing owners / loop / fail-closed middle (`SELF_AUDIT_LOOP` **LIVE** [#18](https://github.com/paulthorson/agentic-governance/pull/18) @ `5c10194`) — **FAIL** under `COE_README_SOT`.

Full write-up: [`docs/CoE.md`](docs/CoE.md).

---

## The engine

The framework is **runtime-agnostic**. The same rules ship through:

1. **MCP server** (`mcp/`) — review tools + the setup wizard for any MCP-capable client.
2. **Local ticket system** (`scripts/ticket.py`) — file-based work items, `in_review` state, verdicts. No external tracker required.
3. **Stuck-review watchdog** — flags reviews that stall (`paperclip`, file/stdin, or `none`).
4. **Veto telemetry** — alerts from `runs/verdicts.jsonl`.
5. **Optional Paperclip** — live agent-team wiring when you want it; not required for a vanilla install.

```bash
# 1. Clone
git clone https://github.com/paulthorson/agentic-governance.git
cd agentic-governance

# 2. Install the MCP server (requires uv)
cd mcp
uv sync
uv run adversarial-mcp # stdio transport (default for MCP clients)
```

Wire the MCP server into your agent, then run the wizard. Per-framework guides:

- [Claude Code](docs/onboarding/claude-code.md)
- [ChatGPT / Codex](docs/onboarding/chatgpt-codex.md)
- [Cursor](docs/onboarding/cursor.md)
- [OpenClaw](docs/onboarding/openclaw.md)
- [Hermes](docs/onboarding/hermes.md)
- [Other MCP clients](docs/onboarding/other-mcp-clients.md)

---

## Setup wizard (BYOA)

The wizard is conversational, exposed through the MCP server — not a hand-edited config file.

```
setup_wizard_start() → setup_wizard_answer(.)
```

It asks for runtime, budget model, roster (`name | role | team | project`), whether adversaries are in play, escalation preferences, quiet hours, autonomy ladder, retry budgets, audit cadence, research bounds, irreversible-action protection, and where review/verdict data lives. Answers go to `config/setup.md` and `config/roster.md`; one persona block is generated per roster row under `config/personas/`.

**Reconcile, never layer.** When you adopt an existing agent, the wizard sorts its current instructions against the harness: covered (drop), compatible (keep), or conflicting (you decide). When adoption finishes, the agent has **exactly one** set of instructions.

**Re-runnable.** Later runs add to the roster rather than wiping it. An agent missing from the roster is outside governance — the framework cannot introspect your runtime, so it asks.

Full walkthrough: [`docs/onboarding/byoa.md`](docs/onboarding/byoa.md).

---

## Repo layout (the Git shape)

```
agentic-governance/
  constitution/           # governing law + vetoes
  harnesses/              # role definitions (pm, ux, engineer, qa, ceo, researcher, …)
  ledger/                 # calibration ledger + human queue
  config/                 # setup.md, roster.md, personas/ (wizard output)
  adversarial-<domain>/   # plugin source of truth (capability)
  agents/ · skills/       # flat namespaced copies for Cursor/Claude
  mcp/                    # MCP server + setup wizard
  scripts/                # validate, tickets, watchdog, telemetry, consolidate
  docs/                   # in-repo wiki + ADRs + ratified spec
  runs/                   # local in_review + verdicts (gitignored)
```

**Governance repo** = rules everyone shares. **Project repos** = epic folders and artifacts only. A governance change and its docs update land in the same commit; the wiki lives in `docs/`, not a separate GitHub wiki that drifts.

---

## The adversaries (enforcement, not the org)

Adversaries **judge** the chain and CEO rulings. They review **blind** — neutral facts, never the worker's rationale. A block sticks only if sustained **unanimously**. The CX / customer-harm veto is absolute; **only a human clears it**.

### Four triple-agent domains

| Domain | Agents |
|---|---|
| UX | critic · cx-advocate · evaluative-uxr |
| Engineer | critic · ops-advocate · reliability-reviewer |
| QA | critic · quality-advocate · edge-case-reviewer |
| Researcher | critic · evidence-advocate · context-reviewer |

### Eight single-adversary domains

| Domain | Focus |
|---|---|
| Universal | Irrecoverable harm |
| Prompt | Injection, drift, safety overrides |
| Security | Vulns, secrets, supply chain |
| Privacy | Consent, retention, transfer |
| Compliance | Regulatory + policy gates |
| Product | Unvalidated assumptions |
| Ops | Rollback, DR, deployability |
| Docs | Wrong / missing / misleading docs |

### Counts

| | |
|---|---|
| 20 | adversary agents (12 domains) |
| 7 | role harnesses (pm, ux, engineer, qa, ceo, researcher, cos) |
| 27 | personas in the framework |
| ~50 | persona blocks generated from the roster (one per registered bot) |

Adversaries can be `in-play` or `not-in-play` at setup. The chain and harnesses still govern either way.

---

## Documentation

| Doc | What |
|---|---|
| [`docs/Home.md`](docs/Home.md) | Wiki entry |
| [`docs/CoE.md`](docs/CoE.md) | Center of Excellence operating model (Cos + AG + Adv) |
| [`docs/agentic-governance-spec.md`](docs/agentic-governance-spec.md) | Ratified framework |
| [`docs/spec-addendum-01.md`](docs/spec-addendum-01.md) | Reversibility, autonomy, BYOA, open problems |
| [`docs/Architecture.md`](docs/Architecture.md) | Review loop |
| [`docs/MCP.md`](docs/MCP.md) | Engine surface |
| [`docs/onboarding/byoa.md`](docs/onboarding/byoa.md) | Adoption walkthrough |
| [`docs/deployment.md`](docs/deployment.md) | Remote MCP |
| [`docs/adr/`](docs/adr/) | Architecture decisions |
| [`AUDIT.md`](AUDIT.md) | Original gap analysis |

## Tooling & CI

- `scripts/validate.py` — structure validator (frontmatter, namespacing, plugin skeleton)
- `.github/workflows/validate.yml` — validate + gitleaks on push/PR
- `scripts/consolidate-adversarial.py` — rebuild flat layer + re-symlink into Cursor/Claude
- `scripts/stuck-review-watchdog.py` — stuck `in_review` detection
- `scripts/veto-telemetry.py` — constitutional veto alerts
- `scripts/messaging.py` — shared alert delivery
- `scripts/ticket.py` — built-in local ticket/story system

## Governance of this repo

- `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `AGENTS.md` at the root
- The **constitution** is the governing law; amendment requires adversarial review + human approval
- Bots do not edit their own rules; a human applies framework diffs

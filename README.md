# Agentic Governance

A **bring-your-own-agent (BYOA)** governance framework: a set of adversarial review
loops, constitutional rules, and a setup wizard that let you run **any** AI agent —
Claude, ChatGPT/Codex, Hermes, OpenAI, Cursor, OpenClaw, or a custom client — under
verifiable governance. You do not start over; you bring the agent you already have
and govern it.

> **What changed from "Adversarial Agents"?** This repo was formerly named
> *Adversarial Agents*. It is the same codebase, renamed to reflect what it actually
> is: a governance framework, not a set of agents. The adversarial reviewers are the
> enforcement mechanism; governance is the product.

---

## What this is

A governed workflow for AI agents that produce work. The core loop:

1. A **worker** produces work (a design, code, research, a decision).
2. **Adversary agents** judge it blind — they see neutral facts, never the worker's
   rationale.
3. A **constitution** gates it with hard vetoes (production harm, user harm,
   unsupported claims, irrecoverable harm).
4. Only a **human** clears a veto.

The same loop is exposed to any MCP-capable client through a single MCP server, so
the governance is identical no matter which agent you run.

## Why it exists

Most agent setups are governed by vibes: a prompt says "be careful," and nothing
checks whether the agent was. This framework makes governance **mechanical** — checks
that produce a pass or a fail, not style-guide language everyone reads differently.
It is designed to be adopted incrementally, one agent at a time, without stopping the
work that is already running.

## The five domains

| Domain | What it reviews | Veto |
|---|---|---|
| `adversarial-ux` | User experience (designs, HUD, voice, personas) | User harm |
| `adversarial-engineer` | Engineering (code, architecture, config, infra) | Production harm |
| `adversarial-qa` | Testing, acceptance criteria, release gates | User harm |
| `adversarial-researcher` | Research, synthesis, evidence | Unsupported claims |
| `adversarial-universal` | Catch-all (any domain) | Irrecoverable harm |

## Quick start (any system)

The framework ships an **MCP server** (`mcp/`) that exposes the review loop as callable
tools. Any agent that supports MCP can wire it in.

```bash
# 1. Clone
git clone https://github.com/paulthorson/agentic-governance.git
cd agentic-governance

# 2. Install the MCP server (requires uv)
cd mcp
uv sync
uv run adversarial-mcp # stdio transport (default for MCP clients)
```

Then wire the MCP server into your agent. See **[`docs/onboarding/`](docs/onboarding/)**
for per-framework guides:

- [Claude Code](docs/onboarding/claude-code.md)
- [ChatGPT / Codex](docs/onboarding/chatgpt-codex.md)
- [Cursor](docs/onboarding/cursor.md)
- [OpenClaw](docs/onboarding/openclaw.md)
- [Hermes](docs/onboarding/hermes.md)
- [Other MCP clients](docs/onboarding/other-mcp-clients.md)

## Adopting your agent (BYOA)

You do not start over. The **setup wizard** (exposed through the MCP server) walks you
through declaring your roster, mapping each existing agent to a role, and reconciling
its existing instructions against the harness — never layering one on top of the other.

- Run the wizard: `setup_wizard_start()` → `setup_wizard_answer(.)`
- See **[`docs/onboarding/byoa.md`](docs/onboarding/byoa.md)** for the adoption walkthrough.

## Documentation

The `docs/` folder is an Obsidian-able wiki (MOCs + pages): architecture, domains,
constitution, vetoes, calibration, MCP, Paperclip wiring, tooling, and the roadmap.
Start at [`docs/Home.md`](docs/Home.md). For remote deployment of the MCP server,
see [`docs/deployment.md`](docs/deployment.md).

## Tooling & CI

- `scripts/validate.py` — structure validator (frontmatter, namespacing, plugin skeleton).
- `.github/workflows/validate.yml` — CI: validate + gitleaks secret scan on push/PR.
- `scripts/consolidate-adversarial.py` — rebuild flat layer + re-symlink into Cursor/Claude.
- `scripts/stuck-review-watchdog.py` — flags in_review tickets stuck with no verdict
  (supports `--json` for machine-parseable output).
- `scripts/veto-telemetry.py` — alerts on constitutional vetoes from the verdict ledger.
- `scripts/messaging.py` — shared alert delivery (discord/whatsapp/imessage/generic).

## Vanilla handoff (ADR-0006, ADR-0007)

The framework is **environment-agnostic** — handoffable to any team in any environment.
Adopters take the constitution + harnesses as a **loadable contract** (no repo mirror)
and load them into their own mode of operation.

- **Constitution, harnesses, vetoes, calibration ledger, messaging** — all
  environment-agnostic.
- **Veto telemetry** — file-based (`runs/verdicts.jsonl`), portable.
- **Stuck-review watchdog** — data-source-agnostic (ADR-0007): `--source paperclip`
  (default), `--source file --issues-file <path>` (JSON file or stdin), or `--source none`
  (disabled until an in_review backend exists). The setup wizard asks which source a
  team uses and writes it to `config/setup.md`.

First real-team adoption: **Ladders Grok Bot** (2026-09-06) — see
[`docs/adr/0006-first-real-team-adoption.md`](docs/adr/0006-first-real-team-adoption.md)
and [`docs/adr/0007-watchdog-data-source.md`](docs/adr/0007-watchdog-data-source.md).

## Governance

- `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `AGENTS.md` at the repo root.
- `AUDIT.md` — the original gap analysis that drove the enterprise expansion.
- The **constitution** (`constitution/constitution.md`) is the governing law; it is
  deliberately hard to change (amendment requires adversarial review + human approval).

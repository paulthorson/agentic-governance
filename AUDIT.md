# Adversarial Agents — Enterprise Audit & Roadmap

**Status:** Gap analysis + expansion plan. Generated 2026-08-26.
**Goal:** A fully end-to-end, enterprise-class adversarial review system that lives in GitHub,
is referenceable from Cursor + Claude, and exposes an MCP.

---

## 1. What exists today (current state)

Five self-contained adversarial plugins, plus a consolidated reference layer, plus Paperclip
wiring:

| Plugin | Domain | Agents | Skills | Veto |
|---|---|---|---|---|
| `adversarial-ux` | User experience | 3 | 10 | User harm |
| `adversarial-engineer` | Engineering | 3 | 9 | Production harm |
| `adversarial-qa` | Testing / release | 3 | 8 | User harm |
| `adversarial-researcher` | Research / evidence | 3 | 8 | Unsupported claims |
| `adversarial-universal` | Catch-all | 1 | 6 | Irrecoverable harm |

- **13 agents, 45 skills** consolidated namespaced into `~/adversarial-agents/agents|skills`.
- **Wired into Cursor** (`~/.cursor/agents`, `~/.cursor/skills`) and **Claude Code**
  (`~/.claude/agents`, `~/.claude/skills`).
- **5 Paperclip agents** (Adversarial Engineer/QA/Researcher/UX/Universal) + mandatory
  review rule in 8 domain agents (Engineer, QA, UXer, UX Researcher, PM, BA, Scrum, CEO).
- Git repo at `~/adversarial-agents`, **but remote is wrong** (`even-weather`).

## 2. Gap analysis

### 2.1 Enterprise governance (foundation) — MISSING
- No `LICENSE`, `CONTRIBUTING.md`, `CHANGELOG.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`.
- No top-level `AGENTS.md` (how an agent/contributor operates inside the repo).
- No `.github/` CI (frontmatter lint, structure validation, collision check, link check).
- No semver discipline (all plugins pinned at `0.1.0`).
- **Git remote points to the wrong repo** — must fix before GitHub push.

### 2.2 Consistency — GAPS
- Skill counts uneven (10 / 9 / 8 / 8 / 6). For enterprise, each domain should carry a
  comparable, well-defined skill set.
- `adversarial-ux` is the original (different authoring); the 4 new ones were written to a
  pattern. Need a shared "house style" + template validator so they stay uniform.
- Every agent should carry the same 4-check frame (constitution + standard + personas +
  calibration-ledger + decision-record template). Verify all 5 conform.

### 2.3 Missing checks (within existing agents) — GAPS
The four-check frame is good but not enterprise-complete. Cross-cutting checks each reviewer
should be able to run:
- **Prompt-injection / agent-safety** — a review must flag injected instructions, prompt
  leakage, tool-abuse, or instructions that would override safety. Critical for AI-agent work.
- **Data privacy** — PII handling, data retention, exfiltration.
- **Software supply chain** — dependencies, provenance, licenses, pinned versions.
- **Security (formal)** — currently only Engineer has it; should be a shared capability.
- **Accessibility** — currently only UX; should be available cross-domain.
- **Performance/latency** — exists as constraint in engineer, not a formal check.
- **Disaster recovery / rollback** — partly in ops-runbook; needs a formal DR gate.
- **Ethical / reputational harm** — beyond user-harm.

### 2.4 Missing — additional agent types
Enterprise-class coverage suggests these specialist reviewers (each a plugin with 3 agents):

| New plugin | Reviews | Veto |
|---|---|---|
| **Adversarial Security** | security posture, secrets, threat model, compliance | Security breach / data exposure |
| **Adversarial Product/Market** | PM decisions, prioritization, market fit | Irreversible product/brand harm |
| **Adversarial Ops/Reliability** | deploy, rollback, SLOs, incident | Production-down / data loss |
| **Adversarial Compliance/Privacy** | PII, regulations, data governance | Regulatory/privacy breach |
| **Adversarial Budget/Cost** | spend, cost-benefit, ROI | Irreversible financial harm |
| **Adversarial Docs** | documentation, API docs, runbooks | Misleading docs causing harm |
| **Adversarial Prompt/AGENTS** | agent instructions, system prompts, the framework itself | Safety/integrity override |

### 2.5 Missing — wiki / documentation
- No `docs/` wiki (Architecture, How-it-works, per-domain guides, governance, MCP reference).
- No architecture diagram of the loop.
- No ADR log (decision record of the framework's own choices — e.g. why namespacing, why the
  blind-review isolation).
- No MOC (map of content) for cross-referencing — Paul uses Obsidian (`~/the assistant`).

### 2.6 MCP — MISSING (explicit ask)
An enterprise MCP server that exposes the review system to any MCP-capable client:
- `list_reviewers` / `get_reviewer` — enumerate agents + their checks
- `run_review` — run critic/advocate/reviewer against a submission and return verdicts
- `get_verdict` / `query_verdicts` — read decision records + calibration ledger
- `veto_state` — track open vetoes, what clears them, who the arbiter is
- `skills` — list/read skill definitions
- `router` — given a ticket, pick the right adversarial agent (mirror the Paperclip routing)

### 2.7 Tooling / automation — MISSING
- A CLI (`adv`) to run a review headlessly.
- CI that validates all frontmatter, structure, naming, and cross-references.
- A test harness to dry-run a reviewer against a fixture.
- **Stuck-ticket watchdog** — if an adversarial agent is paused/down, `in_review` tickets
  stall; need detection + alerting.

## 3. Roadmap (priority order)

### P0 — Foundation (do first; needed for GitHub)
1. Fix git remote to the real target repo.
2. Add `.gitignore`, `LICENSE`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`,
   `CHANGELOG.md`, top-level `AGENTS.md`, `README` update.
3. Add `.github/workflows/validate.yml` — CI that lints frontmatter, checks naming
   uniqueness, validates every SKILL.md/agent structure, checks cross-references.

### P1 — Cross-cutting checks (shared, reusable)
4. Build a `shared/` layer with cross-domain skill definitions so any reviewer can run
   prompt-injection, security, privacy, supply-chain, performance checks.

### P2 — New agents (the list in 2.4)
5. Add `adversarial-security`, `adversarial-product`, `adversarial-compliance` as new
   plugins (reuse the pattern), wire into Paperclip + routing.

### P3 — Docs / wiki
6. Add `docs/` wiki: Architecture, How-it-works, per-domain, governance, MCP reference,
   ADR log, MOC.

### P4 — MCP server
7. Build `mcp/` server (Node or Python) implementing the tool surface in 2.6; register in
   OpenClaw + Cursor + Claude MCP config.

### P5 — Tooling
8. `adv` CLI + dry-run test harness + stuck-ticket watchdog.

## 4. Decisions requested from Paul
1. Confirm the wrong git remote — what is the intended GitHub repo/org?
2. Which additional agent plugins to build first (recommend security + compliance + product).
3. MCP implementation language — **Python** (matches mempalace-mcp pattern) vs **Node**
   (matches the bridge-mcp pattern). Recommend Node/TS for consistency with existing bridge.
4. License: **MIT** (default, permissive) vs Apache-2.0 vs other.

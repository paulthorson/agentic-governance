# Roadmap

Open work, known gaps, and planned enterprise hardening. This is the living
list — update it as the framework evolves.

## Done

- [x] 5 domain plugins (ux, engineer, qa, researcher, universal)
- [x] Adversarial Prompt plugin (self-hosting instruction reviewer)
- [x] Review-loop diagram (docs/assets/review-loop.svg)
- [x] Test harness (tests/, 13 tests) wired into CI
- [x] Flat namespaced layer (13 agents, 45 skills) wired into Cursor + Claude
- [x] 5 Paperclip adversary agents + mandatory-review rule in 8 producers
- [x] Adversarial UX reclassified from the original generic agent
- [x] Enterprise foundation: LICENSE, SECURITY, CONTRIBUTING, CHANGELOG, AGENTS.md
- [x] Structure validator + CI (validate + gitleaks)
- [x] MCP server (11 tools, verified)
- [x] docs/ wiki (MOCs + pages)
- [x] Standalone git repo (fixed home-repo danger)

## Planned / gaps

### Additional adversary agents (enterprise depth)
- [x] **Adversarial Prompt / AGENTS** — reviews the agent instructions
      themselves (self-hosting the framework).
- [x] **Adversarial Security** — dedicated security reviewer (currently folded
      into Engineer). Standalone is stronger for enterprise.
- [x] **Adversarial Data / Privacy** — GDPR/CCPA, data handling, retention.
- [x] **Adversarial Compliance** — regulatory gates.
- [x] **Adversarial Product / Market** — reviews PM/market decisions (currently
      PM → Universal).
- [x] **Adversarial Ops / Reliability** — deployment, rollback, DR (folded into
      Engineer today).
- [x] **Adversarial Documentation** — reviews docs/AGENTS quality.

### Additional checks
- [x] **Prompt-injection / agent-safety** check (critical for AI agents).
- [x] **Software supply-chain** check (dependencies, SBOM).
- [x] **Performance / latency** check (engineer has constraints, no dedicated check).
      `eng-performance-check`.
- [x] **Disaster-recovery / rollback** gate (formal). `ops-rollback-check`,
      `ops-disaster-recovery-check`.
- [x] **Ethical / harm** check beyond user-harm. `univ-ethical-harm-check`.

### Governance & automation
- [x] **ADR log** (architecture decision records) for the framework's own decisions.
      `docs/ADR.md` + `docs/adr/` (5 ADRs + template).
- [x] **Stuck-review watchdog** — detect in_review tickets with no verdict
      (adversary down/paused) and alert. `scripts/stuck-review-watchdog.py`,
      cron every 30 min.
- [x] **Calibration automation** — periodic analysis of the verdict ledger.
      `scripts/calibration-report.py`.
- [x] **Telemetry / alerting** on vetoes.
      `scripts/veto-telemetry.py` (scan + alert + --watch dedupe).

### MCP
- [x] **Streamable HTTP transport** (currently stdio only).
      `--transport streamable-http|sse|stdio`.
- [x] **Auth** for remote deployments.
      `MCP_AUTH_TOKEN` bearer-token middleware.
- [x] **`run_review` deep mode** — actually invoke the adversary agents (LLM)
      rather than only assembling the prompt. `run_review_deep` via Ollama.

### Docs
- [x] **Diagram** of the loop as an image (currently ASCII).
- [x] **Per-domain deep-dive** pages.
      `docs/domains/` (12 pages).

## See also

- [[Home]] · [[Architecture]] · [[Domains]] · [[MCP]] · [[Tooling]]

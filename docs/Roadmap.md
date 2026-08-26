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
- [ ] **Adversarial Security** — dedicated security reviewer (currently folded
      into Engineer). Standalone is stronger for enterprise.
- [ ] **Adversarial Data / Privacy** — GDPR/CCPA, data handling, retention.
- [ ] **Adversarial Compliance** — regulatory gates.
- [ ] **Adversarial Product / Market** — reviews PM/market decisions (currently
      PM → Universal).
- [ ] **Adversarial Ops / Reliability** — deployment, rollback, DR (folded into
      Engineer today).
- [ ] **Adversarial Documentation** — reviews docs/AGENTS quality.
- [ ] **Adversarial Prompt / AGENTS** — reviews the agent instructions
      themselves (self-hosting the framework).

### Additional checks
- [x] **Prompt-injection / agent-safety** check (critical for AI agents).
- [ ] **Software supply-chain** check (dependencies, SBOM).
- [ ] **Performance / latency** check (engineer has constraints, no dedicated check).
- [ ] **Disaster-recovery / rollback** gate (formal).
- [ ] **Ethical / harm** check beyond user-harm.

### Governance & automation
- [ ] **ADR log** (architecture decision records) for the framework's own decisions.
- [ ] **Stuck-review watchdog** — detect in_review tickets with no verdict
      (adversary down/paused) and alert.
- [ ] **Calibration automation** — periodic analysis of the verdict ledger.
- [ ] **Telemetry / alerting** on vetoes.

### MCP
- [ ] **Streamable HTTP transport** (currently stdio only).
- [ ] **Auth** for remote deployments.
- [ ] **`run_review` deep mode** — actually invoke the adversary agents (LLM)
      rather than only assembling the prompt.

### Docs
- [x] **Diagram** of the loop as an image (currently ASCII).
- [ ] **Per-domain deep-dive** pages.

## See also

- [[Home]] · [[Architecture]] · [[Domains]] · [[MCP]] · [[Tooling]]

# Domains

The framework ships five domains, each a self-contained plugin with its own
adversary agents, stateless skills, constitution, standard, personas, and
calibration ledger.

## Domain map

| Domain | Plugin dir | Reviews work from | Adversary agents | Veto for |
|--------|-----------|-------------------|------------------|----------|
| **UX** | `adversarial-ux/` | UXer, UX Researcher | critic, cx-advocate, evaluative-uxr | user harm, dead ends, accessibility impossibility |
| **Engineer** | `adversarial-engineer/` | Engineer | critic, ops-advocate, reliability-reviewer | production harm, security holes, bricked config |
| **QA** | `adversarial-qa/` | QA | critic, quality-advocate, edge-case-reviewer | user harm from quality gaps |
| **Researcher** | `adversarial-researcher/` | general/non-UX research | critic, evidence-advocate, context-reviewer | unsupported claims driving decisions |
| **Universal** | `adversarial-universal/` | PM, BA, Scrum Master, CEO, catch-all | universal-adversary (single) | irrecoverable harm of any kind |
| **Prompt** | `adversarial-prompt/` | the framework's own instructions (self-hosting) | prompt-adversary (single) | safety overrides, injection, drift |
| **Security** | `adversarial-security/` | security-sensitive changes | security-adversary (single) | vulnerabilities, secret exposure, supply chain |
| **Privacy** | `adversarial-privacy/` | data handling, retention, consent | privacy-adversary (single) | unlawful collection, no consent, unbounded retention |
| **Compliance** | `adversarial-compliance/` | regulatory/policy gates | compliance-adversary (single) | regulatory/policy violation, no evidence |
| **Product** | `adversarial-product/` | product/market decisions | product-adversary (single) | unvalidated assumptions, unsound business case |
| **Ops** | `adversarial-ops/` | deployment, rollback, DR | ops-adversary (single) | irreversible deployment, no rollback, no DR |
| **Docs** | `adversarial-docs/` | docs, AGENTS, knowledge bases | docs-adversary (single) | wrong/missing/misleading docs |

## Per-domain detail

### UX (`adversarial-ux/`)
Reviews designs, wireframes, the Even G2 glasses HUD, Sonos voice responses,
TUI/Discord surfaces, and UX research (personas, usability). Four checks:
usability/task completion, clarity/communication, accessibility (WCAG 2.2 AA),
evidence honesty. Skills: `ux-altitude-check`, `ux-a11y-testing`,
`ux-assumption-testing`, `ux-desk-research`, `ux-generative-research`,
`ux-information-architecture`, `ux-interaction-design`, `ux-problem-framing`,
`ux-research-synthesis`, `ux-adversarial-ux` (worker).

### Engineer (`adversarial-engineer/`)
Reviews code, architecture, config, infra, security. Skills: `eng-system-map`,
`eng-threat-model`, `eng-complexity-analysis`, `eng-option-generation`,
`eng-test-coverage-map`, `eng-ops-runbook`, `eng-security-review`,
`eng-altitude-check`, `eng-assumption-testing`, `eng-adversarial-engineer` (worker).

### QA (`adversarial-qa/`)
Reviews test plans, acceptance criteria, release gates. Skills: `qa-acceptance-criteria-parse`,
`qa-coverage-map`, `qa-test-case-generation`, `qa-risk-ranking`,
`qa-edge-case-hunting`, `qa-regression-map`, `qa-release-gate`,
`qa-altitude-check`, `qa-adversarial-qa` (worker).

### Researcher (`adversarial-researcher/`)
Reviews research, synthesis, evidence. Skills: `res-question-reframe`,
`res-desk-research`, `res-source-inventory`, `res-evidence-triage`,
`res-method-design`, `res-research-synthesis`, `res-recommendation`,
`res-altitude-check`, `res-adversarial-researcher` (worker).

### Universal (`adversarial-universal/`)
A single adversary applicable anywhere. Four domain-agnostic checks: altitude,
trade-off, harm/blind-spots, falsifiability. Skills: `univ-altitude-check`,
`univ-assumption-hunt`, `univ-blind-spot-search`, `univ-counter-case`,
`univ-decision-gate`, `univ-risk-scan`, `univ-adversarial-universal` (worker).

### Prompt (`adversarial-prompt/`)
A self-hosting adversary that audits the framework's own instructions (AGENTS.md,
system prompts, skills, plugin manifests) for prompt-injection, drift, and safety
overrides. Skills: `prom-prompt-injection-scan`, `prom-instruction-drift-check`,
`prom-safety-override-scan`, `prom-adversarial-prompt` (worker).

### Security (`adversarial-security/`)
A dedicated security reviewer (previously folded into Engineer). Audits code,
config, infra, and dependencies for vulnerabilities, secret exposure, supply-chain
risk, and data protection. Skills: `sec-vuln-scan`, `sec-secret-exposure-scan`,
`sec-supply-chain-check`, `sec-data-protection-check`, `sec-adversarial-security` (worker).

### Privacy (`adversarial-privacy/`)
A GDPR/CCPA data-privacy reviewer. Audits data collection, consent, retention,
subject rights, and cross-border transfer. Skills: `priv-data-collection-audit`,
`priv-consent-check`, `priv-retention-bound`, `priv-subject-rights-check`,
`priv-transfer-lawfulness`, `priv-adversarial-privacy` (worker).

### Compliance (`adversarial-compliance/`)
A regulatory/policy reviewer. Audits work against regulatory gates, policy
alignment, evidence, audit trail, and liability. Skills: `comp-regulatory-gate-check`,
`comp-policy-alignment-check`, `comp-compliance-evidence`, `comp-audit-trail-check`,
`comp-liability-scan`, `comp-adversarial-compliance` (worker).

### Product (`adversarial-product/`)
A product/market reviewer. Audits market assumptions, user need, competitive
position, business case, and market risk. Skills: `prod-market-assumption-check`,
`prod-user-need-check`, `prod-competitive-position-check`, `prod-business-case-check`,
`prod-market-risk-scan`, `prod-adversarial-product` (worker).

### Ops (`adversarial-ops/`)
An ops/reliability reviewer. Audits deployability, rollback, disaster recovery,
monitoring, and on-call readiness. Skills: `ops-deployability-check`,
`ops-rollback-check`, `ops-disaster-recovery-check`, `ops-monitoring-check`,
`ops-oncall-readiness-check`, `ops-adversarial-ops` (worker).

### Docs (`adversarial-docs/`)
A documentation reviewer. Audits accuracy, completeness, usability,
consistency, and discoverability. Skills: `doc-doc-accuracy-check`,
`doc-doc-completeness-check`, `doc-doc-usability-check`,
`doc-doc-consistency-check`, `doc-doc-discoverability-check`,
`doc-adversarial-docs` (worker).

## Flat namespaced layer

The `agents/` and `skills/` folders at the repo root are the flat, namespaced
consumption layer wired into Cursor and Claude. Names are prefixed by domain
(`ux-critic`, `eng-ops-advocate`, `qa-release-gate`, …) so they register as
distinct agents/skills without collision. Rebuild with
`scripts/consolidate-adversarial.py`.

## See also

- [[Architecture]] · [[Constitution]] · [[Vetoes]] · [[Calibration]] · [[Paperclip]]

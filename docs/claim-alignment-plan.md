# Claim alignment plan — public release hardening

> **Historical plan (commit 1 of the hardening PR).** Citations were HEAD at plan
> time and may drift. **Source of truth for what code does now:**
> [`docs/capability-report.md`](capability-report.md). Do not treat this plan as
> live enforcement claims.

Plan only at authoring time. Governing principle: a control that exists only as text in a spec is guidance, not
enforcement. Never describe advisory as enforcement. Where control can be real in
code, make it real; where not, say advisory.

---

## 10.1 Enforcement claims → code backing

| Claim | File:line | Exact sense | Code backs it? |
|---|---|---|---|
| CEO bots “pace spend” | `docs/agentic-governance-spec.md:29` | Routing/pacing as CEO duty | **NO** — prompt/harness only |
| “Enforce a hard stop where bots halt rather than continue” | `docs/agentic-governance-spec.md:264` | Hard stop at budget | **NO** — no meter, no refuse |
| Metered headroom / billed earlier escalate | `docs/agentic-governance-spec.md:265–266` | Config-driven pacing | **NO** — config write only |
| Stop if budget model unknown | `docs/agentic-governance-spec.md:282` | Stop → wizard | **NO** — instruction only |
| “Spend is recorded per bot” (A7 / §10.10) | `docs/agentic-governance-spec.md:355–388`; `docs/spec-addendum-01.md:281–291` | Per-bot cost attribution | **NO** — no recording implementation |
| Discovery loop stops when “spend budget reached” | `docs/spec-addendum-01.md:656` | Bound includes spend | **NO** |
| CEO harness: “Enforce a hard stop…” | `harnesses/ceo.md:75` | Same as spec §10.4 | **NO** (synced from spec) |
| CEO “paces spend” | `harnesses/ceo.md:17`; `README.md:92` | Role description | **NO** |
| Wizard: “billed = a hard spend cap” | `mcp/adversarial_mcp/setup_wizard.py:58–59` | Operator-facing wording | **NO** — answers written to `config/setup.md` only (`setup_wizard.py:361–383`) |
| Metered allowance / billed_cap / per_epic_budget collected | `setup_wizard.py:64–97` | Config fields | Config only; **no meter reads them** |
| Format is enforcement / prompt-enforced | `docs/agentic-governance-spec.md:39,144` | Artifact-shape discipline | **PARTIAL** — structural review exists in MCP; not a technical wall |
| Veto is hard stop; only human clears | `constitution/vetoes.md:3`; constitutions | Constitutional veto | **YES (partial)** — `check_veto` / review tools flag keywords; clearing is process, not a code lock on humans |
| Blind-review isolation | constitutions / SECURITY.md | Advocates never see rationale | **Advisory + process** — no runtime wall between tools |
| Append-only decision records | SECURITY.md / AGENTS.md | Never edit after commit | **Advisory** — files are ordinary writable files |
| Uvicorn binds for remote HTTP | `mcp/adversarial_mcp/server.py:647` | `host="0.0.0.0"` | **YES (undesired default)** — binds all interfaces |
| Docs say bind private / note 0.0.0.0 | `docs/deployment.md:33,73–74` | Guidance | Docs only until code default changes |
| Irreversible-action protection levels 1–3 | `setup_wizard.py:191–192` | Operator choice | **NO enforcement** of level 1/2 in scripts |
| Alert channel / webhook | `setup_wizard.py:199–214`; `scripts/messaging.py` | Delivery path | **YES** — messaging sends; **no network permission gate** |
| Network permission question | wizard | Operator egress consent | **MISSING** — no question; UNKNOWN not defined |
| Approval checkpoints for subprocess/outbound/outside writes | scripts / server | Gate irreversible sides | **MISSING** |

---

## 10.2 Unbacked claims — enforce or rewrite

| Unbacked claim | Decision | Why |
|---|---|---|
| Spec/harness “Enforce a hard stop” on spend | **Rewrite** to advisory + document framework-unit meter limits | Framework sits beside agents; cannot see Claude/Cursor/$ API spend. A fake “hard stop” on dollars would be dishonest. |
| “billed = a hard spend cap” (wizard) | **Rewrite** | Same. Wizard must tell operator the only hard **dollar** limit is at the model-provider billing console. |
| “Spend is recorded per bot” | **Rewrite** unless/until attribution is implemented | No recorder exists. Optional: framework-visible unit ledger is not per-bot $ attribution. |
| “pace spend” as if enforced | **Rewrite** to “advises pacing / may refuse framework-recorded units at cap” | After meter lands, language must match what code does. |
| Stop if budget unknown | **Keep as advisory** (instruction) | Cannot force external agents to stop; CEO harness remains guidance. |
| Irreversible-action levels | **Partial enforce** where sites are in-repo scripts | Gate subprocess/outbound/outside-write call sites with approval; leave uncovered sites documented as unchecked. |
| Network egress unrestricted by default | **Enforce** | Add wizard network permission; UNKNOWN = no egress; wire messaging. |
| Uvicorn `0.0.0.0` default | **Enforce** | Default `127.0.0.1`; LAN bind = explicit flag + warning. |

---

## 10.3 Proposed spend mechanism + honest limits

### What is technically possible (2.1)

| Mechanism | Possible? | Sees real $? | Can refuse? |
|---|---|---|---|
| Intercept model-provider token/dollar meters (OpenAI/Anthropic/Cursor billing) | **NO** from this repo | N/A | N/A |
| Read provider invoices/APIs without operator credentials and product integration | **NO** (not present) | — | — |
| Meter **framework-visible units** that callers record (reviews, deep reviews, custom increments) against wizard `billed_cap` / `metered_allowance` | **YES** | **NO** — units are whatever the operator/config means, not provider $ | **YES** — refuse gated MCP/script entrypoints when usage ≥ cap |
| After-the-fact detect + alert when recorded usage crosses escalation threshold | **YES** | Only for recorded units | Alert only |
| Prompt CEO to halt (harness text) | Already present | No | Advisory only |

### Proposed implementation (2.2)

1. Add `mcp/adversarial_mcp/spend.py`: parse cap/allowance from `config/setup.md`; append usage to `runs/spend-ledger.jsonl`; `refuse_if_over_cap()` raises when at/over cap; optional threshold alert via `scripts/messaging.send_alert` when available.
2. Gate expensive/networked MCP paths that this process owns (at minimum `run_review_deep`; record usage on successful gated calls).
3. **Honest limits (must appear in wizard + docs):**
   - This meter does **not** observe model-provider tokens or dollars.
   - Agents running outside these gated entrypoints are **unchecked**.
   - The **only hard dollar spend limit** is the operator’s model-provider billing console (and any OS/network controls they apply).
   - Framework refuse-at-cap applies only to **recorded framework units** at configured numeric caps.

### Language after rewrite (2.3–2.4)

- Replace “Enforce a hard stop” with advisory CEO pacing + “framework may refuse its own gated operations when recorded units reach the configured cap.”
- Wizard must not call billed mode a hard spend cap without the provider-console sentence.

---

## 10.4 Proposed approval checkpoint + uncoverable sites

### Classification (audit at HEAD)

| Site | Class | Checkpoint achievable? |
|---|---|---|
| `server.py` Ollama `urlopen` (`~426–449`) | Outbound | **YES** — require approval and/or network allow |
| `server.py` uvicorn bind (`647`) | Listen | Change default bind; LAN = flag + warning (not an approval file) |
| `server.py` `runs/verdicts.jsonl` | Own-dir write | No checkpoint (reversible / expected) |
| `messaging.py` Discord `urlopen` / subprocess helper / `ALERT_COMMAND` | Outbound + subprocess | **YES** — network permission + approval for send |
| `stuck-review-watchdog.py` `paperclipai` CLI | Subprocess (may network) | **YES** — approval before subprocess |
| `veto-telemetry.py` → `send_alert` | Outbound (via messaging) | Covered if messaging gated |
| Dashboard Google OAuth | Outbound (deployer-operated Next app) | **Document unchecked** in this framework process — separate deploy surface |
| `validate.py` `git apply --check` | Subprocess | **YES** — approval before git apply |
| `setup_wizard.py` config/harness/runs writes | Own-dir (absolute path answers can escape) | Path-escape: treat absolute outside-repo as outside write → **checkpoint or refuse** |
| `calibration-report.py --output` | Outside write possible | **YES** if path outside repo |
| `ticket.py`, `sync-harnesses.py`, `gen-plugin.py`, `sync-improve.mjs` | Own-dir writes | No checkpoint |

### Proposed checkpoint

- Shared helper: require `AG_APPROVAL=1` (or a one-shot token file under `runs/`) before classified actions; without it, refuse with a clear error.
- Apply first to: `validate.py` git apply, messaging egress, stuck-review `paperclipai`, Ollama generate, calibration-report outside-repo output.
- Uncoverable / leave unchecked: dashboard Google OAuth & admin SSO; arbitrary agent runtimes not calling these scripts; operator shell outside the framework.

---

## 10.5 Other doc/code mismatches

| Finding | Notes |
|---|---|
| LICENSE prepends `Copyright (c) 2026 paulthorson` before Apache text | Apache-2.0.txt has no copyright line prepended; fix + add NOTICE |
| No `NOTICE` file | Required by release plan |
| `docs/deployment.md` still describes `0.0.0.0` default | Align after bind fix |
| README “governance **mechanical**” / CEO “paces spend” | Overclaims vs code; rewrite after capability report |
| SECURITY “non-negotiable guarantees” | Several are process/advisory, not code walls — reword |
| Git author/committer **configs that SET identity** | **None found** in tree (5.1). History contains `noreply address` and `prior username` authors — **report only; do not rewrite history; no.mailmap** |
| `noreply address` in dashboard allowlist / `.env.example` / README | **Report only** (5.3) — not git identity config |
| `prior username` | Read-only check → **HTTP 404** (5.4) |
| No wizard network permission; messaging egress unrestricted when webhook/command set | Fix in commits 8–9 |
| Dashboard optional for framework use; marketing/admin surface | Report in capability report (7.3) |
| `sharp-libvips*` LGPL-3.0-or-later in dashboard lockfile | Copyleft note for binary redistribution (6.3) |
| Look/stills issues #39/#26 | Untouched per scope |

---

## Commit map (this PR)

1. This plan 
2. LICENSE + NOTICE 
3. uvicorn default `127.0.0.1` 
4. Git identity config changes (none found → empty/no-op change commit documenting that) 
5. Spend meter/refuse for framework units 
6. Spend language alignment (spec/harnesses/wizard) 
7. Approval checkpoints 
8. Network permission in wizard (UNKNOWN = no egress) 
9. Messaging respects network permission 
10. Test contract 
11. `docs/capability-report.md` 
12. README / SECURITY / CONTRIBUTING aligned to capability report 

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
| Dashboard admin gated by this helper? | **NO** — separate localhost Host gate in dashboard middleware | `dashboard/src/middleware.ts`; `dashboard/src/lib/admin-access.ts` |
| Arbitrary agent shells outside these scripts gated? | **NO** | Unchecked |

---

## 12.3 Network and bind

| Question | Answer | Cite |
|---|---|---|
| Wizard asks network permission? | **YES** | `mcp/adversarial_mcp/setup_wizard.py:229–233` (`id: network_permission` at `:230` in `WIZARD_FLOW`) |
| Options | `allow` \| `deny` \| `unknown` | `setup_wizard.py:40` `NETWORK_PERMISSIONS` |
| UNKNOWN / missing → egress? | **NO** (no egress) | `messaging.py:78–80`; `load_network_permission` default `unknown` at `messaging.py:57–58`, `75` |
| Messaging respects permission? | **YES** | `messaging.py:134–141` |
| MCP HTTP default bind | `127.0.0.1` | `server.py:779–785` |
| MCP HTTP auth | Non-stdio requires non-empty `MCP_AUTH_TOKEN` except loopback (warns); non-loopback without token is refused; bearer compare uses `hmac.compare_digest` | `server.py:751–763`, `797–819` |
| LAN bind | Explicit `--host 0.0.0.0` (etc.) + `MCP_AUTH_TOKEN` required + stderr warning | `server.py:801–826` |
| Stdio transport default? | **YES** | `server.py:775–776` |

---

## 12.4 Identity

This repository does not store or set a git author identity.

| Question | Answer | Cite |
|---|---|---|
| In-tree git identity config (`user.name`, `user.email`, `GIT_AUTHOR*`, `GIT_COMMITTER*`) | **None.** Commit identity comes from the host environment. | `tests/test_published_claims.py` (`test_no_git_identity_config_uses_non_noreply_email`) |
| Dashboard admin access | Localhost host only. Remote identity login is not used. | `dashboard/src/lib/admin-access.ts`; `dashboard/src/middleware.ts` |
| Personal phone numbers in tree | **None** found | Repository search |

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
| LGPL obligation (sharp / libvips) | Distributing **binaries** that link LGPL libvips may require providing corresponding source / relink rights under LGPL-3.0-or-later. Source-only consumers of this repo who never ship those native binaries are not distributing the LGPL object. **Operator/redistributor must verify** their own distribution form. | Lockfile license field |

---

## 12.6 Secrets, dashboard, site

### 7.1 History / credentials

| Question | Answer | Cite |
|---|---|---|
| `dashboard/.env.example` remote-login keys | **None** — stub for optional local overrides only (localhost admin) | `dashboard/.env.example` |
| Commit that historically added empty remote-login placeholders | `1bfa1a5` — empty values only; keys later removed | git history |
| Real credentials committed in those env keys | **NO** evidence in example file | Same |
| Admin token pages | Admin UI under `/admin/tokens` shows **placeholder KPI copy** (“Baseline / unpaid”); not live provider tokens | `dashboard/src/components/AdminTokens.tsx` (placeholder posture documented in dashboard README) |

### 7.2 Dashboard admin access (localhost only)

| Question | Answer | Cite |
|---|---|---|
| Remote identity login for admin? | **NO** — removed; localhost Host gate only | `dashboard/README.md`; `middleware.ts` |
| How is `/admin` gated? | Request Host must be localhost / loopback / `*.localhost`. Unspecified-bind Host is not local. Client `X-Forwarded-Host` is ignored unless `AG_TRUST_X_FORWARDED_HOST` is set. Empty host fails closed. Else redirect to `/` with `admin=local-only` | `dashboard/src/middleware.ts`; `admin-access.ts` |
| Email allowlist? | **NO** — remote identity login removed | — |
| Hardcoded allowlist email | **NO** | `admin-access.ts` |

### 7.3 Dashboard required?

| Question | Answer | Cite |
|---|---|---|
| Required to run the governance framework (MCP/scripts/harnesses)? | **NO** | Root install path uses `mcp/` + scripts; dashboard is separate Next app |
| Optional marketing/admin face? | **YES** | `dashboard/README.md`; root README marketing-face note |

### 7.4 Deployed site / routes / storage / analytics / clone builds

| Question | Answer | Cite |
|---|---|---|
| In-repo app routes | `/`, `/admin`, `/admin/login` (redirects to `/admin`), `/admin/reports`, `/admin/traction`, `/admin/tokens`, `/admin/cycle-time`, `/admin/scars` | `dashboard/src/app/**` |
| Input | Public pages render content; `/admin` is localhost Host only (remote identity login removed) | `middleware.ts`; `app/page.tsx` |
| Storage | Traction content from repo files / synced content; no first-party DB module found in dashboard src for AG data | `dashboard/data/`, dashboard sync script |
| Cookies | No remote-login session cookies; no custom cookie module found in `dashboard/src` | Grep: no `cookie` hits under `dashboard/src` |
| Analytics (gtag/plausible/segment) | **NO** matches under `dashboard/src` | Grep |
| Clone-build deps that commonly break cold clones | `dashboard` needs `npm install` including the localhost dashboard UI kit packages and `next`; `prebuild` runs `sync-improve.mjs`. MCP needs `uv`/`pip` for `mcp`+`pydantic`. Native **sharp**/libvips platform packages may fail on unsupported OS/arch. | `dashboard/package.json`; lockfile sharp entries |

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
| Chain routing, reviewer independence, close rule (ADR-0010) | **Code** for writes through `chain.py` (CLI + MCP `ticket_*`) | `scripts/chain.py`; `tests/test_chain.py` |
| Veto clear / escalation resolve / close override | **Code** (approval) | `scripts/ticket.py` + `approval.py`; not exposed over MCP |
| Lost-update protection on shared ledgers | **Code** | `scripts/events.py` `file_lock` |
| CEO pacing / halt language | **Instruction** | harness/spec |
| Veto scan (Rule 1 first pass) | **Code**, fixed term and pattern match only; a harm described without a listed term passes as `REVIEW_REQUIRED` | `server.py` `VETO_KEYWORDS`, `VETO_PATTERNS`, `_veto_hits` |
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
| Fallback helper path | Optional local helper `REPO_ROOT.parent / ".local/workspace/scripts/post-to-discord.py"` **if that file exists on the operator host** — not shipped in this repo; not an author-controlled remote URL. | `messaging.py:97–108` |

---

## 12.10 `runs/approval.token` (write / permissions)

| Question | Answer | Cite |
|---|---|---|
| Who writes `runs/approval.token`? | **This framework never writes it.** Only the operator creates it. Code **reads** it when `AG_APPROVAL_TOKEN` is set. | `scripts/approval.py:42–50` (read only); no `write`/`open(.,"w")` of `approval.token` in tree |
| Default file permissions | Whatever the operator’s umask / create mode produced. Not set by framework create (there is no create). | Operator host |
| Can other local users read it? | **If** the operator left group/world bits set, yes — until tightened. On successful token match path, `has_approval` calls `_tighten_secret_file` which attempts `chmod 0o600` when group/world bits are present; if chmod fails, warns on stderr that other local users may read the token. | `approval.py:46`, `65–84` |
| World-readable by design? | **No.** Best-effort tighten to `0600` on read; cannot guarantee on foreign-owned / unsupported FS. | Same |

---

## 12.11 BYODS (bring your own design system)

| Question | Answer | Cite |
|---|---|---|
| Wizard records a design system? | **YES** — operator link, predefined codified system, or custom build (fonts, colors, CVD-safe data-viz palette, brand voice); written to `config/design-system.md` | `mcp/adversarial_mcp/setup_wizard.py` `DS_SOURCES`, `_write_design_system` |
| Predefined systems offered | Astryx (Meta, recommended), Material, Carbon, Spectrum, Atlassian, Polaris, Primer | `setup_wizard.py` `DS_PRESETS` (URLs verified live 2026-09-29) |
| Starter palette primaries text-safe? | **YES** — every curated primary is ≥ 4.5:1 on white (WCAG AA), asserted by test | `setup_wizard.py` `DS_PALETTES`; `tests/test_wizard_byods.py::test_palette_primaries_are_text_safe_on_white` |
| Data-viz default CVD-safe? | **YES** — Okabe–Ito recommended; custom allowed | `setup_wizard.py` `DS_VIZ_OKABE_ITO` |
| `design_system_palettes` MCP tool enforces anything? | **NO** — returns starter data for the operator's agent to render (swatches / color wheel); the wizard records the choice | `mcp/adversarial_mcp/server.py` `design_system_palettes` docstring |
| Framework pixel-enforces the recorded design system on projects? | **NO — advisory config only.** Initiative-level craft gates (`DESIGN_SYSTEM_FIRST`, Check 7/8, Cos stamp) still apply per project; a per-project kickoff may override the default | `config/design-system.md` ("Advisory, not enforced"); `docs/onboarding/byods.md` |
| Detail tokens quick vs define-each? | **YES** — quick setup applies recommended values; define-each walks neutrals, dark mode, radius, icons, logo, type scale, spacing, shadows, motion, breakpoints | `setup_wizard.py` `ds_detail`, `DS_DETAIL_MODES` |
| Machine-readable tokens? | **YES** — `config/design-tokens.json` (W3C-DTCG-flavored `$value`/`$type`); external sources write a reference entry | `setup_wizard.py` `_write_design_tokens` |

---

## 12.12 Event log and close gate (ADR-0009)

| Question | Answer | Cite |
|---|---|---|
| Is every governed action recorded? | **YES for actions through `scripts/ticket.py`, `scripts/chain.py`, and MCP `record_verdict` / `overturn_verdict` / `ticket_*`.** Each appends one envelope to `runs/events.jsonl`. Ticket transitions write the event before saving the ticket; if the event write fails, the ticket is not saved. Agent runtimes that do not call these are not recorded. | `scripts/events.py`; `scripts/chain.py` `Store.transact`; `tests/test_chain.py::ReviewFindingsTest::test_event_written_before_save_and_uses_transition_time` |
| Is the envelope versioned? | **YES** — `schema_version` "1"; the reference reader raises on unknown versions | `events.py` `read_events`; `tests/test_events.py::LogTest::test_unknown_schema_version_fails_loudly` |
| Can concurrent writers lose updates? | **NO for writers using this code**, unless a holder stalls more than 30 s inside the lock (ADR-0009). O_EXCL lock file per ledger with an owner token; stale locks renamed aside; Windows `PermissionError` retried. Tested on Linux and macOS in CI (`tests/test_identity_integrity.py::CrossPlatformStressTest`); Windows untested. | `events.py` `file_lock`; `tests/test_events.py::LogTest::test_concurrent_processes_lose_no_updates`; `tests/test_chain.py::ReviewFindingsTest::test_lock_holder_never_deletes_a_lock_it_lost` |
| Can a corrupt ticket file be silently replaced? | **NO** — unreadable store raises and every write stops | `chain.py` `Store.load`; `tests/test_chain.py::ReviewFindingsTest::test_corrupt_store_is_never_overwritten` |
| Can `ticket.py done` close unreviewed work? | **NO.** Exits 2 unless already done; override needs operator approval plus `--by` / `--reason` and is logged | `scripts/ticket.py` `cmd_done`; `tests/test_events.py::CloseGateTest` |
| Does an open 1.0 veto survive the upgrade? | **YES** — a ticket whose latest 1.0 verdict carried veto hits loads as `blocked` | `tests/test_chain.py::ReviewFindingsTest::test_legacy_open_veto_survives_upgrade` |
| Can a PASS carry veto hits? | **NO** — refused and logged | `chain.py` `verdict`; `tests/test_events.py::CloseGateTest::test_pass_with_veto_hits_refused` |
| Does every veto alert in `--watch` mode? | **YES** — dedupe on `event_id`; legacy records use a composite key | `scripts/veto-telemetry.py` `_dedupe_key`; `tests/test_events.py::VetoDedupeTest` |
| Is `agent_id` authenticated? | **NO** — self-reported | `events.schema.md` |
| Does the event log leave the machine? | **NO** — local file only; no exporter ships | `events.py` (no network) |

---

## 12.13 Chain state machine and stuck-ticket recovery (ADR-0010)

| Question | Answer | Cite |
|---|---|---|
| Is the chain enforced in code? | **YES for writes through `chain.py`** (CLI and MCP `ticket_*`). Agents that edit `runs/in_review.json` directly bypass it. | `scripts/chain.py`; `tests/test_chain.py::ChainFlowTest::test_full_chain_runs_to_done` |
| Are teams isolated? | **YES for claims, submits, and verdicts** — `claim_next` matches stage and team exactly, and a verdict requires the review claim. **NO for reads** — `ticket_list` returns every team's tickets. | `tests/test_chain.py::ChainFlowTest::test_claims_are_team_scoped`; `tests/test_chain.py::ReviewFindingsTest::test_verdict_requires_review_claim` |
| Can a worker review its own ticket? | **NO** under one `agent_id`; a verdict with no agent id is refused. Without a registry, an agent using two ids is not detected; with one, see §12.14. | `tests/test_chain.py::ChainFlowTest::test_worker_cannot_review_own_work`; `tests/test_chain.py::ReviewFindingsTest::test_verdict_without_agent_refused` |
| Can `done` skip remaining stages after an earlier PASS? | **NO** | `tests/test_chain.py::ChainFlowTest::test_done_refused_mid_chain` |
| What happens when an agent dies holding a ticket? | Lease expires (default 30 min), ticket returns to its queue on the next claim or `recover`. After 3 expiries on one stage it escalates to a human. | `chain.py` `recover`; `tests/test_chain.py::RecoveryTest` |
| Can a ticket loop between roles forever? | **NO** — escalates after `AG_MAX_KICKBACKS` (default 3) | `tests/test_chain.py::ChainFlowTest::test_kick_back_limit_escalates` |
| Does a queue with no agent get noticed? | **YES** — `ticket.stalled` event once per timeout window. State is not changed. | `tests/test_chain.py::RecoveryTest::test_stalled_queue_alerts_once_per_window_without_state_change` |
| Do blocked and escalated tickets get noticed? | **YES** — `ticket.awaiting_human` on the first recovery pass, then once per review window, including escalations raised inside a claim | `tests/test_chain.py::ReviewFindingsTest::test_escalation_raised_during_claim_still_reported` |
| Does the operator get alerted? | **Only if they run `ticket.py recover --alert` (e.g. on a cron) with an alert channel, network permission `allow`, and approval.** It sends each escalation, block, stall, and awaiting-human event once, read from the event log. Nothing pushes alerts on its own. | `scripts/ticket.py` `_unalerted`; `tests/test_events.py::AlertWatermarkTest` |
| Is a scheduler required? | **NO** — recovery runs on every claim. `recover` exists for operators who want a cron. | `tests/test_chain.py::RecoveryTest::test_recovery_runs_on_claim` |
| Can an MCP agent clear a veto, resolve an escalation, or force a close? | **NO** — those exist only in `scripts/ticket.py` | `tests/test_chain.py::McpSurfaceTest::test_human_only_actions_not_exposed_over_mcp` |
| Are those CLI actions limited to humans? | **NO — limited to operator approval.** Any process with shell access while `AG_APPROVAL=1` or `runs/approval.ok` is present can run them. Approval is not bound to a ticket. The approval check runs after validation, so a bad id never consumes it. | `scripts/ticket.py` `_gate`; `tests/test_chain.py::ReviewFindingsTest::test_gate_runs_only_after_validation`; `tests/test_chain.py::CliTest` |
| Are thresholds in the wizard? | **NO** — env vars in 1.1 (`AG_LEASE_MINUTES`, `AG_MAX_ATTEMPTS`, `AG_MAX_KICKBACKS`, `AG_REVIEW_TIMEOUT_MINUTES`, `AG_QUEUE_TIMEOUT_MINUTES`) | `chain.py` `Settings.from_env` |

---

## 12.14 Verified agent identity (ADR-0011)

| Question | Answer | Cite |
|---|---|---|
| Are agent ids verified? | **Only once a registry exists.** With at least one active agent in `config/agents.json`, claim / heartbeat / submit / verdict require a token and the id comes from it. Without one, ids are self-reported and events say `agent_verified: false`. | `scripts/identity.py` `resolve`; `tests/test_identity_integrity.py::IdentityTest::test_token_required_once_registered`, `::test_unregistered_install_is_self_reported` |
| Can a registered agent claim outside its team or stages? | **NO** | `tests/test_identity_integrity.py::IdentityTest::test_team_and_role_come_from_registry` |
| Can one runtime review its own work under two ids? | **NO if the operator registers both under one principal.** Different principals for one runtime defeat it. | `tests/test_identity_integrity.py::IdentityTest::test_same_principal_cannot_review` |
| Are tokens stored? | **NO** — SHA-256 only; registry written 0600 | `tests/test_identity_integrity.py::IdentityTest::test_registry_never_stores_token_and_is_private` |
| Does a broken registry fall back to trusting ids? | **NO** — agent actions are refused | `tests/test_identity_integrity.py::IdentityTest::test_broken_registry_does_not_fall_back` |
| Can identity be switched off by emptying or redirecting the registry? | **Detected** — the head records that identity was on; writes stop until an operator accepts | `tests/test_identity_integrity.py::SecondReviewTest::test_identity_cannot_be_silently_switched_off` |
| Can unattributed work be put straight into review? | **NO** on an enforced install — needs a token (recorded as the worker) or operator approval; MCP creates need a token for the caller's team | `tests/test_identity_integrity.py::SecondReviewTest::test_tokenless_create_into_review_needs_operator_gate`, `::test_mcp_style_create_requires_token_when_enforced` |
| Are recovery events credited to the caller? | **NO** — never `agent_verified` | `tests/test_identity_integrity.py::SecondReviewTest::test_recovery_events_not_credited_as_verified` |
| Can a shared HTTP server inherit one agent's identity? | **NO** — refuses to start with `AG_AGENT_TOKEN` set | `tests/test_identity_integrity.py::HttpIdentityTest` |
| Can an agent read another agent's token? | **Not prevented in code.** Depends on how the operator stores tokens and separates OS users. | `docs/deployment-hardened.md` |
| Do tokens expire? | **NO** — revoke and re-add to rotate | `scripts/identity.py` |

---

## 12.15 Tamper detection (ADR-0012)

| Question | Answer | Cite |
|---|---|---|
| Can an agent write the ticket file or log directly? | **YES if it runs as the framework's OS user.** Code cannot prevent that. Separate users prevent it. | `docs/deployment-hardened.md` |
| Is a direct edit of the ticket file detected? | **YES**, on the next load; all writes stop until an operator runs `integrity accept` (approval) | `tests/test_identity_integrity.py::IntegrityTest::test_direct_ticket_edit_stops_writes_until_accepted` |
| Are edited, deleted, or truncated events detected? | **YES** — events since the last commit and truncation on every write; any line by `verify` (run by every `recover --alert`) | `tests/test_identity_integrity.py::IntegrityTest::test_edited_event_detected`, `::test_deleted_event_detected`, `::test_truncated_log_stops_writes` |
| Is removing the head (and the ticket file) detected? | **YES** once the log holds committed state, even with junk appended | `tests/test_identity_integrity.py::IntegrityTest::test_head_removed_detected`, `::test_head_and_store_removed_detected`; `tests/test_identity_integrity.py::SecondReviewTest::test_head_deleted_plus_junk_line_detected` |
| Is a consistent rollback of `runs/` (older ticket file + truncated log) detected? | **YES if the attacker cannot write `config/`** (the head lives there). Anyone who can write `config/` can roll back. | `tests/test_identity_integrity.py::SecondReviewTest::test_consistent_rollback_detected_when_head_is_protected`, `::test_head_lives_outside_runs` |
| Does accepting a problem hide later edits to the same line? | **NO** — accepted problems are bound to the line's bytes | `tests/test_identity_integrity.py::SecondReviewTest::test_accepted_problem_does_not_cover_later_edit` |
| Does a crash mid-commit look like tampering? | **NO** — rolled forward from the temp file; a torn append is moved aside on the next write | `tests/test_identity_integrity.py::IntegrityTest::test_crash_after_events_rolls_forward`; `tests/test_identity_integrity.py::SecondReviewTest::test_torn_append_is_repaired_not_a_halt` |
| Can a process without the key halt a keyed install by appending? | **NO** — it is refused before writing | `tests/test_identity_integrity.py::SecondReviewTest::test_keyless_process_cannot_poison_keyed_log` |
| Can an agent retry a failed commit and act twice? | **NO** — transient replace failures are retried; a persistent one returns `CommitPending` (do not retry) | `tests/test_identity_integrity.py::ReplaceRetryTest` |
| Can a read-only check race a commit and report false tampering? | **NO** — `verify`, `doctor`, `recover --alert`, and MCP `ticket_verify` hold the ticket lock | `tests/test_identity_integrity.py::LockedVerifyTest` |
| Can a forger recompute the hashes? | **Unkeyed: YES.** **Keyed: only with the key.** Downgrading keyed events to unkeyed and rewriting the head are detected. | `tests/test_identity_integrity.py::KeyedIntegrityTest` |
| Does the operator get told? | **Only via `recover --alert`** with a channel, network `allow`, and approval; integrity problems repeat every run until accepted | `scripts/ticket.py` `cmd_recover` |
| Is the verdict view covered? | **NO** — `runs/verdicts.jsonl` is a convenience view; the event log is the record | ADR-0012 |
| Does `doctor` tell me what is enforced? | **YES** — registry, key, permissions, verification, and the same-user limit | `tests/test_identity_integrity.py::CliIntegrityTest` |

---

## 12.16 Hardened macOS install (ADR-0013)

| Question | Answer | Cite |
|---|---|---|
| Can an agent with a shell write or read governance files? | **NO on a hardened install** for an ordinary account: it cannot list or read `runs/`, read the integrity key, registry, or bearer token, create an approval, or modify the code, the interpreter, or the venv. **YES on a same-user install.** | `.github/workflows/validate.yml` job `macos-hardened`; `scripts/macos/e2e-test.sh` "agent cannot" checks |
| Who can perform operator actions? | Anyone who can `sudo` (via `agctl`). Not an account without sudo. | `scripts/macos/agctl`; e2e check "run agctl without sudo" |
| Does the server leak its bearer token? | **NO** in the launchd plist; it is read from `config/` (700) at start | `scripts/macos/run-server.sh` |
| Does the hardened server inherit an agent identity or approval? | **NO** — stripped from its environment | `scripts/macos/run-server.sh` |
| Is it tested on a real Mac? | **YES** — every PR, `macos-latest` | job `macos-hardened` |
| Does a killed server come back? | **YES** — launchd KeepAlive | e2e check "server restarted by launchd" |
| Can agents on the same OS user read each other's tokens? | **YES** — tokens live in each agent's own config; separate agent users to prevent it | ADR-0013 |
| Is a remote (non-local) reviewer supported? | **Not by this install** — loopback only | ADR-0013 |
| Can an agent edit the Python the service runs? | **NO** — the install carries its own root-owned CPython, pinned by SHA-256; Homebrew's is not used | `scripts/macos/harden.sh`; e2e check "modify the interpreter" |
| Does the MCP server ever hold an operator approval? | **NO** — `agctl` passes approval to one process in its environment and writes no file | `scripts/macos/agctl` |
| Does agctl run on a loosened install? | **NO** — exit 4 if any install file is not root-owned or is writable by others | e2e check "agctl refuses a writable install file" |
| Does the installer accept a dangerous prefix or user? | **NO** — relative, top-level, foreign non-empty, agent-created, or user-owned-ancestor prefixes and non-service accounts are refused | e2e "installer refuses" checks |
| Does the installer run from a checkout an agent can write? | **NO** — refused unless the source is entirely root-owned (override: `--trust-source`) | e2e check "a source tree the agent owns" |
| Does root read the login user's HOME config during install? | **NO** — HOME, Python user site, pip config and cache, and curlrc are all switched off | `scripts/macos/harden.sh` |
| Are pip dependencies hash-pinned? | **NO** | ADR-0013 |

## 12.17 Deliverables and verdict reasons (1.2.1)

| Question | Answer | Cite |
|---|---|---|
| Does the reviewer see the submitted work? | **YES** — `submission.deliverable` on the ticket (up to 64 KiB of UTF-8, or a path/URL) and in the event log | `tests/test_chain.py::DeliverableTest::test_reviewer_sees_the_deliverable` |
| Does a worker see why work was kicked back? | **YES** — `lastVerdict` on the ticket it reclaims | `tests/test_chain.py::DeliverableTest::test_worker_sees_kick_back_reasons_on_reclaim` |
| Is the deliverable verified as the actual work? | **NO** — it is what the worker submitted; the framework stores it, it does not check it | `scripts/chain.py` `submit` |
| Does a reviewer see the worker's summary or earlier verdicts? | **NO** in review claims and `ticket_list` | `tests/test_chain.py::DeliverableTest::test_review_claim_is_blind` |
| Can a reviewer find earlier verdict reasons through `query_verdicts`? | **NO** for chain verdicts (reasons omitted). The event log still holds them for operators. | `tests/test_chain.py::DeliverableTest::test_query_verdicts_hides_chain_reasons` |
| Can an agent overturn a precedent over MCP? | **NO** without operator approval | `tests/test_events.py::ServerVerdictEventTest` |

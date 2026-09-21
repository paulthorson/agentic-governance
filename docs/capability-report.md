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
| 5.3 Personal allowlist email (historical) | Was in allowlist; **removed**. Admin is now localhost Host only (remote identity login removed) | `admin-access.ts` localhost gate; `docs/history-identity-scrub-2026-09-16.md` |
| Personal phone numbers in tree | **NO** found | Repo-wide grep (no matches) |
| 5.4 Prior personal GitHub username URL | HTTP **404** (2026-09-14 probe); tip + history scrubbed to `prior username` | Read-only `curl -sI`; history scrub note |
| History rewrite / `.mailmap` | **Done** 2026-09-16 (operator GO): `git-filter-repo` on `main`; author emails → `paulthorson@users.noreply.github.com` | `docs/history-identity-scrub-2026-09-16.md` |

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
| How is `/admin` gated? | Request Host must be localhost / loopback / `*.localhost`; else redirect to `/` with `admin=local-only` | `dashboard/src/middleware.ts`; `admin-access.ts` |
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
| Storage | Traction/improve content from repo files / synced content; no first-party DB module found in dashboard src for AG data | `dashboard/data/`, `docs/improve` sync script |
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

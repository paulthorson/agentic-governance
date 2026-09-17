# Agentic Governance — localhost improve dashboard

> **Public face is NOT this repo.** Marketing / living board / admin twin → [`paulthorson/agentic-governance-site`](https://github.com/paulthorson/agentic-governance-site) (Vercel project `agentic-governance-site` / [www.agenticgovernance.app](https://www.agenticgovernance.app)). 
> **This repo** = process/agent SoT + feed/corpus **publisher** + framework **download**. 
> **`dashboard/`** = **LOCALHOST-only** app for operator/dev. Framework git must **not** bind a Vercel project. 
> Keep `data/traction.json` + `npm run sync-improve` as publisher sources. **Do not delete** them. 
> Cos CORRECT Tip B [#124](https://github.com/paulthorson/agentic-governance/issues/124): detach framework Vercel (`agentic-governance` / former three host); **KEEP** this localhost app. Marketing-site Vercel untouched. 
> **HOLD:** #39 look pixels; ;. Settled release posture: Apache-2.0 only; **no acceptance gate**.

Next.js **localhost** app with two surfaces (route-split) — run with `npm run dev`; **not** a framework Vercel deploy:

1. **Public marketing preview** (`/`) — KPIs/charts, Get AG CTA, supporting content, traction widgets gated by `data/traction.json`.
2. **Admin backend** (`/admin/*`) — Google SSO + `ADMIN_EMAILS` allowlist (empty = nobody). Sensitive/internal KPI views.

**Publisher (stays in AG):** measured traction (`data/traction.json`), improve corpus (`docs/improve/`), and sync (`scripts/sync-improve.mjs`). Site consumes feeds **read-only**.

**UI source of truth:** this localhost app's declared design system (configured kit in `package.json`). Not a fleet SoT — product briefs name their own DS.

## Public vs admin

| Surface | Routes | Auth | What you see |
|---|---|---|---|
| Public | `/` (marketing) | None | Measured/baseline KPIs from improve reports; traction **only** when `value ≥ minVisible`; never invents numbers; never shows admin-only raw gates |
| Admin | `/admin`, `/admin/reports`, `/admin/traction`, `/admin/tokens`, `/admin/cycle-time`, `/admin/scars` | Google SSO + allowlist | Token placeholders (honest Baseline / unpaid), cycle-time tables, full improve report detail, traction raw values **including** below `minVisible` / null, anonymized scar index |

Public launch rule: traction stays hidden until Cos raises measured values past thresholds in `data/traction.json`. Admin may show unpaid / baseline labels honestly. **Do not invent live token/$ numbers.** No Studio PII in the repo or UI.

## Local run

```bash
cd dashboard
cp.env.example.env.local # fill AUTH_* for admin SSO locally
npm install
npm run sync-improve
# optional: refresh local UI-kit cheat sheet per package.json scripts
npm run dev
```

- Public: [http://localhost:3000](http://localhost:3000)
- Admin login: [http://localhost:3000/admin/login](http://localhost:3000/admin/login)

Without Google env vars, public pages still work; admin sign-in will fail until OAuth is configured.

## Auth (Auth.js v5 + Google)

- Package: `next-auth@beta` (Auth.js v5).
- Provider: Google only.
- Allowlist: `ADMIN_EMAILS` only (comma-separated Google account emails). Empty / unset = **nobody** (fail closed). No hardcoded addresses.
- `*@users.noreply.github.com` cannot authenticate via Google OAuth (not a Google account). Deployer must supply a real Google email.
- Middleware (`src/middleware.ts`) protects `/admin/*` except `/admin/login`.
- Sign-out control lives in admin chrome.

### Env vars (`.env.example`)

| Variable | Purpose |
|---|---|
| `AUTH_SECRET` | Auth.js encryption secret (`npx auth secret`) |
| `AUTH_GOOGLE_ID` | Google OAuth client ID |
| `AUTH_GOOGLE_SECRET` | Google OAuth client secret |
| `ADMIN_EMAILS` | Required for any admin login: comma list of Google emails. Empty = nobody. Placeholder in `.env.example` is `you@example.com` only. |

Never commit real secrets. `.env*.local` is gitignored.

## Framework Vercel — DETACHED

This framework repo must **not** deploy `dashboard/` to Vercel. No in-tree `vercel.json`. No framework GitHub homepage pointing at a `*.vercel.app` host. Public marketing face = **agentic-governance-site** only. Cos/operator detach of Vercel project `agentic-governance` (former three host) is ops outside this tip's git if still linked in the Vercel console.

## Google Cloud OAuth consent (localhost)

1. Google Cloud Console → **APIs & Services** → **Credentials** → Create **OAuth client ID** (Web application).
2. Configure OAuth consent screen (External or Internal as appropriate for your Google Cloud org).
3. **Authorized JavaScript origins**: `http://localhost:3000`.
4. **Authorized redirect URIs**: `http://localhost:3000/api/auth/callback/google`.
5. Copy Client ID → `AUTH_GOOGLE_ID`, Client secret → `AUTH_GOOGLE_SECRET`.

Auth.js auto-detects `AUTH_GOOGLE_ID` / `AUTH_GOOGLE_SECRET` for the Google provider.

## Data sources

| Feed | Path | Notes |
|---|---|---|
| Improve corpus | `../docs/improve/*.md` | Synced into app data for KPI / report views |
| Traction | `../data/traction.json` (and local copy under `dashboard/data/`) | Measured-only; never invent |
| Scars index | derived from improve / ledger publish side | Anonymized |

## Localhost UI kit conventions

Localhost dashboard UI SoT = this app's declared design system (configured in `package.json`). Fleet law does **not** name a private design-system brand as SoT — each product brief declares its own DS. Kit CLI notes (if any) live in `AGENTS.md`.

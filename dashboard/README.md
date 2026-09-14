# Agentic Governance — improve dashboard

> **Marketing face is moving.** Cos ACCEPT MERGED Eng extract plan [#56](https://github.com/paulthorson/agentic-governance/pull/56) @ `e7bb36e` — execute **GO**. 
> Public marketing / living board / admin twin **UI** → [`paulthorson/agentic-governance-site`](https://github.com/paulthorson/agentic-governance-site) (site face + Vercel `agentic-governance-site`). 
> **This repo stays** feed/corpus **publisher** + framework **download** — not the marketing host of record. 
> Keep `data/traction.json` + `npm run sync-improve` as publisher sources. **Do not delete** them. 
> UI below remains in-tree for **rollback** until the site PR lands and serves the extracted face — then retire/redirect legacy Vercel **agentic-governance-three** (do **not** break three yet). 
> **HOLD:** #39 look pixels; Get AG CTA pixels HOLD on look craft. Settled release posture: Apache-2.0 only; **no acceptance gate**; Get AGs removed. Extract execute continues on site repo **in parallel**. Status: [`docs/initiatives/marketing-site-extract-execute.md`](../docs/initiatives/marketing-site-extract-execute.md).

Next.js app with two surfaces on the **same Vercel deploy** (route-split) — **legacy / rollback host** until site extract is live:

1. **Public marketing** (`/`) — KPIs/charts, Get AG CTA, supporting content, traction widgets gated by `data/traction.json`.
2. **Admin backend** (`/admin/*`) — Google SSO + `ADMIN_EMAILS` allowlist (empty = nobody). Sensitive/internal KPI views.

**Publisher (stays in AG):** measured traction (`data/traction.json`), improve corpus (`docs/improve/`), and sync (`scripts/sync-improve.mjs`). Site consumes feeds **read-only**.

**UI source of truth: Meta Astryx** (`@astryxdesign/core` + `@astryxdesign/theme-neutral` + `@astryxdesign/cli`). Not a custom/Tailwind/shadcn primary UI.

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
npx astryx init # refreshes AGENTS.md cheat sheet if needed
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

## Vercel setup

1. **Root Directory** = `dashboard` (see `vercel.json`).
2. **Environment variables** (Production + Preview as needed):
 - `AUTH_SECRET`
 - `AUTH_GOOGLE_ID`
 - `AUTH_GOOGLE_SECRET`
 - `ADMIN_EMAILS` (Google account email(s); empty = nobody can sign in)
3. Build command: `npm run build` (syncs improve markdown when parent tree is present).
4. Deploy the marketing surface publicly when Cos unlocks launch (repo may stay private; site can be a public Vercel project).

## Google Cloud OAuth consent

1. Google Cloud Console → **APIs & Services** → **Credentials** → Create **OAuth client ID** (Web application).
2. Configure OAuth consent screen (External or Internal as appropriate for your Google Cloud org).
3. **Authorized JavaScript origins**: `https://<your-vercel-host>` (and `http://localhost:3000` for local).
4. **Authorized redirect URIs**:
 - `https://<your-vercel-host>/api/auth/callback/google`
 - `http://localhost:3000/api/auth/callback/google` (local)
5. Copy Client ID → `AUTH_GOOGLE_ID`, Client secret → `AUTH_GOOGLE_SECRET`.

Auth.js auto-detects `AUTH_GOOGLE_ID` / `AUTH_GOOGLE_SECRET` for the Google provider.

## Data sources

| Feed | Path | Notes |
|---|---|---|
| Improve reports | `../docs/improve/*.md` or `./content/improve/` | Prefer monorepo docs; `prebuild` syncs a copy |
| Optional JSON | `../data/improve.json` or `./data/improve.json` | If present, overrides markdown |
| Traction gates | `../data/traction.json` or `./data/traction.json` | Null values / high floors → public widgets stay hidden; admin shows raw |
| Scar index (admin) | `../projects/*/scars/*.md` | Anonymized title/status only — no Studio PII |

### Traction config (Cos / Paul)

Edit repo-root [`data/traction.json`](../data/traction.json): set a measured `value` and keep or lower `minVisible`. Flipping **public** visibility is **config-only**. Never invent live numbers. Admin always sees the raw rows.

## Astryx conventions

Agent cheat sheet: [`AGENTS.md`](./AGENTS.md). Discover components with:

```bash
npm run astryx -- component Button
npm run astryx -- build "…"
```

# Agentic Governance — improve dashboard

Next.js app with two surfaces on the **same Vercel deploy** (route-split):

1. **Public marketing** (`/`) — KPIs/charts, Get AG CTA, supporting content, traction widgets gated by `data/traction.json`.
2. **Admin backend** (`/admin/*`) — Google SSO (personal email) + email allowlist for Cos/Paul. Sensitive/internal KPI views.

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
- Allowlist: hardcoded `noreply address`, plus optional `ADMIN_EMAILS` (comma-separated) as override/extension.
- Middleware (`src/middleware.ts`) protects `/admin/*` except `/admin/login`.
- Sign-out control lives in admin chrome.

### Env vars (`.env.example`)

| Variable | Purpose |
|---|---|
| `AUTH_SECRET` | Auth.js encryption secret (`npx auth secret`) |
| `AUTH_GOOGLE_ID` | Google OAuth client ID |
| `AUTH_GOOGLE_SECRET` | Google OAuth client secret |
| `ADMIN_EMAILS` | Optional comma list of extra allowlisted emails |

Never commit real secrets. `.env*.local` is gitignored.

## Vercel setup (Cos / Paul)

1. **Root Directory** = `dashboard` (see `vercel.json`).
2. **Environment variables** (Production + Preview as needed):
   - `AUTH_SECRET`
   - `AUTH_GOOGLE_ID`
   - `AUTH_GOOGLE_SECRET`
   - `ADMIN_EMAILS` (optional; defaults still include `noreply address`)
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

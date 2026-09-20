# Agentic Governance — localhost improve dashboard

> **Public face is NOT this repo.** Marketing / living board → [`paulthorson/agentic-governance-site`](https://github.com/paulthorson/agentic-governance-site) (Vercel project `agentic-governance-site` / [www.agenticgovernance.app](https://www.agenticgovernance.app)). 
> **This repo** = process/agent SoT + feed/corpus **publisher** + framework **download**. 
> **`dashboard/`** = **LOCALHOST-only** app for operator/dev. Framework git must **not** bind a Vercel project. 
> Keep `data/traction.json` + `npm run sync-improve` as publisher sources. **Do not delete** them. 
> Cos CORRECT Tip B [#124](https://github.com/paulthorson/agentic-governance/issues/124): detach framework Vercel (`agentic-governance` / former three host); **KEEP** this localhost app. Marketing-site Vercel untouched. 
> **HOLD:** #39 look pixels; ;. Settled release posture: Apache-2.0 only; **no acceptance gate**.

Next.js **localhost** app with two surfaces (route-split) — run with `npm run dev`; **not** a framework Vercel deploy:

1. **Public marketing preview** (`/`) — KPIs/charts, Get AG CTA, supporting content, traction widgets gated by `data/traction.json`.
2. **Admin backend** (`/admin/*`) — **localhost hostnames only**. Sensitive/internal KPI views. Non-local Host headers are redirected to `/` with a clear notice. Remote identity login is not part of this app.

**Publisher (stays in AG):** measured traction (`data/traction.json`), improve corpus (`docs/improve/`), and sync (`scripts/sync-improve.mjs`). Site consumes feeds **read-only**.

**UI source of truth:** this localhost app's declared design system (configured kit in `package.json`). Not a fleet SoT — product briefs name their own DS.

## Public vs admin

| Surface | Routes | Auth | What you see |
|---|---|---|---|
| Public | `/` (marketing) | None | Measured/baseline KPIs from improve reports; traction **only** when `value ≥ minVisible`; never invents numbers; never shows admin-only raw gates |
| Admin | `/admin`, `/admin/reports`, `/admin/traction`, `/admin/tokens`, `/admin/cycle-time`, `/admin/scars` | Localhost Host only (fail closed off-box) | Token placeholders (honest Baseline / unpaid), cycle-time tables, full improve report detail, traction raw values **including** below `minVisible` / null, anonymized scar index |

Public launch rule: traction stays hidden until Cos raises measured values past thresholds in `data/traction.json`. Admin may show unpaid / baseline labels honestly. **Do not invent live token/$ numbers.** No Studio PII in the repo or UI.

## Local run

```bash
cd dashboard
cp.env.example.env.local # optional; no remote-login secrets required
npm install
npm run sync-improve
# optional: refresh local UI-kit cheat sheet per package.json scripts
npm run dev
```

- Public: [http://localhost:3000](http://localhost:3000)
- Admin metrics: [http://localhost:3000/admin](http://localhost:3000/admin)

Open `/admin` on localhost. Requests whose Host is not a local hostname are redirected to `/` with `?admin=local-only`.

## Access (localhost gate)

- Middleware (`src/middleware.ts`) allows `/admin/*` only when the request Host is `localhost`, loopback (`127.0.0.1` / `::1`), or `*.localhost`.
- Remote identity login is removed. Admin is a localhost Host gate only.
- Legacy path `/admin/login` redirects to `/admin` on localhost.
- Non-local `/admin` requests fail closed → redirect to public `/` with clear copy.

### Env vars (`.env.example`)

No remote-login secrets are required for admin. `.env.example` is a stub for optional local overrides only.

Never commit real secrets. `.env*.local` is gitignored.

## Framework Vercel — DETACHED

This framework repo must **not** deploy `dashboard/` to Vercel. No in-tree `vercel.json`. No framework GitHub homepage pointing at a `*.vercel.app` host. Public marketing face = **agentic-governance-site** only. Cos/operator detach of Vercel project `agentic-governance` (former three host) is ops outside this tip's git if still linked in the Vercel console.

## Data sources

| Feed | Path | Notes |
|---|---|---|
| Improve corpus | `../docs/improve/*.md` | Synced into app data for KPI / report views |
| Traction | `../data/traction.json` (and local copy under `dashboard/data/`) | Measured-only; never invent |
| Scars index | derived from improve / ledger publish side | Anonymized |

## Localhost UI kit conventions

Localhost dashboard UI SoT = this app's declared design system (configured in `package.json`). Fleet law does **not** name a private design-system brand as SoT — each product brief declares its own DS. Kit CLI notes (if any) live in `AGENTS.md`.

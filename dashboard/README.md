# Agentic Governance — public improve dashboard

Minimal Next.js marketing surface for continuous AG improve reporting.

**UI source of truth: Meta Astryx** (`@astryxdesign/core` + `@astryxdesign/theme-neutral` + `@astryxdesign/cli`). Not a custom/Tailwind/shadcn primary UI.

## What it shows (layout order)

1. **KPI strip + charts** — from `docs/improve/*.md` (optional JSON feed). Measured or method-estimated only; baseline/empty states are honest.
2. **Primary CTA** — Get / Download Agentic Governance (GitHub clone + quick start).
3. **Supporting** — what AG is, daily reports, changelog, contribute.
4. **Traction widgets** — fully implemented, **hidden** until `data/traction.json` values meet `minVisible` (launch default: all hidden).

## Local run

```bash
cd dashboard
npm install
npm run sync-improve
npx astryx init # refreshes AGENTS.md cheat sheet if needed
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Data sources

| Feed | Path | Notes |
|---|---|---|
| Improve reports | `../docs/improve/*.md` or `./content/improve/` | Prefer monorepo docs; `prebuild` syncs a copy |
| Optional JSON | `../data/improve.json` or `./data/improve.json` | If present, overrides markdown |
| Traction gates | `../data/traction.json` or `./data/traction.json` | Null values / high floors → widgets stay hidden |

### Traction config (Cos / Paul)

Edit repo-root [`data/traction.json`](../data/traction.json): set a measured `value` and keep or lower `minVisible`. Flipping visibility is **config-only** — no code change. Never invent live numbers.

## Vercel / public launch

- Set **Root Directory** to `dashboard` (see `vercel.json`).
- Build: `npm run build` (syncs improve markdown when parent tree is present).
- The GitHub repo may stay private during scaffold; **Cos/Paul must make the marketing surface public** (repo visibility and/or a separate public Vercel project) before the Get AG CTA reaches strangers.

## Astryx conventions

Agent cheat sheet: [`AGENTS.md`](./AGENTS.md). Discover components with:

```bash
npm run astryx -- component Button
npm run astryx -- build "…"
```

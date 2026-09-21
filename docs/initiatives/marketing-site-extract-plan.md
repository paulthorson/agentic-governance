# Eng extract plan — Marketing site split (Class A ops)

**Plain-English name:** Marketing site extract (Eng plan) 
**Type:** Class A ops / Eng extract plan — **PLAN ONLY** (no file moves, no pixels in this tip) 
**Status:** **MERGED LIVE** — Cos ACCEPT [#56](https://github.com/paulthorson/agentic-governance/pull/56) @ `e7bb36e` (2026-09-14). PRODUCT [#55](https://github.com/paulthorson/agentic-governance/pull/55) **MERGED LIVE** @ `19e451f`. Extract execute **GO** — see companion status [`marketing-site-extract-execute.md`](./marketing-site-extract-execute.md). 
**Owner seat:** Eng (+ Ops for Vercel); look pixels HOLD; Apache-2.0 LICENSE only (no acceptance gate) 
**Companion PRODUCT epic (AG PM owns — do not overwrite):** [`docs/initiatives/marketing-site-split.md`](./marketing-site-split.md) — [#55](https://github.com/paulthorson/agentic-governance/pull/55) @ `19e451f` (**MERGED LIVE**) 
**Companion execute status:** [`marketing-site-extract-execute.md`](./marketing-site-extract-execute.md)

---

## Tip for Cos / AG PM

[#56](https://github.com/paulthorson/agentic-governance/pull/56) is **MERGED LIVE** @ `e7bb36e` — this Eng extract plan is SoT. PRODUCT [#55](https://github.com/paulthorson/agentic-governance/pull/55) remains **MERGED LIVE** @ `19e451f`.

**Extract execute GO** — companion AG status: [`marketing-site-extract-execute.md`](./marketing-site-extract-execute.md). Site face extract lands in `agentic-governance-site` (parallel); this repo documents publisher posture without deleting dashboard UI yet.

**Eng HOLD look pixels** until operator yes (and stills / #39 craft clear). This plan does **not** authorize pixel work or `dashboard/src` look changes on AG.

**operator LOCK 2026-09-14 — Get AG (settled):** Apache-2.0 only; **no acceptance gate**. **Eng HOLD Get AG CTA pixels** remains on #39 look craft only. Class A extract docs / ops OK; site-repo extract continues **in parallel**.

---

## Cos OPEN Q LOCKs (folded 2026-09-14)

| # | LOCK | UI / face | Corpus / feeds |
|---|---|---|---|
| 1 | **Admin twin** | UI → **site repo** (`agentic-governance-site`) | AG owns feeds/corpus — site **consumes read-only** |
| 2 | **Anonymous Improve** | Public UX → **site** | Corpus stays in **AG** |
| 3 | **Living board** | UI → **site** | Feed **publisher stays AG**; site **read-only pull** |

Invariant across all three: **AG publishes / owns corpus; site never invents measured numbers and never owns the framework.**

---

## One-line promise

Site repo [`paulthorson/agentic-governance-site`](https://github.com/paulthorson/agentic-governance-site) hosts the **marketing + living board + admin twin + Anonymous Improve public UX**. Framework git [`paulthorson/agentic-governance`](https://github.com/paulthorson/agentic-governance) stays the product download face and **owns / publishes** measured feeds + improve corpus. Site **pulls read-only**. Get AG CTA always points at the product repo.

---

## Context (as of 2026-09-14)

| Fact | Detail |
|---|---|
| Marketing / site target repo | [`paulthorson/agentic-governance-site`](https://github.com/paulthorson/agentic-governance-site) — site face (marketing + board + admin twin UI + Anon Improve public UX) |
| Product / framework repo | [`paulthorson/agentic-governance`](https://github.com/paulthorson/agentic-governance) — download face + feed/corpus publisher |
| Current Next app (pre-extract) | `dashboard/` on AG = LOCALHOST app only (Tip B #124); public `/` + `/admin/*` live face = agentic-governance-site |
| **Vercel (critical path)** | Project **`agentic-governance-site`** already **created + Git-linked** to the site repo — prefer this path for post-merge execute (vs only rewiring three) |
| This PR | **PLAN DOCS ONLY** — no `dashboard/src` look changes; no #39 stills; no file moves |

Related SoT (do not reopen here):

- PRODUCT extract epic — [`marketing-site-split.md`](./marketing-site-split.md) — [#55](https://github.com/paulthorson/agentic-governance/pull/55) @ `19e451f` (**MERGED LIVE**; AG PM owns; do not overwrite)
- AG website UX Canvas SoT — [`ag-website-ux-canvas.md`](./ag-website-ux-canvas.md) — LIVE [#50](https://github.com/paulthorson/agentic-governance/pull/50) @ `6b24c4bc` (gate named [#48](https://github.com/paulthorson/agentic-governance/pull/48) @ `e9b4827`)
- Eng HOLD look / pixels until Cos craft + operator yes on stills (#39 track)

---

## MOVES → `agentic-governance-site` (site face)

| Surface | Current AG path | Notes |
|---|---|---|
| **Living board UI** | `dashboard/src/app/page.tsx`, `HomeView.tsx`, `KpiPanel.tsx`, `TractionStrip.tsx` | Cos LOCK #3 — UI on site; numbers from AG feed pull |
| Root layout / globals / providers | `dashboard/src/app/layout.tsx`, `globals.css`, `providers.tsx` | Site shell for public + admin twin |
| **Admin twin UI** | `dashboard/src/app/admin/**`, `Admin*` components, admin login route | Cos LOCK #1 — UI on site; consumes AG feeds/corpus read-only |
| Admin auth surface (site-hosted) | `auth.ts`, `middleware.ts`, `api/auth/**`, `lib/admin-access.ts` (as needed for `/admin` on site) | Admin twin on site should stay localhost-or-fail-closed; do not resurrect remote identity login on the framework dashboard |
| **Anonymous Improve public UX** | Public consent / Get AG / improve CTA surfaces on the board (when shipped) | Cos LOCK #2 — public UX on site; corpus stays AG |
| Public UX docs for face | `dashboard/docs/ux/*` (look / userflows / jtbd / visual stills for public `/` + admin twin craft) | Face craft packet travels with site repo |
| Research that feeds the face | `dashboard/docs/research/*` | Keep internal; **no competitor/agency brand names on public chrome** |
| Website design-system packet | `design-system.md` if present for website DS | Move with site face; do not strip AG constitution DS |
| Site Next app shell | `package.json` / lockfile / `tsconfig` / `next.config` to run public `/` + `/admin` twin | Do not add remote identity login for admin twin without a separate operator GO |
| Traction / board **consumer** | Client of `data/traction.json` + improve/KPI feeds | **Pull from AG** — never publish from site |
| Site `vercel.json` | At **repo root** of `agentic-governance-site` | Root directory = repo root |

**Not a move in this tip:** binaries / stills merge (#39). Stills follow Cos craft + operator yes on a later Eng/UX tip.

---

## STAYS in `agentic-governance` (product / framework + publisher)

| Surface | Path / ownership | Why it stays |
|---|---|---|
| Entire AG framework | plugins, harnesses, constitution, ledger, MCP, skills, agents, docs outside site extract | Product SoT — site git must **not** contain framework/harness constitution as product |
| **Feed publisher** (living board) | `data/traction.json`, KPI/scar publish libs, measured board JSON | Cos LOCK #3 — AG publishes; site pulls read-only |
| **Improve / Anonymous Improve corpus** | `docs/improve/**`, intake, sync pipeline `dashboard/scripts/sync-improve.mjs`, scars/KPI source markdown | Cos LOCK #2 — corpus stays AG; site UX only |
| **Feeds / corpus for admin twin** | Same measured + improve publish artifacts | Cos LOCK #1 — AG owns; site admin UI consumes read-only |
| Measured publish libs | `dashboard/src/lib/scars.ts`, `kpis.ts`, `improve.ts`, traction **publish** side | AG publishes; site consumes |
| Get AG / download | Product repo (and/or release assets on AG) | Site CTA points here — never at site repo as download face |
| Product Initiative epics | `docs/initiatives/*` including PM [`marketing-site-split.md`](./marketing-site-split.md) ([#55](https://github.com/paulthorson/agentic-governance/pull/55) @ `19e451f` (**MERGED LIVE**)) + this Eng plan | Plans stay on AG git |

---

## Feeds / contracts

| Rule | Detail |
|---|---|
| Direction | Site **PULLS** analytics / measured board / admin feeds **FROM AG** (git raw or published JSON) — **read-only** |
| Living board | UI on site; **publisher stays AG** |
| Admin twin | UI on site; AG owns feeds/corpus |
| Anonymous Improve | Public UX on site; **corpus stays AG** |
| Honesty | **Measured-only** numbers; hatch / hide when unpaid or below `minVisible`; **no invented KPI/ticker** |
| Product boundary | Site git must **not** contain framework/harness constitution as the product |
| Public chrome | **No** competitor / agency research brand names on public chrome (cites stay INTERNAL) |
| CTA contract | Get AG never targets site repo as the product download |

### Feed pull sketch (post-#55-MERGED Eng execute — not this tip)

1. AG continues to own and update measured `data/traction.json` + improve/KPI publish artifacts (+ Anon Improve corpus).
2. Site build/runtime fetches read-only (raw GitHub URL, release asset, or published JSON from AG).
3. If fetch fails or values unpaid → hatch / hide widgets (same honesty rules as today).
4. Site (public or admin twin) never writes measured feeds or improve corpus back into AG as publisher of record.

---

## Vercel (critical path + post-merge execute)

| Fact / step | Action |
|---|---|
| **Already done (critical path)** | Vercel project **`agentic-governance-site`** is **created + Git-linked** to [`paulthorson/agentic-governance-site`](https://github.com/paulthorson/agentic-governance-site) |
| After [#55](https://github.com/paulthorson/agentic-governance/pull/55) **MERGED** + this plan ACCEPT | Eng execute full extract into site repo; wire build to that Vercel project |
| Root Directory | **repo root** (site app at root — not nested `dashboard/`) |
| Site `vercel.json` | Add at site repo root |
| Site deploy env | Hosts public `/` **and** admin twin `/admin/*` (no remote identity login env on framework dashboard; site twin is a separate decision) |
| Former framework Vercel (`agentic-governance` / three) | **DETACHED** from framework git — public face = site only; do not re-bind |

### Safest default after split (Cos OPEN Q LOCKs)

| Deploy | Repo | Root | Hosts |
|---|---|---|---|
| **Site face** | `agentic-governance-site` | repo root | Public living board `/`, Anonymous Improve public UX, **admin twin** `/admin/*` |
| **Framework / publisher** | `agentic-governance` | (no marketing host required) | Product download + feed/corpus publish; optional AG-only tooling |

Rationale: one site product face (public + admin twin craft); AG remains framework download + measured publisher. Site always **consumes** AG feeds read-only.

---

## CTA

| CTA | Target | Never |
|---|---|---|
| **Get AG / download** | [`https://github.com/paulthorson/agentic-governance`](https://github.com/paulthorson/agentic-governance) (or AG release assets) | Site repo as product download |
| Stars / clone links in traction | Product repo (as measured in feed) | Invented counts |

**operator LOCK (public release, settled):** Get AG / download has **no acceptance gate**. Apache-2.0 LICENSE only. Eng HOLD Get AG CTA **pixels** on #39 look craft. Extract Class A docs/ops OK; site extract continues in parallel.

---

## Sequencing / gates

| Order | Gate | Owner |
|---|---|---|
| 0 | PRODUCT epic **MERGED LIVE** — [`marketing-site-split.md`](./marketing-site-split.md) — [#55](https://github.com/paulthorson/agentic-governance/pull/55) @ `19e451f` | AG PM / Cos |
| 1 | **This Eng extract plan** tipped (Cos OPEN Q LOCKs folded) | Eng |
| 2 | **Cos ACCEPT + MUST-merge this Eng plan** when CI green | Cos |
| 3 | Eng execute full extract + site Vercel wire — **separate PR(s)** (project already Git-linked); only after this plan MERGED | Eng |
| 4 | Look pixels / #39 stills | **HOLD** until Cos craft + **operator yes** — not authorized by this plan |

---

## Out of scope (this tip)

- No look pixel implementation / no `dashboard/src` visual changes on AG
- No #39 stills merge
- No actual file move into `agentic-governance-site` yet
- No Eng execute until **this** Eng plan is Cos ACCEPTed / MERGED ([#55](https://github.com/paulthorson/agentic-governance/pull/55) already **MERGED LIVE** @ `19e451f`)
- No overwrite of AG PM product epic [`marketing-site-split.md`](./marketing-site-split.md) ([#55](https://github.com/paulthorson/agentic-governance/pull/55) @ `19e451f` (**MERGED LIVE**))

---

## Acceptance sketch (for Cos ACCEPT of this Eng plan)

1. MOVES vs STAYS tables fold Cos OPEN Q LOCKs: admin twin UI → site; Anon Improve public UX → site; living board UI → site; AG owns feeds/corpus/publisher (read-only pull).
2. Vercel: `agentic-governance-site` already created + Git-linked (critical path); PRODUCT [#55](https://github.com/paulthorson/agentic-governance/pull/55) **MERGED LIVE** @ `19e451f`; Eng execute after this plan MERGED.
3. Get AG CTA → AG git (never site repo as download).
4. Measured-only honesty; no invented KPIs.
5. Eng HOLD look pixels until operator yes; Eng execute only after Cos ACCEPT / MUST-merge **this** Eng plan ([#55](https://github.com/paulthorson/agentic-governance/pull/55) already **MERGED LIVE** @ `19e451f`).
6. PLAN ONLY — no extract landed in this tip.

---

## Related

- Product epic (PM): [`marketing-site-split.md`](./marketing-site-split.md) — [#55](https://github.com/paulthorson/agentic-governance/pull/55) @ `19e451f` (**MERGED LIVE**)
- UX Canvas SoT: [`ag-website-ux-canvas.md`](./ag-website-ux-canvas.md)
- Improve feed / corpus: [`docs/improve/`](../improve/)
- Traction source (AG publisher): `data/traction.json`

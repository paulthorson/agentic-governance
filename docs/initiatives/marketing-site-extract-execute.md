# Eng extract execute — Marketing site split (Class A status)

**Plain-English name:** Marketing site extract execute (AG companion) 
**Type:** Class A ops / Eng execute **status** — docs + publisher posture only 
**Status:** **GO** after Eng plan [#56](https://github.com/paulthorson/agentic-governance/pull/56) **Cos ACCEPT MERGED LIVE** @ `e7bb36e` (2026-09-14) 
**Owner seat:** Eng (+ Ops for Vercel retire/redirect); Cos coordinates site PR; look pixels HOLD; Get AG acceptance-gate HOLD **superseded** (Apache-only settle) 
**Plans (do not overwrite):** PRODUCT [`marketing-site-split.md`](./marketing-site-split.md) [#55](https://github.com/paulthorson/agentic-governance/pull/55) @ `19e451f`; Eng [`marketing-site-extract-plan.md`](./marketing-site-extract-plan.md) [#56](https://github.com/paulthorson/agentic-governance/pull/56) @ `e7bb36e`

---

## Verdict (this tip)

| Item | Lock |
|---|---|
| Extract execute | **GO** — Eng plan [#56](https://github.com/paulthorson/agentic-governance/pull/56) **LIVE** @ `e7bb36e`; **continues on site repo in parallel** |
| Site face (marketing / living board / admin twin / Anon Improve public UX) | → [`paulthorson/agentic-governance-site`](https://github.com/paulthorson/agentic-governance-site) (parallel Eng extract — this AG tip does not wait on site merge) |
| This repo (`agentic-governance`) | Remains **feed / corpus publisher** + **framework download** — **not** the marketing host of record |
| Look / #39 pixels | **HOLD** — do **not** implement |
| Get AG acceptance gate | **SUPERSEDED** — settled release posture: Apache-2.0 only; **no acceptance gate**; Get AGs removed. Get AG CTA pixels HOLD on #39 look only |
| AG `dashboard/` UI | **Leave in place** for rollback until site PR lands and serves the extracted face — deprecate in README only; **no** full UI deletion in this companion tip |
| Former framework Vercel project (`agentic-governance` / three host) | **DETACH** — framework must not host a Vercel site; public face = `agentic-governance-site` only (Tip B #124) |

---

## Publisher posture (STAYS — do not delete)

AG remains publisher of record. Site **pulls read-only**. Never invent measured numbers.

| Artifact | Path | Rule |
|---|---|---|
| Traction feed | [`data/traction.json`](../../data/traction.json) (+ dashboard copy [`dashboard/data/traction.json`](../../dashboard/data/traction.json)) | **Keep** — living-board publisher source |
| Improve corpus | [`docs/improve/`](../improve/) | **Keep** — Anonymous Improve corpus stays AG |
| Improve sync | [`dashboard/scripts/sync-improve.mjs`](../../dashboard/scripts/sync-improve.mjs) (`npm run sync-improve` / `prebuild`) | **Keep / improve** — publisher pipeline |
| Measured publish libs | `dashboard/src/lib/` scars / kpis / improve / traction **publish** side | **Keep** while UI may still live here for rollback |
| Framework / download face | Repo root README, harnesses, constitution, MCP, release assets | **Keep** — Get AG targets this git only |

Invariant (Cos OPEN Q LOCKs from [#56](https://github.com/paulthorson/agentic-governance/pull/56)): **AG publishes / owns corpus; site never invents measured numbers and never owns the framework.**

---

## Site face vs AG host

| Face | Repo | Host of record (post-extract) |
|---|---|---|
| Marketing + living board UI + admin twin UI + Anon Improve **public UX** | [`agentic-governance-site`](https://github.com/paulthorson/agentic-governance-site) | Vercel project **`agentic-governance-site`** (already created + Git-linked) |
| Framework download + feed/corpus **publisher** | [`agentic-governance`](https://github.com/paulthorson/agentic-governance) | No marketing host required once site serves; optional AG-only tooling |

### Legacy deploy (rollback window)

| Deploy | Action now | Action later |
|---|---|---|
| Former framework Vercel (`agentic-governance` / three) | **DETACH** from framework git (no `vercel.json`; no homepage `*.vercel.app`) | Cos/operator console detach if still linked |
| AG `dashboard/` sources | **KEEP as LOCALHOST app** — do **not** delete | Not a framework Vercel deploy; public face = site only |

---

## operator LOCK 2026-09-14 — Get AG (superseded by release settle)

> **Superseded (operator LOCK public release):** [redacted] Get AG/DRAFT files
> were **removed**. Settled posture: free/open source Apache-2.0; **no acceptance gate
> anywhere**; LICENSE is the only use governor. No replacement legal text.

**Prior HOLD (historical):** [redacted] / counsel-before-ship language from [#57](https://github.com/paulthorson/agentic-governance/pull/57) / site PR #3 is **void** for this repo’s download face under the settled posture.

| Requirement | Detail |
|---|---|
| **No acceptance gate** | Get AG / download proceeds without an accept step. |
| **License only** | Apache-2.0 LICENSE + NOTICE govern use of the software. |
| **Eng HOLD (look)** | Get AG CTA **pixels** remain HOLD on #39 look craft — separate from legal drafts. |
| **CTA target** | Get AG / download → [`https://github.com/paulthorson/agentic-governance`](https://github.com/paulthorson/agentic-governance) (or AG release assets) — **never** the site repo as product download. |

### Parallel track

**Extract execute continues on the site repo in parallel** — AG companion docs / publisher posture here do **not** block site extract PRs. Site-repo acceptance gate cleanup is Cos-owned separately.

---

## This companion tip does / does not

### Does

1. Record extract execute **GO** after [#56](https://github.com/paulthorson/agentic-governance/pull/56) @ `e7bb36e`.
2. Clarify AG = **publisher + download**; site = **marketing host of record** (once serving).
3. Keep traction + improve sync as publisher sources.
4. Fold settled release posture (**no acceptance gate**; Apache-2.0 only; Get AGs removed; Get AG CTA pixels HOLD on #39 look) into execute status.
5. Document legacy three retire/redirect **after** site serves — without breaking three now.
6. Mark `dashboard/` marketing face as moving / deprecated-as-host in README while leaving UI for rollback.
7. Note that **site-repo extract execute continues in parallel** (not gated on this AG companion merge).

### Does not

- Implement #39 look pixels / `dashboard/src` visual redesign.
- Delete dashboard UI in this first companion tip (coordinate with site PR).
- Re-bind framework git to a Vercel marketing host (Cos CORRECT: framework = localhost dashboard only).
- Overwrite PRODUCT epic or Eng extract **plan** files.
- Invent replacement Terms / privacy / warranty text for deleted Get AGs.
- Reintroduce an acceptance gate on Get AG / download.

---

## Sequencing pointer

| Order | Gate | State |
|---|---|---|
| 0 | PRODUCT epic [#55](https://github.com/paulthorson/agentic-governance/pull/55) @ `19e451f` | **MERGED LIVE** |
| 1 | Eng extract plan [#56](https://github.com/paulthorson/agentic-governance/pull/56) @ `e7bb36e` | **MERGED LIVE** — Cos ACCEPT |
| 2 | Site extract PR on `agentic-governance-site` | **In parallel** — marketing face move continues (not blocked by AG companion) |
| 3 | **This AG companion** (docs + publisher posture) | **This tip** |
| 3a | Get AGs | **REMOVED** — no acceptance gate; Apache-2.0 only |
| 4 | Detach framework Vercel / clear homepage | Tip B #124 — site already public face |
| 5 | Optional AG `dashboard/` UI deletion | Only after site PR landed + Cos green |
| 6 | Look / #39 Get AG CTA pixels | **HOLD** until operator yes on look craft |

---

## Related

- Eng plan: [`marketing-site-extract-plan.md`](./marketing-site-extract-plan.md) — [#56](https://github.com/paulthorson/agentic-governance/pull/56) @ `e7bb36e`
- PRODUCT epic: [`marketing-site-split.md`](./marketing-site-split.md) — [#55](https://github.com/paulthorson/agentic-governance/pull/55) @ `19e451f`
- Public release: Apache-2.0 LICENSE + NOTICE; Get AGs **removed**; no acceptance gate
- Anonymous Improve (anonymous basics / value exchange): [`anonymous-improve-feedback.md`](./anonymous-improve-feedback.md)
- Traction publisher: [`data/traction.json`](../../data/traction.json)
- Dashboard publisher README: [`dashboard/README.md`](../../dashboard/README.md)

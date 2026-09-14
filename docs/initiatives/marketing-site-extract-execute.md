# Eng extract execute — Marketing site split (Class A status)

**Plain-English name:** Marketing site extract execute (AG companion) 
**Type:** Class A ops / Eng execute **status** — docs + publisher posture only 
**Status:** **GO** after Eng plan [#56](https://github.com/paulthorson/agentic-governance/pull/56) **Cos ACCEPT MERGED LIVE** @ `e7bb36e` (2026-09-14) 
**Owner seat:** Eng (+ Ops for Vercel retire/redirect); Cos coordinates site PR; look pixels HOLD; Get AG T&Cs HOLD 
**Plans (do not overwrite):** PRODUCT [`marketing-site-split.md`](./marketing-site-split.md) [#55](https://github.com/paulthorson/agentic-governance/pull/55) @ `19e451f`; Eng [`marketing-site-extract-plan.md`](./marketing-site-extract-plan.md) [#56](https://github.com/paulthorson/agentic-governance/pull/56) @ `e7bb36e`

---

## Verdict (this tip)

| Item | Lock |
|---|---|
| Extract execute | **GO** — Eng plan [#56](https://github.com/paulthorson/agentic-governance/pull/56) **LIVE** @ `e7bb36e`; **continues on site repo in parallel** |
| Site face (marketing / living board / admin twin / Anon Improve public UX) | → [`paulthorson/agentic-governance-site`](https://github.com/paulthorson/agentic-governance-site) (parallel Eng extract — this AG tip does not wait on site merge) |
| This repo (`agentic-governance`) | Remains **feed / corpus publisher** + **framework download** — **not** the marketing host of record |
| Look / #39 pixels | **HOLD** — do **not** implement |
| Get AG T&Cs gate | **HOLD** — **acceptance gate** required; DRAFT outline SoT **LIVE** [#57](https://github.com/paulthorson/agentic-governance/pull/57) @ `9b5bcd9` (production ToS **NOT** until [redacted]); **never ship production ToS without counsel**; drafts carry **lawyer-review banner**; Get AG CTA pixels HOLD until acceptance gate path (see below) |
| AG `dashboard/` UI | **Leave in place** for rollback until site PR lands and serves the extracted face — deprecate in README only; **no** full UI deletion in this companion tip |
| Legacy Vercel **agentic-governance-three** | **Do not break** yet — document **retire / redirect** only after site project is serving the extracted face |

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
| **agentic-governance-three** (Root Directory `dashboard`) | **Leave serving** — do not tear down / break | After site is serving extracted face → **retire / redirect** onto site project (Class A ops; Cos/Eng) |
| AG `dashboard/` sources | **Stay in tree** (rollback) — README marks marketing face **moving** / deprecated as host of record | Full UI deletion only after site PR landed + Cos green for delete |

---

## Paul LOCK 2026-09-14 — Get AG T&Cs (fold into execute)

> **DRAFT / counsel gate — lawyer-review banner.** Get AG ToS outline SoT **LIVE** as DRAFT only — [#57](https://github.com/paulthorson/agentic-governance/pull/57) @ `9b5bcd9` → [``](../legal/). Product outline — **not** legal advice and **not** a production ToS. **Never ship production ToS without counsel.** Licensed [redacted] required before Cos treats any draft as production / before Eng ships Get AG CTA pixels.

**Gate:** **[redacted]** Terms & Conditions **before** download / Get AG CTA ship ([redacted] = FAIL).

| Requirement | Detail |
|---|---|
| **[redacted]** | Operator must **affirmatively accept** T&Cs before Get AG / download proceeds — not a passive footer link alone. |
| **Cos ToS outline (DRAFT LIVE)** | [#57](https://github.com/paulthorson/agentic-governance/pull/57) @ `9b5bcd9` — [``](../legal/). DRAFT placeholders only; **lawyer-review banner** on every draft surface. Production ToS **NOT** until [redacted]. |
| **Liability** | T&Cs must cover product liability / scope note baseline for download and use of the framework (plain English; no fake legal advice in chrome). |
| **Anonymous basics** | Fold the free ↔ anonymous-basics value exchange from [`anonymous-improve-feedback.md`](./anonymous-improve-feedback.md): AG is free because operators share **anonymous basics** (default on); richer diagnostic logs remain **opt-in**; never secrets / tokens / PII / absolute paths / product sauce. |
| **Never ship production ToS without counsel** | **Hard lock** — do not promote outline → production ToS, do not treat #57 outline as production legal text, and do not ship Get AG CTA pixels until [redacted] is confirmed by Paul/Cos. |
| **Eng HOLD** | Get AG CTA pixels **HOLD** until **acceptance gate path** + counsel clear — **stacked on** #39 look HOLD. Class A extract docs / publisher / ops (including **parallel site-repo extract**) remain OK. |
| **CTA target** | Get AG / download → [`https://github.com/paulthorson/agentic-governance`](https://github.com/paulthorson/agentic-governance) (or AG release assets) — **never** the site repo as product download. |

### Parallel track

**Extract execute continues on the site repo in parallel** — AG companion docs / publisher posture here do **not** block site extract PRs. ToS / acceptance gate / counsel remain a separate HOLD from Class A file-move execute.

---

## This companion tip does / does not

### Does

1. Record extract execute **GO** after [#56](https://github.com/paulthorson/agentic-governance/pull/56) @ `e7bb36e`.
2. Clarify AG = **publisher + download**; site = **marketing host of record** (once serving).
3. Keep traction + improve sync as publisher sources.
4. Fold Paul LOCK T&Cs (**acceptance gate**; liability + anonymous basics; DRAFT outline [#57](https://github.com/paulthorson/agentic-governance/pull/57) @ `9b5bcd9` LIVE; **never ship production ToS without counsel**; lawyer-review banner on drafts; Get AG CTA pixels HOLD until acceptance gate path) into execute status.
5. Document legacy three retire/redirect **after** site serves — without breaking three now.
6. Mark `dashboard/` marketing face as moving / deprecated-as-host in README while leaving UI for rollback.
7. Note that **site-repo extract execute continues in parallel** (not gated on this AG companion merge or on ToS counsel).

### Does not

- Implement #39 look pixels / `dashboard/src` visual redesign.
- Delete dashboard UI in this first companion tip (coordinate with site PR).
- Break or rewire **agentic-governance-three** until site is serving.
- Overwrite PRODUCT epic or Eng extract **plan** files.
- Ship Get AG ToS / CTA pixels without counsel — **never ship production ToS without counsel**.
- Treat Cos ToS outline [#57](https://github.com/paulthorson/agentic-governance/pull/57) @ `9b5bcd9` as production legal text (it is DRAFT outline SoT only).

---

## Sequencing pointer

| Order | Gate | State |
|---|---|---|
| 0 | PRODUCT epic [#55](https://github.com/paulthorson/agentic-governance/pull/55) @ `19e451f` | **MERGED LIVE** |
| 1 | Eng extract plan [#56](https://github.com/paulthorson/agentic-governance/pull/56) @ `e7bb36e` | **MERGED LIVE** — Cos ACCEPT |
| 2 | Site extract PR on `agentic-governance-site` | **In parallel** — marketing face move continues (not blocked by AG companion or ToS counsel) |
| 3 | **This AG companion** (docs + publisher posture) | **This tip** |
| 3a | Cos Get AG ToS outline | **DRAFT LIVE** [#57](https://github.com/paulthorson/agentic-governance/pull/57) @ `9b5bcd9` — lawyer-review banner; production ToS NOT until [redacted] |
| 4 | Retire / redirect **agentic-governance-three** | **After** site serves extracted face |
| 5 | Optional AG `dashboard/` UI deletion | Only after site PR landed + Cos green |
| 6 | Look / #39 + Get AG **acceptance gate** CTA pixels | **HOLD** until Paul yes + **acceptance gate path** + counsel clears production ToS (never ship without counsel) |

---

## Related

- Eng plan: [`marketing-site-extract-plan.md`](./marketing-site-extract-plan.md) — [#56](https://github.com/paulthorson/agentic-governance/pull/56) @ `e7bb36e`
- PRODUCT epic: [`marketing-site-split.md`](./marketing-site-split.md) — [#55](https://github.com/paulthorson/agentic-governance/pull/55) @ `19e451f`
- Cos Get AG ToS outline (DRAFT LIVE): [#57](https://github.com/paulthorson/agentic-governance/pull/57) @ `9b5bcd9` — [``](../legal/)
- Anonymous Improve (anonymous basics / value exchange): [`anonymous-improve-feedback.md`](./anonymous-improve-feedback.md)
- Traction publisher: [`data/traction.json`](../../data/traction.json)
- Dashboard publisher README: [`dashboard/README.md`](../../dashboard/README.md)

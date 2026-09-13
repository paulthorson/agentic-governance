# Public dashboard — Check 7 JTBD

**Cite Research:** [`../research/evidence.md`](../research/evidence.md) 
**Cos LOCK add-on 2026-09-13:** Delight is tied to **measured events** (improve MD, merged PRs, retros) — never decoration.

---

## Research cite block

| Artifact | Role |
| --- | --- |
| [`dashboard/docs/research/evidence.md`](../research/evidence.md) | ADV_COMP SoT — our-hole / competitor-hole / do-not-copy + Motion / delight patterns |

**Mobbin URLs motivating design choices (Adv must open):**

- Stripe overview — https://mobbin.com/screens/673e89af-fe9e-4ab9-ac27-435dedf21888
- Stripe Radar / zero density — https://mobbin.com/screens/02176a39-e453-4570-af73-6af00fbe681b
- Vercel Analytics — https://mobbin.com/screens/900542f7-c157-4445-8f88-d79dca719c7a
- Linear Overview + Progress — https://mobbin.com/screens/e88b6bd7-3d4b-4e1e-8cd7-a9d2a6852795
- Linear timeline + milestones — https://mobbin.com/screens/c1cc22aa-69de-468c-b200-cf80f05ac1c7
- Mixpanel empty — https://mobbin.com/screens/bef3e439-48d3-42de-9b9d-d8f6eb6ff2cd
- Amplitude empty — https://mobbin.com/screens/1c4908e9-c1e6-4ed7-97f2-a757099c5462
- Mixpanel board empty — https://mobbin.com/screens/194a56e8-d5e0-4349-8353-cf7a6cc25bbf
- Amplitude home KPIs — https://mobbin.com/screens/7ebf30d2-b1ea-4c85-b123-76f4347ba357
- Better Stack Reporting — https://mobbin.com/screens/d4ecfb68-a860-41f6-9dc4-93f1b027c7c9
- Neon inactive hatch — https://mobbin.com/screens/a140f8f1-d12e-407f-81c8-e06186ce5350
- Cloudflare Workers Overview — https://mobbin.com/screens/c2a81c26-677d-43c2-8f93-3fad6513e3bd

---

## JTBD 1 — Visitor evaluating AG

**When** I land on the public dashboard, **I want to** see a living ops/marketing face (KPI cards, real viz, honest empty) **so I can** decide whether Agentic Governance is a serious framework and take Get AG / GitHub.

| Design choice | Motivating evidence |
| --- | --- |
| KPI card system + sparklines | Stripe, Cloudflare, Amplitude home |
| Chart as product hero, not MD dump | Better Stack, Vercel Analytics |
| Designed empty when unpaid | Mixpanel empty, Neon hatch |
| **Delight:** count-up / sparkline flux only if measured feeds update while I watch; otherwise calm | evidence §7 — inferred from live boards; Mobbin stills static |

---

## JTBD 2 — Operator (Paul / Cos) checking measured improve health

**When** I open `/` (or `/reports`), **I want to** see measured improve health at a glance (KPI cards + Latest Update + Progress) **so I can** know what shipped without reading a docs dump as the hero.

| Design choice | Motivating evidence |
| --- | --- |
| Latest Update card + Progress rail | Linear Overview + Progress |
| Full MD secondary / collapsed | evidence our-hole: MD-as-hero |
| **Delight:** subtle activity pulse when a real improve lands; ship toast when a measured ship (e.g. merged PR) is recorded | evidence §7; Linear Latest Update analog |
| No fake ticker / invented pulse | evidence motion do-not-copy |

---

## JTBD 3 — Outsider filing an improve PR

**When** I evaluate contributing, **I want to** see honest Baseline/empty + clear next steps (template / Get AG / improve path) **so I can** file an improve PR without being sold invented traction.

| Design choice | Motivating evidence |
| --- | --- |
| Recovery links on empty | Mixpanel empty, Amplitude no-match, Mixpanel board templates |
| Traction gated | evidence keep; live `/` already gates |
| **Delight:** none until my (or others’) measured merge/retro/improve lands — then count-up / ship toast from feeds | evidence §7 + motion do-not-copy |

---

## Delight ↔ measured event map

| Delight | Measured trigger | JTBD |
| --- | --- | --- |
| KPI count-up | improve MD KPI / merged PRs / retros feed update | 1, 2 |
| Sparkline flux | new measured point on that series | 1, 2 |
| Activity pulse | real improve entry lands | 2 |
| Ship toast | measured ship event recorded | 2, 3 (after merge) |

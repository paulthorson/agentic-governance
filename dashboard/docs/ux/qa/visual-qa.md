# Check 8 — VISUAL_STEP_STILLS index

**Epic:** Public AG dashboard (`/`) — Cos GO 2026-09-13
**Sensor:** `dashboard/docs/ux/qa/visual-stills/` + this index (dashboard-local; same contract as `docs/epics/<slug>/qa/`).
**Stacked on:** `RESEARCH_BEFORE_ENHANCE` + Check 7 (`userflows.md` / `jtbd.md`) + `ADV_COMP` LIVE #20 @ `9721af1` (Adv PASS `b868672`).
**Research:** [`dashboard/docs/research/evidence.md`](../../research/evidence.md).
**Baseline (raw live, not this pack):** AG PM live `/` captures; used only to name current FAILs.
**UI SoT:** Meta Astryx as product face — these stills are the IA/chrome target, not an Eng implementation.
**P0:** no secrets, keys, emails, PII, or absolute host paths.

Stills are **proposed** product chrome. Numbers are the live measured set only (Daily improve 4, Retros 2, AG PRs 2, Cycle time Baseline, Tokens unpaid, 5 traction metrics gated).

## Steps

| Step | Flow | Desktop | Mobile | Motion (what / when / why) |
| --- | --- | --- | --- | --- |
| F1-land | F1 Land & scan | [f1-land-desktop.png](./visual-stills/f1-land-desktop.png) | [f1-land-mobile.png](./visual-stills/f1-land-mobile.png) | **What:** KPI values sit static on first paint; sparklines are already-drawn measured series (no jitter). **When:** only if a feed adds a point after load. **Why:** living board, not a fake ticker. |
| F1-chart | F1 chart | [f1-chart-desktop.png](./visual-stills/f1-chart-desktop.png) | [f1-chart-mobile.png](./visual-stills/f1-chart-mobile.png) | **What:** null-day hatch is static; new point may ease in. **When:** a measured day lands. **Why:** Neon hatch / Stripe designed zero. |
| F2-update | F2 Latest update | [f2-update-desktop.png](./visual-stills/f2-update-desktop.png) | [f2-update-mobile.png](./visual-stills/f2-update-mobile.png) | **What:** card + rail only. **When:** n/a. **Why:** reports stay secondary. |
| F3-empty | F3 Baseline | [f3-empty-desktop.png](./visual-stills/f3-empty-desktop.png) | [f3-empty-mobile.png](./visual-stills/f3-empty-mobile.png) | **What:** hatch/label only; no count-up. **When:** never until a ledger exists. **Why:** designed empty; do not invent Cycle time or Tokens. |
| F4-cta | F4 Get AG | [f4-cta-desktop.png](./visual-stills/f4-cta-desktop.png) | [f4-cta-mobile.png](./visual-stills/f4-cta-mobile.png) | **What:** header Get AG reserved-width; no layout shift. **When:** hover/focus only. **Why:** one primary; live mobile clip is a FAIL we close. |
| F5-toast | F5 Ship toast | [f5-toast-desktop.png](./visual-stills/f5-toast-desktop.png) | [f5-toast-mobile.png](./visual-stills/f5-toast-mobile.png) | **What:** one quiet toast + optional count-up on the KPI that changed. **When:** a measured merge/ship/retro is recorded. **Why:** never on load; no invented pulse. |

## Check 8 FAIL review (UX self-check — Critic still stamps separately)

Per-step mobile AND desktop: yes. CLS/Fitts/Hick designed PASS (one Get AG; theme slot reserved not in CTA cluster). Jakob: mobile menu exception documented in userflows.md. Miller NOTE.

## Next

Stills → AG PM → Cos before Eng. No Eng GO from UX alone.

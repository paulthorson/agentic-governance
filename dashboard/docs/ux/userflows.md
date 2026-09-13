# Userflows — Living graph splash + admin twin

**Gate:** Critic Check 7 — Mermaid (entry, success, empty/error, exits). 
**Jobs:** [`jtbd.md`](./jtbd.md) J1–J7. 
**Splash SoT:** #28 @ `f9f38ff` [`living-graph-splash-2026-09-13.md`](../research/living-graph-splash-2026-09-13.md). 
**Motion SoT:** #27 @ `235610e`. Honesty SoT: #20 @ `9721af1`. 
**Supersedes:** F1 “Land & scan KPIs” strip. Land is **explore-the-graph**. 
**Chrome (Jakob):** Brand + one **Get AG** on public desk and mobile. Graph is the product. Mobile: no CLS on graph (reserved stage height). Admin: same graph chrome, no Get AG.

**Measured on frames (do not invent):** Daily improve **4**, Retros **2**, Merged PRs **2** (12 Sep). Cycle unpaid → hatch/omit. Role nodes are the locked loop, not invented projects. Fleet names omitted on public.

---

## F1 — Land default graph (J1)

Entry: open `/`. Success: they see the loop graph, idle still. Empty: unpaid edges hatched/omitted. Exit: hover (F2), click (F3), Get AG (F6), leave.

```mermaid
flowchart TD
  E1[Entry: open public /] --> G1[Reserved graph stage — no CLS]
  G1 --> L1[Role nodes: Research → PM → UX → Eng → QA → Adv → Cos]
  L1 --> M1{Edge or flux measured?}
  M1 -->|yes: improve 4 / retros 2 / PRs 2| M2[Draw edge or count from store]
  M1 -->|unpaid: cycle / unknown fleet| M3[Hatch or omit — no invented node]
  M2 --> I1[Idle still — no pulse]
  M3 --> I1
  I1 --> X1[Exit: hover F2]
  I1 --> X2[Exit: click F3]
  I1 --> X3[Exit: Get AG F6]
  I1 --> X4[Exit: leave]
```

**Cite:** #28 §1–2, §5 do-not-copy strip / force-graph / fake pulse. Fitness paused = idle still.

---

## F2 — Hover / focus readout (J2)

Entry: pointer or keyboard focus on a node or edge. Success: one quiet tooltip (date / count / stamp family). Empty: unpaid → hatch label, no number. Exit: blur back to idle graph.

```mermaid
flowchart TD
  E2[Entry: hover or focus node/edge] --> Q1{Paid fact in store?}
  Q1 -->|yes| T1[Quiet tooltip: date + count or stamp family]
  Q1 -->|no| T2[Hatch / omit label — never invent]
  T1 --> X1[Exit: blur — tooltip gone, graph idle]
  T2 --> X1
```

**Cite:** #28 §3b Stripe / Arcade hover. Public: no project name in tooltip.

---

## F3 — Click → inspect seat (J3)

Entry: click a role node. Success: zoom/inspect — ROLE + shipped work. Error: no shipped facts → designed empty inspect. Exit: close inspect, back to land.

```mermaid
flowchart TD
  E3[Entry: click role node] --> Z1[Zoom / inspect panel]
  Z1 --> Z2[Show persona ROLE — not a human name]
  Z2 --> Z3{Shipped work in store?}
  Z3 -->|yes| Z4[List measured ships only]
  Z3 -->|no| Z5[Empty inspect: hatch + why unpaid]
  Z4 --> X1[Exit: close — return to land graph]
  Z5 --> X1
  Z1 --> Z6[Error: refuse secrets / paths / Studio]
  Z6 --> X1
```

**Cite:** #28 §3a Cofounder / Railway / Twenty inspect. Competitor-hole: n8n / LangSmith IDE. Public: no project names.

---

## F4 — Mobile graph (J1, Jakob)

Entry: open `/` on a phone. Success: same graph, reserved height, no layout shift. Inspect is a sheet, not a new chrome family. Exit: same as F1–F3.

```mermaid
flowchart TD
  E4[Entry: mobile /] --> H1[Brand + reserved Get AG]
  H1 --> S1[Graph stage reserved height — no CLS]
  S1 --> S2{Gesture}
  S2 -->|hover analog: tap-hold| F2[Readout F2]
  S2 -->|tap node| F3[Inspect as sheet F3]
  S2 -->|none| I1[Idle still]
  I1 --> X1[Exit: leave or Get AG]
```

**Cite:** #28 mobile stills required; Check 8 FAIL = CLS / chrome inconsistency.

---

## F5 — Toast-on-ship, then node stays (J6)

Entry: measured ship/merge/retro written to the store. Success: quiet toast + one node/edge twitch + count remains. Idle: nothing. Exit: toast dismisses; new count stays.

```mermaid
flowchart TD
  E5[Entry: store records a ship] --> Q1{Real measured event?}
  Q1 -->|no| Q2[Idle still — no toast, no twitch]
  Q1 -->|yes| Q3[Quiet toast]
  Q3 --> Q4[Micro-anim: that node or edge only]
  Q4 --> Q5[Count / node updates and STAYS]
  Q5 --> X1[Exit: toast gone; graph calm with new fact]
  Q2 --> X2[Exit: stay calm]
```

**Cite:** #28 §2 rules 6–7; Linear toast; #27 toast; Fitness idle still. No fake ticker.

---

## F6 — Get AG (J4)

Entry: header Get AG. Success: GitHub. Admin: this control does not exist.

```mermaid
flowchart TD
  E6[Entry: public header Get AG] --> A1[One primary → GitHub]
  A1 --> A2{Link up?}
  A2 -->|yes| X1[Exit: clone]
  A2 -->|no| A3[Error: CTA stays — no invented mirror]
  A3 --> X2[Exit: back to graph]
```

**Hick / Fitts:** Graph nodes are not CTAs. One Get AG, reserved width. Admin: zero Get AG.

---

## F7 — Admin twin (J7)

Entry: signed-in `/admin`. Success: same dark graph language; project names allowed in inspect. Empty: unpaid hatch. Exit: stay in admin; never leak names to public `/`.

```mermaid
flowchart TD
  E7[Entry: /admin] --> G1[Same graph chrome as public]
  G1 --> N1[Inspect MAY name projects]
  N1 --> N2[No Get AG]
  N2 --> X1[Exit: stay admin]
  N2 --> X2[Error: do not publish names to /]
```

**Cite:** #28 §1 admin; Cos same board language.

---

## Mobile vs desktop (Jakob)

Same graph, same loop, same Get AG on public. Mobile inspect = sheet. Graph stage has reserved height (no CLS). Documented exception: desktop may show a side inspect rail (Twenty / Databricks); mobile uses a sheet.

---

## Acceptance (Check 7)

| Field | Value |
| --- | --- |
| Mermaid | F1–F7 entry / success / empty-error / exits |
| Map | F1→J1, F2→J2, F3→J3, F4→J1 mobile, F5→J6, F6→J4, F7→J7 |
| Research | #28 @ `f9f38ff` + #27 @ `235610e` + #20 @ `9721af1` |
| Next | Check 8 GO after LIVE #28 @ f9f38ff. Then phone-first: default land, live-update twitch, zoomed inspect, mobile land+inspect, admin twin |

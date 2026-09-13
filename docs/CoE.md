# Center of Excellence (operating model)

Plain-English write-up of how Agentic Governance improves the standing standard from real work.

**Cos HOLD ACCEPT / Adv `COE_README_SOT`.** README and this page must name all seven checklist items below. Soft or marketing-only CoE copy that omits them = **FAIL**.

**Status of this page.** Describes the **operating model**. It does **not** invent a new bot or persona, and it does **not** silently amend the constitution. Named locks that are still in-flight SoT stay **not live** until Cos ACCEPT merge.

---

## 1. What — framework CoE, not a delivery team

A **framework CoE**: standing standard + feedback from shipped work.

- **Not** a delivery team, not a new org-chart box, not a new sidebar persona, not a separate bot.
- The standard lives in this repo: constitution, harnesses, adversary checks, ledger.
- The feed is real work: teams ship, file triad retros, and those retros drive unpaid SoT/plans.
- Improvement is mechanical: named unpaid items with `id` / owner / metric / AC — not vibes or tips.

---

## 2. Who — Cos + AG + Adv; no new bot

No new bot. Three existing seats own the CoE loop. **Project PMs are not constitution owners.**

| Seat | Job |
|---|---|
| **Cos** | ACCEPT funnel. Only Cos ACCEPT merge makes SoT live. Does not invent policy or clear human-only vetoes. |
| **AG seat** | Framework PM for this repo. Drafts the named unpaid SoT/plan. Project PMs do **not** write AG constitution. |
| **Adv** | Challenges the plan. Does **not** author it. |

**Teams are members**, not owners of the framework write. They:

1. Ship under the **live** standard (merged Cos ACCEPT SHAs only).
2. File **triad retros** (well / didn’t / improve) into AG git as the CoE feed.
3. Absorb the next ship after Cos ACCEPT — do not run unmerged intake as law.

---

## 3. Loop

```
triad retro
    →  AG unpaid SoT/plan (id / owner / metric / AC)
    →  Adv challenge (does not author)
    →  Cos ACCEPT
    →  teams absorb
```

---

## 4. Fail-closed middle — `SELF_AUDIT_LOOP` (unpaid item or `AUDIT_CLEAR`)

`SELF_AUDIT_LOOP` is the fail-closed middle of the CoE loop: each audit cycle must produce a **named unpaid SoT/improve item** **or** explicit **`AUDIT_CLEAR`** with evidence. Nag-only digests (no unpaid item and no `AUDIT_CLEAR`) = **FAIL**.

`RETRO_BEFORE_CLOSE` sits beside it as the close-gate twin (epic CLOSED / next-pack GO requires a triad retro in AG git).

---

## 7. Not merged law yet (SoT PRs in flight)

Do **not** claim `SELF_AUDIT_LOOP` or `RETRO_BEFORE_CLOSE` are live harness/constitution law until Cos ACCEPT merge.

| Lock | Live? |
|---|---|
| `SELF_AUDIT_LOOP` | **Not live.** SoT PR in flight: [#18](https://github.com/paulthorson/agentic-governance/pull/18). |
| `RETRO_BEFORE_CLOSE` | **Not live.** SoT PR in flight with the five Adv-named locks: [#17](https://github.com/paulthorson/agentic-governance/pull/17). |

Until those merges land, teams still file retros and Cos still tracks close discipline as operating practice — but harness/constitution law for those two ids waits on Cos ACCEPT.

---

## Already LIVE (cite merged SHAs)

These Critic checks are **live** on `main`. Teams may execute them; cite the merged SHA when claiming SoT:

| Check | What | Merged |
|---|---|---|
| **Check 7** | UX→Eng gate: Mermaid `userflows.md` + `jtbd.md` + Research cite (or explicit `NO_RESEARCH` → human). Stacked on `RESEARCH_BEFORE_ENHANCE`. | [#14](https://github.com/paulthorson/agentic-governance/pull/14) @ `36deb0e` |
| **Check 8** / `VISUAL_STEP_STILLS` | Product UX visual step-stills sensor (mobile + desktop) graded at Critic. | [#15](https://github.com/paulthorson/agentic-governance/pull/15) @ `d61f4c1` |

Scope for both: product UX surfaces. **Not** OpenClaw briefs.

---

## 5. P0 — no secrets

No secrets, keys, emails, PII, absolute host paths, or private operator data in AG git. No invented tokens.

---

## 6. Soft / marketing-only = FAIL

Tips, vibes, chat-only retros, wiki scars without an unpaid item, open/draft PRs treated as live SoT, or a marketing CoE blurb missing owners / loop / fail-closed middle (`SELF_AUDIT_LOOP` unpaid-or-`AUDIT_CLEAR`) — **FAIL** under `COE_README_SOT`. Soft “we should…” language is **rejected**.

---

## See also

- README CoE section (same seven checklist items)
- [`docs/improve/`](improve/) — daily Cos/AG improve digests
- [`docs/agentic-governance-spec.md`](agentic-governance-spec.md) — ratified framework
- Triad retros under `projects/<team>/retros/`

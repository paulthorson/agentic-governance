# Center of Excellence (operating model)

Plain-English write-up of how Agentic Governance improves the standing standard from real work.

**Status of this page.** Describes the **operating model**. It does **not** invent a new bot or persona, and it does **not** silently amend the constitution. Named locks below that are still in-flight SoT stay **not live** until Cos ACCEPT merge.

---

## What a CoE is

A **standing standard** plus **feedback from shipped work** — not a new team, not a new sidebar persona, not a separate bot.

- The standard lives in this repo: constitution, harnesses, adversary checks, ledger.
- The feed is real work: teams ship, file triad retros, and those retros drive unpaid SoT/plans.
- Improvement is mechanical: named unpaid items with `id` / owner / metric / AC — not vibes, tips, or chat-only retros.

---

## Who (owners)

No new persona. Three existing seats own the CoE loop:

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

## The loop

```
triad retro
    →  AG seat drafts named unpaid SoT/plan (id / owner / metric / AC)
    →  Adv challenges (does not author)
    →  Cos ACCEPT merge
    →  teams absorb on next ship
```

Soft “we should…”, tip-only notes, wiki scars without an unpaid item, or open/draft PRs treated as live SoT — **rejected** by this operating model.

---

## Fail-closed middle (named; not live yet)

Two Adv-named locks sit in the middle of the CoE loop. **Name them. Do not claim they are merged law until Cos ACCEPT merge.**

| Lock | Role in the CoE | Live? |
|---|---|---|
| `SELF_AUDIT_LOOP` | Periodic AG self-audit that fail-closes into a named unpaid SoT/improve item (or explicit `AUDIT_CLEAR` with evidence) — not nag theater. | **Not live.** SoT PR in flight: [#18](https://github.com/paulthorson/agentic-governance/pull/18). |
| `RETRO_BEFORE_CLOSE` | Cos/CEO close gate: epic CLOSED / next-pack GO requires a triad retro in AG git. | **Not live.** SoT PR in flight with the five Adv-named locks: [#17](https://github.com/paulthorson/agentic-governance/pull/17). |

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

## P0

No secrets, keys, emails, PII, absolute host paths, or private operator data in AG git. No invented tokens.

---

## See also

- README CoE section (same owners + loop + fail-closed middle)
- [`docs/improve/`](improve/) — daily Cos/AG improve digests
- [`docs/agentic-governance-spec.md`](agentic-governance-spec.md) — ratified framework
- Triad retros under `projects/<team>/retros/`

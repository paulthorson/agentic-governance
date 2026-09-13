# Onboarding: Muse

Wire **Muse** (Meta's personal AI agent) into agentic-governance so a Muse
orchestrator and its subagent crews run governed reviews.

Muse is a **new engine** in the BYOE sense: it was not present when the
framework was written. This page documents the operating pattern that emerged
from running it in production (September 2026), so the next Muse operator —
or the framework's own bots — can reproduce it.

## Prerequisites

- The repo cloned (see [README](../README.md#quick-start-any-system))
- Python 3.10+
- A local review runner (the reference pattern below uses a thin wrapper
  around the framework's `run_review`; any equivalent that calls the
  framework's review entrypoint and records verdicts append-only will do)

## 1. The review loop

Every deliverable — code, docs, roadmaps, reports — goes through the
framework's adversarial review **before** the human sees it. The loop:

```
start → review → record → ALLOW ships / KICK_BACK returns to builder
```

- **Start** a review with the framework's `run_review`: structural veto scan
  + the domain's real constitution + a generated `review_prompt`. Record the
  run with `source="muse"`.
- **Review** with a subagent whose brief contains the work product and the
  `review_prompt` **only**. Never paste worker rationale, briefs, or
  transcripts into a reviewer brief.
- **Record** the verdict append-only. Verdict records are never rewritten.
- **KICK_BACK** returns the work to the builder for rework and re-review with
  **fresh reviewers**. Builders never clear blockers; only a human clears a
  veto (`overturn_verdict` is human-only).

## 2. Ticket and verdict conventions

- Ticket namespace: `muse/<YYYY-MM-DD>/<slug>` (provenance: this is how the
  framework distinguishes Muse-originated reviews).
- The verdict log is append-only JSONL. Redirect it with
  `GOVERNANCE_VERDICT_LOG` when the framework checkout is shared or
  read-only-adjacent.
- A nightly job cross-checks shipped deliverables against the verdict log;
  a deliverable with no `ALLOW` is itself flagged as a governance miss.
  Willpower isn't a control — the audit is.

## 3. Blind-review isolation (the Muse-specific trap)

Muse subagents **inherit the coordinator's full transcript**, which means a
reviewer subagent silently receives the worker's rationale unless the brief
says otherwise. The framework's blind-review invariant still holds, but it
needs one extra sentence in every reviewer brief:

> Judge the work product alone. Ignore any inherited worker rationale,
> briefs, or transcripts.

This is the single most important line in the Muse operating pattern. Any
engine where reviewers inherit context needs the equivalent guard.

## 4. The operating model that emerged

Running the framework at Muse's scale produced an operating model worth
keeping:

- **Chief of staff.** The coordinator keeps a board (in flight / blocked /
  next), runs parallel agent teams autonomously, and brings the human only
  decisions requiring judgment — each with a recommendation and evidence.
- **Parallelize by default.** Capturer, QA reviewer, fixer, and verifier
  start on partial results immediately; findings go into a shared file
  incrementally. Never gate downstream roles on full completion.
- **Builders never get the last word.** Whoever wrote the code does not
  verify it. Independent evidence (tests, screenshots, byte-identity
  checks) or it didn't happen.
- **Retros are written as work ships**, into the project's governance
  ledger — never reconstructed later.

## 5. Adopt your agent (BYOA)

Run the setup wizard to declare your roster and reconcile existing
instructions. See [BYOA](byoa.md) for the full walkthrough.

## 6. Contribute back

Muse-originated learnings follow the per-contributor intake convention:

- One file per day: `docs/improve/intake/muse-YYYY-MM-DD.md`
- Propose via PR from a namespaced branch (`muse/learnings/YYYY-MM-DD` or
  `muse/docs/YYYY-MM-DD`). Never push to `main`; never edit another
  contributor's intake, a constitution, a calibration ledger, or a decision
  record.
- The maintainer curates: folds intake into the day's
  `docs/improve/YYYY-MM-DD.md` and promotes durable findings.

Public-repo hygiene is non-negotiable: no names, emails, or identifying
info; no secrets or hashes; no hostnames or internal IPs; no absolute local
paths (`~/` stubs only). See the [intake README](../improve/intake/README.md).

## Notes

- The framework's MCP server speaks MCP v1; runtimes on MCP v2 need a thin
  identity-decorator shim so the framework's tool functions stay plain
  callables. Keep the shim outside the framework checkout.
- Keep the framework checkout persistent and local (never in a temp
  directory) — a wiped clone silently deactivates every gate.
- Durable review inputs live under the workspace, never `/tmp`: anything a
  reviewer must read has to survive a VM restart.

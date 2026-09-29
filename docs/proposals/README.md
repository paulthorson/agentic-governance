# Proposals — the governance-change workflow (A24)

This directory holds proposals for changes to the governance framework. It is
the formal home of the **exception path** (A24): bots cannot write the
governance repo (Section 9.4 read-only), so for governance-repo work the
engineer produces the diff and a **human applies it**.

## The workflow

1. **Propose.** A governance change is written as a proposal in this directory
   (`docs/proposals/<topic>.md`). The proposal states the problem, the options,
   and a recommendation.
2. **Review.** The proposal is reviewed — by the relevant adversary agent(s)
   and by the operator (a human).
3. **Decide.** The operator approves or rejects. An approved decision is
   recorded in `docs/spec-addendum-01.md` as a numbered section (A20, A21, .).
4. **Apply.** A human applies the change to the governance repo. The engineer
   produces the diff; the human applies it. Bots never write the governance
   repo directly.

## Current proposals

| File | Subject | Status |
|---|---|---|
| `a9-ledger-structure.md` | Calibration ledger structure + growth | DECIDED (A21) |
| `a10-rollback.md` | Rollback / overturning precedent | DECIDED (A22) |
| `a16-harness-duplication.md` | Harness single source of truth | DECIDED (A23) |
| `a17-project-repo.md` | Governance-repo work exception path | DECIDED (A24) |
| `a20-validation-record-home.md` | Where validation records live | DECIDED (A20) |

## Why this exists

The governance repo is read-only to bots (Section 9.4), but the engineer is
obligated to produce applied implementations (Section 5.3). The exception path
resolves this: the engineer produces the diff, the human applies it. This
keeps the governance repo read-only to bots and keeps the human gate explicit —
consistent with the framework's philosophy that humans clear vetoes and apply
governance changes.

## Naming

Proposals are named `<a-number>-<topic>.md` where the number is the addendum
section the decision will occupy (or the open problem it addresses). A proposal
that is not yet assigned a number uses a descriptive topic name.

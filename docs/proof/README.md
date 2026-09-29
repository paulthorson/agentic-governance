# Agentic Governance — Proof

Real analytics and learnings from production multi-agent builds run under the
[Agentic Governance framework](https://github.com/paulthorson/agentic-governance).
This repo exists so the framework's marketing site can cite hard numbers, not claims.

## Who reads this

- The AG marketing-website team pulls proof points from `analytics/` and `learnings/`.
- Build coordinators publish here as initiatives ship (see `initiatives/README.md`).

## Layout

- `analytics/` — evergreen numbers: review verdicts, velocity, quality. This file is
  always current; update it in place, keeping superseded versions in `archive/`.
- `learnings/` — dated operating principles discovered during real runs. Each file: what happened, what we learned, what changed.
- `initiatives/` — one folder per shipped initiative with its evidence: scope, verdicts, metrics, timeline.

## Contribution contract

1. Every number here traces to a real run: a verdict log, a test suite, a commit.
2. `analytics/` is evergreen — update it in place; move the superseded version to
   `archive/`. `learnings/` and `initiatives/` are append-only: new dated files,
   history stays.
3. Public-repo hygiene is non-negotiable: no names (beyond public handles), emails,
   credentials, tokens, hashes, internal hosts/IPs, or absolute local paths (`~/` stubs only).
   Grep every file for secrets and PII before pushing.

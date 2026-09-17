# ADR-0007: Abstract the Watchdog Data Source

- **Status:** Accepted
- **Date:** 2026-09-06

## Context

The first real-team adoption (first adopting team / first product-seat adopter, ADR-0006) exposed that the
stuck-review-watchdog was **Paperclip-native**: it shelled out to
`paperclipai issue list --status in_review --json`, read `~/.paperclip/instances/`
for the company id, and held the framework host's adversary IDs. The first adopting team does not
use Paperclip (work lives in GitHub PRs + epic markdown; no `in_review` ticket
store), so the watchdog could not drop in as-is.

The framework's *logic* (staleness, dedupe, alerting) is portable — only the
*data source* was coupled. The framework is meant to be vanilla-handoffable to
any team in any environment, so the data source must be abstracted.

## Decision

Make the watchdog **data-source-agnostic**. It reads a list of `in_review`
issues and applies the same staleness/dedupe/alert logic regardless of where
the issues come from. Two sources are built in:

- **`--source paperclip` (default)** — the existing adapter. Shells out to
  `paperclipai issue list --status in_review --json`. This is the framework host's default.
- **`--source file --issues-file <path>`** — reads a JSON file (or stdin with
  `-`) containing a list of issue dicts. Any team's store (GitHub PR review
  state, a file ledger in the epic folder, Linear, Jira) can be adapted by
  emitting the expected shape:
  `[{"identifier", "title", "assigneeAgentId", "lastActivityAt"|"updatedAt"}]`.

The `collect_stuck` logic is unchanged — it already operates on a generic list
of issue dicts. The abstraction is a single `load_issues(args)` dispatcher that
returns `(issues, error)` from the configured source.

## Consequences

- **Positive:** the watchdog is now vanilla-handoffable. A non-Paperclip team
  (like the first adopting team) can feed it from its own store via a JSON file or stdin,
  without forking the script. Paperclip remains the default for the framework host.
- **Positive:** backward-compatible — the default `--source paperclip` behavior
  is byte-for-byte unchanged.
- **Negative:** a team using a live store (not a file) still needs a small shim
  to emit the issue shape; the framework does not ship per-store adapters beyond
  Paperclip and file.

## Alternatives considered

- **Keep Paperclip as the only source, document the interface** — rejected: the
  watchdog still could not run for non-Paperclip teams without forking.
- **Ship adapters for every store (GitHub, Linear, Jira)** — rejected: too much
  surface to maintain; the file/stdin interface lets each team adapt its own
  store with a trivial shim.

## See also

- [[ADR-0006]] · [[Architecture]] · [[Calibration]] · [[Roadmap]]

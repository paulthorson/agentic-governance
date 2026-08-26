# ADR-0003: MCP Server for the Review Loop

- **Status:** Accepted
- **Date:** 2026-08-26

## Context

The review loop lives in the framework files. Any agent (Claude, Cursor,
OpenClaw) that wants to run a review must re-read the framework. An MCP server
exposes the loop as callable tools.

## Decision

Build a Python MCP server (`mcp/`) exposing the review loop as tools:
`run_review`, `check_veto`, `record_verdict`, `query_verdicts`, inventory
tools, and `framework_status`. Pin `mcp<2` (v1 FastMCP API). Verdicts append
to `runs/verdicts.jsonl` (gitignored).

## Consequences

- **Positive:** Any agent can run a governed review without re-reading the
  framework. Deterministic first pass (veto scan) + prompt assembly for the
  adversary agents.
- **Negative:** The structural scan is keyword-based; deep review (invoking
  the LLM) is a future enhancement.

## Alternatives considered

- **No MCP, agents read files directly** — rejected: less ergonomic, no
  shared verdict record.

## References

- `mcp/`
- `docs/MCP.md`

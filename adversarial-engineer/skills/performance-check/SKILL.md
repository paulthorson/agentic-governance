---
name: performance-check
description: Stateless skill. Checks a change for performance and latency risk — hot paths, unbounded work, blocking calls, resource leaks. Returns performance findings with severity.
---

# Performance Check

Check a change for performance and latency risk. This is the shared check that
any reviewer can run — not just the engineer-critic.

## What to look for

1. **Hot paths** — work done in a loop, per-request, or per-render that should
   be hoisted or cached.
2. **Unbounded work** — queries, loops, or allocations that grow with input
   size without a bound.
3. **Blocking calls** — synchronous I/O, network, or disk on a hot path.
4. **Resource leaks** — connections, handles, or memory not released.
5. **Latency regressions** — a change that adds measurable latency to a
   user-facing path.

## Method

1. Read the change in full.
2. Identify hot paths and per-request work.
3. Check for unbounded work, blocking calls, and resource leaks.
4. Estimate the latency impact on user-facing paths.

## Output

```
## Performance findings
- <the issue> | Path: <where it occurs> | Severity: BLOCKER/CONCERN/NOTE
  What would clear it: <the specific fix>
```

A BLOCKER performance finding (e.g. a hot path that will time out or exhaust
resources) is a veto: only a human clears it.

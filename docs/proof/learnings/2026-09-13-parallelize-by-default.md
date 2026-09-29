# Learning 2026-09-13 — Parallelize by default

## What happened

A screenshot-capture pipeline sat idle for 15+ minutes: 9 screenshots were on disk
while the QA reviewer "waited" for the capture phase to finish. The human caught it.

## Learning

When a producer emits artifacts incrementally, the consumer starts on partial
results immediately. Findings go into a shared file incrementally so fixers can
start on confirmed defects mid-capture. Never gate a downstream role on full
completion of an upstream role.

## What changed

Binding operating default: roles are defined capturer → QA reviewer → fixer →
verifier, each starting as soon as its input exists. A backgrounded `exec` watch
loop only delivers its terminal result at completion, so incremental consumption
uses chunked watch cycles (sleep 120–180s, list, print, exit) and re-arms —
never one long loop.

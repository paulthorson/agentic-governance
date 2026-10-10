#!/usr/bin/env python3
"""
Append-only event log for the agentic-governance framework (ADR-0009).

Every governed action (ticket created, verdict recorded, ticket closed, veto
cleared, ruling overturned) appends one JSON line to ``runs/events.jsonl``
using a single, versioned envelope. The envelope is a public contract:
dashboards, exporters, and adapters are expected to build on it. See
``scripts/events.schema.md`` for the field reference.

Design constraints:

- **Standard library only.** No new dependencies in the base install.
- **Cross-platform locking.** ``fcntl`` is Unix-only, so the lock is a
  sibling ``<file>.lock`` created with ``O_CREAT | O_EXCL``. That works on
  Linux, macOS, and Windows. A lock older than ``STALE_LOCK_SECONDS`` is
  treated as abandoned by a crashed writer and broken.
- **No subprocess, no network.** The harness git SHA is read from ``.git``
  files directly, so this module never hits an approval-gated call site.
- **Fail loudly on unknown schema.** ``read_events`` raises
  ``UnknownSchemaVersion`` on a record whose ``schema_version`` it does not
  recognize, so a consumer never silently mis-parses a newer log.

What this module does NOT do: it does not stop an agent from writing to the
log file directly, and it does not authenticate ``agent_id``. Those fields
are self-reported by the caller.

Config (env):
  EVENT_LOG             path to the event log (default: runs/events.jsonl)
  AG_LOCK_TIMEOUT       seconds to wait for a lock (default: 10)
  AG_HARNESS_SHA        override the harness SHA (default: read from .git)
  AG_CONSTITUTION_VERSION  optional constitution version label
  AG_AGENT_ID           default agent_id when the caller passes none
"""
from __future__ import annotations

import contextlib
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

SCHEMA_VERSION = "1"
SUPPORTED_SCHEMA_VERSIONS = {"1"}

REPO_ROOT = Path(os.environ.get("ADVERSARIAL_ROOT", Path(__file__).resolve().parent.parent))
EVENT_LOG = Path(os.environ.get("EVENT_LOG", REPO_ROOT / "runs" / "events.jsonl"))

STALE_LOCK_SECONDS = 30.0
_POLL_SECONDS = 0.05

# Envelope fields, in stable order. Optional fields are always present and
# null when unknown, so consumers can rely on the key set.
ENVELOPE_FIELDS = (
    "schema_version",
    "event_id",
    "ts",
    "ts_iso",
    "kind",
    "trace_id",
    "ticket",
    "role",
    "agent_id",
    "harness_sha",
    "constitution_version",
    "model",
    "tokens_in",
    "tokens_out",
    "framework_units",
    "duration_ms",
    "outcome",
    "data",
)


class LockTimeout(RuntimeError):
    """Raised when a file lock cannot be acquired within the timeout."""


class UnknownSchemaVersion(ValueError):
    """Raised when a record carries a schema_version this reader does not know."""


# ---------------------------------------------------------------------------
# Locking
# ---------------------------------------------------------------------------


def _lock_timeout() -> float:
    try:
        return float(os.environ.get("AG_LOCK_TIMEOUT", "10"))
    except ValueError:
        return 10.0


@contextlib.contextmanager
def file_lock(target: Path, timeout: float | None = None) -> Iterator[None]:
    """Hold an exclusive lock on ``target`` for the duration of the block.

    The lock is a sibling file ``<target>.lock`` created atomically with
    ``O_CREAT | O_EXCL``. Every writer in this framework that touches a
    shared ledger takes this lock first, so two agents cannot interleave a
    read-modify-write and lose an update.
    """
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    lock_path = target.with_name(target.name + ".lock")
    wait = _lock_timeout() if timeout is None else timeout
    deadline = time.monotonic() + wait
    fd = None
    while fd is None:
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            try:
                age = time.time() - lock_path.stat().st_mtime
            except FileNotFoundError:
                continue  # released between our open and stat; retry now
            if age > STALE_LOCK_SECONDS:
                print(
                    f"WARN: breaking stale lock {lock_path} (age {age:.0f}s)",
                    file=sys.stderr,
                )
                with contextlib.suppress(FileNotFoundError):
                    lock_path.unlink()
                continue
            if time.monotonic() >= deadline:
                raise LockTimeout(f"Could not lock {target} within {wait}s ({lock_path} held)")
            time.sleep(_POLL_SECONDS)
    try:
        os.write(fd, f"{os.getpid()} {time.time():.3f}\n".encode("ascii"))
        os.close(fd)
        yield
    finally:
        with contextlib.suppress(FileNotFoundError):
            lock_path.unlink()


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    """Append one JSON line to ``path`` under its lock."""
    path = Path(path)
    with file_lock(path):
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")


# ---------------------------------------------------------------------------
# Envelope
# ---------------------------------------------------------------------------


def _git_head_sha(root: Path) -> str | None:
    """Read the checked-out commit SHA from .git without a subprocess."""
    git = root / ".git"
    try:
        if git.is_file():  # worktree / submodule: "gitdir: <path>"
            line = git.read_text(encoding="utf-8").strip()
            if line.startswith("gitdir:"):
                git = (root / line.split(":", 1)[1].strip()).resolve()
        head = (git / "HEAD").read_text(encoding="utf-8").strip()
        if not head.startswith("ref:"):
            return head or None
        ref = head.split(":", 1)[1].strip()
        ref_file = git / ref
        if ref_file.exists():
            return ref_file.read_text(encoding="utf-8").strip() or None
        packed = git / "packed-refs"
        if packed.exists():
            for line in packed.read_text(encoding="utf-8").splitlines():
                parts = line.split()
                if len(parts) == 2 and parts[1] == ref:
                    return parts[0]
    except OSError:
        return None
    return None


def harness_sha() -> str | None:
    return os.environ.get("AG_HARNESS_SHA") or _git_head_sha(REPO_ROOT)


def make_event(
    kind: str,
    *,
    ticket: str | None = None,
    trace_id: str | None = None,
    role: str | None = None,
    agent_id: str | None = None,
    model: str | None = None,
    tokens_in: int | None = None,
    tokens_out: int | None = None,
    framework_units: float | None = None,
    duration_ms: int | None = None,
    outcome: str | None = None,
    data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an envelope. ``trace_id`` defaults to the ticket id, so every
    event for one ticket shares a trace without the caller tracking it."""
    if not kind:
        raise ValueError("event kind is required")
    now = time.time()
    event_id = uuid.uuid4().hex
    ev = {
        "schema_version": SCHEMA_VERSION,
        "event_id": event_id,
        "ts": int(now * 1000),
        "ts_iso": datetime.fromtimestamp(now, timezone.utc).isoformat(),
        "kind": kind,
        "trace_id": trace_id or ticket or event_id,
        "ticket": ticket,
        "role": role,
        "agent_id": agent_id or os.environ.get("AG_AGENT_ID") or None,
        "harness_sha": harness_sha(),
        "constitution_version": os.environ.get("AG_CONSTITUTION_VERSION") or None,
        "model": model,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "framework_units": framework_units,
        "duration_ms": duration_ms,
        "outcome": outcome,
        "data": data or {},
    }
    return {k: ev[k] for k in ENVELOPE_FIELDS}


def emit(kind: str, path: Path | None = None, **fields: Any) -> dict[str, Any]:
    """Build an envelope and append it to the event log. Returns the event."""
    ev = make_event(kind, **fields)
    append_jsonl(Path(path) if path else EVENT_LOG, ev)
    return ev


def read_events(path: Path | None = None, *, strict: bool = True) -> list[dict[str, Any]]:
    """Read the event log. Malformed lines are skipped with a stderr warning.

    With ``strict=True`` (default), a record with an unrecognized
    ``schema_version`` raises ``UnknownSchemaVersion``.
    """
    p = Path(path) if path else EVENT_LOG
    if not p.exists():
        return []
    out: list[dict[str, Any]] = []
    for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            print(f"WARN: {p}:{n} is not valid JSON; skipped", file=sys.stderr)
            continue
        ver = str(rec.get("schema_version", ""))
        if ver not in SUPPORTED_SCHEMA_VERSIONS:
            if strict:
                raise UnknownSchemaVersion(
                    f"{p}:{n} has schema_version {ver!r}; this reader supports "
                    f"{sorted(SUPPORTED_SCHEMA_VERSIONS)}"
                )
            continue
        out.append(rec)
    return out

#!/usr/bin/env python3
"""
Tamper detection for the ticket store and event log (ADR-0012).

Three pieces:

1. **Hash-chained event log.** Every event carries ``prev_hash`` and ``hash``.
   ``hash = H(prev_hash + canonical(event))``. H is HMAC-SHA256 with the
   operator's integrity key when one is configured, plain SHA-256 otherwise.
   Editing, inserting, or deleting a line breaks the chain from that point.

2. **Signed head record** (next to the ticket store, e.g.
   ``runs/in_review.integrity.json``). After every ticket
   transaction the store writes: the byte offset of the event log, the hash
   of the event ending there, and the SHA-256 of the ticket file. With a key,
   the record carries a MAC. This catches what a chain alone cannot:
   truncating the newest events, and editing the ticket file directly.

3. **Crash recovery.** Ticket writes go: temp file, events (carrying the new
   ``state_digest``), replace, head. A crash at any step leaves a state the
   next load can roll forward from the log. Anything else is tampering.

Honest limits (also in docs/deployment-hardened.md):
  - Without an integrity key, anyone who can write the files can also
    recompute SHA-256 hashes. Unkeyed mode catches hand edits and broken
    tools, not a deliberate forger.
  - With a key, a forger needs the key. If agents run as the same OS user
    as the framework, they can read it. Real prevention needs the framework
    to run as a separate user that agents reach only through MCP.

Config (env):
  AG_INTEGRITY_KEY        key material (string). Overrides the key file.
  AG_INTEGRITY_KEY_FILE   key path (default: config/integrity.key)
  AG_INTEGRITY_HEAD       head record path (default: <ticket file stem>.integrity.json)
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
from pathlib import Path
from typing import Any

REPO_ROOT = Path(os.environ.get("ADVERSARIAL_ROOT", Path(__file__).resolve().parent.parent))
GENESIS = "0" * 64
CHAIN_FIELDS = ("prev_hash", "hash", "hash_alg")


class TamperDetected(RuntimeError):
    """The store or log no longer matches what the framework last wrote."""


# ---------------------------------------------------------------------------
# Key
# ---------------------------------------------------------------------------


def key_path() -> Path:
    return Path(os.environ.get("AG_INTEGRITY_KEY_FILE", REPO_ROOT / "config" / "integrity.key"))


def load_key() -> bytes | None:
    env = os.environ.get("AG_INTEGRITY_KEY")
    if env:
        return env.encode("utf-8")
    p = key_path()
    try:
        raw = p.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    return raw.encode("utf-8") if raw else None


def create_key() -> Path:
    """Write a new random key with 0600 permissions. Refuses to overwrite."""
    p = key_path()
    if p.exists():
        raise FileExistsError(f"{p} already exists; rotating a key invalidates the chain, so move it aside yourself")
    p.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(str(p), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(secrets.token_hex(32) + "\n")
    return p


# ---------------------------------------------------------------------------
# Hashing
# ---------------------------------------------------------------------------


def canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _mac(data: bytes, key: bytes | None) -> tuple[str, str]:
    if key:
        return hmac.new(key, data, hashlib.sha256).hexdigest(), "hmac-sha256"
    return hashlib.sha256(data).hexdigest(), "sha256"


def chain_event(ev: dict, prev_hash: str, key: bytes | None) -> dict:
    """Return ``ev`` with prev_hash, hash_alg, and hash filled in."""
    body = {k: v for k, v in ev.items() if k != "hash"}
    body["prev_hash"] = prev_hash
    body["hash_alg"] = "hmac-sha256" if key else "sha256"
    h, _ = _mac(prev_hash.encode("ascii") + canonical(body), key)
    out = dict(ev)
    out.update(prev_hash=prev_hash, hash_alg=body["hash_alg"], hash=h)
    return out


def recompute(ev: dict, key: bytes | None) -> str | None:
    """The hash this event should carry, or None if it cannot be checked
    (keyed event, no key available)."""
    if ev.get("hash_alg") == "hmac-sha256" and not key:
        return None
    use_key = key if ev.get("hash_alg") == "hmac-sha256" else None
    body = {k: v for k, v in ev.items() if k != "hash"}
    h, _ = _mac(str(ev.get("prev_hash", "")).encode("ascii") + canonical(body), use_key)
    return h


def file_digest(path: Path) -> str:
    try:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    except FileNotFoundError:
        return "absent"


# ---------------------------------------------------------------------------
# Log tail
# ---------------------------------------------------------------------------


def line_ending_at(path: Path, offset: int) -> str | None:
    """The complete line whose trailing newline sits at ``offset - 1``."""
    if offset <= 0:
        return None
    with open(path, "rb") as fh:
        size = fh.seek(0, os.SEEK_END)
        if offset > size:
            return None
        window = 65536
        while True:
            start = max(0, offset - window)
            fh.seek(start)
            chunk = fh.read(offset - start)
            if not chunk.endswith(b"\n"):
                return None
            body = chunk[:-1]
            nl = body.rfind(b"\n")
            if nl >= 0 or start == 0:
                return body[nl + 1:].decode("utf-8", "replace")
            window *= 4


def last_hash(path: Path) -> str:
    """Hash of the newest chained event, or GENESIS for an empty/unchained log."""
    try:
        size = os.path.getsize(path)
    except OSError:
        return GENESIS
    line = line_ending_at(path, size)
    if not line:
        return GENESIS
    try:
        return json.loads(line).get("hash") or GENESIS
    except json.JSONDecodeError:
        return GENESIS


# ---------------------------------------------------------------------------
# Head record
# ---------------------------------------------------------------------------


def head_path() -> Path:
    return Path(os.environ.get("AG_INTEGRITY_HEAD", REPO_ROOT / "runs" / "integrity.json"))


def read_head(path: Path | None = None, key: bytes | None = None) -> dict | None:
    p = Path(path) if path else head_path()
    if not p.exists():
        return None
    try:
        rec = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        raise TamperDetected(f"{p} is unreadable")
    body = {k: v for k, v in rec.items() if k != "mac"}
    use_key = key if rec.get("mac_alg") == "hmac-sha256" else None
    if rec.get("mac_alg") == "hmac-sha256" and not key:
        raise TamperDetected(f"{p} is keyed but no integrity key is configured")
    if key and rec.get("mac_alg") != "hmac-sha256":
        raise TamperDetected(f"{p} is unkeyed but an integrity key is configured (downgrade?)")
    expect, _ = _mac(canonical(body), use_key)
    if not hmac.compare_digest(expect, str(rec.get("mac", ""))):
        raise TamperDetected(f"{p} signature does not match")
    return rec


def write_head(log_offset: int, log_head: str, store_digest: str,
               path: Path | None = None, key: bytes | None = None,
               accepted_problems: list[str] | None = None) -> None:
    """``accepted_problems``: historical chain problems an operator reviewed
    and accepted; ``verify`` reports them as accepted instead of failing."""
    p = Path(path) if path else head_path()
    body = {"version": 1, "log_offset": log_offset, "log_head": log_head,
            "store_digest": store_digest, "mac_alg": "hmac-sha256" if key else "sha256",
            "accepted_problems": sorted(set(accepted_problems or []))}
    mac, _ = _mac(canonical(body), key)
    body["mac"] = mac
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(body, indent=2), encoding="utf-8")
    os.replace(tmp, p)


# ---------------------------------------------------------------------------
# Full verification
# ---------------------------------------------------------------------------


def verify_log(path: Path, key: bytes | None) -> dict:
    """Walk the whole log. Returns {"ok", "events", "chained", "unverifiable",
    "problems": [...]}. Leading pre-chain (pre-1.2) events are allowed."""
    problems: list[str] = []
    n = chained = unverifiable = 0
    prev = None
    started = False
    keyed_seen = False
    p = Path(path)
    if not p.exists():
        return {"ok": True, "events": 0, "chained": 0, "unverifiable": 0, "problems": []}
    with open(p, "rb") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.decode("utf-8", "replace").strip()
            if not line:
                continue
            n += 1
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                problems.append(f"line {lineno}: not valid JSON")
                continue
            if "hash" not in ev:
                if started:
                    problems.append(f"line {lineno}: unchained event after the chain began")
                continue
            if not started:
                started = True
                if ev.get("prev_hash") != GENESIS:
                    problems.append(f"line {lineno}: first chained event does not start at genesis")
            elif ev.get("prev_hash") != prev:
                problems.append(f"line {lineno}: prev_hash does not match line before (deleted or reordered events)")
            if ev.get("hash_alg") == "hmac-sha256":
                keyed_seen = True
            elif keyed_seen:
                problems.append(f"line {lineno}: unkeyed event after the keyed chain began (downgrade)")
            expect = recompute(ev, key)
            if expect is None:
                unverifiable += 1
            elif not hmac.compare_digest(expect, ev["hash"]):
                problems.append(f"line {lineno}: hash mismatch (event edited)")
            chained += 1
            prev = ev["hash"]
    return {"ok": not problems, "events": n, "chained": chained,
            "unverifiable": unverifiable, "problems": problems}

#!/usr/bin/env python3
"""
Tamper detection for the ticket store and event log (ADR-0012).

Three pieces:

1. **Hash-chained event log.** Every event carries ``prev_hash`` and ``hash``.
   ``hash = H(prev_hash + canonical(event))``. H is HMAC-SHA256 with the
   operator's integrity key when one is configured, plain SHA-256 otherwise.
   Editing, inserting, or deleting a line breaks the chain from that point.

2. **Signed head record**, kept in the key's directory (``config/``), NOT
   in ``runs/``. After every ticket transaction the store writes: the byte
   offset of the event log, the hash of the event ending there, the SHA-256
   of the ticket file, and whether agent identity was enforced. With a key,
   the record carries a MAC. Keeping it out of ``runs/`` means someone who
   can write ``runs/`` but not ``config/`` cannot delete it or roll it back
   to an older signed copy together with older ticket and log files.

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
  AG_INTEGRITY_HEAD       head record path (default: config/<store>-<hash>.integrity.json,
                          next to the key file)
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


class KeyRequired(RuntimeError):
    """A keyed log cannot be extended by a process that has no key."""


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


def repair_torn_tail(path: Path) -> int:
    """If the log does not end in a newline (a crash or a full disk cut an
    append short), move the fragment to ``<log>.torn`` and truncate it away.
    The fragment was never committed: no reader accepts a line without its
    newline. Returns the fragment length. Caller holds the log lock."""
    p = Path(path)
    try:
        size = p.stat().st_size
    except FileNotFoundError:
        return 0
    if size == 0:
        return 0
    with open(p, "rb+") as fh:
        fh.seek(size - 1)
        if fh.read(1) == b"\n":
            return 0
        window = min(size, 1 << 20)
        fh.seek(size - window)
        chunk = fh.read(window)
        nl = chunk.rfind(b"\n")
        cut = (size - window + nl + 1) if nl >= 0 else 0
        fh.seek(cut)
        fragment = fh.read()
        with open(str(p) + ".torn", "ab") as torn:
            torn.write(fragment + b"\n")
        fh.truncate(cut)
    return len(fragment)


def last_event(path: Path) -> dict | None:
    """Newest complete event line, or None for an empty log."""
    try:
        size = os.path.getsize(path)
    except OSError:
        return None
    line = line_ending_at(path, size)
    if not line:
        return None
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        return {"_bad": True}


def last_hash(path: Path) -> str:
    """Hash of the newest chained event, or GENESIS for an empty/unchained log."""
    ev = last_event(path)
    return (ev or {}).get("hash") or GENESIS


def log_has_committed_state(path: Path) -> bool:
    """True if any complete line in the log is a chained event carrying a
    ticket ``state_digest``. Scans the whole file: a junk line at the end
    must not make a committed log look fresh."""
    p = Path(path)
    if not p.exists():
        return False
    with open(p, "rb") as fh:
        for raw in fh:
            if not raw.endswith(b"\n") or b'"state_digest"' not in raw:
                continue
            try:
                ev = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if ev.get("hash") and (ev.get("data") or {}).get("state_digest"):
                return True
    return False


# ---------------------------------------------------------------------------
# Head record
# ---------------------------------------------------------------------------


def head_path(ticket_file: Path | None = None) -> Path:
    """Head record for a ticket store. Lives beside the key (``config/``) so
    it does not share a directory, and its permissions, with ``runs/``."""
    env = os.environ.get("AG_INTEGRITY_HEAD")
    if env:
        return Path(env)
    if ticket_file is None:
        return key_path().parent / "integrity.json"
    tf = Path(ticket_file).resolve()
    tag = hashlib.sha256(str(tf).encode("utf-8")).hexdigest()[:10]
    return key_path().parent / f"{tf.stem}-{tag}.integrity.json"


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
               accepted_problems: list[str] | None = None,
               identity_enforced: bool = False) -> None:
    """``accepted_problems``: historical chain problems an operator reviewed
    and accepted; ``verify`` reports them as accepted instead of failing."""
    p = Path(path) if path else head_path()
    body = {"version": 1, "log_offset": log_offset, "log_head": log_head,
            "store_digest": store_digest, "mac_alg": "hmac-sha256" if key else "sha256",
            "accepted_problems": sorted(set(accepted_problems or [])),
            "identity_enforced": bool(identity_enforced)}
    mac, _ = _mac(canonical(body), key)
    body["mac"] = mac
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(body, indent=2), encoding="utf-8")
    try:
        os.chmod(tmp, 0o600)
    except OSError:
        pass
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
    notes: list[str] = []
    with open(p, "rb") as fh:
        for lineno, raw in enumerate(fh, 1):
            if not raw.endswith(b"\n"):
                notes.append(f"line {lineno}: unterminated final line (torn write; moved aside on next append)")
                continue
            line = raw.decode("utf-8", "replace").strip()
            if not line:
                continue
            n += 1
            # Problems name the line AND a digest of its bytes, so accepting
            # one problem never covers a later edit to the same line.
            tag = hashlib.sha256(raw).hexdigest()[:16]
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                problems.append(f"line {lineno} [{tag}]: not valid JSON")
                continue
            if "hash" not in ev:
                if started:
                    problems.append(f"line {lineno} [{tag}]: unchained event after the chain began")
                continue
            if not started:
                started = True
                if ev.get("prev_hash") != GENESIS:
                    problems.append(f"line {lineno} [{tag}]: first chained event does not start at genesis")
            elif ev.get("prev_hash") != prev:
                problems.append(f"line {lineno} [{tag}]: prev_hash does not match line before (deleted or reordered events)")
            if ev.get("hash_alg") == "hmac-sha256":
                keyed_seen = True
            elif keyed_seen:
                problems.append(f"line {lineno} [{tag}]: unkeyed event after the keyed chain began (downgrade)")
            expect = recompute(ev, key)
            if expect is None:
                unverifiable += 1
            elif not hmac.compare_digest(expect, ev["hash"]):
                problems.append(f"line {lineno} [{tag}]: hash mismatch (event edited)")
            chained += 1
            prev = ev["hash"]
    return {"ok": not problems, "events": n, "chained": chained,
            "unverifiable": unverifiable, "problems": problems, "notes": notes}


def unaccepted(problems: list[str], accepted: list[str] | None) -> list[str]:
    acc = set(accepted or [])
    return [p for p in problems if p not in acc]

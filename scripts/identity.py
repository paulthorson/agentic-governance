#!/usr/bin/env python3
"""
Agent registry: verified agent identity for the chain (ADR-0011).

Without a registry, ``agent_id`` is whatever the caller says. With one, every
claim, heartbeat, submit, and verdict must present a token the operator
issued, and the framework derives the agent id from the token.

Registry file: ``config/agents.json`` (``config/`` is gitignored). Each entry:

    {
      "agent_id":   "eng-1",
      "team":       "team-a",
      "roles":      ["engineer", "review:qa"],   # "X" = work stage X, "review:X" = review stage X
      "principal":  "runtime-claude-1",          # who runs it; reviewer and worker must differ
      "token_sha256": "<hex>",                   # the token itself is never stored
      "created_at": "...", "revoked_at": null
    }

Tokens are 256-bit random values from ``secrets``, so a plain SHA-256 is a
safe stored form. Lookup compares digests with ``hmac.compare_digest``.

Enforcement rule: if the registry file exists and holds at least one active
agent, identity is REQUIRED for agent actions. Remove or empty the registry
to return to self-reported ids.

What this does NOT do: it does not stop an agent that can read another
agent's token (same OS user, shared env) from using it. Token secrecy is the
operator's job; see docs/deployment-hardened.md.

Config (env):
  AG_AGENT_REGISTRY   registry path (default: config/agents.json)
  AG_AGENT_TOKEN      the calling agent's token (CLI and MCP fallback)
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import secrets
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import events  # noqa: E402

REPO_ROOT = Path(os.environ.get("ADVERSARIAL_ROOT", Path(__file__).resolve().parent.parent))
_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")


class IdentityError(PermissionError):
    """The caller could not be identified or is not allowed to do this."""


@dataclass(frozen=True)
class Agent:
    agent_id: str
    team: str
    roles: tuple[str, ...]
    principal: str

    def may_work(self, stage: str) -> bool:
        return stage in self.roles

    def may_review(self, stage: str) -> bool:
        return f"review:{stage}" in self.roles


def registry_path() -> Path:
    return Path(os.environ.get("AG_AGENT_REGISTRY", REPO_ROOT / "config" / "agents.json"))


def _digest(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


class Registry:
    def __init__(self, path: Path | None = None):
        self.path = Path(path) if path else registry_path()

    # -- storage ------------------------------------------------------------

    def _load(self) -> list[dict]:
        if not self.path.exists():
            return []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            # A broken registry must not silently fall back to self-reported ids.
            raise IdentityError(f"Agent registry {self.path} is unreadable ({e}). Refusing agent actions.")
        if not isinstance(data, list):
            raise IdentityError(f"Agent registry {self.path} is not a JSON list. Refusing agent actions.")
        return data

    def _save(self, rows: list[dict]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_name(self.path.name + ".tmp")
        tmp.write_text(json.dumps(rows, indent=2), encoding="utf-8")
        try:
            os.chmod(tmp, 0o600)
        except OSError:
            pass
        os.replace(tmp, self.path)

    def active(self) -> list[dict]:
        return [r for r in self._load() if not r.get("revoked_at")]

    def enforced(self) -> bool:
        """Identity is required once any active agent is registered."""
        return bool(self.active())

    # -- admin (callers gate these behind operator approval) ---------------

    def add(self, agent_id: str, team: str, roles: list[str], principal: str) -> str:
        if not _ID_RE.match(agent_id or ""):
            raise ValueError("agent_id must be 1-64 chars: letters, digits, . _ -")
        roles = [r.strip() for r in roles if r.strip()]
        if not roles:
            raise ValueError("at least one role is required (e.g. engineer, review:qa)")
        if not principal:
            raise ValueError("principal is required (who runs this agent)")
        token = secrets.token_urlsafe(32)
        with events.file_lock(self.path):
            rows = self._load()
            if any(r["agent_id"] == agent_id and not r.get("revoked_at") for r in rows):
                raise ValueError(f"agent {agent_id} already registered; revoke it first to rotate")
            rows.append({
                "agent_id": agent_id,
                "team": team or "",
                "roles": roles,
                "principal": principal,
                "token_sha256": _digest(token),
                "created_at": datetime.now(timezone.utc).isoformat(),
                "revoked_at": None,
            })
            self._save(rows)
        return token

    def revoke(self, agent_id: str) -> None:
        with events.file_lock(self.path):
            rows = self._load()
            hit = [r for r in rows if r["agent_id"] == agent_id and not r.get("revoked_at")]
            if not hit:
                raise ValueError(f"no active agent {agent_id}")
            for r in hit:
                r["revoked_at"] = datetime.now(timezone.utc).isoformat()
            self._save(rows)

    # -- verification -------------------------------------------------------

    def authenticate(self, token: str | None) -> Agent:
        if not token:
            raise IdentityError("This install requires an agent token (set AG_AGENT_TOKEN or pass agent_token).")
        d = _digest(token)
        match = None
        for r in self.active():
            if hmac.compare_digest(r.get("token_sha256", ""), d):
                match = r
        if match is None:
            raise IdentityError("Unknown or revoked agent token.")
        return Agent(match["agent_id"], match.get("team", ""), tuple(match.get("roles", [])),
                     match.get("principal") or match["agent_id"])


def resolve(claimed_id: str | None, token: str | None, registry: Registry | None = None) -> tuple[str | None, str | None, bool, Agent | None]:
    """Return (agent_id, principal, verified, agent).

    Enforced registry: the token decides the id. A ``claimed_id`` that does
    not match the token's agent is refused, so a typo cannot act as someone
    else. Unenforced: the claimed id is used as-is and marked unverified.
    """
    reg = registry or Registry()
    if reg.enforced():
        agent = reg.authenticate(token or os.environ.get("AG_AGENT_TOKEN"))
        if claimed_id and claimed_id != agent.agent_id:
            raise IdentityError(f"Token belongs to {agent.agent_id}, not {claimed_id}.")
        return agent.agent_id, agent.principal, True, agent
    return claimed_id or None, claimed_id or None, False, None

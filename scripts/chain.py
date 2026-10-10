#!/usr/bin/env python3
"""
Chain state machine and stuck-ticket recovery (ADR-0010).

Moves the documented production chain from instruction to code for every
write that goes through this module (scripts/ticket.py and the MCP
``ticket_*`` tools). Agents keep running their own loops on their own hosts.
This module governs the edges between them.

States
------
    queued ──claim(work)──▶ working ──submit──▶ in_review ──claim(review)──▶ reviewing
      ▲                       │                     │                          │
      │◀──lease expired───────┘                     │◀──────lease expired──────┘
      │                                             │
      │◀───────── KICK_BACK (same or earlier stage) ┤ (verdict from in_review or reviewing)
      │                                             │
    next stage ◀───────── PASS (not last stage) ────┤
    done       ◀───────── PASS (last stage) ────────┤
    blocked    ◀───────── any verdict with veto hits┤──clear-veto (human)──▶ in_review
    escalated  ◀───────── ESCALATE / REVIEW_REQUIRED┘──resolve (human)─────▶ queued
    escalated  ◀───────── kick-back limit or repeated lease expiry

Rules enforced here (refusals raise ``Refused`` and are logged as events):
  - Claims are scoped to (team, stage). An agent cannot claim another team's work.
  - Only the claimant can heartbeat, submit, or record a verdict. A verdict
    requires a review claim, so it inherits the claim's team and stage scope.
  - Every verdict names an agent, and that agent cannot be the one that did
    the work (self-review refused).
  - A PASS cannot carry veto hits. A blocked ticket accepts no verdict.
  - A KICK_BACK may target the current stage or an earlier one, never later.
  - ``done`` without PASS on the last stage needs an approval-gated override.

Recovery (runs on every claim, and on demand via ``recover``):
  - A claim whose lease expired is released back to the queue. After
    ``max_attempts`` expiries on one stage, the ticket escalates to a human.
  - A ticket kicked back more than ``max_kickbacks`` times escalates.
  - A ticket waiting in a queue or for review past its timeout emits a
    ``ticket.stalled`` event (once per timeout window). It does not change
    state: an absent agent is an operator problem, and the alert says so.
  - A blocked or escalated ticket emits ``ticket.awaiting_human`` on the
    first recovery pass after it lands there, then once per review timeout
    window until a human acts.

Not enforced: an agent that writes the ticket file directly bypasses all of
this. ``agent_id`` is self-reported and unauthenticated, so one agent using
two ids can still review its own work. Reads are not team-scoped.

Config (env; defaults in parentheses):
  AG_LEASE_MINUTES (30)  AG_MAX_ATTEMPTS (3)  AG_MAX_KICKBACKS (3)
  AG_REVIEW_TIMEOUT_MINUTES (120)  AG_QUEUE_TIMEOUT_MINUTES (240)
"""
from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import events  # noqa: E402
import identity  # noqa: E402
import integrity  # noqa: E402

CHAIN = ("research", "pm", "ux", "engineer", "qa")
STATES = ("queued", "working", "in_review", "reviewing", "blocked", "escalated", "done")
VALID_VERDICTS = {"PASS", "KICK_BACK", "REVIEW_REQUIRED", "ESCALATE"}


class StoreCorrupt(ValueError):
    """The ticket file exists but cannot be parsed. Never overwrite it."""


class Refused(RuntimeError):
    """A governed transition was refused. ``event`` describes it for the log."""

    def __init__(self, message: str, event: dict[str, Any] | None = None):
        super().__init__(message)
        self.event = event or {}


def _env_num(name: str, default: float) -> float:
    try:
        return float(os.environ.get(name, default))
    except ValueError:
        return float(default)


@dataclass
class Settings:
    lease_minutes: float = 30
    max_attempts: int = 3
    max_kickbacks: int = 3
    review_timeout_minutes: float = 120
    queue_timeout_minutes: float = 240

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            lease_minutes=_env_num("AG_LEASE_MINUTES", 30),
            max_attempts=int(_env_num("AG_MAX_ATTEMPTS", 3)),
            max_kickbacks=int(_env_num("AG_MAX_KICKBACKS", 3)),
            review_timeout_minutes=_env_num("AG_REVIEW_TIMEOUT_MINUTES", 120),
            queue_timeout_minutes=_env_num("AG_QUEUE_TIMEOUT_MINUTES", 240),
        )


# ---------------------------------------------------------------------------
# Time helpers (ISO strings on disk so the file stays human-readable)
# ---------------------------------------------------------------------------


def iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, timezone.utc).isoformat()


def parse(s: str | None) -> float | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Ticket shape
# ---------------------------------------------------------------------------


def compat_status(state: str) -> str:
    """The legacy ``status`` field the watchdog and dashboard read."""
    if state == "done":
        return "done"
    if state in ("in_review", "reviewing"):
        return "in_review"
    return state


def _set_state(t: dict, state: str, now: float) -> None:
    t["state"] = state
    t["status"] = compat_status(state)
    t["lastActivityAt"] = iso(now)
    if state == "queued":
        t["queuedAt"] = iso(now)
    if state == "in_review":
        t["inReviewSince"] = iso(now)
    t.pop("stalledAlertAt", None)


def _clear_claim(t: dict) -> None:
    for k in ("claimedBy", "claimMode", "leaseExpiresAt"):
        t.pop(k, None)
    t["assigneeAgentId"] = t.get("stage", "")  # pre-1.1 value: the role


def normalize(t: dict, legacy_vetoes: set[str] | None = None) -> dict:
    """Upgrade a pre-1.1 ticket in place. Old tickets were single-stage and
    were created already in review. ``legacy_vetoes`` holds ids whose latest
    1.0 verdict carried veto hits; those load as blocked so the upgrade does
    not silently drop an open veto."""
    if "state" not in t:
        role = t.get("role") or "engineer"
        if legacy_vetoes and t.get("identifier") in legacy_vetoes and t.get("status") != "done":
            t["state"] = "blocked"
            t["veto_open"] = True
        else:
            t["state"] = "done" if t.get("status") == "done" else "in_review"
        t.setdefault("stage", role)
        t.setdefault("stages", [role])
        t.setdefault("inReviewSince", t.get("lastActivityAt"))
    t.setdefault("stage", t.get("role") or "engineer")
    t.setdefault("stages", [t["stage"]])
    t.setdefault("team", "")
    t.setdefault("attempts", {})
    t.setdefault("reviewAttempts", 0)
    t.setdefault("kickbacks", 0)
    t.setdefault("veto_open", t.get("state") == "blocked")
    t["status"] = compat_status(t["state"])
    return t


def new_ticket(ident: str, title: str, stage: str, team: str, now: float, *,
               queued: bool, end_stage: str | None = None) -> dict:
    """``queued=True`` starts a chain ticket that agents claim. If ``stage`` is
    in CHAIN, the ticket runs from there through ``end_stage`` (default: the
    last chain stage). ``queued=False`` registers finished work straight into
    review for one stage (the pre-1.1 ``ticket.py new`` behavior)."""
    if end_stage and end_stage not in CHAIN:
        raise ValueError(f"end stage {end_stage!r} is not a chain stage {list(CHAIN)}")
    if end_stage and not (queued and stage in CHAIN):
        raise ValueError("end stage only applies to queued tickets that start on a chain stage")
    if queued and stage in CHAIN:
        start = CHAIN.index(stage)
        end = CHAIN.index(end_stage) if end_stage else len(CHAIN) - 1
        if end < start:
            raise ValueError(f"end stage {end_stage!r} comes before start stage {stage!r}")
        stages = list(CHAIN[start:end + 1])
    else:
        stages = [stage]
    t = {
        "identifier": ident,
        "title": title,
        "role": stage,
        "team": team or "",
        "stage": stage,
        "stages": stages,
        "assigneeAgentId": stage,
        "createdAt": iso(now),
        "attempts": {},
        "reviewAttempts": 0,
        "kickbacks": 0,
        "veto_open": False,
    }
    _set_state(t, "queued" if queued else "in_review", now)
    return t


def _ev(kind: str, t: dict, agent: str | None = None, outcome: str | None = None, **data) -> dict:
    return {"kind": kind, "ticket": t["identifier"], "role": t.get("stage"),
            "agent_id": agent, "outcome": outcome, "data": data}


def _refuse(t: dict, transition: str, reason: str, agent: str | None) -> None:
    raise Refused(
        f"{t['identifier']}: {transition} refused. {reason}",
        _ev("ticket.transition_refused", t, agent, "refused", transition=transition, reason=reason),
    )


def _escalate(t: dict, reason: str, now: float, agent: str | None = None) -> dict:
    _clear_claim(t)
    t["escalationReason"] = reason
    _set_state(t, "escalated", now)
    return _ev("ticket.escalated", t, agent, "escalated", reason=reason)


# ---------------------------------------------------------------------------
# Recovery
# ---------------------------------------------------------------------------


def recover(tickets: list[dict], now: float, s: Settings) -> list[dict]:
    """Release expired claims, escalate repeat failures, flag stalls."""
    out: list[dict] = []
    for t in tickets:
        state = t.get("state")
        if state in ("working", "reviewing"):
            exp = parse(t.get("leaseExpiresAt"))
            if exp is None or exp > now:
                continue
            agent = t.get("claimedBy")
            mode = t.get("claimMode", "work")
            _clear_claim(t)
            if state == "working":
                n = t["attempts"].get(t["stage"], 0) + 1
                t["attempts"][t["stage"]] = n
                _set_state(t, "queued", now)
            else:
                n = t["reviewAttempts"] = t.get("reviewAttempts", 0) + 1
                _set_state(t, "in_review", now)
            out.append(_ev("ticket.lease_expired", t, agent, "released", mode=mode, attempt=n))
            if n >= s.max_attempts:
                out.append(_escalate(t, f"{mode} lease expired {n} times on stage {t['stage']}", now))
        elif state in ("queued", "in_review"):
            since = parse(t.get("queuedAt") if state == "queued" else t.get("inReviewSince"))
            limit = s.queue_timeout_minutes if state == "queued" else s.review_timeout_minutes
            if since is None or (now - since) < limit * 60:
                continue
            last_alert = parse(t.get("stalledAlertAt"))
            if last_alert and (now - last_alert) < limit * 60:
                continue
            t["stalledAlertAt"] = iso(now)
            who = "agent" if state == "queued" else "reviewer"
            out.append(_ev("ticket.stalled", t, None, "stalled",
                           waiting_for=who, minutes=round((now - since) / 60),
                           message=f"No {who} for stage {t['stage']} (team {t['team'] or '-'}) has claimed this."))
        elif state in ("blocked", "escalated"):
            last_alert = parse(t.get("stalledAlertAt"))
            if last_alert and (now - last_alert) < s.review_timeout_minutes * 60:
                continue
            t["stalledAlertAt"] = iso(now)
            why = "open veto" if state == "blocked" else t.get("escalationReason", "escalated")
            out.append(_ev("ticket.awaiting_human", t, None, state, reason=why,
                           message=f"{t['identifier']} is {state} ({why}) and needs a human."))
    return out


# ---------------------------------------------------------------------------
# Transitions (pure: mutate the ticket list, return event specs)
# ---------------------------------------------------------------------------


def claim_next(tickets: list[dict], role: str, team: str, agent: str, now: float,
               s: Settings, mode: str = "work", principal: str | None = None) -> tuple[dict | None, list[dict]]:
    if not agent:
        raise ValueError("agent_id is required to claim")
    if mode not in ("work", "review"):
        raise ValueError("mode must be 'work' or 'review'")
    evs = recover(tickets, now, s)
    want = "queued" if mode == "work" else "in_review"
    candidates = [
        t for t in tickets
        if t.get("state") == want and t.get("stage") == role and t.get("team", "") == (team or "")
        and not (mode == "review" and t.get("workedBy") == agent)
    and not (mode == "review" and principal is not None and t.get("workedByPrincipal") == principal)
    ]
    if not candidates:
        return None, evs
    key = "queuedAt" if mode == "work" else "inReviewSince"
    t = min(candidates, key=lambda x: (parse(x.get(key)) or 0, x["identifier"]))
    _set_state(t, "working" if mode == "work" else "reviewing", now)
    t["claimedBy"] = agent
    t["claimMode"] = mode
    t["assigneeAgentId"] = agent
    t["leaseExpiresAt"] = iso(now + s.lease_minutes * 60)
    evs.append(_ev("ticket.claimed", t, agent, t["state"], mode=mode, lease_minutes=s.lease_minutes))
    return t, evs


def heartbeat(t: dict, agent: str, now: float, s: Settings) -> list[dict]:
    if t.get("state") not in ("working", "reviewing") or t.get("claimedBy") != agent:
        _refuse(t, "heartbeat", f"{agent or 'caller'} does not hold a live claim on this ticket.", agent)
    t["leaseExpiresAt"] = iso(now + s.lease_minutes * 60)
    t["lastActivityAt"] = iso(now)
    return [_ev("ticket.heartbeat", t, agent, t["state"])]


def submit(t: dict, agent: str, now: float, summary: str = "", principal: str | None = None) -> list[dict]:
    if t.get("state") != "working":
        _refuse(t, "submit", f"Ticket is {t.get('state')}, not working.", agent)
    if t.get("claimedBy") != agent:
        _refuse(t, "submit", f"Claimed by {t.get('claimedBy')}, not {agent}.", agent)
    _clear_claim(t)
    t["workedBy"] = agent
    t["workedByPrincipal"] = principal or agent
    t["reviewAttempts"] = 0
    _set_state(t, "in_review", now)
    return [_ev("ticket.submitted", t, agent, "in_review", summary=summary)]


def verdict(t: dict, v: str, agent: str | None, hits: list[str], now: float, s: Settings,
            to_stage: str | None = None, summary: str = "", domain: str | None = None,
            principal: str | None = None) -> list[dict]:
    v = v.upper()
    if v not in VALID_VERDICTS:
        raise ValueError(f"Invalid verdict {v}. Choose from: {', '.join(sorted(VALID_VERDICTS))}")
    state = t.get("state")
    if not agent:
        _refuse(t, f"verdict {v}", "A verdict must name the reviewing agent.", agent)
    if state == "blocked" or t.get("veto_open"):
        _refuse(t, f"verdict {v}", "Ticket has an open veto. A human runs `clear-veto` (operator approval required).", agent)
    if state != "reviewing":
        hint = " Claim it first: claim --mode review (MCP: ticket_claim_next mode=review)." if state == "in_review" else ""
        _refuse(t, f"verdict {v}", f"Ticket is {state}; a verdict needs a live review claim.{hint}", agent)
    if agent != t.get("claimedBy"):
        _refuse(t, f"verdict {v}", f"Review is claimed by {t.get('claimedBy')}.", agent)
    if agent == t.get("workedBy"):
        _refuse(t, f"verdict {v}", "The agent that did the work cannot review it.", agent)
    if (principal or agent) == t.get("workedByPrincipal", t.get("workedBy")):
        _refuse(t, f"verdict {v}", f"Reviewer and worker share principal {principal or agent!r}; review must come from a different runtime.", agent)
    if v == "PASS" and hits:
        _refuse(t, "verdict PASS", f"A PASS cannot carry veto hits ({', '.join(hits)}). Record KICK_BACK; a human clears the veto.", agent)

    stages = t["stages"]
    cur = t["stage"]
    target = to_stage or cur
    if to_stage and v != "KICK_BACK":
        _refuse(t, f"verdict {v}", "to_stage only applies to KICK_BACK.", agent)
    if target not in stages or stages.index(target) > stages.index(cur):
        _refuse(t, f"verdict {v}", f"Kick-back target {target!r} must be this stage or an earlier one in {stages}.", agent)
    _clear_claim(t)
    t["verdict"] = v
    out = [_ev("ticket.verdict", t, agent, v, veto_hits=hits, summary=summary, domain=domain or cur)]

    if hits:
        t["veto_open"] = True
        t["kickbacks"] = t.get("kickbacks", 0) + 1
        _set_state(t, "blocked", now)
        out.append(_ev("ticket.blocked", t, agent, "blocked", veto_hits=hits))
        return out
    if v in ("ESCALATE", "REVIEW_REQUIRED"):
        out.append(_escalate(t, f"reviewer verdict {v}", now, agent))
        return out
    if v == "PASS":
        t["reviewAttempts"] = 0
        i = stages.index(cur)
        if i == len(stages) - 1:
            _set_state(t, "done", now)
            out.append(_ev("ticket.closed", t, agent, "done", via="verdict"))
        else:
            t["stage"] = t["role"] = stages[i + 1]
            t["attempts"].pop(t["stage"], None)
            t.pop("workedBy", None)
            t.pop("workedByPrincipal", None)
            _set_state(t, "queued", now)
            out.append(_ev("ticket.advanced", t, agent, "queued", from_stage=cur, to_stage=t["stage"]))
        return out

    # KICK_BACK (target validated above)
    t["kickbacks"] = t.get("kickbacks", 0) + 1
    if t["kickbacks"] > s.max_kickbacks:
        out.append(_escalate(t, f"kicked back {t['kickbacks']} times (limit {s.max_kickbacks})", now, agent))
        return out
    t["stage"] = t["role"] = target
    t["attempts"].pop(target, None)  # a new round on this stage gets fresh lease attempts
    t.pop("workedBy", None)
    t.pop("workedByPrincipal", None)
    _set_state(t, "queued", now)
    out.append(_ev("ticket.kicked_back", t, agent, "queued", from_stage=cur, to_stage=target, kickbacks=t["kickbacks"]))
    return out


def _pass_gate(gate) -> None:
    """Run the operator-approval check only after the transition is known to
    be valid, so a mistyped id never burns a one-shot approval."""
    if gate is not None:
        gate()


def clear_veto(t: dict, by: str, reason: str, now: float, gate=None) -> list[dict]:
    if not t.get("veto_open"):
        _refuse(t, "clear-veto", "No open veto.", None)
    _pass_gate(gate)
    t["veto_open"] = False
    t["veto_cleared_by"] = by
    _set_state(t, "in_review", now)  # cleared work goes back to review, never straight to done
    return [_ev("ticket.veto_cleared", t, None, "in_review", cleared_by=by, reason=reason)]


def resolve(t: dict, by: str, reason: str, now: float, to_stage: str | None = None, gate=None) -> list[dict]:
    if t.get("state") != "escalated":
        _refuse(t, "resolve", f"Ticket is {t.get('state')}, not escalated.", None)
    target = to_stage or t["stage"]
    if target not in t["stages"]:
        _refuse(t, "resolve", f"Stage {target!r} is not in {t['stages']}.", None)
    _pass_gate(gate)
    t["stage"] = t["role"] = target
    t["attempts"] = {}
    t["reviewAttempts"] = 0
    t["kickbacks"] = 0
    t.pop("escalationReason", None)
    t.pop("workedBy", None)
    t.pop("workedByPrincipal", None)
    _set_state(t, "queued", now)
    return [_ev("ticket.resolved", t, None, "queued", by=by, reason=reason, to_stage=target)]


def close(t: dict, now: float, *, override: bool, by: str | None = None,
          reason: str | None = None, agent: str | None = None, gate=None) -> list[dict]:
    if t.get("state") == "done":
        return []
    if not override:
        _refuse(t, "done", f"Ticket is {t.get('state')} at stage {t.get('stage')}. "
                "It closes through a PASS on its last stage.", agent)
    _pass_gate(gate)
    _clear_claim(t)
    t["closed_by_override"] = by
    _set_state(t, "done", now)
    return [_ev("ticket.closed", t, agent, "done", via="override", by=by, reason=reason)]


# ---------------------------------------------------------------------------
# Store: locked load / mutate / save, plus event and verdict-view writes
# ---------------------------------------------------------------------------


@dataclass
class Store:
    """Locked load / mutate / save over the ticket file, with:

    - identity (ADR-0011): when the agent registry is enforced, agent actions
      present a token; the id, team, stages, and principal come from the
      registry, not the caller.
    - integrity (ADR-0012): every load checks the ticket file and the event
      log against the signed head record; every commit writes temp file,
      events, file, head, in that order, so a crash can be rolled forward and
      anything else is reported as tampering.
    """
    ticket_file: Path
    verdict_log: Path
    event_log: Path
    settings: Settings = field(default_factory=Settings.from_env)
    registry: Any = None
    head_file: Path | None = None

    def __post_init__(self):
        if self.registry is None:
            self.registry = identity.Registry()
        if self.head_file is None:
            # One head per ticket store, next to it: runs/in_review.integrity.json
            self.head_file = Path(os.environ.get(
                "AG_INTEGRITY_HEAD", self.ticket_file.with_name(self.ticket_file.stem + ".integrity.json")))

    # -- reading -------------------------------------------------------------

    def load(self) -> list[dict]:
        """Load and normalize tickets. A missing file is an empty store; a
        file that exists but does not parse raises ``StoreCorrupt`` so no
        write ever replaces it."""
        if not self.ticket_file.exists():
            return []
        try:
            data = json.loads(self.ticket_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError, UnicodeDecodeError) as e:
            raise StoreCorrupt(f"{self.ticket_file} cannot be read ({e}). Fix or move it; refusing to overwrite.")
        if not isinstance(data, list):
            raise StoreCorrupt(f"{self.ticket_file} is not a JSON list. Fix or move it; refusing to overwrite.")
        legacy = None
        if any(isinstance(t, dict) and "state" not in t for t in data):
            legacy = self._legacy_vetoes()
        return [normalize(t, legacy) for t in data if isinstance(t, dict)]

    def _legacy_vetoes(self) -> set[str]:
        """Ticket ids whose latest pre-1.1 verdict carried veto hits."""
        latest: dict[str, bool] = {}
        if not self.verdict_log.exists():
            return set()
        for line in self.verdict_log.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get("ticket"):
                latest[r["ticket"]] = bool(r.get("veto_triggered") or r.get("veto_hits"))
        return {k for k, v in latest.items() if v}

    # -- integrity -------------------------------------------------------------

    def _tmp(self) -> Path:
        return self.ticket_file.with_name(self.ticket_file.name + ".tmp")

    def check_integrity(self, *, repair: bool = True) -> dict:
        """Compare the ticket file and log against the head record. Rolls an
        interrupted commit forward when ``repair``. Raises TamperDetected."""
        key = integrity.load_key()
        head = integrity.read_head(self.head_file, key)
        file_d = integrity.file_digest(self.ticket_file)
        if head is None:
            # A log with committed ticket state but no head: the head (and
            # maybe the ticket file) was removed. Fresh and pre-1.2 installs
            # have no committed state in the log.
            if integrity.last_hash(self.event_log) != integrity.GENESIS and any(
                    (e.get("data") or {}).get("state_digest") for e in self._events_after(0)):
                raise integrity.TamperDetected(f"{self.head_file} is missing but the log has committed ticket state")
            return {"head": None, "store_digest": file_d}
        line = integrity.line_ending_at(self.event_log, int(head["log_offset"])) if self.event_log.exists() else None
        try:
            at = json.loads(line).get("hash") if line else None
        except json.JSONDecodeError:
            at = None
        if at != head["log_head"]:
            raise integrity.TamperDetected("event log was truncated or rewritten before the last commit")
        tail = self._events_after(int(head["log_offset"]))
        self._check_segment(tail, head["log_head"], key)
        digests = [e["data"]["state_digest"] for e in tail if (e.get("data") or {}).get("state_digest")]
        expected = digests[-1] if digests else head["store_digest"]
        if file_d == expected:
            return {"head": head, "store_digest": file_d, "rolled_forward": bool(digests)}
        # Interrupted commit: events were written, the replace was not.
        if digests and self._tmp().exists() and integrity.file_digest(self._tmp()) == expected:
            if repair:
                os.replace(self._tmp(), self.ticket_file)
                return {"head": head, "store_digest": expected, "rolled_forward": True}
            return {"head": head, "store_digest": file_d, "pending_roll_forward": True}
        raise integrity.TamperDetected(
            f"{self.ticket_file} does not match the last committed state (edited outside the framework?)")

    def _events_after(self, offset: int) -> list[dict]:
        if not self.event_log.exists():
            return []
        out = []
        with open(self.event_log, "rb") as fh:
            fh.seek(offset)
            for raw in fh:
                try:
                    out.append(json.loads(raw))
                except json.JSONDecodeError:
                    out.append({"_bad": True})
        return out

    def _check_segment(self, evs: list[dict], prev: str, key: bytes | None) -> None:
        for e in evs:
            if e.get("_bad") or "hash" not in e or e.get("prev_hash") != prev:
                raise integrity.TamperDetected("event log chain is broken after the last commit")
            if key and e.get("hash_alg") != "hmac-sha256":
                raise integrity.TamperDetected("unkeyed event appended to a keyed log")
            expect = integrity.recompute(e, key)
            if expect is not None and expect != e["hash"]:
                raise integrity.TamperDetected("event after the last commit was edited")
            prev = e["hash"]

    def _report_tamper(self, err: Exception, now: float) -> None:
        try:
            events.emit("store.tamper_detected", path=self.event_log, now=now, outcome="refused",
                        data={"reason": str(err)})
        except Exception:  # noqa: BLE001 - the refusal matters more than the report
            pass

    # -- identity --------------------------------------------------------------

    def who(self, claimed: str | None, token: str | None, ticket: dict | None = None):
        """(agent_id, principal, verified, agent). Identity failures become
        logged refusals."""
        try:
            return identity.resolve(claimed, token, self.registry)
        except identity.IdentityError as e:
            stub = ticket or {"identifier": None, "stage": None}
            raise Refused(str(e), _ev("ticket.transition_refused", stub, claimed, "refused",
                                      transition="identify", reason=str(e)))

    # -- commit ----------------------------------------------------------------

    def _emit_all(self, specs: list[dict], now: float, verified_id: str | None = None,
                  state_digest: str | None = None) -> tuple[list[dict], int | None, str | None]:
        out, offset, last = [], None, None
        for spec in specs:
            spec = dict(spec)
            spec["data"] = dict(spec.get("data") or {})
            if state_digest:
                spec["data"]["state_digest"] = state_digest
            verified = bool(verified_id) and spec.get("agent_id") == verified_id
            ev, offset = events.emit_at(spec.pop("kind"), path=self.event_log, now=now,
                                        agent_verified=verified, **spec)
            last = ev["hash"]
            out.append(ev)
            if ev["kind"] == "ticket.verdict":
                hits = ev["data"].get("veto_hits") or []
                events.append_jsonl(self.verdict_log, {
                    "kind": "verdict",
                    "domain": ev["data"].get("domain") or ev["role"] or "unknown",
                    "verdict": ev["outcome"],
                    "veto_triggered": bool(hits),
                    "veto_hits": hits,
                    "ticket": ev["ticket"],
                    "summary": ev["data"].get("summary", ""),
                    "ts": ev["ts"],
                    "event_id": ev["event_id"],
                    "agent_id": ev["agent_id"],
                    "agent_verified": ev["agent_verified"],
                })
        return out, offset, last

    def transact(self, fn, *, now: float | None = None, ids: dict | None = None):
        """Run ``fn(tickets, now) -> (result, event_specs)`` under the ticket
        lock. Order: integrity check, mutate, temp file, events (stamped with
        the new state digest), replace, head. A failure before the replace
        saves nothing. Refusals are logged; nothing is saved on refusal."""
        now = time.time() if now is None else now
        with events.file_lock(self.ticket_file):
            try:
                state = self.check_integrity()
            except integrity.TamperDetected as e:
                self._report_tamper(e, now)
                raise
            accepted = (state.get("head") or {}).get("accepted_problems", [])
            tickets = self.load()
            before = self.ticket_file.read_bytes() if self.ticket_file.exists() else None
            try:
                result, specs = fn(tickets, now)
            except Refused as r:
                if r.event:
                    self._emit_all([r.event], now)
                raise
            content = json.dumps(tickets, indent=2).encode("utf-8")
            if not specs and content == before:
                return result
            if not specs:
                specs = [{"kind": "store.committed", "ticket": None, "role": None,
                          "agent_id": None, "outcome": "saved", "data": {}}]
            digest = integrity.hashlib.sha256(content).hexdigest()
            self.ticket_file.parent.mkdir(parents=True, exist_ok=True)
            self._tmp().write_bytes(content)
            verified_id = (ids or {}).get("v")
            _, offset, last = self._emit_all(specs, now, verified_id, digest)
            os.replace(self._tmp(), self.ticket_file)
            integrity.write_head(offset, last, digest, self.head_file, integrity.load_key(), accepted)
        return result

    def accept_current_state(self, by: str, reason: str, gate=None, now: float | None = None,
                             accepted_problems: list[str] | None = None) -> dict:
        """Operator re-baseline after investigating a tamper report. Records
        who accepted what; the event stays in the log forever."""
        now = time.time() if now is None else now
        key = integrity.load_key()
        with events.file_lock(self.ticket_file):
            problem = None
            try:
                self.check_integrity(repair=False)
            except integrity.TamperDetected as e:
                problem = str(e)
            new_log_problems = list(accepted_problems or [])
            if problem is None and not new_log_problems:
                raise Refused("Integrity check passes; nothing to accept.")
            if gate is not None:
                gate()
            self.load()  # still refuse an unparseable file
            try:
                prior = (integrity.read_head(self.head_file, key) or {}).get("accepted_problems", [])
            except integrity.TamperDetected:
                prior = []
            digest = integrity.file_digest(self.ticket_file)
            ev, offset = events.emit_at("store.integrity_accepted", path=self.event_log, now=now,
                                        outcome="accepted",
                                        data={"by": by, "reason": reason, "problem": problem,
                                              "log_problems": new_log_problems, "state_digest": digest})
            integrity.write_head(offset, ev["hash"], digest, self.head_file, key,
                                 prior + new_log_problems)
        return {"accepted": problem, "log_problems": new_log_problems, "store_digest": digest}

    # -- wrappers ----------------------------------------------------------------

    def _one(self, tickets: list[dict], ident: str) -> dict:
        t = next((x for x in tickets if x.get("identifier") == ident), None)
        if t is None:
            raise KeyError(f"Ticket {ident} not found.")
        return t

    def create(self, title: str, stage: str, team: str = "", *, queued: bool = True,
               end_stage: str | None = None, agent: str | None = None, now: float | None = None,
               token: str | None = None) -> dict:
        ids = {}

        def fn(tickets, now):
            # Operators may create without a token; an agent that presents
            # one is recorded as verified.
            aid, _, verified, _ = self.who(agent, token) if (token or not self.registry.enforced()) else (None, None, False, None)
            ids["v"] = aid if verified else None
            nums = [int(t["identifier"][2:]) for t in tickets
                    if str(t.get("identifier", "")).startswith("T-") and t["identifier"][2:].isdigit()]
            t = new_ticket(f"T-{(max(nums) + 1) if nums else 1}", title, stage, team, now,
                           queued=queued, end_stage=end_stage)
            tickets.append(t)
            return t, [_ev("ticket.created", t, aid, t["state"], title=title, team=t["team"], stages=t["stages"])]
        return self.transact(fn, now=now, ids=ids)

    def claim_next(self, role: str, team: str, agent: str | None, mode: str = "work",
                   now: float | None = None, token: str | None = None):
        ids = {}

        def fn(tickets, n):
            aid, principal, verified, who = self.who(agent, token)
            if not aid:
                raise ValueError("agent_id is required to claim")
            ids["v"] = aid if verified else None
            use_team = team
            if who is not None:
                if team and team != who.team:
                    raise Refused(f"{aid} belongs to team {who.team!r}, not {team!r}.",
                                  _ev("ticket.transition_refused", {"identifier": None, "stage": role}, aid,
                                      "refused", transition="claim", reason="team mismatch"))
                use_team = who.team
                allowed = who.may_work(role) if mode == "work" else who.may_review(role)
                if not allowed:
                    need = role if mode == "work" else f"review:{role}"
                    raise Refused(f"{aid} is not registered for {need!r}.",
                                  _ev("ticket.transition_refused", {"identifier": None, "stage": role}, aid,
                                      "refused", transition="claim", reason=f"missing role {need}"))
            return claim_next(tickets, role, use_team, aid, n, self.settings, mode,
                              principal if verified else None)
        return self.transact(fn, now=now, ids=ids)

    def heartbeat(self, ident: str, agent: str | None, now: float | None = None, token: str | None = None):
        ids = {}

        def fn(ts, n):
            t = self._one(ts, ident)
            aid, _, verified, _ = self.who(agent, token, t)
            ids["v"] = aid if verified else None
            return t, heartbeat(t, aid, n, self.settings)
        return self.transact(fn, now=now, ids=ids)

    def submit(self, ident: str, agent: str | None, summary: str = "", now: float | None = None,
               token: str | None = None):
        ids = {}

        def fn(ts, n):
            t = self._one(ts, ident)
            aid, principal, verified, _ = self.who(agent, token, t)
            ids["v"] = aid if verified else None
            return t, submit(t, aid, n, summary, principal)
        return self.transact(fn, now=now, ids=ids)

    def verdict(self, ident: str, v: str, agent: str | None, hits: list[str], *,
                to_stage: str | None = None, summary: str = "", domain: str | None = None,
                now: float | None = None, token: str | None = None):
        ids = {}

        def fn(ts, n):
            t = self._one(ts, ident)
            aid, principal, verified, _ = self.who(agent, token, t)
            ids["v"] = aid if verified else None
            return t, verdict(t, v, aid, hits, n, self.settings, to_stage, summary, domain, principal)
        return self.transact(fn, now=now, ids=ids)

    def clear_veto(self, ident: str, by: str, reason: str, now: float | None = None, gate=None):
        return self.transact(lambda ts, n: (self._one(ts, ident), clear_veto(self._one(ts, ident), by, reason, n, gate)), now=now)

    def resolve(self, ident: str, by: str, reason: str, to_stage: str | None = None,
                now: float | None = None, gate=None):
        return self.transact(lambda ts, n: (self._one(ts, ident), resolve(self._one(ts, ident), by, reason, n, to_stage, gate)), now=now)

    def close(self, ident: str, *, override: bool, by: str | None = None, reason: str | None = None,
              agent: str | None = None, now: float | None = None, gate=None):
        def fn(ts, n):
            t = self._one(ts, ident)
            return t, close(t, n, override=override, by=by, reason=reason, agent=agent, gate=gate)
        return self.transact(fn, now=now)

    def recover(self, now: float | None = None) -> list[dict]:
        specs_out: list[dict] = []

        def fn(ts, n):
            specs = recover(ts, n, self.settings)
            specs_out.extend(dict(s) for s in specs)
            return None, specs
        self.transact(fn, now=now)
        return specs_out

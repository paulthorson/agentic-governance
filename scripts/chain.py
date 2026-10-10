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
  - Claims are scoped to (team, stage). An agent never sees another team's work.
  - Only the claimant can heartbeat or submit a claimed ticket.
  - The agent that did the work cannot review it (self-review refused).
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

Not enforced: an agent that writes the ticket file directly bypasses all of
this. ``agent_id`` is self-reported and unauthenticated.

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

CHAIN = ("research", "pm", "ux", "engineer", "qa")
STATES = ("queued", "working", "in_review", "reviewing", "blocked", "escalated", "done")
VALID_VERDICTS = {"PASS", "KICK_BACK", "REVIEW_REQUIRED", "ESCALATE"}


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
    t["assigneeAgentId"] = ""


def normalize(t: dict) -> dict:
    """Upgrade a pre-1.1 ticket in place. Old tickets were single-stage and
    were created already in review."""
    if "state" not in t:
        role = t.get("role") or "engineer"
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
        "assigneeAgentId": "",
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
    return out


# ---------------------------------------------------------------------------
# Transitions (pure: mutate the ticket list, return event specs)
# ---------------------------------------------------------------------------


def claim_next(tickets: list[dict], role: str, team: str, agent: str, now: float,
               s: Settings, mode: str = "work") -> tuple[dict | None, list[dict]]:
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


def submit(t: dict, agent: str, now: float, summary: str = "") -> list[dict]:
    if t.get("state") != "working":
        _refuse(t, "submit", f"Ticket is {t.get('state')}, not working.", agent)
    if t.get("claimedBy") != agent:
        _refuse(t, "submit", f"Claimed by {t.get('claimedBy')}, not {agent}.", agent)
    _clear_claim(t)
    t["workedBy"] = agent
    _set_state(t, "in_review", now)
    return [_ev("ticket.submitted", t, agent, "in_review", summary=summary)]


def verdict(t: dict, v: str, agent: str | None, hits: list[str], now: float, s: Settings,
            to_stage: str | None = None, summary: str = "", domain: str | None = None) -> list[dict]:
    v = v.upper()
    if v not in VALID_VERDICTS:
        raise ValueError(f"Invalid verdict {v}. Choose from: {', '.join(sorted(VALID_VERDICTS))}")
    state = t.get("state")
    if state == "blocked" or t.get("veto_open"):
        _refuse(t, f"verdict {v}", "Ticket has an open veto. A human runs `clear-veto` (operator approval required).", agent)
    if state not in ("in_review", "reviewing"):
        _refuse(t, f"verdict {v}", f"Ticket is {state}; verdicts apply to work in review.", agent)
    if state == "reviewing" and agent != t.get("claimedBy"):
        _refuse(t, f"verdict {v}", f"Review is claimed by {t.get('claimedBy')}.", agent)
    if agent and agent == t.get("workedBy"):
        _refuse(t, f"verdict {v}", "The agent that did the work cannot review it.", agent)
    if v == "PASS" and hits:
        _refuse(t, "verdict PASS", f"A PASS cannot carry veto hits ({', '.join(hits)}). Record KICK_BACK; a human clears the veto.", agent)

    stages = t["stages"]
    cur = t["stage"]
    target = to_stage or cur
    if v == "KICK_BACK" and not hits and (
        target not in stages or stages.index(target) > stages.index(cur)
    ):
        _refuse(t, "verdict KICK_BACK", f"Kick-back target {target!r} must be this stage or an earlier one in {stages}.", agent)
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
            t.pop("workedBy", None)
            _set_state(t, "queued", now)
            out.append(_ev("ticket.advanced", t, agent, "queued", from_stage=cur, to_stage=t["stage"]))
        return out

    # KICK_BACK (target validated above)
    t["kickbacks"] = t.get("kickbacks", 0) + 1
    if t["kickbacks"] > s.max_kickbacks:
        out.append(_escalate(t, f"kicked back {t['kickbacks']} times (limit {s.max_kickbacks})", now, agent))
        return out
    t["stage"] = t["role"] = target
    t.pop("workedBy", None)
    _set_state(t, "queued", now)
    out.append(_ev("ticket.kicked_back", t, agent, "queued", from_stage=cur, to_stage=target, kickbacks=t["kickbacks"]))
    return out


def clear_veto(t: dict, by: str, reason: str, now: float) -> list[dict]:
    if not t.get("veto_open"):
        _refuse(t, "clear-veto", "No open veto.", None)
    t["veto_open"] = False
    t["veto_cleared_by"] = by
    _set_state(t, "in_review", now)  # cleared work goes back to review, never straight to done
    return [_ev("ticket.veto_cleared", t, None, "in_review", cleared_by=by, reason=reason)]


def resolve(t: dict, by: str, reason: str, now: float, to_stage: str | None = None) -> list[dict]:
    if t.get("state") != "escalated":
        _refuse(t, "resolve", f"Ticket is {t.get('state')}, not escalated.", None)
    target = to_stage or t["stage"]
    if target not in t["stages"]:
        _refuse(t, "resolve", f"Stage {target!r} is not in {t['stages']}.", None)
    t["stage"] = t["role"] = target
    t["attempts"] = {}
    t["reviewAttempts"] = 0
    t["kickbacks"] = 0
    t.pop("escalationReason", None)
    t.pop("workedBy", None)
    _set_state(t, "queued", now)
    return [_ev("ticket.resolved", t, None, "queued", by=by, reason=reason, to_stage=target)]


def close(t: dict, now: float, *, override: bool, by: str | None = None,
          reason: str | None = None, agent: str | None = None) -> list[dict]:
    if t.get("state") == "done":
        return []
    if not override:
        _refuse(t, "done", f"Ticket is {t.get('state')} at stage {t.get('stage')}. "
                "It closes through a PASS on its last stage.", agent)
    _clear_claim(t)
    t["closed_by_override"] = by
    _set_state(t, "done", now)
    return [_ev("ticket.closed", t, agent, "done", via="override", by=by, reason=reason)]


# ---------------------------------------------------------------------------
# Store: locked load / mutate / save, plus event and verdict-view writes
# ---------------------------------------------------------------------------


@dataclass
class Store:
    ticket_file: Path
    verdict_log: Path
    event_log: Path
    settings: Settings = field(default_factory=Settings.from_env)

    def load(self) -> list[dict]:
        if not self.ticket_file.exists():
            return []
        try:
            data = json.loads(self.ticket_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
        return [normalize(t) for t in data] if isinstance(data, list) else []

    def _save(self, tickets: list[dict]) -> None:
        self.ticket_file.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.ticket_file.with_name(self.ticket_file.name + ".tmp")
        tmp.write_text(json.dumps(tickets, indent=2), encoding="utf-8")
        os.replace(tmp, self.ticket_file)

    def _emit_all(self, specs: list[dict]) -> list[dict]:
        out = []
        for spec in specs:
            ev = events.emit(spec.pop("kind"), path=self.event_log, **spec)
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
                })
        return out

    def transact(self, fn, *, now: float | None = None):
        """Run ``fn(tickets, now) -> (result, event_specs)`` under the ticket
        lock. Refusals are logged and re-raised; nothing is saved on refusal."""
        now = time.time() if now is None else now
        with events.file_lock(self.ticket_file):
            tickets = self.load()
            try:
                result, specs = fn(tickets, now)
            except Refused as r:
                if r.event:
                    self._emit_all([dict(r.event)])
                raise
            self._save(tickets)
        self._emit_all(specs)
        return result

    # Convenience wrappers --------------------------------------------------

    def _one(self, tickets: list[dict], ident: str) -> dict:
        t = next((x for x in tickets if x.get("identifier") == ident), None)
        if t is None:
            raise KeyError(f"Ticket {ident} not found.")
        return t

    def create(self, title: str, stage: str, team: str = "", *, queued: bool = True,
               end_stage: str | None = None, agent: str | None = None, now: float | None = None) -> dict:
        def fn(tickets, now):
            nums = [int(t["identifier"][2:]) for t in tickets
                    if str(t.get("identifier", "")).startswith("T-") and t["identifier"][2:].isdigit()]
            t = new_ticket(f"T-{(max(nums) + 1) if nums else 1}", title, stage, team, now,
                           queued=queued, end_stage=end_stage)
            tickets.append(t)
            return t, [_ev("ticket.created", t, agent, t["state"], title=title, team=t["team"], stages=t["stages"])]
        return self.transact(fn, now=now)

    def claim_next(self, role: str, team: str, agent: str, mode: str = "work", now: float | None = None):
        return self.transact(lambda ts, n: claim_next(ts, role, team, agent, n, self.settings, mode), now=now)

    def heartbeat(self, ident: str, agent: str, now: float | None = None):
        return self.transact(lambda ts, n: (self._one(ts, ident), heartbeat(self._one(ts, ident), agent, n, self.settings)), now=now)

    def submit(self, ident: str, agent: str, summary: str = "", now: float | None = None):
        return self.transact(lambda ts, n: (self._one(ts, ident), submit(self._one(ts, ident), agent, n, summary)), now=now)

    def verdict(self, ident: str, v: str, agent: str | None, hits: list[str], *,
                to_stage: str | None = None, summary: str = "", domain: str | None = None,
                now: float | None = None):
        def fn(ts, n):
            t = self._one(ts, ident)
            return t, verdict(t, v, agent, hits, n, self.settings, to_stage, summary, domain)
        return self.transact(fn, now=now)

    def clear_veto(self, ident: str, by: str, reason: str, now: float | None = None):
        return self.transact(lambda ts, n: (self._one(ts, ident), clear_veto(self._one(ts, ident), by, reason, n)), now=now)

    def resolve(self, ident: str, by: str, reason: str, to_stage: str | None = None, now: float | None = None):
        return self.transact(lambda ts, n: (self._one(ts, ident), resolve(self._one(ts, ident), by, reason, n, to_stage)), now=now)

    def close(self, ident: str, *, override: bool, by: str | None = None, reason: str | None = None,
              agent: str | None = None, now: float | None = None):
        def fn(ts, n):
            t = self._one(ts, ident)
            return t, close(t, n, override=override, by=by, reason=reason, agent=agent)
        return self.transact(fn, now=now)

    def recover(self, now: float | None = None) -> list[dict]:
        specs_out: list[dict] = []

        def fn(ts, n):
            specs = recover(ts, n, self.settings)
            specs_out.extend(dict(s) for s in specs)
            return None, specs
        self.transact(fn, now=now)
        return specs_out

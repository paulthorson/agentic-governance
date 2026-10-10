#!/usr/bin/env python3
"""
Local ticket/story system for the agentic-governance framework.

A built-in, file-based ticket base so a default install works with NO external
tracker (no Paperclip, no GitHub, no Linear). It gives a team a simple way to:

  - create work items (epics/stories) that flow through the review chain
  - track their state (in_review -> verdict -> done)
  - feed the stuck-review-watchdog (writes runs/in_review.json)
  - feed the veto-telemetry (writes runs/verdicts.jsonl)
  - feed the event log (writes runs/events.jsonl, ADR-0009)

This is the "local ticket base" for teams that don't use Paperclip (ADR-0007).
The watchdog reads runs/in_review.json via `--source file`, and telemetry reads
runs/verdicts.jsonl, so the whole loop works out of the box.

Close gate (ADR-0009, code-enforced for this script only):
  - A ticket closes only through a recorded PASS verdict.
  - `done` refuses unless the ticket's latest verdict is PASS. It exists for
    idempotent re-closes and for the approval-gated `--override` path.
  - A PASS that carries veto hits is refused. A ticket with an open veto
    refuses PASS until `clear-veto` is run, which requires operator approval
    (scripts/approval.py) and records who cleared it and why.
  - Refusals are recorded in the event log, so a bypass attempt is visible.
Agents that edit runs/in_review.json directly are outside this gate.

Usage:
  python3 scripts/ticket.py new "Title" [--role engineer] [--team team-a] [--agent ID]
  python3 scripts/ticket.py list [--status in_review|done|all]
  python3 scripts/ticket.py verdict <id> PASS|KICK_BACK|REVIEW_REQUIRED|ESCALATE [--domain ux] [--veto-hits "a,b"] [--summary "."] [--agent ID]
  python3 scripts/ticket.py clear-veto <id> --by "Name" --reason "."      (needs approval)
  python3 scripts/ticket.py done <id> [--override --by "Name" --reason "."] (override needs approval)
  python3 scripts/ticket.py show <id>

Config (env):
  TICKET_FILE   path to the in_review ledger (default: runs/in_review.json)
  VERDICT_LOG   path to the verdict ledger (default: runs/verdicts.jsonl)
  EVENT_LOG     path to the event log      (default: runs/events.jsonl)
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import events  # noqa: E402
from approval import ApprovalRequired, require_approval  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
TICKET_FILE = Path(os.environ.get("TICKET_FILE", REPO_ROOT / "runs" / "in_review.json"))
VERDICT_LOG = Path(os.environ.get("VERDICT_LOG", REPO_ROOT / "runs" / "verdicts.jsonl"))
EVENT_LOG = Path(os.environ.get("EVENT_LOG", REPO_ROOT / "runs" / "events.jsonl"))

VALID_VERDICTS = {"PASS", "KICK_BACK", "REVIEW_REQUIRED", "ESCALATE"}


class Refused(RuntimeError):
    """A governed transition was refused. The message says why."""


def _load_tickets() -> list[dict]:
    if not TICKET_FILE.exists():
        return []
    try:
        data = json.loads(TICKET_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def _save_tickets(tickets: list[dict]) -> None:
    """Write atomically: temp file + os.replace, so a crash mid-write never
    leaves a truncated ledger. Callers hold the TICKET_FILE lock."""
    TICKET_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = TICKET_FILE.with_name(TICKET_FILE.name + ".tmp")
    tmp.write_text(json.dumps(tickets, indent=2), encoding="utf-8")
    os.replace(tmp, TICKET_FILE)


def _next_id(tickets: list[dict]) -> str:
    # Highest numeric suffix + 1, e.g. T-1, T-2, ...
    nums = []
    for t in tickets:
        ident = t.get("identifier", "")
        if ident.startswith("T-") and ident[2:].isdigit():
            nums.append(int(ident[2:]))
    return f"T-{(max(nums) + 1) if nums else 1}"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _find(tickets: list[dict], ident: str) -> dict | None:
    return next((x for x in tickets if x.get("identifier") == ident), None)


def _emit(kind: str, **fields) -> dict:
    return events.emit(kind, path=EVENT_LOG, **fields)


def _refuse(ticket_id: str, transition: str, reason: str, agent: str | None) -> None:
    _emit(
        "ticket.transition_refused",
        ticket=ticket_id,
        agent_id=agent,
        outcome="refused",
        data={"transition": transition, "reason": reason},
    )
    raise Refused(f"{ticket_id}: {transition} refused. {reason}")


def _agent(args) -> str | None:
    return getattr(args, "agent", None)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_new(args) -> None:
    with events.file_lock(TICKET_FILE):
        tickets = _load_tickets()
        ident = _next_id(tickets)
        ticket = {
            "identifier": ident,
            "title": args.title,
            "role": args.role or "engineer",
            "team": args.team or "",
            "status": "in_review",
            "assigneeAgentId": args.role or "",
            "lastActivityAt": _now_iso(),
            "createdAt": _now_iso(),
            "veto_open": False,
        }
        tickets.append(ticket)
        _save_tickets(tickets)
    _emit(
        "ticket.created",
        ticket=ident,
        role=ticket["role"],
        agent_id=_agent(args),
        outcome="in_review",
        data={"title": args.title, "team": ticket["team"]},
    )
    print(f"Created {ident}: {args.title} (status: in_review)")


def cmd_list(args) -> None:
    tickets = _load_tickets()
    if args.status and args.status != "all":
        tickets = [t for t in tickets if t.get("status") == args.status]
    if not tickets:
        print("No tickets.")
        return
    for t in tickets:
        print(f"{t.get('identifier','?'):6} [{t.get('status','?'):9}] {t.get('title','')[:60]}")


def cmd_show(args) -> None:
    t = _find(_load_tickets(), args.id)
    if not t:
        print(f"Ticket {args.id} not found.")
        return
    for k, v in t.items():
        print(f"{k}: {v}")


def cmd_verdict(args) -> None:
    if args.verdict not in VALID_VERDICTS:
        print(f"Invalid verdict {args.verdict}. Choose from: {', '.join(sorted(VALID_VERDICTS))}")
        sys.exit(1)
    hits = [h.strip() for h in args.veto_hits.split(",") if h.strip()] if args.veto_hits else []
    agent = _agent(args)
    with events.file_lock(TICKET_FILE):
        tickets = _load_tickets()
        t = _find(tickets, args.id)
        if not t:
            print(f"Ticket {args.id} not found.")
            return
        domain = args.domain or t.get("role", "unknown")
        if args.verdict == "PASS" and hits:
            _refuse(args.id, "verdict PASS", f"A PASS cannot carry veto hits ({', '.join(hits)}). Record KICK_BACK; a human clears the veto.", agent)
        if args.verdict == "PASS" and t.get("veto_open"):
            _refuse(args.id, "verdict PASS", "Ticket has an open veto. Run `clear-veto` (operator approval required) first.", agent)

        ev = _emit(
            "ticket.verdict",
            ticket=args.id,
            role=domain,
            agent_id=agent,
            outcome=args.verdict,
            data={"veto_hits": hits, "summary": args.summary or ""},
        )
        # Compatibility view: veto-telemetry and the dashboard read this file.
        record = {
            "kind": "verdict",
            "domain": domain,
            "verdict": args.verdict,
            "veto_triggered": bool(hits),
            "veto_hits": hits,
            "ticket": args.id,
            "summary": args.summary or "",
            "ts": ev["ts"],
            "event_id": ev["event_id"],
        }
        events.append_jsonl(VERDICT_LOG, record)

        t["verdict"] = args.verdict
        t["lastActivityAt"] = _now_iso()
        if hits:
            t["veto_open"] = True
        if args.verdict == "PASS":
            t["status"] = "done"
        _save_tickets(tickets)

    if args.verdict == "PASS":
        _emit("ticket.closed", ticket=args.id, agent_id=agent, outcome="done", data={"via": "verdict"})
        print(f"{args.id}: PASS, marked done.")
    else:
        print(f"{args.id}: {args.verdict}, still in_review (needs rework).")


def cmd_clear_veto(args) -> None:
    if not args.by or not args.reason:
        print("clear-veto requires --by and --reason.")
        sys.exit(1)
    try:
        require_approval("clear_veto", REPO_ROOT, consume=True)
    except ApprovalRequired as e:
        _emit("ticket.transition_refused", ticket=args.id, outcome="refused",
              data={"transition": "clear-veto", "reason": str(e)})
        raise Refused(str(e))
    with events.file_lock(TICKET_FILE):
        tickets = _load_tickets()
        t = _find(tickets, args.id)
        if not t:
            print(f"Ticket {args.id} not found.")
            return
        if not t.get("veto_open"):
            print(f"{args.id}: no open veto.")
            return
        t["veto_open"] = False
        t["veto_cleared_by"] = args.by
        t["lastActivityAt"] = _now_iso()
        _save_tickets(tickets)
    _emit("ticket.veto_cleared", ticket=args.id, outcome="cleared",
          data={"cleared_by": args.by, "reason": args.reason})
    print(f"{args.id}: veto cleared by {args.by}.")


def cmd_done(args) -> None:
    agent = _agent(args)
    override = getattr(args, "override", False)
    if override:
        if not getattr(args, "by", None) or not getattr(args, "reason", None):
            print("--override requires --by and --reason.")
            sys.exit(1)
        try:
            require_approval("ticket_done_override", REPO_ROOT, consume=True)
        except ApprovalRequired as e:
            _refuse(args.id, "done --override", str(e), agent)
    with events.file_lock(TICKET_FILE):
        tickets = _load_tickets()
        t = _find(tickets, args.id)
        if not t:
            print(f"Ticket {args.id} not found.")
            return
        if t.get("status") == "done":
            print(f"{args.id}: already done.")
            return
        if not override:
            if t.get("veto_open"):
                _refuse(args.id, "done", "Ticket has an open veto.", agent)
            if t.get("verdict") != "PASS":
                _refuse(args.id, "done", f"No PASS verdict recorded (latest: {t.get('verdict') or 'none'}). Close through `verdict <id> PASS`.", agent)
        t["status"] = "done"
        t["lastActivityAt"] = _now_iso()
        if override:
            t["closed_by_override"] = args.by
        _save_tickets(tickets)
    data = {"via": "override", "by": args.by, "reason": args.reason} if override else {"via": "done"}
    _emit("ticket.closed", ticket=args.id, agent_id=agent, outcome="done", data=data)
    print(f"{args.id}: marked done{' (override by ' + args.by + ')' if override else ''}.")


def main() -> None:
    ap = argparse.ArgumentParser(description="Local ticket/story system (built-in, no external tracker)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_new = sub.add_parser("new", help="create a ticket")
    p_new.add_argument("title")
    p_new.add_argument("--role", default=None, help="role/assignee (engineer, ux, qa, ...)")
    p_new.add_argument("--team", default=None, help="team name")
    p_new.add_argument("--agent", default=None, help="self-reported agent id (event log)")
    p_new.set_defaults(fn=cmd_new)

    p_list = sub.add_parser("list", help="list tickets")
    p_list.add_argument("--status", default="all", choices=["in_review", "done", "all"])
    p_list.set_defaults(fn=cmd_list)

    p_show = sub.add_parser("show", help="show a ticket")
    p_show.add_argument("id")
    p_show.set_defaults(fn=cmd_show)

    p_verdict = sub.add_parser("verdict", help="record a review verdict")
    p_verdict.add_argument("id")
    p_verdict.add_argument("verdict", choices=sorted(VALID_VERDICTS))
    p_verdict.add_argument("--domain", default=None)
    p_verdict.add_argument("--veto-hits", default=None, help="comma-separated veto hits")
    p_verdict.add_argument("--summary", default=None)
    p_verdict.add_argument("--agent", default=None, help="self-reported agent id (event log)")
    p_verdict.set_defaults(fn=cmd_verdict)

    p_clear = sub.add_parser("clear-veto", help="clear an open veto (operator approval required)")
    p_clear.add_argument("id")
    p_clear.add_argument("--by", required=True, help="name of the human clearing the veto")
    p_clear.add_argument("--reason", required=True)
    p_clear.set_defaults(fn=cmd_clear_veto)

    p_done = sub.add_parser("done", help="close a ticket that already has a PASS verdict")
    p_done.add_argument("id")
    p_done.add_argument("--override", action="store_true", help="close without PASS (operator approval required)")
    p_done.add_argument("--by", default=None, help="name of the human overriding")
    p_done.add_argument("--reason", default=None)
    p_done.add_argument("--agent", default=None, help="self-reported agent id (event log)")
    p_done.set_defaults(fn=cmd_done)

    args = ap.parse_args()
    try:
        args.fn(args)
    except Refused as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        sys.exit(2)
    except events.LockTimeout as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()

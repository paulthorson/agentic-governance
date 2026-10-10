#!/usr/bin/env python3
"""
Local ticket/story system for the agentic-governance framework.

A built-in, file-based ticket base so a default install works with NO external
tracker (no Paperclip, no GitHub, no Linear). Since 1.1 it runs the production
chain as an enforced state machine with stuck-ticket recovery
(scripts/chain.py, ADR-0009, ADR-0010). The same store backs the MCP
``ticket_*`` tools, so CLI and MCP agents see one queue.

Files:
  runs/in_review.json   ticket store (watchdog reads tickets whose status is in_review)
  runs/verdicts.jsonl   verdict view (veto-telemetry reads this)
  runs/events.jsonl     append-only event log (record of truth)

Agent loop (one agent, one team, one stage):
  python3 scripts/ticket.py claim --role engineer --team team-a --agent eng-1
  python3 scripts/ticket.py heartbeat T-3 --agent eng-1          # while working
  python3 scripts/ticket.py submit T-3 --agent eng-1 --summary "."

Reviewer loop (a different agent than the worker):
  python3 scripts/ticket.py claim --role engineer --team team-a --agent eng-critic --mode review
  python3 scripts/ticket.py verdict T-3 PASS|KICK_BACK|REVIEW_REQUIRED|ESCALATE --agent eng-critic \\
      [--veto-hits "a,b"] [--to-stage ux] [--summary "."]

Create work:
  python3 scripts/ticket.py new "Title" --queue [--role research] [--end-stage qa] [--team team-a]
  python3 scripts/ticket.py new "Title" [--role engineer]   # pre-1.1: register finished work into review

Recovery (also runs automatically on every claim):
  python3 scripts/ticket.py recover [--alert]   # --alert sends every escalation, veto, and
                                                # stall not yet alerted, wherever it was raised

Human-only (operator approval required, see scripts/approval.py):
  python3 scripts/ticket.py clear-veto <id> --by "Name" --reason "."
  python3 scripts/ticket.py resolve <id> --by "Name" --reason "." [--to-stage pm]
  python3 scripts/ticket.py done <id> --override --by "Name" --reason "."

Read:
  python3 scripts/ticket.py list [--status in_review|done|all] [--state STATE] [--team T]
  python3 scripts/ticket.py show <id>

Exit codes: 0 ok, 1 bad input or unreadable store, 2 refused by governance,
3 lock timeout.

Config (env):
  TICKET_FILE, VERDICT_LOG, EVENT_LOG   file locations (defaults above)
  AG_LEASE_MINUTES, AG_MAX_ATTEMPTS, AG_MAX_KICKBACKS,
  AG_REVIEW_TIMEOUT_MINUTES, AG_QUEUE_TIMEOUT_MINUTES   (see scripts/chain.py)
"""
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chain  # noqa: E402
import events  # noqa: E402
from approval import ApprovalRequired, require_approval  # noqa: E402

REPO_ROOT = Path(os.environ.get("ADVERSARIAL_ROOT", Path(__file__).resolve().parent.parent))
TICKET_FILE = Path(os.environ.get("TICKET_FILE", REPO_ROOT / "runs" / "in_review.json"))
VERDICT_LOG = Path(os.environ.get("VERDICT_LOG", REPO_ROOT / "runs" / "verdicts.jsonl"))
EVENT_LOG = Path(os.environ.get("EVENT_LOG", REPO_ROOT / "runs" / "events.jsonl"))

VALID_VERDICTS = chain.VALID_VERDICTS
Refused = chain.Refused


def _store() -> chain.Store:
    return chain.Store(TICKET_FILE, VERDICT_LOG, EVENT_LOG)


def _load_tickets() -> list[dict]:
    return _store().load()


def _gate(action: str, ident: str):
    """Operator-approval gate for a human-only action. The store calls it
    only after the transition is validated, so a mistyped id or a ticket in
    the wrong state never consumes a one-shot approval. A refusal is logged."""
    def gate() -> None:
        try:
            require_approval(action, REPO_ROOT, consume=True)
        except ApprovalRequired as e:
            raise Refused(str(e), {"kind": "ticket.transition_refused", "ticket": ident,
                                   "outcome": "refused",
                                   "data": {"transition": action, "reason": str(e)}})
    return gate


def _hits(raw: str | None) -> list[str]:
    return [h.strip() for h in raw.split(",") if h.strip()] if raw else []


def _print_ticket(t: dict, prefix: str = "") -> None:
    print(f"{prefix}{t['identifier']} [{t['state']}] stage={t['stage']} team={t.get('team') or '-'}: {t.get('title', '')[:60]}")


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_new(args) -> None:
    queued = bool(getattr(args, "queue", False))
    t = _store().create(args.title, args.role or ("research" if queued else "engineer"),
                        args.team or "", queued=queued,
                        end_stage=getattr(args, "end_stage", None), agent=getattr(args, "agent", None))
    print(f"Created {t['identifier']}: {args.title} (state: {t['state']}, stages: {' > '.join(t['stages'])})")


def cmd_list(args) -> None:
    tickets = _load_tickets()
    if args.status and args.status != "all":
        tickets = [t for t in tickets if t.get("status") == args.status]
    if getattr(args, "state", None):
        tickets = [t for t in tickets if t.get("state") == args.state]
    if getattr(args, "team", None):
        tickets = [t for t in tickets if t.get("team") == args.team]
    if not tickets:
        print("No tickets.")
        return
    for t in tickets:
        _print_ticket(t)


def cmd_show(args) -> None:
    t = next((x for x in _load_tickets() if x.get("identifier") == args.id), None)
    if not t:
        print(f"Ticket {args.id} not found.")
        return
    for k, v in t.items():
        print(f"{k}: {v}")


def cmd_claim(args) -> None:
    t = _store().claim_next(args.role, args.team or "", args.agent, args.mode)
    if t is None:
        print(f"Nothing to {args.mode} for stage={args.role} team={args.team or '-'}.")
        return
    if args.json:
        print(json.dumps(t, indent=2))
    else:
        _print_ticket(t, "Claimed ")
        print(f"Lease expires {t['leaseExpiresAt']}. Heartbeat to extend it.")


def cmd_heartbeat(args) -> None:
    t = _store().heartbeat(args.id, args.agent)
    print(f"{args.id}: lease extended to {t['leaseExpiresAt']}.")


def cmd_submit(args) -> None:
    _store().submit(args.id, args.agent, args.summary or "")
    print(f"{args.id}: submitted for review.")


def cmd_verdict(args) -> None:
    if args.verdict not in VALID_VERDICTS:
        print(f"Invalid verdict {args.verdict}. Choose from: {', '.join(sorted(VALID_VERDICTS))}")
        sys.exit(1)
    try:
        t = _store().verdict(args.id, args.verdict, getattr(args, "agent", None), _hits(args.veto_hits),
                             to_stage=getattr(args, "to_stage", None), summary=args.summary or "",
                             domain=args.domain)
    except KeyError as e:
        print(str(e).strip("'"))
        return
    if t["state"] == "done":
        print(f"{args.id}: PASS, marked done.")
    elif t["state"] == "queued":
        print(f"{args.id}: {args.verdict}, queued at stage {t['stage']}.")
    else:
        print(f"{args.id}: {args.verdict}, now {t['state']}" +
              (f" ({t['escalationReason']})" if t.get("escalationReason") else "") + ".")


def cmd_clear_veto(args) -> None:
    if not args.by or not args.reason:
        print("clear-veto requires --by and --reason.")
        sys.exit(1)
    _store().clear_veto(args.id, args.by, args.reason, gate=_gate("clear_veto", args.id))
    print(f"{args.id}: veto cleared by {args.by}; back in review.")


def cmd_resolve(args) -> None:
    t = _store().resolve(args.id, args.by, args.reason, getattr(args, "to_stage", None),
                         gate=_gate("resolve_escalation", args.id))
    print(f"{args.id}: resolved by {args.by}; queued at stage {t['stage']}.")


def cmd_done(args) -> None:
    override = bool(getattr(args, "override", False))
    agent = getattr(args, "agent", None)
    if override:
        if not getattr(args, "by", None) or not getattr(args, "reason", None):
            print("--override requires --by and --reason.")
            sys.exit(1)
    try:
        t = _store().close(args.id, override=override, by=getattr(args, "by", None),
                           reason=getattr(args, "reason", None), agent=agent,
                           gate=_gate("ticket_done_override", args.id) if override else None)
    except KeyError as e:
        print(str(e).strip("'"))
        return
    if override and t.get("closed_by_override"):
        print(f"{args.id}: marked done (override by {args.by}).")
    else:
        print(f"{args.id}: already done.")


URGENT_KINDS = ("ticket.escalated", "ticket.blocked", "ticket.stalled", "ticket.awaiting_human")
ALERT_STATE = Path(os.environ.get("TICKET_ALERT_STATE", REPO_ROOT / "runs" / "ticket-alerts-state.json"))


def _describe(e: dict) -> str:
    d = e.get("data", {})
    detail = (d.get("message") or d.get("reason")
              or (", ".join(d["veto_hits"]) if d.get("veto_hits") else "")
              or f"{d.get('mode', '')} attempt {d.get('attempt', '')}".strip())
    return f"{e['kind']} {e['ticket']} stage={e.get('role')}: {detail}"


def _unalerted(evs: list[dict]) -> tuple[list[dict], dict]:
    """Urgent events not yet alerted. The watermark lives in a state file,
    so escalations raised during a claim or a verdict (not only during this
    recover call) still reach the operator."""
    try:
        state = json.loads(ALERT_STATE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        state = {}
    mark = state.get("ts", 0)
    seen = set(state.get("ids_at_ts", []))
    new = [e for e in evs if e["kind"] in URGENT_KINDS
           and (e["ts"] > mark or (e["ts"] == mark and e["event_id"] not in seen))]
    if new:
        top = max(e["ts"] for e in new)
        ids = {e["event_id"] for e in new if e["ts"] == top}
        state = {"ts": top, "ids_at_ts": sorted(ids | (seen if top == mark else set()))}
    return new, state


def cmd_recover(args) -> None:
    evs = _store().recover()
    for e in evs:
        print(_describe(e))
    if not evs:
        print("Nothing stuck.")
    if args.alert:
        from messaging import send_alert
        new, state = _unalerted(events.read_events(EVENT_LOG, strict=False))
        if not new:
            return
        if send_alert("Tickets need attention:\n" + "\n".join(_describe(e) for e in new)):
            ALERT_STATE.parent.mkdir(parents=True, exist_ok=True)
            ALERT_STATE.write_text(json.dumps(state), encoding="utf-8")
        else:
            print("WARN: alert not delivered (check network permission / approval); will retry next run.",
                  file=sys.stderr)


def main() -> None:
    ap = argparse.ArgumentParser(description="Local ticket system and chain state machine")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("new", help="create a ticket")
    p.add_argument("title")
    p.add_argument("--role", default=None, help="starting stage (research, pm, ux, engineer, qa, or any domain)")
    p.add_argument("--team", default=None)
    p.add_argument("--queue", action="store_true", help="queue for agents to claim (chain ticket)")
    p.add_argument("--end-stage", dest="end_stage", default=None, help="last chain stage (default qa)")
    p.add_argument("--agent", default=None, help="self-reported agent id")
    p.set_defaults(fn=cmd_new)

    p = sub.add_parser("list", help="list tickets")
    p.add_argument("--status", default="all",
                   choices=["all", "in_review", "done", "queued", "working", "blocked", "escalated"])
    p.add_argument("--state", default=None, choices=list(chain.STATES))
    p.add_argument("--team", default=None)
    p.set_defaults(fn=cmd_list)

    p = sub.add_parser("show", help="show a ticket")
    p.add_argument("id")
    p.set_defaults(fn=cmd_show)

    p = sub.add_parser("claim", help="claim the next ticket for a stage and team")
    p.add_argument("--role", required=True)
    p.add_argument("--team", default="")
    p.add_argument("--agent", required=True)
    p.add_argument("--mode", default="work", choices=["work", "review"])
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_claim)

    p = sub.add_parser("heartbeat", help="extend a claim's lease")
    p.add_argument("id")
    p.add_argument("--agent", required=True)
    p.set_defaults(fn=cmd_heartbeat)

    p = sub.add_parser("submit", help="submit claimed work for review")
    p.add_argument("id")
    p.add_argument("--agent", required=True)
    p.add_argument("--summary", default=None)
    p.set_defaults(fn=cmd_submit)

    p = sub.add_parser("verdict", help="record a review verdict")
    p.add_argument("id")
    p.add_argument("verdict", choices=sorted(VALID_VERDICTS))
    p.add_argument("--domain", default=None, help="adversary domain (default: the ticket's stage)")
    p.add_argument("--veto-hits", default=None, help="comma-separated veto hits")
    p.add_argument("--to-stage", dest="to_stage", default=None, help="KICK_BACK target (this stage or earlier)")
    p.add_argument("--summary", default=None)
    p.add_argument("--agent", required=True, help="reviewer agent id (must hold the review claim)")
    p.set_defaults(fn=cmd_verdict)

    p = sub.add_parser("recover", help="release expired claims, escalate repeat failures, flag stalls")
    p.add_argument("--alert", action="store_true",
                   help="send unalerted escalations, vetoes, and stalls via scripts/messaging.py")
    p.set_defaults(fn=cmd_recover)

    p = sub.add_parser("clear-veto", help="clear an open veto (operator approval required)")
    p.add_argument("id")
    p.add_argument("--by", required=True)
    p.add_argument("--reason", required=True)
    p.set_defaults(fn=cmd_clear_veto)

    p = sub.add_parser("resolve", help="return an escalated ticket to a queue (operator approval required)")
    p.add_argument("id")
    p.add_argument("--by", required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--to-stage", dest="to_stage", default=None)
    p.set_defaults(fn=cmd_resolve)

    p = sub.add_parser("done", help="close a ticket (only via --override; normal closes come from PASS)")
    p.add_argument("id")
    p.add_argument("--override", action="store_true")
    p.add_argument("--by", default=None)
    p.add_argument("--reason", default=None)
    p.add_argument("--agent", default=None)
    p.set_defaults(fn=cmd_done)

    args = ap.parse_args()
    try:
        args.fn(args)
    except Refused as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        sys.exit(2)
    except events.LockTimeout as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(3)
    except (KeyError, ValueError) as e:
        print(f"ERROR: {str(e).strip(chr(39))}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

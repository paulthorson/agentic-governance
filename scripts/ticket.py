#!/usr/bin/env python3
"""
Local ticket/story system for the agentic-governance framework.

A built-in, file-based ticket base so a vanilla install works with NO external
tracker (no Paperclip, no GitHub, no Linear). It gives a team a simple way to:

  - create work items (epics/stories) that flow through the review chain
  - track their state (draft -> in_review -> verdict -> done)
  - feed the stuck-review-watchdog (writes runs/in_review.json)
  - feed the veto-telemetry (writes runs/verdicts.jsonl)

This is the "local ticket base" for teams that don't use Paperclip (ADR-0007).
The watchdog reads runs/in_review.json via `--source file`, and telemetry reads
runs/verdicts.jsonl, so the whole loop works out of the box.

Usage:
  python3 scripts/ticket.py new "Title" [--role engineer] [--team team-a]
  python3 scripts/ticket.py list [--status in_review|done|all]
  python3 scripts/ticket.py verdict <id> PASS|KICK_BACK|REVIEW_REQUIRED [--domain ux] [--veto-hits "a,b"] [--summary "."]
  python3 scripts/ticket.py done <id>
  python3 scripts/ticket.py show <id>

Config (env):
  TICKET_FILE   path to the in_review ledger (default: runs/in_review.json)
  VERDICT_LOG   path to the verdict ledger (default: runs/verdicts.jsonl)
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TICKET_FILE = Path(os.environ.get("TICKET_FILE", REPO_ROOT / "runs" / "in_review.json"))
VERDICT_LOG = Path(os.environ.get("VERDICT_LOG", REPO_ROOT / "runs" / "verdicts.jsonl"))

VALID_VERDICTS = {"PASS", "KICK_BACK", "REVIEW_REQUIRED", "ESCALATE"}

def _load_tickets() -> list[dict]:
    if not TICKET_FILE.exists():
        return []
    try:
        data = json.loads(TICKET_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []

def _save_tickets(tickets: list[dict]) -> None:
    TICKET_FILE.parent.mkdir(parents=True, exist_ok=True)
    TICKET_FILE.write_text(json.dumps(tickets, indent=2), encoding="utf-8")

def _next_id(tickets: list[dict]) -> str:
    # Highest numeric suffix + 1, e.g. T-1, T-2, .
    nums = []
    for t in tickets:
        ident = t.get("identifier", "")
        if ident.startswith("T-") and ident[2:].isdigit():
            nums.append(int(ident[2:]))
    return f"T-{(max(nums) + 1) if nums else 1}"

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def cmd_new(args) -> None:
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
    }
    tickets.append(ticket)
    _save_tickets(tickets)
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
    tickets = _load_tickets()
    t = next((x for x in tickets if x.get("identifier") == args.id), None)
    if not t:
        print(f"Ticket {args.id} not found.")
        return
    for k, v in t.items():
        print(f"{k}: {v}")

def cmd_verdict(args) -> None:
    if args.verdict not in VALID_VERDICTS:
        print(f"Invalid verdict {args.verdict}. Choose from: {', '.join(sorted(VALID_VERDICTS))}")
        sys.exit(1)
    tickets = _load_tickets()
    t = next((x for x in tickets if x.get("identifier") == args.id), None)
    if not t:
        print(f"Ticket {args.id} not found.")
        return
    # Record the verdict in the verdict ledger (telemetry reads this).
    record = {
        "kind": "verdict",
        "domain": args.domain or t.get("role", "unknown"),
        "verdict": args.verdict,
        "veto_triggered": bool(args.veto_hits),
        "veto_hits": [h.strip() for h in args.veto_hits.split(",")] if args.veto_hits else [],
        "ticket": args.id,
        "summary": args.summary or "",
        "ts": int(time.time() * 1000),
    }
    VERDICT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with VERDICT_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    # If KICK_BACK or ESCALATE, keep in_review (still needs work). If PASS, mark done.
    if args.verdict == "PASS":
        t["status"] = "done"
        t["verdict"] = "PASS"
        t["lastActivityAt"] = _now_iso()
        _save_tickets(tickets)
        print(f"{args.id}: PASS — marked done.")
    else:
        t["verdict"] = args.verdict
        t["lastActivityAt"] = _now_iso()
        _save_tickets(tickets)
        print(f"{args.id}: {args.verdict} — still in_review (needs rework).")

def cmd_done(args) -> None:
    tickets = _load_tickets()
    t = next((x for x in tickets if x.get("identifier") == args.id), None)
    if not t:
        print(f"Ticket {args.id} not found.")
        return
    t["status"] = "done"
    t["lastActivityAt"] = _now_iso()
    _save_tickets(tickets)
    print(f"{args.id}: marked done.")

def main() -> None:
    ap = argparse.ArgumentParser(description="Local ticket/story system (vanilla, no external tracker)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_new = sub.add_parser("new", help="create a ticket")
    p_new.add_argument("title")
    p_new.add_argument("--role", default=None, help="role/assignee (engineer, ux, qa, .)")
    p_new.add_argument("--team", default=None, help="team name")
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
    p_verdict.set_defaults(fn=cmd_verdict)

    p_done = sub.add_parser("done", help="mark a ticket done")
    p_done.add_argument("id")
    p_done.set_defaults(fn=cmd_done)

    args = ap.parse_args()
    args.fn(args)

if __name__ == "__main__":
    main()

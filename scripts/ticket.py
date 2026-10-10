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
3 lock timeout, 4 tamper detected / missing key / doctor failure,
5 commit logged but not yet applied (do not retry).

Identity (ADR-0011) and integrity (ADR-0012):
  python3 scripts/ticket.py agent add eng-1 --team team-a --roles engineer --principal runtime-a  (approval)
  python3 scripts/ticket.py agent revoke eng-1                                                    (approval)
  python3 scripts/ticket.py agent list
  python3 scripts/ticket.py integrity init-key                                                     (approval)
  python3 scripts/ticket.py integrity accept --by "Name" --reason "."                             (approval)
  python3 scripts/ticket.py verify
  python3 scripts/ticket.py doctor
  Once any agent is registered, agent commands need --token or AG_AGENT_TOKEN.

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
import identity  # noqa: E402
import integrity  # noqa: E402
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


def _token(args) -> str | None:
    return getattr(args, "token", None) or os.environ.get("AG_AGENT_TOKEN") or None


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
                        end_stage=getattr(args, "end_stage", None), agent=getattr(args, "agent", None),
                        token=_token(args),
                        gate=None if queued else _gate("create_in_review", "new"))
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
    t = _store().claim_next(args.role, args.team or "", args.agent, args.mode, token=_token(args))
    if t is None:
        print(f"Nothing to {args.mode} for stage={args.role} team={args.team or '-'}.")
        return
    if args.json:
        print(json.dumps(t, indent=2))
    else:
        _print_ticket(t, "Claimed ")
        print(f"Lease expires {t['leaseExpiresAt']}. Heartbeat to extend it.")


def cmd_heartbeat(args) -> None:
    t = _store().heartbeat(args.id, args.agent, token=_token(args))
    print(f"{args.id}: lease extended to {t['leaseExpiresAt']}.")


def cmd_submit(args) -> None:
    _store().submit(args.id, args.agent, args.summary or "", token=_token(args))
    print(f"{args.id}: submitted for review.")


def cmd_verdict(args) -> None:
    if args.verdict not in VALID_VERDICTS:
        print(f"Invalid verdict {args.verdict}. Choose from: {', '.join(sorted(VALID_VERDICTS))}")
        sys.exit(1)
    try:
        t = _store().verdict(args.id, args.verdict, getattr(args, "agent", None), _hits(args.veto_hits),
                             to_stage=getattr(args, "to_stage", None), summary=args.summary or "",
                             domain=args.domain, token=_token(args))
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
    tamper = None
    try:
        evs = _store().recover()
    except integrity.TamperDetected as e:
        tamper, evs = e, []
    for e in evs:
        print(_describe(e))
    if not evs and not tamper:
        print("Nothing stuck.")
    if args.alert:
        from messaging import send_alert
        new, state = _unalerted(events.read_events(EVENT_LOG, strict=False))
        ok, lines = _verify_report()
        problems = [] if ok else [l for l in lines if l.startswith("PROBLEM")]
        if new or problems:
            body = []
            if problems:
                body.append("INTEGRITY (writes stopped until an operator runs `ticket.py integrity accept`):")
                body.extend(problems)
            if new:
                body.append("Tickets need attention:")
                body.extend(_describe(e) for e in new)
            if send_alert("\n".join(body)):
                if new:
                    ALERT_STATE.parent.mkdir(parents=True, exist_ok=True)
                    ALERT_STATE.write_text(json.dumps(state), encoding="utf-8")
            else:
                print("WARN: alert not delivered (check network permission / approval); will retry next run.",
                      file=sys.stderr)
    if tamper:
        raise tamper


def _verify_report() -> tuple[bool, list[str]]:
    """Full check. Runs under the ticket lock so a commit landing mid-check
    is never reported as tampering."""
    lines: list[str] = []
    ok = True
    key = integrity.load_key()
    store = _store()
    with events.file_lock(store.ticket_file):
        rep = integrity.verify_log(EVENT_LOG, key)
        head = None
        try:
            head = integrity.read_head(store.head_file, key)
        except integrity.TamperDetected as e:
            ok = False
            lines.append(f"PROBLEM head record: {e}")
        try:
            store.check_integrity(repair=False)
            store_line = "ticket store: matches the last commit"
        except integrity.TamperDetected as e:
            ok = False
            store_line = f"PROBLEM ticket store: {e}"
    lines.insert(0, f"event log: {rep['events']} events, {rep['chained']} chained"
                 + (f", {rep['unverifiable']} keyed but no key to check" if rep["unverifiable"] else ""))
    accepted = (head or {}).get("accepted_problems", [])
    for prob in rep["problems"]:
        if prob in accepted:
            lines.append(f"accepted earlier: {prob}")
        else:
            ok = False
            lines.append(f"PROBLEM {prob}")
    lines.extend(f"note: {n}" for n in rep.get("notes", []))
    lines.append(store_line)
    lines.append(f"mode: {'keyed (hmac-sha256)' if key else 'unkeyed (sha256): detects edits, not a forger'}")
    return ok, lines


def cmd_verify(args) -> None:
    ok, lines = _verify_report()
    for line in lines:
        print(line)
    if not ok:
        sys.exit(4)


def cmd_agent(args) -> None:
    reg = identity.Registry()
    if args.action == "list":
        rows = reg._load()
        if not rows:
            print("No registered agents. Identity is NOT enforced (agent ids are self-reported).")
            return
        print(f"Identity enforced: {reg.enforced()}")
        for r in rows:
            state = "revoked" if r.get("revoked_at") else "active"
            print(f"{r['agent_id']:20} {state:8} team={r.get('team') or '-'} principal={r.get('principal')} roles={','.join(r.get('roles', []))}")
        return
    if not args.id:
        print("agent add/revoke needs an agent id.")
        sys.exit(1)
    try:
        require_approval(f"agent_{args.action}", REPO_ROOT, consume=True)
    except ApprovalRequired as e:
        raise Refused(str(e))
    if args.action == "add":
        if not args.roles or not args.principal:
            print("agent add needs --roles and --principal.")
            sys.exit(1)
        token = reg.add(args.id, args.team or "", args.roles.split(","), args.principal)
        events.emit("agent.registered", path=EVENT_LOG, agent_id=args.id, outcome="registered",
                    data={"team": args.team or "", "roles": args.roles.split(","), "principal": args.principal})
        print(f"Registered {args.id}. Token (shown once, store it in that agent's secret config):")
        print(token)
    else:
        reg.revoke(args.id)
        events.emit("agent.revoked", path=EVENT_LOG, agent_id=args.id, outcome="revoked")
        print(f"Revoked {args.id}.")


def cmd_integrity(args) -> None:
    if args.action == "init-key":
        if integrity.load_key():
            print("An integrity key is already configured.")
            return
        ok, lines = _verify_report()
        if not ok:
            for line in lines:
                print(line)
            raise Refused("Keying needs a clean `ticket.py verify` (or accepted problems) first.")
        store = _store()
        with events.file_lock(store.ticket_file):
            store.check_integrity(repair=True)  # apply any pending commit before re-signing
            try:
                require_approval("integrity_init_key", REPO_ROOT, consume=True)
            except ApprovalRequired as e:
                raise Refused(str(e))
            path = integrity.create_key()
            key = integrity.load_key()
            digest = integrity.file_digest(store.ticket_file)
            ev, offset = events.emit_at("store.integrity_keyed", path=EVENT_LOG, outcome="keyed",
                                        data={"state_digest": digest})
            prior = (integrity.read_head(store.head_file, None) or {}).get("accepted_problems", [])
            integrity.write_head(offset, ev["hash"], digest, store.head_file, key, prior,
                                 store._identity_enforced())
        print(f"Created {path} (0600). The log and head are keyed from here on.")
        print("Keep this file away from agents: see docs/deployment-hardened.md.")
        return
    # accept
    if not args.by or not args.reason:
        print("integrity accept needs --by and --reason.")
        sys.exit(1)
    ok, lines = _verify_report()
    if ok:
        print("Integrity check passes; nothing to accept.")
        return
    rep = integrity.verify_log(EVENT_LOG, integrity.load_key())
    store = _store()
    try:
        prior = (integrity.read_head(store.head_file, integrity.load_key()) or {}).get("accepted_problems", [])
    except integrity.TamperDetected:
        prior = []
    res = store.accept_current_state(args.by, args.reason, gate=_gate("integrity_accept", "store"),
                                     accepted_problems=integrity.unaccepted(rep["problems"], prior))
    print(f"Accepted current state as the new baseline ({res['store_digest'][:12]}). Recorded who and why.")


def cmd_doctor(args) -> None:
    """Report how much of the governance is actually enforced on this install."""
    import stat
    findings = []

    def add(level, msg):
        findings.append((level, msg))

    reg = identity.Registry()
    try:
        add("OK" if reg.enforced() else "WARN",
            "agent identity enforced" if reg.enforced() else
            "no agent registry: agent ids are self-reported (ticket.py agent add)")
    except identity.IdentityError as e:
        add("FAIL", str(e))
    add("OK" if integrity.load_key() else "WARN",
        "integrity key configured" if integrity.load_key() else
        "no integrity key: tamper detection catches edits, not a deliberate forger (ticket.py integrity init-key)")
    for label, path in (("integrity key", integrity.key_path()), ("agent registry", identity.registry_path())):
        if path.exists() and os.name == "posix":
            mode = path.stat().st_mode
            if mode & (stat.S_IRGRP | stat.S_IROTH | stat.S_IWGRP | stat.S_IWOTH):
                add("FAIL", f"{label} {path} is group/world accessible (chmod 600)")
    for path in (TICKET_FILE.parent,):
        if path.exists() and os.name == "posix" and path.stat().st_mode & (stat.S_IWGRP | stat.S_IWOTH):
            add("FAIL", f"{path} is group/world writable")
    ok, _ = _verify_report()
    add("OK" if ok else "FAIL", "log chain and ticket store verify" if ok else "integrity problems: run ticket.py verify")
    add("INFO", "file writes by agents running as this OS user cannot be prevented in code; "
                "see docs/deployment-hardened.md for the separate-user setup")
    for level, msg in findings:
        print(f"[{level:4}] {msg}")
    if any(level == "FAIL" for level, _ in findings):
        sys.exit(4)


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
    p.add_argument("--token", default=None)
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
    p.add_argument("--agent", default=None)
    p.add_argument("--mode", default="work", choices=["work", "review"])
    p.add_argument("--token", default=None, help="agent token (default: AG_AGENT_TOKEN)")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_claim)

    p = sub.add_parser("heartbeat", help="extend a claim's lease")
    p.add_argument("id")
    p.add_argument("--agent", default=None)
    p.add_argument("--token", default=None)
    p.set_defaults(fn=cmd_heartbeat)

    p = sub.add_parser("submit", help="submit claimed work for review")
    p.add_argument("id")
    p.add_argument("--agent", default=None)
    p.add_argument("--token", default=None)
    p.add_argument("--summary", default=None)
    p.set_defaults(fn=cmd_submit)

    p = sub.add_parser("verdict", help="record a review verdict")
    p.add_argument("id")
    p.add_argument("verdict", choices=sorted(VALID_VERDICTS))
    p.add_argument("--domain", default=None, help="adversary domain (default: the ticket's stage)")
    p.add_argument("--veto-hits", default=None, help="comma-separated veto hits")
    p.add_argument("--to-stage", dest="to_stage", default=None, help="KICK_BACK target (this stage or earlier)")
    p.add_argument("--summary", default=None)
    p.add_argument("--agent", default=None, help="reviewer agent id (must hold the review claim); "
                                                 "with a registry, the token decides it")
    p.add_argument("--token", default=None)
    p.set_defaults(fn=cmd_verdict)

    p = sub.add_parser("verify", help="check the event log chain and the ticket store against the last commit")
    p.set_defaults(fn=cmd_verify)

    p = sub.add_parser("doctor", help="report what is and is not enforced on this install")
    p.set_defaults(fn=cmd_doctor)

    p = sub.add_parser("agent", help="manage the agent registry (add/revoke need operator approval)")
    p.add_argument("action", choices=["add", "revoke", "list"])
    p.add_argument("id", nargs="?")
    p.add_argument("--team", default="")
    p.add_argument("--roles", default=None, help="comma-separated: stages to work and review:<stage> to review")
    p.add_argument("--principal", default=None, help="who runs this agent; reviewer and worker must differ")
    p.set_defaults(fn=cmd_agent)

    p = sub.add_parser("integrity", help="init-key, or accept the current state after investigating a tamper report")
    p.add_argument("action", choices=["init-key", "accept"])
    p.add_argument("--by", default=None)
    p.add_argument("--reason", default=None)
    p.set_defaults(fn=cmd_integrity)

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
    except chain.CommitPending as e:
        print(f"PENDING: {e}", file=sys.stderr)
        sys.exit(5)
    except integrity.KeyRequired as e:
        print(f"ERROR: {e}. Run with the integrity key configured.", file=sys.stderr)
        sys.exit(4)
    except integrity.TamperDetected as e:
        print(f"TAMPER: {e}. All writes are stopped. Run `ticket.py verify`, investigate, then "
              f"`ticket.py integrity accept --by NAME --reason ...` (operator approval).", file=sys.stderr)
        sys.exit(4)
    except (KeyError, ValueError) as e:
        print(f"ERROR: {str(e).strip(chr(39))}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

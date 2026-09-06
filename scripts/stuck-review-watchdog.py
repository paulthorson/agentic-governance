#!/usr/bin/env python3
"""
Stuck-review watchdog for the adversarial-agents framework.

Detects `in_review` tickets that have been sitting without a verdict for too
long — the assigned adversary agent is down, paused, or stalled. Alerts via
Discord so a human can intervene before the pipeline silently stalls.

Logic:
  1. Query Paperclip for all `in_review` issues.
  2. For each, compute how long since `lastActivityAt` (or `updatedAt`).
  3. If older than the staleness threshold, it is stuck.
  4. Alert (Discord) for each stuck ticket, unless already alerted recently
     (dedupe via a state file).

Usage:
  python3 scripts/stuck-review-watchdog.py [--stale-minutes 120] [--dry-run]
  python3 scripts/stuck-review-watchdog.py --json [--stale-minutes 120] [--dry-run]

Machine-parseable output:
  With `--json` (or `--format json`), the watchdog emits a single, versioned
  JSON document to stdout for the whole run. The human-readable report remains
  the default and is byte-for-byte unchanged when the flag is absent. See
  scripts/stuck-review-watchdog.schema.md for the schema reference.

Config (env):
  PAPERCLIP_COMPANY_ID   company id (default: auto-detect)
  DISCORD_WEBHOOK_URL    webhook for alerts (optional; falls back to post-to-discord.py)
  STUCK_STATE_FILE       path to dedupe state (default: runs/stuck-watchdog.json)
"""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Shared messaging: sends alerts to the operator's configured channel
# (discord/whatsapp/imessage/generic), set by the setup wizard.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from messaging import send_alert # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = Path(os.environ.get("STUCK_STATE_FILE", REPO_ROOT / "runs" / "stuck-watchdog.json"))

# Version of the machine-parseable JSON schema. Bump when the emitted shape
# changes; consumers must treat an unknown version as incompatible.
SCHEMA_VERSION = "1"

# Adversary agents by id (the reviewers that should clear in_review tickets).
# If a ticket is in_review and assigned to one of these, it is waiting on a verdict.
ADVERSARY_AGENT_IDS = {
    "42432a98-9ff2-445b-bd2f-d7aced2ac003": "Adversarial Engineer",
    "4b51f379-66fc-4414-ac19-02b56c2d5e02": "Adversarial QA",
    "efa203bc-ff0e-4d4c-bec5-0324f9f22585": "Adversarial UX",
    "7d798b0e-fdd2-4231-bfd7-e35ee4bbe050": "Adversarial Researcher",
    "d60f5755-af59-49cd-bb94-337521106061": "Adversarial Universal",
    "276d36c5-c1ae-4946-bd48-344734510c3d": "Adversarial Security",
    "390d2d66-6d84-4f89-b55e-54024bbd21ef": "Adversarial Privacy",
    "d5701004-429c-410b-8fcc-15eab4e9217a": "Adversarial Compliance",
    "bf531c06-3198-4522-b3b8-474db019d2b9": "Adversarial Product",
    "60da788b-4f36-4154-899e-72f718f9a3f5": "Adversarial Ops",
    "badc169b-2cd6-4593-8a1d-c5125bb81ebd": "Adversarial Docs",
}

def get_company_id() -> str:
    env = os.environ.get("PAPERCLIP_COMPANY_ID")
    if env:
        return env
    # Auto-detect from the Paperclip instance.
    companies = Path.home() / ".paperclip" / "instances" / "default" / "companies"
    if companies.is_dir():
        entries = [d for d in companies.iterdir() if d.is_dir()]
        if len(entries) == 1:
            return entries[0].name
    raise SystemExit("Could not determine company id. Set PAPERCLIP_COMPANY_ID.")

def query_in_review(company_id: str) -> tuple[list[dict], dict | None]:
    """Query Paperclip for in_review issues via the CLI.

    Returns (issues, error). On success error is None. On failure issues is []
    and error is a machine-readable descriptor {"reason", "message"} so the
    caller can distinguish a genuine empty result from a failed query (F5).
    """
    cmd = [
        "paperclipai", "issue", "list",
        "--company-id", company_id,
        "--status", "in_review",
        "--json",
    ]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"WARN: could not query Paperclip: {e}", file=sys.stderr)
        return [], {"reason": "query_failed", "message": str(e)}
    if out.returncode != 0:
        print(f"WARN: paperclipai issue list failed: {out.stderr.strip()}", file=sys.stderr)
        return [], {"reason": "query_failed", "message": out.stderr.strip()}
    try:
        return json.loads(out.stdout), None
    except json.JSONDecodeError:
        print("WARN: could not parse paperclipai output", file=sys.stderr)
        return [], {"reason": "parse_error", "message": "could not parse paperclipai output"}

def parse_ts(ts: str | None) -> float | None:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None

def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            return {}
    return {}

def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))

def collect_stuck(issues: list[dict], args, now: float, state: dict) -> list[dict]:
    """Return stuck-ticket dicts: identifier, title, reviewer, age_min, reason.

    Shared by the human and JSON paths so the two surfaces cannot drift.
    """
    stale_secs = args.stale_minutes * 60
    stuck = []
    for issue in issues:
        ident = issue.get("identifier", issue.get("id", "?"))
        assignee = issue.get("assigneeAgentId", "")
        last = parse_ts(issue.get("lastActivityAt") or issue.get("updatedAt"))
        if last is None:
            continue
        age_min = (now - last) / 60
        if age_min < args.stale_minutes:
            continue
        reviewer = ADVERSARY_AGENT_IDS.get(assignee, "unknown reviewer")
        # Dedupe: skip if we already alerted for this ticket recently.
        last_alert = state.get(ident)
        if last_alert and (now - last_alert) < stale_secs:
            continue
        stuck.append({
            "identifier": ident,
            "title": issue.get("title", "")[:120],
            "reviewer": reviewer,
            "age_min": round(age_min),
            "reason": f"In in_review for {age_min:.0f} min with no verdict. Adversary may be down/paused.",
        })
    return stuck

def build_report(args, company_id: str) -> dict:
    """Build the machine-parseable JSON report document for the run."""
    now = time.time()
    run = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": "dry_run" if args.dry_run else "alert",
    }
    base = {"schema_version": SCHEMA_VERSION, "run": run}

    issues, err = query_in_review(company_id)
    if err is not None:
        return {**base, "status": "error", "error": err, "tickets": []}
    if not issues:
        return {**base, "status": "ok_no_findings", "tickets": []}
    state = load_state()
    stuck = collect_stuck(issues, args, now, state)
    if not stuck:
        return {**base, "status": "ok_no_findings", "tickets": []}
    return {**base, "status": "ok_with_findings", "tickets": stuck}

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stale-minutes", type=int, default=120,
                    help="in_review tickets older than this are stuck (default 120)")
    ap.add_argument("--dry-run", action="store_true", help="report without alerting")
    ap.add_argument("--json", action="store_true",
                    help="emit a single versioned JSON document to stdout")
    ap.add_argument("--format", choices=["text", "json"], default="text",
                    help="output format; --json is an alias for --format json")
    args = ap.parse_args()

    json_mode = args.json or args.format == "json"

    # Resolve company id. In JSON mode a hard failure emits a structured error
    # document; in the default mode the existing SystemExit behavior is kept.
    try:
        company_id = get_company_id()
    except SystemExit as e:
        if json_mode:
            print(json.dumps({
                "schema_version": SCHEMA_VERSION,
                "run": {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "mode": "dry_run" if args.dry_run else "alert",
                },
                "status": "error",
                "error": {"reason": "hard_failure", "message": str(e)},
                "tickets": [],
            }, indent=2))
            return
        raise

    if json_mode:
        print(json.dumps(build_report(args, company_id), indent=2))
        return

    # ---- human-readable default path (unchanged) ----
    issues, _ = query_in_review(company_id)
    if not issues:
        print("No in_review issues. All clear.")
        return

    now = time.time()
    state = load_state()
    stuck = collect_stuck(issues, args, now, state)

    if not stuck:
        print("No stuck in_review tickets.")
        return

    for t in stuck:
        ident, title, reviewer, age_min = t["identifier"], t["title"], t["reviewer"], t["age_min"]
        line = (
            f"⚠️ **Stuck review: {ident}**\n"
            f"Title: {title[:120]}\n"
            f"Reviewer: {reviewer}\n"
            f"In in_review for {age_min:.0f} min with no verdict.\n"
            f"Adversary may be down/paused — check it."
        )
        print(f"[{'DRY-RUN' if args.dry_run else 'ALERT'}] {ident} ({reviewer}) stuck {age_min:.0f} min")
        if not args.dry_run:
            send_alert(line)
            state[ident] = now

    if not args.dry_run:
        save_state(state)

if __name__ == "__main__":
    main()

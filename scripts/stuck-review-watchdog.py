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

REPO_ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = Path(os.environ.get("STUCK_STATE_FILE", REPO_ROOT / "runs" / "stuck-watchdog.json"))
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")

# Adversary agents by id (the reviewers that should clear in_review tickets).
# If a ticket is in_review and assigned to one of these, it is waiting on a verdict.
ADVERSARY_AGENT_IDS = {
    "42432a98-9ff2-445b-bd2f-d7aced2ac003": "Adversarial Engineer",
    "4b51f379-66fc-4414-ac19-02b56c2d5e02": "Adversarial QA",
    "efa203bc-ff0e-4d4c-bec5-0324f9f22585": "Adversarial UX",
    "7d798b0e-fdd2-4231-bfd7-e35ee4bbe050": "Adversarial Researcher",
    "d60f5755-af59-49cd-bb94-337521106061": "Adversarial Universal",
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

def query_in_review(company_id: str) -> list[dict]:
    """Query Paperclip for in_review issues via the CLI."""
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
        return []
    if out.returncode != 0:
        print(f"WARN: paperclipai issue list failed: {out.stderr.strip()}", file=sys.stderr)
        return []
    try:
        return json.loads(out.stdout)
    except json.JSONDecodeError:
        print("WARN: could not parse paperclipai output", file=sys.stderr)
        return []

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

def alert_discord(message: str) -> None:
    """Send an alert to Discord via webhook or the post-to-discord helper."""
    if DISCORD_WEBHOOK_URL:
        import urllib.request

        payload = json.dumps({"content": message}).encode()
        req = urllib.request.Request(
            DISCORD_WEBHOOK_URL, data=payload, headers={"Content-Type": "application/json"}
        )
        try:
            urllib.request.urlopen(req, timeout=15)
            return
        except Exception as e:
            print(f"WARN: Discord webhook failed: {e}", file=sys.stderr)
            return
    # Fallback: post-to-discord.py helper (channel #briefs).
    helper = REPO_ROOT.parent / ".openclaw" / "workspace" / "scripts" / "post-to-discord.py"
    if helper.exists():
        try:
            subprocess.run(
                [sys.executable, str(helper), message],
                capture_output=True, text=True, timeout=30,
            )
        except Exception as e:
            print(f"WARN: post-to-discord failed: {e}", file=sys.stderr)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stale-minutes", type=int, default=120,
                    help="in_review tickets older than this are stuck (default 120)")
    ap.add_argument("--dry-run", action="store_true", help="report without alerting")
    args = ap.parse_args()

    company_id = get_company_id()
    issues = query_in_review(company_id)
    if not issues:
        print("No in_review issues. All clear.")
        return

    now = time.time()
    stale_secs = args.stale_minutes * 60
    state = load_state()
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
        stuck.append((ident, issue.get("title", ""), reviewer, age_min))

    if not stuck:
        print("No stuck in_review tickets.")
        return

    for ident, title, reviewer, age_min in stuck:
        line = (
            f"⚠️ **Stuck review: {ident}**\n"
            f"Title: {title[:120]}\n"
            f"Reviewer: {reviewer}\n"
            f"In in_review for {age_min:.0f} min with no verdict.\n"
            f"Adversary may be down/paused — check it."
        )
        print(f"[{'DRY-RUN' if args.dry_run else 'ALERT'}] {ident} ({reviewer}) stuck {age_min:.0f} min")
        if not args.dry_run:
            alert_discord(line)
            state[ident] = now

    if not args.dry_run:
        save_state(state)

if __name__ == "__main__":
    main()

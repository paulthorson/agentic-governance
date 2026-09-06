#!/usr/bin/env python3
"""
Veto telemetry for the adversarial-agents framework.

Scans the verdict ledger (runs/verdicts.jsonl) for constitutional veto hits and
alerts when a veto fires. This is the "telemetry / alerting on vetoes" roadmap
item: a veto is the framework's strongest signal, and a veto that fires silently
is a veto that might as well not exist.

Usage:
  python3 scripts/veto-telemetry.py [--days 1] [--json] [--dry-run]
  python3 scripts/veto-telemetry.py --watch   # alert on new vetoes since last run

Config (env):
  VERDICT_LOG          path to the verdict ledger (default: runs/verdicts.jsonl)
  DISCORD_WEBHOOK_URL  webhook for alerts (optional; falls back to post-to-discord.py)
  VETO_STATE_FILE      state file for --watch dedupe (default: runs/veto-telemetry-state.json)
"""
import argparse
import json
import os
import sys
import time
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VERDICT_LOG = Path(os.environ.get("VERDICT_LOG", REPO_ROOT / "runs" / "verdicts.jsonl"))
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")
VETO_STATE_FILE = Path(os.environ.get("VETO_STATE_FILE", REPO_ROOT / "runs" / "veto-telemetry-state.json"))

def load_verdicts(days: int) -> list[dict]:
    if not VERDICT_LOG.exists():
        return []
    cutoff = (datetime.now(timezone.utc).timestamp() - days * 86400) * 1000
    rows = []
    for line in VERDICT_LOG.read_text().splitlines():
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if r.get("ts", 0) < cutoff:
            continue
        rows.append(r)
    return rows

def veto_events(rows: list[dict]) -> list[dict]:
    """Extract veto events: verdicts where a constitutional veto triggered."""
    events = []
    for r in rows:
        if r.get("veto_triggered") or r.get("veto_hits"):
            events.append({
                "ts": r.get("ts"),
                "domain": r.get("domain", "unknown"),
                "verdict": r.get("verdict", "?"),
                "veto_hits": r.get("veto_hits", []),
                "ticket": r.get("ticket", ""),
                "rule": r.get("rule", ""),
                "case_tag": r.get("case_tag", ""),
            })
    return events

def alert_discord(message: str) -> None:
    """Send an alert to Discord via webhook or the post-to-discord helper."""
    if DISCORD_WEBHOOK_URL:
        try:
            payload = json.dumps({"content": message}).encode("utf-8")
            req = urllib.request.Request(
                DISCORD_WEBHOOK_URL, data=payload,
                headers={"Content-Type": "application/json"},
            )
            urllib.request.urlopen(req, timeout=10)
            return
        except Exception as e:
            print(f"WARN: Discord webhook failed: {e}", file=sys.stderr)
    # Fallback: post-to-discord.py helper.
    helper = REPO_ROOT.parent / ".openclaw" / "workspace" / "scripts" / "post-to-discord.py"
    if helper.exists():
        try:
            import subprocess
            subprocess.run([sys.executable, str(helper), message], check=False)
            return
        except Exception as e:
            print(f"WARN: post-to-discord failed: {e}", file=sys.stderr)
    print(f"ALERT (no delivery): {message}")

def _load_state() -> dict:
    if not VETO_STATE_FILE.exists():
        return {}
    try:
        return json.loads(VETO_STATE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}

def _save_state(state: dict) -> None:
    VETO_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    VETO_STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=1, help="look back window (default 1 day)")
    ap.add_argument("--json", action="store_true", help="emit JSON to stdout")
    ap.add_argument("--dry-run", action="store_true", help="report without alerting")
    ap.add_argument("--watch", action="store_true", help="alert only on new vetoes since last run")
    args = ap.parse_args()

    rows = load_verdicts(args.days)
    events = veto_events(rows)

    if args.watch:
        # Dedupe: only alert on vetoes not seen in the last run.
        state = _load_state()
        seen = set(state.get("seen", []))
        new_events = [e for e in events if e.get("ts") not in seen]
        if new_events:
            for e in new_events:
                msg = (
                    f"🚨 **VETO** [{e['domain']}] {e['verdict']} "
                    f"ticket={e['ticket'] or '?'} rule={e['rule'] or '?'} "
                    f"hits={', '.join(e['veto_hits']) or 'none'}"
                )
                if not args.dry_run:
                    alert_discord(msg)
                else:
                    print(f"[DRY-RUN] {msg}")
            state["seen"] = sorted({e.get("ts") for e in events})
            _save_state(state)
        else:
            print("No new vetoes since last run.")
        return

    report = {
        "window_days": args.days,
        "total_verdicts": len(rows),
        "veto_events": len(events),
        "veto_rate": round(len(events) / len(rows), 3) if rows else 0,
        "by_domain": dict(Counter(e["domain"] for e in events)),
        "top_veto_hits": Counter(
            h for e in events for h in e["veto_hits"]
        ).most_common(5),
    }

    if args.json:
        print(json.dumps(report, indent=2))
        return

    print(f"=== Veto telemetry (last {args.days} days) ===")
    print(f"Total verdicts: {report['total_verdicts']} | veto events: {report['veto_events']} "
          f"({report['veto_rate']:.0%})")
    if report["by_domain"]:
        for d, n in report["by_domain"].items():
            print(f"  [{d}] {n} veto(es)")
    if report["top_veto_hits"]:
        top = ", ".join(f"{k} ({n})" for k, n in report["top_veto_hits"])
        print(f"  top veto hits: {top}")
    else:
        print("  no vetoes recorded in window.")

if __name__ == "__main__":
    main()

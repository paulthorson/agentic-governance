#!/usr/bin/env python3
"""
Calibration automation for the adversarial-agents framework.

Analyzes the verdict ledger (runs/verdicts.jsonl) to reveal whether the
adversaries are calibrated: too strict (everything kicked back), too lax
(vetoes missed), or healthy. Produces a summary report.

Usage:
  python3 scripts/calibration-report.py [--days 30] [--json]
"""
import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VERDICT_LOG = Path(os.environ.get("VERDICT_LOG", REPO_ROOT / "runs" / "verdicts.jsonl"))

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

def analyze(rows: list[dict]) -> dict:
    by_domain = defaultdict(list)
    for r in rows:
        by_domain[r.get("domain", "unknown")].append(r)

    report = {"total": len(rows), "domains": {}}
    for domain, dr in sorted(by_domain.items()):
        verdicts = [r.get("verdict", "?") for r in dr]
        counts = Counter(verdicts)
        kick = counts.get("KICK_BACK", 0)
        allow = counts.get("ALLOW", 0)
        total = len(dr)
        kick_rate = kick / total if total else 0
        # Calibration heuristic
        if kick_rate >= 0.8:
            cal = "TOO STRICT — nearly everything kicked back; check for over-inflation"
        elif kick_rate <= 0.1:
            cal = "TOO LAX — nearly everything allowed; check for missed vetoes"
        else:
            cal = "HEALTHY"
        report["domains"][domain] = {
            "total": total,
            "kick_back": kick,
            "allow": allow,
            "kick_rate": round(kick_rate, 2),
            "calibration": cal,
            "veto_hits": Counter(
                v for r in dr for v in r.get("veto_hits", [])
            ).most_common(5),
        }
    return report

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = load_verdicts(args.days)
    report = analyze(rows)

    if args.json:
        print(json.dumps(report, indent=2))
        return

    print(f"=== Calibration report (last {args.days} days) ===")
    print(f"Total verdicts: {report['total']}\n")
    if not report["domains"]:
        print("No verdicts recorded yet. Run reviews to populate the ledger.")
        return
    for domain, d in report["domains"].items():
        print(f"[{domain}] {d['total']} verdicts | kick {d['kick_back']} / allow {d['allow']} "
              f"({d['kick_rate']:.0%} kick) | {d['calibration']}")
        if d["veto_hits"]:
            top = ", ".join(f"{k} ({n})" for k, n in d["veto_hits"])
            print(f"  top veto hits: {top}")

if __name__ == "__main__":
    main()

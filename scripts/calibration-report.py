#!/usr/bin/env python3
"""
Calibration automation for the adversarial-agents framework.

Analyzes the verdict ledger (runs/verdicts.jsonl) to reveal whether the
adversaries are calibrated: too strict (everything kicked back), too lax
(vetoes missed), or healthy. Produces a summary report.

Usage:
  python3 scripts/calibration-report.py [--days 30] [--json]
  python3 scripts/calibration-report.py [--days 30] [--json] --output report.txt

--output <path> writes the report to the given file instead of stdout.
The file is overwritten if it already exists. The parent directory must
already exist. Works with both the text report and --json. The write is
atomic (temp file + rename), so a mid-write failure never leaves a partial
file, and the file output is byte-identical to stdout (including the
trailing newline).
"""
import argparse
import json
import os
import sys
import tempfile
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

def build_text(report: dict, days: int) -> str:
    """Build the human-readable report as a string (with trailing newline)."""
    lines = [f"=== Calibration report (last {days} days) ==="]
    lines.append(f"Total verdicts: {report['total']}\n")
    if not report["domains"]:
        lines.append("No verdicts recorded yet. Run reviews to populate the ledger.")
        return "\n".join(lines) + "\n"
    for domain, d in report["domains"].items():
        lines.append(f"[{domain}] {d['total']} verdicts | kick {d['kick_back']} / allow {d['allow']} "
                     f"({d['kick_rate']:.0%} kick) | {d['calibration']}")
        if d["veto_hits"]:
            top = ", ".join(f"{k} ({n})" for k, n in d["veto_hits"])
            lines.append(f"  top veto hits: {top}")
    return "\n".join(lines) + "\n"

def emit(text: str, output: str | None) -> None:
    """Route output to a file (atomic write) or stdout.

    D1 fix: the file content is byte-identical to stdout (trailing newline
    included). D2 fix: the file is written to a temp file then atomically
    renamed, so a mid-write failure never leaves a partial file.
    Outside-repo writes require operator approval.
    """
    if output is None:
        sys.stdout.write(text)
        return
    out = Path(output)
    scripts_dir = str(Path(__file__).resolve().parent)
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    from approval import ApprovalRequired, is_outside_repo, require_approval

    if is_outside_repo(out, REPO_ROOT):
        try:
            require_approval("outside_write", REPO_ROOT)
        except ApprovalRequired as e:
            print(f"error: {e}", file=sys.stderr)
            sys.exit(1)
    if not out.parent.exists():
        print(f"error: output directory does not exist: {out.parent}", file=sys.stderr)
        sys.exit(1)
    # Atomic write: temp file in the same directory, then rename.
    fd, tmp_path = tempfile.mkstemp(dir=str(out.parent), prefix=".calib-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.replace(tmp_path, out)
    except OSError as e:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        print(f"error: cannot write report to {output}: {e}", file=sys.stderr)
        sys.exit(1)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--output", metavar="PATH",
                    help="write the report to PATH instead of stdout (overwrites existing file)")
    args = ap.parse_args()

    rows = load_verdicts(args.days)
    report = analyze(rows)

    if args.json:
        emit(json.dumps(report, indent=2) + "\n", args.output)
        return

    emit(build_text(report, args.days), args.output)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""CLI stub — Cos memory seating hook (part of AG install when Cos is seated).

The setup wizard calls `apply_at_cos_seating` in
`mcp/adversarial_mcp/cos_memory_setup.py` when a Chief of Staff roster row is
present. This stub re-runs the same hook for operators who need to (re)scaffold
after seating.

Usage:
  python3 scripts/cos_memory_setup.py --mode private_git --label cos-memory-private
  python3 scripts/cos_memory_setup.py --mode local_folder --label desk-cos-memory
  python3 scripts/cos_memory_setup.py --show-prompt

operator + Cos clarified store = private git.
Framework ASK: private_git OR local_folder — do not force.
Keep private operator data out of AG git.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HOOK = REPO_ROOT / "mcp" / "adversarial_mcp" / "cos_memory_setup.py"

def _load_hook():
    """Load seating hook module without importing adversarial_mcp package __init__."""
    spec = importlib.util.spec_from_file_location("cos_memory_setup", HOOK)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load seating hook at {HOOK}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def main(argv: list[str] | None = None) -> int:
    hook = _load_hook()
    parser = argparse.ArgumentParser(
        description=(
            "Cos memory seating hook — runs at AG install/setup when Cos is seated "
            "(same hook the setup wizard must call). Not a deferred README-only step."
        )
    )
    parser.add_argument(
        "--mode",
        choices=hook.COS_MEMORY_MODES,
        help="private_git OR local_folder (framework ASK — do not force one)",
    )
    parser.add_argument(
        "--label",
        help="Short private label only — no host paths, emails, or secrets",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Governance repo root (default: this checkout)",
    )
    parser.add_argument(
        "--show-prompt",
        action="store_true",
        help="Print the seating ASK summary as JSON and exit",
    )
    args = parser.parse_args(argv)

    if args.show_prompt:
        print(json.dumps(hook.seating_prompt_summary(), indent=2))
        return 0

    if not args.mode or not args.label:
        parser.error("--mode and --label are required unless --show-prompt")

    if hook.looks_like_forbidden_memory_label(args.label):
        print(
            "error: label must be a short private name only — "
            "no private operator data",
            file=sys.stderr,
        )
        return 2

    written = hook.apply_at_cos_seating(
        args.repo_root.resolve(),
        args.mode,
        args.label,
        has_cos=True,
    )
    print(
        json.dumps(
            {
                "status": "ok",
                "when": "Cos seating / AG install-setup hook",
                "mode": args.mode,
                "label": args.label,
                "operator_cos_clarified_store": "private_git",
                "force_one_mode": False,
                "wrote": [str(p) for p in written],
            },
            indent=2,
        )
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

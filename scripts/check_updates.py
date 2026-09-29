#!/usr/bin/env python3
"""Check for newer published framework versions.

Runs the opt-in, network-gated update check from
mcp/adversarial_mcp/updates.py and prints a human-readable summary.
Refreshes the status file read by the localhost dashboard
(runs/update-check.json, gitignored).

Opt in with AG_UPDATE_CHECK=allow, or a "## Update checks" section with
"- allow" in config/setup.md. Safe to run from cron: it never raises,
never sends anything anywhere, and does nothing at all unless the
operator opted in AND allows network egress.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_updates():
    import importlib.util

    path = REPO_ROOT / "mcp" / "adversarial_mcp" / "updates.py"
    spec = importlib.util.spec_from_file_location("ag_updates", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load updates module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


updates = _load_updates()


def main() -> int:
    force = "--force" in sys.argv[1:]
    status = updates.check_for_updates(force=force, repo_root=REPO_ROOT)

    if not status.get("checked"):
        print(f"Update check skipped: {status.get('reason')}")
        return 0

    current = status["current_version"]
    latest = status["latest_version"]
    if status.get("update_available"):
        print(f"Update available: {current} -> {latest}")
        print(f"Changelog: {status['changelog_url']}")
        print(f"Releases:  {status['releases_url']}")
    else:
        cached = " (cached)" if status.get("cached") else ""
        print(f"Up to date: framework {current} matches published {latest}{cached}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

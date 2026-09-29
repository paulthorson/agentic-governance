#!/usr/bin/env python3
"""
Smoke-test every MCP tool for every domain, failing loudly on empty/error
results. Regression guard for silent-empty returns — the class of bug where
get_standard returned nothing for nine days and nothing caught it.

Invokes the MCP server's tools in-process (no network, no external LLM).
Exits non-zero (and names the tool + domain) if any covered tool returns an
empty or error result. An empty string is never a pass.

Run: python3 scripts/smoke_test_mcp.py
CI: add to the validation workflow alongside scripts/validate.py
"""

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "mcp"))
sys.path.insert(0, str(REPO_ROOT))
os.environ.setdefault("ADVERSARIAL_ROOT", str(REPO_ROOT))

try:
    from adversarial_mcp import server as mcp_server  # noqa: E402
except ImportError:
    print(
        "SMOKE TEST BLOCKED: the 'mcp' package is not importable under this Python.\n"
        "Run with the repo virtualenv (which has 'mcp' installed):\n"
        f"  {REPO_ROOT / 'mcp' / '.venv' / 'bin' / 'python'} {Path(__file__).resolve()}\n"
        "or install it:  pip install 'mcp<2'"
    )
    sys.exit(1)

def is_empty(value) -> bool:
    """True when a tool result is empty in a way that should never pass."""
    if value is None:
        return True
    if isinstance(value, (str, list, tuple, dict, set)):
        return len(value) == 0
    return False

def fails(value) -> bool:
    """True when a result is empty OR an explicit error sentinel is present."""
    if is_empty(value):
        return True
    blob = str(value).lower()
    # explicit error markers the tools emit instead of raising
    for marker in ("no constitution found", "no standard found",
                   "standard missing", "standard ambiguous"):
        if marker in blob:
            return True
    return False

def main() -> int:
    domains = mcp_server.list_domains()  # derived, not hardcoded
    failures: list[str] = []

    # --- non-domain / whole-system tools (called once) ---
    # list_domains and framework_status must be non-empty. query_verdicts is
    # legitimately empty on a fresh log, so it is checked for errors only (not
    # for non-emptiness) — an empty verdict history is a valid state.
    for name, call in [
        ("list_domains", lambda: mcp_server.list_domains()),
        ("framework_status", lambda: mcp_server.framework_status()),
    ]:
        try:
            if fails(call()):
                failures.append(f"{name} (no domain) returned empty/error")
        except Exception as e:  # noqa: BLE001
            failures.append(f"{name} (no domain) raised: {e}")
    try:
        mcp_server.query_verdicts(limit=5)  # must not raise; empty is valid
    except Exception as e:  # noqa: BLE001
        failures.append(f"query_verdicts (no domain) raised: {e}")

    # --- per-domain tools (all domains) ---
    for d in domains:
        for name, call in [
            ("list_agents", lambda d=d: mcp_server.list_agents(d)),
            ("list_skills", lambda d=d: mcp_server.list_skills(d)),
            ("get_constitution", lambda d=d: mcp_server.get_constitution(d)),
            ("get_standard", lambda d=d: mcp_server.get_standard(d)),
            ("check_veto", lambda d=d: mcp_server.check_veto(d, "test work")),
        ]:
            try:
                if fails(call()):
                    failures.append(f"{name} ({d}) returned empty/error")
            except Exception as e:  # noqa: BLE001
                failures.append(f"{name} ({d}) raised: {e}")

        # get_agent needs a real agent name for this domain; derive from list_agents
        agents = mcp_server.list_agents(d)
        if agents:
            name = agents[0]["name"]
            call = lambda d=d, n=name: mcp_server.get_agent(d, n)
            try:
                if fails(call()):
                    failures.append(f"get_agent ({d}) returned empty/error")
            except Exception as e:  # noqa: BLE001
                failures.append(f"get_agent ({d}) raised: {e}")
        else:
            failures.append(f"get_agent ({d}) skipped — no agents to look up")

        # run_review returns a structured dict (structural scan + prompt, no LLM).
        # Tagged source=smoke_test so its verdict-log records can be filtered out
        # of the real-review log (runs/verdicts.jsonl).
        try:
            res = mcp_server.run_review(d, "smoke test work", source="smoke_test")
            if fails(res):
                failures.append(f"run_review ({d}) returned empty/error")
        except Exception as e:  # noqa: BLE001
            failures.append(f"run_review ({d}) raised: {e}")

    # --- excluded tools (documented) ---
    # run_review_deep: requires an external LLM (Ollama) — would hang/fail
    #   without one; deliberately out of the no-LLM smoke loop.
    # record_verdict: writes a verdict record; not a content-return to smoke.
    # setup_wizard_start/answer: stateful; writes config/wizard-state.json.

    if failures:
        print(f"SMOKE TEST FAILED ({len(failures)} issue(s)):")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"SMOKE TEST PASSED — {len(domains)} domains, all covered tools non-empty")
    return 0

if __name__ == "__main__":
    sys.exit(main())

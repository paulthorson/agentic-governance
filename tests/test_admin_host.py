"""Admin host resolution: Host wins; X-Forwarded-Host only when trust is on."""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROBE = REPO_ROOT / "tests" / "admin_access_probe.mts"
DENY_CASES = ("host-0.0.0.0-denied", "host-0.0.0.0-port-denied")


def _node_major() -> int:
    try:
        out = subprocess.check_output(["node", "-v"], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return 0
    if not out.startswith("v"):
        return 0
    try:
        return int(out[1:].split(".", 1)[0])
    except ValueError:
        return 0


class TestAdminHostResolution(unittest.TestCase):
    def test_resolve_request_host_cases(self):
        major = _node_major()
        self.assertGreaterEqual(
            major,
            22,
            "Admin Host deny coverage requires Node 22+ "
            f"(found {major or 'none'}). Install Node 22 so Host/XFH "
            "fail-closed and unspecified-bind deny probes run.",
        )
        result = subprocess.run(
            ["node", "--experimental-strip-types", "--no-warnings", str(PROBE)],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            0,
            result.stdout + result.stderr,
        )
        cases = json.loads(result.stdout)
        names = {row["name"] for row in cases}
        for required in DENY_CASES:
            self.assertIn(required, names)
        self.assertGreaterEqual(len(cases), 8)
        for row in cases:
            self.assertTrue(row["ok"], row)
        denied = [row for row in cases if row["name"] in DENY_CASES]
        self.assertEqual(len(denied), len(DENY_CASES))
        for row in denied:
            self.assertFalse(row["local"], row)


if __name__ == "__main__":
    unittest.main()

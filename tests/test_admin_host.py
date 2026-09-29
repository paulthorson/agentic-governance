"""Admin host resolution: Host wins; X-Forwarded-Host only when trust is on."""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROBE = REPO_ROOT / "tests" / "admin_access_probe.mts"


class TestAdminHostResolution(unittest.TestCase):
    def test_resolve_request_host_cases(self):
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
        self.assertGreaterEqual(len(cases), 6)
        for row in cases:
            self.assertTrue(row["ok"], row)


if __name__ == "__main__":
    unittest.main()

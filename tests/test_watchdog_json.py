"""Tests for the stuck-review watchdog's machine-parseable JSON output.

Runs the watchdog via subprocess with a fake `paperclipai` CLI on PATH so no
network or external service is needed. Covers the three-state contract, the
conformance of the emitted document, and the default-unchanged regression.

Run:  python3 -m pytest tests/test_watchdog_json.py -q
   or: python3 tests/test_watchdog_json.py
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WATCHDOG = REPO_ROOT / "scripts" / "stuck-review-watchdog.py"

# A reviewer id from ADVERSARY_AGENT_IDS in the watchdog.
ENGINEER_ID = "42432a98-9ff2-445b-bd2f-d7aced2ac003"

FAKE_CLI = textwrap.dedent(
    """\
    #!/usr/bin/env python3
    import json, os, sys
    mode = os.environ.get("WATCHDOG_FIXTURE", "empty")
    if mode == "empty":
        print("[]")
    elif mode == "fresh":
        import datetime
        recent = (datetime.datetime.now(datetime.timezone.utc)
                  - datetime.timedelta(minutes=10)).isoformat()
        print(json.dumps([{
            "identifier": "T-1",
            "title": "Fresh ticket",
            "assigneeAgentId": "%s",
            "lastActivityAt": recent,
        }]))
    elif mode == "stuck":
        print(json.dumps([{
            "identifier": "T-100",
            "title": "A very long title " + "x" * 200,
            "assigneeAgentId": "%s",
            "lastActivityAt": "2026-08-20T00:00:00Z",
        }]))
    elif mode == "fail":
        print("boom", file=sys.stderr)
        sys.exit(1)
    """
) % (ENGINEER_ID, ENGINEER_ID)


class WatchdogJsonTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._bindir = Path(self._tmp.name) / "bin"
        self._bindir.mkdir()
        cli = self._bindir / "paperclipai"
        cli.write_text(FAKE_CLI)
        cli.chmod(0o755)
        self._state = Path(self._tmp.name) / "state.json"
        self._env = dict(os.environ)
        self._env["PAPERCLIP_COMPANY_ID"] = "company-1"
        self._env["STUCK_STATE_FILE"] = str(self._state)
        self._env["PATH"] = str(self._bindir) + os.pathsep + self._env.get("PATH", "")

    def tearDown(self):
        self._tmp.cleanup()

    def run_watchdog(self, fixture, *extra):
        env = dict(self._env)
        env["WATCHDOG_FIXTURE"] = fixture
        return subprocess.run(
            [sys.executable, str(WATCHDOG), *extra],
            capture_output=True, text=True, env=env,
        )

    def test_no_findings_status(self):
        r = self.run_watchdog("empty", "--json")
        self.assertEqual(r.returncode, 0, r.stderr)
        doc = json.loads(r.stdout)
        self.assertEqual(doc["status"], "ok_no_findings")
        self.assertEqual(doc["tickets"], [])
        self.assertEqual(doc["schema_version"], "1")

    def test_with_findings_fields(self):
        r = self.run_watchdog("stuck", "--json", "--dry-run")
        self.assertEqual(r.returncode, 0, r.stderr)
        doc = json.loads(r.stdout)
        self.assertEqual(doc["status"], "ok_with_findings")
        self.assertEqual(doc["run"]["mode"], "dry_run")
        self.assertEqual(len(doc["tickets"]), 1)
        t = doc["tickets"][0]
        self.assertEqual(t["identifier"], "T-100")
        self.assertEqual(t["reviewer"], "Adversarial Engineer")
        self.assertIsInstance(t["age_min"], int)
        self.assertLessEqual(len(t["title"]), 120)
        self.assertTrue(t["reason"])

    def test_query_failure_is_error(self):
        r = self.run_watchdog("fail", "--json")
        self.assertEqual(r.returncode, 0, r.stderr)
        doc = json.loads(r.stdout)
        self.assertEqual(doc["status"], "error")
        self.assertEqual(doc["error"]["reason"], "query_failed")
        self.assertEqual(doc["tickets"], [])

    def test_hard_failure_is_error(self):
        env = dict(self._env)
        env.pop("PAPERCLIP_COMPANY_ID")
        env["WATCHDOG_FIXTURE"] = "empty"
        env["HOME"] = str(Path(self._tmp.name) / "home")
        Path(env["HOME"]).mkdir(exist_ok=True)
        r = subprocess.run(
            [sys.executable, str(WATCHDOG), "--json"],
            capture_output=True, text=True, env=env,
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        doc = json.loads(r.stdout)
        self.assertEqual(doc["status"], "error")
        self.assertEqual(doc["error"]["reason"], "hard_failure")

    def test_three_state_classification(self):
        # A consumer can classify each run from the document alone.
        for fixture, expected in [("empty", "ok_no_findings"),
                                  ("stuck", "ok_with_findings"),
                                  ("fail", "error")]:
            r = self.run_watchdog(fixture, "--json")
            doc = json.loads(r.stdout)
            self.assertEqual(doc["status"], expected, fixture)

    def test_default_path_unchanged_empty(self):
        r = self.run_watchdog("empty")
        self.assertEqual(r.stdout, "No in_review issues. All clear.\n")
        self.assertEqual(r.stderr, "")

    def test_default_path_unchanged_no_stuck(self):
        r = self.run_watchdog("fresh")
        self.assertEqual(r.stdout, "No stuck in_review tickets.\n")
        self.assertEqual(r.stderr, "")

    def test_default_path_stuck_line_format(self):
        r = self.run_watchdog("stuck", "--dry-run")
        self.assertRegex(
            r.stdout,
            r"^\[DRY-RUN\] T-100 \(Adversarial Engineer\) stuck \d+ min\n$",
        )

    def test_format_json_alias(self):
        r = self.run_watchdog("empty", "--format", "json")
        doc = json.loads(r.stdout)
        self.assertEqual(doc["status"], "ok_no_findings")

    def test_schema_version_matches_reference(self):
        ref = (REPO_ROOT / "scripts" / "stuck-review-watchdog.schema.md").read_text()
        r = self.run_watchdog("empty", "--json")
        doc = json.loads(r.stdout)
        self.assertEqual(doc["schema_version"], "1")
        self.assertIn('The current version\nis `"1"`', ref)


if __name__ == "__main__":
    unittest.main(verbosity=2)

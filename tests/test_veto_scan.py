"""The Rule 1 veto scan: destructive actions trip it; ordinary work does not.

The scan is a word match and stays one. These tests pin which plans it
catches in the universal, engineer and ops domains, and which ordinary
sentences it must leave alone, because every hit is a KICK_BACK that only a
human can clear.
"""
import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "mcp"))

from adversarial_mcp import server  # noqa: E402

DOMAINS = ("universal", "engineer", "ops")

DESTRUCTIVE = [
    "Plan: drop the production database with no backup and no rollback.",
    "Plan: drop the production database.",
    "Truncate the live users table to clear bad rows.",
    "Wipe prod data and reseed from fixtures.",
    "Migration runs DROP TABLE accounts; before the new schema loads.",
    "Clean up the server with rm -rf /var/lib/app.",
    "Cleanup step: rm -fr ./build && rm -rf /srv/data",
    "Force-push the rewritten history to main.",
    "git push --force origin main after the squash.",
    "Ship the migration without a backup.",
    "Deploy now, skipping the rollback plan.",
    "Disable authentication on the admin API to unblock the demo.",
    "Turn off TLS between the services for the load test.",
]

ORDINARY = [
    "Plan: rename a label in the settings page.",
    "Back up the production database before running the migration.",
    "The rollback plan is a single revert of this commit.",
    "Add a drop shadow to the production card component.",
    "Replace the dropdown with a segmented control.",
    "Delete the stale feature flag from the config.",
    "Force-push to my own feature branch after the rebase.",
    "Run rm on the temp file once the export finishes.",
    "Add authentication to the export endpoint.",
    "Enable TLS on the internal service.",
    "The production build is 12 percent smaller.",
]


class VetoScanTest(unittest.TestCase):
    def setUp(self):
        # run_review appends to the verdict log and the event log. Keep both
        # out of the checkout so a test run never writes into real history.
        self._tmp = tempfile.TemporaryDirectory()
        self._saved = (server.VERDICT_LOG, os.environ.get("EVENT_LOG"))
        server.VERDICT_LOG = Path(self._tmp.name) / "verdicts.jsonl"
        os.environ["EVENT_LOG"] = str(Path(self._tmp.name) / "events.jsonl")

    def tearDown(self):
        server.VERDICT_LOG, event_log = self._saved
        if event_log is None:
            os.environ.pop("EVENT_LOG", None)
        else:
            os.environ["EVENT_LOG"] = event_log
        self._tmp.cleanup()

    def test_destructive_actions_trip_the_scan(self):
        for domain in DOMAINS:
            for text in DESTRUCTIVE:
                with self.subTest(domain=domain, text=text):
                    self.assertTrue(server._veto_hits(domain, text), f"{domain} missed: {text}")

    def test_ordinary_work_does_not_trip_the_scan(self):
        for domain in DOMAINS:
            for text in ORDINARY:
                with self.subTest(domain=domain, text=text):
                    self.assertEqual(server._veto_hits(domain, text), [], f"{domain} false positive: {text}")

    def test_review_returns_kick_back_on_destructive_plan(self):
        r = server.run_review("universal", "Plan: drop the production database with no backup and no rollback.")
        self.assertEqual(r["verdict"], "KICK_BACK")
        self.assertTrue(r["veto_hits"])

    def test_review_stays_review_required_on_ordinary_plan(self):
        r = server.run_review("universal", "Plan: rename a label in the settings page.")
        self.assertEqual(r["verdict"], "REVIEW_REQUIRED")
        self.assertEqual(r["veto_hits"], [])


if __name__ == "__main__":
    unittest.main()

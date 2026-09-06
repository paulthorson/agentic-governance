"""Tests for the local ticket/story system (scripts/ticket.py).

Covers: creating tickets, listing, recording verdicts, and the watchdog +
telemetry integration (ADR-0007 vanilla ticket base).

Run:  python3 -m pytest tests/test_ticket.py -q
"""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TICKET = REPO_ROOT / "scripts" / "ticket.py"

_spec = importlib.util.spec_from_file_location("ticket", TICKET)
tk = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tk)


class TicketTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.ticket_file = self.root / "in_review.json"
        self.verdict_log = self.root / "verdicts.jsonl"
        tk.TICKET_FILE = self.ticket_file
        tk.VERDICT_LOG = self.verdict_log

    def tearDown(self):
        self._tmp.cleanup()

    def _new(self, title, role="engineer", team="team-a"):
        class A:
            pass
        A.title = title
        A.role = role
        A.team = team
        tk.cmd_new(A())

    def test_create_and_list(self):
        self._new("Fix login", "engineer", "team-a")
        self._new("Add a11y", "ux", "team-a")
        tickets = tk._load_tickets()
        self.assertEqual(len(tickets), 2)
        self.assertEqual(tickets[0]["identifier"], "T-1")
        self.assertEqual(tickets[1]["identifier"], "T-2")
        self.assertEqual(tickets[0]["status"], "in_review")

    def test_verdict_kickback_keeps_in_review(self):
        self._new("Fix login")
        class A:
            id = "T-1"
            verdict = "KICK_BACK"
            domain = "engineer"
            veto_hits = "security hole"
            summary = "API key exposed"
        tk.cmd_verdict(A())
        # Verdict written to ledger
        lines = self.verdict_log.read_text().strip().splitlines()
        self.assertEqual(len(lines), 1)
        rec = json.loads(lines[0])
        self.assertEqual(rec["verdict"], "KICK_BACK")
        self.assertTrue(rec["veto_triggered"])
        # Ticket still in_review
        tickets = tk._load_tickets()
        self.assertEqual(tickets[0]["status"], "in_review")

    def test_verdict_pass_marks_done(self):
        self._new("Fix login")
        class A:
            id = "T-1"
            verdict = "PASS"
            domain = "engineer"
            veto_hits = None
            summary = None
        tk.cmd_verdict(A())
        tickets = tk._load_tickets()
        self.assertEqual(tickets[0]["status"], "done")

    def test_done_marks_done(self):
        self._new("Fix login")
        class A:
            id = "T-1"
        tk.cmd_done(A())
        tickets = tk._load_tickets()
        self.assertEqual(tickets[0]["status"], "done")

    def test_watchdog_integration(self):
        # A ticket created now is fresh (not stuck) -> ok_no_findings
        self._new("Fix login")
        import subprocess, sys
        out = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "stuck-review-watchdog.py"),
             "--source", "file", "--issues-file", str(self.ticket_file),
             "--stale-minutes", "120", "--dry-run", "--json"],
            capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(out.returncode, 0)
        report = json.loads(out.stdout)
        self.assertEqual(report["status"], "ok_no_findings")


if __name__ == "__main__":
    unittest.main(verbosity=2)

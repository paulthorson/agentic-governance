"""Tests for the ADR-0009 event log, the ticket close gate, and veto dedupe.

Each test maps to a claim in docs/capability-report.md §12.12. Deleting one
means that claim must be removed or rewritten.

Run:  python3 -m pytest tests/test_events.py -q
"""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


events = _load("events", SCRIPTS / "events.py")
tk = _load("ticket_under_test", SCRIPTS / "ticket.py")
vt = _load("veto_telemetry", SCRIPTS / "veto-telemetry.py")


class _Args:
    def __init__(self, **kw):
        self.__dict__.update(kw)


class EnvelopeTest(unittest.TestCase):
    def test_envelope_has_every_field_in_stable_order(self):
        ev = events.make_event("ticket.created", ticket="T-1")
        self.assertEqual(tuple(ev.keys()), events.ENVELOPE_FIELDS)
        self.assertEqual(ev["schema_version"], "1")

    def test_trace_id_defaults_to_ticket(self):
        ev = events.make_event("ticket.created", ticket="T-7")
        self.assertEqual(ev["trace_id"], "T-7")

    def test_event_ids_unique_within_same_millisecond(self):
        ids = {events.make_event("x")["event_id"] for _ in range(500)}
        self.assertEqual(len(ids), 500)

    def test_kind_required(self):
        with self.assertRaises(ValueError):
            events.make_event("")

    def test_harness_sha_read_without_subprocess(self):
        with mock.patch("subprocess.run", side_effect=AssertionError("no subprocess")):
            events.make_event("x")  # must not shell out to git


class LogTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.log = Path(self._tmp.name) / "events.jsonl"

    def tearDown(self):
        self._tmp.cleanup()

    def test_emit_and_read_roundtrip(self):
        events.emit("a", path=self.log, ticket="T-1")
        events.emit("b", path=self.log, ticket="T-1")
        rows = events.read_events(self.log)
        self.assertEqual([r["kind"] for r in rows], ["a", "b"])

    def test_unknown_schema_version_fails_loudly(self):
        self.log.write_text(json.dumps({"schema_version": "99", "kind": "x"}) + "\n")
        with self.assertRaises(events.UnknownSchemaVersion):
            events.read_events(self.log)
        self.assertEqual(events.read_events(self.log, strict=False), [])

    def test_malformed_line_skipped(self):
        events.emit("a", path=self.log)
        with self.log.open("a") as fh:
            fh.write("{not json\n")
        events.emit("b", path=self.log)
        self.assertEqual(len(events.read_events(self.log)), 2)

    def test_lock_released_after_block(self):
        with events.file_lock(self.log):
            self.assertTrue(self.log.with_name("events.jsonl.lock").exists())
        self.assertFalse(self.log.with_name("events.jsonl.lock").exists())

    def test_held_lock_times_out(self):
        with events.file_lock(self.log):
            with self.assertRaises(events.LockTimeout):
                with events.file_lock(self.log, timeout=0.2):
                    pass

    def test_stale_lock_is_broken(self):
        lock = self.log.with_name("events.jsonl.lock")
        lock.write_text("12345 0\n")
        old = time.time() - events.STALE_LOCK_SECONDS - 5
        os.utime(lock, (old, old))
        with events.file_lock(self.log, timeout=1):
            pass

    def test_concurrent_processes_lose_no_updates(self):
        """Claim: concurrent ticket writers do not lose updates."""
        root = Path(self._tmp.name)
        env = dict(os.environ,
                   TICKET_FILE=str(root / "in_review.json"),
                   VERDICT_LOG=str(root / "verdicts.jsonl"),
                   EVENT_LOG=str(root / "events.jsonl"))
        n = 8
        procs = [
            subprocess.Popen([sys.executable, str(SCRIPTS / "ticket.py"), "new", f"t{i}"],
                             env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            for i in range(n)
        ]
        for p in procs:
            self.assertEqual(p.wait(timeout=60), 0, p.stderr.read())
        tickets = json.loads((root / "in_review.json").read_text())
        self.assertEqual(len(tickets), n)
        self.assertEqual(len({t["identifier"] for t in tickets}), n)
        created = [e for e in events.read_events(root / "events.jsonl") if e["kind"] == "ticket.created"]
        self.assertEqual(len(created), n)


class CloseGateTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "runs").mkdir()
        tk.TICKET_FILE = self.root / "in_review.json"
        tk.VERDICT_LOG = self.root / "verdicts.jsonl"
        tk.EVENT_LOG = self.root / "events.jsonl"
        tk.REPO_ROOT = self.root
        self._env = mock.patch.dict(os.environ, {}, clear=False)
        self._env.start()
        for k in ("AG_APPROVAL", "AG_APPROVAL_TOKEN"):
            os.environ.pop(k, None)
        tk.cmd_new(_Args(title="Fix login", role="engineer", team="", agent="eng-bot"))

    def tearDown(self):
        self._env.stop()
        self._tmp.cleanup()

    def _verdict(self, verdict, hits=None):
        tk.cmd_verdict(_Args(id="T-1", verdict=verdict, domain="qa",
                             veto_hits=hits, summary="", agent="qa-bot"))

    def _ticket(self):
        return tk._load_tickets()[0]

    def _kinds(self):
        return [e["kind"] for e in events.read_events(tk.EVENT_LOG)]

    def test_pass_closes_and_emits(self):
        self._verdict("PASS")
        self.assertEqual(self._ticket()["status"], "done")
        self.assertEqual(self._kinds(), ["ticket.created", "ticket.verdict", "ticket.closed"])

    def test_verdict_record_carries_event_id(self):
        self._verdict("KICK_BACK")
        rec = json.loads(tk.VERDICT_LOG.read_text().splitlines()[0])
        ev = [e for e in events.read_events(tk.EVENT_LOG) if e["kind"] == "ticket.verdict"][0]
        self.assertEqual(rec["event_id"], ev["event_id"])

    def test_pass_with_veto_hits_refused(self):
        with self.assertRaises(tk.Refused):
            self._verdict("PASS", hits="data loss")
        self.assertEqual(self._ticket()["status"], "in_review")
        self.assertFalse(tk.VERDICT_LOG.exists())

    def test_open_veto_blocks_pass(self):
        self._verdict("KICK_BACK", hits="data loss")
        self.assertTrue(self._ticket()["veto_open"])
        with self.assertRaises(tk.Refused):
            self._verdict("PASS")
        self.assertEqual(self._ticket()["status"], "in_review")

    def test_clear_veto_requires_approval(self):
        self._verdict("KICK_BACK", hits="data loss")
        with self.assertRaises(tk.Refused):
            tk.cmd_clear_veto(_Args(id="T-1", by="Operator", reason="fixed"))
        self.assertTrue(self._ticket()["veto_open"])

    def test_clear_veto_with_approval_then_pass(self):
        self._verdict("KICK_BACK", hits="data loss")
        (self.root / "runs" / "approval.ok").write_text("")
        tk.cmd_clear_veto(_Args(id="T-1", by="Operator", reason="fixed"))
        self.assertFalse((self.root / "runs" / "approval.ok").exists())  # one-shot consumed
        self._verdict("PASS")
        t = self._ticket()
        self.assertEqual(t["status"], "done")
        self.assertEqual(t["veto_cleared_by"], "Operator")
        self.assertIn("ticket.veto_cleared", self._kinds())

    def test_done_after_kickback_refused(self):
        self._verdict("KICK_BACK")
        with self.assertRaises(tk.Refused):
            tk.cmd_done(_Args(id="T-1", override=False, agent="eng-bot"))

    def test_override_requires_approval(self):
        with self.assertRaises(tk.Refused):
            tk.cmd_done(_Args(id="T-1", override=True, by="Operator", reason="hotfix", agent=None))
        self.assertEqual(self._ticket()["status"], "in_review")

    def test_override_with_approval_is_recorded(self):
        (self.root / "runs" / "approval.ok").write_text("")
        tk.cmd_done(_Args(id="T-1", override=True, by="Operator", reason="hotfix", agent=None))
        self.assertEqual(self._ticket()["closed_by_override"], "Operator")
        closed = [e for e in events.read_events(tk.EVENT_LOG) if e["kind"] == "ticket.closed"][0]
        self.assertEqual(closed["data"]["via"], "override")

    def test_cli_refusal_exit_code(self):
        env = dict(os.environ, TICKET_FILE=str(tk.TICKET_FILE),
                   VERDICT_LOG=str(tk.VERDICT_LOG), EVENT_LOG=str(tk.EVENT_LOG),
                   ADVERSARIAL_ROOT=str(self.root))
        out = subprocess.run([sys.executable, str(SCRIPTS / "ticket.py"), "done", "T-1"],
                             env=env, capture_output=True, text=True, timeout=30)
        self.assertEqual(out.returncode, 2)
        self.assertIn("REFUSED", out.stderr)


class VetoDedupeTest(unittest.TestCase):
    def test_two_vetoes_same_millisecond_both_distinct(self):
        a = {"ts": 1000, "event_id": "a", "ticket": "T-1", "domain": "qa", "verdict": "KICK_BACK", "veto_hits": ["x"]}
        b = dict(a, event_id="b", ticket="T-2")
        self.assertNotEqual(vt._dedupe_key(a), vt._dedupe_key(b))

    def test_legacy_records_without_event_id_still_distinct(self):
        a = {"ts": 1000, "ticket": "T-1", "domain": "qa", "verdict": "KICK_BACK", "veto_hits": ["x"]}
        b = dict(a, ticket="T-2")
        self.assertNotEqual(vt._dedupe_key(a), vt._dedupe_key(b))


class ServerVerdictEventTest(unittest.TestCase):
    """Claim: MCP record_verdict writes an event and stamps event_id on the record."""

    def test_record_verdict_emits_event(self):
        sys.path.insert(0, str(REPO_ROOT / "mcp"))
        from adversarial_mcp import server as srv

        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            orig_log = srv.VERDICT_LOG
            srv.VERDICT_LOG = d / "verdicts.jsonl"
            try:
                with mock.patch.dict(os.environ, {"EVENT_LOG": str(d / "events.jsonl")}):
                    out = srv.record_verdict("qa", "kick_back", "missing edge case", ticket="T-9")
                    evs = events.read_events(d / "events.jsonl")
                    self.assertEqual(len(evs), 1)
                    self.assertEqual(evs[0]["kind"], "verdict.recorded")
                    self.assertEqual(evs[0]["trace_id"], "T-9")
                    self.assertEqual(out["record"]["event_id"], evs[0]["event_id"])

                    srv.overturn_verdict("T-9", "precedent was wrong")
                    kinds = [e["kind"] for e in events.read_events(d / "events.jsonl")]
                    self.assertEqual(kinds, ["verdict.recorded", "verdict.overturned"])
                    rec = json.loads((d / "verdicts.jsonl").read_text().splitlines()[0])
                    self.assertEqual(rec["status"], "overturned")
            finally:
                srv.VERDICT_LOG = orig_log


if __name__ == "__main__":
    unittest.main(verbosity=2)

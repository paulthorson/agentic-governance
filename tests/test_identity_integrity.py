"""Tests for agent identity (ADR-0011) and tamper detection (ADR-0012).

Each test maps to a claim in docs/capability-report.md §12.14 / §12.15.
Deleting one means that claim must be removed or rewritten.

Run:  python3 -m pytest tests/test_identity_integrity.py -q
"""

import importlib.util
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


chain = _load("chain", SCRIPTS / "chain.py")
events = chain.events
identity = chain.identity
integrity = chain.integrity
T0 = 1_800_000_000.0
MIN = 60.0


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.d = Path(self._tmp.name)
        self.reg = identity.Registry(self.d / "agents.json")
        self.store = chain.Store(self.d / "in_review.json", self.d / "verdicts.jsonl", self.d / "events.jsonl",
                                 chain.Settings(), registry=self.reg)
        self._env = mock.patch.dict(os.environ, {"AG_INTEGRITY_KEY_FILE": str(self.d / "integrity.key")})
        self._env.start()
        os.environ.pop("AG_INTEGRITY_KEY", None)
        os.environ.pop("AG_AGENT_TOKEN", None)

    def tearDown(self):
        self._env.stop()
        self._tmp.cleanup()

    def t(self, ident="T-1"):
        return next(x for x in self.store.load() if x["identifier"] == ident)

    def evs(self):
        return events.read_events(self.store.event_log)


# ---------------------------------------------------------------------------
# Identity
# ---------------------------------------------------------------------------


class IdentityTest(Base):
    def setUp(self):
        super().setUp()
        self.eng = self.reg.add("eng-1", "team-a", ["engineer"], "runtime-a")
        self.critic = self.reg.add("eng-critic", "team-a", ["review:engineer"], "runtime-b")
        self.store.create("x", "engineer", "team-a", end_stage="engineer", now=T0)

    def test_unregistered_install_is_self_reported(self):
        store = chain.Store(self.d / "t2.json", self.d / "v2.jsonl", self.d / "e2.jsonl",
                            registry=identity.Registry(self.d / "none.json"))
        store.create("x", "pm", "a", now=T0)
        store.claim_next("pm", "a", "anyone", now=T0)
        claimed = [e for e in events.read_events(self.d / "e2.jsonl") if e["kind"] == "ticket.claimed"][0]
        self.assertFalse(claimed["agent_verified"])

    def test_token_required_once_registered(self):
        """Claim: with a registry, a self-reported id is refused."""
        with self.assertRaises(chain.Refused):
            self.store.claim_next("engineer", "team-a", "eng-1", now=T0)
        with self.assertRaises(chain.Refused):
            self.store.claim_next("engineer", "team-a", "eng-1", now=T0, token="not-a-token")
        self.assertEqual(self.t()["state"], "queued")
        self.assertIn("ticket.transition_refused", [e["kind"] for e in self.evs()])

    def test_token_decides_identity(self):
        t = self.store.claim_next("engineer", "", None, now=T0, token=self.eng)
        self.assertEqual(t["claimedBy"], "eng-1")
        claimed = [e for e in self.evs() if e["kind"] == "ticket.claimed"][0]
        self.assertTrue(claimed["agent_verified"])

    def test_claimed_id_must_match_token(self):
        with self.assertRaises(chain.Refused):
            self.store.claim_next("engineer", "team-a", "eng-critic", now=T0, token=self.eng)

    def test_team_and_role_come_from_registry(self):
        """Claim: a registered agent cannot claim outside its team or stages."""
        with self.assertRaises(chain.Refused):
            self.store.claim_next("engineer", "team-b", None, now=T0, token=self.eng)
        with self.assertRaises(chain.Refused):
            self.store.claim_next("engineer", "", None, mode="review", now=T0, token=self.eng)
        with self.assertRaises(chain.Refused):
            self.store.claim_next("engineer", "", None, now=T0, token=self.critic)

    def test_full_verified_loop(self):
        self.store.claim_next("engineer", "", None, now=T0, token=self.eng)
        self.store.submit("T-1", None, now=T0, token=self.eng)
        self.store.claim_next("engineer", "", None, mode="review", now=T0, token=self.critic)
        self.store.verdict("T-1", "PASS", None, [], now=T0, token=self.critic)
        self.assertEqual(self.t()["state"], "done")
        v = json.loads(self.store.verdict_log.read_text().splitlines()[-1])
        self.assertEqual((v["agent_id"], v["agent_verified"]), ("eng-critic", True))

    def test_same_principal_cannot_review(self):
        """Claim: one runtime holding two registered ids cannot review its own work."""
        twin = self.reg.add("eng-twin", "team-a", ["review:engineer"], "runtime-a")
        self.store.claim_next("engineer", "", None, now=T0, token=self.eng)
        self.store.submit("T-1", None, now=T0, token=self.eng)
        self.assertIsNone(self.store.claim_next("engineer", "", None, mode="review", now=T0, token=twin))

    def test_same_principal_verdict_refused_even_with_claim(self):
        """Pure-function guard: principal match refuses the verdict."""
        t = {"identifier": "T-9", "stage": "qa", "stages": ["qa"], "state": "reviewing",
             "claimedBy": "b", "workedBy": "a", "workedByPrincipal": "rt", "attempts": {}}
        with self.assertRaises(chain.Refused):
            chain.verdict(t, "PASS", "b", [], T0, chain.Settings(), principal="rt")

    def test_revoked_token_refused(self):
        self.reg.revoke("eng-1")
        with self.assertRaises(chain.Refused):
            self.store.claim_next("engineer", "", None, now=T0, token=self.eng)

    def test_registry_never_stores_token_and_is_private(self):
        raw = self.reg.path.read_text()
        self.assertNotIn(self.eng, raw)
        if os.name == "posix":
            self.assertEqual(stat.S_IMODE(self.reg.path.stat().st_mode), 0o600)

    def test_broken_registry_does_not_fall_back(self):
        """Claim: an unreadable registry refuses agent actions instead of trusting ids."""
        self.reg.path.write_text("{not json")
        with self.assertRaises(chain.Refused):
            self.store.claim_next("engineer", "team-a", "eng-1", now=T0)

    def test_cli_agent_add_needs_approval(self):
        env = {k: v for k, v in os.environ.items() if k not in ("AG_APPROVAL", "AG_APPROVAL_TOKEN")}
        root = self.d / "root"
        (root / "runs").mkdir(parents=True)
        env.update(ADVERSARIAL_ROOT=str(root), AG_AGENT_REGISTRY=str(root / "agents.json"),
                   TICKET_FILE=str(root / "t.json"), EVENT_LOG=str(root / "e.jsonl"),
                   VERDICT_LOG=str(root / "v.jsonl"))
        cmd = [sys.executable, str(SCRIPTS / "ticket.py"), "agent", "add", "x-1",
               "--roles", "pm", "--principal", "rt"]
        self.assertEqual(subprocess.run(cmd, env=env, capture_output=True, timeout=30).returncode, 2)
        (root / "runs" / "approval.ok").write_text("")
        out = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=30)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertTrue(identity.Registry(root / "agents.json").enforced())


# ---------------------------------------------------------------------------
# Integrity
# ---------------------------------------------------------------------------


class IntegrityTest(Base):
    def setUp(self):
        super().setUp()
        self.store.create("x", "pm", "a", now=T0)
        self.store.claim_next("pm", "a", "w", now=T0)

    def _lines(self):
        return self.store.event_log.read_text().splitlines()

    def _write_lines(self, lines):
        self.store.event_log.write_text("\n".join(lines) + "\n")

    def test_clean_log_verifies(self):
        rep = integrity.verify_log(self.store.event_log, None)
        self.assertTrue(rep["ok"], rep)
        self.assertEqual(rep["chained"], rep["events"])
        self.store.check_integrity(repair=False)

    def test_edited_event_detected(self):
        """Claim: editing a logged event is detected."""
        lines = self._lines()
        ev = json.loads(lines[0])
        ev["agent_id"] = "someone-else"
        lines[0] = json.dumps(ev)
        self._write_lines(lines)
        self.assertFalse(integrity.verify_log(self.store.event_log, None)["ok"])

    def test_deleted_event_detected(self):
        lines = self._lines()
        self.store.submit("T-1", "w", now=T0)
        lines = self._lines()
        del lines[1]
        self._write_lines(lines)
        self.assertFalse(integrity.verify_log(self.store.event_log, None)["ok"])

    def test_truncated_log_stops_writes(self):
        """Claim: deleting the newest events is detected on the next write."""
        self._write_lines(self._lines()[:-1])
        with self.assertRaises(integrity.TamperDetected):
            self.store.submit("T-1", "w", now=T0)

    def test_direct_ticket_edit_stops_writes_until_accepted(self):
        """Claim: editing the ticket file outside the framework stops all writes."""
        data = json.loads(self.store.ticket_file.read_text())
        data[0]["state"] = "done"
        data[0]["status"] = "done"
        self.store.ticket_file.write_text(json.dumps(data, indent=2))
        with self.assertRaises(integrity.TamperDetected):
            self.store.submit("T-1", "w", now=T0)
        with self.assertRaises(integrity.TamperDetected):
            self.store.claim_next("pm", "a", "w2", now=T0)
        self.assertIn("store.tamper_detected", [e["kind"] for e in self.evs()])
        gate_calls = []
        self.store.accept_current_state("Operator", "reviewed edit", gate=lambda: gate_calls.append(1))
        self.assertEqual(gate_calls, [1])
        self.store.recover(now=T0)  # writes resume
        kinds = [e["kind"] for e in self.evs()]
        self.assertIn("store.integrity_accepted", kinds)

    def test_head_removed_detected(self):
        self.store.head_file.unlink()
        with self.assertRaises(integrity.TamperDetected):
            self.store.submit("T-1", "w", now=T0)

    def test_head_and_store_removed_detected(self):
        """Claim: wiping the ticket file and head together is still detected."""
        self.store.head_file.unlink()
        self.store.ticket_file.unlink()
        with self.assertRaises(integrity.TamperDetected):
            self.store.create("y", "pm", "a", now=T0)

    def test_crash_after_events_rolls_forward(self):
        """Claim: a crash mid-commit is recovered, not reported as tampering."""
        real = os.replace
        calls = {"n": 0}

        def flaky(src, dst):
            if str(dst) == str(self.store.ticket_file) and calls["n"] == 0:
                calls["n"] += 1
                raise OSError("simulated crash before replace")
            return real(src, dst)
        with mock.patch.object(chain.os, "replace", side_effect=flaky):
            with self.assertRaises(OSError):
                self.store.submit("T-1", "w", now=T0)
        self.store.check_integrity()  # rolls forward from the temp file
        self.assertEqual(self.t()["state"], "in_review")

    def test_crash_before_events_changes_nothing(self):
        with mock.patch.object(chain.events, "emit_at", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                self.store.submit("T-1", "w", now=T0)
        self.store.check_integrity()
        self.assertEqual(self.t()["state"], "working")

    def test_pre_chain_events_are_allowed(self):
        log = self.d / "legacy.jsonl"
        log.write_text(json.dumps({"schema_version": "1", "kind": "old"}) + "\n")
        events.emit("new", path=log)
        self.assertTrue(integrity.verify_log(log, None)["ok"])
        with log.open("a") as fh:
            fh.write(json.dumps({"schema_version": "1", "kind": "inserted"}) + "\n")
        self.assertFalse(integrity.verify_log(log, None)["ok"])


class KeyedIntegrityTest(Base):
    def setUp(self):
        super().setUp()
        os.environ["AG_INTEGRITY_KEY"] = "operator-secret"
        self.store.create("x", "pm", "a", now=T0)

    def tearDown(self):
        os.environ.pop("AG_INTEGRITY_KEY", None)
        super().tearDown()

    def test_forger_without_key_detected(self):
        """Claim: with a key, an edited event re-hashed without the key is detected."""
        lines = self.store.event_log.read_text().splitlines()
        ev = json.loads(lines[-1])
        ev["data"]["title"] = "forged"
        os.environ.pop("AG_INTEGRITY_KEY")
        forged = integrity.chain_event({k: v for k, v in ev.items() if k not in integrity.CHAIN_FIELDS},
                                       ev["prev_hash"], b"guessed-key")
        lines[-1] = json.dumps(forged)
        self.store.event_log.write_text("\n".join(lines) + "\n")
        os.environ["AG_INTEGRITY_KEY"] = "operator-secret"
        self.assertFalse(integrity.verify_log(self.store.event_log, b"operator-secret")["ok"])

    def test_downgrade_to_unkeyed_detected(self):
        lines = self.store.event_log.read_text().splitlines()
        ev = json.loads(lines[-1])
        plain = integrity.chain_event({k: v for k, v in ev.items() if k not in integrity.CHAIN_FIELDS},
                                      ev["prev_hash"], None)
        lines[-1] = json.dumps(plain)
        self.store.event_log.write_text("\n".join(lines) + "\n")
        # The signed head pins the keyed hash of the last commit.
        with self.assertRaises(integrity.TamperDetected):
            self.store.check_integrity()

    def test_head_signature_checked(self):
        """Claim: the head record cannot be rewritten without the key."""
        head = json.loads(self.store.head_file.read_text())
        head["store_digest"] = "0" * 64
        self.store.head_file.write_text(json.dumps(head))
        with self.assertRaises(integrity.TamperDetected):
            self.store.check_integrity()

    def test_missing_key_on_keyed_install_refuses(self):
        os.environ.pop("AG_INTEGRITY_KEY")
        with self.assertRaises(integrity.TamperDetected):
            self.store.check_integrity()


class CliIntegrityTest(unittest.TestCase):
    def test_verify_doctor_and_tamper_exit_codes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "runs").mkdir()
            env = {k: v for k, v in os.environ.items()
                   if k not in ("AG_APPROVAL", "AG_APPROVAL_TOKEN", "AG_INTEGRITY_KEY")}
            env.update(ADVERSARIAL_ROOT=str(root), TICKET_FILE=str(root / "runs" / "t.json"),
                       EVENT_LOG=str(root / "runs" / "e.jsonl"), VERDICT_LOG=str(root / "runs" / "v.jsonl"),
                       AG_AGENT_REGISTRY=str(root / "agents.json"),
                       AG_INTEGRITY_KEY_FILE=str(root / "integrity.key"))

            def run(*a):
                return subprocess.run([sys.executable, str(SCRIPTS / "ticket.py"), *a],
                                      env=env, capture_output=True, text=True, timeout=30)

            self.assertEqual(run("new", "x", "--queue", "--role", "pm").returncode, 0)
            self.assertEqual(run("verify").returncode, 0)
            self.assertEqual(run("doctor").returncode, 0)  # WARNs only on a fresh install
            # init-key needs approval, then keys the chain from a clean state
            self.assertEqual(run("integrity", "init-key").returncode, 2)
            (root / "runs" / "approval.ok").write_text("")
            self.assertEqual(run("integrity", "init-key").returncode, 0)
            if os.name == "posix":
                self.assertEqual(stat.S_IMODE((root / "integrity.key").stat().st_mode), 0o600)
            self.assertEqual(run("claim", "--role", "pm", "--agent", "w").returncode, 0)
            self.assertEqual(run("verify").returncode, 0)
            t = root / "runs" / "t.json"
            t.write_text(t.read_text().replace('"working"', '"done"'))
            self.assertEqual(run("verify").returncode, 4)
            out = run("submit", "T-1", "--agent", "w")
            self.assertEqual(out.returncode, 4)
            self.assertIn("TAMPER", out.stderr)


class McpIntegrityTest(unittest.TestCase):
    def test_mcp_verify_tool_and_tamper_status(self):
        sys.path.insert(0, str(REPO_ROOT / "mcp"))
        from adversarial_mcp import server as srv
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            orig = srv.VERDICT_LOG
            srv.VERDICT_LOG = d / "v.jsonl"
            try:
                with mock.patch.dict(os.environ, {"TICKET_FILE": str(d / "t.json"), "EVENT_LOG": str(d / "e.jsonl")}):
                    srv.ticket_create("x", stage="pm", team="a")
                    self.assertTrue(srv.ticket_verify()["ok"])
                    (d / "t.json").write_text("[]")
                    self.assertEqual(srv.ticket_claim_next("pm", "a", "w")["status"], "tampered")
                    self.assertFalse(srv.ticket_verify()["ok"])
            finally:
                srv.VERDICT_LOG = orig


if __name__ == "__main__":
    unittest.main(verbosity=2)

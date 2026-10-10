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
        self._env = mock.patch.dict(os.environ, {"AG_INTEGRITY_KEY_FILE": str(self.d / "config" / "integrity.key")})
        self._env.start()
        self.reg = identity.Registry(self.d / "config" / "agents.json")
        (self.d / "runs").mkdir()
        self.store = chain.Store(self.d / "runs" / "in_review.json", self.d / "runs" / "verdicts.jsonl",
                                 self.d / "runs" / "events.jsonl", chain.Settings(), registry=self.reg)
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
        store = chain.Store(self.d / "runs" / "t2.json", self.d / "runs" / "v2.jsonl", self.d / "runs" / "e2.jsonl",
                            registry=identity.Registry(self.d / "none.json"))
        store.create("x", "pm", "a", now=T0)
        store.claim_next("pm", "a", "anyone", now=T0)
        claimed = [e for e in events.read_events(self.d / "runs" / "e2.jsonl") if e["kind"] == "ticket.claimed"][0]
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
            with self.assertRaises(chain.CommitPending):  # tells the agent not to retry
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


class HttpIdentityTest(unittest.TestCase):
    def test_http_server_refuses_shared_agent_token(self):
        """Claim: a shared HTTP server cannot inherit one agent's identity."""
        sys.path.insert(0, str(REPO_ROOT / "mcp"))
        from adversarial_mcp import server as srv
        with mock.patch.dict(os.environ, {"AG_AGENT_TOKEN": "x"}):
            self.assertTrue(srv.refuse_http_with_agent_token())
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("AG_AGENT_TOKEN", None)
            self.assertFalse(srv.refuse_http_with_agent_token())
        src = (REPO_ROOT / "mcp" / "adversarial_mcp" / "server.py").read_text()
        main = src[src.index("def main()"):]
        self.assertLess(main.index("refuse_http_with_agent_token()"), main.index("uvicorn.run") if "uvicorn.run" in main else len(main))


class SecondReviewTest(Base):
    """Regression tests for the 1.2 adversarial review."""

    def _keyed(self):
        os.environ["AG_INTEGRITY_KEY"] = "operator-secret"
        self.addCleanup(os.environ.pop, "AG_INTEGRITY_KEY", None)

    def _cycle(self):
        self.store.create("x", "pm", "a", now=T0)
        self.store.claim_next("pm", "a", "w", now=T0)
        self.store.submit("T-1", "w", now=T0)

    def test_head_lives_outside_runs(self):
        """Claim: the head record is not in the ticket store's directory."""
        self.assertNotEqual(self.store.head_file.parent.resolve(), self.store.ticket_file.parent.resolve())
        self.assertEqual(self.store.head_file.parent, integrity.key_path().parent)

    def test_head_deleted_plus_junk_line_detected(self):
        """H1: a junk last line must not make a committed log look fresh."""
        self._keyed()
        self._cycle()
        self.store.head_file.unlink()
        with self.store.event_log.open("a") as fh:
            fh.write('{"note": "x"}\n')
        with self.assertRaises(integrity.TamperDetected):
            self.store.check_integrity()

    def test_consistent_rollback_detected_when_head_is_protected(self):
        """H2: restoring older ticket + log files is caught by the head kept in config/."""
        self._keyed()
        self._cycle()
        snap_t = self.store.ticket_file.read_bytes()
        snap_size = self.store.event_log.stat().st_size
        self.store.claim_next("pm", "a", "r", mode="review", now=T0)
        self.store.verdict("T-1", "KICK_BACK", "r", ["user harm"], now=T0)
        self.store.ticket_file.write_bytes(snap_t)
        with open(self.store.event_log, "rb+") as fh:
            fh.truncate(snap_size)
        with self.assertRaises(integrity.TamperDetected):
            self.store.check_integrity()

    def test_tokenless_create_into_review_needs_operator_gate(self):
        """H3: no path puts unattributed work straight into review on an enforced install."""
        eng = self.reg.add("eng-1", "team-a", ["engineer"], "runtime-a")
        critic = self.reg.add("eng-critic", "team-a", ["review:engineer"], "runtime-a")
        with self.assertRaises(chain.Refused):
            self.store.create("mine", "engineer", "team-a", queued=False, now=T0)
        # With a token, the creator is recorded as the worker.
        self.store.create("mine", "engineer", "team-a", queued=False, now=T0, token=eng)
        self.assertIsNone(self.store.claim_next("engineer", "", None, mode="review", now=T0, token=critic))
        # An operator may do it with approval; the gate runs.
        calls = []
        self.store.create("ops", "engineer", "team-a", queued=False, now=T0, gate=lambda: calls.append(1))
        self.assertEqual(calls, [1])

    def test_mcp_style_create_requires_token_when_enforced(self):
        """M6: require_token refuses tokenless creates; tokens are team-bound."""
        eng = self.reg.add("eng-1", "team-a", ["engineer"], "runtime-a")
        with self.assertRaises(chain.Refused):
            self.store.create("x", "qa", "team-a", now=T0, require_token=True)
        with self.assertRaises(chain.Refused):
            self.store.create("x", "qa", "team-b", now=T0, token=eng, require_token=True)
        self.store.create("x", "qa", "team-a", now=T0, token=eng, require_token=True)

    def test_accepted_problem_does_not_cover_later_edit(self):
        """M1: accepting a problem on a line does not accept future edits to it."""
        self._cycle()
        lines = self.store.event_log.read_text().splitlines()
        ev = json.loads(lines[1]); ev["outcome"] = "x"; lines[1] = json.dumps(ev)
        self.store.event_log.write_text("\n".join(lines) + "\n")
        first = integrity.verify_log(self.store.event_log, None)["problems"]
        ev["outcome"] = "y"; lines[1] = json.dumps(ev)
        self.store.event_log.write_text("\n".join(lines) + "\n")
        second = integrity.verify_log(self.store.event_log, None)["problems"]
        self.assertTrue(integrity.unaccepted(second, first))

    def test_keyless_process_cannot_poison_keyed_log(self):
        """M2: an emitter without the key refuses instead of appending a downgrade."""
        self._keyed()
        self._cycle()
        os.environ.pop("AG_INTEGRITY_KEY")
        with self.assertRaises(integrity.KeyRequired):
            events.emit("x", path=self.store.event_log)
        os.environ["AG_INTEGRITY_KEY"] = "operator-secret"
        self.store.check_integrity()
        self.store.claim_next("pm", "a", "r", mode="review", now=T0)

    def test_torn_append_is_repaired_not_a_halt(self):
        """M5: a partial last line from a crash does not stop the loop."""
        self._cycle()
        with self.store.event_log.open("a") as fh:
            fh.write('{"schema_version": "1", "kind": "half')
        self.store.check_integrity()
        self.store.claim_next("pm", "a", "r", mode="review", now=T0)
        self.assertTrue(Path(str(self.store.event_log) + ".torn").exists())
        self.assertTrue(integrity.verify_log(self.store.event_log, None)["ok"])

    def test_torn_tail_longer_than_one_megabyte_keeps_committed_lines(self):
        """A fragment longer than the old 1 MB scan window must not truncate
        the committed log to zero."""
        self._cycle()
        before = self.store.event_log.read_bytes()
        with self.store.event_log.open("a") as fh:
            fh.write('{"kind": "' + "x" * (3 << 20))
        n = integrity.repair_torn_tail(self.store.event_log)
        self.assertGreater(n, 3 << 20)
        self.assertEqual(self.store.event_log.read_bytes(), before)

    def test_identity_cannot_be_silently_switched_off(self):
        """L6: emptying or redirecting the registry after commits under identity is detected."""
        eng = self.reg.add("eng-1", "a", ["pm"], "runtime-a")
        self.store.create("x", "pm", "a", now=T0, token=eng)
        self.store.registry = identity.Registry(self.d / "elsewhere.json")
        with self.assertRaises(integrity.TamperDetected):
            self.store.claim_next("pm", "a", "anyone", now=T0)

    def test_recovery_events_not_credited_as_verified(self):
        """L4: events produced by recovery are never marked verified."""
        eng = self.reg.add("eng-1", "a", ["pm"], "runtime-a")
        self.store.create("x", "pm", "a", now=T0, token=eng)
        self.store.claim_next("pm", "", None, now=T0, token=eng)
        self.store.claim_next("pm", "", None, now=T0 + 31 * MIN, token=eng)
        expired = [e for e in self.evs() if e["kind"] == "ticket.lease_expired"][0]
        self.assertFalse(expired["agent_verified"])
        claims = [e for e in self.evs() if e["kind"] == "ticket.claimed"]
        self.assertTrue(all(c["agent_verified"] for c in claims))

    def test_no_env_agent_id_fallback(self):
        with mock.patch.dict(os.environ, {"AG_AGENT_ID": "ghost"}):
            self.assertIsNone(events.make_event("x")["agent_id"])


class ReplaceRetryTest(Base):
    def test_transient_permission_error_retried(self):
        """M3: a Windows sharing violation on replace is retried, not surfaced as a failure."""
        self.store.create("x", "pm", "a", now=T0)
        real = os.replace
        calls = {"n": 0}

        def flaky(src, dst):
            if str(dst) == str(self.store.ticket_file) and calls["n"] < 2:
                calls["n"] += 1
                raise PermissionError("in use")
            return real(src, dst)
        with mock.patch.object(chain.os, "replace", side_effect=flaky), \
                mock.patch.object(chain.time, "sleep"):
            self.store.claim_next("pm", "a", "w1", now=T0)
        self.assertEqual(self.t()["claimedBy"], "w1")

    def test_claim_retry_returns_the_held_claim(self):
        """M3: an agent that retries a claim does not end up holding two tickets."""
        self.store.create("a", "pm", "a", now=T0)
        self.store.create("b", "pm", "a", now=T0 + 1)
        first = self.store.claim_next("pm", "a", "w1", now=T0 + 2)
        again = self.store.claim_next("pm", "a", "w1", now=T0 + 3)
        self.assertEqual(first["identifier"], again["identifier"])
        self.assertEqual([t["state"] for t in self.store.load()], ["working", "queued"])


class LockedVerifyTest(unittest.TestCase):
    def test_verify_paths_hold_the_ticket_lock(self):
        """M4: verify / doctor / recover --alert / MCP ticket_verify never race a commit."""
        src = (SCRIPTS / "ticket.py").read_text()
        body = src[src.index("def _verify_report"):src.index("def cmd_verify")]
        self.assertIn("events.file_lock(store.ticket_file)", body)
        srv = (REPO_ROOT / "mcp" / "adversarial_mcp" / "server.py").read_text()
        tool = srv[srv.index("def ticket_verify"):srv.index("def ticket_list")]
        self.assertIn("file_lock(store.ticket_file)", tool)


_STRESS_WORKER = r"""
import os, sys, json
sys.path.insert(0, os.environ["SCRIPTS"])
import chain, events
from pathlib import Path
d = Path(os.environ["D"])
store = chain.Store(d / "runs" / "t.json", d / "runs" / "v.jsonl", d / "runs" / "e.jsonl")
me, n = sys.argv[1], int(sys.argv[2])
if me.startswith("emit"):
    for i in range(n):
        events.emit("verdict.recorded", path=d / "runs" / "e.jsonl", data={"i": i, "who": me})
else:
    for i in range(n):
        store.create(f"{me}-{i}", "pm", "a")
        t = store.claim_next("pm", "a", me)
        if t is not None:
            store.submit(t["identifier"], me)
"""


class CrossPlatformStressTest(unittest.TestCase):
    """Runs on Linux and macOS in CI: concurrent processes through the real
    lock, replace, and chain code. Nothing lost, nothing flagged."""

    def test_concurrent_writers_and_emitters(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "runs").mkdir()
            worker = d / "worker.py"
            worker.write_text(_STRESS_WORKER)
            env = dict(os.environ, SCRIPTS=str(SCRIPTS), D=str(d),
                       AG_INTEGRITY_KEY_FILE=str(d / "config" / "integrity.key"),
                       AG_AGENT_REGISTRY=str(d / "config" / "agents.json"),
                       AG_INTEGRITY_KEY="stress-key")
            names = [f"w{i}" for i in range(4)] + [f"emit{i}" for i in range(3)]
            per = 15
            procs = [subprocess.Popen([sys.executable, str(worker), n, str(per)], env=env,
                                      stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
                     for n in names]
            for p in procs:
                self.assertEqual(p.wait(timeout=180), 0, p.stderr.read().decode())
            with mock.patch.dict(os.environ, {"AG_INTEGRITY_KEY": "stress-key",
                                              "AG_INTEGRITY_KEY_FILE": str(d / "config" / "integrity.key")}):
                store = chain.Store(d / "runs" / "t.json", d / "runs" / "v.jsonl", d / "runs" / "e.jsonl",
                                    registry=identity.Registry(d / "config" / "agents.json"))
                store.check_integrity(repair=False)
                rep = integrity.verify_log(d / "runs" / "e.jsonl", b"stress-key")
            self.assertTrue(rep["ok"], rep["problems"][:5])
            tickets = store.load()
            self.assertEqual(len(tickets), 4 * per)
            self.assertEqual(len({t["identifier"] for t in tickets}), 4 * per)
            self.assertTrue(all(t["state"] == "in_review" for t in tickets))
            emitted = [e for e in events.read_events(d / "runs" / "e.jsonl") if e["kind"] == "verdict.recorded"]
            self.assertEqual(len(emitted), 3 * per)


if __name__ == "__main__":
    unittest.main(verbosity=2)

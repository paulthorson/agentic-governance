"""Tests for the chain state machine and stuck-ticket recovery (ADR-0010).

Each test maps to a claim in docs/capability-report.md §12.13. Deleting one
means that claim must be removed or rewritten. Time is injected (``now=``)
so lease expiry and stall detection are deterministic.

Run:  python3 -m pytest tests/test_chain.py -q
"""

import importlib.util
import json
import os
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
    sys.modules[name] = mod  # dataclasses resolve annotations via sys.modules
    spec.loader.exec_module(mod)
    return mod


chain = _load("chain", SCRIPTS / "chain.py")
events = _load("events", SCRIPTS / "events.py")
T0 = 1_800_000_000.0  # fixed epoch for deterministic leases
MIN = 60.0


class ChainBase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        d = Path(self._tmp.name)
        self.store = chain.Store(d / "in_review.json", d / "verdicts.jsonl", d / "events.jsonl",
                                 chain.Settings(lease_minutes=30, max_attempts=3, max_kickbacks=2,
                                                review_timeout_minutes=120, queue_timeout_minutes=240))

    def tearDown(self):
        self._tmp.cleanup()

    def t(self, ident="T-1"):
        return next(x for x in self.store.load() if x["identifier"] == ident)

    def kinds(self):
        return [e["kind"] for e in events.read_events(self.store.event_log)]

    def work_and_submit(self, stage, team="a", worker="w", now=T0):
        got = self.store.claim_next(stage, team, worker, now=now)
        self.assertIsNotNone(got, f"nothing to claim at {stage}")
        self.store.submit(got["identifier"], worker, now=now)
        return got["identifier"]

    def review(self, ident, stage, v, team="a", reviewer="r", now=T0, **kw):
        got = self.store.claim_next(stage, team, reviewer, mode="review", now=now)
        self.assertEqual(got["identifier"], ident)
        return self.store.verdict(ident, v, reviewer, kw.pop("hits", []), now=now, **kw)


class ChainFlowTest(ChainBase):
    def test_full_chain_runs_to_done(self):
        """Claim: a queued ticket walks every stage and closes only on the last PASS."""
        self.store.create("Feature", "research", "a", now=T0)
        for stage in chain.CHAIN:
            ident = self.work_and_submit(stage)
            self.review(ident, stage, "PASS")
        t = self.t()
        self.assertEqual(t["state"], "done")
        self.assertEqual(self.kinds().count("ticket.advanced"), len(chain.CHAIN) - 1)
        self.assertEqual(self.kinds()[-1], "ticket.closed")

    def test_end_stage_shortens_chain(self):
        t = self.store.create("Bug", "engineer", "a", end_stage="qa", now=T0)
        self.assertEqual(t["stages"], ["engineer", "qa"])

    def test_claims_are_team_scoped(self):
        """Claim: an agent never claims another team's work."""
        self.store.create("A's work", "pm", "team-a", now=T0)
        self.assertIsNone(self.store.claim_next("pm", "team-b", "b-agent", now=T0))
        self.assertIsNotNone(self.store.claim_next("pm", "team-a", "a-agent", now=T0))

    def test_claims_are_stage_scoped(self):
        self.store.create("x", "pm", "a", now=T0)
        self.assertIsNone(self.store.claim_next("ux", "a", "ux-agent", now=T0))

    def test_oldest_first(self):
        self.store.create("old", "pm", "a", now=T0)
        self.store.create("new", "pm", "a", now=T0 + 5)
        self.assertEqual(self.store.claim_next("pm", "a", "w", now=T0 + 10)["title"], "old")

    def test_only_claimant_submits_and_heartbeats(self):
        self.store.create("x", "pm", "a", now=T0)
        self.store.claim_next("pm", "a", "w1", now=T0)
        with self.assertRaises(chain.Refused):
            self.store.submit("T-1", "w2", now=T0)
        with self.assertRaises(chain.Refused):
            self.store.heartbeat("T-1", "w2", now=T0)
        self.assertIn("ticket.transition_refused", self.kinds())

    def test_worker_cannot_review_own_work(self):
        """Claim: the agent that did the work cannot review it."""
        self.store.create("x", "pm", "a", now=T0)
        self.work_and_submit("pm", worker="w")
        self.assertIsNone(self.store.claim_next("pm", "a", "w", mode="review", now=T0))
        with self.assertRaises(chain.Refused):
            self.store.verdict("T-1", "PASS", "w", [], now=T0)
        self.assertEqual(self.t()["state"], "in_review")

    def test_reviewing_claim_is_exclusive(self):
        self.store.create("x", "pm", "a", now=T0)
        self.work_and_submit("pm")
        self.store.claim_next("pm", "a", "r1", mode="review", now=T0)
        with self.assertRaises(chain.Refused):
            self.store.verdict("T-1", "PASS", "r2", [], now=T0)

    def test_refusal_saves_nothing(self):
        self.store.create("x", "pm", "a", now=T0)
        before = self.t()
        with self.assertRaises(chain.Refused):
            self.store.verdict("T-1", "PASS", "r", [], now=T0)  # still queued
        self.assertEqual(self.t(), before)

    def test_kick_back_to_earlier_stage(self):
        self.store.create("x", "pm", "a", now=T0)
        self.review(self.work_and_submit("pm"), "pm", "PASS")
        self.review(self.work_and_submit("ux"), "ux", "KICK_BACK", to_stage="pm")
        t = self.t()
        self.assertEqual((t["state"], t["stage"], t["kickbacks"]), ("queued", "pm", 1))

    def test_kick_back_to_later_stage_refused(self):
        self.store.create("x", "pm", "a", now=T0)
        ident = self.work_and_submit("pm")
        self.store.claim_next("pm", "a", "r", mode="review", now=T0)
        with self.assertRaises(chain.Refused):
            self.store.verdict(ident, "KICK_BACK", "r", [], to_stage="qa", now=T0)
        self.assertEqual(self.t()["state"], "reviewing")

    def test_kick_back_limit_escalates(self):
        """Claim: a ticket cannot bounce between roles forever."""
        self.store.create("x", "pm", "a", now=T0)
        for _ in range(3):  # limit is 2
            self.review(self.work_and_submit("pm"), "pm", "KICK_BACK")
        t = self.t()
        self.assertEqual(t["state"], "escalated")
        self.assertIn("kicked back 3 times", t["escalationReason"])

    def test_escalate_verdict(self):
        self.store.create("x", "pm", "a", now=T0)
        self.review(self.work_and_submit("pm"), "pm", "ESCALATE")
        self.assertEqual(self.t()["state"], "escalated")

    def test_veto_blocks_until_cleared_then_rereviewed(self):
        self.store.create("x", "pm", "a", now=T0)
        self.review(self.work_and_submit("pm"), "pm", "KICK_BACK", hits=["user harm"])
        self.assertEqual(self.t()["state"], "blocked")
        self.assertIsNone(self.store.claim_next("pm", "a", "w2", now=T0))
        with self.assertRaises(chain.Refused):
            self.store.verdict("T-1", "PASS", "r", [], now=T0)
        self.store.clear_veto("T-1", "Operator", "accepted", now=T0)
        self.assertEqual(self.t()["state"], "in_review")

    def test_done_refused_mid_chain(self):
        """Claim: `done` cannot skip remaining stages after an earlier PASS."""
        self.store.create("x", "pm", "a", now=T0)
        self.review(self.work_and_submit("pm"), "pm", "PASS")
        self.assertEqual(self.t()["verdict"], "PASS")
        with self.assertRaises(chain.Refused):
            self.store.close("T-1", override=False, now=T0)
        self.assertEqual(self.t()["state"], "queued")

    def test_resolve_returns_to_queue_and_resets_counters(self):
        self.store.create("x", "pm", "a", now=T0)
        self.review(self.work_and_submit("pm"), "pm", "ESCALATE")
        self.store.resolve("T-1", "Operator", "scope cut", now=T0)
        t = self.t()
        self.assertEqual((t["state"], t["kickbacks"], t["attempts"]), ("queued", 0, {}))


class RecoveryTest(ChainBase):
    def test_expired_work_lease_requeues(self):
        """Claim: work held by a dead agent returns to the queue."""
        self.store.create("x", "pm", "a", now=T0)
        self.store.claim_next("pm", "a", "dead", now=T0)
        evs = self.store.recover(now=T0 + 31 * MIN)
        t = self.t()
        self.assertEqual((t["state"], t["attempts"]["pm"]), ("queued", 1))
        self.assertEqual(evs[0]["kind"], "ticket.lease_expired")
        self.assertIsNotNone(self.store.claim_next("pm", "a", "alive", now=T0 + 32 * MIN))

    def test_recovery_runs_on_claim(self):
        """Claim: no scheduler is needed; the next claim recovers stuck work."""
        self.store.create("x", "pm", "a", now=T0)
        self.store.claim_next("pm", "a", "dead", now=T0)
        got = self.store.claim_next("pm", "a", "alive", now=T0 + 31 * MIN)
        self.assertEqual(got["claimedBy"], "alive")

    def test_heartbeat_prevents_expiry(self):
        self.store.create("x", "pm", "a", now=T0)
        self.store.claim_next("pm", "a", "w", now=T0)
        self.store.heartbeat("T-1", "w", now=T0 + 20 * MIN)
        self.store.recover(now=T0 + 40 * MIN)
        self.assertEqual(self.t()["state"], "working")

    def test_repeated_expiry_escalates(self):
        """Claim: a stage that keeps killing agents goes to a human."""
        self.store.create("x", "pm", "a", now=T0)
        now = T0
        for _ in range(3):
            self.store.claim_next("pm", "a", "flaky", now=now)
            now += 31 * MIN
            self.store.recover(now=now)
        t = self.t()
        self.assertEqual(t["state"], "escalated")
        self.assertIn("lease expired 3 times", t["escalationReason"])

    def test_expired_review_lease_returns_to_review(self):
        self.store.create("x", "pm", "a", now=T0)
        self.work_and_submit("pm")
        self.store.claim_next("pm", "a", "dead-reviewer", mode="review", now=T0)
        self.store.recover(now=T0 + 31 * MIN)
        t = self.t()
        self.assertEqual((t["state"], t["reviewAttempts"]), ("in_review", 1))

    def test_stalled_queue_alerts_once_per_window_without_state_change(self):
        self.store.create("x", "pm", "a", now=T0)
        first = self.store.recover(now=T0 + 241 * MIN)
        again = self.store.recover(now=T0 + 250 * MIN)
        later = self.store.recover(now=T0 + 482 * MIN)
        self.assertEqual([e["kind"] for e in first], ["ticket.stalled"])
        self.assertEqual(again, [])
        self.assertEqual([e["kind"] for e in later], ["ticket.stalled"])
        self.assertEqual(self.t()["state"], "queued")

    def test_stalled_review_alerts(self):
        self.store.create("x", "pm", "a", now=T0)
        self.work_and_submit("pm")
        evs = self.store.recover(now=T0 + 121 * MIN)
        self.assertEqual(evs[0]["data"]["waiting_for"], "reviewer")


class CompatTest(ChainBase):
    def test_pre_1_1_ticket_file_is_upgraded(self):
        legacy = [
            {"identifier": "T-1", "title": "old", "role": "ux", "status": "in_review",
             "lastActivityAt": chain.iso(T0)},
            {"identifier": "T-2", "title": "older", "role": "qa", "status": "done",
             "lastActivityAt": chain.iso(T0)},
        ]
        self.store.ticket_file.write_text(json.dumps(legacy))
        t1, t2 = self.store.load()
        self.assertEqual((t1["state"], t1["stages"]), ("in_review", ["ux"]))
        self.assertEqual(t2["state"], "done")
        self.store.verdict("T-1", "PASS", None, [], now=T0)  # legacy CLI path, no agent
        self.assertEqual(self.t("T-1")["state"], "done")

    def test_watchdog_only_reads_tickets_in_review(self):
        """Claim: done / queued / blocked tickets are never reported as stuck reviews."""
        import time
        old = time.time() - 600 * MIN  # the watchdog reads the real clock
        self.store.create("queued", "pm", "a", now=old)
        self.store.create("in review", "pm", "a", queued=False, now=old)
        self.store.create("done", "pm", "a", queued=False, now=old)
        self.store.verdict("T-3", "PASS", None, [], now=old)
        out = subprocess.run(
            [sys.executable, str(SCRIPTS / "stuck-review-watchdog.py"), "--source", "file",
             "--issues-file", str(self.store.ticket_file), "--stale-minutes", "120",
             "--dry-run", "--json"],
            capture_output=True, text=True, timeout=30,
            env=dict(os.environ, STUCK_STATE_FILE=str(Path(self._tmp.name) / "wd.json")),
        )
        self.assertEqual(out.returncode, 0, out.stderr)
        ids = [t["identifier"] for t in json.loads(out.stdout)["tickets"]]
        self.assertEqual(ids, ["T-2"])


class CliTest(unittest.TestCase):
    def test_cli_agent_loop_and_resolve_needs_approval(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "runs").mkdir()
            env = {k: v for k, v in os.environ.items() if k not in ("AG_APPROVAL", "AG_APPROVAL_TOKEN")}
            env.update(TICKET_FILE=str(root / "t.json"), VERDICT_LOG=str(root / "v.jsonl"),
                       EVENT_LOG=str(root / "e.jsonl"), ADVERSARIAL_ROOT=str(root))

            def run(*a):
                return subprocess.run([sys.executable, str(SCRIPTS / "ticket.py"), *a],
                                      env=env, capture_output=True, text=True, timeout=30)

            self.assertEqual(run("new", "x", "--queue", "--role", "qa", "--team", "a").returncode, 0)
            self.assertEqual(run("claim", "--role", "qa", "--team", "a", "--agent", "w").returncode, 0)
            self.assertEqual(run("submit", "T-1", "--agent", "w").returncode, 0)
            self.assertEqual(run("claim", "--role", "qa", "--team", "a", "--agent", "r", "--mode", "review").returncode, 0)
            self.assertEqual(run("verdict", "T-1", "ESCALATE", "--agent", "r").returncode, 0)
            refused = run("resolve", "T-1", "--by", "Op", "--reason", "x")
            self.assertEqual(refused.returncode, 2, refused.stderr)
            (root / "runs" / "approval.ok").write_text("")
            self.assertEqual(run("resolve", "T-1", "--by", "Op", "--reason", "x").returncode, 0)
            self.assertIn("[queued]", run("list").stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)

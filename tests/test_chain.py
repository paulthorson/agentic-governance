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
        self.store.claim_next("ux", "", "ux-critic", mode="review", now=T0)
        self.store.verdict("T-1", "PASS", "ux-critic", [], now=T0)
        self.assertEqual(self.t("T-1")["state"], "done")

    def test_watchdog_only_reads_tickets_in_review(self):
        """Claim: done / queued / blocked tickets are never reported as stuck reviews."""
        import time
        old = time.time() - 600 * MIN  # the watchdog reads the real clock
        self.store.create("queued", "pm", "a", now=old)
        self.store.create("in review", "pm", "a", queued=False, now=old)
        self.store.create("done", "pm", "a", queued=False, now=old)
        self.store.claim_next("pm", "a", "r", mode="review", now=old)  # oldest in review: T-2
        self.store.verdict("T-2", "PASS", "r", [], now=old)
        self.store.claim_next("pm", "a", "r", mode="review", now=old)
        out = subprocess.run(
            [sys.executable, str(SCRIPTS / "stuck-review-watchdog.py"), "--source", "file",
             "--issues-file", str(self.store.ticket_file), "--stale-minutes", "120",
             "--dry-run", "--json"],
            capture_output=True, text=True, timeout=30,
            env=dict(os.environ, STUCK_STATE_FILE=str(Path(self._tmp.name) / "wd.json")),
        )
        self.assertEqual(out.returncode, 0, out.stderr)
        ids = [t["identifier"] for t in json.loads(out.stdout)["tickets"]]
        # T-1 queued, T-2 done, T-3 being reviewed (status in_review, stale) -> only T-3
        self.assertEqual(ids, ["T-3"])


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


class ReviewFindingsTest(ChainBase):
    """Regression tests for the 1.1 pre-merge review."""

    def test_verdict_without_agent_refused(self):
        """Claim: every verdict names a reviewer; an empty id cannot self-review."""
        self.store.create("x", "pm", "a", now=T0)
        self.work_and_submit("pm", worker="w")
        for anon in (None, ""):
            with self.assertRaises(chain.Refused):
                self.store.verdict("T-1", "PASS", anon, [], now=T0)
        self.assertEqual(self.t()["state"], "in_review")

    def test_verdict_requires_review_claim(self):
        """Claim: a verdict inherits the review claim's team and stage scope."""
        self.store.create("x", "engineer", "team-a", end_stage="engineer", now=T0)
        self.work_and_submit("engineer", team="team-a")
        with self.assertRaises(chain.Refused):
            self.store.verdict("T-1", "PASS", "ux-critic-team-b", [], now=T0)
        self.assertIsNone(self.store.claim_next("engineer", "team-b", "ux-critic-team-b", mode="review", now=T0))
        self.assertEqual(self.t()["state"], "in_review")

    def test_event_written_before_save_and_uses_transition_time(self):
        self.store.create("x", "pm", "a", now=T0)
        with mock.patch.object(chain.events, "emit_at", side_effect=events.LockTimeout("boom")):
            with self.assertRaises(events.LockTimeout):
                self.store.claim_next("pm", "a", "w", now=T0 + MIN)
        self.assertEqual(self.t()["state"], "queued")  # nothing saved without its event
        self.store.claim_next("pm", "a", "w", now=T0 + MIN)
        claimed = [e for e in events.read_events(self.store.event_log) if e["kind"] == "ticket.claimed"][0]
        self.assertEqual(claimed["ts"], int((T0 + MIN) * 1000))

    def test_gate_runs_only_after_validation(self):
        """Claim: a mistyped id or wrong state never consumes an approval."""
        self.store.create("x", "pm", "a", now=T0)
        calls = []
        gate = lambda: calls.append(1)  # noqa: E731
        with self.assertRaises(KeyError):
            self.store.clear_veto("T-9", "Op", "r", now=T0, gate=gate)
        with self.assertRaises(chain.Refused):
            self.store.resolve("T-1", "Op", "r", now=T0, gate=gate)  # not escalated
        with self.assertRaises(chain.Refused):
            self.store.clear_veto("T-1", "Op", "r", now=T0, gate=gate)  # no veto
        self.assertEqual(calls, [])

    def test_escalation_raised_during_claim_still_reported(self):
        """Claim: tickets waiting on a human are reported, wherever they escalated."""
        self.store.settings.max_attempts = 1
        self.store.create("x", "pm", "a", now=T0)
        self.store.claim_next("pm", "a", "dead", now=T0)
        self.store.claim_next("pm", "a", "other", now=T0 + 31 * MIN)  # recovery escalates here
        self.assertEqual(self.t()["state"], "escalated")
        first = self.store.recover(now=T0 + 32 * MIN)
        self.assertEqual([e["kind"] for e in first], ["ticket.awaiting_human"])
        self.assertEqual(self.store.recover(now=T0 + 40 * MIN), [])
        self.assertEqual([e["kind"] for e in self.store.recover(now=T0 + 160 * MIN)], ["ticket.awaiting_human"])

    def test_blocked_ticket_reported(self):
        self.store.create("x", "pm", "a", now=T0)
        self.review(self.work_and_submit("pm"), "pm", "KICK_BACK", hits=["user harm"])
        self.assertEqual(self.store.recover(now=T0 + MIN)[0]["data"]["reason"], "open veto")

    def test_corrupt_store_is_never_overwritten(self):
        self.store.create("x", "pm", "a", now=T0)
        self.store.ticket_file.write_text('[{"identifier": "T-1", "title": "tr')
        before = self.store.ticket_file.read_text()
        # 1.2: the integrity check sees the edit before the parser does.
        with self.assertRaises((chain.StoreCorrupt, chain.integrity.TamperDetected)):
            self.store.create("y", "pm", "a", now=T0)
        self.assertEqual(self.store.ticket_file.read_text(), before)

    def test_legacy_open_veto_survives_upgrade(self):
        self.store.ticket_file.write_text(json.dumps([
            {"identifier": "T-1", "title": "old", "role": "ux", "status": "in_review",
             "lastActivityAt": chain.iso(T0)}]))
        self.store.verdict_log.write_text(json.dumps(
            {"kind": "verdict", "ticket": "T-1", "verdict": "KICK_BACK", "veto_triggered": True,
             "veto_hits": ["user harm"], "ts": 1}) + "\n")
        t = self.store.load()[0]
        self.assertEqual((t["state"], t["veto_open"]), ("blocked", True))

    def test_to_stage_only_on_kick_back(self):
        self.store.create("x", "pm", "a", now=T0)
        self.work_and_submit("pm")
        self.store.claim_next("pm", "a", "r", mode="review", now=T0)
        with self.assertRaises(chain.Refused):
            self.store.verdict("T-1", "PASS", "r", [], to_stage="pm", now=T0)

    def test_bad_end_stage_message(self):
        with self.assertRaisesRegex(ValueError, "not a chain stage"):
            self.store.create("x", "pm", "a", end_stage="qaa", now=T0)
        with self.assertRaisesRegex(ValueError, "only applies"):
            self.store.create("x", "security", "a", end_stage="qa", now=T0)

    def test_kick_back_gives_fresh_lease_attempts(self):
        self.store.create("x", "pm", "a", now=T0)
        self.store.claim_next("pm", "a", "dead", now=T0)
        self.store.recover(now=T0 + 31 * MIN)
        self.assertEqual(self.t()["attempts"]["pm"], 1)
        self.review(self.work_and_submit("pm", now=T0 + 32 * MIN), "pm", "KICK_BACK", now=T0 + 33 * MIN)
        self.assertNotIn("pm", self.t()["attempts"])

    def test_lock_holder_never_deletes_a_lock_it_lost(self):
        lock = self.store.ticket_file.with_name("in_review.json.lock")
        with events.file_lock(self.store.ticket_file):
            lock.write_text("someone else\n")  # simulate: our lock was broken and re-taken
        self.assertTrue(lock.exists())
        lock.unlink()


class McpSurfaceTest(unittest.TestCase):
    def test_human_only_actions_not_exposed_over_mcp(self):
        """Claim: an MCP agent cannot clear a veto, resolve an escalation, or force a close."""
        src = (REPO_ROOT / "mcp" / "adversarial_mcp" / "server.py").read_text(encoding="utf-8")
        tools = set()
        lines = src.splitlines()
        for i, line in enumerate(lines):
            if line.strip() == "@mcp.tool()":
                tools.add(lines[i + 1].split("def ", 1)[1].split("(", 1)[0])
        self.assertIn("ticket_verdict", tools)
        for name in tools:
            self.assertNotRegex(name, r"clear|veto_clear|resolve|override|close|done")

    def test_mcp_verdict_log_honors_env(self):
        src = (REPO_ROOT / "mcp" / "adversarial_mcp" / "server.py").read_text(encoding="utf-8")
        self.assertIn('VERDICT_LOG = Path(os.environ.get("VERDICT_LOG"', src)


class DeliverableTest(ChainBase):
    """1.2.1: the work and the reasons travel on the ticket (pilot findings)."""

    def test_reviewer_sees_the_deliverable(self):
        self.store.create("x", "pm", "a", now=T0)
        self.store.claim_next("pm", "a", "w", now=T0)
        self.store.submit("T-1", "w", "one line", now=T0, deliverable="the full paragraph")
        got = self.store.claim_next("pm", "a", "r", mode="review", now=T0)
        sub = got["submission"]
        self.assertEqual((sub["by"], sub["deliverable"], sub["stage"]), ("w", "the full paragraph", "pm"))
        self.assertEqual(self.t()["submission"]["summary"], "one line")  # stored, for the operator
        ev = [e for e in events.read_events(self.store.event_log) if e["kind"] == "ticket.submitted"][0]
        self.assertEqual(ev["data"]["deliverable"], "the full paragraph")

    def test_worker_sees_kick_back_reasons_on_reclaim(self):
        """Claim: a worker reclaiming a kicked-back ticket sees who decided and why."""
        self.store.create("x", "pm", "a", now=T0)
        self.store.claim_next("pm", "a", "w", now=T0)
        self.store.submit("T-1", "w", now=T0, deliverable="draft")
        self.store.claim_next("pm", "a", "r", mode="review", now=T0)
        self.store.verdict("T-1", "KICK_BACK", "r", [], summary="fix the second sentence", now=T0)
        got = self.store.claim_next("pm", "a", "w", now=T0 + 1)
        lv = got["lastVerdict"]
        self.assertEqual((lv["verdict"], lv["by"], lv["summary"], lv["to_stage"]),
                         ("KICK_BACK", "r", "fix the second sentence", "pm"))
        self.assertEqual(got["submission"]["deliverable"], "draft")  # previous round, for reference

    def test_oversized_deliverable_refused(self):
        self.store.create("x", "pm", "a", now=T0)
        self.store.claim_next("pm", "a", "w", now=T0)
        with self.assertRaises(chain.Refused):
            self.store.submit("T-1", "w", now=T0, deliverable="x" * (chain.DELIVERABLE_MAX_BYTES + 1))
        self.assertEqual(self.t()["state"], "working")

    def test_review_claim_is_blind(self):
        """AGENTS.md rule 1: a reviewer never gets the worker's pitch or an
        earlier reviewer's verdict, only the work."""
        self.store.create("x", "pm", "a", now=T0)
        self.store.claim_next("pm", "a", "w", now=T0)
        self.store.submit("T-1", "w", "this is great, ship it", now=T0, deliverable="v1")
        self.store.claim_next("pm", "a", "r1", mode="review", now=T0)
        self.store.verdict("T-1", "KICK_BACK", "r1", [], summary="weak opening", now=T0)
        self.store.claim_next("pm", "a", "w", now=T0 + 1)
        self.store.submit("T-1", "w", "fixed everything", now=T0 + 1, deliverable="v2")
        got = self.store.claim_next("pm", "a", "r2", mode="review", now=T0 + 2)
        self.assertNotIn("summary", got["submission"])
        self.assertNotIn("lastVerdict", got)
        self.assertEqual(got["submission"]["deliverable"], "v2")
        self.assertNotIn("fixed everything", json.dumps(got))
        self.assertNotIn("weak opening", json.dumps(got))

    def test_deliverable_cap_counts_bytes(self):
        self.store.create("x", "pm", "a", now=T0)
        self.store.claim_next("pm", "a", "w", now=T0)
        with self.assertRaises(chain.Refused):  # 4 bytes per character in UTF-8
            self.store.submit("T-1", "w", now=T0, deliverable="\U0001F600" * (chain.DELIVERABLE_MAX_BYTES // 4 + 1))

    def test_long_summaries_refused(self):
        self.store.create("x", "pm", "a", now=T0)
        self.store.claim_next("pm", "a", "w", now=T0)
        with self.assertRaises(chain.Refused):
            self.store.submit("T-1", "w", "s" * (chain.SUMMARY_MAX_CHARS + 1), now=T0)
        self.store.submit("T-1", "w", now=T0)
        self.store.claim_next("pm", "a", "r", mode="review", now=T0)
        with self.assertRaises(chain.Refused):
            self.store.verdict("T-1", "PASS", "r", [], summary="s" * (chain.SUMMARY_MAX_CHARS + 1), now=T0)
        self.assertEqual(self.t()["state"], "reviewing")

    def test_cli_show_prints_deliverable_and_reasons(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "runs").mkdir()
            env = {k: v for k, v in os.environ.items() if k not in ("AG_APPROVAL", "AG_APPROVAL_TOKEN")}
            env.update(TICKET_FILE=str(root / "t.json"), VERDICT_LOG=str(root / "v.jsonl"),
                       EVENT_LOG=str(root / "e.jsonl"), ADVERSARIAL_ROOT=str(root))

            def run(*a):
                return subprocess.run([sys.executable, str(SCRIPTS / "ticket.py"), *a],
                                      env=env, capture_output=True, text=True, timeout=30)

            (root / "work.md").write_text("line one\nline two\n")
            run("new", "x", "--queue", "--role", "qa", "--team", "a")
            run("claim", "--role", "qa", "--team", "a", "--agent", "w")
            self.assertEqual(run("submit", "T-1", "--agent", "w", "--deliverable-file", str(root / "work.md")).returncode, 0)
            run("claim", "--role", "qa", "--team", "a", "--agent", "r", "--mode", "review")
            run("verdict", "T-1", "KICK_BACK", "--agent", "r", "--summary", "tighten line two")
            out = run("show", "T-1").stdout
            self.assertIn("| line two", out)
            self.assertIn("reasons: tighten line two", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)

"""Test suite for the adversarial-agents framework.

Runs the structure validator and exercises the MCP server's tools
in-process (no network, no external LLM). Designed to run in CI.

Run:  python3 -m pytest tests/ -q
  or: python3 tests/test_framework.py
"""

import os
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "mcp"))
sys.path.insert(0, str(REPO_ROOT))

os.environ.setdefault("ADVERSARIAL_ROOT", str(REPO_ROOT))

from adversarial_mcp import server as mcp_server  # noqa: E402

DOMAINS = mcp_server.list_domains()  # derived from the server, not hardcoded


class TestStructure(unittest.TestCase):
    """The repo must pass the structure validator."""

    def test_validator_passes(self):
        import subprocess

        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "validate.py")],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("VALIDATION PASSED", result.stdout)


class TestFrameworkDiscovery(unittest.TestCase):
    def test_all_domains_present(self):
        self.assertEqual(mcp_server.list_domains(), DOMAINS)

    def test_each_domain_has_agents(self):
        for d in DOMAINS:
            agents = mcp_server.list_agents(d)
            self.assertGreaterEqual(len(agents), 1, f"{d} should have >=1 agent")

    def test_each_domain_has_skills(self):
        for d in DOMAINS:
            skills = mcp_server.list_skills(d)
            self.assertGreaterEqual(len(skills), 1, f"{d} should have >=1 skill")

    def test_constitution_exists_per_domain(self):
        for d in DOMAINS:
            c = mcp_server.get_constitution(d)
            self.assertNotIn("No constitution found", c, f"{d} missing constitution")

    def test_agent_lookup(self):
        body = mcp_server.get_agent("ux", "ux-critic")
        self.assertIn("critic", body.lower())


class TestReviewEngine(unittest.TestCase):
    def test_veto_detection_engineer(self):
        r = mcp_server.check_veto("engineer", "This change exposes an API key in logs.")
        self.assertTrue(r["veto_triggered"])
        # Should be caught by keyword and/or regex pattern, not just one literal.
        self.assertTrue(r["veto_hits"])

    def test_veto_detection_ux(self):
        r = mcp_server.check_veto("ux", "This flow is a dead end for screen readers.")
        self.assertTrue(r["veto_triggered"])
        self.assertIn("dead end", r["veto_hits"])

    def test_no_false_veto(self):
        r = mcp_server.check_veto("engineer", "Refactor the config loader for clarity.")
        self.assertFalse(r["veto_triggered"])

    def test_run_review_kicks_back_on_veto(self):
        r = mcp_server.run_review(
            "engineer", "Deploy change that leaks credentials to logs."
        )
        self.assertEqual(r["verdict"], "KICK_BACK")
        self.assertTrue(r["veto_triggered"])

    def test_run_review_assembles_prompt(self):
        r = mcp_server.run_review("ux", "A new onboarding flow for the glasses HUD.")
        self.assertIn("Adversarial review", r["review_prompt"])
        # The prompt lists the domain's agents by their frontmatter name.
        for a in mcp_server.list_agents("ux"):
            self.assertIn(a["name"], r["review_prompt"])


class TestVerdictRecord(unittest.TestCase):
    def setUp(self):
        self._log = mcp_server.VERDICT_LOG
        self._before = self._log.read_text().count("\n") if self._log.exists() else 0

    def test_record_and_query(self):
        mcp_server.record_verdict("qa", "KICK_BACK", "release-blocking defect", "T-1")
        rows = mcp_server.query_verdicts("qa", limit=10)
        self.assertTrue(any(r.get("ticket") == "T-1" for r in rows))

    def test_framework_status(self):
        st = mcp_server.framework_status()
        self.assertEqual(st["domains"], DOMAINS)
        self.assertIn("verdict_count", st)


if __name__ == "__main__":
    unittest.main(verbosity=2)

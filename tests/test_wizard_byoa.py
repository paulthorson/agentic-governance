"""Tests for the setup wizard's A6 BYOA adoption flow.

Covers: adopting an existing agent (A6.2), reconcile-never-layer (A6.3),
defining a new role with harness generation (A6.4), and the refuse-never-
overwrite rule (A6.5).

Run:  python3 -m pytest tests/test_wizard_byoa.py -q
   or: python3 tests/test_wizard_byoa.py
"""

import importlib.util
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WIZARD = REPO_ROOT / "mcp" / "adversarial_mcp" / "setup_wizard.py"

# Load the wizard module in isolation (it imports no MCP deps at module load).
_spec = importlib.util.spec_from_file_location("setup_wizard", WIZARD)
sw = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sw)


def _valid_answers():
    return {
        "runtime": "claude-code",
        "budget_model": "metered",
        "metered_allowance": "100",
        "metered_reset_cadence": "weekly",
        "metered_headroom": "20",
        "per_epic_budget": "30",
        "adversarial_agents": "in-play",
        "project_repos": "~/projects",
        "escalation_preferences": "none",
        "domain_risk": "none",
        "quiet_hours": "23:00-08:00",
        "stall_threshold": "3",
        "precedent_decay_window": "90d",
        "autonomy_starting_level": "1",
        "clean_runs_per_promotion": "3",
        "retry_count": "3",
        "retry_escalation_on_exhaustion": "escalate",
        "audit_cadence": "weekly",
        "research_rounds_without_findings": "3",
        "research_round_budget": "5",
        "irreversible_action_protection": "2",
    }


class WizardByoaTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "harnesses").mkdir(parents=True, exist_ok=True)
        (self.root / "harnesses" / "engineer.md").write_text(
            "# Engineer Harness\n\n## What you own\nYou own engineering. "
            "You never ship to production without review.\n"
        )

    def tearDown(self):
        self._tmp.cleanup()

    def _run_full_wizard(self, adopt_agent=True, define_role=True):
        """Drive the wizard to completion, returning the finalize result."""
        valid = _valid_answers()
        r = sw.start_wizard(self.root)
        roster_rows = 0
        adopt_done = False
        new_role_name = None
        steps = 0
        while r["status"] == "question" and steps < 60:
            qid = r["question_id"]
            steps += 1
            if qid == "roster":
                val = "bot1 | engineer | team-a | ~/proj" if roster_rows == 0 else "done"
                roster_rows = 1
            elif qid == "adopt_existing":
                if not adopt_done:
                    instr = self.root / "legacy-instructions.md"
                    instr.write_text(
                        "You are a data analyst. You never ship to production "
                        "without review. You use pandas.\n"
                    )
                    val = f"legacy-bot | data analysis | engineer | {instr}"
                    adopt_done = True
                else:
                    val = "done"
            elif qid == "define_new_role":
                if new_role_name is None:
                    val = "data-analyst"
                    new_role_name = "data-analyst"
                else:
                    val = "none"
            elif qid.startswith("new_role."):
                val = "field-answer"
            else:
                val = valid.get(qid, "x")
            r = sw.answer_wizard(self.root, val)
            if r["status"] == "complete":
                break
        return r

    def test_full_wizard_with_adoption_completes(self):
        r = self._run_full_wizard()
        self.assertEqual(r["status"], "complete")
        self.assertEqual(r["adopted_agents"], 1)
        self.assertEqual(r["roster_rows"], 1)
        self.assertIsNotNone(r["generated_harness"])
        # Adoption record written
        self.assertTrue((self.root / "config" / "adoption.md").exists())
        # Generated harness written
        self.assertTrue((self.root / "harnesses" / "data-analyst.md").exists())

    def test_reconcile_covered_line(self):
        # 'never ship to production without review' is in the engineer harness
        rec = sw._reconcile_instructions(
            "You never ship to production without review.\n", "engineer", self.root
        )
        self.assertEqual(len(rec["covered"]), 1)
        self.assertEqual(len(rec["conflicting"]), 0)

    def test_reconcile_conflict_detected(self):
        (self.root / "harnesses" / "qa.md").write_text(
            "# QA Harness\n\n## What you own\nYou verify against acceptance criteria.\n"
        )
        rec = sw._reconcile_instructions(
            "You never verify against acceptance criteria.\n", "qa", self.root
        )
        self.assertEqual(len(rec["conflicting"]), 1)
        self.assertIn("never verify", rec["conflicting"][0].lower())

    def test_generate_harness_refuses_overwrite(self):
        # A6.5: never overwrite an existing harness
        result = sw._generate_harness("engineer", {"role_identity": "x"}, self.root)
        self.assertIsNone(result)
        # And the existing file is untouched
        self.assertIn("You own engineering", (self.root / "harnesses" / "engineer.md").read_text())

    def test_generate_harness_creates_new(self):
        result = sw._generate_harness("data-analyst", {"role_identity": "id"}, self.root)
        self.assertIsNotNone(result)
        text = (self.root / "harnesses" / "data-analyst.md").read_text()
        # 9-section skeleton present
        for section in sw.HARNESS_SKELETON:
            self.assertIn(section, text)


if __name__ == "__main__":
    unittest.main(verbosity=2)

"""Tests for the setup wizard's BYODS (bring your own design system) step.

Covers: predefined codified design system selection, operator link with URL
validation, custom build (fonts, hex colors, starter-palette picker, CVD-safe
data-viz default, brand voice with deferred sample), default vs per-project
scope, and the design_system_palettes MCP helper data.

Run:  python3 -m pytest tests/test_wizard_byods.py -q
   or: python3 tests/test_wizard_byods.py
"""

import importlib.util
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WIZARD = REPO_ROOT / "mcp" / "adversarial_mcp" / "setup_wizard.py"

_spec = importlib.util.spec_from_file_location("setup_wizard", WIZARD)
sw = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sw)


def _base_answers(**over):
    a = {
        "runtime": "claude-code",
        "engine": "limen",
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
        "quiet_hours_p0_behavior": "defer",
        "daytime_sla_hours": "4",
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
        "network_permission": "deny",
        "alert_channel": "generic",
        "alert_command": "/tmp/alert.sh",
        "issue_source": "file",
        "issues_file": "/tmp/issues.json",
        "verdict_log": "/tmp/verdicts.jsonl",
        "multi_team": "no",
        "adopt_existing": "__DONE__",
        "define_new_role": "__SKIP__",
        "ds_detail": "quick (recommended)",
    }
    a.update(over)
    return a


def _answer_map(extra):
    """Answer function: base answers, then per-question overrides."""
    def _fn(qid):
        return extra.get(qid, _base_answers().get(qid, "x"))
    return _fn


def _drive(root, answer_fn, max_steps=80):
    r = sw.start_wizard(root)
    steps = 0
    roster_done = False
    while r["status"] == "question" and steps < max_steps:
        steps += 1
        qid = r["question_id"]
        if qid == "roster":
            val = "bot1 | engineer | team-a | ~/proj" if not roster_done else "done"
            roster_done = True
        elif qid == "adopt_existing":
            val = "done"
        elif qid == "define_new_role":
            val = "none"
        else:
            val = answer_fn(qid)
        r = sw.answer_wizard(root, val)
        if r["status"] != "question":
            break
    return r


class WizardByodsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_skip_writes_no_design_system(self):
        r = _drive(self.root, _answer_map({"design_system_source": "skip"}))
        self.assertEqual(r["status"], "complete")
        self.assertIsNone(r["wrote"]["design_system"])
        self.assertFalse((self.root / "config" / "design-system.md").exists())

    def test_predefined_preset_records_name_and_url(self):
        r = _drive(self.root, _answer_map({
            "design_system_source": "choose-predefined",
            "design_system_preset": "astryx",
            "ds_scope": "default",
        }))
        self.assertEqual(r["status"], "complete")
        p = self.root / "config" / "design-system.md"
        self.assertTrue(p.exists())
        text = p.read_text()
        self.assertIn("Source: choose-predefined", text)
        self.assertIn("preset: astryx", text)
        self.assertIn("https://github.com/facebook/astryx", text)
        self.assertIn("Scope: default", text)
        self.assertIn("advisory", text.lower())

    def test_link_requires_url(self):
        r = sw.start_wizard(self.root)
        # walk manually to the link question
        seen_link_q = False
        steps = 0
        roster_done = False
        while r["status"] == "question" and steps < 80:
            steps += 1
            qid = r["question_id"]
            if qid == "roster":
                val = "bot1 | engineer | team-a | ~/proj" if not roster_done else "done"
                roster_done = True
            elif qid == "adopt_existing":
                val = "done"
            elif qid == "define_new_role":
                val = "none"
            elif qid == "design_system_source":
                val = "i-have-a-link"
            elif qid == "design_system_link":
                seen_link_q = True
                r = sw.answer_wizard(self.root, "not-a-url")
                self.assertEqual(r["status"], "invalid")
                self.assertEqual(r.get("question"), "design_system_link")
                r = sw.answer_wizard(self.root, "https://example.com/design-system")
                continue
            elif qid == "ds_scope":
                val = "per-project"
            else:
                val = _answer_map({})(qid)
            r = sw.answer_wizard(self.root, val)
            if r["status"] != "question":
                break
        self.assertTrue(seen_link_q)
        self.assertEqual(r["status"], "complete")
        text = (self.root / "config" / "design-system.md").read_text()
        self.assertIn("https://example.com/design-system", text)
        self.assertIn("Scope: per-project", text)

    def test_custom_build_with_palette_help(self):
        r = _drive(self.root, _answer_map({
            "design_system_source": "build-custom",
            "ds_font_primary": "Inter (recommended)",
            "ds_font_secondary": "custom",
            "ds_font_secondary_custom": "Fraunces",
            "ds_color_primary": "help",
            "ds_palette_pick": "ocean",
            "ds_viz_palette": "okabe-ito (CVD-safe, recommended)",
            "ds_brand_voice": "direct-founder — plain-spoken, first person, no fluff",
            "ds_scope": "default",
        }))
        self.assertEqual(r["status"], "complete")
        text = (self.root / "config" / "design-system.md").read_text()
        self.assertIn("primary: Inter", text)
        self.assertIn("secondary: Fraunces", text)
        self.assertIn("#0B5FFF", text)
        self.assertIn("#00A6B6", text)
        self.assertIn("#FF6B4A", text)
        self.assertIn("Okabe", text)
        self.assertIn("direct-founder", text)

    def test_custom_build_explicit_hexes_rejects_bad_hex(self):
        r = sw.start_wizard(self.root)
        steps = 0
        roster_done = False
        bad_hex_rejected = False
        while r["status"] == "question" and steps < 80:
            steps += 1
            qid = r["question_id"]
            if qid == "roster":
                val = "bot1 | engineer | team-a | ~/proj" if not roster_done else "done"
                roster_done = True
            elif qid == "adopt_existing":
                val = "done"
            elif qid == "define_new_role":
                val = "none"
            elif qid == "design_system_source":
                val = "build-custom"
            elif qid == "ds_font_primary":
                val = "Roboto"
            elif qid == "ds_font_secondary":
                val = "Poppins"
            elif qid == "ds_color_primary":
                # first a bad hex -> invalid; then a good one
                r = sw.answer_wizard(self.root, "blue")
                self.assertEqual(r["status"], "invalid")
                self.assertEqual(r.get("question"), "ds_color_primary")
                bad_hex_rejected = True
                r = sw.answer_wizard(self.root, "#1B6DE0")
                continue
            elif qid == "ds_color_secondary":
                val = "#00A6B6"
            elif qid == "ds_color_tertiary":
                val = "#FF6B4A"
            elif qid == "ds_viz_palette":
                val = "custom"
            elif qid == "ds_viz_custom":
                val = "#E69F00, #56B4E9, #009E73"
            elif qid == "ds_brand_voice":
                val = "i-have-one-already"
            elif qid == "ds_brand_voice_sample":
                val = "later"
            elif qid == "ds_scope":
                val = "default"
            else:
                val = _answer_map({})(qid)
            r = sw.answer_wizard(self.root, val)
            if r["status"] != "question":
                break
        self.assertTrue(bad_hex_rejected)
        self.assertEqual(r["status"], "complete")
        text = (self.root / "config" / "design-system.md").read_text()
        self.assertIn("#1B6DE0", text)
        self.assertIn("#E69F00, #56B4E9, #009E73", text)
        self.assertIn("PENDING", text)

    def test_palette_primaries_are_text_safe_on_white(self):
        # WCAG AA: primary must be >= 4.5:1 on white. Verified at authoring;
        # re-assert here so a future palette edit can't silently break it.
        def lum(h):
            h = h.lstrip("#")
            r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
            f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
            return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

        def contrast(a, b):
            l1, l2 = sorted([lum(a), lum(b)], reverse=True)
            return (l1 + 0.05) / (l2 + 0.05)

        for pid, (name, phex, _s, _t) in sw.DS_PALETTES.items():
            self.assertGreaterEqual(
                contrast(phex, "#FFFFFF"), 4.5, f"palette {pid} primary fails WCAG AA"
            )

    def test_persona_references_design_system(self):
        _drive(self.root, _answer_map({
            "design_system_source": "choose-predefined",
            "design_system_preset": "material",
            "ds_scope": "default",
        }))
        persona = (self.root / "config" / "personas" / "bot1.md").read_text()
        self.assertIn("config/design-system.md", persona)

    def test_setup_md_summarizes_design_system(self):
        _drive(self.root, _answer_map({
            "design_system_source": "choose-predefined",
            "design_system_preset": "primer",
            "ds_scope": "per-project",
        }))
        setup = (self.root / "config" / "setup.md").read_text()
        self.assertIn("## Design system (BYODS)", setup)
        self.assertIn("preset: primer", setup)

    def test_brand_voice_options_include_six_styles_plus_owned(self):
        self.assertEqual(len(sw.BRAND_VOICES), 7)
        self.assertIn("i-have-one-already", sw.BRAND_VOICES)

    def test_presets_have_verified_urls(self):
        for pid, (name, url) in sw.DS_PRESETS.items():
            self.assertTrue(url.startswith("https://"), pid)
            self.assertTrue(name, pid)

    # --- BYODS detail tokens: quick vs define-each ---

    def _drive_with_overrides(self, extra):
        answered = {}

        def fn(qid):
            return extra.get(qid, _base_answers().get(qid, "x"))

        r = sw.start_wizard(self.root)
        steps = 0
        roster_done = False
        while r["status"] == "question" and steps < 120:
            steps += 1
            qid = r["question_id"]
            answered[qid] = True
            if qid == "roster":
                val = "bot1 | engineer | team-a | ~/proj" if not roster_done else "done"
                roster_done = True
            elif qid == "adopt_existing":
                val = "done"
            elif qid == "define_new_role":
                val = "none"
            else:
                val = fn(qid)
            r = sw.answer_wizard(self.root, val)
            if r["status"] != "question":
                break
        return r, answered

    def test_quick_setup_writes_recommended_tokens(self):
        import json

        r, answered = self._drive_with_overrides({
            "design_system_source": "build-custom",
            "ds_font_primary": "Inter (recommended)",
            "ds_font_secondary": "Space Grotesk",
            "ds_color_primary": "#1B6DE0",
            "ds_color_secondary": "#00A6B6",
            "ds_color_tertiary": "#FF6B4A",
            "ds_viz_palette": "okabe-ito (CVD-safe, recommended)",
            "ds_brand_voice": "warm-expert — knowledgeable, encouraging, jargon-free",
            "ds_scope": "default",
        })
        self.assertEqual(r["status"], "complete")
        # quick mode: no detail questions asked
        for qid in ("ds_neutral_style", "ds_radius", "ds_icons", "ds_type_scale",
                    "ds_spacing", "ds_shadows", "ds_motion", "ds_breakpoints"):
            self.assertNotIn(qid, answered, qid)
        tokens = json.loads((self.root / "config" / "design-tokens.json").read_text())
        self.assertEqual(tokens["source"], "build-custom")
        self.assertEqual(tokens["color"]["brand"]["primary"]["$value"], "#1B6DE0")
        self.assertEqual(tokens["color"]["neutral"]["style"], "cool-gray")
        self.assertEqual(tokens["color"]["neutral"]["light"]["bg"]["$value"], "#F8FAFC")
        self.assertIn("dark", tokens["color"]["neutral"])  # auto dark ramp
        self.assertTrue(tokens["color"]["dataViz"]["cvdSafe"])
        self.assertEqual(tokens["font"]["scale"]["$value"], [12, 14, 16, 20, 24, 32, 48])
        self.assertEqual(tokens["radius"]["$value"], "8px")
        self.assertEqual(tokens["icons"]["$value"], "lucide")
        self.assertEqual(tokens["breakpoints"]["$value"], [640, 768, 1024, 1280])
        # persona references the tokens file
        persona = (self.root / "config" / "personas" / "bot1.md").read_text()
        self.assertIn("config/design-tokens.json", persona)

    def test_define_each_with_customs(self):
        import json

        r, answered = self._drive_with_overrides({
            "design_system_source": "build-custom",
            "ds_font_primary": "Roboto",
            "ds_font_secondary": "Poppins",
            "ds_color_primary": "#1B6DE0",
            "ds_color_secondary": "#00A6B6",
            "ds_color_tertiary": "#FF6B4A",
            "ds_viz_palette": "okabe-ito (CVD-safe, recommended)",
            "ds_brand_voice": "minimal-luxury — quiet, precise, confident",
            "ds_detail": "define-each",
            "ds_neutral_style": "custom",
            "ds_neutral_custom": "#111111, #222222, #EEEEEE, #999999, #333333",
            "ds_dark_mode": "light-only",
            "ds_radius": "custom",
            "ds_radius_custom": "6px",
            "ds_icons": "custom",
            "ds_icons_custom": "https://example.com/icons",
            "ds_logo": "later",
            "ds_type_scale": "custom",
            "ds_type_scale_custom": "13, 15, 18, 24, 36",
            "ds_spacing": "4pt grid",
            "ds_shadows": "none",
            "ds_motion": "none",
            "ds_breakpoints": "custom",
            "ds_breakpoints_custom": "600, 900, 1200",
            "ds_scope": "per-project",
        })
        self.assertEqual(r["status"], "complete")
        for qid in ("ds_neutral_style", "ds_neutral_custom", "ds_radius_custom",
                    "ds_type_scale_custom", "ds_breakpoints_custom"):
            self.assertIn(qid, answered, qid)
        tokens = json.loads((self.root / "config" / "design-tokens.json").read_text())
        self.assertEqual(tokens["color"]["neutral"]["style"], "custom")
        self.assertEqual(tokens["color"]["neutral"]["light"]["bg"]["$value"], "#111111")
        self.assertNotIn("dark", tokens["color"]["neutral"])  # light-only
        self.assertEqual(tokens["radius"]["$value"], "6px")
        self.assertEqual(tokens["icons"]["$value"], "https://example.com/icons")
        self.assertEqual(tokens["logo"]["$value"],
                         "PENDING — ask for it at the first project kickoff")
        self.assertEqual(tokens["font"]["scale"]["$value"], [13, 15, 18, 24, 36])
        self.assertEqual(tokens["spacing"]["$value"], "4pt grid")
        self.assertEqual(tokens["breakpoints"]["$value"], [600, 900, 1200])
        md = (self.root / "config" / "design-system.md").read_text()
        self.assertIn("## Neutrals", md)
        self.assertIn("## Shape, icons, assets", md)
        self.assertIn("## Type & layout", md)
        self.assertIn("config/design-tokens.json", md)

    def test_detail_custom_validation(self):
        bad = {
            "ds_neutral_custom": ("#111111, #222222", "five comma-separated hex codes"),
            "ds_radius_custom": ("huge", "a radius like 6px"),
            "ds_type_scale_custom": ("big, bigger", "comma-separated pixel numbers"),
            "ds_breakpoints_custom": ("wide", "comma-separated pixel numbers"),
        }
        for qid, (bad_val, hint) in bad.items():
            with self.subTest(qid=qid):
                # fresh wizard state per subtest (state file persists in self.root)
                import shutil
                shutil.rmtree(self.root / "config", ignore_errors=True)
                parent = {
                    "ds_neutral_custom": ("ds_neutral_style", "custom"),
                    "ds_radius_custom": ("ds_radius", "custom"),
                    "ds_type_scale_custom": ("ds_type_scale", "custom"),
                    "ds_breakpoints_custom": ("ds_breakpoints", "custom"),
                }[qid]
                defaults = dict(_base_answers())
                defaults.update({
                    "design_system_source": "build-custom",
                    "ds_font_primary": "Roboto",
                    "ds_font_secondary": "Poppins",
                    "ds_color_primary": "#1B6DE0",
                    "ds_color_secondary": "#00A6B6",
                    "ds_color_tertiary": "#FF6B4A",
                    "ds_viz_palette": "okabe-ito (CVD-safe, recommended)",
                    "ds_brand_voice": "direct-founder — plain-spoken, first person, no fluff",
                    "ds_detail": "define-each",
                    "ds_neutral_style": "cool-gray (recommended)",
                    "ds_dark_mode": "auto (recommended) — light + dark ramps",
                    "ds_radius": "rounded (recommended) — 8px",
                    "ds_icons": "lucide (recommended)",
                    "ds_logo": "none",
                    "ds_type_scale": "recommended — 12/14/16/20/24/32/48px",
                    "ds_spacing": "8pt grid (recommended)",
                    "ds_shadows": "subtle (recommended)",
                    "ds_motion": "subtle (recommended) — 150–250ms ease-out, honors prefers-reduced-motion",
                    "ds_breakpoints": "recommended — 640/768/1024/1280px",
                    "ds_scope": "default",
                    parent[0]: parent[1],
                })
                # drive from scratch to the custom question under test
                r = sw.start_wizard(self.root)
                steps = 0
                roster_done = False
                while r["status"] == "question" and r["question_id"] != qid and steps < 120:
                    steps += 1
                    cq = r["question_id"]
                    if cq == "roster":
                        v = "bot1 | engineer | team-a | ~/proj" if not roster_done else "done"
                        roster_done = True
                    elif cq == "adopt_existing":
                        v = "done"
                    elif cq == "define_new_role":
                        v = "none"
                    else:
                        v = defaults.get(cq, "x")
                    r = sw.answer_wizard(self.root, v)
                self.assertEqual(r["status"], "question")
                self.assertEqual(r["question_id"], qid)
                r = sw.answer_wizard(self.root, bad_val)
                self.assertEqual(r["status"], "invalid", qid)
                self.assertIn(hint.split()[0], r["error"])

    def test_logo_none_and_dark_only(self):
        import json

        r, _ = self._drive_with_overrides({
            "design_system_source": "build-custom",
            "ds_font_primary": "Roboto",
            "ds_font_secondary": "Poppins",
            "ds_color_primary": "#1B6DE0",
            "ds_color_secondary": "#00A6B6",
            "ds_color_tertiary": "#FF6B4A",
            "ds_viz_palette": "okabe-ito (CVD-safe, recommended)",
            "ds_brand_voice": "direct-founder — plain-spoken, first person, no fluff",
            "ds_detail": "define-each",
            "ds_neutral_style": "warm-gray",
            "ds_dark_mode": "dark-only",
            "ds_radius": "sharp — 2px",
            "ds_icons": "heroicons",
            "ds_logo": "none",
            "ds_type_scale": "recommended — 12/14/16/20/24/32/48px",
            "ds_spacing": "8pt grid (recommended)",
            "ds_shadows": "subtle (recommended)",
            "ds_motion": "subtle (recommended) — 150–250ms ease-out, honors prefers-reduced-motion",
            "ds_breakpoints": "recommended — 640/768/1024/1280px",
            "ds_scope": "default",
        })
        self.assertEqual(r["status"], "complete")
        tokens = json.loads((self.root / "config" / "design-tokens.json").read_text())
        self.assertEqual(tokens["logo"]["$value"], "(none)")
        # dark-only: light ramp replaced by the dark ramp
        self.assertEqual(tokens["color"]["neutral"]["light"]["bg"]["$value"], "#1C1917")

    def test_predefined_source_writes_reference_tokens(self):
        import json

        r, _ = self._drive_with_overrides({
            "design_system_source": "choose-predefined",
            "design_system_preset": "carbon",
            "ds_scope": "default",
        })
        self.assertEqual(r["status"], "complete")
        tokens = json.loads((self.root / "config" / "design-tokens.json").read_text())
        self.assertEqual(tokens["externalReference"], "https://carbondesignsystem.com")


if __name__ == "__main__":
    unittest.main(verbosity=2)

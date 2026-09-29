"""Tests for the opt-in framework update check (mcp/adversarial_mcp/updates.py).

No network access: the fetcher and both gates are injected via test seams.
"""

import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_updates():
    path = REPO_ROOT / "mcp" / "adversarial_mcp" / "updates.py"
    spec = importlib.util.spec_from_file_location("ag_updates_under_test", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


updates = _load_updates()


def _changelog(version: str) -> str:
    return f"# Changelog\n\n## [{version}] - 2026-01-01\n\n### Added\n- thing\n"


class TestParseVersion(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(updates.parse_version("1.2.3"), (1, 2, 3))
        self.assertEqual(updates.parse_version(" 0.3.0 "), (0, 3, 0))

    def test_invalid(self):
        self.assertIsNone(updates.parse_version("abc"))
        self.assertIsNone(updates.parse_version("1.2"))
        self.assertIsNone(updates.parse_version("1.2.3.4"))


class TestChangelogParsing(unittest.TestCase):
    def test_first_heading_wins(self):
        text = "# Changelog\n\n## [Unreleased]\n\n## [0.2.0] - 2026-09-27\n"
        self.assertEqual(updates.latest_version_in_changelog(text), "0.2.0")

    def test_no_heading(self):
        self.assertIsNone(updates.latest_version_in_changelog("# nothing here\n"))


class TestVersionInSync(unittest.TestCase):
    def test_current_version_matches_changelog(self):
        text = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        latest = updates.latest_version_in_changelog(text)
        self.assertEqual(
            updates.CURRENT_VERSION,
            latest,
            "CURRENT_VERSION drifted from CHANGELOG.md — update both together",
        )


class TestOptIn(unittest.TestCase):
    def test_default_off(self):
        with tempfile.TemporaryDirectory() as td:
            self.assertFalse(updates.update_check_opted_in(Path(td)))

    def test_env_opt_in(self):
        with tempfile.TemporaryDirectory() as td:
            os.environ["AG_UPDATE_CHECK"] = "allow"
            try:
                self.assertTrue(updates.update_check_opted_in(Path(td)))
            finally:
                del os.environ["AG_UPDATE_CHECK"]

    def test_config_opt_in(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "config").mkdir()
            (root / "config" / "setup.md").write_text(
                "# Setup\n\n## Update checks\n\n- allow\n", encoding="utf-8"
            )
            self.assertTrue(updates.update_check_opted_in(root))

    def test_config_deny(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "config").mkdir()
            (root / "config" / "setup.md").write_text(
                "# Setup\n\n## Update checks\n\n- deny\n", encoding="utf-8"
            )
            self.assertFalse(updates.update_check_opted_in(root))


class TestCheckForUpdates(unittest.TestCase):
    def test_not_opted_in_skips_without_network(self):
        with tempfile.TemporaryDirectory() as td:
            def boom(url):
                raise AssertionError("must not touch the network")

            status = updates.check_for_updates(
                repo_root=Path(td), _fetcher=boom,
                _network_ok=True, _opted_in=False,
            )
            self.assertFalse(status["checked"])
            self.assertIn("opt-in", status["reason"])

    def test_network_denied_skips(self):
        with tempfile.TemporaryDirectory() as td:
            def boom(url):
                raise AssertionError("must not touch the network")

            status = updates.check_for_updates(
                repo_root=Path(td), _fetcher=boom,
                _network_ok=False, _opted_in=True,
            )
            self.assertFalse(status["checked"])
            self.assertFalse(status["update_available"])

    def test_newer_version_detected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            status = updates.check_for_updates(
                repo_root=root,
                _fetcher=lambda url: _changelog("9.9.9"),
                _network_ok=True, _opted_in=True,
            )
            self.assertTrue(status["checked"])
            self.assertTrue(status["update_available"])
            self.assertEqual(status["latest_version"], "9.9.9")
            self.assertEqual(status["current_version"], updates.CURRENT_VERSION)

    def test_up_to_date(self):
        with tempfile.TemporaryDirectory() as td:
            status = updates.check_for_updates(
                repo_root=Path(td),
                _fetcher=lambda url: _changelog(updates.CURRENT_VERSION),
                _network_ok=True, _opted_in=True,
            )
            self.assertTrue(status["checked"])
            self.assertFalse(status["update_available"])

    def test_fetch_failure_never_raises(self):
        with tempfile.TemporaryDirectory() as td:
            def fail(url):
                raise OSError("no route to host")

            status = updates.check_for_updates(
                repo_root=Path(td), _fetcher=fail,
                _network_ok=True, _opted_in=True,
            )
            self.assertFalse(status["checked"])
            self.assertIn("reason", status)

    def test_cache_hit_avoids_network(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            first = updates.check_for_updates(
                repo_root=root,
                _fetcher=lambda url: _changelog("9.9.9"),
                _network_ok=True, _opted_in=True,
            )
            self.assertTrue(first["checked"])
            cache_file = root / "runs" / "update-check.json"
            self.assertTrue(cache_file.exists())
            cached_payload = json.loads(cache_file.read_text(encoding="utf-8"))

            def boom(url):
                raise AssertionError("cache should have been used")

            second = updates.check_for_updates(
                repo_root=root, _fetcher=boom,
                _network_ok=True, _opted_in=True,
            )
            self.assertTrue(second.get("cached"))
            self.assertEqual(second["latest_version"], cached_payload["latest_version"])

    def test_force_bypasses_cache(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            updates.check_for_updates(
                repo_root=root,
                _fetcher=lambda url: _changelog("9.9.9"),
                _network_ok=True, _opted_in=True,
            )
            status = updates.check_for_updates(
                force=True, repo_root=root,
                _fetcher=lambda url: _changelog(updates.CURRENT_VERSION),
                _network_ok=True, _opted_in=True,
            )
            self.assertFalse(status.get("cached"))
            self.assertFalse(status["update_available"])


if __name__ == "__main__":
    sys.path.insert(0, str(REPO_ROOT / "tests"))
    unittest.main(verbosity=2)

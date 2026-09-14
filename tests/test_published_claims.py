"""Tests encode published claims; removing one means a doc claim became false.

This module is the contract between public docs and code behavior after the
release hardening pass. Each assertion maps to a claim operators are
allowed to believe. If a test here is deleted, a corresponding README /
SECURITY / capability-report sentence must be removed or rewritten — never
left as an unbacked claim.
"""

from __future__ import annotations

import ast
import importlib.util
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


class TestPublishedClaims(unittest.TestCase):
    """Contract tests for claims published after capability-report alignment."""

    def test_uvicorn_default_bind_is_loopback(self):
        """Claim: MCP HTTP transport defaults to 127.0.0.1, not 0.0.0.0."""
        src = (REPO_ROOT / "mcp" / "adversarial_mcp" / "server.py").read_text(
            encoding="utf-8"
        )
        tree = ast.parse(src)
        # Find main()'s argparse --host default and uvicorn.run host=args.host
        found_host_default = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # ap.add_argument("--host", default="127.0.0.1", ...)
                if (
                    isinstance(node.func, ast.Attribute)
                    and node.func.attr == "add_argument"
                ):
                    args = []
                    for a in node.args:
                        if isinstance(a, ast.Constant) and isinstance(a.value, str):
                            args.append(a.value)
                    if "--host" in args:
                        for kw in node.keywords:
                            if kw.arg == "default" and isinstance(kw.value, ast.Constant):
                                self.assertEqual(kw.value.value, "127.0.0.1")
                                found_host_default = True
        self.assertTrue(found_host_default, "--host default 127.0.0.1 not found")
        self.assertNotIn('host="0.0.0.0"', src)
        self.assertNotIn("host='0.0.0.0'", src)

    def test_wizard_unknown_network_permits_no_egress(self):
        """Claim: network_permission unknown/deny/missing → messaging no egress."""
        messaging = _load("messaging_contract", REPO_ROOT / "scripts" / "messaging.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "config").mkdir()
            # missing setup
            self.assertEqual(messaging.load_network_permission(root), "unknown")
            self.assertFalse(messaging.network_permits_egress(root))
            (root / "config" / "setup.md").write_text(
                "## Network permission\n- unknown\n", encoding="utf-8"
            )
            self.assertFalse(messaging.network_permits_egress(root))
            (root / "config" / "setup.md").write_text(
                "## Network permission\n- deny\n", encoding="utf-8"
            )
            self.assertFalse(messaging.network_permits_egress(root))
            (root / "config" / "setup.md").write_text(
                "## Network permission\n- allow\n", encoding="utf-8"
            )
            self.assertTrue(messaging.network_permits_egress(root))

        # Wizard exposes the question with unknown as an option
        wizard = _load(
            "setup_wizard_contract",
            REPO_ROOT / "mcp" / "adversarial_mcp" / "setup_wizard.py",
        )
        self.assertIn("unknown", wizard.NETWORK_PERMISSIONS)
        ids = [q["id"] for q in wizard.WIZARD_FLOW]
        self.assertIn("network_permission", ids)

    def test_spend_enforcement_refuses_at_cap(self):
        """Claim: framework-unit meter refuses when recorded units meet cap."""
        spend = _load("spend_contract", REPO_ROOT / "mcp" / "adversarial_mcp" / "spend.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "config").mkdir()
            (root / "config" / "setup.md").write_text(
                "## Budget model\n- billed\n\n### Billed\n"
                "- total spend cap: 1\n"
                "- escalation threshold (% of cap): 100\n",
                encoding="utf-8",
            )
            spend.record_usage(1.0, source="test", repo_root=root)
            with self.assertRaises(spend.SpendCapExceeded):
                spend.refuse_if_over_cap(root, pending_units=0.0)

    def test_approval_checkpoints_block_without_approval(self):
        """Claim: gated actions refuse without AG_APPROVAL / approval.ok."""
        approval = _load("approval_contract", REPO_ROOT / "scripts" / "approval.py")
        prev = os.environ.pop("AG_APPROVAL", None)
        os.environ.pop("AG_APPROVAL_TOKEN", None)
        try:
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root / "runs").mkdir()
                self.assertFalse(approval.has_approval(root))
                with self.assertRaises(approval.ApprovalRequired):
                    approval.require_approval("git_apply", root)
                os.environ["AG_APPROVAL"] = "1"
                approval.require_approval("git_apply", root)
        finally:
            if prev is None:
                os.environ.pop("AG_APPROVAL", None)
            else:
                os.environ["AG_APPROVAL"] = prev

    def test_no_shipped_config_contains_real_credential(self):
        """Claim: shipped example/env templates do not embed real secrets."""
        suspects = [
            REPO_ROOT / "dashboard" / ".env.example",
        ]
        secretish = re.compile(
            r"(?i)(api[_-]?key|secret|token|password)\s*=\s*['\"]?[^\s'\"]{20,}"
        )
        placeholder = re.compile(
            r"(?i)(change.?me|your_|xxx|todo|example|placeholder|<.*>|\.\.\.)"
        )
        for path in suspects:
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            for line in text.splitlines():
                if not line.strip() or line.strip().startswith("#"):
                    continue
                if "=" not in line:
                    continue
                _, _, val = line.partition("=")
                val = val.strip().strip("'").strip('"')
                if not val:
                    continue  # empty value = placeholder
                # Non-empty secret-looking values must look like placeholders
                if secretish.search(line) and not placeholder.search(val):
                    self.fail(f"possible real credential in {path}: {line}")

        # .env.example AUTH_* must be empty
        env_ex = REPO_ROOT / "dashboard" / ".env.example"
        if env_ex.exists():
            for line in env_ex.read_text(encoding="utf-8").splitlines():
                if line.startswith(("AUTH_SECRET=", "AUTH_GOOGLE_ID=", "AUTH_GOOGLE_SECRET=")):
                    self.assertTrue(
                        line.endswith("=") or line.split("=", 1)[1].strip() == "",
                        f"non-empty auth secret in example: {line}",
                    )

    def test_no_git_identity_config_uses_non_noreply_email(self):
        """Claim: no shipped config sets git author/committer to a non-noreply address.

        Allowed address when a setter exists: paulthorson@users.noreply.github.com.
        Today there are no setters; this test fails if one appears with another email.
        """
        setter_re = re.compile(
            r"(?:git\s+config\b[^\n]*\buser\.email\b"
            r"|\bGIT_AUTHOR_EMAIL\s*="
            r"|\bGIT_COMMITTER_EMAIL\s*="
            r"|\buser\.email\s*=)",
            re.IGNORECASE,
        )
        email_re = re.compile(r"[\w.+-]+@[\w.-]+\.\w+")
        allow = "paulthorson@users.noreply.github.com"
        hits = []
        for dp, dns, fns in os.walk(REPO_ROOT):
            dns[:] = [d for d in dns if d not in {".git", "node_modules", ".venv"}]
            for fn in fns:
                if not fn.endswith(
                    (".py", ".md", ".yml", ".yaml", ".sh", ".json", ".toml", ".mjs", ".ts")
                ):
                    continue
                path = Path(dp) / fn
                # Skip this contract file — it mentions the patterns under test.
                if path.resolve() == Path(__file__).resolve():
                    continue
                try:
                    text = path.read_text(encoding="utf-8")
                except (OSError, UnicodeDecodeError):
                    continue
                for m in setter_re.finditer(text):
                    start = text.rfind("\n", 0, m.start()) + 1
                    end = text.find("\n", m.end())
                    line = text[start : end if end != -1 else None]
                    emails = email_re.findall(line)
                    for em in emails:
                        if em.lower() != allow.lower():
                            hits.append(f"{path}:{line.strip()}")
        self.assertEqual(
            hits,
            [],
            "git identity config references non-noreply email: " + "; ".join(hits),
        )

    def test_spend_qualifier_adjacent_on_numeric_wizard_prompts(self):
        """Claim: every wizard spend-number prompt includes the unit qualifier."""
        wizard = _load(
            "setup_wizard_q",
            REPO_ROOT / "mcp" / "adversarial_mcp" / "setup_wizard.py",
        )
        needle = wizard.SPEND_UNIT_QUALIFIER
        for qid in (
            "budget_model",
            "metered_allowance",
            "metered_headroom",
            "billed_cap",
            "billed_escalation_threshold",
            "per_epic_budget",
        ):
            q = next(x for x in wizard.WIZARD_FLOW if x["id"] == qid)
            self.assertIn(needle, q["question"], f"{qid} missing spend qualifier")

    def test_spend_status_and_refuse_include_qualifier(self):
        """Claim: operator-facing spend refuse/status carry the unit qualifier."""
        spend = _load("spend_q", REPO_ROOT / "mcp" / "adversarial_mcp" / "spend.py")
        self.assertIn("model provider", spend.SPEND_UNIT_QUALIFIER)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "config").mkdir()
            (root / "config" / "setup.md").write_text(
                "## Budget model\n- billed\n\n### Billed\n"
                "- total spend cap: 1\n"
                "- escalation threshold (% of cap): 50\n",
                encoding="utf-8",
            )
            spend.record_usage(1.0, source="t", repo_root=root)
            status = spend.spend_status(root)
            self.assertEqual(status["qualifier"], spend.SPEND_UNIT_QUALIFIER)
            with self.assertRaises(spend.SpendCapExceeded) as ctx:
                spend.refuse_if_over_cap(root)
            self.assertIn(spend.SPEND_UNIT_QUALIFIER, str(ctx.exception))

    def test_messaging_blocks_without_network_allow_even_if_approved(self):
        """Claim: messaging egress requires network_permission=allow."""
        messaging = _load("messaging_net", REPO_ROOT / "scripts" / "messaging.py")
        prev_net = os.environ.get("NETWORK_PERMISSION")
        prev_ap = os.environ.get("AG_APPROVAL")
        try:
            os.environ["NETWORK_PERMISSION"] = "unknown"
            os.environ["AG_APPROVAL"] = "1"
            self.assertFalse(messaging.send_alert("test-msg"))
            os.environ["NETWORK_PERMISSION"] = "deny"
            self.assertFalse(messaging.send_alert("test-msg"))
        finally:
            if prev_net is None:
                os.environ.pop("NETWORK_PERMISSION", None)
            else:
                os.environ["NETWORK_PERMISSION"] = prev_net
            if prev_ap is None:
                os.environ.pop("AG_APPROVAL", None)
            else:
                os.environ["AG_APPROVAL"] = prev_ap

    def test_messaging_blocks_without_approval_when_network_allow(self):
        """Claim: messaging still requires approval after network allow."""
        messaging = _load("messaging_ap", REPO_ROOT / "scripts" / "messaging.py")
        prev_net = os.environ.get("NETWORK_PERMISSION")
        prev_ap = os.environ.pop("AG_APPROVAL", None)
        os.environ.pop("AG_APPROVAL_TOKEN", None)
        try:
            os.environ["NETWORK_PERMISSION"] = "allow"
            # No approval → False (and no webhook configured anyway)
            self.assertFalse(messaging.send_alert("test-msg"))
        finally:
            if prev_net is None:
                os.environ.pop("NETWORK_PERMISSION", None)
            else:
                os.environ["NETWORK_PERMISSION"] = prev_net
            if prev_ap is None:
                os.environ.pop("AG_APPROVAL", None)
            else:
                os.environ["AG_APPROVAL"] = prev_ap

    def test_admin_allowlist_empty_is_fail_closed_and_no_personal_default(self):
        """Claim: ADMIN_EMAILS empty → nobody; no hardcoded personal email."""
        src = (REPO_ROOT / "dashboard" / "src" / "lib" / "admin-access.ts").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("noreply address", src)
        self.assertIn("fail closed", src.lower())
        self.assertIn("ADMIN_EMAILS", src)
        # No hardcoded string-literal email arrays
        self.assertNotRegex(src, r'HARDCODED_ADMIN_EMAILS\s*=\s*\[["\'][^"\']+@')

        env_ex = (REPO_ROOT / "dashboard" / ".env.example").read_text(encoding="utf-8")
        self.assertNotIn("noreply address", env_ex)
        # Placeholder only
        self.assertRegex(env_ex, r"(?m)^ADMIN_EMAILS=you@example\.com\s*$")

    def test_no_personal_email_in_functional_config_defaults(self):
        """Claim: functional configs/defaults/allowlists lack personal addresses."""
        banned = re.compile(r"paul\.thorson@gmail\.com", re.I)
        functional_globs = [
            "dashboard/src/**/*",
            "dashboard/.env.example",
            "mcp/**/*.py",
            "scripts/**/*.py",
            "tests/**/*.py",
            ".github/**/*",
        ]
        # Walk explicit functional roots
        roots = [
            REPO_ROOT / "dashboard" / "src",
            REPO_ROOT / "dashboard" / ".env.example",
            REPO_ROOT / "mcp",
            REPO_ROOT / "scripts",
            REPO_ROOT / "tests",
            REPO_ROOT / ".github",
        ]
        hits = []
        for root in roots:
            if root.is_file():
                text = root.read_text(encoding="utf-8")
                if banned.search(text):
                    hits.append(str(root))
                continue
            if not root.is_dir():
                continue
            for p in root.rglob("*"):
                if not p.is_file():
                    continue
                if p.suffix not in {
                    ".ts", ".tsx", ".js", ".mjs", ".py", ".yml", ".yaml",
                    ".json", ".example", ".md", ".toml",
                }:
                    continue
                try:
                    text = p.read_text(encoding="utf-8")
                except (OSError, UnicodeDecodeError):
                    continue
                if banned.search(text):
                    hits.append(str(p))
        # Exclude this contract file (it mentions the banned string under test).
        hits = [h for h in hits if Path(h).resolve() != Path(__file__).resolve()]
        self.assertEqual(hits, [], "personal email in functional paths: " + ", ".join(hits))

    def test_gitignore_excludes_env_and_pem(self):
        """Claim: .gitignore excludes .env and *.pem (secret hygiene)."""
        text = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
        lines = {ln.strip() for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("#")}
        self.assertIn(".env", lines)
        self.assertIn("*.pem", lines)

    def test_license_is_apache_without_prepended_copyright(self):
        """Claim: LICENSE is upstream Apache-2.0 text (no copyright line prepended)."""
        text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertTrue(text.lstrip().startswith("Apache License"))
        self.assertNotRegex(text[:80], r"(?i)^Copyright")

    def test_stdio_is_default_transport(self):
        """Claim: MCP transport defaults to stdio."""
        src = (REPO_ROOT / "mcp" / "adversarial_mcp" / "server.py").read_text(
            encoding="utf-8"
        )
        self.assertIn('default="stdio"', src)

    def test_dashboard_not_required_by_mcp_package(self):
        """Claim: dashboard is optional — MCP package does not depend on it."""
        pyproject = (REPO_ROOT / "mcp" / "pyproject.toml").read_text(encoding="utf-8")
        self.assertNotIn("dashboard", pyproject.lower())
        server = (REPO_ROOT / "mcp" / "adversarial_mcp" / "server.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("dashboard/", server)


if __name__ == "__main__":
    unittest.main()

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

        # .env.example must not ship remote-login / session secret key lines
        env_ex = REPO_ROOT / "dashboard" / ".env.example"
        if env_ex.exists():
            text = env_ex.read_text(encoding="utf-8")
            for line in text.splitlines():
                stripped = line.strip()
                if stripped.startswith("#") or not stripped:
                    continue
                self.assertFalse(
                    stripped.startswith("AUTH_") or stripped.startswith("ADMIN_EMAILS="),
                    f"remote-login secret key line must not ship in .env.example: {stripped}",
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

    def test_admin_localhost_gate_fail_closed_no_remote_login(self):
        """Claim: /admin is localhost Host only; remote identity login removed."""
        access = (REPO_ROOT / "dashboard" / "src" / "lib" / "admin-access.ts").read_text(
            encoding="utf-8"
        )
        self.assertIn("fail closed", access.lower())
        self.assertIn("isLocalAdminHost", access)
        self.assertIn("localhost", access)
        self.assertNotIn('"0.0.0.0"', access)
        self.assertNotIn("'0.0.0.0'", access)
        self.assertNotIn("isAdminEmail", access)
        self.assertNotIn("process.env.ADMIN_EMAILS", access)

        middleware = (REPO_ROOT / "dashboard" / "src" / "middleware.ts").read_text(
            encoding="utf-8"
        )
        self.assertIn("isLocalAdminHost", middleware)
        self.assertIn('set("admin", "local-only")', middleware)
        self.assertNotIn('from "@/auth"', middleware)
        self.assertNotIn("from '@/auth'", middleware)
        self.assertNotIn("next-auth", middleware.lower())

        # No Auth.js entrypoint / remote sign-in provider module on tip.
        auth_ts = REPO_ROOT / "dashboard" / "src" / "auth.ts"
        self.assertFalse(auth_ts.exists(), "dashboard/src/auth.ts must not exist")

        nextauth_route = (
            REPO_ROOT
            / "dashboard"
            / "src"
            / "app"
            / "api"
            / "auth"
            / "[...nextauth]"
            / "route.ts"
        )
        self.assertFalse(
            nextauth_route.exists(), "Auth.js catch-all API route must not exist"
        )

        pkg = (REPO_ROOT / "dashboard" / "package.json").read_text(encoding="utf-8")
        self.assertNotIn("next-auth", pkg)

        # No next-auth provider imports / remote sign-in actions under dashboard/src.
        dash_src = REPO_ROOT / "dashboard" / "src"
        for path in list(dash_src.rglob("*.ts")) + list(dash_src.rglob("*.tsx")):
            body = path.read_text(encoding="utf-8")
            self.assertNotIn(
                "next-auth/providers",
                body,
                f"remote sign-in provider import must not exist: {path}",
            )
            self.assertNotIn("signInWith", body, f"unexpected remote sign-in action in {path}")

        env_ex = (REPO_ROOT / "dashboard" / ".env.example").read_text(encoding="utf-8")
        self.assertNotIn("@gmail.com", env_ex)
        for line in env_ex.splitlines():
            stripped = line.strip()
            if stripped.startswith("#") or not stripped:
                continue
            self.assertFalse(
                stripped.startswith("AUTH_") or stripped.startswith("ADMIN_EMAILS="),
                f"remote-login secret key line must not ship: {stripped}",
            )

        login = (
            REPO_ROOT / "dashboard" / "src" / "app" / "admin" / "login" / "page.tsx"
        ).read_text(encoding="utf-8")
        self.assertIn("redirect", login)
        self.assertNotIn("allowlisted", login.lower())
        self.assertNotIn("Sign in with", login)

    def test_no_personal_email_in_functional_config_defaults(self):
        """Claim: functional configs/defaults/allowlists lack personal email defaults.

        Uses a generic local-part pattern (no full personal address stored in tip).
        """
        # Generic: first-name.local-part @ gmail — does not embed a specific address.
        banned = re.compile(r"paul\.[a-z0-9._+-]+@gmail\.com", re.I)
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

    def test_dashboard_sends_restrictive_security_headers(self):
        """Claim: dashboard responses include CSP self-only and clickjacking headers."""
        src = (REPO_ROOT / "dashboard" / "next.config.ts").read_text(encoding="utf-8")
        self.assertIn("async headers()", src)
        self.assertIn("default-src 'self'", src)
        self.assertIn("frame-ancestors 'none'", src)
        self.assertIn("object-src 'none'", src)
        self.assertIn('value: "DENY"', src)
        self.assertIn("X-Frame-Options", src)
        self.assertIn("X-Content-Type-Options", src)
        self.assertIn("nosniff", src)
        self.assertIn("strict-origin-when-cross-origin", src)
        self.assertIn("Permissions-Policy", src)
        self.assertIn("camera=()", src)
        self.assertIn("geolocation=()", src)

    def test_admin_host_ignores_forwarded_host_by_default(self):
        """Claim: admin gate uses Host; X-Forwarded-Host is opt-in."""
        access = (REPO_ROOT / "dashboard" / "src" / "lib" / "admin-access.ts").read_text(
            encoding="utf-8"
        )
        self.assertIn("AG_TRUST_X_FORWARDED_HOST", access)
        self.assertIn("resolveRequestHost", access)
        self.assertIn("fail closed", access.lower())
        middleware = (REPO_ROOT / "dashboard" / "src" / "middleware.ts").read_text(
            encoding="utf-8"
        )
        self.assertIn("resolveRequestHost", middleware)
        self.assertNotIn('headers.get("x-forwarded-host")?.split(",")[0]?.trim() ||', middleware)
        host_test = (REPO_ROOT / "tests" / "test_admin_host.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("skipUnless", host_test)
        self.assertNotIn("skipIf", host_test)
        probe = (REPO_ROOT / "tests" / "admin_access_probe.mts").read_text(
            encoding="utf-8"
        )
        self.assertIn("host-0.0.0.0-denied", probe)
        self.assertIn("host-0.0.0.0-port-denied", probe)

    def test_http_transport_refuses_non_loopback_without_token(self):
        """Claim: MCP HTTP off loopback requires MCP_AUTH_TOKEN."""
        src = (REPO_ROOT / "mcp" / "adversarial_mcp" / "server.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("refuse_http_without_token", src)
        self.assertIn("hmac.compare_digest", src)
        deploy = (REPO_ROOT / "docs" / "deployment.md").read_text(encoding="utf-8")
        self.assertIn("Off loopback", deploy)
        self.assertIn("missing token is refused", deploy)

    # ---- Constitution claims --------------------------------------------------

    def _constitution_files(self):
        root = REPO_ROOT / "constitution"
        return [root / "constitution.md", *sorted((root / "domains").glob("*.md"))]

    def test_constitution_does_not_claim_mechanical_enforcement_of_all_rules(self):
        """Capability report 12.8: blind review, human-only veto clear and
        append-only are 'Instruction + process'. Only the Rule 1 veto scan and
        the veto-clear approval are code. No constitution page may say every
        rule is enforced mechanically."""
        for f in self._constitution_files():
            text = " ".join(f.read_text(encoding="utf-8").split())  # collapse line wrapping
            self.assertNotIn("enforced mechanically", text, f"{f.relative_to(REPO_ROOT)} overclaims enforcement")
            self.assertIn("Rule 1 is enforced by code", text, f"{f.relative_to(REPO_ROOT)} must say what code enforces")
            self.assertIn("Rules 2 through 4 are instructions", text, f"{f.relative_to(REPO_ROOT)} must say rules 2-4 are instructions")

    def test_constitution_rule_1_code_gate_exists(self):
        """The one enforcement claim the constitution does make must be true:
        a veto hit flips the MCP verdict to KICK_BACK and clear-veto is gated."""
        server = (REPO_ROOT / "mcp" / "adversarial_mcp" / "server.py").read_text(encoding="utf-8")
        self.assertIn('"KICK_BACK" if structural["veto_triggered"]', server)
        ticket = (REPO_ROOT / "scripts" / "ticket.py").read_text(encoding="utf-8")
        self.assertIn('gate=_gate("clear_veto"', ticket)

    def test_constitution_states_the_veto_scan_limit(self):
        """The veto scan is a word match. The root page and the capability
        report must both say a harm described without a listed term passes
        the scan, so nobody reads the Rule 1 code gate as a harm detector."""
        root_text = " ".join((REPO_ROOT / "constitution" / "constitution.md").read_text(encoding="utf-8").split())
        self.assertIn("The scan matches words, not meaning.", root_text)
        self.assertIn("passes the scan with `REVIEW_REQUIRED`", root_text)
        report = (REPO_ROOT / "docs" / "capability-report.md").read_text(encoding="utf-8")
        self.assertIn("| Veto scan (Rule 1 first pass) | **Code**, fixed term and pattern match only", report)

    def test_root_constitution_rule_pattern_matches_domain_files(self):
        """The root page describes a shared shape for ten domains and two
        exceptions. The domain files must actually have that shape."""
        domains = sorted((REPO_ROOT / "constitution" / "domains").glob("*.md"))
        self.assertEqual(len(domains), 12)
        for f in domains:
            text = f.read_text(encoding="utf-8")
            heads = re.findall(r"^## Rule (\d): (.+)$", text, re.M)
            self.assertEqual([h[0] for h in heads], ["1", "2", "3", "4"], f"{f.name} must have Rules 1-4 in order")
            self.assertIn("vetoes are absolute", heads[0][1], f"{f.name} Rule 1 must be the veto")
            if f.stem in ("security", "prompt"):
                continue
            self.assertIn("Genuine", heads[1][1], f"{f.name} Rule 2 must be genuine alternatives")
            self.assertIn("can't silently win", heads[2][1], f"{f.name} Rule 3 must be the fast-path rule")
            self.assertTrue("falsify" in heads[3][1] or "must tie to" in heads[3][1], f"{f.name} Rule 4: {heads[3][1]}")

    def test_constitution_amendment_procedure_is_one_procedure(self):
        """Root and domain pages state the same procedure, and the ledger each
        domain points at exists."""
        root_text = (REPO_ROOT / "constitution" / "constitution.md").read_text(encoding="utf-8")
        on_trial = r"(Three overrides of one rule puts the rule on trial|overridden three times, the rule goes on trial)"
        self.assertRegex(root_text, on_trial)
        self.assertNotIn("designated human master", root_text)
        for f in sorted((REPO_ROOT / "constitution" / "domains").glob("*.md")):
            text = f.read_text(encoding="utf-8")
            self.assertRegex(text, on_trial, f.name)
            m = re.search(r"logged in `([^`]+calibration-ledger\.md)`", text)
            self.assertIsNotNone(m, f"{f.name} must name its ledger")
            self.assertTrue((f.parent / m.group(1)).exists(), f"{f.name}: {m.group(1)} does not resolve")
            self.assertRegex(text, r"(Only a human edits `constitution/domains/" + f.stem + r"\.md`|only by a human editing this file)", f.name)


if __name__ == "__main__":
    unittest.main()

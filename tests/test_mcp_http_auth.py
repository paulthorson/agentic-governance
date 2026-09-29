"""HTTP transport auth: token required off loopback; constant-time bearer compare."""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "mcp"))
os.environ.setdefault("ADVERSARIAL_ROOT", str(REPO_ROOT))

from adversarial_mcp import server as mcp_server  # noqa: E402


class TestLoopbackBind(unittest.TestCase):
    def test_loopback_hosts(self):
        for host in ("127.0.0.1", "::1", "localhost", "[::1]", "LOCALHOST", " 127.0.0.1 "):
            self.assertTrue(mcp_server.is_loopback_bind(host), host)

    def test_non_loopback_hosts(self):
        for host in ("0.0.0.0", "::", "[::]", "192.168.1.5", "example.com", "", None):
            self.assertFalse(mcp_server.is_loopback_bind(host or ""), host)


class TestRefuseHttpWithoutToken(unittest.TestCase):
    def test_refuse_wildcard_without_token(self):
        for host in ("0.0.0.0", "::", "[::]", "192.168.0.10"):
            self.assertTrue(mcp_server.refuse_http_without_token(host, ""))

    def test_allow_loopback_without_token(self):
        for host in ("127.0.0.1", "::1", "localhost", "[::1]"):
            self.assertFalse(mcp_server.refuse_http_without_token(host, ""))

    def test_allow_any_host_with_token(self):
        for host in ("0.0.0.0", "::", "127.0.0.1", "10.0.0.2"):
            self.assertFalse(mcp_server.refuse_http_without_token(host, "secret"))


class TestBearerCompare(unittest.TestCase):
    def test_match(self):
        self.assertTrue(mcp_server.bearer_token_matches("Bearer secret", "secret"))

    def test_mismatch_and_missing(self):
        self.assertFalse(mcp_server.bearer_token_matches("Bearer other", "secret"))
        self.assertFalse(mcp_server.bearer_token_matches("", "secret"))
        self.assertFalse(mcp_server.bearer_token_matches("secret", "secret"))
        self.assertFalse(mcp_server.bearer_token_matches("Bearer secret", "secre"))

    def test_uses_compare_digest(self):
        src = (REPO_ROOT / "mcp" / "adversarial_mcp" / "server.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("hmac.compare_digest", src)


class TestHttpAuthTokenEnv(unittest.TestCase):
    def test_strips_whitespace_and_empty(self):
        with mock.patch.dict(os.environ, {"MCP_AUTH_TOKEN": "  "}, clear=False):
            self.assertEqual(mcp_server.http_auth_token(), "")
        with mock.patch.dict(os.environ, {"MCP_AUTH_TOKEN": "  tok  "}, clear=False):
            self.assertEqual(mcp_server.http_auth_token(), "tok")


if __name__ == "__main__":
    unittest.main()

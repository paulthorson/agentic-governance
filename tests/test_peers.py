"""S1.1.1: doctor reports which OS user each live MCP connection runs as.

Parsers are tested against captured-format fixtures for macOS lsof and Linux
/proc/net/tcp. On Linux a live test opens a real listener and a real client
and checks the report end to end. The macOS root path (agctl doctor) is
tested on a hardened install in scripts/macos/e2e-test.sh.
"""
import os
import pwd
import socket
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import peers  # noqa: E402


def _doctor(*extra):
    """Run ticket.py doctor against a fresh, empty install in a temp directory."""
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "runs").mkdir()
        env = {k: v for k, v in os.environ.items()
               if k not in ("AG_APPROVAL", "AG_APPROVAL_TOKEN", "AG_INTEGRITY_KEY", "SUDO_USER")}
        env.update(ADVERSARIAL_ROOT=str(root), TICKET_FILE=str(root / "runs" / "t.json"),
                   EVENT_LOG=str(root / "runs" / "e.jsonl"), VERDICT_LOG=str(root / "runs" / "v.jsonl"),
                   AG_AGENT_REGISTRY=str(root / "agents.json"),
                   AG_INTEGRITY_KEY_FILE=str(root / "integrity.key"))
        return subprocess.run([sys.executable, str(REPO_ROOT / "scripts" / "ticket.py"), "doctor", *extra],
                              env=env, capture_output=True, text=True, timeout=30)

LSOF_FIXTURE = """\
p812
cpython3.12
u450
f5
n127.0.0.1:8765
f9
n127.0.0.1:8765->127.0.0.1:50211
f10
n127.0.0.1:8765->127.0.0.1:50300
p901
cnode
u502
f22
n127.0.0.1:50211->127.0.0.1:8765
p955
cclaude-runtime
u501
f31
n127.0.0.1:50300->127.0.0.1:8765
p960
cSafari
u501
f40
n192.168.1.20:50400->17.253.144.10:443
"""

# /proc/net/tcp: a listener on 127.0.0.1:8765 (0x223D) owned by uid 998, the
# server's accepted socket, and a client from uid 1001. Plus an unrelated
# connection to port 443 from uid 1001.
PROC_FIXTURE = """\
  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode
   0: 0100007F:223D 00000000:0000 0A 00000000:00000000 00:00000000 00000000   998        0 1 1 0000000000000000 100 0 0 10 0
   1: 0100007F:223D 0100007F:C3A3 01 00000000:00000000 00:00000000 00000000   998        0 2 1 0000000000000000 20 4 30 10 -1
   2: 0100007F:C3A3 0100007F:223D 01 00000000:00000000 00:00000000 00000000  1001        0 3 1 0000000000000000 20 4 30 10 -1
   3: 1401A8C0:C4D0 0A90FD11:01BB 01 00000000:00000000 00:00000000 00000000  1001        0 4 1 0000000000000000 20 4 30 10 -1
"""


class ParseTest(unittest.TestCase):
    def test_lsof_listener_and_clients(self):
        socks = peers.parse_lsof(LSOF_FIXTURE)
        self.assertEqual(peers.server_ports(socks, 450), {8765})
        clients = peers.client_sockets(socks, {8765}, 450)
        self.assertEqual(sorted((c.pid, c.uid, c.command) for c in clients),
                         [(901, 502, "node"), (955, 501, "claude-runtime")])

    def test_lsof_ipv6(self):
        socks = peers.parse_lsof("p1\ncsrv\nu450\nn[::1]:8765\np2\ncagent\nu502\nn[::1]:50000->[::1]:8765\n")
        self.assertEqual(peers.server_ports(socks, 450), {8765})
        self.assertEqual([c.uid for c in peers.client_sockets(socks, {8765}, 450)], [502])

    def test_proc_net_tcp(self):
        socks = peers.parse_proc_net_tcp(PROC_FIXTURE)
        self.assertEqual(peers.server_ports(socks, 998), {8765})
        clients = peers.client_sockets(socks, {8765}, 998)
        self.assertEqual([(c.uid, c.local, c.remote) for c in clients],
                         [(1001, ("127.0.0.1", 50083), ("127.0.0.1", 8765))])

    def test_non_loopback_remote_ignored(self):
        socks = peers.parse_lsof("p2\ncx\nu502\nn10.0.0.5:50000->10.0.0.9:8765\n")
        self.assertEqual(peers.client_sockets(socks, {8765}, 450), [])


class ClassifyTest(unittest.TestCase):
    def _s(self, uid, cmd="agent", pid=1):
        return peers.Socket(pid, cmd, uid, ("127.0.0.1", 50000 + pid), ("127.0.0.1", 8765))

    def _run(self, clients, admins=(), operator="opuser", service="_aggov", names=None):
        names = names or {}
        orig = peers._user_name
        peers._user_name = lambda uid: names.get(uid, f"u{uid}")
        try:
            return peers.classify(clients, service_user=service, operator=operator,
                                  is_admin=lambda u: u in admins)
        finally:
            peers._user_name = orig

    def test_no_connections_is_info(self):
        self.assertEqual(self._run([])[0][0], "INFO")

    def test_non_admin_agent_passes_and_is_listed(self):
        res = self._run([self._s(502, "node", 1), self._s(502, "node", 2)], names={502: "agent-eng"})
        self.assertEqual(res, [("PASS", "agent user agent-eng (node; 2 processes)")])

    def test_root_fails(self):
        self.assertEqual(self._run([self._s(0)], names={0: "root"})[0][0], "FAIL")

    def test_operator_login_fails(self):
        res = self._run([self._s(501)], names={501: "opuser"})
        self.assertEqual(res[0][0], "FAIL")
        self.assertIn("operator's login user", res[0][1])

    def test_admin_fails(self):
        res = self._run([self._s(503)], admins={"someadmin"}, names={503: "someadmin"})
        self.assertEqual(res[0][0], "FAIL")
        self.assertIn("an admin", res[0][1])

    def test_service_user_as_client_fails(self):
        res = self._run([self._s(450)], names={450: "_aggov"})
        self.assertEqual(res[0][0], "FAIL")
        self.assertIn("service user", res[0][1])

    def test_one_line_per_user_mixed(self):
        res = self._run([self._s(502, pid=1), self._s(501, pid=2)], names={502: "agent", 501: "opuser"})
        self.assertEqual([lvl for lvl, _ in res], ["FAIL", "PASS"])


# The live client runs as whoever runs the tests. As root that is the root
# check; as anyone else it is the "client runs as the service user" check.
EXPECTED_SELF_FAIL = "root" if os.getuid() == 0 else "the service user"


@unittest.skipUnless(sys.platform.startswith("linux"), "Linux /proc path")
class LinuxLiveTest(unittest.TestCase):
    """A real listener and a real client, both as the user running the tests.

    The client runs as the 'service user' (the same uid as the listener), which
    must be a FAIL. That proves the report sees the live connection and names
    its owner.
    """

    def setUp(self):
        self.srv = socket.socket()
        self.srv.bind(("127.0.0.1", 0))
        self.srv.listen(1)
        self.port = self.srv.getsockname()[1]
        self.cli = socket.create_connection(("127.0.0.1", self.port))
        self.acc, _ = self.srv.accept()

    def tearDown(self):
        for s in (self.cli, self.acc, self.srv):
            s.close()

    def test_findings_see_the_live_client(self):
        me = pwd.getpwuid(os.getuid()).pw_name
        res = peers.findings(me, None, self.port)
        self.assertIn(("INFO", f"MCP server port checked: {self.port}"), res)
        fails = [m for lvl, m in res if lvl == "FAIL"]
        self.assertTrue(any(EXPECTED_SELF_FAIL in m for m in fails), res)

    def test_port_autodetect_finds_the_listener(self):
        socks = peers.collect_linux()
        self.assertIn(self.port, peers.server_ports(socks, os.getuid()))

    def test_ticket_doctor_reports_and_fails(self):
        r = _doctor("--mcp-port", str(self.port))
        self.assertIn(f"MCP server port checked: {self.port}", r.stdout)
        self.assertIn(f"[FAIL] an MCP client runs as {EXPECTED_SELF_FAIL}", r.stdout)
        self.assertEqual(r.returncode, 4, r.stdout + r.stderr)


class DoctorWithoutPortTest(unittest.TestCase):
    def test_doctor_without_port_only_informs(self):
        if sys.platform == "darwin":
            self.skipTest("macOS prints the agctl pointer instead")
        r = _doctor()
        self.assertIn("pass --mcp-port", r.stdout)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()

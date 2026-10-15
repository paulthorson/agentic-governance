#!/usr/bin/env python3
"""Report which OS user is on the other end of each live MCP connection.

The hardened install keeps agents away from governance files by running them
as users other than the service user. That only holds if no agent runs as an
admin, as root, as the operator's own login, or as the service user itself.
A token in a process's memory cannot be seen from outside; a TCP connection
to the MCP server can. This script lists those connections and the user that
owns each client socket.

  macOS:  lsof, run as root (only root can see other users' sockets). agctl
          runs this before `doctor`.
  Linux:  /proc/net/tcp, readable without root.

A connection is only visible while it is open. An agent that is not running,
or that connects only when it has work, does not show up. Run doctor while
the agents are up.

Standard library only. Exit 4 if any connection is owned by a user an agent
must not run as; 0 otherwise.

Usage:
  python3 scripts/peers.py --service-user _aggov [--operator NAME] [--port N]
"""

from __future__ import annotations

import argparse
import grp
import ipaddress
import os
import pwd
import subprocess
import sys
from dataclasses import dataclass, field

LSOF = "/usr/sbin/lsof"
DSEDITGROUP = "/usr/sbin/dseditgroup"
ADMIN_GROUPS_LINUX = ("sudo", "wheel", "admin", "root")


@dataclass
class Socket:
    pid: int | None
    command: str
    uid: int
    local: tuple[str, int]
    remote: tuple[str, int] | None
    listening: bool = False


@dataclass
class Peer:
    user: str
    uid: int
    commands: set[str] = field(default_factory=set)
    pids: set[int] = field(default_factory=set)


# ---- parsing -----------------------------------------------------------------

def _split_hostport(s: str) -> tuple[str, int]:
    """'127.0.0.1:8765' or '[::1]:8765' -> (host, port)."""
    if s.startswith("["):
        host, _, port = s[1:].partition("]:")
    else:
        host, _, port = s.rpartition(":")
    return host, int(port)


def parse_lsof(text: str) -> list[Socket]:
    """Parse `lsof -nP -F pcun` output (one field per line, prefixed by its key).

    A `p` line starts a process; `c` and `u` belong to it. Each `n` line is a
    socket of that process: 'local->remote' for a connection, 'local' for a
    listener.
    """
    out: list[Socket] = []
    pid: int | None = None
    command = ""
    uid = -1
    for line in text.splitlines():
        if not line:
            continue
        key, val = line[0], line[1:]
        if key == "p":
            pid, command, uid = int(val), "", -1
        elif key == "c":
            command = val
        elif key == "u":
            uid = int(val)
        elif key == "n":
            if "->" in val:
                loc, rem = val.split("->", 1)
                out.append(Socket(pid, command, uid, _split_hostport(loc), _split_hostport(rem)))
            else:
                try:
                    out.append(Socket(pid, command, uid, _split_hostport(val), None, listening=True))
                except ValueError:
                    continue
    return out


def _proc_addr(hexaddr: str) -> tuple[str, int]:
    """'0100007F:2238' -> ('127.0.0.1', 8760). IPv4 in /proc is little-endian."""
    h, p = hexaddr.split(":")
    port = int(p, 16)
    if len(h) == 8:
        ip = ipaddress.IPv4Address(bytes.fromhex(h)[::-1])
    else:  # IPv6: four little-endian 32-bit words
        b = bytes.fromhex(h)
        ip = ipaddress.IPv6Address(b"".join(b[i:i + 4][::-1] for i in range(0, 16, 4)))
        if ip.ipv4_mapped:
            ip = ip.ipv4_mapped
    return str(ip), port


def parse_proc_net_tcp(text: str) -> list[Socket]:
    """Parse /proc/net/tcp or /proc/net/tcp6. State 0A is LISTEN, 01 ESTABLISHED."""
    out: list[Socket] = []
    for line in text.splitlines()[1:]:
        cols = line.split()
        if len(cols) < 8:
            continue
        state = cols[3]
        if state not in ("01", "0A"):
            continue
        local = _proc_addr(cols[1])
        uid = int(cols[7])
        if state == "0A":
            out.append(Socket(None, "", uid, local, None, listening=True))
        else:
            out.append(Socket(None, "", uid, local, _proc_addr(cols[2])))
    return out


# ---- finding the server and its clients ---------------------------------------

def _loopback(host: str) -> bool:
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return host == "localhost"


def server_ports(sockets: list[Socket], service_uid: int) -> set[int]:
    """Ports the service user is listening on."""
    return {s.local[1] for s in sockets if s.listening and s.uid == service_uid}


def client_sockets(sockets: list[Socket], ports: set[int], service_uid: int) -> list[Socket]:
    """Established loopback connections whose remote end is one of the server's ports.

    The server's own accepted sockets have the port on the local side, so they
    drop out. A client running as the service user stays in: that is a finding.
    """
    return [s for s in sockets
            if not s.listening and s.remote is not None
            and s.remote[1] in ports and _loopback(s.remote[0])
            and not (s.uid == service_uid and s.local[1] in ports)]


# ---- who is allowed ----------------------------------------------------------

def _user_name(uid: int) -> str:
    try:
        return pwd.getpwuid(uid).pw_name
    except KeyError:
        return f"uid {uid}"


def is_admin_macos(user: str) -> bool:
    r = subprocess.run([DSEDITGROUP, "-o", "checkmember", "-m", user, "admin"],
                       capture_output=True, text=True)
    return r.returncode == 0


def is_admin_linux(user: str) -> bool:
    try:
        pw = pwd.getpwnam(user)
    except KeyError:
        return False
    if pw.pw_uid == 0:
        return True
    names = set()
    for g in grp.getgrall():
        if user in g.gr_mem or g.gr_gid == pw.pw_gid:
            names.add(g.gr_name)
    return bool(names & set(ADMIN_GROUPS_LINUX))


def classify(clients: list[Socket], *, service_user: str, operator: str | None,
             is_admin) -> list[tuple[str, str]]:
    """Group connections by user and decide, per user, PASS or FAIL."""
    peers: dict[int, Peer] = {}
    for s in clients:
        p = peers.setdefault(s.uid, Peer(_user_name(s.uid), s.uid))
        if s.command:
            p.commands.add(s.command)
        if s.pid is not None:
            p.pids.add(s.pid)

    if not peers:
        return [("INFO", "no live MCP connections; start the agents and run doctor again "
                         "to see which OS users they run as")]

    findings: list[tuple[str, str]] = []
    for uid in sorted(peers):
        p = peers[uid]
        if p.pids:
            n = len(p.pids)
            tail = f"({', '.join(sorted(p.commands)) or 'unnamed'}; {n} process{'es' if n != 1 else ''})"
        else:  # /proc/net/tcp gives the socket's uid, not its process
            tail = "(process not visible without root)"
        if uid == 0:
            findings.append(("FAIL", f"an MCP client runs as root {tail}"))
        elif p.user == service_user:
            findings.append(("FAIL", f"an MCP client runs as the service user {p.user}, which owns runs/ and config/ {tail}"))
        elif operator and p.user == operator:
            findings.append(("FAIL", f"an MCP client runs as the operator's login user {p.user} {tail}"))
        elif is_admin(p.user):
            findings.append(("FAIL", f"an MCP client runs as {p.user}, an admin {tail}"))
        else:
            findings.append(("PASS", f"agent user {p.user} {tail}"))
    return findings


# ---- collection per platform ---------------------------------------------------

def collect_macos() -> list[Socket]:
    if os.geteuid() != 0:
        raise PermissionError("on macOS only root can see other users' connections; run via sudo agctl doctor")
    r = subprocess.run([LSOF, "-nP", "-iTCP", "-sTCP:LISTEN,ESTABLISHED", "-F", "pcun"],
                       capture_output=True, text=True)
    # lsof exits 1 when it finds nothing; any other failure leaves stdout empty.
    return parse_lsof(r.stdout)


def collect_linux() -> list[Socket]:
    socks: list[Socket] = []
    for path in ("/proc/net/tcp", "/proc/net/tcp6"):
        try:
            with open(path, encoding="ascii") as fh:
                socks += parse_proc_net_tcp(fh.read())
        except FileNotFoundError:
            continue
    return socks


def findings(service_user: str, operator: str | None = None, port: int | None = None) -> list[tuple[str, str]]:
    try:
        service_uid = pwd.getpwnam(service_user).pw_uid
    except KeyError:
        return [("FAIL", f"service user {service_user} does not exist")]
    if sys.platform == "darwin":
        try:
            socks = collect_macos()
        except PermissionError as e:
            return [("INFO", str(e))]
        is_admin = is_admin_macos
    elif sys.platform.startswith("linux"):
        socks = collect_linux()
        is_admin = is_admin_linux
    else:
        return [("INFO", f"connection peers are not checked on {sys.platform}")]

    ports = {port} if port else server_ports(socks, service_uid)
    if not ports:
        return [("WARN", f"no MCP server listening as {service_user}; cannot check which users agents run as")]
    out = [("INFO", f"MCP server port{'s' if len(ports) > 1 else ''} checked: {', '.join(map(str, sorted(ports)))}")]
    out += classify(client_sockets(socks, ports, service_uid),
                    service_user=service_user, operator=operator, is_admin=is_admin)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--service-user", required=True, help="the user the MCP server runs as")
    ap.add_argument("--operator", default=None, help="the operator's login user (agctl passes SUDO_USER)")
    ap.add_argument("--port", type=int, default=None, help="server port (default: every port the service user listens on)")
    args = ap.parse_args()
    res = findings(args.service_user, args.operator or None, args.port)
    for level, msg in res:
        print(f"[{level:4}] {msg}")
    return 4 if any(level == "FAIL" for level, _ in res) else 0


if __name__ == "__main__":
    sys.exit(main())

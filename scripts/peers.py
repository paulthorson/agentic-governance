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

class CheckError(Exception):
    """The check could not see what it needs. Reported as FAIL, never as PASS."""


def _loopback(host: str) -> bool:
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return host == "localhost"


def server_ports(sockets: list[Socket], service_uid: int) -> set[int]:
    """Ports the service user is listening on."""
    return {s.local[1] for s in sockets if s.listening and s.uid == service_uid}


def client_sockets(sockets: list[Socket], ports: set[int], service_uid: int) -> list[Socket]:
    """Established connections from this host whose remote end is one of the server's ports.

    A connection counts when its remote address is loopback or any address this
    host owns (a server bound to 0.0.0.0 can be reached on a LAN address too).
    The server's own accepted sockets have the port on the local side, so they
    drop out. A client running as the service user stays in: that is a finding.
    """
    own = {s.local[0] for s in sockets} | {"127.0.0.1", "::1"}
    return [s for s in sockets
            if not s.listening and s.remote is not None
            and s.remote[1] in ports and (_loopback(s.remote[0]) or s.remote[0] in own)
            and not (s.uid == service_uid and s.local[1] in ports)]


# ---- who is allowed ----------------------------------------------------------

TIMEOUT = 15  # seconds for each external command; a stall is a FAIL, not a hang


def _user_name(uid: int) -> str:
    try:
        return pwd.getpwuid(uid).pw_name
    except KeyError:
        return f"uid {uid}"


def _in_group(user: str, group: str) -> bool:
    try:
        g = grp.getgrnam(group)
    except KeyError:
        return False
    try:
        primary = pwd.getpwnam(user).pw_gid
    except KeyError:
        primary = None
    return user in g.gr_mem or primary == g.gr_gid


def is_admin_macos(user: str) -> bool:
    """Member of the admin group, by dseditgroup and by the group database.

    Either source saying yes is enough. dseditgroup output that is neither a
    clear yes nor a clear no raises CheckError, so a directory-service failure
    can never turn an admin into a PASS.
    """
    if _in_group(user, "admin"):
        return True
    try:
        r = subprocess.run([DSEDITGROUP, "-o", "checkmember", "-m", user, "admin"],
                           capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        raise CheckError(f"dseditgroup timed out checking whether {user} is an admin")
    out = r.stdout.strip().lower()
    if out.startswith("yes"):
        return True
    if out.startswith("no") and "not a member" in out:
        return False
    raise CheckError(f"could not tell whether {user} is an admin "
                     f"(dseditgroup exit {r.returncode}: {(r.stdout or r.stderr).strip()[:120]})")


def is_admin_linux(user: str) -> bool:
    try:
        pw = pwd.getpwnam(user)
    except KeyError:
        raise CheckError(f"no account named {user}")
    if pw.pw_uid == 0:
        return True
    return any(_in_group(user, g) for g in ADMIN_GROUPS_LINUX)


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
        return [("INFO", "no live MCP connections, so no agent was checked; start the agents "
                         "and run doctor again while they are connected")]

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
            continue
        if p.user == service_user:
            findings.append(("FAIL", f"an MCP client runs as the service user {p.user}, which owns runs/ and config/ {tail}"))
            continue
        if operator and p.user == operator:
            findings.append(("FAIL", f"an MCP client runs as the operator's login user {p.user} {tail}"))
            continue
        try:
            admin = is_admin(p.user)
        except CheckError as e:
            findings.append(("FAIL", f"{e}; treating {p.user} as unchecked {tail}"))
            continue
        if admin:
            findings.append(("FAIL", f"an MCP client runs as {p.user}, an admin {tail}"))
        else:
            findings.append(("PASS", f"agent user {p.user} {tail}"))
    return findings


# ---- collection per platform ---------------------------------------------------

def collect_macos() -> list[Socket]:
    if os.geteuid() != 0:
        raise PermissionError("on macOS only root can see other users' connections; run via sudo agctl doctor")
    try:
        r = subprocess.run([LSOF, "-nP", "-iTCP", "-sTCP:LISTEN,ESTABLISHED", "-F", "pcun"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        raise CheckError("lsof timed out listing connections")
    except OSError as e:
        raise CheckError(f"could not run lsof: {e}")
    # lsof exits 0 with results, 1 with none. Anything else, or exit 1 with an
    # error message, means the list cannot be trusted.
    if r.returncode not in (0, 1) or (r.returncode == 1 and r.stderr.strip()):
        raise CheckError(f"lsof failed (exit {r.returncode}): {r.stderr.strip()[:160]}")
    return parse_lsof(r.stdout)


def collect_linux() -> list[Socket]:
    socks: list[Socket] = []
    read_any = False
    for path in ("/proc/net/tcp", "/proc/net/tcp6"):
        try:
            with open(path, encoding="ascii", errors="replace") as fh:
                socks += parse_proc_net_tcp(fh.read())
            read_any = True
        except FileNotFoundError:
            continue
    if not read_any:
        raise CheckError("could not read /proc/net/tcp")
    return socks


def findings(service_user: str, operator: str | None = None, port: int | None = None) -> list[tuple[str, str]]:
    try:
        service_uid = pwd.getpwnam(service_user).pw_uid
    except KeyError:
        return [("FAIL", f"service user {service_user} does not exist")]
    out: list[tuple[str, str]] = []
    if not operator:
        out.append(("INFO", "operator login unknown (not run through sudo); an agent running as "
                            "the operator's own account is caught only if that account is an admin"))
    try:
        if sys.platform == "darwin":
            try:
                socks = collect_macos()
            except PermissionError as e:
                return out + [("INFO", str(e))]
            is_admin = is_admin_macos
        elif sys.platform.startswith("linux"):
            socks = collect_linux()
            is_admin = is_admin_linux
        else:
            return out + [("INFO", f"connection peers are not checked on {sys.platform}")]
    except CheckError as e:
        return out + [("FAIL", f"{e}; cannot check which users agents run as")]

    listening = server_ports(socks, service_uid)
    if port:
        if port not in listening:
            return out + [("FAIL", f"nothing is listening on port {port} as {service_user}; "
                                   f"cannot check which users agents run as")]
        ports = {port}
    else:
        ports = listening
    if not ports:
        return out + [("FAIL", f"no MCP server is listening as {service_user}; "
                               f"cannot check which users agents run as")]
    out.append(("INFO", f"MCP server port{'s' if len(ports) > 1 else ''} checked: {', '.join(map(str, sorted(ports)))}"))
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

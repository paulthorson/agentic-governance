#!/bin/bash
# Hardened macOS install for Agentic Governance (ADR-0013).
#
# Runs the framework as its own hidden service user, so agents running as
# your login user can reach it only over MCP and cannot read or write its
# files, even with a shell. Installs:
#
#   <prefix>/                 code, root-owned, read-only for everyone else
#   <prefix>/runs, /config    owned by the service user, mode 700
#   /Library/LaunchDaemons/<label>.mcp.plist      MCP server over HTTP on 127.0.0.1
#   /Library/LaunchDaemons/<label>.recover.plist  stuck-ticket recovery every 10 min
#
# Usage:
#   sudo scripts/macos/harden.sh [--prefix /Library/AgenticGovernance] [--user _aggov]
#                                [--label app.agenticgovernance] [--port 8765]
#                                [--python /opt/homebrew/bin/python3.12]
#   sudo scripts/macos/harden.sh --uninstall [--purge] [same options]
#
# --uninstall stops and removes the launchd services and keeps your data.
# --purge additionally deletes the install directory (tickets, event log,
# integrity key, agent registry), the logs, and the service user. It cannot
# be undone.
#
# Requires: macOS, sudo, Python 3.11+ readable by other users (Homebrew's is).
# Network: pip downloads mcp and pydantic once during install.

set -euo pipefail

ACTION=install
PURGE=0
PREFIX=/Library/AgenticGovernance
SVC_USER=_aggov
LABEL=app.agenticgovernance
PORT=8765
PY=""
SRC="$(cd "$(dirname "$0")/../.." && pwd)"
cd /  # commands run as the service user must not inherit an unreadable working directory

usage() { sed -n '2,25p' "$0" | sed 's/^# \{0,1\}//'; }
die() { echo "ERROR: $*" >&2; exit 1; }
log() { echo "==> $*"; }

while [ $# -gt 0 ]; do
  case "$1" in
    --uninstall) ACTION=uninstall ;;
    --purge) PURGE=1 ;;
    --prefix) PREFIX="$2"; shift ;;
    --user) SVC_USER="$2"; shift ;;
    --label) LABEL="$2"; shift ;;
    --port) PORT="$2"; shift ;;
    --python) PY="$2"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) usage; die "unknown argument: $1" ;;
  esac
  shift
done

[ "$(uname)" = Darwin ] || die "this installer is for macOS"
[ "$(id -u)" -eq 0 ] || die "run with sudo"
case "$PREFIX" in /|/Users|/Users/*|/System*|/usr|/usr/*) die "refusing prefix $PREFIX" ;; esac

LOGDIR="/Library/Logs/$(basename "$PREFIX")"
MCP_PLIST="/Library/LaunchDaemons/$LABEL.mcp.plist"
REC_PLIST="/Library/LaunchDaemons/$LABEL.recover.plist"

uninstall() {
  log "Stopping services"
  launchctl bootout system "$MCP_PLIST" 2>/dev/null || true
  launchctl bootout system "$REC_PLIST" 2>/dev/null || true
  rm -f "$MCP_PLIST" "$REC_PLIST"
  if [ "$PURGE" -eq 1 ]; then
    log "Purging $PREFIX, $LOGDIR, and user $SVC_USER"
    rm -rf "$PREFIX" "$LOGDIR"
    dscl . -delete "/Users/$SVC_USER" 2>/dev/null || true
    dscl . -delete "/Groups/$SVC_USER" 2>/dev/null || true
  else
    log "Kept $PREFIX (tickets, log, key, registry). Use --purge to delete them."
  fi
}

if [ "$ACTION" = uninstall ]; then
  uninstall
  exit 0
fi

# --- Python -----------------------------------------------------------------

ok_python() { "$1" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' 2>/dev/null; }
if [ -n "$PY" ]; then
  ok_python "$PY" || die "$PY is not Python 3.11+"
else
  for c in /opt/homebrew/bin/python3.12 /opt/homebrew/bin/python3.13 /opt/homebrew/bin/python3 \
           /usr/local/bin/python3.12 /usr/local/bin/python3.13 /usr/local/bin/python3; do
    if [ -x "$c" ] && ok_python "$c"; then PY="$c"; break; fi
  done
  [ -n "$PY" ] || die "no Python 3.11+ found. Install one: brew install python@3.12"
fi
log "Python: $PY ($("$PY" --version 2>&1))"

# --- Service user -------------------------------------------------------------

if dscl . -read "/Users/$SVC_USER" >/dev/null 2>&1; then
  log "Service user $SVC_USER exists"
else
  used=$( { dscl . -list /Users UniqueID; dscl . -list /Groups PrimaryGroupID; } | awk '{print $2}' )
  NEWID=""
  for i in $(seq 450 499); do
    if ! echo "$used" | grep -qx "$i"; then NEWID=$i; break; fi
  done
  [ -n "$NEWID" ] || die "no free id between 450 and 499"
  log "Creating hidden service user $SVC_USER (uid/gid $NEWID)"
  if ! dscl . -read "/Groups/$SVC_USER" >/dev/null 2>&1; then
    dscl . -create "/Groups/$SVC_USER"
    dscl . -create "/Groups/$SVC_USER" PrimaryGroupID "$NEWID"
    dscl . -create "/Groups/$SVC_USER" RealName "Agentic Governance service"
    dscl . -create "/Groups/$SVC_USER" Password '*'
  fi
  GID=$(dscl . -read "/Groups/$SVC_USER" PrimaryGroupID | awk '{print $2}')
  dscl . -create "/Users/$SVC_USER"
  dscl . -create "/Users/$SVC_USER" UniqueID "$NEWID"
  dscl . -create "/Users/$SVC_USER" PrimaryGroupID "$GID"
  dscl . -create "/Users/$SVC_USER" UserShell /usr/bin/false
  dscl . -create "/Users/$SVC_USER" NFSHomeDirectory /var/empty
  dscl . -create "/Users/$SVC_USER" RealName "Agentic Governance service"
  dscl . -create "/Users/$SVC_USER" Password '*'
  dscl . -create "/Users/$SVC_USER" IsHidden 1
fi

# --- Files ----------------------------------------------------------------------

log "Installing code to $PREFIX"
mkdir -p "$PREFIX"
rsync -a --delete \
  --exclude '/runs/' --exclude '/config/' --exclude '/.venv/' \
  --exclude '__pycache__/' --exclude 'node_modules/' --exclude '/dashboard/' \
  "$SRC/" "$PREFIX/"
# Code: root-owned, readable by all, writable by none. runs/ and config/
# hold the key, registry, tokens, and tickets, so this pass must never
# descend into them (a recursive chmod a+r there would expose the key on a
# reinstall).
find "$PREFIX" \( -path "$PREFIX/runs" -o -path "$PREFIX/config" \) -prune -o -exec chown -h root:wheel {} +
find "$PREFIX" \( -path "$PREFIX/runs" -o -path "$PREFIX/config" \) -prune -o ! -type l -exec chmod go-w,a+rX {} +

mkdir -p "$PREFIX/runs" "$PREFIX/config" "$LOGDIR"
chown -R "$SVC_USER:$SVC_USER" "$PREFIX/runs" "$PREFIX/config" "$LOGDIR"
chmod 700 "$PREFIX/runs" "$PREFIX/config"
chmod -R go-rwx "$PREFIX/runs" "$PREFIX/config"
chmod 750 "$LOGDIR"

log "Python environment"
if [ ! -x "$PREFIX/.venv/bin/python" ]; then
  "$PY" -m venv "$PREFIX/.venv"
fi
"$PREFIX/.venv/bin/pip" install --quiet --disable-pip-version-check --upgrade "mcp>=1.0.0,<2" "pydantic>=2"
chown -R root:wheel "$PREFIX/.venv"
chmod -R go-w "$PREFIX/.venv"
chmod -R a+rX "$PREFIX/.venv"
sudo -u "$SVC_USER" "$PREFIX/.venv/bin/python" -c 'import mcp' \
  || die "the service user cannot run $PY. Use a Python outside your home folder, e.g. --python /opt/homebrew/bin/python3.12"

TOK="$PREFIX/config/mcp_auth_token"
if [ ! -s "$TOK" ]; then
  log "Generating the MCP bearer token"
  (umask 077; openssl rand -hex 32 > "$TOK")
fi
chown "$SVC_USER:$SVC_USER" "$TOK"
chmod 600 "$TOK"

if [ ! -f "$PREFIX/config/integrity.key" ]; then
  log "Keying the event log"
  "$PREFIX/scripts/macos/agctl" integrity init-key
fi

# --- launchd --------------------------------------------------------------------

log "Writing launchd services"
cat > "$MCP_PLIST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL.mcp</string>
  <key>UserName</key><string>$SVC_USER</string>
  <key>GroupName</key><string>$SVC_USER</string>
  <key>ProgramArguments</key>
  <array><string>/bin/bash</string><string>$PREFIX/scripts/macos/run-server.sh</string></array>
  <key>EnvironmentVariables</key>
  <dict><key>AG_PORT</key><string>$PORT</string></dict>
  <key>WorkingDirectory</key><string>$PREFIX</string>
  <key>Umask</key><integer>63</integer>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>$LOGDIR/mcp.log</string>
  <key>StandardErrorPath</key><string>$LOGDIR/mcp.err.log</string>
</dict>
</plist>
PLIST

cat > "$REC_PLIST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL.recover</string>
  <key>UserName</key><string>$SVC_USER</string>
  <key>GroupName</key><string>$SVC_USER</string>
  <key>ProgramArguments</key>
  <array><string>$PREFIX/.venv/bin/python</string><string>$PREFIX/scripts/ticket.py</string><string>recover</string></array>
  <key>EnvironmentVariables</key>
  <dict><key>ADVERSARIAL_ROOT</key><string>$PREFIX</string></dict>
  <key>WorkingDirectory</key><string>$PREFIX</string>
  <key>Umask</key><integer>63</integer>
  <key>StartInterval</key><integer>600</integer>
  <key>StandardOutPath</key><string>$LOGDIR/recover.log</string>
  <key>StandardErrorPath</key><string>$LOGDIR/recover.err.log</string>
</dict>
</plist>
PLIST

chown root:wheel "$MCP_PLIST" "$REC_PLIST"
chmod 644 "$MCP_PLIST" "$REC_PLIST"
for p in "$MCP_PLIST" "$REC_PLIST"; do
  launchctl bootout system "$p" 2>/dev/null || true
  launchctl bootstrap system "$p"
done

log "Waiting for the MCP server on 127.0.0.1:$PORT"
code=000
for _ in $(seq 1 40); do
  code=$(curl -s -o /dev/null -w '%{http_code}' -X POST "http://127.0.0.1:$PORT/mcp" || true)
  [ "$code" = 401 ] && break
  sleep 1
done
if [ "$code" != 401 ]; then
  tail -20 "$LOGDIR/mcp.err.log" 2>/dev/null || true
  die "MCP server did not come up (last HTTP status $code)"
fi

log "Doctor"
"$PREFIX/scripts/macos/agctl" doctor || true

cat <<DONE

Installed. The MCP server runs as $SVC_USER on http://127.0.0.1:$PORT/mcp
and rejects requests without the bearer token (HTTP 401).

Next (each runs as the service user; sudo is the operator gate):
  Register every agent in one sitting, workers and reviewers with different principals:
    sudo $PREFIX/scripts/macos/agctl agent add <id> --team <team> --roles <stage|review:stage> --principal <runtime>
  Each prints a token once. Put it only in that agent's MCP client config.
  Agents connect with two headers' worth of secrets:
    Authorization: Bearer <contents of $TOK>   (read it with: sudo cat $TOK)
    agent_token=<its own token> on every ticket_* call
  Check status any time:  sudo $PREFIX/scripts/macos/agctl doctor
Uninstall (keeps data):    sudo $PREFIX/scripts/macos/harden.sh --uninstall --prefix $PREFIX --user $SVC_USER --label $LABEL
DONE

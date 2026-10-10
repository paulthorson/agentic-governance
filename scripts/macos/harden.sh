#!/bin/bash
# Hardened macOS install for Agentic Governance (ADR-0013).
#
# Runs the framework as its own hidden service user, so agents running as
# your login user can reach it only over MCP and cannot read or write its
# files, even with a shell. Installs:
#
#   <prefix>/                 code, root-owned, read-only for everyone else
#   <prefix>/python           pinned standalone CPython, root-owned (never Homebrew's:
#                             /opt/homebrew is writable by your login user)
#   <prefix>/runs, /config    owned by the service user, mode 700
#   /Library/LaunchDaemons/<label>.mcp.plist      MCP server over HTTP on 127.0.0.1
#   /Library/LaunchDaemons/<label>.recover.plist  stuck-ticket recovery every 10 min
#   /Library/Logs/AgenticGovernance-<label>/      service logs
#
# Usage:
#   sudo scripts/macos/harden.sh [--prefix /Library/AgenticGovernance] [--user _aggov]
#                                [--label app.agenticgovernance] [--port 8765]
#                                [--python-archive FILE]
#   sudo scripts/macos/harden.sh --uninstall [--purge] [same options]
#
# Run it from a fresh clone of a release tag that no agent can write to,
# never from a checkout your agents work in: this script runs as root.
#
# --python-archive uses a local copy of the pinned Python download instead of
# fetching it (it must still match the pinned SHA-256).
# --uninstall stops and removes the launchd services and keeps your data.
# --purge additionally deletes the install directory (tickets, event log,
# integrity key, agent registry), the logs, and the service user. It cannot
# be undone.
#
# Network: downloads the pinned Python once, and pip installs mcp and pydantic.

set -euo pipefail
# Root must never run a program an agent could have replaced (a user-owned
# PATH entry such as /opt/homebrew/bin). System directories only.
export PATH=/usr/bin:/bin:/usr/sbin:/sbin
umask 022

ACTION=install
PURGE=0
PREFIX=/Library/AgenticGovernance
SVC_USER=_aggov
LABEL=app.agenticgovernance
PORT=8765
PY_ARCHIVE=""
SRC="$(cd "$(dirname "$0")/../.." && pwd -P)"
MARKER=.agentic-governance-install
cd /  # commands run as the service user must not inherit an unreadable working directory

# Pinned standalone CPython (python-build-standalone release 20260814).
PBS_RELEASE=20260814
PBS_VERSION=3.12.14
PBS_SHA_arm64=4572133a5542f306b9bdb155da5800f9e38950cd0a98d469b832ce256fe299ea
PBS_SHA_x86_64=1a94c83264731e9603fbea78e57e7ca8f20e7d91eb866627ac2304621b0f6f1f

usage() { sed -n '2,32p' "$0" | sed 's/^# \{0,1\}//'; }
die() { echo "ERROR: $*" >&2; exit 1; }
log() { echo "==> $*"; }

while [ $# -gt 0 ]; do
  case "$1" in
    --uninstall) ACTION=uninstall ;;
    --purge) PURGE=1 ;;
    --prefix) PREFIX="${2:-}"; shift ;;
    --user) SVC_USER="${2:-}"; shift ;;
    --label) LABEL="${2:-}"; shift ;;
    --port) PORT="${2:-}"; shift ;;
    --python-archive) PY_ARCHIVE="${2:-}"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) usage; die "unknown argument: $1" ;;
  esac
  shift
done

[ "$(uname)" = Darwin ] || die "this installer is for macOS"
[ "$(id -u)" -eq 0 ] || die "run with sudo"

# --- Argument checks ------------------------------------------------------------
# Every value below ends up in rm -rf, rsync --delete, chown -R, or dscl -delete.

echo "$LABEL" | grep -Eq '^[A-Za-z0-9][A-Za-z0-9.-]{0,100}$' || die "--label may use letters, digits, '.', '-' only"
echo "$PORT" | grep -Eq '^[0-9]{2,5}$' && [ "$PORT" -ge 1024 ] && [ "$PORT" -le 65535 ] || die "--port must be 1024-65535"
echo "$SVC_USER" | grep -Eq '^_[a-z][a-z0-9_]{1,30}$' || die "--user must look like a service account: _name (leading underscore)"
[ -n "${SUDO_USER:-}" ] && [ "$SVC_USER" = "_${SUDO_USER}" ] && die "--user must not be derived from your own account"

# Owner uid and whether group/other can write (sticky directories excepted,
# since others cannot rename or delete root's entries in them).
unsafe_dir() {
  [ "$(stat -f %u "$1")" = 0 ] || return 0
  [ -n "$(find "$1" -maxdepth 0 \( -perm -0002 -o -perm -0020 \) ! -perm -1000)" ]
}

case "$PREFIX" in /*) ;; *) die "--prefix must be an absolute path" ;; esac
case "$PREFIX" in */|*//*|*/./*|*/../*|*/.|*/..) die "--prefix must be a plain path (no '.', '..', '//', or trailing '/')" ;; esac
PARENT="$(dirname "$PREFIX")"
[ -d "$PARENT" ] || die "parent directory $PARENT does not exist"
PARENT="$(cd "$PARENT" && pwd -P)"
[ "$PARENT" != / ] || die "refusing a top-level prefix ($PREFIX); use something like /Library/AgenticGovernance"
PREFIX="$PARENT/$(basename "$PREFIX")"
case "$PREFIX" in /Users/*|/System/*|/usr/*|/bin/*|/sbin/*|/opt/homebrew/*) die "refusing prefix $PREFIX" ;; esac
p="$PARENT"
while :; do
  unsafe_dir "$p" && die "$p is not root-owned or is writable by others; someone could swap the install out from under root"
  [ "$p" = / ] && break
  p="$(dirname "$p")"
done
[ -L "$PREFIX" ] && die "$PREFIX is a symlink"
case "$PREFIX/" in "$SRC/"*) die "prefix is inside the source tree" ;; esac
case "$SRC/" in "$PREFIX/"*) die "source tree is inside the prefix" ;; esac

LOGDIR="/Library/Logs/AgenticGovernance-$LABEL"
MCP_PLIST="/Library/LaunchDaemons/$LABEL.mcp.plist"
REC_PLIST="/Library/LaunchDaemons/$LABEL.recover.plist"

# A service user we may hand files to or delete: hidden, no shell, uid in
# the range this installer allocates, never root or the invoking user.
is_service_user() {
  local u="$1" uid shell hidden
  uid=$(dscl . -read "/Users/$u" UniqueID 2>/dev/null | awk '{print $2}')
  shell=$(dscl . -read "/Users/$u" UserShell 2>/dev/null | awk '{print $2}')
  hidden=$(dscl . -read "/Users/$u" IsHidden 2>/dev/null | awk '{print $2}')
  [ -n "$uid" ] && [ "$uid" -ge 450 ] && [ "$uid" -le 499 ] && [ "$shell" = /usr/bin/false ] \
    && [ "$hidden" = 1 ] && [ "$u" != root ] && [ "$u" != "${SUDO_USER:-}" ]
}

marker_ok() { # the prefix was made by this installer, for this user and label
  [ -f "$PREFIX/$MARKER" ] && [ ! -L "$PREFIX/$MARKER" ] \
    && grep -qx "user=$SVC_USER" "$PREFIX/$MARKER" && grep -qx "label=$LABEL" "$PREFIX/$MARKER"
}

uninstall() {
  log "Stopping services"
  launchctl bootout system "$MCP_PLIST" 2>/dev/null || true
  launchctl bootout system "$REC_PLIST" 2>/dev/null || true
  rm -f "$MCP_PLIST" "$REC_PLIST"
  if [ "$PURGE" -eq 1 ]; then
    if [ -e "$PREFIX" ]; then
      marker_ok || die "$PREFIX has no install marker for user $SVC_USER and label $LABEL; not deleting it"
      log "Purging $PREFIX"
      rm -rf "$PREFIX"
    fi
    [ -L "$LOGDIR" ] && rm -f "$LOGDIR"
    rm -rf "$LOGDIR"
    if dscl . -read "/Users/$SVC_USER" >/dev/null 2>&1; then
      is_service_user "$SVC_USER" || die "$SVC_USER does not look like a service account this installer made; not deleting it"
      log "Deleting service user $SVC_USER"
      dscl . -delete "/Users/$SVC_USER" 2>/dev/null || true
    fi
    dscl . -delete "/Groups/$SVC_USER" 2>/dev/null || true
  else
    log "Kept $PREFIX (tickets, log, key, registry). Use --purge to delete them."
  fi
}

if [ "$ACTION" = uninstall ]; then
  uninstall
  exit 0
fi

if [ -e "$PREFIX" ]; then
  [ -d "$PREFIX" ] || die "$PREFIX exists and is not a directory"
  [ "$(stat -f %u "$PREFIX")" = 0 ] || die "$PREFIX exists and is not owned by root"
  if [ -n "$(ls -A "$PREFIX")" ] && ! marker_ok; then
    die "$PREFIX is not empty and is not an install for user $SVC_USER and label $LABEL"
  fi
fi

# No git here: running git as root inside a user-owned clone would execute
# that clone's config (hooks, fsmonitor) as root.
log "Source: $SRC (version $(sed -n 's/^CURRENT_VERSION = "\(.*\)"/\1/p' "$SRC/mcp/adversarial_mcp/updates.py" 2>/dev/null | head -1))"
log "Install only from a fresh clone of a release tag that no agent can write to."

# --- Service user -------------------------------------------------------------

if dscl . -read "/Users/$SVC_USER" >/dev/null 2>&1; then
  is_service_user "$SVC_USER" || die "$SVC_USER exists but is not a hidden, shell-less service account (uid 450-499)"
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
chown root:wheel "$PREFIX"
chmod 755 "$PREFIX"
printf 'user=%s\nlabel=%s\n' "$SVC_USER" "$LABEL" > "$PREFIX/$MARKER"
for d in runs config; do
  [ -L "$PREFIX/$d" ] && die "$PREFIX/$d is a symlink"
done
rsync -a --delete \
  --exclude '/runs/' --exclude '/config/' --exclude '/.venv/' --exclude '/python/' \
  --exclude "/$MARKER" \
  --exclude '__pycache__/' --exclude 'node_modules/' --exclude '/dashboard/' --exclude '/.git/' \
  "$SRC/" "$PREFIX/"
# Code: root-owned, readable by all, writable by none. runs/ and config/
# hold the key, registry, tokens, and tickets, so this pass must never
# descend into them (a recursive chmod a+r there would expose the key on a
# reinstall).
find "$PREFIX" \( -path "$PREFIX/runs" -o -path "$PREFIX/config" \) -prune -o -exec chown -h root:wheel {} +
find "$PREFIX" \( -path "$PREFIX/runs" -o -path "$PREFIX/config" \) -prune -o ! -type l -exec chmod go-w,a+rX {} +

[ -L "$LOGDIR" ] && die "$LOGDIR is a symlink"
mkdir -p "$PREFIX/runs" "$PREFIX/config" "$LOGDIR"
for d in "$PREFIX/runs" "$PREFIX/config" "$LOGDIR"; do
  [ -L "$d" ] && die "$d is a symlink"
done
chown -R "$SVC_USER:$SVC_USER" "$PREFIX/runs" "$PREFIX/config" "$LOGDIR"
chmod 700 "$PREFIX/runs" "$PREFIX/config"
chmod -R go-rwx "$PREFIX/runs" "$PREFIX/config"
chmod 750 "$LOGDIR"

# --- Python -----------------------------------------------------------------------
# A root-owned interpreter inside the prefix. A venv on Homebrew's Python
# would load its standard library from /opt/homebrew, which the login user
# (and so every agent) can write: code execution as the service user, and
# as root on the next reinstall.

case "$(uname -m)" in
  arm64) PBS_ARCH=aarch64; PBS_SHA=$PBS_SHA_arm64 ;;
  x86_64) PBS_ARCH=x86_64; PBS_SHA=$PBS_SHA_x86_64 ;;
  *) die "unsupported CPU $(uname -m)" ;;
esac
PBS_FILE="cpython-${PBS_VERSION}+${PBS_RELEASE}-${PBS_ARCH}-apple-darwin-install_only.tar.gz"
PBS_STAMP="$PBS_RELEASE $PBS_VERSION $PBS_ARCH"
if [ "$(cat "$PREFIX/python/.ag-release" 2>/dev/null)" != "$PBS_STAMP" ]; then
  log "Python $PBS_VERSION (python-build-standalone $PBS_RELEASE, $PBS_ARCH)"
  TMPD="$(mktemp -d /private/tmp/ag-python.XXXXXX)"
  trap 'rm -rf "$TMPD"' EXIT
  if [ -n "$PY_ARCHIVE" ]; then
    cp "$PY_ARCHIVE" "$TMPD/py.tgz"
  else
    curl -fsSL --retry 3 -o "$TMPD/py.tgz" \
      "https://github.com/astral-sh/python-build-standalone/releases/download/$PBS_RELEASE/${PBS_FILE//+/%2B}"
  fi
  got=$(shasum -a 256 "$TMPD/py.tgz" | awk '{print $1}')
  [ "$got" = "$PBS_SHA" ] || die "Python download does not match the pinned SHA-256 (got $got)"
  tar -xzf "$TMPD/py.tgz" -C "$TMPD"
  [ -x "$TMPD/python/bin/python3" ] || die "unexpected Python archive layout"
  rm -rf "$PREFIX/python" "$PREFIX/.venv"
  mv "$TMPD/python" "$PREFIX/python"
  echo "$PBS_STAMP" > "$PREFIX/python/.ag-release"
  rm -rf "$TMPD"; trap - EXIT
fi
chown -R root:wheel "$PREFIX/python"
chmod -R go-w,a+rX "$PREFIX/python"
PY="$PREFIX/python/bin/python3"

log "Python environment"
if [ ! -x "$PREFIX/.venv/bin/python" ] || ! grep -q "^home = $PREFIX/python/bin\$" "$PREFIX/.venv/pyvenv.cfg" 2>/dev/null; then
  rm -rf "$PREFIX/.venv"
  "$PY" -m venv "$PREFIX/.venv"
fi
"$PREFIX/.venv/bin/python" -m pip install --quiet --disable-pip-version-check --upgrade "mcp>=1.0.0,<2" "pydantic>=2"
chown -R root:wheel "$PREFIX/.venv"
chmod -R go-w,a+rX "$PREFIX/.venv"
sudo -u "$SVC_USER" "$PREFIX/.venv/bin/python" -c 'import mcp' || die "the service user cannot import mcp"

TOK="$PREFIX/config/mcp_auth_token"
[ -L "$TOK" ] && die "$TOK is a symlink"
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
  <dict><key>AG_PORT</key><string>$PORT</string><key>PATH</key><string>/usr/bin:/bin</string></dict>
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
  <dict><key>ADVERSARIAL_ROOT</key><string>$PREFIX</string><key>PATH</key><string>/usr/bin:/bin</string></dict>
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
  Agents connect with two secrets:
    Authorization: Bearer <contents of $TOK>   (read it with: sudo cat $TOK)
    agent_token=<its own token> on every ticket_* call
  Check status any time:  sudo $PREFIX/scripts/macos/agctl doctor
Uninstall (keeps data):    sudo $PREFIX/scripts/macos/harden.sh --uninstall --prefix $PREFIX --user $SVC_USER --label $LABEL
DONE

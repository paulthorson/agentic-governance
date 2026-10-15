#!/bin/bash
# End-to-end test of the hardened macOS install (ADR-0013).
#
#   sudo scripts/macos/e2e-test.sh [--python-archive FILE]
#
# Self-cleaning: installs into a throwaway prefix under a throwaway service
# user and launchd label, runs every check, then uninstalls with --purge.
# The "agent" is the user who invoked sudo (SUDO_USER): an ordinary account
# with a shell, which is exactly the threat the hardened setup addresses.
#
# Exits 0 only if every check passes. Safe to run on a real Mac: it never
# touches /Library/AgenticGovernance, _aggov, or app.agenticgovernance.

set -uo pipefail
SRC="$(cd "$(dirname "$0")/../.." && pwd)"
PYARG=()
[ "${1:-}" = "--python-archive" ] && PYARG=(--python-archive "$2")

[ "$(uname)" = Darwin ] || { echo "macOS only"; exit 1; }
[ "$(id -u)" -eq 0 ] || { echo "run with sudo"; exit 1; }
AGENT="${SUDO_USER:-}"
[ -n "$AGENT" ] && [ "$AGENT" != root ] || { echo "run via sudo from a normal user account"; exit 1; }

ID=$$
# A root-created directory with an unguessable name, so no other account can
# plant the prefix (or symlinks inside it) ahead of the install.
BASE="$(mktemp -d /private/var/tmp/ag-e2e.XXXXXX)"
chmod 755 "$BASE"
PREFIX="$BASE/install"
SVC="_age2e$ID"
LABEL="app.agenticgovernance.e2e$ID"
PORT=$((18000 + ID % 1000))
URL="http://127.0.0.1:$PORT/mcp"
# --trust-source: CI installs from its own checkout, which a runner user owns.
HARDEN=("$SRC/scripts/macos/harden.sh" --prefix "$PREFIX" --user "$SVC" --label "$LABEL" --port "$PORT" --trust-source)
AGCTL="$PREFIX/scripts/macos/agctl"

PASS=0; FAIL=0
ok()  { echo "PASS: $1"; PASS=$((PASS+1)); }
bad() { echo "FAIL: $1"; FAIL=$((FAIL+1)); }
as_agent() { sudo -u "$AGENT" "$@"; }
denied() { # name, command...: passes when the agent account CANNOT do it
  local name="$1"; shift
  if as_agent "$@" >/dev/null 2>&1; then bad "agent could: $name"; else ok "agent cannot: $name"; fi
}

PEER=""
cleanup() {
  echo "== cleanup"
  [ -n "${HOLD_PIDS:-}" ] && kill $HOLD_PIDS 2>/dev/null
  if [ -n "$PEER" ]; then
    dscl . -delete "/Users/$PEER" 2>/dev/null || true
    dscl . -delete "/Groups/$PEER" 2>/dev/null || true
  fi
  "${HARDEN[@]}" --uninstall --purge >/dev/null 2>&1 || true
  rm -rf "$BASE"
}
trap cleanup EXIT

echo "== the installer refuses dangerous arguments"
refuses() { # name, harden.sh args...: passes when harden.sh exits non-zero before touching anything
  local name="$1"; shift
  if "$SRC/scripts/macos/harden.sh" "$@" >/dev/null 2>&1; then bad "installer accepted: $name"; else ok "installer refuses: $name"; fi
}
refuses "a source tree the agent owns" --prefix "$PREFIX" --user "$SVC" --label "$LABEL" --port "$PORT"
refuses "relative prefix"            --prefix . --user "$SVC" --label "$LABEL" --port "$PORT"
refuses "top-level prefix"           --prefix /Library --user "$SVC" --label "$LABEL" --port "$PORT"
refuses "non-empty foreign dir"      --prefix /Library/Logs --user "$SVC" --label "$LABEL" --port "$PORT"
refuses "purge of a foreign dir"     --uninstall --purge --prefix /Library/Logs --user "$SVC" --label "$LABEL"
refuses "prefix under a user-owned dir" --prefix "/Users/$AGENT/ag" --user "$SVC" --label "$LABEL" --port "$PORT"
refuses "a real account as service user" --prefix "$PREFIX" --user "$AGENT" --label "$LABEL" --port "$PORT"
refuses "label with a slash"         --prefix "$PREFIX" --user "$SVC" --label "../x" --port "$PORT"
AGDIR="$(sudo -u "$AGENT" mktemp -d /private/var/tmp/ag-agent.XXXXXX)"
refuses "prefix the agent created"   --prefix "$AGDIR" --user "$SVC" --label "$LABEL" --port "$PORT"
rm -rf "$AGDIR"
if [ ! -e "$PREFIX" ] && ! dscl . -read "/Users/$SVC" >/dev/null 2>&1; then ok "refusals changed nothing"; else bad "a refused run left changes"; fi

if dscl . -read /Groups/_lpadmin >/dev/null 2>&1; then
  "$SRC/scripts/macos/harden.sh" --uninstall --purge --prefix "$BASE/none" --user _lpadmin --label "$LABEL" >/dev/null 2>&1 || true
  if dscl . -read /Groups/_lpadmin >/dev/null 2>&1; then ok "purge keeps a system group"; else bad "purge deleted the system group _lpadmin"; fi
fi

echo "== install (prefix $PREFIX, user $SVC, port $PORT, agent $AGENT)"
if ! "${HARDEN[@]}" ${PYARG[@]+"${PYARG[@]}"}; then
  echo "FAIL: install"; exit 1
fi
ok "install"

echo "== register agents (operator via sudo agctl)"
ENG=$("$AGCTL" agent add eng-1 --team team-a --roles engineer --principal rt-a | tail -1)
CRIT=$("$AGCTL" agent add eng-critic --team team-a --roles review:engineer --principal rt-b | tail -1)
TWIN=$("$AGCTL" agent add eng-twin --team team-a --roles review:engineer --principal rt-a | tail -1)
if [ ${#ENG} -ge 40 ] && [ ${#CRIT} -ge 40 ] && [ ${#TWIN} -ge 40 ]; then ok "register 3 agents"; else bad "register agents"; fi
if [ ! -e "$PREFIX/runs/approval.ok" ]; then ok "agctl leaves no approval file"; else bad "approval.ok exists"; fi

echo "== the agent account cannot reach governance files"
denied "write runs/"                 /usr/bin/touch "$PREFIX/runs/x"
denied "create approval.ok"          /usr/bin/touch "$PREFIX/runs/approval.ok"
denied "list runs/"                  /bin/ls "$PREFIX/runs"
denied "read the ticket file"        /bin/cat "$PREFIX/runs/in_review.json"
denied "read the integrity key"      /bin/cat "$PREFIX/config/integrity.key"
denied "read the agent registry"     /bin/cat "$PREFIX/config/agents.json"
denied "read the bearer token"       /bin/cat "$PREFIX/config/mcp_auth_token"
denied "modify framework code"       /bin/sh -c "echo x >> '$PREFIX/scripts/chain.py'"
denied "replace framework code"      /bin/mv "$PREFIX/scripts/chain.py" "$PREFIX/scripts/chain.bak"
SITE=$(/usr/bin/find "$PREFIX/python/lib" -maxdepth 2 -name site.py | head -1)
denied "modify the interpreter"      /bin/sh -c "echo x >> '$SITE'"
denied "add to the venv"             /usr/bin/touch "$PREFIX/.venv/lib/x.pth"
if grep -q "^home = $PREFIX/python/bin\$" "$PREFIX/.venv/pyvenv.cfg"; then ok "venv uses the install's own Python"; else bad "venv is not on the install's Python"; fi
denied "run agctl without sudo"      "$AGCTL" agent list
denied "run ticket.py against the store" "$PREFIX/.venv/bin/python" "$PREFIX/scripts/ticket.py" claim --role engineer --team team-a --agent x
if as_agent /bin/test -r "$PREFIX/scripts/ticket.py"; then ok "agent can read code (expected)"; else bad "agent cannot read code"; fi

echo "== agent works through MCP over HTTP"
BEARER=$(cat "$PREFIX/config/mcp_auth_token")
if as_agent /usr/bin/env URL="$URL" BEARER="$BEARER" ENG="$ENG" CRIT="$CRIT" TWIN="$TWIN" \
     "$PREFIX/.venv/bin/python" "$SRC/scripts/macos/e2e_client.py"; then
  ok "agent-side MCP checks"
else
  bad "agent-side MCP checks (see FAIL lines above)"
fi

echo "== operator checks"
if "$AGCTL" verify >/dev/null; then ok "verify clean"; else bad "verify"; fi
DOC=$("$AGCTL" doctor); echo "$DOC"
if echo "$DOC" | grep -q '\[FAIL'; then bad "doctor reports FAIL"; else ok "doctor has no FAIL"; fi

echo "== doctor reports the OS user behind each live MCP connection (S1.1.1)"
# A throwaway hidden, non-admin account stands in for a properly separated
# agent. The account that ran sudo (the CI runner, an admin) stands in for an
# agent running as the operator.
PEER="_agpeer$ID"
used=$( { dscl . -list /Users UniqueID; dscl . -list /Groups PrimaryGroupID; } | awk '{print $2}' )
PEERID=""
for i in $(seq 400 449); do echo "$used" | grep -qx "$i" || { PEERID=$i; break; }; done
dscl . -create "/Groups/$PEER"; dscl . -create "/Groups/$PEER" PrimaryGroupID "$PEERID"
dscl . -create "/Users/$PEER"; dscl . -create "/Users/$PEER" UniqueID "$PEERID"
dscl . -create "/Users/$PEER" PrimaryGroupID "$PEERID"; dscl . -create "/Users/$PEER" UserShell /usr/bin/false
dscl . -create "/Users/$PEER" NFSHomeDirectory /var/empty; dscl . -create "/Users/$PEER" IsHidden 1
HOLD='import socket,sys,time; c=socket.create_connection(("127.0.0.1",int(sys.argv[1]))); time.sleep(30)'
sudo -u "$PEER" "$PREFIX/python/bin/python3" -c "$HOLD" "$PORT" & HOLD_PIDS="$!"
sleep 2
DOC=$("$AGCTL" doctor 2>&1); rc=$?
echo "$DOC" | grep -E '^\[(PASS|FAIL|INFO)\] (agent user|an MCP client|MCP server|no live)' || true
if echo "$DOC" | grep -q "^\[PASS\] agent user $PEER "; then ok "doctor lists a non-admin agent user as PASS"; else bad "doctor did not list $PEER as PASS"; fi
if [ "$rc" -eq 0 ]; then ok "doctor exits 0 with only a non-admin agent connected"; else bad "doctor exit $rc with a non-admin agent"; fi
as_agent "$PREFIX/python/bin/python3" -c "$HOLD" "$PORT" & HOLD_PIDS="$HOLD_PIDS $!"
sleep 2
DOC=$("$AGCTL" doctor 2>&1); rc=$?
if echo "$DOC" | grep -q "^\[FAIL\] an MCP client runs as the operator's login user $AGENT "; then
  ok "doctor fails an agent running as the operator's login"; else bad "doctor did not flag $AGENT"; echo "$DOC"; fi
if [ "$rc" -eq 4 ]; then ok "doctor exits 4 when an agent runs as the operator"; else bad "doctor exit $rc with the operator connected"; fi
kill $HOLD_PIDS 2>/dev/null; wait $HOLD_PIDS 2>/dev/null; HOLD_PIDS=""
dscl . -delete "/Users/$PEER"; dscl . -delete "/Groups/$PEER"; PEER=""

echo "== tamper (simulating someone with service-user rights) is detected and stops writes"
sudo -u "$SVC" /usr/bin/sed -i '' 's/"state": "done"/"state": "queued"/' "$PREFIX/runs/in_review.json"
"$AGCTL" verify >/dev/null 2>&1; rc=$?
if [ "$rc" -eq 4 ]; then ok "tamper detected (exit 4)"; else bad "tamper not detected (exit $rc)"; fi
if "$AGCTL" integrity accept --by e2e --reason "test" >/dev/null; then ok "operator accept"; else bad "operator accept"; fi
if "$AGCTL" verify >/dev/null; then ok "verify clean after accept"; else bad "verify after accept"; fi

echo "== launchd restarts the server if it dies"
PID=$(launchctl print "system/$LABEL.mcp" 2>/dev/null | awk '/^\tpid = /{print $3; exit}')
if [ -n "$PID" ]; then
  kill "$PID" 2>/dev/null || true
  code=000
  for _ in $(seq 1 30); do
    sleep 1
    NEWPID=$(launchctl print "system/$LABEL.mcp" 2>/dev/null | awk '/^\tpid = /{print $3; exit}')
    code=$(curl -s -o /dev/null -w '%{http_code}' -X POST "$URL" || true)
    if [ -n "$NEWPID" ] && [ "$NEWPID" != "$PID" ] && [ "$code" = 401 ]; then break; fi
  done
  if [ "$code" = 401 ] && [ "${NEWPID:-}" != "$PID" ]; then ok "server restarted by launchd"; else bad "server not restarted (pid $PID -> ${NEWPID:-none}, http $code)"; fi
else
  bad "could not find server pid"
fi
PSUSER=$(ps -o user= -p "${NEWPID:-0}" 2>/dev/null | tr -d ' ')
if [ "$PSUSER" = "$SVC" ]; then ok "server runs as $SVC"; else bad "server runs as '${PSUSER:-?}'"; fi

echo "== recovery job runs as the service user"
launchctl kickstart -k "system/$LABEL.recover" >/dev/null 2>&1 || true
sleep 6
if launchctl print "system/$LABEL.recover" 2>/dev/null | grep -q 'last exit code = 0'; then
  ok "recover job exited 0"
else
  bad "recover job did not exit 0"; launchctl print "system/$LABEL.recover" 2>/dev/null | grep -i 'exit' || true
fi

echo "== agctl refuses when the install has been loosened"
chmod o+w "$PREFIX/scripts/chain.py"
"$AGCTL" verify >/dev/null 2>&1; rc=$?
if [ "$rc" -eq 4 ]; then ok "agctl refuses a writable install file (exit 4)"; else bad "agctl ran on a writable install (exit $rc)"; fi
chmod o-w "$PREFIX/scripts/chain.py"

echo "== reinstall over an existing install keeps data and locks"
if "${HARDEN[@]}" ${PYARG[@]+"${PYARG[@]}"} >/dev/null 2>&1; then ok "reinstall"; else bad "reinstall"; fi
if [ "$(stat -f %Lp "$PREFIX/config")" = 700 ] && [ "$(stat -f %Lp "$PREFIX/config/integrity.key")" = 600 ]; then
  ok "config/ still 700, key still 600"; else bad "permissions loosened by reinstall"; fi
if "$AGCTL" verify >/dev/null; then ok "verify clean after reinstall"; else bad "verify after reinstall"; fi

echo "== uninstall --purge removes everything"
trap - EXIT
"${HARDEN[@]}" --uninstall --purge >/dev/null 2>&1
gone=1
[ -e "$PREFIX" ] && gone=0
[ -e "/Library/Logs/AgenticGovernance-$LABEL" ] && gone=0
[ -e "/Library/LaunchDaemons/$LABEL.mcp.plist" ] && gone=0
[ -e "/Library/LaunchDaemons/$LABEL.recover.plist" ] && gone=0
dscl . -read "/Users/$SVC" >/dev/null 2>&1 && gone=0
launchctl print "system/$LABEL.mcp" >/dev/null 2>&1 && gone=0
if [ "$gone" -eq 1 ]; then ok "uninstall --purge left nothing behind"; else bad "uninstall left something behind"; fi
rm -rf "$BASE"

echo "== SUMMARY: PASS=$PASS FAIL=$FAIL"
[ "$FAIL" -eq 0 ]

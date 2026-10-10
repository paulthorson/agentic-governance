#!/bin/bash
# End-to-end test of the hardened macOS install (ADR-0013).
#
#   sudo scripts/macos/e2e-test.sh [--python /opt/homebrew/bin/python3.12]
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
[ "${1:-}" = "--python" ] && PYARG=(--python "$2")

[ "$(uname)" = Darwin ] || { echo "macOS only"; exit 1; }
[ "$(id -u)" -eq 0 ] || { echo "run with sudo"; exit 1; }
AGENT="${SUDO_USER:-}"
[ -n "$AGENT" ] && [ "$AGENT" != root ] || { echo "run via sudo from a normal user account"; exit 1; }

ID=$$
PREFIX="/private/var/tmp/ag-e2e-$ID"
SVC="_age2e$ID"
LABEL="app.agenticgovernance.e2e$ID"
PORT=$((18000 + ID % 1000))
URL="http://127.0.0.1:$PORT/mcp"
HARDEN=("$SRC/scripts/macos/harden.sh" --prefix "$PREFIX" --user "$SVC" --label "$LABEL" --port "$PORT")
AGCTL="$PREFIX/scripts/macos/agctl"

PASS=0; FAIL=0
ok()  { echo "PASS: $1"; PASS=$((PASS+1)); }
bad() { echo "FAIL: $1"; FAIL=$((FAIL+1)); }
as_agent() { sudo -u "$AGENT" "$@"; }
denied() { # name, command...: passes when the agent account CANNOT do it
  local name="$1"; shift
  if as_agent "$@" >/dev/null 2>&1; then bad "agent could: $name"; else ok "agent cannot: $name"; fi
}

cleanup() {
  echo "== cleanup"
  "${HARDEN[@]}" --uninstall --purge >/dev/null 2>&1 || true
}
trap cleanup EXIT

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
if [ ! -e "$PREFIX/runs/approval.ok" ]; then ok "agctl leaves no approval behind"; else bad "approval.ok left behind"; fi

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

echo "== uninstall --purge removes everything"
trap - EXIT
"${HARDEN[@]}" --uninstall --purge >/dev/null 2>&1
gone=1
[ -e "$PREFIX" ] && gone=0
[ -e "/Library/LaunchDaemons/$LABEL.mcp.plist" ] && gone=0
[ -e "/Library/LaunchDaemons/$LABEL.recover.plist" ] && gone=0
dscl . -read "/Users/$SVC" >/dev/null 2>&1 && gone=0
launchctl print "system/$LABEL.mcp" >/dev/null 2>&1 && gone=0
if [ "$gone" -eq 1 ]; then ok "uninstall --purge left nothing behind"; else bad "uninstall left something behind"; fi

echo "== SUMMARY: PASS=$PASS FAIL=$FAIL"
[ "$FAIL" -eq 0 ]

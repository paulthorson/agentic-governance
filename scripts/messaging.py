#!/usr/bin/env python3
"""
Shared messaging for the adversarial-agents framework.

Sends alerts to the operator's configured messaging system. The channel is
configured by the setup wizard (written to config/setup.md) and read here via
env vars, so the framework is not hardcoded to any one platform.

Supported channels (set ALERT_CHANNEL):
  discord    — send via a Discord webhook (ALERT_WEBHOOK_URL)
  whatsapp   — send via a WhatsApp helper command (ALERT_COMMAND)
  imessage   — send via an iMessage helper command (ALERT_COMMAND)
  generic    — send via any command (ALERT_COMMAND); the message is passed as
               the last argument

Config (env):
  ALERT_CHANNEL      the messaging system: discord | whatsapp | imessage | generic
  ALERT_WEBHOOK_URL  webhook URL (discord)
  ALERT_COMMAND      command to run for whatsapp/imessage/generic; the message
                     is appended as the final argument
  ALERT_TO           optional recipient/target (e.g. a phone number or chat id)
  NETWORK_PERMISSION optional override: allow | deny | unknown
                     (else read from config/setup.md). unknown/deny/unset = no egress.

Usage:
  from messaging import send_alert
  send_alert("🚨 VETO .")
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

ALERT_CHANNEL = os.environ.get("ALERT_CHANNEL", "").lower()
ALERT_WEBHOOK_URL = os.environ.get("ALERT_WEBHOOK_URL", "")
ALERT_COMMAND = os.environ.get("ALERT_COMMAND", "")
ALERT_TO = os.environ.get("ALERT_TO", "")

def load_network_permission(repo_root: Path | None = None) -> str:
    """Return allow|deny|unknown.

    Env NETWORK_PERMISSION wins when set. Otherwise parse config/setup.md.
    Missing config → unknown (no egress).
    """
    env = os.environ.get("NETWORK_PERMISSION", "").strip().lower()
    if env in ("allow", "deny", "unknown"):
        return env
    root = repo_root or REPO_ROOT
    p = root / "config" / "setup.md"
    if not p.exists():
        return "unknown"
    section = ""
    try:
        for line in p.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s.startswith("## "):
                section = s[3:].strip().lower()
                continue
            if section == "network permission" and s.startswith("- "):
                body = s[2:].strip().lower()
                if body in ("allow", "deny", "unknown"):
                    return body
                if body == "(unset)":
                    return "unknown"
                # skip honesty bullets under the section
    except OSError:
        return "unknown"
    return "unknown"

def network_permits_egress(repo_root: Path | None = None) -> bool:
    """True only when permission is explicitly allow. unknown/deny = no egress."""
    return load_network_permission(repo_root) == "allow"

def _send_discord(message: str) -> bool:
    """Send via a Discord webhook, or the post-to-discord helper as fallback.
    Returns True on success."""
    if ALERT_WEBHOOK_URL:
        try:
            payload = json.dumps({"content": message}).encode("utf-8")
            req = urllib.request.Request(
                ALERT_WEBHOOK_URL, data=payload,
                headers={"Content-Type": "application/json"},
            )
            urllib.request.urlopen(req, timeout=15)
            return True
        except Exception as e:
            print(f"WARN: Discord webhook failed: {e}", file=sys.stderr)
    # Fallback: post-to-discord.py helper (uses the configured bot token).
    helper = REPO_ROOT.parent / ".openclaw" / "workspace" / "scripts" / "post-to-discord.py"
    if helper.exists():
        try:
            subprocess.run(
                [sys.executable, str(helper), "--text", message],
                capture_output=True, text=True, timeout=30, check=False,
            )
            return True
        except Exception as e:
            print(f"WARN: post-to-discord failed: {e}", file=sys.stderr)
    return False

def _send_command(message: str) -> bool:
    """Send via a configured command (whatsapp/imessage/generic). The message is
    appended as the final argument. Returns True on success."""
    if not ALERT_COMMAND:
        return False
    try:
        cmd = ALERT_COMMAND.split()
        cmd.append(message)
        subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
        return True
    except Exception as e:
        print(f"WARN: alert command failed: {e}", file=sys.stderr)
        return False

def send_alert(message: str) -> bool:
    """Send an alert to the configured channel. Returns True if delivered.

    Requires:
      1. network_permission == allow (unknown/deny/unset = no egress)
      2. operator approval (AG_APPROVAL / runs/approval.ok) before outbound
         webhook or subprocess delivery.
    """
    if not network_permits_egress(REPO_ROOT):
        perm = load_network_permission(REPO_ROOT)
        print(
            f"ALERT blocked (network_permission={perm}; only 'allow' permits egress): "
            f"{message}",
            file=sys.stderr,
        )
        return False

    scripts_dir = str(Path(__file__).resolve().parent)
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    from approval import ApprovalRequired, require_approval

    try:
        require_approval("outbound_alert", REPO_ROOT)
    except ApprovalRequired as e:
        print(f"ALERT blocked (approval required): {e}", file=sys.stderr)
        print(f"ALERT (not delivered): {message}")
        return False

    if ALERT_CHANNEL == "discord":
        return _send_discord(message)
    if ALERT_CHANNEL in ("whatsapp", "imessage", "generic"):
        return _send_command(message)
    # No channel configured: fall back to Discord webhook if present, else print.
    if _send_discord(message):
        return True
    print(f"ALERT (no delivery channel configured): {message}")
    return False

if __name__ == "__main__":
    # CLI: python3 messaging.py "message"
    if len(sys.argv) > 1:
        send_alert(sys.argv[1])
    else:
        print("usage: python3 messaging.py \"message\"")

# Credential Rotation Readiness Checklist — 2026-09-18

Filed by Engineer for THO-152 (Security Hardening, THO-28). Sprint 2026-09-18.
Supports P0 THO-71 unblock. Companion token-purge re-verification evidence is
posted on THO-71.

**Scope note:** This READINESS checklist is the pre-flight for immediate rotation
the moment the owner regenerates tokens. It does NOT perform rotation (THO-57
rotation remains blocked on owner token regen). No secrets are stored here —
only token prefixes and rotation mechanics.

---

## 1. Live credential inventory (as of 2026-09-18)

### 1a. STALE credentials ≥180 days — rotation REQUIRED

| Credential file | Age (days) | Type | Rotate where | In git history risk |
|---|---|---|---|---|
| `gateway-token.txt` + `muse-gateway-token.txt` | — | Live gateway token `935b278f…` (48 chars) | **owner** regenerates gateway token; update all consumers | **YES — compromised in history (THO-71)** |
| `anthropic.json` | 208 | Anthropic API key | console.anthropic.com | no |
| `discord-bot.json` | 208 | Discord bot token | Discord Developer Portal | no |
| `elevenlabs.json` | 206 | ElevenLabs API key | elevenlabs.io dashboard | no |
| `notion.json` | 217 | Notion integration token | Notion integration settings | no |
| `otter-ai.json` | 222 | Otter.ai password | otter.ai account settings | no |

> Per THO-57: the original "8" was a miscount of 7 files; only the 5 above are
> real secrets needing rotation. `discord-allowFrom.json` and `discord-pairing.json`
> are not secrets (allowlist + empty state) and need no rotation.

### 1b. Current (recent) credentials — no rotation needed

`anthropic-key.b64` (28d), `brave.json` (23d), `browser-extension-relay.secret`
(33d), `memori.json` (139d), `openrouter.json` (101d), `supabase.json` (31d),
`sag-api-key` (51 chars), 6 agentmail API keys (all < 3d), paperclip agent keys
(22–23d).

---

## 2. Gateway token rotation readiness (critical path — THO-71 unblock)

**Current state:** `~/.openclaw/secrets/gateway-token.txt` and
`~/.openclaw/secrets/muse-gateway-token.txt` both still hold the compromised
token `935b278f…` (48 chars). The SAME token is embedded in all 9 Paperclip
agent `adapterConfig`s via the `x-openclaw-token` header (verified in
`GET /api/agents/me` response). This is a system-wide rotation.

### Rotation procedure (executes immediately after owner regenerates)
1. **owner** regenerates the gateway token (owner action, not autonomous).
2. Update `~/.openclaw/secrets/gateway-token.txt` (48 chars, new value).
3. Update `~/.openclaw/secrets/muse-gateway-token.txt` to the SAME new value.
4. Update all 9 Paperclip agent `adapterConfig` `x-openclaw-token` headers in the
   paperclip instance config to the new token.
5. Recycle the gateway via the single-owner LaunchAgent
   (`launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway`) — never a
   competing `gateway run` (GATEWAY_SINGLE_OWNER lock).
6. Verify handshake (`prove-handshake.mjs`) passes; confirm all agents
   re-authenticate with the new token.
7. Re-run `scripts/credential-audit.sh` to confirm the token files/rotation
   state is clean and no plaintext regression.

### Rotation scope — all consumers of the gateway token
- `~/.openclaw/secrets/gateway-token.txt`
- `~/.openclaw/secrets/muse-gateway-token.txt`
- All 9 Paperclip agent `adapterConfig.x-openclaw-token` headers
- Gateway process (restart required)

---

## 3. Security posture verification (this run)

- **Permission enforcement:** 0 issues — all credential + paperclip-keys files
  are 0600, dirs 0700.
- **Plaintext secret scan:** 0 issues in workspace config.
- **Credential audit exit:** 0 (clean).

---

## 4. Git history re-verification (THO-71) — summary

Re-verified against `github.com/paulthorson/agentic-governance` after remote
advanced 151 commits to `ebe2a1d`:
- Live gateway token `935b278f…` / `4fe7482c…` — **absent** from all of:
  - full `origin/main` history (`git log -S` = nothing)
  - all refs (`git rev-list --all` + grep = nothing)
  - the 151 new commits (`15ead2e..ebe2a1d`)
  - all 4 new branches
- The personal Gmail address was **not** used as any author/committer identity
  (`git log --format` = only noreply + Cursor Agent).
- No local absolute paths (`/Users/…`) or proper-name PII in the new commits.
- One benign prose reference to the scrubbed Gmail address inside
  `docs/history-identity-scrub-2026-09-18.md` (documents the scrub; not a live
  identity leak).

**Conclusion:** The 2026-08-24/2026-08-27 purge held; no fresh token exposure
re-landed. The only outstanding item on THO-71 is the live gateway token
**rotation**, which remains blocked on owner regeneration.

---

## 5. Immediate unblock chain

- THO-152 (this story) → done-when met: purge re-verified (evidence on THO-71)
  + rotation-readiness checklist filed (this doc).
- THO-71 (purge incomplete) → the purge is verified COMPLETE; only item is token
  rotation awaiting owner approval/regeneration. Re-verified by Engineer this run.
- THO-57 (rotate stale creds) → remains blocked on owner regenerating the 5
  external-service tokens (Anthropic, Discord, ElevenLabs, Notion, Otter.ai)
  + the gateway token.

**Everything is staged and ready to execute the moment owner regenerates the
tokens.**

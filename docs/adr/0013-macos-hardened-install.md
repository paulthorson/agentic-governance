# ADR-0013: Hardened Install on macOS

- **Status:** Proposed
- **Date:** 2026-10-10
- **Builds on:** ADR-0011, ADR-0012

## Context

ADR-0012 detects edits to governance files but cannot prevent them: code
cannot stop a process from writing files its own OS user can write. The
first pilot ran on a Mac where every agent inherited a shell and ran as the
operator's user. Those agents could have read the integrity key, the agent
registry, and other agents' tokens, and could have created
`runs/approval.ok` to act as an operator. The governance was an audit
trail, not a control.

`docs/deployment-hardened.md` described the fix (a separate OS user) for
Linux only. The pilot's agents run on macOS.

## Decision

Ship a scripted, tested macOS install:

- `scripts/macos/harden.sh` creates a hidden service user (`_aggov`, no
  shell, no home), installs the code root-owned and read-only, gives the
  service user sole ownership of `runs/` and `config/` (mode 700), and runs
  two launchd daemons as that user: the MCP server on 127.0.0.1 with a
  bearer token, and recovery every 10 minutes. It keys the event log on
  first install. The code-permission pass never descends into `runs/` or
  `config/`, so a reinstall cannot expose the key.
- **The interpreter is part of the code.** The install carries its own
  CPython (a pinned python-build-standalone release, SHA-256 checked),
  owned by root. A venv on Homebrew's Python would load its standard
  library from `/opt/homebrew`, which the login user owns on Apple
  Silicon: any agent could run code as the service user, and as root on
  the next reinstall.
- **Arguments are checked before anything is touched.** `--prefix` must be
  absolute and plain, below the top level, with every ancestor root-owned
  and not writable by others (sticky directories excepted). A prefix that
  exists must be root-owned and either empty or carry the installer's
  marker for this user and label; `rsync --delete` and `--purge` never run
  without it. `--user` must be a hidden, shell-less account in the uid
  range the installer allocates. `runs/`, `config/`, and the log folder
  must not be symlinks. Root runs with a system-only PATH and never runs
  git.
- The bearer token lives in `config/` and is read by
  `scripts/macos/run-server.sh` at start, so it never appears in the
  world-readable LaunchDaemon plist. The server's environment is stripped of
  agent tokens and approval variables.
- `scripts/macos/agctl` is the operator interface. It requires sudo, runs
  `ticket.py` as the service user with a clean environment, and passes
  approval to that one process as `AG_APPROVAL=1`. It never writes
  `runs/approval.ok`, which the long-running server (same uid) would also
  honor, and deletes one if found. Before running, it refuses (exit 4) if
  any install file outside `runs/` and `config/` is not root-owned or is
  group- or other-writable, or if the venv is not built on the install's
  own Python. **sudo becomes the operator gate:** an agent that cannot sudo
  cannot perform operator actions, shell or not.
- `overturn_verdict` requires operator approval. The hardened server never
  has approval, so agents cannot overturn precedent over MCP.
- `scripts/macos/e2e-test.sh` installs under a throwaway user, label, and
  prefix, attacks the install from an ordinary account, runs a full MCP
  ticket loop over HTTP, checks tamper detection, launchd restart, and the
  recovery job, then uninstalls with `--purge`. CI runs it on
  `macos-latest` on every pull request.

## Consequences

- **Positive:** on a hardened install, agents with a shell cannot read or
  write governance state, cannot read other agents' tokens from the
  registry, and cannot act as an operator. Detection (ADR-0012) becomes
  prevention for everything below root.
- **Positive:** the claim is tested on a real Mac on every PR, not argued.
- **Negative:** anyone who can sudo can do anything, including agents if
  they are given sudo or the operator's password. Agents must not have it.
- **Negative:** the installer runs as root from whatever source it is given.
  Installing from a checkout an agent can write hands that agent root. The
  docs install from a root-owned fresh clone of a release tag; the script
  cannot enforce this.
- **Negative:** `pip` fetches `mcp` and `pydantic` from PyPI without hash
  pinning. A compromised package release would run as root during install.
- **Negative:** there is no operator path to overturn precedent on a
  hardened install yet (`overturn_verdict` is refused over MCP and has no
  `ticket.py` command).
- **Negative:** agent tokens still live in each agent's own config. Two
  agents running as the same user can read each other's token files. Give
  each agent runtime its own OS user, or accept that risk per agent.
- **Negative:** the MCP server listens on loopback only. Remote reviewers
  need a deliberate, authenticated path in; this ADR does not provide one.
- **Negative:** one service user per install. Several teams on one Mac
  either share an install (and a store) or use separate prefixes, users,
  labels, and ports.

## Alternatives considered

- **Have an agent run the installer:** rejected. The installer needs sudo,
  and the agent being governed would configure its own governance.
- **macOS sandbox profiles:** finer-grained, but `sandbox-exec` is
  deprecated and profiles would have to wrap every agent runtime.
- **Containers:** not native on macOS without a VM; the agents in scope run
  as native processes.

## References

- [[ADR-0011]] · [[ADR-0012]] · `scripts/macos/` · `docs/deployment-hardened.md`
  · `.github/workflows/validate.yml` job `macos-hardened`

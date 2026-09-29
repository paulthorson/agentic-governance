"""Approval checkpoints for irreversible or high-impact actions.

A control that exists only as text is guidance. This module is real enforcement
for the call sites that import it: without approval, the action refuses.

Approval is granted when any of:
  - env ``AG_APPROVAL=1`` (or ``true`` / ``yes``)
  - env ``AG_APPROVAL_TOKEN`` matches the contents of ``runs/approval.token``
  - file ``runs/approval.ok`` exists (operator-created one-shot; deleted after use
    when ``consume=True``)

Own-directory writes under the repo are generally not gated here. Subprocess,
outbound network, and writes outside the repo root are.
"""

from __future__ import annotations

import os
import stat
import sys
from pathlib import Path


class ApprovalRequired(RuntimeError):
    """Raised when a gated action is attempted without operator approval."""


def _repo_root() -> Path:
    return Path(os.environ.get("ADVERSARIAL_ROOT", Path(__file__).resolve().parents[1]))


def _truthy(val: str | None) -> bool:
    if not val:
        return False
    return val.strip().lower() in ("1", "true", "yes", "on")


def has_approval(repo_root: Path | None = None, *, consume: bool = False) -> bool:
    """Return True if the operator has granted approval for a gated action."""
    if _truthy(os.environ.get("AG_APPROVAL")):
        return True

    root = repo_root or _repo_root()
    token_env = os.environ.get("AG_APPROVAL_TOKEN", "").strip()
    token_file = root / "runs" / "approval.token"
    if token_env and token_file.exists():
        try:
            _tighten_secret_file(token_file)
            if token_file.read_text(encoding="utf-8").strip() == token_env:
                return True
        except OSError:
            pass

    ok = root / "runs" / "approval.ok"
    if ok.exists():
        if consume:
            try:
                ok.unlink()
            except OSError:
                pass
        return True
    return False


def _tighten_secret_file(path: Path) -> None:
    """If approval.token is group/world-readable, chmod 0o600 when possible.

    This framework never creates approval.token — the operator does. On read we
    attempt to tighten mode so other local users cannot read a shared token.
    If chmod fails (not owner / unsupported FS), warn on stderr and continue.
    """
    try:
        mode = path.stat().st_mode
    except OSError:
        return
    if mode & (stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH):
        try:
            path.chmod(0o600)
        except OSError as e:
            print(
                f"WARN: {path} is group/world-accessible and could not be "
                f"chmod 0600 ({e}). Other local users may read the approval token.",
                file=sys.stderr,
            )


def require_approval(
    action: str,
    repo_root: Path | None = None,
    *,
    consume: bool = False,
) -> None:
    """Refuse unless approval is present.

    ``action`` is a short label included in the error (e.g. ``git_apply``,
    ``outbound_alert``, ``paperclip_subprocess``, ``ollama_generate``,
    ``outside_write``).
    """
    if has_approval(repo_root, consume=consume):
        return
    raise ApprovalRequired(
        f"Approval required for '{action}'. Set AG_APPROVAL=1, or place "
        f"runs/approval.ok, or set AG_APPROVAL_TOKEN to match runs/approval.token. "
        f"Without approval this action is blocked."
    )


def is_outside_repo(path: Path, repo_root: Path | None = None) -> bool:
    """True if path resolves outside the repo root."""
    root = (repo_root or _repo_root()).resolve()
    try:
        path.resolve().relative_to(root)
        return False
    except ValueError:
        return True

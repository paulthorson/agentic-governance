"""Cos memory seating hook — part of AG install/setup when Chief of Staff is seated.

Not a deferred README-only step. The conversational setup wizard
(`setup_wizard.py`) MUST call `apply_at_cos_seating` when a Cos roster row
is present. Operators may also re-run this module via the CLI stub at
`scripts/cos_memory_setup.py`.

operator + Cos clarified store = private git (their operator memory).
Framework Cos ASKS private_git OR local_folder — do not force one mode.
Skeleton SoT: docs/templates/cos-memory/
Local scaffold: config/cos-memory/ (gitignored)
P0: no secrets/keys/emails/PII/absolute host paths.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

COS_MEMORY_MODES = ["private_git", "local_folder"]

SKELETON_REL = Path("docs") / "templates" / "cos-memory"
SCAFFOLD_REL = Path("config") / "cos-memory"


def looks_like_forbidden_memory_label(value: str) -> bool:
    """P0: reject absolute host paths, emails, and obvious secret-shaped labels."""
    v = (value or "").strip()
    if not v:
        return True
    if "/" in v or "\\" in v or v.startswith("~"):
        return True
    if "@" in v:
        return True
    if len(v) > 64:
        return True
    return False


def apply_at_cos_seating(
    repo_root: Path,
    mode: str,
    label: str,
    *,
    has_cos: bool,
) -> list[Path]:
    """Scaffold Cos memory at Cos seating time.

    Called by the setup wizard finalize path when Chief of Staff is seated.
    Supports both private_git and local_folder — same scaffold either way.
    private_git operators copy this pack into their private repo; local_folder
    operators keep it under gitignored config/. Never writes absolute host paths.
    """
    if not has_cos:
        return []
    if mode not in COS_MEMORY_MODES:
        return []
    safe_label = (label or "").strip() or "cos-memory"
    if looks_like_forbidden_memory_label(safe_label):
        return []

    dest = repo_root / SCAFFOLD_REL
    dest.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    src = repo_root / SKELETON_REL
    if src.is_dir():
        for path in sorted(src.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(src)
            target = dest / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                target.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
                written.append(target)
    else:
        stubs = {
            "README.md": (
                "# Cos memory store\n\n"
                "Scaffolded at Cos seating (AG install/setup). "
                "Skeleton SoT: docs/templates/cos-memory/.\n"
            ),
            "profile.md": (
                "# Cos operator profile\n\n"
                "## Storage mode\n\n"
                "- operator + Cos clarified store: private git\n"
                "- Mode (this install): (see STORAGE_MODE.md)\n"
            ),
            "locks.md": "# Operator / Cos LOCKs\n\n",
            "log.md": "# Cos↔human episode log\n\n",
            "log/README.md": "# Dated episode files\n\n",
            "log/_episode.md": "# YYYY-MM-DD — episode title\n\n",
        }
        for rel, body in stubs.items():
            target = dest / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                target.write_text(body, encoding="utf-8")
                written.append(target)

    mode_path = dest / "STORAGE_MODE.md"
    mode_body = (
        "# Cos memory storage mode\n\n"
        "Set at AG install/setup when Chief of Staff was seated — "
        "**not** a later optional README-only step.\n\n"
        "- **operator + Cos clarified store:** private git (their operator memory — "
        "not a force on every install).\n"
        "- **Framework ASK:** Cos prompts `private_git` OR `local_folder` — "
        "do not force one mode.\n\n"
        f"- mode (this install): `{mode}`\n"
        f"- label: `{safe_label}`\n"
        f"- skeleton SoT: `{SKELETON_REL.as_posix()}`\n"
        f"- local scaffold: `{SCAFFOLD_REL.as_posix()}` (gitignored)\n\n"
        "## Path A — private_git\n\n"
        "Copy this scaffold into a **private** git repo and commit there. "
        "Do not push filled memory to public AG.\n\n"
        "## Path B — local_folder\n\n"
        f"Keep this scaffold as your on-machine private store under "
        f"`{SCAFFOLD_REL.as_posix()}`.\n\n"
        "## P0\n\n"
        "No secrets, keys, emails, PII, or absolute host paths.\n"
    )
    mode_path.write_text(mode_body, encoding="utf-8")
    written.append(mode_path)
    return written


def seating_prompt_summary() -> dict[str, Any]:
    """Operator-facing summary of the Cos seating memory ASK (for docs/CLI)."""
    return {
        "when": "AG install/setup when Chief of Staff is seated (setup wizard after roster)",
        "not": "deferred README-only optional step",
        "operator_cos_clarified_store": "private_git",
        "framework_ask": COS_MEMORY_MODES,
        "force_one_mode": False,
        "skeleton": SKELETON_REL.as_posix(),
        "scaffold": SCAFFOLD_REL.as_posix(),
        "wizard_must_call": "apply_at_cos_seating",
        "cli_stub": "scripts/cos_memory_setup.py",
    }

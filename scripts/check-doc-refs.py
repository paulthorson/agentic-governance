#!/usr/bin/env python3
"""
Check that paths mentioned in the repo's markdown point at things that exist.

This is the guard against the two ways the docs have gone stale before:
a file is moved and the prose still names the old place (the constitution
relocation), or a script is described that was never committed.

Checked, in every tracked .md file:

  1. `scripts/<name>.py|.sh|.mjs` mentions: the file must exist.
  2. Relative paths that start with `../` (in backticks or link targets):
     resolved from the file's own directory, the target must exist. These are
     the harness "Read first" paths, so a broken one means an agent loads
     without its constitution or standard.
  3. Bare relative `.md` paths in backticks (`docs/foo.md`) whose first
     directory exists beside the file or at the repo root: the file must too.
     Paths into directories the repo does not have (`config/`, a run's `qa/`)
     are created by an operator or a run and are skipped, as is any line that
     calls the file optional, proposed ("(new)"), or "not in this repo".
  4. Relative markdown link targets `[text](path)` with no scheme: the target
     must exist (anchors are stripped; anchor-only links are skipped).
  5. The retired path `references/constitution.md` must not appear anywhere
     except CHANGELOG.md, which records that it was retired.

Paths containing a placeholder (`<`, `*`, `{`, `$`) are skipped: they are
patterns, not references. Exit 1 on any failure.

Usage: python3 scripts/check-doc-refs.py [--root <repo root>]
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_REF = re.compile(r"(?<![\w/.])scripts/[A-Za-z0-9_./-]+\.(?:py|sh|mjs)\b")
REL_PATH = re.compile(r"`((?:\.\./)+[^\s`'\"<>]+)`|\]\(((?:\.\./)+[^)\s#]+)")
MD_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
BARE_MD = re.compile(r"`((?!\.\./)(?!/)[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+\.md)`")
PLACEHOLDER = re.compile(r"[<>*{}$]|NNNN")
# A line that says the file is optional, proposed, or lives elsewhere is not a claim it exists.
OPTIONAL = re.compile(r"if present|if it exists|optional|to fill in|\(new\)|not in this repo", re.I)
RETIRED = ["references/constitution.md"]
SKIP_DIRS = {".git", "runs", "node_modules", ".venv", "python"}


def tracked_markdown(root: Path) -> list[Path]:
    try:
        out = subprocess.run(["git", "-C", str(root), "ls-files", "*.md", "**/*.md"],
                             capture_output=True, text=True, check=True).stdout
        files = [root / line for line in out.splitlines() if line]
    except (subprocess.CalledProcessError, FileNotFoundError):
        files = [p for p in root.rglob("*.md")]
    return sorted(p for p in files
                  if p.is_file() and not (set(p.relative_to(root).parts[:-1]) & SKIP_DIRS))


def tracked_directories(root: Path) -> set[str]:
    """Every directory that holds a tracked file, as a posix path relative to root."""
    try:
        out = subprocess.run(["git", "-C", str(root), "ls-files"], capture_output=True, text=True, check=True).stdout
        paths = [Path(line) for line in out.splitlines() if line]
    except (subprocess.CalledProcessError, FileNotFoundError):
        paths = [p.relative_to(root) for p in root.rglob("*") if p.is_file()]
    dirs: set[str] = set()
    for p in paths:
        for parent in p.parents:
            if parent.as_posix() != ".":
                dirs.add(parent.as_posix())
    return dirs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    args = ap.parse_args()
    root = Path(args.root).resolve()

    errors: list[str] = []
    files = tracked_markdown(root)
    tracked_dirs = tracked_directories(root)
    for f in files:
        rel = f.relative_to(root)
        text = f.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()

        for lineno, line in enumerate(lines, 1):
            for retired in RETIRED:
                if retired in line and rel.name != "CHANGELOG.md":
                    errors.append(f"{rel}:{lineno}: retired path `{retired}` (constitutions live in constitution/domains/)")

            for m in SCRIPT_REF.finditer(line):
                target = m.group(0)
                if PLACEHOLDER.search(target):
                    continue
                if not (root / target).exists() and not (f.parent / target).exists():
                    errors.append(f"{rel}:{lineno}: `{target}` does not exist")

            for m in REL_PATH.finditer(line):
                target = m.group(1) or m.group(2)
                target = target.rstrip(".,;:").split("#")[0]
                if PLACEHOLDER.search(target):
                    continue
                if not (f.parent / target).exists():
                    errors.append(f"{rel}:{lineno}: `{target}` does not resolve from {rel.parent}/")

            for m in BARE_MD.finditer(line):
                target = m.group(1)
                if PLACEHOLDER.search(target) or OPTIONAL.search(line):
                    continue
                head = target.split("/")[0]
                # Resolve from the file's directory, each ancestor, and the root
                # (plugin files write paths relative to the plugin root). Flag only
                # when none resolves AND some base has a tracked directory named
                # like the first segment. `config/setup.md` or a run's `qa/results.md`
                # name files an operator or a run creates later; nothing to check.
                bases = [f.parent, *f.parent.parents]
                bases = [b for b in bases if b == root or root in b.parents]
                if any((b / target).exists() for b in bases):
                    continue
                claimed = [b for b in bases if (b / head).relative_to(root).as_posix() in tracked_dirs]
                if claimed:
                    where = ", ".join((b.relative_to(root).as_posix() or ".") + "/" for b in claimed)
                    errors.append(f"{rel}:{lineno}: `{target}` does not exist under {where}")

            for m in MD_LINK.finditer(line):
                target = m.group(1)
                if "://" in target or target.startswith(("#", "mailto:", "/")) or PLACEHOLDER.search(target):
                    continue
                if target.startswith("../"):
                    continue  # handled above
                path = target.split("#")[0]
                if not path:
                    continue
                if not (f.parent / path).exists():
                    errors.append(f"{rel}:{lineno}: link target `{target}` does not exist")

    if errors:
        for e in errors:
            print(e)
        print(f"\n{len(errors)} broken reference(s) in {len(files)} markdown files")
        return 1
    print(f"doc refs OK: {len(files)} markdown files, no broken paths")
    return 0


if __name__ == "__main__":
    sys.exit(main())

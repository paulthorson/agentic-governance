#!/usr/bin/env python3
"""A23: make the harness files the single source of truth.

The harness bodies are duplicated between `harnesses/<role>.md` and the spec's
inline copies (Sections 5.0-5.4 and 10). A23 decides the harness file is the
source of truth and the spec's inline copy is replaced by a pointer.

This script replaces each inline harness body in the spec with a pointer to
the harness file, so the two cannot drift. It keeps the surrounding spec
content (e.g. Research's "Why the chain needs it", the CEO intro and decision
procedure) and replaces only the harness body itself.

Usage:
  python3 scripts/sync-harnesses.py            # replace inline bodies with pointers
  python3 scripts/sync-harnesses.py --check    # verify the spec has no inline bodies
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SPEC = REPO_ROOT / "docs" / "agentic-governance-spec.md"

# role -> the section header that precedes its inline harness body, and the
# next section header that ends it. The harness body starts at "**Read first**"
# and runs to the next section header.
INLINE_BOUNDS = [
    # (role, section_header, next_section_header)
    ("researcher", "#### The harness", "### 5.1"),
    ("pm", "### 5.1 Product Manager Harness", "### 5.2"),
    ("ux", "### 5.2 UX Harness", "### 5.3"),
    ("engineer", "### 5.3 Engineer Harness", "### 5.4"),
    ("qa", "### 5.4 QA Harness", "## 10."),
    ("ceo", "## 10. CEO Bot Harness", "### 10.1"),
]

def _pointer_block(role: str) -> str:
    return (
        f"The harness is the **source of truth** at `harnesses/{role}.md` "
        f"(A23). The inline copy is not maintained here; edit the harness file.\n"
    )

def _replace_inline(text: str, role: str, section_header: str, next_header: str) -> tuple[str, bool]:
    """Replace the inline harness body for `role` with a pointer.

    The body starts at the first "**Read first**" at or after the section header
    and runs to the next section header. Returns (new_text, changed).
    """
    sec_idx = text.find(section_header)
    if sec_idx == -1:
        return text, False
    # Find the harness body start: the first "**Read first**" after the header.
    body_start = text.find("**Read first**", sec_idx)
    if body_start == -1:
        return text, False
    # Find the end: the next section header after the body start.
    end_idx = text.find(next_header, body_start)
    if end_idx == -1:
        return text, False
    # Keep everything up to the body start, replace the body with a pointer,
    # keep everything from the next header on.
    new_text = text[:body_start] + _pointer_block(role) + "\n" + text[end_idx:]
    return new_text, True

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="verify no inline bodies remain")
    args = ap.parse_args()

    text = SPEC.read_text(encoding="utf-8")
    changed = False
    for role, section_header, next_header in INLINE_BOUNDS:
        text, c = _replace_inline(text, role, section_header, next_header)
        changed = changed or c

    if args.check:
        # Verify no inline harness bodies remain. A harness body starts with
        # "**Read first**\n" (a standalone line); an inline reference like
        # "**Read first** is not decoration" is not a body and is fine.
        remaining = text.count("**Read first**\n")
        if remaining:
            print(f"FAIL: {remaining} inline harness body(s) remain in the spec.")
            return 1
        print("OK: no inline harness bodies remain; harness files are the source of truth.")
        return 0

    if changed:
        SPEC.write_text(text, encoding="utf-8")
        print("Replaced inline harness bodies with pointers to harnesses/.")
    else:
        print("No changes needed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())

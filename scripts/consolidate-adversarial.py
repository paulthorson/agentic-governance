#!/usr/bin/env python3
"""
Rebuild the flat, namespaced `agents/` and `skills/` layers from the plugin
folders, or check that they are already in sync.

The plugin folders (`adversarial-<domain>/`) are the source of truth. The
flat layer exists so that a single checkout can be pointed at by a harness
that registers agents and skills from one directory. It is generated, never
hand-edited:

  adversarial-engineer/agents/critic.md          -> agents/eng-critic.md
  adversarial-qa/skills/adversarial-qa/SKILL.md  -> skills/qa-adversarial-qa/SKILL.md

Two things change on the way across:

  1. `name:` in the frontmatter gets the domain prefix, so names stay unique
     across all plugins (every plugin has a `critic` and an `altitude-check`).
  2. Relative paths (`../references/x.md`, `../../constitution/domains/x.md`)
     are re-pointed so they still resolve from the flat location.

Nothing else is touched, and nothing is written outside the repo: this script
does not symlink into any harness directory. How a harness picks up the flat
layer is that harness's business.

Usage:
  python3 scripts/consolidate-adversarial.py            # rebuild agents/ and skills/
  python3 scripts/consolidate-adversarial.py --check    # exit 1 if the flat layer is stale
  python3 scripts/consolidate-adversarial.py --root <repo root>

`--check` is what CI runs. It fails on any flat file that differs from what the
plugins would generate, and on any flat file that no plugin produces.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

# plugin directory suffix -> flat-layer prefix
PREFIXES = {
    "compliance": "comp",
    "docs": "doc",
    "engineer": "eng",
    "ops": "ops",
    "privacy": "priv",
    "product": "prod",
    "prompt": "prom",
    "qa": "qa",
    "researcher": "res",
    "security": "sec",
    "universal": "univ",
    "ux": "ux",
}

# A relative path token: one or more `../` followed by a path with no spaces,
# quotes, backticks or closing brackets/parens. Markdown wraps these in
# backticks or link parens, so stopping at those characters is enough.
REL_PATH = re.compile(r"(?:\.\./)+[^\s`'\")\]>]+")


def rewrite_paths(text: str, src_dir: Path, dst_dir: Path, root: Path) -> str:
    """Re-point every `../...` path so it resolves from dst_dir instead of src_dir."""

    def fix(m: re.Match) -> str:
        token = m.group(0)
        # Trailing punctuation that belongs to the sentence, not the path.
        trail = ""
        while token and token[-1] in ".,;:":
            trail = token[-1] + trail
            token = token[:-1]
        slash = "/" if token.endswith("/") else ""
        target = (src_dir / token).resolve()
        try:
            target.relative_to(root)
        except ValueError:
            return m.group(0)  # points outside the repo; leave it alone
        return os.path.relpath(target, dst_dir).replace(os.sep, "/") + slash + trail

    return REL_PATH.sub(fix, text)


def rewrite_name(text: str, prefix: str) -> str:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return text
    fm = m.group(1)
    new_fm, n = re.subn(r"^name:\s*(\S+)\s*$", lambda mm: f"name: {prefix}-{mm.group(1)}", fm, count=1, flags=re.MULTILINE)
    if n == 0:
        return text
    return text[: m.start(1)] + new_fm + text[m.end(1):]


def generate(root: Path) -> dict[Path, bytes]:
    """Return {flat path relative to root: bytes} for the whole flat layer."""
    out: dict[Path, bytes] = {}
    for plugin in sorted(p for p in root.iterdir() if p.is_dir() and p.name.startswith("adversarial-")):
        domain = plugin.name[len("adversarial-"):]
        prefix = PREFIXES.get(domain)
        if prefix is None:
            raise SystemExit(f"no flat-layer prefix for plugin {plugin.name}; add it to PREFIXES")

        agents = plugin / "agents"
        if agents.is_dir():
            for f in sorted(agents.iterdir()):
                if f.suffix != ".md":
                    continue
                dst = Path("agents") / f"{prefix}-{f.name}"
                text = f.read_text(encoding="utf-8")
                text = rewrite_name(text, prefix)
                text = rewrite_paths(text, agents, root / "agents", root)
                out[dst] = text.encode("utf-8")

        skills = plugin / "skills"
        if skills.is_dir():
            for sk in sorted(d for d in skills.iterdir() if d.is_dir() and not d.name.startswith(".")):
                dst_dir = Path("skills") / f"{prefix}-{sk.name}"
                for f in sorted(p for p in sk.rglob("*") if p.is_file()):
                    rel = f.relative_to(sk)
                    dst = dst_dir / rel
                    if f.suffix == ".md":
                        text = f.read_text(encoding="utf-8")
                        if f.name == "SKILL.md":
                            text = rewrite_name(text, prefix)
                        text = rewrite_paths(text, f.parent, root / dst.parent, root)
                        out[dst] = text.encode("utf-8")
                    else:
                        out[dst] = f.read_bytes()
    return out


def existing(root: Path) -> dict[Path, bytes]:
    out: dict[Path, bytes] = {}
    for layer in ("agents", "skills"):
        base = root / layer
        if not base.is_dir():
            continue
        for f in base.rglob("*"):
            if f.is_file() and not any(part.startswith(".") for part in f.relative_to(root).parts):
                out[f.relative_to(root)] = f.read_bytes()
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--check", action="store_true", help="report drift and exit 1 instead of writing")
    args = ap.parse_args()
    root = Path(args.root).resolve()

    want = generate(root)
    have = existing(root)

    stale = sorted(p for p in want if have.get(p) != want[p])
    orphan = sorted(p for p in have if p not in want)

    if args.check:
        for p in stale:
            print(f"STALE   {p}  (differs from what {'adversarial-*' } would generate)")
        for p in orphan:
            print(f"ORPHAN  {p}  (no plugin produces this file)")
        if stale or orphan:
            print(f"\nflat layer out of sync: {len(stale)} stale, {len(orphan)} orphan. "
                  f"Run: python3 scripts/consolidate-adversarial.py")
            return 1
        print(f"flat layer in sync: {sum(1 for p in want if p.parts[0] == 'agents')} agents, "
              f"{len({p.parts[1] for p in want if p.parts[0] == 'skills'})} skills")
        return 0

    for p in stale:
        dst = root / p
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(want[p])
        print(f"wrote   {p}")
    for p in orphan:
        (root / p).unlink()
        print(f"removed {p}")
    # Drop skill folders left empty by removals.
    skills = root / "skills"
    if skills.is_dir():
        for d in sorted(skills.rglob("*"), reverse=True):
            if d.is_dir() and not any(d.iterdir()):
                d.rmdir()
    print(f"flat layer rebuilt: {len(stale)} written, {len(orphan)} removed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

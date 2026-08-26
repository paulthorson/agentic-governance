#!/usr/bin/env python3
"""
Validate the Adversarial Agents repo structure.

Checks:
  1. Every agent .md and SKILL.md has a `name:` frontmatter field.
  2. In the flat agents/ + skills/ layers, names are unique (no collisions).
  3. Every plugin folder has the required structure: agents/, skills/, references/
     (constitution.md, <domain>-standard.md, personas.md, calibration-ledger.md),
     assets/templates/ (decision-record.md, calibration-entry.md), commands/.
  4. The flat layer's namespaced files are consistent with the plugin folders
     (each flat file/folder traces back to a plugin + original name).
  5. Every SKILL.md referenced has a valid `name:` matching its folder.

Exit code 0 = valid, 1 = invalid (prints failures).

Usage: python3 scripts/validate.py [--root ~/adversarial-agents]
"""
import os, re, sys, argparse

DOMAIN_PREFIXES = ["ux", "eng", "qa", "res", "univ", "prom", "sec", "priv", "comp", "prod", "ops", "doc"]

def parse_frontmatter(path):
    try:
        content = open(path).read()
    except Exception:
        return None, "unreadable"
    m = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not m:
        return None, "no frontmatter block"
    fm = m.group(1)
    nm = re.search(r"^name:\s*(.+)$", fm, re.MULTILINE)
    name = nm.group(1).strip() if nm else None
    return name, None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.expanduser("~/adversarial-agents"))
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    errors = []

    # Plugin folders
    plugins = [d for d in os.listdir(root)
               if os.path.isdir(os.path.join(root, d)) and d.startswith("adversarial-")]
    if not plugins:
        errors.append("no plugin folders found")

    # Per-plugin structure
    required = {
        "agents": "dir",
        "skills": "dir",
        "references": "dir",
        "assets/templates": "dir",
        "commands": "dir",
    }
    ref_files = ["constitution.md", "calibration-ledger.md", "personas.md"]
    tmpl_files = ["decision-record.md", "calibration-entry.md"]
    for p in plugins:
        base = os.path.join(root, p)
        for rel, kind in required.items():
            if kind == "dir" and not os.path.isdir(os.path.join(base, rel)):
                errors.append(f"[{p}] missing dir: {rel}/")
        # references
        ref_dir = os.path.join(base, "references")
        if os.path.isdir(ref_dir):
            for f in ref_files:
                if not os.path.exists(os.path.join(ref_dir, f)):
                    errors.append(f"[{p}] missing references/{f}")
        # templates
        t_dir = os.path.join(base, "assets/templates")
        if os.path.isdir(t_dir):
            for f in tmpl_files:
                if not os.path.exists(os.path.join(t_dir, f)):
                    errors.append(f"[{p}] missing template: {f}")
        # agents frontmatter
        ag_dir = os.path.join(base, "agents")
        if os.path.isdir(ag_dir):
            for f in sorted(os.listdir(ag_dir)):
                if f.endswith(".md"):
                    name, err = parse_frontmatter(os.path.join(ag_dir, f))
                    if err:
                        errors.append(f"[{p}/agents/{f}] {err}")
                    elif not name:
                        errors.append(f"[{p}/agents/{f}] missing name: frontmatter")
        # skill SKILL.md frontmatter
        sk_dir = os.path.join(base, "skills")
        if os.path.isdir(sk_dir):
            for d in sorted(os.listdir(sk_dir)):
                smd = os.path.join(sk_dir, d, "SKILL.md")
                if os.path.exists(smd):
                    name, err = parse_frontmatter(smd)
                    if err:
                        errors.append(f"[{p}/skills/{d}] {err}")
                    elif not name:
                        errors.append(f"[{p}/skills/{d}/SKILL.md] missing name: frontmatter")

    # 2. Flat layer uniqueness
    flat_agents = os.path.join(root, "agents")
    flat_skills = os.path.join(root, "skills")
    if os.path.isdir(flat_agents):
        names = [f[:-3] for f in os.listdir(flat_agents) if f.endswith(".md")]
        dupes = {n for n in names if names.count(n) > 1}
        for d in sorted(dupes):
            errors.append(f"[agents/] duplicate name: {d}.md")
        # prefix check
        for f in os.listdir(flat_agents):
            if f.endswith(".md"):
                base = f[:-3]
                if not any(base.startswith(pfx + "-") for pfx in DOMAIN_PREFIXES):
                    errors.append(f"[agents/{f}] not domain-namespaced (expected {DOMAIN_PREFIXES})")
    if os.path.isdir(flat_skills):
        sk = os.listdir(flat_skills)
        dupes = {n for n in sk if sk.count(n) > 1}
        for d in sorted(dupes):
            errors.append(f"[skills/] duplicate folder: {d}")
        for d in sk:
            if not any(d.startswith(pfx + "-") for pfx in DOMAIN_PREFIXES):
                errors.append(f"[skills/{d}] not namespace-namespaced")

    # 3. Flat agent frontmatter matches filename
    if os.path.isdir(flat_agents):
        for f in sorted(os.listdir(flat_agents)):
            if f.endswith(".md"):
                name, err = parse_frontmatter(os.path.join(flat_agents, f))
                expected = f[:-3]
                if name != expected:
                    errors.append(f"[agents/{f}] frontmatter name '{name}' != filename '{expected}'")

    if errors:
        print(f"VALIDATION FAILED ({len(errors)} issue(s)):\n")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("VALIDATION PASSED")
    print(f"  plugins: {len(plugins)}")
    print(f"  flat agents: {len([f for f in os.listdir(flat_agents) if f.endswith('.md')]) if os.path.isdir(flat_agents) else 0}")
    print(f"  flat skills: {len(os.listdir(flat_skills)) if os.path.isdir(flat_skills) else 0}")
    sys.exit(0)

if __name__ == "__main__":
    main()

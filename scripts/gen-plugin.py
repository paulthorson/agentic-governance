#!/usr/bin/env python3
"""
Generate a new adversarial plugin from a spec. Creates the full plugin
structure (plugin.json, README, agent, constitution, standard, personas,
calibration-ledger, skills, commands, templates) mirroring the existing
plugins, with domain-specific content.

Usage:
  python3 scripts/gen-plugin.py <domain> <prefix> <agent-name> \
      --title "." --desc "." \
      --checks "Check1:desc|Check2:desc|." \
      --skills "skill1:desc|skill2:desc|." \
      --veto "kw1,kw2,kw3" \
      --personas "P1:desc|P2:desc|."
"""
import argparse
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"  wrote {path.relative_to(ROOT)}")

def gen(args):
    domain = args.domain
    prefix = args.prefix
    agent = args.agent_name
    folder = f"adversarial-{domain}"
    base = ROOT / folder

    # Constitutional content is law, not capability: refuse to regenerate it.
    # Constitutions are amended by a human editing the file, not regenerated from
    # a scaffold. Unconditional — no override flag.
    _con = ROOT / "constitution" / "domains" / f"{domain}.md"
    if _con.exists():
        raise SystemExit(
            f"refusing: {_con.relative_to(ROOT)} already exists. "
            "Constitutions are amended by a human editing the file, not regenerated."
        )

    checks = [c.split(":", 1) for c in args.checks.split("|")]
    skills = [s.split(":", 1) for s in args.skills.split("|")]
    personas = [p.split(":", 1) for p in args.personas.split("|")]
    veto_kw = [k.strip() for k in args.veto.split(",")]

    print(f"=== Generating {folder} ===")

    # plugin.json
    write(base / ".claude-plugin" / "plugin.json", f"""{{
  "name": "{folder}",
  "version": "0.1.0",
  "description": "{args.desc}",
  "author": {{
    "name": "agentic-governance"
  }}
}}
""")

    # README
    skill_lines = "\n".join(f"- `{s}` — {d}." for s, d in skills)
    check_lines = "\n".join(f"{i}. **{c}** — {d}." for i, (c, d) in enumerate(checks, 1))
    write(base / "README.md", f"""# Adversarial {args.title}

{args.desc}

Built from the Adversarial Agents framework, applied to {domain}.

## The agent

- **`agents/{agent}.md`** — a single adversary that reviews {domain} work.
  Holds a hard veto.

## The checks

{check_lines}

## Skills

{skill_lines}
- `adversarial-{domain}` — the worker skill (the review loop).

## References

- `constitution/domains/{domain}.md` — the {domain}-review constitution (in the governance repo, not in the plugin).
- `references/{domain}-standard.md` — the {domain} quality bar.
- `references/personas.md` — the stress personas.
- `references/calibration-ledger.md` — the verdict record.

## Commands

- `adversarial-{domain}` — the loop.
- `{domain}-review` — run a single review.

## Templates

- `assets/templates/decision-record.md`
- `assets/templates/calibration-entry.md`
""")

    # agent
    check_sections = "\n".join(
        f"### Check {i}: {c} — {d}\nLook for the ways a {domain} change can fail this check.\n\n"
        f"Raise **BLOCKER** for any {c.lower()} that causes irrecoverable harm."
        for i, (c, d) in enumerate(checks, 1)
    )
    write(base / "agents" / f"{agent}.md", f"""---
name: {agent}
description: {args.desc} Holds a hard veto that only a human can clear. Use when {domain} work needs an adversarial pass.
tools: Read, Grep, Glob, Bash
model: inherit
---

# The {args.title} Adversary

You are a devil's advocate for {domain}. You review {domain} work for the ways
it can fail, and you hold a hard veto for irrecoverable harm.

You never fix the work. You name the risk, the assumption, and the blind spot,
and you say what would have to be true for the harm to be gone.

## Before you review anything

Read, in this order:

1. `../../constitution/domains/{domain}.md`
2. `../references/{domain}-standard.md`
3. The work you were handed

If the work is incomplete, say which checks are UNVERIFIABLE and why.

## The checks

{check_sections}

## Severity

- **BLOCKER**: irrecoverable harm, or a claim that drives action with no
  support. Routes to the human gate. You hold the veto.
- **CONCERN**: real but recoverable, or a blind spot worth naming.
- **NOTE**: would fix if free.

Do not inflate. A blocker you cannot defend in one sentence is a concern.

## What you may never do

- Clear your own veto.
- Withdraw a blocker because the author explained a deadline or a constraint.
- Accept "everyone does it this way", "we'll fix it later", or "it's out of
  scope" as reasons a blocker is not a blocker.
- Invent consequences. Speculation is labeled as speculation, never as
  outcome.
- Soften language to be agreeable.

Only a human arbiter can clear what you raise. Say so every time.

## Output

```
## {args.title.upper()} ADVERSARY VERDICT

### Checks
- <finding> | Severity: BLOCKER/CONCERN/NOTE | What would clear it

### Blockers
- <one sentence of harm> | Blast radius: <what breaks> | Recoverable: yes/no
  What would clear it: <the specific change or evidence>

### Concerns
- <item> | <what would clear it>

### Notes
- <item>

### The strongest counter-case
- <the best argument for proceeding, from the work's own facts>

### Questions the work did not answer
- <anything you needed and did not get>

VETO: ACTIVE | NONE
```

When VETO is ACTIVE, end with this line verbatim:

> This veto can only be cleared by a human arbiter. No AI in this system may clear it.
""")

    # constitution — written to the governance repo at constitution/domains/<domain>.md,
    # NOT into the plugin's references/ (constitutional content is not capability content).
    rule_lines = "\n".join(
        f"**What triggers it.** The {args.title} Adversary raises a blocker when "
        f"{domain} work can cause irrecoverable harm: {d.lower()}."
        for i, (c, d) in enumerate(checks, 1)
    )
    write(ROOT / "constitution" / "domains" / f"{domain}.md", f"""# The Constitution

Four rules for reviewing {domain}. They are enforced mechanically, by checks
that produce a pass or a fail, regardless of the work under review.

Every agent in this system reads this file before acting. No agent may edit it.

---

## Rule 1: {args.title}-harm vetoes are absolute

An AI worker can never clear a {domain} veto. Only a human can.

{rule_lines}

**What the worker may do.** Revise and resubmit. Nothing else. The worker may
not argue the blocker away, downgrade it, or proceed with a note that it was
considered.

**How it clears.** A human arbiter writes a clearing entry naming themselves
and the reason.

---

## Rule 2: Genuine alternatives are mandatory

Every {domain} proposal must name what it trades away. An option that does not
name its cost is not a decision; it is an assumption wearing a decision's
clothes.

**The mechanical check.** The work carries an alternatives line: "This trades
away X to get Y." If the work cannot name what it gives up, Rule 2 fails.

---

## Rule 3: The fast path can't silently win

The easy, cheap, or quick option is legitimate. The easy option that changes
the outcome and is never stated is not.

**The mechanical check.** The work carries a `convenience_driven` field, true
or false. When true, it names what is given up and what is saved.

---

## Rule 4: Claims must name what would falsify them

A claim that cannot be wrong is not informative. Every asserted claim should
carry what would show it false.

**The mechanical check.** For each central claim, the work names what would
falsify it, or says plainly it cannot name one (which is itself a finding).

---

## Standing constraints

1. **The reviewer never grades its own work.**
2. **The record is append-only.** The verdict is committed verbatim.
3. **No invented consequences.** The Adversary names risks, not fabricated
   outcomes, and labels speculation as speculation.
4. **Uncertainty is labeled.** Estimates, guesses, and unknowns are marked.

---

## Amendment procedure

- Every human override is logged in `references/calibration-ledger.md`.
- Three overrides of one rule puts the rule on trial.
- Only a human edits `constitution/domains/{domain}.md`.
""")

    # standard
    write(base / "references" / f"{domain}-standard.md", f"""# {args.title} Standard

The quality bar for {domain} work to pass adversarial review.

## Required inputs

A piece of {domain} work must carry, or reference, each of these. A missing
input is a finding (UNVERIFIABLE for the checks it would support).

| Input | Purpose | Supports check |
|-------|---------|-----------------|
| `work` | The {domain} artifact under review | All checks |
| `alternatives` | What the work trades away | Rule 2 |
| `convenience_driven` | Whether the fast path silently won | Rule 3 |
| `falsifiability` | What would show each claim false | Rule 4 |

## Quality bar

1. **No irrecoverable harm.** No {domain} outcome that cannot be undone.
2. **Genuine alternatives.** The work names what it trades away.
3. **No silent fast path.** The easy option that changes the outcome is stated.
4. **Falsifiable.** Each central claim names what would show it false.
5. **Complete.** No required input is missing or UNVERIFIABLE without a stated
   reason.

## Severity mapping

- **BLOCKER** — irrecoverable harm, or a claim that drives action with no
  support.
- **CONCERN** — real but recoverable, or a blind spot worth naming.
- **NOTE** — would fix if free.

## Veto conditions

- {", ".join(veto_kw)}.
""")

    # personas
    persona_lines = "\n".join(
        f"## {p}\n\n{d}\n" for p, d in personas
    )
    write(base / "references" / "personas.md", f"""# Personas

The stress personas the {args.title} Adversary uses to walk {domain} work and
find blind spots. Each is a distinct way the work can fail.

{persona_lines}
""")

    # calibration ledger
    write(base / "references" / "calibration-ledger.md", f"""# Calibration Ledger

Append-only record of {domain}-review verdicts and human overrides. A
correction is a new entry referencing the old one — never an edit.

## Verdicts

| Date | Work | Verdict | Veto | Summary |
|------|------|---------|------|---------|
| _(append)_ | | | | |

## Human overrides

| Date | Rule | Override | Reason | Arbiter |
|------|------|----------|--------|---------|
| _(append)_ | | | | |

## Calibration notes

- Three overrides of one rule puts the rule on trial.
- Recurring veto hits point to systemic gaps in how {domain} work is written.
""")

    # worker skill
    skill_names = ", ".join(f"`{s}`" for s, _ in skills)
    write(base / "skills" / f"adversarial-{domain}" / "SKILL.md", f"""---
name: adversarial-{domain}
description: The worker skill for the adversarial-{domain} loop. Orchestrates a governed review: the {agent} agent reviews blind, the constitution gates, and only a human clears a veto.
---

# Adversarial {args.title} — Worker Skill

This is the orchestration loop for reviewing {domain} work. It mirrors the
adversarial-ux loop: a worker produces, the adversary reviews blind, the
constitution gates, and only a human clears a veto.

## The loop

1. **Gather.** Read the work under review plus the constitution and standard.
2. **Adversary review.** Spawn the `{agent}` agent. Give it the work, the
   constitution, and the standard. It reviews blind — it does not see the
   worker's rationale.
3. **Verdict.** The adversary returns KICK_BACK or ALLOW with findings.
4. **Gate.** If the verdict is KICK_BACK with a BLOCKER or a veto, the work
   returns to the worker to fix and resubmit. Only a human clears a veto.
5. **Record.** Append the verdict to `references/calibration-ledger.md`.

## Stateless skills

- {skill_names}.

## Rules

- The adversary never grades its own work.
- The record is append-only.
- Only a human clears a veto.
""")

    # stateless skills
    for s, d in skills:
        write(base / "skills" / s / "SKILL.md", f"""---
name: {s}
description: Stateless skill. {d} Returns findings with severity.
---

# {s.replace('-', ' ').title()}

{d} This is the shared check that any reviewer can run.

## Method

1. Read the work in full.
2. Apply the check to the work.
3. Assign severity (BLOCKER/CONCERN/NOTE) to each finding.

## Output

```
## Findings
- <finding> | Severity: BLOCKER/CONCERN/NOTE | What would clear it
```

A BLOCKER finding is a veto: only a human clears it.
""")

    # commands
    write(base / "commands" / f"adversarial-{domain}.md", f"""# Adversarial {args.title}

Run the adversarial-{domain} loop on work.

## Usage

```
/adversarial-{domain} <path-to-work>
```

## What it does

1. Reads the work.
2. Spawns the `{agent}` agent to review it blind.
3. Returns a KICK_BACK or ALLOW verdict with findings.
4. Records the verdict to the calibration ledger.

## Rules

- The adversary never grades its own work.
- Only a human clears a veto.
- The record is append-only.
""")
    write(base / "commands" / f"{domain}-review.md", f"""# {args.title} Review

Run a single {agent} review on work.

## Usage

```
/{domain}-review <path-to-work>
```

## What it does

Runs the checks on the work and returns a verdict with findings.

## Output

- **KICK_BACK** — a BLOCKER or veto was found. The work must be fixed and
  resubmitted. Only a human clears a veto.
- **ALLOW** — the work passes. It can proceed.
""")

    # templates
    write(base / "assets" / "templates" / "decision-record.md", f"""# Decision Record

Append-only record of a {domain}-review verdict. A correction is a new entry
referencing the old one — never an edit.

## Verdict

- **Date:** _(YYYY-MM-DD)_
- **Work:** _(path or name)_
- **Reviewer:** {agent}
- **Verdict:** KICK_BACK | ALLOW
- **Veto:** ACTIVE | NONE

## Findings

- _(BLOCKER/CONCERN/NOTE)_ — finding | What would clear it

## Human clearing (only if a veto was raised)

- **Cleared by:** _(human arbiter)_
- **Reason:** _(stated reason)_
- **Date:** _(YYYY-MM-DD)_
""")
    write(base / "assets" / "templates" / "calibration-entry.md", f"""# Calibration Entry

Append-only entry for the {domain}-review calibration ledger.

## Entry

- **Date:** _(YYYY-MM-DD)_
- **Work:** _(path or name)_
- **Verdict:** KICK_BACK | ALLOW
- **Veto:** ACTIVE | NONE
- **Summary:** _(one line)_

## Notes

- Three overrides of one rule puts the rule on trial.
- Recurring veto hits point to systemic gaps in how {domain} work is written.
""")

    print(f"=== Done: {folder} ===")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("domain")
    ap.add_argument("prefix")
    ap.add_argument("agent_name")
    ap.add_argument("--title", required=True)
    ap.add_argument("--desc", required=True)
    ap.add_argument("--checks", required=True)
    ap.add_argument("--skills", required=True)
    ap.add_argument("--veto", required=True)
    ap.add_argument("--personas", required=True)
    args = ap.parse_args()
    gen(args)

if __name__ == "__main__":
    main()

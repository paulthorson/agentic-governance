---
name: doc-framework-technical-writing
description: >-
  Use when writing or reviewing public framework git docs. Human-facing pages
  must read for general users. Agent markdown must be executable. Compose dual-
  audience Framework TW with enterprise craft (clarity, task-based writing,
  progressive disclosure, scannable structure, accuracy review). Writing bar
  only — not a tool grant. Keep public git vanilla; no private product laundry
  or vendor capture tool names.
---

# Framework technical writing

Write public framework documentation for two audiences. Do not mix their jobs in
one file unless the file is explicitly a bridge (short human summary at the top,
then an agent-spec section labeled as such).

This skill is vanilla. It names no private products, hardware brands, operator
identity, project-specific paths, or vendor capture tools. Capture method lives
on each installer’s product brief — not in shared framework files.

**Provenance (NOTICE-style):** Dual-audience Framework TW bar composed with
upstream technical-writer craft (clarity, task-based writing, progressive
disclosure, scannable structure, API/user-guide patterns, accuracy review).
Upstream cite (path only):
https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/08-business-product/technical-writer.md
Upstream tool-grant and model frontmatter is stripped — this file is
a writing bar only, not a tool grant. Public git stays vanilla.

## Classify the file first

Human-facing (general users, installers, visitors):

- README
- getting started / overview / install
- public site copy that describes the framework
- contributing / security / license notices meant for people
- CHANGELOG human face
- capability-report

Agent-facing (seats that execute):

- harnesses
- locks
- checklists
- CoE tables
- story / acceptance-criteria templates
- any markdown an agent is told to follow as procedure

If unsure, split the file rather than blending.

## Human-facing bar

Write as a technical writer for people who have never seen this repo.

- Open with what this is and who it is for.
- Everyday words. Define a term the first time it appears.
- Short sections. Sentence case headings.
- Show the next action a person can take.
- No private product names, hardware brands, operator identity,
  project-specific paths, or vendor capture tools.
- No internal slang, ticket numbers as the only explanation, or "as we discussed."
- No marketing-slop words (delve, unlock, elevate, seamless, robust, leverage,
  empower, journey).
- Neutral, specific, checkable. Completeness is not clarity.

Fail the human page if a new installer cannot say what the framework does, how
to install it, and where to go next.

## Agent-facing bar

Write so an agent can execute without inventing.

- Lead with the rule, then the steps, then the fail condition.
- Use stable names for seats and checks. Spell seat names in full on public
  chrome (Chief of Staff, Product Manager, User Experience, Engineer, Quality,
  Adversary).
- Requirements numbered. Acceptance criteria as checkable boxes.
- Metric: what "done" and "miss" mean. Who detects. Who may not stamp.
- Cite other framework files by path, not by chat.
- Fail-closed: name what is rejected (Do not treat a narrative pass as acceptance, skipped seat, invented source
  of truth).
- Enough detail to program the behavior. Ambiguity is a defect.
- Still vanilla: generic process only. If a scar came from private work, rewrite
  it as anonymized process before it lands.
- Capture rule in shared files: "capture the live product the way users actually
  see it, then enhance those frames." Do not name a vendor capture tool. How to
  capture lives on the product brief.

Fail the agent file if a seat could reasonably invent a path, a stamp, a date,
or a product-specific example to fill a gap.

## Craft procedure (enterprise TW)

Apply these as procedure when composing or reviewing public docs. They do not
replace the dual-audience bars or AG locks above.

### Clarity and scan

- Prefer clear language, active voice, and short sentences.
- Keep terminology consistent; define once, reuse the same word.
- Structure for scan: logical headings, one job per section, visual breaks
  between steps.
- Progressive disclosure: start with the next action; put detail after the
  reader needs it.
- Minimalist: cut filler; completeness without clarity is a miss.

### Task-based writing

- Orient human pages around tasks the reader must complete (install, contribute,
  report a security issue), not around internal org charts.
- Step-by-step where a sequence matters; name the outcome of each step.
- Include common scenarios and troubleshooting only when they are checkable and
  vanilla (no private incident narrative).

### Information types (when the surface needs them)

- Getting started / overview for humans.
- User guides: feature docs, FAQs, quick references — still dual-audience
  classified first.
- API / integration surfaces (when present): endpoint purpose, parameters,
  request/response examples, auth, errors, version notes — verify against the
  shipped surface; do not invent samples.
- Agent procedure files stay rule → steps → fail condition (see agent bar).

### Accuracy review

Before on public content:

1. Facts match the shipped repo (paths, commands, claims).
2. Examples run or match real artifacts; invented KPIs and fake satisfaction
   scores are rejected.
3. Links resolve; version and changelog human face stay aligned with git.
4. Human bar and agent bar both pass for their classified surfaces.
5. Vanilla lock holds (no product laundry, no operator PII, no vendor capture
   tool names in shared framework text).

Measured claims only. Do not invent delivery metrics, page counts, API counts,
readability scores, or satisfaction percentages to prove the work.

### Illustrative workflow (not live connectors)

The following is **illustrative workflow text only**. It is not a live
connector, not an agent bus, and not an external side-effect. Do not treat it as
authority to call tools or notify other seats.

Planning checklist (illustrative):

- Audience classified (human vs agent vs bridge)
- Content gaps named against existing public files
- Outline matches one job per section
- Review path named (who runs accuracy review)

Progress markers (illustrative shape only — fill with real, measured values when
reporting, or omit):

```text
status: documenting
audience: human | agent | bridge
surfaces: <paths under review>
accuracy_review: unpaid | paid
vanilla_lock: hold | clear
```

Do not emit invented KPI delivery blurbs. Status belongs in chat / PR with
evidence, not fabricated adoption numbers.

## Bind this skill to your environment

This skill ships generic. It does not know your product. Before your team
writes, fill these in and keep them on *your* product brief, not in the shared
framework:

- Product name and what it is
- Surfaces that exist (for example phone app, website, hardware display,
  terminal)
- How you capture a live screen as users actually see it (production URL,
  device, preview tool, or whatever you use). Do not put that method into the
  shared framework.
- Size, type, density, and other hard limits of each surface
- Where your living design standards live
- Where product-specific craft rules live (brand, motion, copy voice)
- How a build gets placed, and how the operator looks at it

Human-facing pages in the shared framework still talk to any installer. They use
everyday words and never require your private names.

Agent files in the shared framework stay generic on purpose: capture the live
product, enhance those frames, wireframe only what can ship on that surface.
They tell your agents what kind of thing to write, not the names of someone
else's apps or tools.

When your agents write your product docs, they must get specific. Use your real
product name. Cite your real screens. State your real limits and your real
capture method. Detail belongs on your brief.

Do not copy your filled brief back into the shared framework. If a process
lesson is worth sharing, rewrite it as generic process first (the kind of
surface, the kind of capture, the kind of miss) and drop your names and tools.

What good looks like after you bind it:

- A new person on your team can install the framework and then, from your brief,
  say what your product is and how live screens are captured.
- An agent can execute a mock or a ship without inventing your capture path,
  your size limits, or your design standards.
- The public framework git still reads as if it has never heard of your company
  or your tools.

## Vanilla lock

Public git is for the masses. Private product work never leaks. Process
improvements mined from private work are rewritten as generic process before
they land. Vendor capture tools are product-brief only.

## Review

Product Manager owns the human-facing layer and rejects pages that only an
insider can read. Every seat that writes to public git runs this skill on their
own files. Quality checks both bars against this skill. Adversary fails product
leakage, named vendor tools in framework law, and unreadable or unexecutable
docs.

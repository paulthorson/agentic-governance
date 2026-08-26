# Adversarial Universal

A single universal adversarial reviewer you can point at anything: a decision, a plan, a
design, a code change, a piece of research, a contract, a message before you send it. One agent,
four universal checks, a hard veto only a human can clear.

Built from paulthorson's Adversarial Agents deck, as a domain-agnostic catch-all.

## The idea

The domain-specific plugins (adversarial-ux, adversarial-engineer, adversarial-qa,
adversarial-researcher) each have three specialized adversaries. This one is the opposite: a
single **Universal Adversary** that does not need to know the domain to find the failure modes
that are the same everywhere — unstated assumptions, silent trade-offs, irreversible actions,
evidence that does not support the claim, and the fast path that quietly wins.

Use it when you want an adversarial pass over something that does not fit a specialized loop, or
as a first sweep before deciding which specialized plugin applies.

## The single agent

| Role | File | What it does |
|---|---|---|
| The Universal Adversary | `agents/universal-adversary.md` | Runs four universal checks, names the assumption and the blind spot, holds a hard veto for irrecoverable harm |

## The constitution

Four universal rules, in `references/constitution.md`, each with a mechanical check:

1. **Irrecoverable-harm vetoes are absolute.** Only a human can clear one.
2. **Genuine alternatives are mandatory.** A submitted plan must name what it trades away.
3. **The fast path can't silently win.** Convenience that changes the outcome must be named.
4. **Claims must name what would falsify them.** An un-falsifiable claim is a red flag.

## The universal skills

| Skill | Produces |
|---|---|
| `altitude-check` | What is really being decided, and the assumed answer named |
| `assumption-hunt` | The unstated assumptions the proposal rests on, each with a kill condition |
| `blind-spot-search` | The perspective nobody argued: the user, the operator, the skeptic, the future |
| `risk-scan` | The failure modes, ranked by likelihood and irrecoverability |
| `counter-case` | The strongest argument against, argued from the proposal's own facts |
| `decision-gate` | What a human must decide, and what would change the answer |

## The loop

```
Submit → Universal Review → Commit & Alert → Human Gate
```

## Commands

| Command | What it does |
|---|---|
| `/adversarial-universal <thing>` | Runs the universal adversarial review on any decision, plan, design, change, or claim |
| `/universal-review <path>` | Runs the review against an existing artifact |

## Layout

```
adversarial-universal/
├──.claude-plugin/plugin.json
├── agents/ universal-adversary
├── skills/ adversarial-universal (worker) + 6 stateless skills
├── references/ constitution.md, calibration-ledger.md, review-standard.md
├── assets/templates/ decision-record.md, calibration-entry.md
└── commands/ adversarial-universal, universal-review
```

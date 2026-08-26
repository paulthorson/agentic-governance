# Prompt Standard

The quality bar for an instruction set (AGENTS.md, system prompt, skill
SKILL.md, plugin manifest) to pass adversarial review.

## Required sections

An instruction set must carry, or reference, each of these. A missing section
is a finding (UNVERIFIABLE for the checks it would support).

| Section | Purpose | Supports check |
|---------|---------|-----------------|
| `identity` | Who the agent is, its loyalty, its arbiter | Injection, drift |
| `constitution` / `rules` | The governing rules the agent must not violate | Drift, safety |
| `safety` / `guarantees` | The non-negotiable guarantees (veto, record, secrets) | Safety overrides |
| `veto` / `human gate` | What only a human can clear, and how | Safety overrides |
| `falsifiability` | What would show each central instruction violated | Falsifiability |

## Quality bar

1. **No injected instructions.** No text that overrides safety, loyalty, or
   judgment, or treats untrusted content as authoritative.
2. **No drift.** No contradiction of the constitution or the domain standard.
3. **No safety overrides.** The human-only veto, append-only record, and
   no-secret-exfiltration guarantees are intact.
4. **Falsifiable.** Each central instruction names what would violate it.
5. **Complete.** No required section is missing or UNVERIFIABLE without a
   stated reason.

## Severity mapping

- **BLOCKER** — injection, drift, or override that weakens a safety guarantee,
  clears a veto, or exfiltrates data.
- **CONCERN** — real but recoverable, or a drift worth naming.
- **NOTE** — would fix if free.

## Veto conditions

- An injected instruction that overrides a safety guarantee.
- An instruction that clears or downgrades a veto.
- An instruction that would cause secret/credential exfiltration.
- A drift that directly contradicts a constitutional rule.

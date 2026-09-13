# Home

The **Adversarial Agents** framework is a governed review system: every piece
of work — code, design, research, a decision, a message — is put through an
adversarial review before it is allowed to proceed. A dedicated adversary
agent for the relevant domain examines the work, runs its checks, and either
**kicks it back** (with findings) or **allows it** to proceed. Only a human
can clear a hard constitutional veto.

## Why

Most review systems are advisory — a reviewer comments, and the author
decides. This one is different: the adversary agents hold **hard vetoes** for
irrecoverable harm (data loss, security holes, user harm, unsupported claims
driving decisions). The loop is mechanical and governed by a constitution,
not by style-guide taste.

## Quick start

1. **Read the framework** — start at [[Architecture]].
2. **Pick a domain** — [[Domains]] lists ux, engineer, qa, researcher, universal.
3. **Run a review** — via the [[MCP]] server (`run_review`) or by invoking the
   domain's adversary agents directly.
4. **Wire into your team** — see [[Paperclip]] for the agent-team integration.

## The core loop

```
produce → in_review → adversary agent → KICK_BACK (fix + resubmit)
                                        └→  ALLOW (proceed)
                                        └→  VETO (only a human clears)
```

## Repo layout

```
adversarial-agents/
  adversarial-<domain>/     # plugin source of truth (5 domains)
    agents/                 # adversary agent definitions
    skills/                 # stateless skills
    references/             # constitution, standard, personas, calibration-ledger
    commands/               # slash commands
    assets/templates/       # review templates
  agents/                   # flat namespaced agents (ux-critic, eng-.)
  skills/                   # flat namespaced skills (ux-altitude-check, .)
  mcp/                      # MCP server
  docs/                     # this documentation
  scripts/                  # validate.py, consolidate script
  runs/                     # verdict decision record (gitignored)
```

## See also

- [[Architecture]] · [[CoE]] · [[Domains]] · [[Governance]] · [[MCP]] · [[Paperclip]] · [[Tooling]] · [[Roadmap]]

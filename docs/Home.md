# Home

**Agentic Governance** is a bring-your-own-agent (BYOA) governance framework:
role harnesses, a directed production chain, constitutions, a calibration
ledger, an MCP server, and a setup wizard. Adversary agents review work
against domain checks and either **kick it back**, **allow** it, or raise a
hard **veto**. Only a human can clear a constitutional veto.

Claims in this file trace to the
[`capability-report.md`](capability-report.md); if you find a discrepancy,
open an issue.

## Why

Most review systems are advisory — a reviewer comments, and the author
decides. Here, adversary agents hold **hard vetoes** for irrecoverable harm
(data loss, security holes, user harm, unsupported claims driving decisions).
The loop is governed by a constitution, not by style-guide taste.

## Quick start

1. **Install the framework** — see [README Install](../README.md#install-framework)
   (repo is private; clone needs GitHub access).
2. **Read what the code actually does** — [`capability-report.md`](capability-report.md).
3. **Understand the loop** — [Architecture](Architecture.md).
4. **Pick a domain** — [Domains](Domains.md) lists the adversary plugins.
5. **Run a review** — via the [MCP](MCP.md) server (`run_review`) or by
   invoking domain adversary agents directly.
6. **Wire into your team** — see [Paperclip](Paperclip.md) for agent-team
   integration.

## The core loop

```
produce → in_review → adversary agent → KICK_BACK (fix + resubmit)
                                        └→  ALLOW (proceed)
                                        └→  VETO (only a human clears)
```

## Repo layout

```
agentic-governance/
  adversarial-<domain>/     # plugin source of truth
    agents/                 # adversary agent definitions
    skills/                 # stateless skills
    references/             # domain standard, personas, calibration-ledger
    commands/               # slash commands
    assets/templates/       # review templates
  agents/                   # flat namespaced agents (ux-critic, eng-.)
  skills/                   # flat namespaced skills (ux-altitude-check, .)
  constitution/             # shared constitution + domain vetoes
  harnesses/                # role instructions
  mcp/                      # MCP server
  docs/                     # this documentation
  scripts/                  # validate.py, consolidate script
  runs/                     # verdict decision record (gitignored)
```

## See also

- [Architecture](Architecture.md) · [CoE](CoE.md) · [Domains](Domains.md) ·
  [constitution](../constitution/constitution.md) · [MCP](MCP.md) ·
  [Paperclip](Paperclip.md) · [Tooling](Tooling.md) · [Roadmap](Roadmap.md) ·
  [capability-report](capability-report.md)

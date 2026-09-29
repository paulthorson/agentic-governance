# Engineer Domain — deep dive

**Plugin:** `adversarial-engineer/` · **Veto:** production harm, security holes, bricked config

## What it reviews

Code, architecture, config, infrastructure, and security. Any work that could
affect a running system.

## Adversary agents

| Agent | Role |
|---|---|
| `critic` | The primary reviewer — judges the work blind against the engineering standard |
| `ops-advocate` | Advocates for operational reliability; flags deployment risk |
| `reliability-reviewer` | Reviews for reliability, failure modes, and recovery |

## The checks

- **System map** — does the change fit the system's actual structure?
- **Threat model** — what could go wrong, and is it mitigated?
- **Complexity analysis** — is the change needlessly complex?
- **Option generation** — were genuine alternatives explored (constitution rule 2)?
- **Test coverage map** — is the change actually tested?
- **Ops runbook** — can an operator run/recover it?
- **Security review** — vulnerabilities, secret exposure, supply chain.

## Skills

`eng-system-map`, `eng-threat-model`, `eng-complexity-analysis`,
`eng-option-generation`, `eng-test-coverage-map`, `eng-ops-runbook`,
`eng-security-review`, `eng-altitude-check`, `eng-assumption-testing`,
`eng-adversarial-engineer` (worker).

## Constitution / veto

The engineering constitution gates on **production harm** — a change that risks
data loss, a security hole, or a bricked config is kicked back. Only a human
clears a veto.

## How to use

```
Use the governance server to run a review of this code in the engineer domain:
<your code>
```

## See also

- [[Domains]] · [[Architecture]] · [[Constitution]]

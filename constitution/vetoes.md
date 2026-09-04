# Vetoes

A **veto** is the hard stop defined by Rule 1 of the constitution: production harm is a veto, and only a human clears it. See `constitution.md`, Rule 1.

## Veto conditions by domain

| Domain | Veto keywords / conditions |
|--------|---------------------------|
| **UX** | dead end, accessibility impossible, silent divergence, data loss, money loss |
| **Engineer** | data loss, security hole, bricked config, production outage, credential leak |
| **QA** | user harm, data loss, money loss, release-blocking defect |
| **Researcher** | unsupported claim, fabricated user, causal claim from correlation, no source |
| **Universal** | irrecoverable harm, data loss, security breach, credential leak, safety |

## How a veto works

1. The adversary agent runs its checks and detects a veto condition.
2. The work is **kicked back** to the producer with the findings.
3. The producer may fix the work and resubmit — but **cannot** override the
   veto themselves.
4. Only a human (a master) can clear a veto, explicitly, after review.

## Mechanical enforcement

The MCP server exposes `check_veto(domain, text)` which deterministically
scans text for the domain's veto keywords. `run_review` also reports
`veto_triggered` and `veto_hits` in its verdict. This gives a fast, objective
first pass before the adversary agents do their deeper review.

## Why vetoes exist

The framework's whole point is that some harms are not recoverable. A leaked
credential, a bricked config, a fabricated user driving a product decision, a
dead end for a screen-reader user — these are not "fix it in review" issues.
They are stops. The veto is the mechanism that makes the stop real.

## See also

- [[Constitution]] · [[Architecture]] · [[Calibration]] · [[MCP]]

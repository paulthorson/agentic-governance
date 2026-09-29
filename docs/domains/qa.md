# QA Domain — deep dive

**Plugin:** `adversarial-qa/` · **Veto:** user harm from quality gaps

## What it reviews

Test plans, acceptance criteria, and release gates. Any work that defines or
verifies quality.

## Adversary agents

| Agent | Role |
|---|---|
| `critic` | The primary reviewer — judges the work blind against the QA standard |
| `quality-advocate` | Advocates for quality; flags gaps that could reach users |
| `edge-case-reviewer` | Hunts edge cases and failure modes |

## The checks

- **Acceptance criteria parse** — are the criteria testable and unambiguous?
- **Coverage map** — does the test plan cover the acceptance criteria?
- **Test case generation** — are the test cases real and meaningful?
- **Risk ranking** — which gaps are highest risk?
- **Edge case hunting** — what unusual inputs/conditions break it?
- **Regression map** — what could this change break?
- **Release gate** — is it safe to release?

## Skills

`qa-acceptance-criteria-parse`, `qa-coverage-map`, `qa-test-case-generation`,
`qa-risk-ranking`, `qa-edge-case-hunting`, `qa-regression-map`,
`qa-release-gate`, `qa-altitude-check`, `qa-adversarial-qa` (worker).

## Constitution / veto

The QA constitution gates on **user harm from quality gaps** — a release that
could harm users because of a quality gap is kicked back. Only a human clears a
veto.

## How to use

```
Use the governance server to run a review of this test plan in the qa domain:
<your test plan>
```

## See also

- [[Domains]] · [[Architecture]] · [[Constitution]]

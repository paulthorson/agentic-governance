# Stress Personas — Operations

The three personas the Reliability Reviewer runs every change through. They are deliberately
extreme. They are not job titles with demographics; each is a set of conditions that breaks a
different assumption engineers make.

Run the change start to finish as each persona. For every step, record what the persona sees,
what they try, and where the system fails them. A failure is a finding.

---

## 1. First deploy

**Conditions.** This change is going out for the first time, right now, to a system with real
users. There is no "we'll fix it in the next deploy" — the next deploy is weeks away. The
operator pressing the button has read the runbook, not the code.

**Breaks these assumptions:** that the deploy will be watched, that the author will be present,
that a subtle mistake will be caught by a human who understands the change.

**Ask at every step:** Does the runbook match what the deploy actually does? If the deploy
half-succeeds, does anything detect it? What is the first observable signal that this is wrong?
Can the operator tell success from silent partial failure?

---

## 2. Midnight pager

**Conditions.** 2 AM. The page is terse ("outage", "high error rate", "disk full"). The operator
is half-asleep, has not read this change, and must act on alerts and dashboards alone. Every
minute of confusion is a minute of user impact.

**Breaks these assumptions:** that the person responding knows what the change was, that
documentation is read before action, that the obvious fix is the safe one.

**Ask at every step:** What alerts fire when this breaks, and do they name the thing that
broke? Is the fastest wrong action (restart, rollback, scale-up) also safe? What does the
operator have to guess because the change did not leave a monitor or a runbook note?

---

## 3. Handoff to a stranger

**Conditions.** Six months later. The author is gone. A competent engineer who has never seen
this system must extend, debug, or operate it from the code and the docs alone. Nothing is in
their head.

**Breaks these assumptions:** that institutional memory survives, that "it works now" is
legible, that the original author will be around to explain.

**Ask at every step:** Can a stranger tell what this module is for, what it assumes, and what
it breaks if changed? Are the invariants written down? Is the config self-explanatory, or does
it require a comment the author never wrote? If this were the only file they had, could they
safely make a change?

---

## Output format

The Reliability Reviewer reports per persona:

```
### <Persona>
- Step <n>: <what happens> → <finding>
- Stalls: <list, or "none">
- Severity: BLOCKER | CONCERN | NOTE
```

A finding under First deploy that can take production down with no rollback is a BLOCKER and is
referred to the Operations Advocate.

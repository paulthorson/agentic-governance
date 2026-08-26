# Stress Perspectives — Universal Review

The four blind-spot perspectives the Universal Adversary runs every submission through. Each is
a party or frame the proposal may have silently ignored. They are deliberately adversarial:
each breaks a different assumption about who is affected and who would have to live with the
outcome.

Run the submission start to finish as each perspective. For each, record what that party or
frame would say, and whether the proposal has an answer. A silence is a finding.

---

## 1. The affected party

The person (or system) on the receiving end of the outcome. The one harmed, charged, or changed
by the decision if it goes wrong.

**Ask at every step:** Who is harmed if this is wrong, and can they recover? Is the harm
irrecoverable (data, money, accounts, reputation, safety)? Could they see the consequence
coming from where they committed? Is there a guard, an undo, a confirmation?

**Breaks the assumption:** that the author's intent defines the outcome, that "it works for me"
means it works for the affected party.

---

## 2. The operator

The person or system that must run, fix, or undo this. The one on call at 2 AM, or the next
engineer holding the code.

**Ask:** What does the operator face when this breaks? Do alerts and docs name the thing that
broke? Is the fastest wrong action (restart, rollback, override) also safe? Is the rollback
real, or does it lose state? Can a stranger operate it six months from now?

**Breaks the assumption:** that the author will be present, that the happy path is the only
path, that "it works now" is legible later.

---

## 3. The skeptic

A hostile-but-fair reviewer with domain knowledge, reading the submission to find the weak
claim. They find the single unsupported number, the correlation dressed as causation, the
"everyone does it this way" with no evidence.

**Ask:** Which claim dies on first contact with a skeptic? Is there a number with no source, a
causal claim from correlation, a general claim from one example? What would falsify the central
claim?

**Breaks the assumption:** that assertions count as evidence, that a confident sentence is a
supported one.

---

## 4. The future

Six months from now, the author is gone. A stranger must extend, debug, or live with this from
the artifacts alone.

**Ask:** What breaks in six months? Is the provenance recoverable? Are the invariants written
down? Is the decision's reasoning legible, or is the "why" only in the author's head? Does the
proposal leave a debt someone will have to pay?

**Breaks the assumption:** that institutional memory survives, that "it works now" is legible
later.

---

## Output format

The Universal Adversary reports per perspective:

```
### <Perspective>
- What this party/frame says: <.>
- The proposal's answer or silence: <.>
- Severity: BLOCKER | CONCERN | NOTE
```

A BLOCKER under the affected party that is irrecoverable is a hard veto, referred to the human
arbiter.

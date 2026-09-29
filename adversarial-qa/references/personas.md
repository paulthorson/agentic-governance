# Stress Personas — Product Use

The four personas the Edge-Case Reviewer runs every test plan through. They are deliberately
extreme. Each is a set of conditions that breaks a different assumption QA makes.

Run the plan start to finish as each persona. Record what the persona does, what the system
does, and where the plan missed a real path. A miss is a finding.

---

## 1. First-timer
Never seen the product. No mental model, no prior state. Arrived from a deep link.

**Ask:** Does the plan cover the first load with nothing saved? The external-link entry? Labels
a stranger would not understand? Does the plan assume prior state that does not exist yet?

## 2. Hurried
Thirty seconds, one thumb, scanning. Will tap the biggest thing that looks close. Will abandon
at the second unexpected screen.

**Ask:** Does the plan cover the fastest wrong path? An irreversible action in under three
taps? Returning tomorrow to a state the user does not remember?

## 3. Screen reader
Non-visual. Tab order and announcements are the interface. Dynamic content that does not
announce itself does not exist.

**Ask:** Does the plan verify what is announced on arrival, tab order matching reading order,
named icon-only controls, and content changes that announce themselves? Is a screen reader
stall that prevents completion a blocker in the plan?

## 4. Distracted
Interrupted mid-flow, repeatedly. Two tabs of the same flow. Cannot remember what they entered.

**Ask:** Does the plan cover what survives a background and return, what a timeout destroys,
what double-entry does, and whether previous decisions are visible or only remembered?

---

## Output format

```
### <Persona>
- Path: <what the persona does> → <what the plan covers / misses>
- Severity: BLOCKER | CONCERN | NOTE
```

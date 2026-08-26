# Stress Personas

The four personas the Evaluative UXR agent runs every flow through. They are deliberately
extreme. They are not marketing personas and they carry no demographics, no names, and no
backstory. Each one is a set of conditions that breaks a different assumption designers make.

Run the flow start to finish as each persona. For every step, record what the persona sees,
what they try, and where they stall. A stall is a finding.

---

## 1. First-timer

**Conditions.** Has never seen this product. No mental model of the vocabulary. Does not know
what is possible, so does not know what to look for. Arrived from an external link, not the
home screen.

**Breaks these assumptions:** that labels are self-explanatory, that the user knows where they
are in a process, that prior state exists, that empty states are rare.

**Ask at every step:** Can this person tell what this screen is for without reading help text?
Does any label use an internal term? What happens on the very first load, with nothing saved?

---

## 2. Hurried

**Conditions.** Thirty seconds of attention. One thumb. Scanning, not reading. Will tap the
biggest thing that looks close to what they want. Will abandon at the second unexpected screen.

**Breaks these assumptions:** that users read confirmation copy, that a multi-step flow will be
finished in one sitting, that a warning prevents an action.

**Ask at every step:** What does the fastest wrong path look like, and how bad is it? Can this
person cause an irreversible action in under three taps? If they leave here and come back
tomorrow, what state do they return to?

---

## 3. Screen reader

**Conditions.** Non-visual. Navigating by headings, landmarks, and form controls. Tab order and
announcements are the entire interface. Dynamic content that does not announce itself does not
exist.

**Breaks these assumptions:** that layout communicates grouping, that color communicates state,
that a modal is obviously a modal, that an inline error is noticed.

**Ask at every step:** What is announced on arrival? Is the tab order the same as the reading
order? When content changes without a page load, what tells this person? Is every icon-only
control named?

---

## 4. Distracted

**Conditions.** Interrupted mid-flow, repeatedly. Switches apps, takes a call, comes back four
minutes later. May have two tabs of the same flow open. Cannot remember what they already
entered.

**Breaks these assumptions:** that sessions are continuous, that a form holds its values, that
timeouts are harmless, that the user remembers what they selected two screens ago.

**Ask at every step:** What survives a background and return? What does a session timeout
destroy? If this step is entered twice, does anything double? Is the previous decision visible
here, or only remembered?

---

## Output format

The Evaluative UXR agent reports per persona:

```
### <Persona>
- Step <n>: <what happens> → <finding>
- Stall points: <list, or "none">
- Severity: BLOCKER | CONCERN | NOTE
```

A finding under Screen reader that prevents task completion is a BLOCKER, not a CONCERN.
A finding under Hurried that reaches an irreversible action is referred to the CX-Quality
Advocate.

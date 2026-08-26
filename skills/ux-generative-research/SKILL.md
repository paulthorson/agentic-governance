---
name: ux-generative-research
description: Design an unrun generative research study (objectives, recruiting screener, discussion guide, analysis plan) for a design question that desk research could not answer. Use in the adversarial-ux Discover phase when a gap needs real participants, and whenever someone asks for an interview guide, a discovery study plan, or a diary study design. Produces a study instrument only. It never produces findings, because it never ran.
---

# Generative Research

A pure function. Question in, study instrument out. This skill designs a study. It does not run
one and it never returns results.

## Method

1. **State the decision the study serves.** If nothing changes based on the outcome, say that,
   and stop. A study that cannot change a decision is not worth someone's hour.
2. **Pick the method** and say why the others were rejected:
   - Interviews: understanding reasoning, history, workarounds
   - Contextual inquiry: how the work actually happens, in place
   - Diary study: behavior over time, memory-unreliable moments
   - Concept exploration: reactions to a direction, not a design
3. **Write the screener.** Behavior-based criteria, not attitude-based. Include the
   disqualifiers.
4. **Write the guide.** Open, non-leading, ordered from broad to specific.
5. **Write the analysis plan** before running anything: what gets coded, how themes get built,
   what would count as a strong signal at this sample size.

## Output

```markdown
# Study Plan: <title>

## Decision this serves
<what changes depending on the outcome>

## Objectives
1. <objective, phrased as a question the study can answer>

## Method
<chosen method>, chosen over <alternatives> because <reason>
Sample: <n> participants. <Why this n is enough for this decision, and what it cannot tell us>

## Screener
- Qualify if: <observable past behavior>
- Disqualify if: <criteria>
- Quotas: <segments, if any>

## Discussion guide
### Warm-up
1. <question>
### Core
2. <question>
   - Probe: <follow-up>
### Wrap
9. <question>

## Analysis plan
- Coding scheme: <what gets tagged>
- Theme threshold: <what counts as a theme at this n>
- What would surprise us: <stated in advance>

## Limits
- <what this design cannot tell you>
- <known bias in the sample or the method>
```

## Rules

- Never write leading questions. "What frustrates you about X" presumes frustration.
- Never ask participants to predict their future behavior. Ask what they did last time.
- Never produce findings, quotes, personas, or numbers. Nobody has been interviewed.
- State the sample's limits in the plan, not after someone over-reads the results.

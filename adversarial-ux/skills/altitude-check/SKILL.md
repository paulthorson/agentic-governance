---
name: altitude-check
description: Re-state a solution-shaped design request at problem altitude. Names the solution that was smuggled into the request, the problem it assumes, and who is assumed to have it. Use as the first step of the adversarial-ux Discover phase, or any time a request names an answer ("add a modal", "build a dashboard", "make onboarding better") instead of a problem. Produces an artifact, never an opinion about what to build.
---

# Altitude Check

A pure function. Request in, altitude analysis out. No recommendation, no preferred direction,
no design.

## Method

1. **Quote the request verbatim.** Do not clean it up.
2. **Name the solution inside it.** Most requests arrive with the answer attached. Say what
   artifact the requester already has in mind.
3. **Name the problem that solution would solve.** State it as a sentence about a person, not a
   feature: "Someone cannot X because Y."
4. **Climb one level.** What is the problem behind that problem? Stop climbing when you reach a
   business outcome or a human need that no longer implies an interface.
5. **Descend one level.** What smaller, more specific problem might actually be the whole thing?
6. **Name the assumed user.** Who is this for, according to the request? How would we know that
   is the right population?
7. **Name what would have to be true** for the requested solution to be correct.
8. **Name what is unknown.** Explicitly. Do not fill gaps with plausible detail.

## Output

```markdown
# Altitude Check: <short title>

## The request, verbatim
> <quote>

## Solution already assumed
<what interface or feature the request presumes>

## Problem it implies
<one sentence about a person>

## One level up
<the wider problem, and what it would mean to solve it instead>

## One level down
<the narrower problem, and what it would mean if this is all there is>

## Assumed user
<who>. Confidence: <stated by requester | inferred | unknown>

## For the requested solution to be right, all of this must hold
1. <assumption>
2. <assumption>

## Unknown
- <what nobody in this conversation knows yet>

## Recommended altitude for this run
<up | as-stated | down>, because <reason>
```

## Rules

- Never propose the design. That is not this skill.
- Never invent a user population, a metric, or a pain point that nobody mentioned.
- "The requester did not say" is a valid and expected answer. Use it instead of guessing.
- Keep the requester's own words for the problem where they used any. Do not upgrade their
  phrasing into product vocabulary.

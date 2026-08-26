---
name: ux-assumption-testing
description: Surface the assumptions a design or brief rests on, rank them by how much damage a wrong one does, and name the cheapest test that would kill each. Use in the adversarial-ux loop before committing to a direction, before Gate 1 or Gate 2, and whenever someone asks what could be wrong with a plan or what to validate first. Produces a ranked assumption register with kill criteria, never a verdict on the design.
---

# Assumption Testing

A pure function. Design or brief in, ranked assumption register out.

## What counts as an assumption

Anything that must be true for the plan to work, that nobody has verified. Look in four places:

- **Desirability.** People want this, enough to change what they do now.
- **Viability.** It moves a business metric enough to be worth the build.
- **Feasibility.** It can be built with what exists, in the time available.
- **Usability.** People can figure it out without help.

Then look in the place people forget: **the assumptions inside the evidence**. That the research
population matches the launch population. That the metric measures what its name says. That last
year's behavior still holds.

## Method

1. Extract every assumption. Aim wide first, prune later.
2. For each, score two things:
   - **Impact if wrong**: high, medium, low. High means the plan does not work at all.
   - **Evidence today**: strong, weak, none.
3. Rank by impact-if-wrong first, then by weakness of evidence. High impact plus no evidence
   goes to the top and stays there.
4. For each of the top assumptions, write the **kill criterion**: the specific result that would
   prove it false. Not "we would learn more". A result.
5. Name the cheapest test that could produce that result, and what it costs in days.

## Output

```markdown
# Assumption Register: <subject>

## Ranked
| # | Assumption | Type | Impact if wrong | Evidence today | Kill criterion | Cheapest test | Cost |
|---|---|---|---|---|---|---|---|
| 1 | <statement> | desirability | high | none | <result that disproves it> | <test> | <days> |

## Top three, expanded
### A1: <assumption>
- **Why it matters.** <what breaks if this is false>
- **What we have.** <current evidence, or "nothing">
- **Kill criterion.** <specific observable result>
- **Test.** <method, sample, duration>
- **If it dies.** <what the team does instead>

## Assumptions inside the evidence
- <assumption about the data itself>

## Assumptions we are choosing not to test
- <assumption>, because <reason>. Accepted risk: <what happens if wrong>
```

## Rules

- A kill criterion that no realistic result could satisfy is not a kill criterion. Rewrite it.
- Never rank by how easy something is to test. Easy tests of low-impact assumptions are how
  teams stay busy while the risky assumption sits untouched.
- The untested-and-accepted list is required. An assumption nobody will test is a decision, and
  decisions get recorded.
- Do not judge the design. Rank the risk and stop.

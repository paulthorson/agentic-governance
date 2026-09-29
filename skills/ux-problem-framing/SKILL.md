---
name: ux-problem-framing
description: Turn a design question into three genuinely distinct problem framings, each with its own user, its own success measure, and its own implied direction. Use in the adversarial-ux Discover phase after altitude-check and desk-research, and whenever a team needs to agree on what problem they are solving before anyone designs. Produces three framings and a comparison, never a pick.
---

# Problem Framing

A pure function. Evidence in, three framings out. You do not choose. Choosing is the human's job
at Gate 1.

## What makes framings distinct

Three framings are distinct when they disagree about at least two of these:

- Who has the problem
- When the problem happens in the person's day or journey
- What the person is actually trying to accomplish
- What would count as it being solved
- What would have to change to solve it

Three framings that share a user, a moment, and a success measure are one framing written three
ways. That fails, and the Critic will say so.

## Method

1. Read the altitude check and the desk research. Use their unknowns, do not paper over them.
2. Write framing A from the most obvious reading of the evidence.
3. Write framing B by changing who has the problem.
4. Write framing C by changing when the problem occurs, or by taking seriously a piece of
   evidence that framings A and B both explain away.
5. For each framing, write the sentence that would falsify it.
6. Compare them on what each one would cost to be wrong about.

## Output

```markdown
# Problem Framings: <topic>

## Framing A: <short name>
- **Statement.** <Person> cannot <do thing> because <reason>, which matters because <stake>.
- **Who.** <population, and how we would identify them>
- **When.** <moment in the journey>
- **Solved looks like.** <observable change, with the metric that would move>
- **This framing is wrong if.** <falsifier>
- **Evidence for.** <cite desk research findings>
- **Evidence against.** <cite, or "none found">
- **Implied direction.** <what kind of work this would lead to, one line>

## Framing B: <short name>
<same structure>

## Framing C: <short name>
<same structure>

## How they differ
| | A | B | C |
|---|---|---|---|
| Who | | | |
| When | | | |
| Success measure | | | |
| Cost of being wrong | | | |

## What all three assume
- <shared assumption that nobody has tested>

## Open questions for Gate 1
- <the question the human has to answer to pick>
```

## Rules

- No framing is the strawman. If one is obviously weakest, rewrite it until it is defensible.
- Do not rank. Do not recommend. Do not say which one you find most likely.
- Every framing names a metric that would move. "Users would be happier" is not a metric.
- The shared-assumption section is not optional. Three framings that all rest on one untested
  belief is the finding.

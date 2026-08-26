---
name: desk-research
description: Gather what is already known about a design problem from sources that already exist (prior research, analytics, support themes, connected tools, the product itself, public documentation) and mark the gaps that remain. Use in the adversarial-ux Discover phase before any framing or design work, and any time someone asks what is already known about a UX problem. Produces a sourced evidence file with unknowns named, never a conclusion about what to build.
---

# Desk Research

A pure function. Question in, sourced evidence out, gaps labeled. No recommendation.

## Method

1. **Write the questions first.** Three to six specific questions the research must answer. A
   question you cannot imagine an answer to is too vague.
2. **Inventory reachable sources** before reading any of them:
   - Files and folders the user has connected
   - Connected tools: research repositories, analytics, ticketing, chat, document stores
   - The product's own documentation, code, or content
   - Public sources: standards, platform guidelines, published research
3. **Read and extract.** For each finding, capture the claim, the source, the date, and the
   population it describes.
4. **Separate evidence from inference.** Anything you concluded rather than read gets marked.
5. **Mark the gaps.** For each question with no answer, say so and name what source would
   answer it.

## Output

```markdown
# Desk Research: <topic>

## Questions
1. <question>

## Findings
### <Question 1>
- **Finding.** <claim>
  - Source: <file, tool, URL, or "internal knowledge, unverified">
  - Date: <when the source is from, or "unknown">
  - Population: <who this describes, or "unclear">
  - Confidence: <direct evidence | indirect | inference>

## Gaps
| Question | Status | What would answer it |
|---|---|---|
| <q> | unanswered | <source or study> |

## Conflicts
- <where two sources disagree, both quoted, no resolution attempted>

## Sources consulted
- <list, including sources that turned up nothing>
```

## Rules

- Every number carries its source and its date. A number with neither does not go in the file.
- Never write "research shows", "studies suggest", or "best practice says". Name the source or
  cut the claim.
- A stale source stays in with its date visible and a note that it may no longer hold.
- Sources that turned up nothing are listed. A silent gap looks like a search nobody ran.
- Do not resolve conflicting evidence. Present both and let the framing step deal with it.

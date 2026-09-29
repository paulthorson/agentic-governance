---
name: research-synthesis
description: Turn supplied raw research input (interview notes, transcripts, survey responses, support tickets, session recordings) into evidence-linked themes with frequency, severity, and contradictions preserved. Use in the adversarial-ux Discover phase when raw material exists, and whenever someone hands over a pile of user feedback and asks what it says. Produces themes traceable to specific quotes, never conclusions beyond the supplied data.
---

# Research Synthesis

A pure function. Raw input in, themes out, every theme traceable to specific evidence. If no raw
input was supplied, this skill does not run. Say so rather than synthesizing from memory.

## Method

1. **Inventory the corpus.** Count the sources, name what each is, note the date and the
   population. State the sample's shape before reading it.
2. **Extract observations.** One per line, each carrying its source ID and a verbatim quote or a
   close paraphrase marked as such.
3. **Cluster bottom-up.** Group by what the person was trying to do or what stopped them, not by
   the feature they mentioned. Feature-shaped clusters reproduce the org chart, not the problem.
4. **Name each theme** in the participants' language where possible.
5. **Count.** How many distinct sources support each theme. Report the count and the denominator.
6. **Keep the contradictions.** Evidence that cuts against a theme stays attached to it.
7. **Mark the singletons.** A one-source observation can be the most important thing in the pile
   and it is still a one-source observation. Label it.

## Output

```markdown
# Synthesis: <study or corpus name>

## Corpus
- <n> sources: <what they are>
- Collected: <dates>
- Population: <who, and who is missing>
- Known bias: <recruiting, self-selection, survivorship>

## Themes
### T1: <theme in participants' words>
- Support: <n> of <total> sources
- Severity: <blocking | painful | annoying>, basis: <what in the data indicates this>
- Evidence:
  - [S3] "<quote>"
  - [S7] "<quote>"
- Counter-evidence:
  - [S2] "<quote that does not fit>"
- Interpretation: <yours, marked as interpretation>

## Singletons worth keeping
- [S5] "<quote>". Why it may matter: <reason>

## Contradictions unresolved
- <where the data disagrees with itself>

## What this corpus cannot tell you
- <questions outside its reach>
```

## Rules

- Every theme cites sources by ID. A theme with no citation gets deleted, not softened.
- Never generate a quote. Never adjust a quote to read better. Mark paraphrase as paraphrase.
- Report counts as "n of total", never as percentages, unless the sample is a survey large
  enough for a percentage to mean anything. Say which.
- Interpretation is labeled as interpretation, in its own line, never blended into the evidence.
- Do not turn themes into recommendations. That happens later, under review.

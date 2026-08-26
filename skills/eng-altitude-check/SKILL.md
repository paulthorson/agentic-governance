---
name: eng-altitude-check
description: Re-state the engineering request at problem altitude, naming the assumed solution so it can be examined rather than taken at face value.
argument-hint: "<the request>"
---

# Altitude Check

Produce a pure artifact. Input in, artifact out. No opinion about whether the request is good.

## Output

```
## REQUEST AT PROBLEM ALTITUDE

### What the user asked for (verbatim)
> <quote>

### The assumed solution (named)
- The request implies: <the solution shape it presumes>

### The problem it is really trying to solve
- <one sentence, at problem level, not solution level>

### Why the shape may be wrong
- <assumption the shape makes that may not hold, or "none obvious">

### Lanes this could belong in
- Lane 1 (Discover & Define): <why or why not>
- Lane 2 (Develop & Deliver): <why or why not>
```

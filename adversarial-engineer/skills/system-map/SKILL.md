---
name: system-map
description: Map the components, data flows, and failure boundaries that an engineering change touches, so the blast radius is explicit before any design.
argument-hint: "<the change and the system it touches>"
---

# System Map

Produce a structural map. Input in, artifact out. No verdict.

## Output

1. **Components involved**: each subsystem the change touches.
2. **Data flows** — what reads, writes, or destroys data, and whether it is recoverable.
3. **Failure boundaries**: what breaks if each component fails, and what that takes down.
4. **External effects**: anything that leaves the system (money, accounts, email, network), and
   whether it is reversible.
5. **Config / scheduler touchpoints**: any config path, cron, or scheduler the change touches,
   and its blast radius.
6. **Unknowns**: boundaries you cannot see, named as such.

```
## SYSTEM MAP

| Component | Reads | Writes | Destroys (recoverable?) | If it fails, what breaks |
|---|---|---|---|---|

### Data flows
- <what flows where, and reversibility>

### Failure boundaries
- <component -> blast radius>

### Config / scheduler touchpoints
- <path | blast radius | validate-before-apply?>

### Unknowns
- <what you could not determine>
```

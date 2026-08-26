---
name: threat-model
description: Enumerate attack surfaces and abuse cases for an engineering change, unranked and without a verdict, so security is examined rather than assumed.
argument-hint: "<the change>"
---

# Threat Model

Produce a threat surface inventory. Input in, artifact out. No verdict on severity.

## Output

1. **Attack surfaces** — every boundary where untrusted input or control enters.
2. **Abuse cases** — what a hostile or careless actor could do at each surface.
3. **Secret exposure paths** — everywhere credentials, keys, or user data could leak (code,
   config, logs, git history, backups).
4. **Destructive paths** — every operation that deletes, overwrites, resets, kills, or shuts
   down, and whether it has a guard.
5. **What was not checked** — surfaces you could not inspect, named as such.

```
## THREAT MODEL

| Surface | Entry point | Abuse case | Exposure | Guard present? |
|---|---|---|---|---|

### Secret exposure paths
- <where secrets could leak, or "none identified">

### Destructive operations
- <operation | guard | what it destroys>

### Not examined
- <what you could not inspect, and why>
```

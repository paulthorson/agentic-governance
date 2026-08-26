# ADR-0002: Domain-Namespaced Flat Layer

- **Status:** Accepted
- **Date:** 2026-08-26

## Context

Each adversarial plugin has a `critic` agent and an `altitude-check` skill.
When consolidating into a flat `agents/` + `skills/` layer for Cursor and
Claude, these names collide — every plugin would register as `critic`.

## Decision

Namespace the flat layer by domain: `ux-critic`, `eng-critic`, `qa-critic`,
etc. Rewrite each agent's and skill's frontmatter `name:` to the namespaced
name so Cursor/Claude register them as distinct. The plugin folders remain
the source of truth; the flat layer is a generated consumption layer.

## Consequences

- **Positive:** No collisions. Agents/skills are unambiguous across domains.
- **Negative:** The flat layer is a copy, not a symlink — edits must flow
  through the consolidate script.

## Alternatives considered

- **Symlink the flat layer to plugin folders** — rejected: namespaced
  filenames wouldn't match plugin filenames.

## References

- `scripts/consolidate-adversarial.py`
- `docs/Domains.md`

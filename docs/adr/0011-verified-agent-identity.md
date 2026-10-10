# ADR-0011: Verified Agent Identity

- **Status:** Proposed
- **Date:** 2026-10-10
- **Builds on:** ADR-0010

## Context

ADR-0010 enforced reviewer independence by comparing `agent_id` strings. Those
strings were self-reported. An agent could claim work as `eng-1`, then claim
the review as `eng-critic`, and pass its own work. It could also name any
team or stage it liked. Capability report §12.13 said so.

For teams to run without a human checking who did what, the framework has to
decide who an agent is.

## Decision

**Operator-managed registry** at `config/agents.json` (gitignored, written
0600). Each entry binds an `agent_id` to a team, a list of roles, and a
principal:

- `engineer` lets the agent claim work at the engineer stage.
- `review:engineer` lets it claim reviews at that stage.
- `principal` names who runs the agent: a runtime, a process, a vendor
  account. The operator chooses the granularity.

`ticket.py agent add` issues a 256-bit random token, prints it once, and
stores only its SHA-256. `agent revoke` retires it. Both require operator
approval.

**Enforcement switch.** If the registry holds at least one active agent,
identity is required for claim, heartbeat, submit, and verdict. The token
(from `--token`, `AG_AGENT_TOKEN`, or MCP `agent_token`) decides the agent
id. A claimed id that differs from the token's is refused. Team and stages
come from the registry, so an agent cannot widen its own scope. Without a
registry, ids stay self-reported, and every event says so
(`agent_verified: false`).

**Principal separation.** A reviewer whose principal matches the worker's
cannot claim or judge the review. One runtime holding two tokens still
cannot review its own work, as long as the operator registers both under
the same principal.

**Fail closed.** An unreadable registry refuses agent actions. It never
falls back to self-reported ids.

**Ticket creation.**

- MCP `ticket_create` requires a token once identity is enforced, and the
  token's team must match.
- The CLI lets an operator create queued tickets without a token.
- Creating a ticket straight into review (`ticket.py new` without
  `--queue`) has two forms:
  - With a token, it records that agent and principal as the worker, so
    the same principal cannot review it.
  - Without a token, it needs operator approval.

  Otherwise unattributed work could reach review and be passed by any
  reviewer.

**Switching identity off is visible.** The head record (ADR-0012) stores
whether identity was enforced. If the registry later goes missing or empty
(deleted, or `AG_AGENT_REGISTRY` pointed elsewhere), writes stop as
tampering until an operator accepts it.

## Consequences

- **Positive:** self-review, cross-team claims, and stage hopping are
  refused for registered agents through the CLI, `chain.Store`, and the MCP
  `ticket_*` tools. These are tested per path in
  `tests/test_identity_integrity.py`.
- **Positive:** events and verdict records carry `agent_verified`, so
  dashboards can separate verified work from self-reported work.
- **Negative:** identity is only as strong as token secrecy. Two agents
  running as the same OS user with tokens in readable env vars or files can
  read each other's tokens. `docs/deployment-hardened.md` covers separation.
- **Negative:** principal separation depends on the operator registering
  principals honestly. Two tokens for one runtime under different
  principals defeat it.
- **Negative:** no token expiry. Rotation is revoke plus add.

## Alternatives considered

- **mTLS / OIDC per agent:** stronger, but needs infrastructure the
  framework cannot assume in a bring-your-own-agent install. A future
  adapter can map those identities onto registry entries.
- **HMAC-signed requests:** the token would never cross the wire, but every
  agent host would need signing code. Bearer tokens work with any MCP
  client today.
- **Infer principal from process info:** not portable and spoofable.

## References

- [[ADR-0010]] · [[ADR-0012]] · `scripts/identity.py` ·
  `tests/test_identity_integrity.py::IdentityTest` · capability report §12.14

# Personas

The stress personas the Security Adversary uses to walk a change and find
blind spots. Each is a distinct way a change can be exploited or can fail.

## The Attacker

Reads the change looking for a way in. Asks: what input, if crafted, would
reach a dangerous code path? What is trusted that should not be? What is the
cheapest path from untrusted input to compromise?

## The Operator

Must run, maintain, and debug the system. Asks: can I tell what is exposed?
Can I rotate a leaked secret? Can I undo a bad deployment? Is the dependency
tree reproducible and auditable?

## The Skeptic

Reads the change as a hostile reviewer. Asks: which security claim dies on
first contact with a contradiction? Which "it's internal only" assumption is
false? Which dependency is trusted without evidence?

## The Regulator

Must answer for the change under audit. Asks: is sensitive data protected as
required? Is retention bounded? Is there a record of what was decided and why?
Can I show this change is compliant?

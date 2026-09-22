# Disposable acceptance environments

**Status:** Recommended practice (optional per project)  
**Not required** for every release. Projects adopt it when they want stronger, repeatable acceptance evidence.

## Purpose

Run acceptance tests against a fresh, isolated copy of the service — not against a developer’s hand-tuned machine or a shared staging environment that has drifted.

## Method

1. **Provision** a short-lived local environment with the service under test and only the dependencies that run needs (containers are a common implementation; the project chooses its tooling).
2. **Execute** the acceptance suite against that environment alone.
3. **Destroy** everything the run created, including when tests fail (use a reliable cleanup path such as `trap` / try-finally, not a bare command chain that skips cleanup on failure).

## Requirements when adopted

- Seed data must be **synthetic, sanitized, and version-controlled**. Never use production data.
- The person who built the change must **not** be the sole verifier on a machine they personally tuned for a passing run. Verification belongs in an environment they did not customize for a lucky green.
- If the project uses recorded responses for external services, **stale or missing recordings must fail the run clearly**. Recorded stubs are optional; when used, they must be trustworthy.

## Out of scope

This practice does **not** require:

- A fixed multi-command platform or named command contract
- Production-identical databases in every case
- A second contract-testing layer as policy
- An organization-wide schedule for re-recording external stubs
- A mandatory release gate for every project

## Implementation notes

Watch for caches that break isolation, incorrect migrate-then-seed ordering, async or streaming paths left outside the sealed environment, and cleanup that leaves residue or turns into a long-lived local stack. Capture those choices in the project’s own adoption note rather than expanding this page into a platform.

## History

An earlier, broader platform-shaped draft existed in this repository. The current guidance is the short recommended practice above. Older platform rules are not in force.

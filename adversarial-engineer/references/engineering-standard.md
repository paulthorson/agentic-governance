# Engineering Standard

The baseline the Engineering Critic checks against. This file ships with placeholders. Replace
them with the real stack, language, and operational contracts before the Critic's compliance
checks mean anything.

Until this file is filled in, the Critic reports the affected checks as **UNVERIFIABLE** rather
than passing them.

---

## How to point this at a real baseline

Set the fields below. Delete the entries that do not apply to the current repo.

```yaml
stack: UNSET # e.g. node 22 / typescript, python 3.12, go 1.22
package_manager: UNSET # e.g. npm, pnpm, uv, go modules
test_command: UNSET # e.g. pnpm test
lint_command: UNSET # e.g. pnpm lint
typecheck_command: UNSET # e.g. pnpm typecheck
build_command: UNSET # e.g. pnpm build
ci_provider: UNSET # e.g. github-actions
config_validate_command: UNSET # e.g. "openclaw config validate" for gateway config
last_verified: UNSET
```

## The four checks the Critic runs

### Check 1: Correctness & contracts

- Every function, endpoint, and module declares its contract: inputs, outputs, error behavior,
  side effects.
- Error paths are handled or explicitly deferred; no swallowed exceptions, no empty `catch {}`.
- State transitions are complete: every state has an exit, every async path has a failure path.
- No placeholder implementations ("TODO: implement", `return null`) left in a submitted change.
- If types exist in the stack, the change is typechecked with no `any`-bypass without a comment.

### Check 2: Security and secrets

Against `references/security-baseline.md` if present, else the defaults below:

- No credentials, tokens, keys, or secrets in code, config, logs, or git history. A SecretRef or
  env-var reference is the only acceptable form.
- Inputs are validated at the boundary; no unsanitized input reaches a shell, SQL, template, or
  file path.
- No destructive operation (delete, overwrite, drop, reset, kill, shutdown) without a guard:
  a flag, a confirmation, a backup, or an explicit non-interactive guard.
- External effects (money, accounts, emails, network calls) have a correctable confirmation.
- Any command that touches configuration, schedulers, or infrastructure names its blast radius.

### Check 3: Maintainability and testability

- New logic is covered by a test, or the gap is named with a reason in the record.
- Functions do one thing; no God objects, no 400-line functions introduced.
- Dependencies are pinned or locked; no new unpinned transitive dependency without a note.
- Error messages say what happened and what to do next.

### Check 4: Operations and reversibility

- Every change names its deploy path, rollback path, and observability (what to watch).
- Any irreversible action is named as such and routed to a human gate (Rule 1).
- Config and infrastructure changes are version-controlled and validate before apply.
- No change that can take the system down ships without a rollback and a monitor.

## Standards to fill in (delete what does not apply)

- `references/security.md` — the security baseline the Critic checks Check 2 against.
- `references/config.md` — the config paths that are protected and how changes are validated.

## If a check is UNVERIFIABLE

The Critic reports the check as UNVERIFIABLE and says why (no test command, no security
baseline, no config path). It never reports an unverifiable check as a pass.

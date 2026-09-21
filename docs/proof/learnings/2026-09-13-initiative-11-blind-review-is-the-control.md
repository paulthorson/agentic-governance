# Learning — the blind review is the control, not the ceremony

Date: 2026-09-13. Source: Initiative 11 governed extension platform build.

The security review of the extension sandbox returned KICK_BACK with five
blockers, and every one of them was a *working bypass demonstrated live* —
not a style note, not a hypothetical. Three of the five were exploitable
through pure documented-API usage with no introspection tricks at all:
traversing `ctx._host` to self-mint confirmation tokens (a human-gate bypass),
mutating context-owned scope sets shared with the enforcement checks (scope
escalation), and downgrading action metadata from `confirm-required` to `read`.

The builder believed the invariant "extension code only ever receives `ctx`"
was the whole security story. The review showed the invariant was necessary
but not sufficient: what matters is whether *mutable state is shared between
the subject and the enforcement check*. The fix was architectural, not a
patch list: a token-dispatch broker in a module with safe globals (no
plain-attribute path from context to host — verified programmatically),
deep-frozen manifests with enforcement reading the frozen copy, and a widened
import ban where bare `open()` is a hard verification violation.

Two corollaries worth keeping:

1. **State the invariant, then attack the invariant.** "The context is the only
   thing extensions receive" sounded complete. The review asked the next
   question — "what can the context *reach*, and what does it *share*?" — and
   found five answers. Every capability story should be reviewed against its
   own stated invariant, adversarially, before the verdict.
2. **Disclose the residual honestly and name the compensating control.**
   In-process sandboxing cannot close dunder introspection; the design closes
   every plain-attribute path, says so in the threat model, and names the
   real controls (registry human review reads the code — the AST scan is a
   tripwire, the review is the control — plus signatures and audit).
   Disclosure without a compensating control leaves the residual uncovered;
   with one, it is an architecture.

Compounding note: this is the same depth-2 pattern as earlier builds —
coordinator-executed reviews with framework adversary prompts applied to the
work product alone keep finding real defects. The isolation caveat belongs in
every recorded verdict summary, and a genuinely independent re-review belongs
on the program coordinator's list before any verdict is treated as fully
cleared.

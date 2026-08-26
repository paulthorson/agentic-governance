# Review Standard

The baseline the Universal Adversary uses for its four checks. Ships with placeholders. Most
universal checks run without a baseline; the domain-specific ones become UNVERIFIABLE until
filled.

```yaml
domain: UNSET # e.g. ux, engineering, qa, research, product, contract
standards_ref: UNSET # path to a domain standard, if the review is domain-specific
known_risk_register: UNSET # path to a risk register to check against
last_verified: UNSET
```

## The four checks

### Check 1: Altitude
What is really being decided, distinct from what is being assumed. The assumed answer is named.

### Check 2: Alternatives
The proposal names what it trades away (Rule 2), and the alternative is genuine, not cosmetic.

### Check 3: Harm and reversibility
Irrecoverable harm, security exposure, and irreversible external effects are named and guarded
(Rule 1). Blind spots — the perspective nobody argued — are surfaced.

### Check 4: Falsifiability
Central claims name what would falsify them (Rule 4), or are flagged as un-falsifiable.

## If a check is UNVERIFIABLE
Report UNVERIFIABLE and say why. If `standards_ref` is UNSET and the review is domain-specific,
say the domain checks are UNVERIFIABLE. Never report an unverifiable check as a pass.

# Research Standard

The baseline the Research Critic checks against. Ships with placeholders. Fill in the source
policy, method norms, and confidence definitions before the Critic's checks mean anything.

```yaml
source_policy: UNSET # e.g. primary sources preferred, date < 1yr for tech
citation_style: UNSET # e.g. inline links, numbered, URL+date
allowed_evidence_types: UNSET # e.g. primary research, docs, code, official docs
confidence_definitions: UNSET # what high/medium/low mean here
last_verified: UNSET
```

## The four checks the Critic runs

### Check 1: Method matches the claim
- A prevalence claim needs a survey or observed population. A depth claim needs interviews. A
  causal claim needs a controlled test or an explicit "correlation only" label.
- If the method cannot establish the claim, the claim is downgraded or the method is a finding.

### Check 2: Evidence is attributed
- Every number, quote, and factual claim carries a source: what, where, when, what type.
- No unattributed number. An estimate is labeled an estimate, not a measurement.

### Check 3: Sources are sound
- Sources are checked against the `name_policy`: primary over secondary, dated, not
  promotional, not a single source standing for a general claim.
- A claim resting on one source is flagged, not passed.

### Check 4: Synthesis stays honest
- No invented users, quotes, studies, or numbers.
- Uncertainty is labeled; a synthesis does not assert what the raw input does not contain.
- The output names the decision it informs and the confidence it earns (Rule 4).

## If a check is UNVERIFIABLE
Report UNVERIFIABLE and say why. Never report an unverifiable check as a pass.

# Adversarial Product & Market

A dedicated product-market adversarial reviewer. Audits product and market decisions for unvalidated assumptions, weak evidence, and market risk, with a hard veto that only a human can clear.

Built from the Adversarial Agents framework, applied to product.

## The agent

- **`agents/product-adversary.md`** — a single adversary that reviews product work.
  Holds a hard veto.

## The checks

1. **Market assumption** — is the market assumption validated or assumed.
2. **User need** — is the user need real and evidenced.
3. **Competitive position** — is the competitive claim supported.
4. **Business case** — does the business case hold up.
5. **Risk** — what is the downside if the bet is wrong.

## Skills

- `market-assumption-check` — Checks whether market assumptions are validated or assumed.
- `user-need-check` — Checks whether the user need is real and evidenced.
- `competitive-position-check` — Checks whether competitive claims are supported.
- `business-case-check` — Checks whether the business case holds up.
- `market-risk-scan` — Scans for downside if the bet is wrong.
- `adversarial-product` — the worker skill (the review loop).

## References

- `references/constitution.md` — the product-review constitution.
- `references/product-standard.md` — the product quality bar.
- `references/personas.md` — the stress personas.
- `references/calibration-ledger.md` — the verdict record.

## Commands

- `adversarial-product` — the loop.
- `product-review` — run a single review.

## Templates

- `assets/templates/decision-record.md`
- `assets/templates/calibration-entry.md`

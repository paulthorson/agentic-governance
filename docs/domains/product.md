# Product Domain — deep dive

**Plugin:** `adversarial-product/` · **Veto:** unvalidated assumptions, unsound business case

## What it reviews

Product and market decisions. A product/market reviewer that audits market
assumptions, user need, competitive position, business case, and market risk.

## Adversary agents

| Agent | Role |
|---|---|
| `product-adversary` | The single reviewer — audits market assumptions, user need, competitive position, business case, and market risk |

## The checks

- **Market-assumption check** — are the market assumptions validated?
- **User-need check** — is there a real user need?
- **Competitive-position check** — how does this compare to alternatives?
- **Business-case check** — is the business case sound?
- **Market-risk scan** — what market risks exist?

## Skills

`prod-market-assumption-check`, `prod-user-need-check`,
`prod-competitive-position-check`, `prod-business-case-check`,
`prod-market-risk-scan`, `prod-adversarial-product` (worker).

## Constitution / veto

The product constitution gates on **unvalidated assumptions and an unsound
business case** — a decision built on unvalidated assumptions or a weak business
case is kicked back. Only a human clears a veto.

## How to use

```
Use the governance server to run a review of this product decision in the product domain:
<your decision>
```

## See also

- [[Domains]] · [[Architecture]] · [[Constitution]]

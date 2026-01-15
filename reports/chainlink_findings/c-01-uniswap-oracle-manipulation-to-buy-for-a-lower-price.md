---
# Core Classification
protocol: Forgottenplayland
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31718
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/ForgottenPlayland-security-review.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - oracle

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[C-01] Uniswap oracle manipulation to buy for a lower price

### Overview


The report states that there is a high severity bug in the `uniswapV2Router.getAmountsIn()` function. This bug can be easily manipulated by a large swap in Uniswap pairs. The attacker can use this to flashloan `referenceToken` and sell it in the Uniswap pair, causing the price of `referenceToken` to decrease significantly. They can then use the manipulated price to buy TokenBox at a very low cost using `paymentToken` and return the flashloaned `referenceToken`. 

To prevent this, it is recommended to use TWAP to read prices from Uniswap V2 pairs. However, even TWAP can be manipulated for low liquidity pairs. It is suggested to use centralized oracles like Chainlink instead. These feeds can be used when allowing a token as `paymentToken`.

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** High

**Description**

`uniswapV2Router.getAmountsIn()` is used to calculate the amount of `paymentToken` required for the amount in `referenceToken`.
This feed is easily manipulated by a large swap in Uniswap pairs.
So the attacker can in one transaction:

1. Flashloan `referenceToken`
2. Sell this `referenceToken` in the Uniswap pair buying `paymentToken`. The price of `referenceToken` is decreased up to almost zero.
3. Paying using `paymentToken` to mint in TokenBox. The manipulated price will help to spend a very small amount of `paymentToken` to buy TokenBox priced in `referenceToken`
4. Return flashloaned `referenceToken`.

**Recommendations**

TWAP is the recommended way of reading the price from Uniswap V2 pairs. But it is also can be manipulated for low liquidity pairs.
Consider using centralized oracles like Chainlink. E.g. Chainlink feeds can be provided when allowing a token as paymentToken.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Forgottenplayland |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/ForgottenPlayland-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


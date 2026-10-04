---
# Core Classification
protocol: f(x) v2 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61796
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/fx-v2-audit
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Minimum Price Deviation Is Calculated Incorrectly in Price Oracles

### Overview


The getPrice() function in the ETHPriceOracle, LSDPriceOracleBase, and BTCDerivativeOracleBase contracts are not correctly calculating the minimum price deviation. This is because they are using the wrong formula, which checks the deviation from the minPrice instead of the anchorPrice. This makes the deviation always lower than the maximum allowed deviation from the anchor price. The correct formula is to check the deviation against the anchorPrice. This bug has been resolved in a recent pull request.

### Original Finding Content

The [`getPrice()` function of `ETHPriceOracle`](https://github.com/AladdinDAO/fx-protocol-contracts/blob/56a47eab8d10334e479df83a2b13a8b68ce390e9/contracts/price-oracle/ETHPriceOracle.sol#L61-L74), [the `getPrice()` function of `LSDPriceOracleBase`](https://github.com/AladdinDAO/fx-protocol-contracts/blob/56a47eab8d10334e479df83a2b13a8b68ce390e9/contracts/price-oracle/LSDPriceOracleBase.sol#L85-L99), [the `getPrice()` and `getExchangePrice()` functions of `BTCDerivativeOracleBase`](https://github.com/AladdinDAO/fx-protocol-contracts/blob/56a47eab8d10334e479df83a2b13a8b68ce390e9/contracts/price-oracle/BTCDerivativeOracleBase.sol#L58-L72), all calculate the minimum price deviation by using the `(anchorPrice - minPrice) / minPrice > maxDeviation` formula. If the deviation is higher than the max deviation allowed, the minimum price is reset to the anchor price.

However, this calculation is incorrect. It checks the deviation from `minPrice` which makes deviation restrictive and causes it to always be less than the max deviation allowed from the anchor price. The correct formula is to check the deviation against `anchorPrice` instead of `minPrice`: `(anchorPrice - minPrice) / anchorPrice > maxDeviation`.

When calculating the minimum price deviation, consider checking the deviation against `anchorPrice` instead of `minPrice`.

***Update:** Resolved in [pull request #20](https://github.com/AladdinDAO/fx-protocol-contracts/pull/20).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | f(x) v2 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/fx-v2-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


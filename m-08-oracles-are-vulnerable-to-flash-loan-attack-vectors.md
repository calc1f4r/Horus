---
# Core Classification
protocol: StakeDAO_2025-07-21
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63607
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/StakeDAO-security-review_2025-07-21.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-08] Oracles are vulnerable to flash loan attack vectors

### Overview


The report addresses a bug in the current system where the oracles directly fetch the current price of LP tokens in the pool. This is not safe because the price can be manipulated for a short period of time by multiple attack vectors, with the biggest threat being flashloan attacks. This is due to the direct usage of the pool state in the oracle price calculation. The report recommends implementing a TWAP logic to eliminate imbalanced pool state scenarios and improve the accuracy and smoothness of the price calculation. 

### Original Finding Content


_Acknowledged_

## Severity

**Impact:** High

**Likelihood:** Law

## Description

Both of the oracles directly fetch the current price of LP tokens in the pool. However, this is not safe because price can be manipulated for a very short time-range by multiple attack vectors. One of the biggest threats is flashloan attack vectors. When the pool is imbalanced in terms of liquidity, oracles will return an incorrect value for LP price.

The root cause of this situation is the direct usage of Pool state in oracle price calculation. Implementation like TWAP is crucial in this kind of scenarios. Morpho Blue will use this vulnerable oracle, and attacker can liquidate every position by manipulating the price of LP token. 

```solidity
        uint256 priceLpInPeg = CURVE_POOL.get_virtual_price(); // @audit on-chain price without TWAP
```

## Recommendations

Implement a TWAP logic in order to eliminate imbalanced curve pool state scenarios. Time averaged price will be more accurate and smooth than the current price calculation.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | StakeDAO_2025-07-21 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/StakeDAO-security-review_2025-07-21.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


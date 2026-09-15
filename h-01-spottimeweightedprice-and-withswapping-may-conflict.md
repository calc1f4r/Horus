---
# Core Classification
protocol: Radiant-July
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41031
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Radiant-security-review-July.md
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-01] `spotTimeWeightedPrice` and `withSwapping` may conflict

### Overview


The `autoRebalance` function has two input parameters that are used to determine the new `baseLower` and `baseUpper` values. However, when the `useOracleForNewBounds` parameter is set to `false` and the `withSwapping` parameter is set to `true`, there is a problem that causes the spot price after the swap to be different from the `spotTimeWeightedPrice` obtained before the swap. This results in an unreasonable final liquidity range, which can lead to issues such as mint failure or uncompensated losses. To fix this, it is recommended to ensure that the swap limit price is the same as `priceRefForBounds`.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

The `autoRebalance` function has two input parameters.

- `useOracleForNewBounds`: If `false`, use `spotTimeWeightedPrice` to determine the new `baseLower` and `baseUpper`
- `withSwapping`: If `true`, when the difference between spot and oracle prices is too large, some tokens will be swapped to make the spot price closer to the oracle price.

The following scenario occurs when `useOracleForNewBounds` is `false` and `withSwapping` is `true` and the price difference between spot and oracle is too large. There is a discrepancy between the spot price after the swap and the `spotTimeWeightedPrice` obtained before the swap. The `baseLower` and `baseUppe` are determined by the price before the swap. This will lead to an unreasonable final liquidity range.

In extreme cases, this may result in mint failure or uncompensated losses due to the use of unreasonable liquidity ranges.

## Recommendations

Make sure the swap limit price is the same as `priceRefForBounds`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Radiant-July |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Radiant-security-review-July.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


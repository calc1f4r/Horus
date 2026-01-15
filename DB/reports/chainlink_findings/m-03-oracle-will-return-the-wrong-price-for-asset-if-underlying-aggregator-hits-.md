---
# Core Classification
protocol: Pear V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44103
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Pear-v2-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[M-03] Oracle Will Return the Wrong Price for Asset if Underlying Aggregator Hits `minAnswer`

### Overview


The bug report discusses a problem with two functions, `convertFeeToEth()` and `calculateArbAmount()`, in two different files, `PlatformLogic.sol` and `RewardsClaimer.sol`. These functions use Chainlink's aggregators to get the price of an asset. However, if the asset experiences a large drop in value, the aggregator will return a minimum price instead of the actual price. This can be manipulated by users, allowing them to borrow at the wrong price. The recommended solution is to check the returned answer against the minimum and maximum price and revert if it is outside of the bounds. The team has acknowledged the issue.

### Original Finding Content

## Severity

Medium Risk

## Description

`convertFeeToEth()` in `PlatformLogic.sol` and `calculateArbAmount()` in `RewardsClaimer.sol` will return the wrong price for the asset if the underlying aggregator hits `minAnswer`.

Chainlink's aggregators have a built-in circuit breaker if the price of an asset goes outside of a predetermined price band. The result is that if an asset experiences a huge drop in value (i.e. LUNA crash), the price of the oracle will continue to return the `minPrice` instead of the actual price of the asset. This would allow users to continue borrowing with the asset but at the wrong price. This is exactly what happened to [Venus on BSC when LUNA imploded](https://rekt.news/venus-blizz-rekt/).

When `latestRoundData()` is called, it requests data from the aggregator. The aggregator has a `minPrice` and a `maxPrice`. If the price falls below the `minPrice` instead of reverting, it will just return the min price.

## Impact

In the event that an asset crashes, the price can be manipulated.

## Location of Affected Code

File: [src/PlatformLogic.sol#L486](https://github.com/pear-protocol/gmx-v2-core/blob/f3329d0474013d60d183a5773093b94a9e55caae/src/PlatformLogic.sol#L486)

File: [src/rewards/RewardsClaimer.sol#L414](https://github.com/pear-protocol/gmx-v2-core/blob/f3329d0474013d60d183a5773093b94a9e55caae/src/rewards/RewardsClaimer.sol#L414)

## Recommendation

The `convertFeeToEth()` and `calculateArbAmount()` functions should check the returned answer against the `minPrice/maxPrice` and revert if the answer is outside of the bounds.

## Team Response

Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Pear V2 |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Pear-v2-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


---
# Core Classification
protocol: Olympusdao
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6678
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/50
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-olympus-judging/issues/210

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - cross_chain
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Bahurum
---

## Vulnerability Title

M-2: Vault can experience long downtime periods

### Overview


This bug report is about an issue where the Vault can experience long downtime periods due to the `_isPoolSafe()` function checking if the balancer pool spot price is within the boundaries defined by `THRESHOLD` respect to the last fetched chainlink price. If `THRESHOLD` is less than 2%, then the Chainlink price can deviate by more than 1% from the pool spot price and less than 2% from the on-chain trusted price for up to 24 hours. During this period, withdrawals and deposits will not be possible. The impact of this issue is that withdrawals and deposits can be often unavailable for several hours. The bug was found by Bahurum and was identified through manual review. The recommended solution is to ensure that `THRESHOLD` is only allowed to take a tight range of values around 2% to avoid this issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-olympus-judging/issues/210 

## Found by 
Bahurum

## Summary
The chainlink price could stay up to 24 hours (heartbeat period) outside the boundaries defined by `THRESHOLD` but within the chainlink deviation threshold. Deposits and withdrawals will not be possible during this period of time.

## Vulnerability Detail
The `_isPoolSafe()` function checks if the balancer pool spot price is within the boundaries defined by `THRESHOLD` respect to the last fetched chainlink price. 

Since in `_valueCollateral()` the `updateThreshold` should be 24 hours (as in the tests), then the OHM derived oracle price could stay at up to 2% from the on-chain trusted price. The value is 2% because in [WstethLiquidityVault.sol#L223](https://github.com/sherlock-audit/2023-02-olympus/blob/main/src/policies/lending/WstethLiquidityVault.sol#L223):
```solidity
return (amount_ * stethPerWsteth * stethUsd * decimalAdjustment) / (ohmEth * ethUsd * 1e18);
```
`stethPerWsteth` is mostly stable and changes in `stethUsd` and `ethUsd` will cancel out, so the return value changes will be close to changes in `ohmEth`, so up to 2% from the on-chain trusted price.

If `THRESHOLD` < 2%, say 1% as in the tests, then the Chainlink price can deviate by more than 1% from the pool spot price and less than 2% from the on-chain trusted price fro up to 24 h. During this period withdrawals and deposits will revert.

## Impact
Withdrawals and deposits can be often unavailable for several hours.
## Code Snippet
https://github.com/sherlock-audit/2023-02-olympus/blob/main/src/policies/lending/abstracts/SingleSidedLiquidityVault.sol#L411-L421

## Tool used

Manual Review

## Recommendation
`THRESHOLD` is not fixed and can be changed by the admin, meaning that it can take different values over time.Only a tight range of values around 2% should be allowed to avoid the scenario above.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Olympusdao |
| Report Date | N/A |
| Finders | Bahurum |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-olympus-judging/issues/210
- **Contest**: https://app.sherlock.xyz/audits/contests/50

### Keywords for Search

`vulnerability`


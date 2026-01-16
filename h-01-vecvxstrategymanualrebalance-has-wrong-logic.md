---
# Core Classification
protocol: BadgerDAO
chain: everychain
category: uncategorized
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 737
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-09-bvecvx-by-badgerdao-contest
source_link: https://code4rena.com/reports/2021-09-bvecvx
github_link: https://github.com/code-423n4/2021-09-bvecvx-findings/issues/47

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - wrong_math

protocol_categories:
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - cmichel
  - tabish
---

## Vulnerability Title

[H-01] veCVXStrategy.manualRebalance has wrong logic

### Overview


This bug report is about a vulnerability in the `veCVXStrategy.manualRebalance` function. It compares two ratios, `currentLockRatio` and `newLockRatio`, which compute different things and are not comparable. `currentLockRatio` is a percentage value with 18 decimals (i.e. `1e18 = 100%`) and its max value can at most be `1e18`, whereas `newLockRatio` is a CVX token amount which is unbounded and just depends on the `totalCVXBalance` amount. The comparison that follows does not make sense and leads to locking nearly everything if `totalCVXBalance` is high. The recommended mitigation steps suggest that the "ratios" should actually be in CVX amounts and not in percentages, and that `currentLockRatio` should just be `balanceInLock`. The variables should also be renamed as they aren't really ratios but absolute CVX balance amounts.

### Original Finding Content

## Handle

cmichel


## Vulnerability details

## Vulnerability Details
The `veCVXStrategy.manualRebalance` function computes two ratios `currentLockRatio` and `newLockRatio` and compares them.

However, these ratios compute different things and are not comparable:
- `currentLockRatio = balanceInLock.mul(10**18).div(totalCVXBalance)` is a **percentage value** with 18 decimals (i.e. `1e18 = 100%`). Its max value can at most be `1e18`.
- `newLockRatio = totalCVXBalance.mul(toLock).div(MAX_BPS)` is a **CVX token amount**. It's unbounded and just depends on the `totalCVXBalance` amount.

The comparison that follows does not make sense:

```solidity
if (newLockRatio <= currentLockRatio) {
  // ...
}
```

## Impact
The rebalancing is broken and does not correctly rebalance.
It usually leads to locking nearly everything if `totalCVXBalance` is high.

## Recommended Mitigation Steps
Judging from the `cvxToLock = newLockRatio.sub(currentLockRatio)` it seems the desired computation is that the "ratios" should actually be in CVX amounts and not in percentages. Therefore, `currentLockRatio` should just be `balanceInLock`. (The variables should be renamed as they aren't really ratios but absolute CVX balance amounts.)

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | BadgerDAO |
| Report Date | N/A |
| Finders | cmichel, tabish |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-bvecvx
- **GitHub**: https://github.com/code-423n4/2021-09-bvecvx-findings/issues/47
- **Contest**: https://code4rena.com/contests/2021-09-bvecvx-by-badgerdao-contest

### Keywords for Search

`Wrong Math`


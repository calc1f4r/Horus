---
# Core Classification
protocol: Canto
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27561
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-10-canto
source_link: https://code4rena.com/reports/2023-10-canto
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-05] Missing week validation while claiming rewards

### Overview

See description below for full details.

### Original Finding Content


- https://github.com/code-423n4/2023-10-canto/blob/main/canto_ambient/contracts/mixins/LiquidityMining.sol#L156
- https://github.com/code-423n4/2023-10-canto/blob/main/canto_ambient/contracts/mixins/LiquidityMining.sol#L256

In `claimConcentratedRewards()` and `claimAmbientRewards()`, the implementation takes an array of the weeks which are expected to be claimed. This is user input, and lacks any validation over the provided argument values.

Using `claimConcentratedRewards()` as the example, we can see each element in `weeksToClaim` is not checked to be an actual _week_, i.e. that `week % WEEK == 0`.

```solidity
174:         for (uint256 i; i < weeksToClaim.length; ++i) {
175:             uint32 week = weeksToClaim[i];
176:             require(week + WEEK < block.timestamp, "Week not over yet");
177:             require(
178:                 !concLiquidityRewardsClaimed_[poolIdx][posKey][week],
179:                 "Already claimed"
180:             );
181:             uint256 overallInRangeLiquidity = timeWeightedWeeklyGlobalConcLiquidity_[poolIdx][week];
```

Consider adding an explicit check to ensure the elements in `weeksToClaim` are valid weeks.

```diff
    uint32 week = weeksToClaim[i];
    require(week + WEEK < block.timestamp, "Week not over yet");
+   require(week % WEEK == 0, "Invalid week");
```

## Non Critical Issues



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2023-10-canto
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2023-10-canto

### Keywords for Search

`vulnerability`


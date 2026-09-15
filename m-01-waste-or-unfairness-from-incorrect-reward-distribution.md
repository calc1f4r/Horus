---
# Core Classification
protocol: Tangent_2025-10-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63866
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Tangent-security-review_2025-10-30.md
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

[M-01] Waste or unfairness from incorrect reward distribution

### Overview


This bug report discusses two smart contracts, `VsTAN.sol` and `RewardAccumulator.sol`, which have issues when the total supply is zero. When rewards are added during a zero-supply period, the contracts waste rewards that were never distributed. Additionally, when the first user stakes after a zero-supply period, all accumulated rewards from that period are incorrectly distributed to the first staker, giving them an unfair advantage. The report recommends that zero-supply periods should be handled consistently and correctly.

### Original Finding Content


_Resolved_

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

Both `VsTAN.sol` and `RewardAccumulator.sol` implement Synthetix-style staking reward systems but have flaws when `totalSupply (or totalCollateral) is zero`. 

- When rewards are added during a zero-supply period, when leftover rewards from the previous period are included in the new `rewardRate`, wasting rewards that were never distributed. 

```solidity
if (timestamp >= rData.periodFinish) {
    rewardData[rewardToken].rewardRate = amount / ONE_WEEK;
} else {
    uint256 leftover = (rData.periodFinish - timestamp) * rData.rewardRate;
    rewardData[rewardToken].rewardRate = (amount + leftover) / ONE_WEEK;
}
```
When `totalSupply = 0`, no rewards are actually distributed (no one to distribute to). However, leftover is calculated as if rewards for these periods were being distributed, effectively wasting rewards that were never distributed.

- Additionally, when the first user stakes after a zero-supply period, `lastUpdateTime` is not updated during the zero-supply period, causing all accumulated rewards from that period to be incorrectly distributed to the first staker, creating an unfair advantage.

```solidity
if (_totalSupplyVsTan != 0) {  // or totalCollateral != 0
    rewardData[token].rewardPerTokenStored = _rewardPerToken(token);
    rewardData[token].lastUpdateTime = _lastTimeRewardApplicable(rewardData[token].periodFinish);
}
```

```solidity
return rewardData[_rewardToken].rewardPerTokenStored +
    (((_lastTimeRewardApplicable(...) - rewardData[_rewardToken].lastUpdateTime) * 
      rewardData[_rewardToken].rewardRate * 1e18) / totalSupplyVsTan);
```

1. When `totalSupply = 0`, lastUpdateTime is NOT updated.
2. When the first user stakes, totalSupply is still zero before the update.
3. `lastUpdateTime` still reflects the old timestamp (before the zero-supply period) and is not updated. 
4. After the stake, `totalsupply` is updated.
5. In the next stake/other operation, the `_rewardPerToken()` calculates rewards from `lastUpdateTime` to now, including the entire zero-supply period, and distribute it to the first user.

## Recommendations
Zero-supply periods should be handled consistently and correctly.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Tangent_2025-10-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Tangent-security-review_2025-10-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


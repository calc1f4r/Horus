---
# Core Classification
protocol: Planar Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35313
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar Finance.md
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
  - Zokyo
---

## Vulnerability Title

Lack of Epoch End Block Consideration in `pendingRewards` Function

### Overview


This bug report describes a problem with the `pendingRewards` function in the LpNFTPool.sol source code. The function does not take into account the end of the epoch block, which can result in over-distribution of rewards. The report recommends adding a check for the end of the epoch block to ensure rewards are only calculated within the designated epoch. This will prevent potential over-distribution and align the reward distribution with the intended epochs set by the contract owner or protocol. The report also includes a code snippet showing the recommended modification to the function. 

### Original Finding Content

**Severity**: Medium

**Status**:  Unresolved


**Source**: LpNFTPool.sol

**Description**: 

The `pendingRewards` function calculates the pending rewards for a staking position without considering the end of the epoch block `(endOfEpochBlock)`. This omission can lead to the calculation of rewards beyond the intended reward distribution period, potentially resulting in over-distribution of rewards. The function recalculates `accRewardsPerShare` based on the current block timestamp, last reward time, reserve, and pool emission rate without checking if the current period is within the active epoch defined for reward distribution.

**Recommendation**: 

To ensure that rewards are accurately calculated and distributed within the designated epochs, it is recommended to incorporate a check for the `endOfEpochBlock` within the `pendingRewards` function. This check should ensure that rewards are only calculated up to the end of the active epoch. If the current block number exceeds the `endOfEpochBlock`, the calculation should use the `endOfEpochBlock` as the upper limit for the rewards period. This modification will prevent the potential over-distribution of rewards and ensure that the reward distribution aligns with the intended epochs set by the contract owner or protocol.


```solidity
function pendingRewards(uint256 tokenId) external view returns (uint256) {
    StakingPosition storage position = _stakingPositions[tokenId];

    uint256 accRewardsPerShare = _accRewardsPerShare;
    (,,uint256 lastRewardTime, uint256 reserve, uint256 poolEmissionRate) = master.getPoolInfo(address(this));
    uint256 endOfEpochBlock = master.getEndOfEpochBlock(address(this)); // Assume this function exists or a similar mechanism to retrieve endOfEpochBlock

    // Ensure rewards are calculated within the epoch
    uint256 effectiveLastRewardBlock = lastRewardTime < endOfEpochBlock ? lastRewardTime : endOfEpochBlock;

    if ((reserve > 0 || _currentBlockTimestamp() > effectiveLastRewardBlock) && _lpSupplyWithMultiplier > 0) {
        uint256 duration = _currentBlockTimestamp().sub(effectiveLastRewardBlock);
        uint256 tokenRewards = duration.mul(poolEmissionRate).add(reserve);
        accRewardsPerShare = accRewardsPerShare.add(tokenRewards.mul(1e18).div(_lpSupplyWithMultiplier));
    }

    return position.amountWithMultiplier.mul(accRewardsPerShare).div(1e18).sub(position.rewardDebt)
        .add(position.pendingXPlaneRewards).add(position.pendingPlaneRewards);
}


```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Planar Finance |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


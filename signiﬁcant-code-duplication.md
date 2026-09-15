---
# Core Classification
protocol: Frax Solidity
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17926
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Samuel Moelius Maximilian Krüger Troy Sargent
---

## Vulnerability Title

Signiﬁcant code duplication

### Overview

See description below for full details.

### Original Finding Content

## Frax Solidity Security Assessment

## Difficulty
**High**

## Type
**Access Controls**

## Target
**Various**

## Description
Significant code duplication exists throughout the codebase. Duplicate code can lead to incomplete fixes or inconsistent behavior (e.g., because the code is modified in one location but not in all).

For example, the `FraxUnifiedFarmTemplate.sol` and `StakingRewardsMultiGauge.sol` files both contain a `retroCatchUp` function. As seen in Figure 13.1, the functions are almost identical.

```solidity
// If the period expired, renew it
function retroCatchUp() internal {
    // Pull in rewards from the rewards distributor
    rewards_distributor.distributeReward(address(this));

    // Ensure the provided reward amount is not more than the balance in the contract.
    // This keeps the reward rate in the right range, preventing overflows due to very high values of rewardRate in the earned and rewardsPerToken functions;
    // Reward + leftover must be less than 2^256 / 10^18 to avoid overflow.
    uint256 num_periods_elapsed = uint256(block.timestamp - periodFinish) / rewardsDuration;  // Floor division to the nearest period

    // Make sure there are enough tokens to renew the reward period
    for (uint256 i = 0; i < rewardTokens.length; i++) {
        require((rewardRates(i) * rewardsDuration * (num_periods_elapsed + 1)) <= ERC20(rewardTokens[i]).balanceOf(address(this)), string(abi.encodePacked("Not enough reward tokens available: ", rewardTokens[i])));
    }
    
    // uint256 old_lastUpdateTime = lastUpdateTime;
    // uint256 new_lastUpdateTime = block.timestamp;
    // lastUpdateTime = periodFinish;
    periodFinish = periodFinish + ((num_periods_elapsed + 1) * rewardsDuration);

    // Update the rewards and time
    _updateStoredRewardsAndTime();
    emit RewardsPeriodRenewed(address(stakingToken));
}
```
    
**Figure 13.1:** Left: `contracts/Staking/FraxUnifiedFarmTemplate.sol#L463-L490`  
**Right: `contracts/Staking/StakingRewardsMultiGauge.sol#L637-L662`**

## Exploit Scenario
Alice, a Frax Finance developer, is asked to fix a bug in the `retroCatchUp` function. Alice updates one instance of the function, but not both. Eve discovers a copy of the function in which the bug is not fixed and exploits the bug.

## Recommendations
**Short term:** Perform a comprehensive code review and identify pieces of code that are semantically similar. Factor out those pieces of code into separate functions where it makes sense to do so. This will reduce the risk that those pieces of code diverge after the code is updated.

**Long term:** Adopt code practices that discourage code duplication. Doing so will help to prevent this problem from recurring.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Solidity |
| Report Date | N/A |
| Finders | Samuel Moelius Maximilian Krüger Troy Sargent |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf

### Keywords for Search

`vulnerability`


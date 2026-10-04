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
solodit_id: 17927
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
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
  - Samuel Moelius Maximilian Krüger Troy Sargent
---

## Vulnerability Title

StakingRewardsMultiGauge.recoverERC20 allows token managers to steal rewards

### Overview


A bug has been identified in the StakingRewardsMultiGauge contract that allows token managers to steal rewards. The recoverERC20 function, which is supposed to be callable only by the contract owner, allows token managers to send themselves the requested amount of the token they manage. This violates conventions established by other Frax Solidity contracts. To prevent this bug, the token manager's ability to call recoverERC20 should be eliminated in the short-term and regularly reviewing all uses of contract modifiers should be done in the long-term. This will help to expose bugs like the one described and bring recoverERC20 in line with established conventions.

### Original Finding Content

## Frax Solidity Security Assessment

## Difficulty: High

**Type:** Access Controls  
**Target:** StakingRewardsMultiGauge.sol  

### Description
The `recoverERC20` function in the `StakingRewardsMultiGauge` contract allows token managers to steal rewards. This violates conventions established by other Frax Solidity contracts in which `recoverERC20` can be called only by the contract owner.

The relevant code appears in figure 14.1. The `recoverERC20` function checks whether the caller is a token manager and, if so, sends him the requested amount of the token he manages. Convention states that this function should be callable only by the contract owner. Moreover, its purpose is typically to recover tokens unrelated to the contract.

```solidity
// Added to support recovering LP Rewards and other mistaken tokens from other systems to be distributed to holders
function recoverERC20(address tokenAddress, uint256 tokenAmount) external onlyTknMgrs(tokenAddress) {
    // Check if the desired token is a reward token
    bool isRewardToken = false;
    for (uint256 i = 0; i < rewardTokens.length; i++) {
        if (rewardTokens[i] == tokenAddress) {
            isRewardToken = true;
            break;
        }
    }
    // Only the reward managers can take back their reward tokens
    if (isRewardToken && rewardManagers[tokenAddress] == msg.sender) {
        ERC20(tokenAddress).transfer(msg.sender, tokenAmount);
        emit Recovered(msg.sender, tokenAddress, tokenAmount);
        return;
    }
}
```
*Figure 14.1: contracts/Staking/StakingRewardsMultiGauge.sol#L798-L814*

For comparison, consider the `CCFrax1to1AMM` contract’s `recoverERC20` function. It is callable only by the contract owner and specifically disallows transferring tokens used by the contract.

```solidity
function recoverERC20(address tokenAddress, uint256 tokenAmount) external onlyByOwner {
    require(!is_swap_token[tokenAddress], "Cannot withdraw swap tokens");
    TransferHelper.safeTransfer(address(tokenAddress), msg.sender, tokenAmount);
}
```
*Figure 14.2: contracts/Misc_AMOs/__CROSSCHAIN/Moonriver/CCFrax1to1AMM.sol#L340-L344*

### Exploit Scenario
Eve tricks Frax Finance into making her a token manager for the `StakingRewardsMultiGauge` contract. When the contract’s token balance is high, Eve withdraws the tokens and vanishes.

### Recommendations
Short term, eliminate the token manager’s ability to call `recoverERC20`. This will bring `recoverERC20` in line with established conventions regarding the function’s purpose and usage.

Long term, regularly review all uses of contract modifiers, such as `onlyTknMgrs`. Doing so will help to expose bugs like the one described here.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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


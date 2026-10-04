---
# Core Classification
protocol: Alchemix
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38254
audit_firm: Immunefi
contest_link: https://immunefi.com/bounty/alchemix-boost/
source_link: none
github_link: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Alchemix/31575%20-%20%5bSC%20-%20Medium%5d%20depositIntoRewardPool%20and%20%20withdrawFromRewardPo....md

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

protocol_categories:
  - liquid_staking
  - dexes
  - yield
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Kenzo
---

## Vulnerability Title

`depositIntoRewardPool()` and  `withdrawFromRewardPool()` in `RewardPoolManager` contract  are missing slippage control mechanism

### Overview


This report discusses a bug in the `RewardPoolManager` smart contract on the GitHub platform. This bug affects the functions `depositIntoRewardPool()` and `withdrawFromRewardPool()` by not including a mechanism to control slippage. This can lead to loss of tokens or shares for users, and in the worst case, malicious attacks can result in significant financial losses. The report recommends implementing a proper slippage control mechanism in these functions to prevent this issue.

### Original Finding Content

Report type: Smart Contract


Target: https://github.com/alchemix-finance/alchemix-v2-dao/blob/main/src/RewardPoolManager.sol

Impacts:
- Contract fails to deliver promised returns, but doesn't lose value
- Theft of unclaimed yield

## Description
## Title
`depositIntoRewardPool()` and  `withdrawFromRewardPool()` in `RewardPoolManager`  are missing slippage control mechanism

## Vulnerability Details
The `RewardPoolManger` is meant to be compatible with ERC4626. The `depositIntoRewardPool()` and `withdrawFromRewardPool()` functions are used to deposit and withdraw funds with Aura Pools and the shares and tokens are minted  but as it is pool deposit, there is always fluctuations in the ratio deposit to mint or burn to withdraw.  The the issue is these two functions don't implement any slippage mechanism to avoid such ratio drop. At worst case, the MEV attacks such as frontrunning the transaction can make loss of shares while depositing and loss of tokens while withdrawing. 
`RewardPoolHandler::depositIntoRewardPool` :
```solidity
    function depositIntoRewardPool(uint256 _amount) external returns (bool) {
        require(msg.sender == veALCX, "must be veALCX");

        IERC20(poolToken).approve(rewardPool, _amount);
    
@>      IRewardPool4626(rewardPool).deposit(_amount, address(this));
        return true;
    }
```umm
`RewardPoolHandler::withdrawFromRewardPool` :

```solidity
    function withdrawFromRewardPool(uint256 _amount) external returns (bool) {
        require(msg.sender == veALCX, "must be veALCX");

@>      IRewardPool4626(rewardPool).withdraw(_amount, veALCX, address(this));
        return true;
    }

```
## Impact Details
Users will loss tokens or shares due to not handling the slippage case. At worst, MEV may make user loss a huge amount of funds. 

## References
https://github.com/alchemix-finance/alchemix-v2-dao/blob/main/src/RewardPoolManager.sol?utm_source=immunefi#L84

https://github.com/alchemix-finance/alchemix-v2-dao/blob/main/src/RewardPoolManager.sol?utm_source=immunefi#L93
## Recommendation
Implement proper slippage control mechanism in these two functions to avoid the mentioned issue.



## Proof of Concept 
Attack is straightforward and POC for Mev attacks are hard to simulate.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Immunefi |
| Protocol | Alchemix |
| Report Date | N/A |
| Finders | Kenzo |

### Source Links

- **Source**: N/A
- **GitHub**: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Alchemix/31575%20-%20%5bSC%20-%20Medium%5d%20depositIntoRewardPool%20and%20%20withdrawFromRewardPo....md
- **Contest**: https://immunefi.com/bounty/alchemix-boost/

### Keywords for Search

`vulnerability`


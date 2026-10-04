---
# Core Classification
protocol: Lybra Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21149
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-06-lybra
source_link: https://code4rena.com/reports/2023-06-lybra
github_link: https://github.com/code-423n4/2023-06-lybra-findings/issues/867

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
finders_count: 2
finders:
  - Toshii
  - bytes032
---

## Vulnerability Title

[M-04] The `EUSDMiningIncentives` contract is incorrectly implemented and can allow for more than the intended amount of rewards to be minted

### Overview


A bug has been found in the EUSDMiningIncentives contract of the LybraFinance project. This contract is intended to function similarly to the Synthetix staking rewards contract and the rewards per second, defined as `rewardRatio`, should be distributed to users as an equivalent percentage of how much the user has staked as compared to the total amount staked. However, the calculated amount staked per user is equal to the total amount borrowed of tokens (EUSD and PeUSD) across all vaults, meaning the amount returned by the `totalStaked` function is wrong, as it should also include the total supply of all the vaults which are included in the `pools` array (EUSD and PeUSD). This will result in much more than the intended amount of rewards to be minted, as the numerator (total amount of EUSD and PeUSD) across all users is much more than the denominator (total amount of EUSD).

The `totalStaked` function should be updated to sum up the `totalSupply` of EUSD and all the PeUSD vaults which are in the `pools` array, in order to fix this bug. This bug was discovered through manual review and has been confirmed by LybraFinance.

### Original Finding Content


### Lines of code

<https://github.com/code-423n4/2023-06-lybra/blob/main/contracts/lybra/miner/EUSDMiningIncentives.sol#L132-L134>
<br><https://github.com/code-423n4/2023-06-lybra/blob/main/contracts/lybra/miner/EUSDMiningIncentives.sol#L136-L147>

### Impact

The `EUSDMiningIncentives` contract is intended to function similarly to the Synthetix staking rewards contract. This means the rewards per second, defined as `rewardRatio`, which is set in the `notifyRewardAmount` function, is supposed to be distributed to users as an equivalent percentage of how much the user has staked as compared to the total amount staked. In this contract, the total amount staked is equal to the total supply of EUSD tokens. However, the calculated amount staked PER user is equal to the total amount borrowed of tokens (EUSD and PeUSD) across ALL vaults. This means, the amount returned by the `totalStaked` function is wrong, as it should also include the total supply of all the vaults which are included in the `pools` array (EUSD and PeUSD). This will effectively result in much more than the intended amount of rewards to be minted, as the numerator (total amount of EUSD and PeUSD) across all users is much more than the denominator (total amount of EUSD).

### Proof of Concept

First consider the `stakedOf` function, which sums up the borrowed amount across all vaults in the `pools` array (both EUSD and PeUSD):

```solidity
function stakedOf(address user) public view returns (uint256) {
    uint256 amount;
    for (uint i = 0; i < pools.length; i++) {
        ILybra pool = ILybra(pools[i]);
        uint borrowed = pool.getBorrowedOf(user);
        if (pool.getVaultType() == 1) {
            borrowed = borrowed * (1e20 + peUSDExtraRatio) / 1e20;
        }
        amount += borrowed;
    }
    return amount;
}
```

Then consider the `totalStaked` function, which just returns the total supply of EUSD:

```solidity
function totalStaked() internal view returns (uint256) {
    return EUSD.totalSupply();
}
```

The issue arrises in the `earned` function, which references both the `stakedOf` value and the `totalSupply` value:

```solidity
function earned(address _account) public view returns (uint256) { // @note - read
    return ((stakedOf(_account) * getBoost(_account) * (rewardPerToken() - userRewardPerTokenPaid[_account])) / 1e38) + rewards[_account];
}
```

Here, `stakedOf` (which includes EUSD and PeUSD), is multiplied by a call to `rewardPerToken` minus the old user reward debt. This function has `totalStaked()` in the denominator, which is where this skewed calculation is occurring:

```solidity
function rewardPerToken() public view returns (uint256) {
	...
	return rewardPerTokenStored + (rewardRatio * (lastTimeRewardApplicable() - updatedAt) * 1e18) / totalStaked();
}
```

This will effectively result in much more than the intended amount of rewards to be minted to the users, which will result in the supply of esLBR inflating much faster than intended.

### Tools Used

Manual review

### Recommended Mitigation Steps

The `totalStaked` function should be updated to sum up the `totalSupply` of EUSD and all the PeUSD vaults which are in the `pools` array.

### Assessed type

Math

**[LybraFinance confirmed](https://github.com/code-423n4/2023-06-lybra-findings/issues/867#issuecomment-1639589998)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Lybra Finance |
| Report Date | N/A |
| Finders | Toshii, bytes032 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-06-lybra
- **GitHub**: https://github.com/code-423n4/2023-06-lybra-findings/issues/867
- **Contest**: https://code4rena.com/reports/2023-06-lybra

### Keywords for Search

`vulnerability`


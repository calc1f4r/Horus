---
# Core Classification
protocol: Sturdy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2336
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-sturdy-contest
source_link: https://code4rena.com/reports/2022-05-sturdy
github_link: https://github.com/code-423n4/2022-05-sturdy-findings/issues/70

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
  - lending
  - bridge
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - leastwood  StErMi
  - IllIllI
---

## Vulnerability Title

[M-03] `processYield()` and `distributeYield()` may run out of gas and revert due to long list of extra rewards/yields

### Overview


A bug has been discovered in the code of a smart contract that could prevent yields from being distributed to lenders. The code in question is located in two files: ConvexCurveLPVault.sol and YieldManager.sol. In the first file, the `processYield()` function loops through all extra rewards and transfers them, but there is no guarantee that the tokens involved will be efficient in their use of gas. Additionally, there is no upper bounds on the number of extra rewards. In the second file, `_getAssetYields()` has a similar issue. An attacker could sprinkle each one with dust, forcing a transfer by this function. The bug was discovered through code inspection.

In order to mitigate this bug, it is recommended to include an offset and length as is done in `YieldManager.distributeYield()`. This would ensure that the code is efficient in its use of gas and that there is an upper bound on the number of extra rewards.

### Original Finding Content

_Submitted by IllIllI, also found by leastwood and StErMi_

Yields will not be able to be distributed to lenders because attempts to do so will revert.

### Proof of Concept

The `processYield()` function loops overall of the extra rewards and transfers them

```solidity
File: smart-contracts/ConvexCurveLPVault.sol   #1

105       uint256 extraRewardsLength = IConvexBaseRewardPool(baseRewardPool).extraRewardsLength();
106       for (uint256 i = 0; i < extraRewardsLength; i++) {
107         address _extraReward = IConvexBaseRewardPool(baseRewardPool).extraRewards(i);
108         address _rewardToken = IRewards(_extraReward).rewardToken();
109         _transferYield(_rewardToken);
110       }
```

[ConvexCurveLPVault.sol#L105-L110](https://github.com/code-423n4/2022-05-sturdy/blob/78f51a7a74ebe8adfd055bdbaedfddc05632566f/smart-contracts/ConvexCurveLPVault.sol#L105-L110)<br>

There is no guarantee that the tokens involved will be efficient in their use of gas, and there are no upper bounds on the number of extra rewards:

```solidity
    function extraRewardsLength() external view returns (uint256) {
        return extraRewards.length;
    }


    function addExtraReward(address _reward) external returns(bool){
        require(msg.sender == rewardManager, "!authorized");
        require(_reward != address(0),"!reward setting");


        extraRewards.push(_reward);
        return true;
    }
```

[BaseRewardPool.sol#L105-L115](https://github.com/convex-eth/platform/blob/main/contracts/contracts/BaseRewardPool.sol#L105-L115)<br>

Even if not every extra reward token has a balance, an attacker can sprinkle each one with dust, forcing a transfer by this function

`_getAssetYields()` has a similar issue:

```solidity
File: smart-contracts/YieldManager.sol   #X

129       AssetYield[] memory assetYields = _getAssetYields(exchangedAmount);
130       for (uint256 i = 0; i < assetYields.length; i++) {
131         if (assetYields[i].amount > 0) {
132           uint256 _amount = _convertToStableCoin(assetYields[i].asset, assetYields[i].amount);
133           // 3. deposit Yield to pool for suppliers
134           _depositYield(assetYields[i].asset, _amount);
135         }
136       }
```

[YieldManager.sol#L129-L136](https://github.com/code-423n4/2022-05-sturdy/blob/78f51a7a74ebe8adfd055bdbaedfddc05632566f/smart-contracts/YieldManager.sol#L129-L136)<br>

### Recommended Mitigation Steps

Include an offset and length as is done in `YieldManager.distributeYield()`.

**[sforman2000 (Sturdy) confirmed](https://github.com/code-423n4/2022-05-sturdy-findings/issues/70)**

**[atozICT20 (Sturdy) commented](https://github.com/code-423n4/2022-05-sturdy-findings/issues/70):**
 > [Fix the issue of processYield()'s run out of gas due to convex's extra rewards sturdyfi/code4rena-may-2022#4](https://github.com/sturdyfi/code4rena-may-2022/pull/4)

**[hickuphh3 (judge) commented](https://github.com/code-423n4/2022-05-sturdy-findings/issues/70#issuecomment-1145570424):**
 > I've considered this issue. The reason why I chose not to raise it up is because adding reward tokens is restricted on Convex's side. Given the number of integrations they have, it's unlikely that they will add too many tokens or gas-guzzling ones that will cause claims to run OOG.
> 
> Nevertheless, it is a possibility, albeit an unlikely one, so I'll let the issue stand (also since the sponsor confirmed it).



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Sturdy |
| Report Date | N/A |
| Finders | leastwood  StErMi, IllIllI |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-sturdy
- **GitHub**: https://github.com/code-423n4/2022-05-sturdy-findings/issues/70
- **Contest**: https://code4rena.com/contests/2022-05-sturdy-contest

### Keywords for Search

`vulnerability`


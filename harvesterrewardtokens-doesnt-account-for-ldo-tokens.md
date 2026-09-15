---
# Core Classification
protocol: Brahma Fi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13259
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2022/05/brahma-fi/
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

protocol_categories:
  - dexes
  - services

# Audit Details
report_date: unknown
finders_count: 3
finders:
  -  George Kobakhidze

  - David Oz Kashi
  -  Sergii Kravchenko
---

## Vulnerability Title

Harvester.rewardTokens doesn’t account for LDO tokens

### Overview


This bug report is about a problem with the reward tokens for participating in Curve's ETH-stETH pool and Convex staking. The `ConvexPositionHandler` contract calls an API from Convex via `baseRewardPool.getReward()`, which transfers the reward tokens to the handler’s address. The tokens are then sent to the harvester to be swapped from `ConvexPositionHandler` by getting their list from `harvester.rewardTokens()` and calling `harvester.harvest()`. However, the LDO token’s address is not in the list, so they will not be transferred to the harvester to be swapped. This results in missed rewards and therefore yield for the vault. A mitigation is available that requires governance to call `sweep()` on the LDO balance from the `BaseTradeExecutor` contract and then transferring those LDO tokens to the harvester contract to perform the swap at a later rewards claim. The recommendation is to add the LDO token address to the `rewardTokens()` function.

### Original Finding Content

#### Description


As part of the vault’s strategy, the reward tokens for participating in Curve’s ETH-stETH pool and Convex staking are claimed and swapped for ETH. This is done by having the `ConvexPositionHandler` contract call the reward claims API from Convex via `baseRewardPool.getReward()`, which transfers the reward tokens to the handler’s address. Then, the tokens are iterated through and sent to the harvester to be swapped from `ConvexPositionHandler` by getting their list from `harvester.rewardTokens()` and calling `harvester.harvest()`


**code/contracts/ConvexExecutor/ConvexPositionHandler.sol:L274-L290**



```
// get list of tokens to transfer to harvester
address[] memory rewardTokens = harvester.rewardTokens();
//transfer them
uint256 balance;
for (uint256 i = 0; i < rewardTokens.length; i++) {
    balance = IERC20(rewardTokens[i]).balanceOf(address(this));

    if (balance > 0) {
        IERC20(rewardTokens[i]).safeTransfer(
            address(harvester),
            balance
        );
    }
}

// convert all rewards to WETH
harvester.harvest();

```
However, `harvester.rewardTokens()` doesn’t have the LDO token’s address in its list, so they will not be transferred to the harvester to be swapped.


**code/contracts/ConvexExecutor/Harvester.sol:L77-L82**



```
function rewardTokens() external pure override returns (address[] memory) {
    address[] memory rewards = new address[](2);
    rewards[0] = address(crv);
    rewards[1] = address(cvx);
    return rewards;
}

```
As a result, `harvester.harvest()` will not be able to execute its `_swapLidoForWETH()` function since its `ldoBalance` will be 0. This results in missed rewards and therefore yield for the vault as part of its normal flow.


There is a possible mitigation in the current state of the contract that would require governance to call `sweep()` on the LDO balance from the `BaseTradeExecutor` contract (that `ConvexPositionHandler` inherits) and then transferring those LDO tokens to the harvester contract to perform the swap at a later rewards claim. This, however, requires transactions separate from the intended flow of the system as well as governance intervention.


#### Recommendation


Add the LDO token address to the `rewardTokens()` function by adding the following line
`rewards[2] = address(ldo);`

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Brahma Fi |
| Report Date | N/A |
| Finders |  George Kobakhidze
, David Oz Kashi,  Sergii Kravchenko |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2022/05/brahma-fi/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


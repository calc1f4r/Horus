---
# Core Classification
protocol: Tapioca DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27529
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-07-tapioca
source_link: https://code4rena.com/reports/2023-07-tapioca
github_link: https://github.com/code-423n4/2023-07-tapioca-findings/issues/990

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - carrotsmuggler
  - kaden
  - ladboy233
  - Vagner
  - 0xfuje
---

## Vulnerability Title

[H-39] `AaveStrategy.sol`: Changing swapper breaks the contract

### Overview


A bug has been discovered in the `AaveStrategy.sol` contract which manages wETH tokens and deposits them into the Aave lending pool to collect rewards, which are then swapped into WETH again. This process is done in the `compound` function. The swapper contract needs to be given approval to use the tokens stored in the strategy contract, however the `setMultiSwapper` function does not give approval to the new swapper contract when it is changed, making the swappers dysfunctional. This is classified as a high severity issue.

The bug is due to the absence of `approve` calls in the `setMultiSwapper` function, which can be seen from the implementation of the function. To mitigate this issue, the `setMultiSwapper` function should remove approval from the old swapper and add approval to the new swapper. The same function has the proper implementation in the `ConvexTricryptoStrategy.sol` contract which can be used here as well.

### Original Finding Content


The contract `AaveStrategy.sol` manages wETH tokens and deposits them to the aave lending pool, and collects rewards. These rewards are then swapped into WETH again to compound on the WETH being managed by the contract. this is done in the `compound` function.

```solidity
uint256 calcAmount = swapper.getOutputAmount(swapData, "");
uint256 minAmount = calcAmount - (calcAmount * 50) / 10_000; //0.5%
swapper.swap(swapData, minAmount, address(this), "");
```

To carry out these operations, the swapper contract needs to be given approval to use the tokens being stored in the strategy contract. This is required since the swapper contract calls transferFrom on the tokens to pull it out of the strategy contract. This allowance is set in the constructor.

```solidity
rewardToken.approve(_multiSwapper, type(uint256).max);
```

The issue arises when the swapper contract is changed. The change is done via the `setMultiSwapper` function. This function however does not give approval to the new swapper contract. Thus if the swapper is upgraded/changed, the approval is not transferred to the new swapper contract, which makes the swappers dysfunctional.

Since the swapper is critical to the system, and `compound` is called before withdrawals, a broken swapper will break the withdraw functionality of the contract. Thus this is classified as a high severity issue.

### Proof of Concept

The bug is due to the absence of `approve` calls in the `setMultiSwapper` function. This can be seen from the implementation of the function.

```solidity
function setMultiSwapper(address _swapper) external onlyOwner {
        emit MultiSwapper(address(swapper), _swapper);
        swapper = ISwapper(_swapper);
    }
```
### Recommended Mitigation Steps

In the `setMultiSwapper` function, remove approval from the old swapper and add approval to the new swapper. The same function has the proper implementation in the `ConvexTricryptoStrategy.sol` contract which can be used here as well.

```solidity
function setMultiSwapper(address _swapper) external onlyOwner {
    emit MultiSwapper(address(swapper), _swapper);
    rewardToken.approve(address(swapper), 0);
    swapper = ISwapper(_swapper);
    rewardToken.approve(_swapper, type(uint256).max);
}
```

**[0xRektora (Tapioca) confirmed via duplicate issue 222](https://github.com/code-423n4/2023-07-tapioca-findings/issues/222)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Tapioca DAO |
| Report Date | N/A |
| Finders | carrotsmuggler, kaden, ladboy233, Vagner, 0xfuje, rvierdiiev |

### Source Links

- **Source**: https://code4rena.com/reports/2023-07-tapioca
- **GitHub**: https://github.com/code-423n4/2023-07-tapioca-findings/issues/990
- **Contest**: https://code4rena.com/reports/2023-07-tapioca

### Keywords for Search

`vulnerability`


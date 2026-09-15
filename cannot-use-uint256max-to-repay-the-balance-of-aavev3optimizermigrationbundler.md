---
# Core Classification
protocol: Morpho
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40863
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/c8366258-22bd-4e11-a6e9-c39ce06539ad
source_link: https://cdn.cantina.xyz/reports/cantina_competition_morpho_metamorpho_dec2023.pdf
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
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Christoph Michel
  - J4X98
---

## Vulnerability Title

Cannot use uint256.max to repay the balance of aavev3optimizermigrationbundler 

### Overview


The bug report is about an issue with the AaveV3OptimizerMigrationBundler contract. The problem is that when trying to repay the bundler's underlying balance by passing the maximum value, it does not work. This is because the code caps the amount to be repaid to the entire borrow balance, not just the bundler's balance. This means that if a user tries to migrate part of their position by repaying half of their borrow balance, the batch will fail because the bundler only has half of the assets. The recommendation is to always cap the amount to the bundler's balance to prevent this issue.

### Original Finding Content

## AaveV3OptimizerMigrationBundler.sol #L37

## Description
The `aaveV3OptimizerRepay`'s natspec states the following for the amount parameter:

> The amount of underlying to repay. Pass `type(uint256).max` to repay the bundler's underlying.

Passing `type(uint256).max` to repay the bundler's underlying balance does not work. Note that if `amount == type(uint256).max`, this value is not adjusted and just forwarded to the `AAVE_V3_OPTIMIZER.repay` call.

The `AaveV3Optimizer` will forward the calls to Morpho's `PositionManager`, which executes:

```solidity
// AaveV3Optimizer
function _repay(address underlying, uint256 amount, address from, address onBehalf) internal returns (uint256) {
    bytes memory returnData = _positionsManager.functionDelegateCall(
        abi.encodeCall(IPositionsManager.repayLogic, (underlying, amount, from, onBehalf))
    );
    return (abi.decode(returnData, (uint256)));
}
```

```solidity
// PositionManager
function repayLogic(address underlying, uint256 amount, address repayer, address onBehalf) external returns (uint256) {
    amount = Math.min(_getUserBorrowBalanceFromIndexes(underlying, onBehalf, indexes), amount);
}
```

This caps the amount to be repaid to the entire borrow balance, not to the bundler's balance. The call will revert as it tries to repay the entire borrow balance with the bundler's balance.

## Example
A user tries to migrate part of their position by attempting to repay half of their borrow balance of 1000 assets. The first action in the bundle redeems shares from another protocol to receive the desired repay amount of roughly 500 assets, and the second action is to repay by setting `assets = type(uint256).max` to "repay the bundler's asset balance," as defined by the natspec. The batch will revert as `AaveV3Optimizer` will try to repay the entire borrow balance of 1000, but the bundler only has 500 assets.

## Recommendation
Consider always capping the amount to the bundler's balance. Trying to repay more will never work, and the protocol itself will already cap it to the entire borrow balance:

```solidity
if (amount != type(uint256).max) 
    amount = Math.min(amount, ERC20(underlying).balanceOf(address(this)));
```

```solidity
amount = Math.min(amount, ERC20(underlying).balanceOf(address(this)));
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | Christoph Michel, J4X98 |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_morpho_metamorpho_dec2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/c8366258-22bd-4e11-a6e9-c39ce06539ad

### Keywords for Search

`vulnerability`


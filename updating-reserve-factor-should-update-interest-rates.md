---
# Core Classification
protocol: Cod3x lend
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49184
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Cod3x-Spearbit-Security-Review-December-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Cod3x-Spearbit-Security-Review-December-2024.pdf
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
finders_count: 3
finders:
  - Saw-mon and Natalie
  - Cergyk
  - Jonatas Martins
---

## Vulnerability Title

Updating reserve factor should update interest rates

### Overview


This bug report discusses a medium risk issue in the LendingPoolConfigurator and MiniPoolConfigurator smart contracts. The issue involves the reserve factor, which is the percentage of borrow interest that goes to the protocol's reserve. The bug allows the reserve factor to be changed without updating the interest rates, potentially leading to insolvency for lenders. The report recommends implementing a function to update the pool when changing the reserve factors. The issue has been fixed in a recent commit.

### Original Finding Content

## Severity: Medium Risk

## Context
- LendingPoolConfigurator.sol#L443-L455
- MiniPoolConfigurator.sol#L167-L178
- MiniPoolConfigurator.sol#L463-L474

## Description
The reserve factor is the percentage of borrow interest attributed to the protocol (goes to reserve). It directly influences the ratio between borrow rate and liquidity rate, as can be seen in the `getLiquidityRate` implementation:

```solidity
// BasePiReserveRateStrategy.sol#L291-L299
function getLiquidityRate(
    uint256 currentVariableBorrowRate,
    uint256 utilizationRate,
    uint256 reserveFactor
) internal pure returns (uint256) {
    return currentVariableBorrowRate.rayMul(utilizationRate).percentMul(
        PercentageMath.PERCENTAGE_FACTOR - reserveFactor // <<<
    );
}
```

It can be changed directly by the admin by calling `setCod3xReserveFactor`:

```solidity
// LendingPoolConfigurator.sol#L443-L455
function setCod3xReserveFactor(address asset, bool reserveType, uint256 reserveFactor)
    external
    onlyPoolAdmin
{
    DataTypes.ReserveConfigurationMap memory currentConfig =
        pool.getConfiguration(asset, reserveType);
    currentConfig.setCod3xReserveFactor(reserveFactor);
    pool.setConfiguration(asset, reserveType, currentConfig.data);
    emit ReserveFactorChanged(asset, reserveType, reserveFactor);
}
```

However, since calling this function does not update interest rates, this could lead to insolvency towards lenders in the case where the reserve factor is increased.

Indeed, during the next accrual, the current liquidity rate will be applied to the liquidity index, and at the same time, the new reserve factor will be taken out of accrued borrow interest:

```solidity
// ReserveLogic.sol#L284-L304
function _updateIndexes(
    DataTypes.ReserveData storage reserve,
    uint256 scaledVariableDebt,
    uint256 liquidityIndex,
    uint256 variableBorrowIndex,
    uint40 timestamp
) internal returns (uint256, uint256) {
    uint256 currentLiquidityRate = reserve.currentLiquidityRate;
    uint256 newLiquidityIndex = liquidityIndex;
    uint256 newVariableBorrowIndex = variableBorrowIndex;
    
    // Only cumulating if there is any income being produced.
    if (currentLiquidityRate != 0) {
        uint256 cumulatedLiquidityInterest =
            MathUtils.calculateLinearInterest(currentLiquidityRate, timestamp);
        newLiquidityIndex = cumulatedLiquidityInterest.rayMul(liquidityIndex);
        require(newLiquidityIndex <= type(uint128).max, Errors.RL_LIQUIDITY_INDEX_OVERFLOW);
        reserve.liquidityIndex = uint128(newLiquidityIndex);
    }
    // ...
}
```

```solidity
// MiniPoolReserveLogic.sol#L251-L269
function _mintToTreasury(
    DataTypes.MiniPoolReserveData storage reserve,
    uint256 scaledVariableDebt,
    uint256 previousVariableBorrowIndex,
    uint256 newLiquidityIndex,
    uint256 newVariableBorrowIndex,
    uint40
) internal {
    MintToTreasuryLocalVars memory vars;
    vars.cod3xReserveFactor = reserve.configuration.getCod3xReserveFactor(); // <<<
    vars.minipoolOwnerReserveFactor = reserve.configuration.getMinipoolOwnerReserveFactor();
    if (vars.cod3xReserveFactor == 0 && vars.minipoolOwnerReserveFactor == 0) {
        return;
    }
    // Calculate the last principal variable debt.
    vars.previousVariableDebt = scaledVariableDebt.rayMul(previousVariableBorrowIndex);
    // ...
}
```

## Recommendation
The pool should be touched when updating reserve factors (Cod3x and MinipoolOwner):

```solidity
// LendingPoolConfigurator.sol#L443-L455
function setCod3xReserveFactor(address asset, bool reserveType, uint256 reserveFactor)
    external
    onlyPoolAdmin
{
    //@audit please note that this function needs to be implemented, because there is no endpoint
    // which can be called with zero amount!
    pool.updateState();

    DataTypes.ReserveConfigurationMap memory currentConfig =
        pool.getConfiguration(asset, reserveType);
    currentConfig.setCod3xReserveFactor(reserveFactor);
    pool.setConfiguration(asset, reserveType, currentConfig.data);
    emit ReserveFactorChanged(asset, reserveType, reserveFactor);
}
```

- Cod3x: Fixed in commit 4bbb4351.
- Spearbit: Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Cod3x lend |
| Report Date | N/A |
| Finders | Saw-mon and Natalie, Cergyk, Jonatas Martins |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Cod3x-Spearbit-Security-Review-December-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Cod3x-Spearbit-Security-Review-December-2024.pdf

### Keywords for Search

`vulnerability`


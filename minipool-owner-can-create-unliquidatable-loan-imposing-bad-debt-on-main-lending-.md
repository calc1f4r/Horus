---
# Core Classification
protocol: Astera
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62293
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astera-Spearbit-Security-Review-December-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astera-Spearbit-Security-Review-December-2024.pdf
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

Minipool owner can create unliquidatable loan, imposing bad debt on main lending pool

### Overview


This bug report discusses a medium risk severity issue in the MiniPoolConfigurator.sol code. The bug can be exploited if the owner of a mini pool is different from the main pool admin and the mini pool has some borrowing capacity from the main lending pool. The bug allows the mini pool owner to create an unliquidatable loan, causing bad debt for the main lending pool. This can be achieved by deactivating the reserve associated with the collateral of the loan. The report suggests a more robust check on the supply of the asset to prevent this issue. The bug has been fixed in the code and verified by Spearbit.

### Original Finding Content

## Medium Risk Severity Report

## Context
MiniPoolConfigurator.sol#L481-L490

## Description
In the scenario where the minipool owner is not the same entity as the main pool admin, and the minipool has some borrowing capacity from the main lending pool (available flow), the minipool owner can create an unliquidatable loan, forcing bad debt upon the main lending pool. 

Note that initially, the main lending pool owner and minipool owners should be the same entity. The risk reported here would be impactful with the decentralization of minipool ownership in the future.

To achieve this, the minipool owner can simply deactivate the reserve associated with the collateral of their loan. This is possible due to a flawed `_checkNoLiquidity` function for deactivating reserves:

```solidity
function _checkNoLiquidity(address asset, IMiniPool pool) internal view {
    DataTypes.MiniPoolReserveData memory reserveData = pool.getReserveData(asset);
    uint256 availableLiquidity = IERC20Detailed(asset).balanceOf(reserveData.aTokenAddress); 
    require(
        availableLiquidity == 0 && reserveData.currentLiquidityRate == 0,
        Errors.LPC_RESERVE_LIQUIDITY_NOT_0
    );
}
```

## Scenario
Let's examine the concrete way of creating an unliquidatable loan:

### Parameters
| Parameter         | Value          |
|-------------------|----------------|
| Collateral         | aWETH         |
| Debt               | aUSDC         |
| Available flow     | 500k aUSDC    |
| aUSDC Liquidity    | 0              |
| aWETH LTV          | 1.2            |

### Steps
- Alice, the minipool owner, deposits $600k of WETH into the minipool and borrows $500k USDC, using all available flow.
- Alice flashloans all of WETH out of the ERC6909 market, enabling the deactivation of the reserve because `_checkNoLiquidity` allows it.

## Recommendation
A more robust check could be made on the supply of the asset:

```solidity
function _checkNoLiquidity(address asset, IMiniPool pool) internal view {
    DataTypes.MiniPoolReserveData memory reserveData = pool.getReserveData(asset);
    uint256 availableLiquidity = IERC6909(reserveData.aTokenAddress).scaledTotalSupply();
    require(
        availableLiquidity == 0 && reserveData.currentLiquidityRate == 0,
        Errors.LPC_RESERVE_LIQUIDITY_NOT_0
    );
}
```

## Notes
- **Astera:** Fixed in commit df0b9abf.
- **Spearbit:** Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Astera |
| Report Date | N/A |
| Finders | Saw-mon and Natalie, Cergyk, Jonatas Martins |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astera-Spearbit-Security-Review-December-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astera-Spearbit-Security-Review-December-2024.pdf

### Keywords for Search

`vulnerability`


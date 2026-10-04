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
solodit_id: 62296
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

Mini pool reserves for unique tokens can be reinitialised

### Overview


This bug report discusses a medium risk issue in the Mini Pool Reserve feature. The problem occurs when unique tokens are added to the ATokenERC6909 multiple times with different incremental IDs. This causes the liquidity and variable borrow indexes to be reset, user accounting to be lost, and potential issues with stateful interest rate models. The report recommends restructuring the mini pool to prevent this issue and mentions that it has been fixed in a recent commit. A third party has also verified the fix.

### Original Finding Content

## Severity: Medium Risk

## Context
(No context files were provided by the reviewer)

## Description
Mini pool reserves can be reinitialized. This is due to the following factors:

1. For unique tokens, one can add them to `ATokenERC6909` multiple times but with different incremental IDs.

2. In `MiniPoolReserveLogic`, we have:

```solidity
function init(
    DataTypes.MiniPoolReserveData storage reserve,
    address asset,
    IAERC6909 aTokenAddress,
    uint256 aTokenID,
    uint256 variableDebtTokenID,
    address interestRateStrategyAddress
) internal {
    require(
        aTokenAddress.getUnderlyingAsset(aTokenID) == asset, // this just checks to make sure the
        `asset` has been added in `aTokenAddress`, !
        Errors.RL_RESERVE_ALREADY_INITIALIZED
    );
    reserve.liquidityIndex = uint128(WadRayMath.ray());
    reserve.variableBorrowIndex = uint128(WadRayMath.ray());
    reserve.aTokenAddress = address(aTokenAddress);
    reserve.aTokenID = aTokenID;
    reserve.variableDebtTokenID = variableDebtTokenID;
    reserve.interestRateStrategyAddress = interestRateStrategyAddress;
}
```

This will cause:

1. `liquidityIndex` and `variableBorrowIndex` to be reset.
2. `aTokenID` and `variableDebtTokenID` to be updated, thus all user accounting will be lost.
3. `interestRateStrategyAddress` to be updated, which for stateful IRMs can cause an issue.

## Recommendation
1. Make sure there is only one reserve per unique token, just like the non-rebasing AToken of the main lending pool.

2. The mini pool needs to be restructured so that adding a unique token multiple times would not override the reserve of the previously added unique token.

## Astera
Fixed in commit b46b15a3.

## Spearbit
Fix verified.

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


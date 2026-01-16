---
# Core Classification
protocol: Morpho
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6902
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/MorphoV1-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/MorphoV1-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - validation

protocol_categories:
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - EBaizel
  - JayJonah8
  - Christoph Michel
  - Datapunk
  - Emanuele Ricci
---

## Vulnerability Title

setIsPausedForAllMarkets bypass the check done in setIsBorrowPaused and allow resuming borrow on a deprecated market

### Overview


The bug report is about a vulnerability in the MorphoGovernance contract that allows Morpho to set the isBorrowPaused to false even if the market is deprecated. This is because the check is not enforced by the _setPauseStatus function, which is called by setIsPausedForAllMarkets. To reproduce the issue, a test was created using the TestSetup contract. The recommendation for a fix was to follow the same approach implemented in the aave-v3 codebase, which only updates the isBorrowPaused if the market is not deprecated. Morpho fixed the issue in PR 1642 and Spearbit verified it.

### Original Finding Content

## Medium Risk Vulnerability Report

## Severity
**Medium Risk**

## Context
- `aave-v2/MorphoGovernance.sol#L470`
- `compound/MorphoGovernance.sol#L470`

## Description
The `MorphoGovernance` contract allows Morpho to set the `isBorrowPaused` to `false` only if the market is not deprecated.

```solidity
function setIsBorrowPaused(address _poolToken, bool _isPaused) external onlyOwner isMarketCreated(_poolToken) {
    if (!_isPaused && marketPauseStatus[_poolToken].isDeprecated) revert MarketIsDeprecated();
    marketPauseStatus[_poolToken].isBorrowPaused = _isPaused;
    emit IsBorrowPausedSet(_poolToken, _isPaused);
}
```

This check is not enforced by the `_setPauseStatus` function, which is called by `setIsPausedForAllMarkets`, allowing Morpho to resume borrowing for deprecated markets.

## Test to Reproduce the Issue
```solidity
// SPDX-License-Identifier: AGPL-3.0-only
pragma solidity ^0.8.0;

import "./setup/TestSetup.sol";

contract TestSpearbit is TestSetup {
    using WadRayMath for uint256;

    function testBorrowPauseCheckSkipped() public {
        // Deprecate a market
        morpho.setIsBorrowPaused(aDai, true);
        morpho.setIsDeprecated(aDai, true);
        checkPauseEquality(aDai, true, true);
        
        // you cannot resume borrowing if the market is deprecated
        hevm.expectRevert(abi.encodeWithSignature("MarketIsDeprecated()"));
        morpho.setIsBorrowPaused(aDai, false);
        checkPauseEquality(aDai, true, true);
        
        // but this check is skipped if I call directly `setIsPausedForAllMarkets `
        morpho.setIsPausedForAllMarkets(false);
        
        // this should revert because you cannot resume borrowing for a deprecated market
        checkPauseEquality(aDai, false, true);
    }

    function checkPauseEquality(
        address aToken,
        bool shouldBePaused,
        bool shouldBeDeprecated
    ) public {
        (
            bool isSupplyPaused,
            bool isBorrowPaused,
            bool isWithdrawPaused,
            bool isRepayPaused,
            bool isLiquidateCollateralPaused,
            bool isLiquidateBorrowPaused,
            bool isDeprecated
        ) = morpho.marketPauseStatus(aToken);
        
        assertEq(isBorrowPaused, shouldBePaused);
        assertEq(isDeprecated, shouldBeDeprecated);
    }
}
```

## Recommendation
One possible solution is to follow the same approach implemented in the Aave V3 codebase. The update of the `isBorrowPaused` must only occur if the market is not deprecated.

## Morpho
This issue has been fixed in PR 1642.

## Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | EBaizel, JayJonah8, Christoph Michel, Datapunk, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/MorphoV1-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/MorphoV1-Spearbit-Security-Review.pdf

### Keywords for Search

`Validation`


---
# Core Classification
protocol: Morpho
chain: everychain
category: logic
vulnerability_type: pause

# Attack Vector Details
attack_type: pause
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6901
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
  - pause
  - business_logic

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

A market could be deprecated but still prevent liquidators to liquidate borrowers if isLiquidateBorrowPaused istrue

### Overview


This bug report is about the MorphoGovernance.sol code in the aave-v2 and compound projects. The code is designed to prevent the deprecation of a market unless borrowing has been paused. However, the same check should also be done for isLiquidateBorrowPaused, to ensure that liquidators cannot liquidate borrowers on a deprecated market. The recommendation is to prevent deprecation of a market if isLiquidateBorrowPaused is set to true, and also to check the isDeprecated flag in setIsLiquidateBorrowPaused to prevent pausing liquidation if the market is deprecated. Morpho acknowledges the issue and has decided to leave things as they are, as there may be an issue with the liquidation borrow that the operator is not aware of. Spearbit has acknowledged this.

### Original Finding Content

## Severity: Medium Risk

## Context 
- aave-v2/MorphoGovernance.sol#L358-L366 
- compound/MorphoGovernance.sol#L368-L376 

## Description 
Currently, when a market must be deprecated, Morpho checks that borrowing has been paused before applying the new value for the flag.

```solidity
function setIsDeprecated(address _poolToken, bool _isDeprecated)
external
onlyOwner
isMarketCreated(_poolToken)
{
    if (!marketPauseStatus[_poolToken].isBorrowPaused) revert BorrowNotPaused();
    marketPauseStatus[_poolToken].isDeprecated = _isDeprecated;
    emit IsDeprecatedSet(_poolToken, _isDeprecated);
}
```

The same check should be done in `isLiquidateBorrowPaused`, allowing the deprecation of a market only if `isLiquidateBorrowPaused == false`, otherwise liquidators would not be able to liquidate borrowers on a deprecated market.

## Recommendation 
Prevent the deprecation of a market if the `isLiquidateBorrowPaused` flag is set to true. Consider also checking the `isDeprecated` flag in the `setIsLiquidateBorrowPaused` to prevent pausing the liquidation if the market is deprecated. If Morpho implements the specific behavior, it should also be aware of the issue described in "setIsPausedForAllMarkets" bypassing the check done in `setIsBorrowPaused` and allowing resuming borrow on a deprecated market.

## Morpho 
We acknowledge this issue. The reason behind this is the following: given what @MathisGD said, if we want to be consistent, we should prevent pausing the liquidation borrow on a deprecated asset. However, there might be an issue (we don't know) with the liquidation borrow, and the operator would not be able to pause it. For this reason, we prefer to leave things as it is.

## Spearbit 
Acknowledged.

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

`Pause, Business Logic`


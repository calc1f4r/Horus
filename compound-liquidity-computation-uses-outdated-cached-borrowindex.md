---
# Core Classification
protocol: Morpho
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6914
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

Compound liquidity computation uses outdated cached borrowIndex

### Overview


This bug report concerns MorphoUtils.sol#L211 in the Compound/MorphoUtils codebase. The issue is that the _isLiquidatable function iterates over all user-entered markets and calls _getUserLiquidity-DataForAsset(poolToken), but only updates the indexes of markets that correspond to the borrow and collateral assets. This means that Morpho's liquidation procedure may not match Compound's liquidation procedure, and users may not be liquidated on Morpho that could be liquidated on Compound. 

The recommendation to fix this issue is to consider using Compound's borrowIndex, which may have been updated after Morpho updated its internal indexes. This would match Compound's liquidation procedure. The fix was implemented in PR 1558 and verified by Spearbit.

### Original Finding Content

## Severity: Medium Risk

## Context
`compound/MorphoUtils.sol#L211`

## Description
The `_isLiquidatable` function iterates over all user-entered markets and calls `_getUserLiquidityDataForAsset(poolToken)` followed by `_getUserBorrowBalanceInOf(poolToken)`. However, it only updates the indexes of markets that correspond to the borrow and collateral assets. The `_getUserBorrowBalanceInOf` function computes the underlying pool amount of the user as:

```
userBorrowBalance.onPool.mul(lastPoolIndexes[_poolToken].lastBorrowPoolIndex);
```

Note that `lastPoolIndexes[_poolToken].lastBorrowPoolIndex` is a value that was cached by Morpho and it can be outdated if there has not been a user interaction with that market for a long time.

The liquidation does not match Compound's liquidation anymore, and users might not be liquidated on Morpho that could be liquidated on Compound. Liquidators would first need to trigger updates to Morpho's internal borrow indexes.

## Recommendation
To match Compound's liquidation procedure, consider using Compound's `borrowIndex`, which might have been updated after Morpho updated its own internal indexes.

### Function Code
```solidity
function _getUserBorrowBalanceInOf(address _poolToken, address _user)
    internal
    view
    returns (uint256)
{
    Types.BorrowBalance memory userBorrowBalance = borrowBalanceInOf[_poolToken][_user];
    return
        userBorrowBalance.inP2P.mul(p2pBorrowIndex[_poolToken]) +
        userBorrowBalance.onPool.mul(lastPoolIndexes[_poolToken].lastBorrowPoolIndex);
    // Changed to:
    // userBorrowBalance.onPool.mul(ICToken(_poolToken).borrowIndex());
}
```

## Morpho
Fixed in PR 1558.

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

`Business Logic`


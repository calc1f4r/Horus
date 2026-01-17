---
# Core Classification
protocol: Connext
chain: everychain
category: uncategorized
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7237
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - wrong_math
  - decimals

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0xLeastwood
  - Jonah1005
---

## Vulnerability Title

_slippageTol does not adjust for decimal differences

### Overview


This bug report is about an issue with the AssetLogic.sol#L273 in the AssetLogic library. It states that when users set the slippage tolerance in percentage, the assetLogic calculates a minReceived value with the wrong amount. This leads to users either always hitting the slippage or suffering huge slippage when the assetIn and assetOut have different number of decimals. For example, if the number of decimals of assetIn is 6 and the decimal of assetOut is 18, the minReceived value will be set to 10ˆ-12 smaller than the correct value, making users vulnerable to sandwich attacks. On the other hand, if the number of decimals of assetIn is 18 and the number of decimals of assetOut is 6, the minReceived will be set to 10ˆ12 larger than the correct value, causing the cross-chain transfer to get stuck.

The recommendation is to adjust the value with swapStorage.tokenPrecisionMultipliers for internal swap and according to token.decimals for external swap. This issue has been solved in PR 1574 and has been verified by Spearbit.

### Original Finding Content

## Vulnerability Report

## Severity
**Medium Risk**

## Context
AssetLogic.sol#L273

## Description
Users set the slippage tolerance in percentage. The `assetLogic` calculates:

```
minReceived = (_amount * _slippageTol) / s.LIQUIDITY_FEE_DENOMINATOR
```

Then `assetLogic` uses `minReceived` in the swap functions. However, the `minReceived` does not adjust for the decimal differences between `assetIn` and `assetOut`. Users will either always hit the slippage or suffer huge slippage when `assetIn` and `assetOut` have a different number of decimals.

Assume the number of decimals of `assetIn` is 6 and the number of decimals of `assetOut` is 18. The `minReceived` will be set to `10^-12` smaller than the correct value. Users would be vulnerable to sandwich attacks in this case. 

Alternatively, if the number of decimals of `assetIn` is 18 and the number of decimals of `assetOut` is 6, the `minReceived` will be set to `10^12` larger than the correct value. Users would always hit the slippage, and the cross-chain transfer will get stuck.

### Code Snippet
```solidity
library AssetLogic {
    function _swapAsset(... ) ... {
        // Swap the asset to the proper local asset
        uint256 minReceived = (_amount * _slippageTol) / s.LIQUIDITY_FEE_DENOMINATOR;
        ...
        return (pool.swapExact(_amount, _assetIn, _assetOut, minReceived), _assetOut);
        ...
    }
}
```

## Recommendation
Recommend to adjust the value with `swapStorage.tokenPrecisionMultipliers` for internal swap. For the external swap, the value should be adjusted according to `token.decimals`.

## Connext
Solved in PR 1574.

## Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Spearbit |
| Protocol | Connext |
| Report Date | N/A |
| Finders | 0xLeastwood, Jonah1005 |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf

### Keywords for Search

`Wrong Math, Decimals`


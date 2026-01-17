---
# Core Classification
protocol: ZeroLend One
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41836
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/466
source_link: none
github_link: https://github.com/sherlock-audit/2024-06-new-scope-judging/issues/488

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
  - lending
  - oracle

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Obsidian
  - ether\_sky
  - dany.armstrong90
---

## Vulnerability Title

M-15: The repayment process in the NFTPositionManager can sometimes be reverted

### Overview


The NFTPositionManager has a bug where the repayment process can sometimes be reversed. This means that users who supply assets to the pools to earn rewards in zero tokens may have their repayments fail due to a small rounding error. This can cause a denial-of-service situation where repayments fail. The bug was found by Obsidian, dany.armstrong90, and ether_sky. The code for the conversion between shares and assets is causing the issue and needs to be adjusted to allow for a small mismatch to prevent unnecessary reversions. The recommendation is to either remove the check or adjust it to allow for a 1 wei mismatch. The bug was found through manual review and can occur with various combinations of borrow index, share amounts, and repaid assets.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-06-new-scope-judging/issues/488 

## Found by 
Obsidian, dany.armstrong90, ether\_sky
## Summary
Users can `supply` `assets` to the `pools` through the `NFTPositionManager` to earn `rewards` in  `zero` tokens. 
Functions like `deposit`, `withdraw`, `repay`, and `borrow` should operate normally. 
However, due to an additional check, `repayments` might be reverted.
## Vulnerability Detail
Here's the relationship between `shares` (`s`) and `assets` (`a`) in the `Pool`:
-  **Share to Asset Conversion:**
   `a = [(s * I + 10^27 / 2) / 10^27] (rayMul)`
```solidity
function rayMul(uint256 a, uint256 b) internal pure returns (uint256 c) {
  assembly {
    if iszero(or(iszero(b), iszero(gt(a, div(sub(not(0), HALF_RAY), b))))) { revert(0, 0) }
    c := div(add(mul(a, b), HALF_RAY), RAY)
  }
}
```
- **Asset to Share Conversion:**
    `s = [(a * 10^27 + I / 2) / I] (rayDiv)`
```solidity
function rayDiv(uint256 a, uint256 b) internal pure returns (uint256 c) {
  assembly {
    if or(iszero(b), iszero(iszero(gt(a, div(sub(not(0), div(b, 2)), RAY))))) { revert(0, 0) }
    c := div(add(mul(a, RAY), div(b, 2)), b)
  }
}
```

**Numerical Example:**
Suppose there is a `pool` `P` where users `borrow` `assets` `A` using the `NFTPositionManager`.
- The current `borrow index` of `P` is `2 * 10^27`, and the `share` is `5`.
- The `previous debt balance` is as below (`Line 119`):
    `previousDebtBalance = [(s * I + 10^27 / 2) / 10 ^27] = [(5 * 2 * 10^27 + 10^27 / 2) / 10^27] = 10`
- If we are going to `repay` `3` `assets`:
    - The removed `shares` is:
        `[(a * 10^27 + I / 2) / I] = [(3 * 10^27 + 2 * 10^27 / 2) / (2 * 10^27)] = 2`
    - Therefore, the remaining `share` is:
        `5 - 2 = 3`
- The `current debt balance` is as below  (`Line 121`):
    `currentDebtBalance = [(s * I + 10^27 / 2) / 10 ^27] = [(3 * 2 * 10^27 + 10^27 / 2) / 10^27 = 6`
Then in `line 123`, `previousDebtBalance - currentDebtBalance` would be `4` and `repaid.assets` is `3`.
As a result, the `repayment` would be reverted.
```solidity
function _repay(AssetOperationParams memory params) internal nonReentrant {
119:  uint256 previousDebtBalance = pool.getDebt(params.asset, address(this), params.tokenId);

  DataTypes.SharesType memory repaid = pool.repay(params.asset, params.amount, params.tokenId, params.data);

121:  uint256 currentDebtBalance = pool.getDebt(params.asset, address(this), params.tokenId);
  
123:  if (previousDebtBalance - currentDebtBalance != repaid.assets) {
    revert NFTErrorsLib.BalanceMisMatch();
  }
}
```
This example demonstrates a `potential 1 wei mismatch` between `previousDebtBalance` and `currentDebtBalance` due to rounding in the calculations.
## Impact
This check seems to cause a `denial-of-service (DoS)` situation where `repayments` can fail due to small rounding errors. 
This issue can occur with various combinations of `borrow index`, `share amounts`, and `repaid assets`.
## Code Snippet
https://github.com/sherlock-audit/2024-06-new-scope/blob/c8300e73f4d751796daad3dadbae4d11072b3d79/zerolend-one/contracts/core/pool/utils/WadRayMath.sol#L77
https://github.com/sherlock-audit/2024-06-new-scope/blob/c8300e73f4d751796daad3dadbae4d11072b3d79/zerolend-one/contracts/core/pool/utils/WadRayMath.sol#L93
https://github.com/sherlock-audit/2024-06-new-scope/blob/c8300e73f4d751796daad3dadbae4d11072b3d79/zerolend-one/contracts/core/positions/NFTPositionManagerSetters.sol#L119-L125
## Tool used

Manual Review

## Recommendation
Either remove this check or adjust it to allow a `1 wei mismatch` to prevent unnecessary reversion of `repayments`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | ZeroLend One |
| Report Date | N/A |
| Finders | Obsidian, ether\_sky, dany.armstrong90 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-06-new-scope-judging/issues/488
- **Contest**: https://app.sherlock.xyz/audits/contests/466

### Keywords for Search

`vulnerability`


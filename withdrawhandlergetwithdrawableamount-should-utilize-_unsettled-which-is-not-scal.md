---
# Core Classification
protocol: DESK
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53112
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/5c335680-b1a3-4d45-8948-bcc18c53a6f3
source_link: https://cdn.cantina.xyz/reports/cantina_competition_hmx_january2025.pdf
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
finders_count: 2
finders:
  - trachev
  - KupiaSec
---

## Vulnerability Title

WithdrawHandler.getWithdrawableAmount() should utilize _unsettled, which is not scaled by the collateral factor 

### Overview


This bug report discusses an issue where the withdrawable amount for users is being miscalculated due to the collateral factor being applied during the withdrawal process. This results in users being unable to access the full amount they are entitled to, leading to locked funds. The report recommends that the function responsible for calculating the withdrawable amount should not use the collateral factor and instead use the unsettled amount that is not scaled by the collateral factor. This issue has a high impact as it prevents users from fully withdrawing their funds and has a high likelihood of occurring whenever withdrawals are processed. 

### Original Finding Content

## Issue Summary

## Context
(No context files were provided by the reviewer)

## Summary
When withdrawing `settlementToken`, the `getWithdrawableAmount()` function calculates the maximum withdrawable amount using the formula `collaterals + _unsettled`, where `collaterals` is the recorded state value in `AssetService`, and `_unsettled` includes values from PnL and lending/borrowing fees. The issue is that `_unsettled` is scaled by the collateral factor. The collateral factor should only be applied when checking the health factor, not during the withdrawal process. As a result, the withdrawable amount is miscalculated, preventing withdrawers from accessing the full amount they are entitled to, leading to locked funds.

## Finding Description
The `WithdrawHandler.getWithdrawableAmount()` function accounts for `_unsettled`. `_unsettled` is the sum of PnL and lending/borrowing fees, representing the amount the account should receive from or pay to the protocol. This value is calculated by the `_getSubaccountUnsettledE18()` function, as seen at line 96.

```solidity
function getWithdrawableAmount(bytes32 _subaccount, address _tokenAddress) public view returns (uint256 _amount) {
    IAssetService _assetService = IAssetService(assetService);
    int256 _subaccountTotalBalance = _assetService.collaterals(_subaccount, _tokenAddress);
    address _settlementToken = _assetService.settlementToken();
    
    if (_tokenAddress == _settlementToken) {
        uint256 _decimals = _assetService.collateralTokenDecimals(_settlementToken);
        int256 _unsettled = _getSubaccountUnsettledE18(_subaccount) / int256(10 ** (18 - _decimals));
        
        if (_unsettled > 0) {
            _subaccountTotalBalance += _unsettled;
        }
    }
    _amount = _subaccountTotalBalance > 0 ? uint256(_subaccountTotalBalance) : uint256(0);
}
```

However, in the `_getSubaccountUnsettledE18()` function, `_unsettledE18` is scaled by the collateral factor of the `settlementToken`, which is less than 1. The collateral factor is intended for checking the health factor. By applying the collateral factor, the calculated withdrawable amount is less than it should be, resulting in withdrawers being unable to withdraw the full amount they are entitled to.

```solidity
function _getSubaccountUnsettledE18(bytes32 _subaccount) internal view returns (int256 _unsettledE18) {
    IAssetService _assetService = IAssetService(assetService);
    address _perpService = perpService;
    (int256 _totalUPnLE18, int256 _totalFundingFeeE18) =
        IPerpService(_perpService).getSubaccountTotalUnrealizedPNLAndFundingFee(_subaccount);
    int256 _borrowingFeeE18 = _assetService.getSubaccountPendingBorrowingFee(_subaccount);
    _unsettledE18 = _totalUPnLE18 - _totalFundingFeeE18 - _borrowingFeeE18;
    
    // apply collateral factor if unsettled balance is positive
    if (_unsettledE18 > 0) {
        _unsettledE18 = _unsettledE18 * _assetService.collateralFactors(_assetService.settlementToken()).toInt256() / BPS.toInt256();
    }
}
```

## Impact Explanation
**High.** Using the collateral factor results in a lower withdrawable amount, preventing withdrawers from accessing the full amount they are entitled to. Consequently, users' collateral cannot be fully withdrawn, and a portion will remain locked in the protocol.

## Likelihood Explanation
**High.** This issue occurs whenever withdrawals are processed.

## Recommendation
The `getWithdrawableAmount()` function should not use `_getSubaccountUnsettledE18()` to calculate the unsettled amount. Instead, it should utilize the unsettled amount that is not scaled by the collateral factor.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | DESK |
| Report Date | N/A |
| Finders | trachev, KupiaSec |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_hmx_january2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/5c335680-b1a3-4d45-8948-bcc18c53a6f3

### Keywords for Search

`vulnerability`


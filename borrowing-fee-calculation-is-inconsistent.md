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
solodit_id: 53113
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
finders_count: 1
finders:
  - Amar Fares
---

## Vulnerability Title

Borrowing fee calculation is inconsistent 

### Overview


The AssetService::_settlePendingBorrowingFee() function is causing issues when a user's settlement token balance is negative. This function is called to update the user's borrowing and lending information and calculate the borrowing fee. However, the way the borrowing fee is calculated can result in users being charged different amounts depending on when the function is called. This can lead to incorrect protocol calculations and losses in the long-term. The recommendation is to change the way fees are accumulated to ensure consistency.

### Original Finding Content

## Context
(No context files were provided by the reviewer)

## Description
The `AssetService::_settlePendingBorrowingFee()` function is called when the user's settlement balance is updated or it's needed for a calculation.

## Function: `_settlePendingBorrowingFee`
```solidity
function _settlePendingBorrowingFee(bytes32 _subaccount) internal {
    IAssetService.BorrowingAndLendingInfo memory _currentInfo = getCurrentProtocolBorrowingAndLendingInfo();
    IAssetService.BorrowingAndLendingInfo memory _userInfo = borrowingAndLendingInfos[_subaccount];

    // if _subaccount's rates info is up-to-current, early return.
    if (
        _currentInfo.borrowingRateE18 == _userInfo.borrowingRateE18
        && _currentInfo.lendingRateE18 == _userInfo.lendingRateE18
    ) {
        return;
    }

    int256 _settlementTokenBalance = collaterals[_subaccount][settlementToken];
    if (_settlementTokenBalance > 0) {
        _payLendingFeeToSubaccount(
            _subaccount, _userInfo.lendingRateE18, _currentInfo.lendingRateE18, _settlementTokenBalance
        );
    } else if (_settlementTokenBalance < 0) {
        _receiveBorrowingFeeFromSubaccount(
            _subaccount, _userInfo.borrowingRateE18, _currentInfo.borrowingRateE18, _settlementTokenBalance
        );
    }

    // update _subaccount's rates info to current rates info
    borrowingAndLendingInfos[_subaccount] = _currentInfo;
}
```

Let's look at the scenario when a user's settlement token balance is in the negative, where `_receiveBorrowingFeeFromSubaccount()` is called:

## Function: `_receiveBorrowingFeeFromSubaccount`
```solidity
function _receiveBorrowingFeeFromSubaccount(
    bytes32 _subaccount,
    uint128 _userBorrowingRateE18,
    uint128 _protocolBorrowingRateE18,
    int256 _negativeSettlementAssetBalance
) internal {
    int256 _borrowingFee = uint256(_protocolBorrowingRateE18 - _userBorrowingRateE18).toInt256()
        * _negativeSettlementAssetBalance / 1e18;
    _adjustCollateral(_subaccount, settlementToken, _borrowingFee);
    emit LogSubaccountPayBorrowingFee(_subaccount, uint256(-_borrowingFee));
}
```

The borrowing fee to be paid is the difference between the current protocol borrowing rate and the last borrowing rate checkpoint the user has, multiplied by their balance. The protocol's borrowing rate is pushed manually by the protocol using `AdminHandler.sol`. But due to the way it is calculated, a user might be charged more or less depending on when this function is called. 

Let's look at an example:

### Example
- **Alice:**
  - Alice's balance is -100.
  - Rate jumps from 10% → 20%, function is called, and has to pay 10 (Balance at -110 now).
  - Rate jumps from 20% → 30%, function is called, and she has to pay 11 (Balance at -121 now).
  - Paid: 21, Balance: -121.

- **Bob:**
  - Bob's balance is -100.
  - Rate jumps from 10% → 20% but Bob does not interact with the protocol so function is not called; other people can't call it for Bob either.
  - Rate jumps from 20% → 30%. Bob now interacts with the protocol; he still pays 20% but that is -20 in this case.
  - Paid: 20, Balance: -120.

Both users were taxed the same rate and for the same amount, but if the user did not interact with the protocol during the period between the first and second rate hike, they will pay a smaller fee. This will just lead to the protocol calculations getting messed up, and in the long-term the protocol will suffer losses from it.

## Recommendation
Accumulate the fees in a different manner so they add up, regardless if the user interacted with the protocol during that time or not.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | DESK |
| Report Date | N/A |
| Finders | Amar Fares |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_hmx_january2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/5c335680-b1a3-4d45-8948-bcc18c53a6f3

### Keywords for Search

`vulnerability`


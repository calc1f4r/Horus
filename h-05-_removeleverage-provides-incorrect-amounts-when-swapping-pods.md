---
# Core Classification
protocol: Peapods_2024-11-16
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45992
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Peapods-security-review_2024-11-16.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-05] `_removeLeverage()` provides incorrect amounts when swapping pods

### Overview


This report discusses a bug in a code that affects the `_removeLeverage` function. This function is triggered when the `_removeLeverage` is lower than the `_repayAmount`. The bug occurs when positions using self-lending pods, where it swaps to `lendingPair` and `redeems` the lendingPair shares to acquire the actual borrow tokens. However, the redeemed lendingPair shares are not 1:1 with the borrow token, causing issues when the received borrow tokens exceed the `_borrowAmtNeededToSwap` or are insufficient to cover the repayment amount. The recommendation is to provide the amount of shares required from `_borrowAmtNeededToSwap` instead of the `_swapPodForBorrowToken` function. This will help to avoid the excess borrow tokens not being returned to the user or the call to revert due to insufficient borrow tokens for repayment.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

When `_removeLeverage` is triggered, if `_pairedAmtReceived` is lower than `_repayAmount`, it triggers `_acquireBorrowTokenForRepayment`.

```solidity
    function _removeLeverage(bytes memory _userData)
        internal
        returns (uint256 _podAmtRemaining, uint256 _borrowAmtRemaining)
    {
        // ....

        // pay back flash loan and send remaining to borrower
        uint256 _repayAmount = _d.amount + _d.fee;
        if (_pairedAmtReceived < _repayAmount) {
>>>         _podAmtRemaining = _acquireBorrowTokenForRepayment(
                _props,
                _posProps.pod,
                _d.token,
                _repayAmount,
                _pairedAmtReceived,
                _podAmtReceived,
                _userProvidedDebtAmtMax
            );
        }
        IERC20(_d.token).safeTransfer(IFlashLoanSource(_getFlashSource(_props.positionId)).source(), _repayAmount);
        _borrowAmtRemaining = _pairedAmtReceived > _repayAmount ? _pairedAmtReceived - _repayAmount : 0;
        emit RemoveLeverage(_props.positionId, _props.user, _collateralAssetRemoveAmt);
    }
```

For positions using self-lending pods, it swaps to `lendingPair` and `redeems` the lendingPair shares to acquire the actual borrow tokens.

```solidity
    function _acquireBorrowTokenForRepayment(
        LeverageFlashProps memory _props,
        address _pod,
        address _borrowToken,
        uint256 _repayAmount,
        uint256 _pairedAmtReceived,
        uint256 _podAmtReceived,
        uint256 _userProvidedDebtAmtMax
    ) internal returns (uint256 _podAmtRemaining) {
        _podAmtRemaining = _podAmtReceived;
        uint256 _borrowNeeded = _repayAmount - _pairedAmtReceived;
        uint256 _borrowAmtNeededToSwap = _borrowNeeded;
        if (_userProvidedDebtAmtMax > 0) {
            uint256 _borrowAmtFromUser =
                _userProvidedDebtAmtMax >= _borrowNeeded ? _borrowNeeded : _userProvidedDebtAmtMax;
            _borrowAmtNeededToSwap -= _borrowAmtFromUser;
            IERC20(_borrowToken).safeTransferFrom(_props.user, address(this), _borrowAmtFromUser);
        }
        // sell pod token into LP for enough borrow token to get enough to repay
        // if self-lending swap for lending pair then redeem for borrow token
        if (_borrowAmtNeededToSwap > 0) {
            if (_isPodSelfLending(_props.positionId)) {
                _podAmtRemaining = _swapPodForBorrowToken(
>>>                 _pod, positionProps[_props.positionId].lendingPair, _podAmtReceived, _borrowAmtNeededToSwap
                );
                _podAmtRemaining = IFraxlendPair(positionProps[_props.positionId].lendingPair).redeem(
                    _podAmtRemaining, address(this), address(this)
                );
            } else {
                _podAmtRemaining = _swapPodForBorrowToken(_pod, _borrowToken, _podAmtReceived, _borrowAmtNeededToSwap);
            }
        }
    }
```

It uses `_borrowAmtNeededToSwap` as the requested output for the `lendingPair` and then `redeems` it. However, the redeemed lendingPair shares are not 1:1 with the borrow token. This can cause issues: if the received borrow tokens exceed `_borrowAmtNeededToSwap` from the lendingPair, the excess will not be returned to the user. Conversely, if the received borrow tokens are insufficient, they won't cover the repayment amount, causing the call to revert.

## Recommendations

Provide the amount of shares required from `_borrowAmtNeededToSwap` instead of the `_swapPodForBorrowToken`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Peapods_2024-11-16 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Peapods-security-review_2024-11-16.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


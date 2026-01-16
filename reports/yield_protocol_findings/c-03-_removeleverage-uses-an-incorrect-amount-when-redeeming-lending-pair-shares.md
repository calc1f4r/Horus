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
solodit_id: 45985
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

[C-03] `_removeLeverage` uses an incorrect amount when redeeming lending pair shares

### Overview


This bug report discusses an issue with a function called `_acquireBorrowTokenForRepayment` that is used to remove or decrease leverage from positions. The function incorrectly provides an incorrect amount when calling the `redeem` function, causing positions with self-lending pods to fail. The report recommends updating the function to fix this issue.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** High

## Description

When users remove or decrease leverage from their positions if the `_pairedAmtReceived` is lower than `_repayAmount`, it will try to get the remaining token from `_userProvidedDebtAmtMax`, or if `_userProvidedDebtAmtMax` is not provided, it will swap the `_podAmtReceived` to repay token until it enough to cover the `_repayAmount`.

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
>>>             _podAmtRemaining = _swapPodForBorrowToken(
                    _pod, positionProps[_props.positionId].lendingPair, _podAmtReceived, _borrowAmtNeededToSwap
                );
>>>             _podAmtRemaining = IFraxlendPair(positionProps[_props.positionId].lendingPair).redeem(
                    _podAmtRemaining, address(this), address(this)
                );
            } else {
                _podAmtRemaining = _swapPodForBorrowToken(_pod, _borrowToken, _podAmtReceived, _borrowAmtNeededToSwap);
            }
        }
    }
```

```solidity
    function _swapPodForBorrowToken(address _pod, address _targetToken, uint256 _podAmt, uint256 _targetNeededAmt)
        internal
        returns (uint256 _podRemainingAmt)
    {
        IDexAdapter _dexAdapter = IDecentralizedIndex(_pod).DEX_HANDLER();
        uint256 _balBefore = IERC20(_pod).balanceOf(address(this));
        IERC20(_pod).safeIncreaseAllowance(address(_dexAdapter), _podAmt);
        _dexAdapter.swapV2SingleExactOut(_pod, _targetToken, _podAmt, _targetNeededAmt, address(this));
        _podRemainingAmt = _podAmt - (_balBefore - IERC20(_pod).balanceOf(address(this)));
    }
```

`_acquireBorrowTokenForRepayment` calls `_swapPodForBorrowToken` to swap the pod for `lendingPair`, then redeems the swapped lending pair by calling `redeem`. However, it incorrectly provides `_podAmtRemaining` instead of the received lending pair tokens to the `redeem` function.

Additionally, it unnecessarily updates `_podAmtRemaining` with the returned value of the `redeem` function, causing `_podAmtRemaining` to reflect the redeemed borrow token amount instead of the remaining pod token amount.

As a result, positions with self-lending pods cannot utilize the `_acquireBorrowTokenForRepayment` mechanism to decrease or remove their leverage positions, as the calls will revert due to incorrect amounts being used..

## Recommendations

Update the function to the following :

```diff
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
                    _pod, positionProps[_props.positionId].lendingPair, _podAmtReceived, _borrowAmtNeededToSwap
                );
+               uint256 redeemAmount = IERC20(positionProps[_props.positionId].lendingPair).balanceOf(address(this));
-               _podAmtRemaining = IFraxlendPair(positionProps[_props.positionId].lendingPair).redeem(
-                   _podAmtRemaining, address(this), address(this)
-               );
+               IFraxlendPair(positionProps[_props.positionId].lendingPair).redeem(
+                   redeemAmount, address(this), address(this)
+               );
            } else {
                _podAmtRemaining = _swapPodForBorrowToken(_pod, _borrowToken, _podAmtReceived, _borrowAmtNeededToSwap);
            }
        }
    }
```

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


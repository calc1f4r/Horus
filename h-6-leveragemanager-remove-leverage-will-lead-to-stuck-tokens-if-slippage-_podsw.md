---
# Core Classification
protocol: Peapods
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52751
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/749
source_link: none
github_link: https://github.com/sherlock-audit/2025-01-peapods-finance-judging/issues/446

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
finders_count: 4
finders:
  - pkqs90
  - ZoA
  - elolpuer
  - X77
---

## Vulnerability Title

H-6: LeverageManager remove leverage will lead to stuck tokens if slippage `_podSwapAmtOutMin` is set.

### Overview


This bug report discusses an issue with the LeverageManager in the Peapods Finance system. The issue occurs when removing leverage and setting a parameter for slippage, causing leftover borrowed tokens to become stuck in the contract. This is due to the contract conducting an exactOutput swap, which is vulnerable to frontrunning and sandwich attacks. The bug report provides code snippets and explains the impact and potential attack path. The suggested mitigation is to also transfer the remaining borrowed tokens back to the user.

### Original Finding Content

Source: https://github.com/sherlock-audit/2025-01-peapods-finance-judging/issues/446 

## Found by 
X77, ZoA, elolpuer, pkqs90


### Summary

LeverageManager remove leverage will lead to stuck tokens if slippage `_podSwapAmtOutMin` is set.

### Root Cause

First we need to understand the workflow of removeLeverage in LeverageManager.

1. Borrow `_borrowAssetAmt` underlying token from flashloan source.
2. Repay these tokens to FraxlendPair.
3. Withdraw collateral (aspTKN) to borrowedTKN and pTKN. If borrowedTKN is not enough to repay the flashloan, swap pTKN to borrowedTKN.
4. Repay flashloan.
5. Send leftover borrowedTKN and pTKN back to position owner.

In step 3, it conducts an exactOutput swap. The target amount of output is the required amount of borrowedTKN for repay. However, this is susceptible to frontrunning and sandwich attacks. So the user needs to explicitly set a `_podSwapAmtOutMin` parameter as slippage.

The issue here is, if `_podSwapAmtOutMin` is set, and there are leftover borrowTKNs, they are not transferred to the user, but stuck in the contract. This is because `_borrowAmtRemaining` will always be zero in this case.

For example, after redeeming the spTKN, we have 100 pTKN and 100 borrowedTKN (pTKN:borrowedTKN = 1:1). However, we need to repay 120 borrowedTKN. If user don't set `_podSwapAmtOutMin`, the pTKN -> borrowedTKN swap would be a maxInput=100, exactOutput=20 swap, which can obviously be sandwiched. If user sets `_podSwapAmtOutMin` to 95 for slippage, the remaining 95-20=75 borrowedTokens are not transferred back to user.

https://github.com/sherlock-audit/2025-01-peapods-finance/blob/main/contracts/contracts/lvf/LeverageManager.sol#L1

```solidity
    function _swapPodForBorrowToken(
        address _pod,
        address _targetToken,
        uint256 _podAmt,
        uint256 _targetNeededAmt,
        uint256 _podSwapAmtOutMin
    ) internal returns (uint256 _podRemainingAmt) {
        IDexAdapter _dexAdapter = IDecentralizedIndex(_pod).DEX_HANDLER();
        uint256 _balBefore = IERC20(_pod).balanceOf(address(this));
        IERC20(_pod).safeIncreaseAllowance(address(_dexAdapter), _podAmt);
@>      _dexAdapter.swapV2SingleExactOut(
            _pod, _targetToken, _podAmt, _podSwapAmtOutMin == 0 ? _targetNeededAmt : _podSwapAmtOutMin, address(this)
        );
        _podRemainingAmt = _podAmt - (_balBefore - IERC20(_pod).balanceOf(address(this)));
    }

    function _removeLeveragePostCallback(bytes memory _userData)
        internal
        returns (uint256 _podAmtRemaining, uint256 _borrowAmtRemaining)
    {
        ...
        // pay back flash loan and send remaining to borrower
        uint256 _repayAmount = _d.amount + _d.fee;
        if (_pairedAmtReceived < _repayAmount) {
            _podAmtRemaining = _acquireBorrowTokenForRepayment(
                _props,
                _posProps.pod,
                _d.token,
                _repayAmount - _pairedAmtReceived,
                _podAmtReceived,
                _podSwapAmtOutMin,
                _userProvidedDebtAmtMax
            );
        }
        IERC20(_d.token).safeTransfer(IFlashLoanSource(_getFlashSource(_props.positionId)).source(), _repayAmount);
@>      _borrowAmtRemaining = _pairedAmtReceived > _repayAmount ? _pairedAmtReceived - _repayAmount : 0;
        emit RemoveLeverage(_props.positionId, _props.owner, _collateralAssetRemoveAmt);
    }

```

### Internal pre-conditions

- When removing leverage, a pTKN -> borrowTKN swap is required, and user sets `_podSwapAmtOutMin` for slippage.

### External pre-conditions

N/A

### Attack Path

N/A

### Impact

Leftover borrowedTokens are locked in the contract.

### PoC

N/A

### Mitigation

Also transfer the remaining borrowTKN to user.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Peapods |
| Report Date | N/A |
| Finders | pkqs90, ZoA, elolpuer, X77 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-01-peapods-finance-judging/issues/446
- **Contest**: https://app.sherlock.xyz/audits/contests/749

### Keywords for Search

`vulnerability`


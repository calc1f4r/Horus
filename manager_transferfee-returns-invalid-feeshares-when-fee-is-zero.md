---
# Core Classification
protocol: Yieldfi
chain: everychain
category: uncategorized
vulnerability_type: overflow/underflow

# Attack Vector Details
attack_type: overflow/underflow
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55540
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - overflow/underflow

protocol_categories:
  - yield

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Immeas
  - Jorge
---

## Vulnerability Title

`Manager::_transferFee` returns invalid `feeShares` when `fee` is zero

### Overview


The report describes a bug in the `Manager` contract where deposits with a fee of zero can result in incorrect calculations and potentially cause the deposit to fail or result in zero shares being credited to the user. The recommended mitigation is to update the `_transferFee` function to return `0` when the fee is zero. The bug has been fixed by YieldFi and verified by Cyfrin.

### Original Finding Content

**Description:** When a user deposits directly into `Manager::deposit`, the protocol fee is calculated via the [`Manager::_transferFee`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/Manager.sol#L226-L242) function:

```solidity
function _transferFee(address _yToken, uint256 _shares, uint256 _fee) internal returns (uint256) {
    if (_fee == 0) {
        return _shares;
    }
    uint256 feeShares = (_shares * _fee) / Constants.HUNDRED_PERCENT;

    IERC20(_yToken).safeTransfer(treasury, feeShares);

    return feeShares;
}
```

The issue is that when `_fee == 0`, the function returns the full `_shares` amount instead of returning `0`. This leads to incorrect logic downstream in [`Manager::_deposit`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/Manager.sol#L286-L296), where the result is subtracted from the total shares:

```solidity
// transfer fee to treasury, already applied on adjustedShares
uint256 adjustedFeeShares = _transferFee(order.yToken, adjustedShares, _fee);

// Calculate adjusted gas fee shares
uint256 adjustedGasFeeShares = (_gasFeeShares * order.exchangeRateInUnderlying) / currentExchangeRate;

// transfer gas to caller
IERC20(order.yToken).safeTransfer(_caller, adjustedGasFeeShares);

// remaining shares after gas fee
uint256 sharesAfterAllFee = adjustedShares - adjustedFeeShares - adjustedGasFeeShares;
```

If `_fee == 0`, the `adjustedFeeShares` value will incorrectly equal `adjustedShares`, causing `sharesAfterAllFee` to underflow (revert), assuming `adjustedGasFeeShares` is non-zero.

**Impact:** Deposits into the `Manager` contract with a fee of zero will revert if any gas fee is also deducted. In the best-case scenario, the deposit fails. In the worst case—if the subtraction somehow passes unchecked—it could result in zero shares being credited to the user.

**Recommended Mitigation:** Update `_transferFee` to return `0` when `_fee == 0`, to ensure downstream calculations behave correctly:

```diff
  if (_fee == 0) {
-     return _shares;
+     return 0;
  }
```

**YieldFi:** Fixed in commit [`6e76d5b`](https://github.com/YieldFiLabs/contracts/commit/6e76d5beee3ba7a49af6becc58a596a4b67841c3)

**Cyfrin:** Verified. `_transferFee` now returns `0` when `_fee = 0`

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Cyfrin |
| Protocol | Yieldfi |
| Report Date | N/A |
| Finders | Immeas, Jorge |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Overflow/Underflow`


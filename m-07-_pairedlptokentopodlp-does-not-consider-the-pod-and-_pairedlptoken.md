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
solodit_id: 46001
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Peapods-security-review_2024-11-16.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-07] `_pairedLpTokenToPodLp` does not consider the `pod` and `_pairedLpToken`

### Overview


The bug report states that when a certain function, `_pairedLpTokenToPodLp`, is called, it tries to call another function, `indexUtils.addLPAndStake`, with specific tokens. However, if the `addLPAndStake` function fails, the tokens are not properly tracked and become stuck in the contract. The severity of this bug is high and the likelihood is low. The recommendation is to handle the tokens properly in case the `addLPAndStake` function fails.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

When `_pairedLpTokenToPodLp` is called, it will try to call `indexUtils.addLPAndStake`, providing the `_pairedLpToken` and the `pod` tokens.

```solidity
    function _pairedLpTokenToPodLp(uint256 _amountIn, uint256 _deadline) internal returns (uint256 _amountOut) {
        address _pairedLpToken = pod.PAIRED_LP_TOKEN();
        uint256 _pairedSwapAmt = _getSwapAmt(_pairedLpToken, address(pod), _pairedLpToken, _amountIn);
        uint256 _pairedRemaining = _amountIn - _pairedSwapAmt;
        uint256 _minPtknOut;
        if (address(podOracle) != address(0)) {
            // calculate the min out with 5% slippage
            _minPtknOut = (
                podOracle.getPodPerBasePrice() * _pairedSwapAmt * 10 ** IERC20Metadata(address(pod)).decimals() * 95
            ) / 10 ** IERC20Metadata(_pairedLpToken).decimals() / 10 ** 18 / 100;
        }
        IERC20(_pairedLpToken).safeIncreaseAllowance(address(DEX_ADAPTER), _pairedSwapAmt);
        try DEX_ADAPTER.swapV2Single(_pairedLpToken, address(pod), _pairedSwapAmt, _minPtknOut, address(this)) returns (
            uint256 _podAmountOut
        ) {
            IERC20(pod).safeIncreaseAllowance(address(indexUtils), _podAmountOut);
            IERC20(_pairedLpToken).safeIncreaseAllowance(address(indexUtils), _pairedRemaining);
            try indexUtils.addLPAndStake(
                pod, _podAmountOut, _pairedLpToken, _pairedRemaining, _pairedRemaining, LP_SLIPPAGE, _deadline
            ) returns (uint256 _lpTknOut) {
                _amountOut = _lpTknOut;
>>>         } catch {
                IERC20(pod).safeDecreaseAllowance(address(indexUtils), _podAmountOut);
                IERC20(_pairedLpToken).safeDecreaseAllowance(address(indexUtils), _pairedRemaining);
                emit AddLpAndStakeError(address(pod), _amountIn);
            }
        } catch {
            IERC20(_pairedLpToken).safeDecreaseAllowance(address(DEX_ADAPTER), _pairedSwapAmt);
            emit AddLpAndStakeV2SwapError(_pairedLpToken, address(pod), _pairedRemaining);
        }
    }
```

However, if the `addLPAndStake` call fails, the `pod` and `_pairedLpToken` are not properly tracked, causing the tokens to become stuck inside the contract.

## Recommendations

Consider properly handling the `pod` and `_pairedLpToken` in case the `addLPAndStake` call reverts.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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


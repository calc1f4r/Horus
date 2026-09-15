---
# Core Classification
protocol: Fyde May
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36410
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Fyde-security-review-May.md
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

protocol_categories:
  - yield

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-05] `swapOn1INCH()` slippage may be ineffective

### Overview


The report states that there is a bug in the `swapOn1INCH()` function that checks for slippage when swapping tokens. This check may not be effective if there are already tokens of the output asset in the contract. This means that the check may not catch instances where the minimum amount of output tokens is not received. To fix this issue, it is recommended to update the function to also check the balance of the output token before and after the swap to ensure that the minimum amount is received. 

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** Low

**Description**

The `swapOn1INCH()` function attempts to check for slippage as follows:

```solidity
  function swapOn1INCH(
    address _assetIn,
    uint256 _amountIn,
    address _assetOut,
    uint256 _minAmountOut,
    bytes calldata _swapData
  ) external {
    IERC20(_assetIn).approve(ONEINCH_AGGREGATION_ROUTER, _amountIn);
    (bool success, bytes memory data) = ONEINCH_AGGREGATION_ROUTER.call(_swapData);
    require(IERC20(_assetOut).balanceOf(address(this)) >= _minAmountOut, "Slippage Exceeded");
  }
```

This slippage check may be ineffective when there are already tokens of `_assetOut` in the contract. Here's a simple example to illustrate the issue:

- The owner wants to swap 1000 token1 for token2.
  - Assume there are already 500 token2 in the contract.
- The owner sets `_minAmountOut` to 995.
- The swap returns 500 token2 for the 1000 token1.
- The slippage check will pass because the total token2 balance (1000) exceeds `_minAmountOut` (995).

**Recommendations**

To ensure the slippage check is effective, consider updating the `swapOn1INCH()` function as follows:

```solidity
  function swapOn1INCH(
    address _assetIn,
    uint256 _amountIn,
    address _assetOut,
    uint256 _minAmountOut,
    bytes calldata _swapData
  ) external {
    uint256 balBefore = IERC20(_assetOut).balanceOf(address(this));
    IERC20(_assetIn).approve(ONEINCH_AGGREGATION_ROUTER, _amountIn);
    (bool success, bytes memory data) = ONEINCH_AGGREGATION_ROUTER.call(_swapData);
    uint256 balAfter = IERC20(_assetOut).balanceOf(address(this));
    require((balAfter - balBefore) >= _minAmountOut, "Slippage Exceeded");
  }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Fyde May |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Fyde-security-review-May.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


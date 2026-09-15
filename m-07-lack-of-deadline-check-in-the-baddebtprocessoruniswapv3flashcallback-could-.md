---
# Core Classification
protocol: Stackingsalmon
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52795
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/StackingSalmon-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[M-07] Lack of `deadline` Check in the `BadDebtProcessor::uniswapV3FlashCallback()` Could Lead To Loss of Funds to the User

### Overview


This report talks about a bug in the `BadDebtProcessor::uniswapV3FlashCallback()` function. The function only performs a slippage check and not a deadline check. This can lead to the `BadDebtProcessor::process()` transaction being executed at a later time with different price points, causing loss to the user. The recommendation is to implement a deadline check and pass the deadline as a user input to ensure the transaction is not executed after a certain time. The team has fixed the bug.

### Original Finding Content

## Severity

Medium Risk

## Description

The `UNISWAP_POOL().swap()` is performed in the `FrontendManager::callback()` when the `action == 6` and in the `BoostManager::_action2Burn()` functions. In both those occasions, the `deadline` check is performed in addition to the slippage checks. This is to ensure that the transaction is not executed after a delay at an unfavourable price point to the user. The `slippage` check alone can not mitigate this issue since slippage applies to the derived swap value at the time of the transaction execution.

But the `UNISWAP_POOL().swap()` performed in the `BadDebtProcessor::uniswapV3FlashCallback()` only performs the slippage check but does not perform a deadline check.

## Location of Affected Code

File: [src/BadDebtProcessor.sol](https://github.com/cryptovash/sammin-core/blob/c49807ae2965cf6d121a10507a43de1d64ba1e70/helpers/src/BadDebtProcessor.sol)

```solidity
if (exactAmountOut < 0) {
      // Need to swap `token1` (the one we received during liquidation) for `token0` (which is `flashToken`)
    (, swapped) = borrower.UNISWAP_POOL().swap(
        address(this), false, exactAmountOut, TickMath.MAX_SQRT_RATIO - 1, bytes("")
    );
    require(uint256(swapped) < recovered * slippage / 10_000, "slippage");
}
```

## Impact

The `BadDebtProcessor::process()` transaction can be executed after a significant delay, which could prompt the asset ratios in the UniswapV3Pool to have changed considerably.

Hence the swapped and recovered asset amounts are calculated based on the highly altered price points. As a result, the provided slippage is stale and will not provide the required protection to the user, thus incurring loss to the user.

## Recommendation

Hence it is recommended to implement the deadline check in the `BadDebtProcessor::uniswapV3FlashCallback()` function to ensure execution of `BadDebtProcessor::process()` is not allowed after the given deadline.

The `deadline` should be passed as a user input to the `BadDebtProcessor::process()` function. This will ensure users will not lose funds due to delayed execution with stale slippage checks.

## Team Response

Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Stackingsalmon |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/StackingSalmon-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


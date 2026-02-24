---
# Core Classification
protocol: generic
chain: everychain
category: slippage_protection
vulnerability_type: dex_aggregator_slippage_check_bypass

# Attack Vector Details
attack_type: economic_exploit
affected_component: swap_output_validation

# Technical Primitives
primitives:
  - slippage_check
  - balance_snapshot
  - dex_aggregator
  - oneinch
  - fee_on_transfer
  - absolute_vs_delta_balance
  - minAmountOut
  - pre_existing_balance
  - sandwich_attack

# Impact Classification
severity: medium
impact: fund_loss
exploitability: 0.6
financial_impact: medium

# Context Tags
tags:
  - defi
  - slippage
  - oneinch
  - aggregator
  - swap
  - dex
  - balance_check
  - fee_on_transfer
  - mev

# Version Info
language: solidity
version: all

# Source
source: solodit + audit-reports
---

## Reference

| # | Report File | Protocol | Severity | Auditor |
|---|-------------|----------|----------|---------|
| 1 | [m-05-swapon1inch-slippage-may-be-ineffective.md](reports/dex_aggregator_findings/m-05-swapon1inch-slippage-may-be-ineffective.md) | Fyde May | MEDIUM | Pashov Audit Group |
| 2 | [m-2-when-the-amout-of-token-acquired-by-a-flash-loan-exceeds-the-expected-value-.md](reports/dex_aggregator_findings/m-2-when-the-amout-of-token-acquired-by-a-flash-loan-exceeds-the-expected-value-.md) | WagmiLeverage V2 | MEDIUM | Sherlock |
| 3 | [m-01-fee-on-transfer-tokens-can-cause-accounting-errors-in-swappee-contract.md](reports/dex_aggregator_findings/m-01-fee-on-transfer-tokens-can-cause-accounting-errors-in-swappee-contract.md) | Swappee | MEDIUM | solodit |

---

# DEX Aggregator Slippage Check Bypass via Pre-Existing Balance

## Overview

When protocols integrate DEX aggregators (1inch, Paraswap, 0x, Uniswap), slippage protection is typically enforced by checking the post-swap token balance against a `minAmountOut` threshold. If this check uses the **absolute final balance** rather than the **delta (balance_after − balance_before)**, the check is ineffective whenever the contract already holds a non-zero balance of the output token. An attacker or MEV bot can manipulate the swap to return far fewer tokens than expected, and the check still passes because pre-existing tokens inflate the apparent output.

**Root Cause Statement**: This vulnerability exists because slippage checks compare `balanceOf(outputToken)` after the swap against `minAmountOut`, rather than computing `balanceAfter − balanceBefore`, allowing pre-existing contract balances of the output token to mask a catastrophically under-performing swap, enabling MEV extraction and sandwich attacks.

**Pattern Frequency**: Common (3/32 DEX aggregator reports — 9%)
**Consensus Severity**: MEDIUM (all 3 reports)
**Cross-Auditor Validation**: MODERATE — 3 independent auditors across different protocols

---

## Vulnerability Description

### Root Cause

The typical slippage check pattern in aggregator integrations is:

```solidity
aggregator.call(swapData);
require(IERC20(assetOut).balanceOf(address(this)) >= minAmountOut, "Slippage");
```

This reads the **total** balance post-swap. If the contract already holds `N` tokens of `assetOut`, then even a completely failed or heavily manipulated swap — returning 0 output — will pass the check as long as `N >= minAmountOut`.

The correct pattern measures only the **incremental yield** from the swap:

```solidity
uint256 before = IERC20(assetOut).balanceOf(address(this));
aggregator.call(swapData);
require(IERC20(assetOut).balanceOf(address(this)) - before >= minAmountOut, "Slippage");
```

### When Does Pre-Existing Balance Occur?

- Incomplete previous swaps left residual output tokens
- Fee-on-transfer tokens accumulate in the contract over many transactions
- Multi-step operations where a previous step deposited the same token
- Re-entrant or batched calls where balance state is shared

---

## Attack Scenarios

### Scenario 1 — Residual Balance Masks Bad Swap (Fyde May)

1. Protocol holds 500 token2 as residual from previous operations
2. Admin initiates `swapOn1INCH(token1 → token2, amount=1000, minAmountOut=995)`
3. MEV/sandwich attack manipulates price; swap returns only 300 token2
4. Post-swap balance: 500 + 300 = 800 < 995 → SHOULD revert
5. But actual check: `balanceOf(token2) = 800`, which is NOT >= 995 in this case
6. **However**: if residual was 700+, balance would be 1000+ and the bad swap (300 received instead of 995) silently passes

### Scenario 2 — Flash Loan Excess Amount Breaks Callback (WagmiLeverage V2)

1. Protocol takes a flash loan expecting exactly `expectedAmount` of `holdToken`
2. Flash loan provider returns `actualAmount > expectedAmount` (excess)
3. Callback function hardcodes the expected amount: `require(holdToken.received == expectedAmount)`
4. Call reverts because `actualAmount != expectedAmount` — DoS on all flash-loan paths
5. Root: no tolerance for receiving *more* than expected; amounts not normalized before slippage check

### Scenario 3 — Fee-on-Transfer Token Accounting Error (Swappee)

1. Protocol swaps a fee-on-transfer token through an aggregator
2. Input amount is `1000`, but fee takes 1% → only 990 arrives at aggregator
3. Aggregator swap executes on `990`, output is calculated on deflated input
4. Slippage check passes (absolute balance check) even though effective output is below threshold
5. User receives fewer tokens than `minAmountOut` implied by their input

---

## Vulnerable Pattern Examples

**Example 1: Absolute Balance Slippage Check** [MEDIUM — Fyde May, Pashov Audit Group]

Reference: [m-05-swapon1inch-slippage-may-be-ineffective.md](reports/dex_aggregator_findings/m-05-swapon1inch-slippage-may-be-ineffective.md)

```solidity
// ❌ VULNERABLE: slippage check uses ABSOLUTE balance, not delta
// If contract already holds _assetOut tokens, this check is ineffective
function swapOn1INCH(
    address _assetIn,
    uint256 _amountIn,
    address _assetOut,
    uint256 _minAmountOut,
    bytes calldata _swapData
) external {
    IERC20(_assetIn).approve(ONEINCH_AGGREGATION_ROUTER, _amountIn);
    (bool success,) = ONEINCH_AGGREGATION_ROUTER.call(_swapData);
    require(success, "swap failed");

    // ❌ Uses absolute balance, not delta
    // If 500 _assetOut was already in contract and swap returns 0,
    // this check still passes when _minAmountOut <= 500
    require(
        IERC20(_assetOut).balanceOf(address(this)) >= _minAmountOut,
        "Slippage Exceeded"
    );
}
```

**Example 2: Hardcoded Expected Amount in Flash Loan Callback** [MEDIUM — WagmiLeverage V2, Sherlock]

Reference: [m-2-when-the-amout-of-token-acquired-by-a-flash-loan-exceeds-the-expected-value-.md](reports/dex_aggregator_findings/m-2-when-the-amout-of-token-acquired-by-a-flash-loan-exceeds-the-expected-value-.md)

```solidity
// ❌ VULNERABLE: callback assumes received == expectedAmount exactly
// If flash loan sends MORE than expected, the callback reverts (DoS)
function holdTokenFlashCallback(
    address initiator,
    address token,
    uint256 amount,    // actual amount received (may be > expectedHoldAmount)
    uint256 fee,
    bytes calldata data
) external {
    (uint256 expectedHoldAmount, ...) = abi.decode(data, (...));

    // ❌ strict equality: any excess causes revert
    require(
        IERC20(token).balanceOf(address(this)) == expectedHoldAmount + fee,
        "unexpected balance"
    );
    // entire swap integration breaks if pool donates extra tokens
}
```

**Example 3: Fee-on-Transfer Token Breaks Swap Accounting** [MEDIUM — Swappee]

Reference: [m-01-fee-on-transfer-tokens-can-cause-accounting-errors-in-swappee-contract.md](reports/dex_aggregator_findings/m-01-fee-on-transfer-tokens-can-cause-accounting-errors-in-swappee-contract.md)

```solidity
// ❌ VULNERABLE: uses nominal amount for swap approval, not actual received amount
function swap(
    address tokenIn,
    uint256 amountIn,   // nominal amount BEFORE fee deduction
    address tokenOut,
    uint256 minAmountOut,
    bytes calldata swapData
) external {
    // Transfer in — fee deducted, actual received = amountIn * (1 - fee%)
    IERC20(tokenIn).transferFrom(msg.sender, address(this), amountIn);

    // ❌ Approves for full nominalAmount, but only amountIn*(1-fee%) is available
    IERC20(tokenIn).approve(aggregator, amountIn);

    // Aggregator sees less input than approved, swap output is deflated
    (bool success,) = aggregator.call(swapData);

    // ❌ Absolute balance check masks the accounting error
    require(IERC20(tokenOut).balanceOf(address(this)) >= minAmountOut);
}
```

---

## Impact Analysis

### Technical Impact
- Slippage protection silently bypassed — protocol accepts worse-than-expected swap rates (2/3 reports)
- DoS on flash-loan dependent swap paths when received > expected (1/3 reports)
- Fee-on-transfer token accounting errors propagate through the entire swap flow (1/3 reports)

### Business Impact
- Users lose funds proportional to undetected slippage (up to full input loss in extreme manipulation)
- MEV bots can sandwich swap transactions without triggering slippage reverts
- Protocol can accumulate residual balances over time, progressively worsening the effective slippage protection

### Affected Scenarios
- Any protocol integrating DEX aggregators where the contract holds output tokens between operations
- Multi-step DeFi flows (leverage, yield, liquidation) that reuse the same contract for multiple swaps
- Fee-on-transfer token swaps through aggregators
- Flash-loan-powered operations with strict amount expectations in callbacks

---

## Secure Implementation

**Fix 1: Snapshot Balance Before Swap — Compare Delta** [Recommended]

Reference: [m-05-swapon1inch-slippage-may-be-ineffective.md](reports/dex_aggregator_findings/m-05-swapon1inch-slippage-may-be-ineffective.md) — auditor recommendation

```solidity
// ✅ SECURE: snapshot before, check delta after
function swapOn1INCH(
    address _assetIn,
    uint256 _amountIn,
    address _assetOut,
    uint256 _minAmountOut,
    bytes calldata _swapData
) external {
    // Snapshot output balance BEFORE swap
    uint256 balanceBefore = IERC20(_assetOut).balanceOf(address(this));

    IERC20(_assetIn).approve(ONEINCH_AGGREGATION_ROUTER, _amountIn);
    (bool success,) = ONEINCH_AGGREGATION_ROUTER.call(_swapData);
    require(success, "swap failed");

    // ✅ Check DELTA — pre-existing balance cannot mask a bad swap
    uint256 received = IERC20(_assetOut).balanceOf(address(this)) - balanceBefore;
    require(received >= _minAmountOut, "Slippage Exceeded");
}
```

**Fix 2: Use Actual Received Amount in Flash Loan Callback**

```solidity
// ✅ SECURE: use >= instead of ==, allow excess, work with available balance
function holdTokenFlashCallback(
    address initiator,
    address token,
    uint256 amountReceived,  // actual amount received
    uint256 fee,
    bytes calldata data
) external {
    (uint256 minimumRequired, ...) = abi.decode(data, (...));

    // ✅ Accept any amount >= minimum, don't revert on excess
    require(
        amountReceived >= minimumRequired,
        "insufficient flash loan amount"
    );

    // Use actual available balance downstream, not hardcoded expected amount
    uint256 availableBalance = IERC20(token).balanceOf(address(this));
    _executeSwapLogic(token, availableBalance, ...);
}
```

**Fix 3: Measure Actual Received Amount for Fee-on-Transfer Tokens**

```solidity
// ✅ SECURE: measure actual received amount post-transfer
function swap(
    address tokenIn,
    uint256 amountIn,
    address tokenOut,
    uint256 minAmountOut,
    bytes calldata swapData
) external {
    uint256 balInBefore = IERC20(tokenIn).balanceOf(address(this));
    IERC20(tokenIn).transferFrom(msg.sender, address(this), amountIn);
    // ✅ Actual received (accounts for fee-on-transfer)
    uint256 actualAmountIn = IERC20(tokenIn).balanceOf(address(this)) - balInBefore;

    uint256 balOutBefore = IERC20(tokenOut).balanceOf(address(this));
    IERC20(tokenIn).approve(aggregator, actualAmountIn);  // approve actual
    (bool success,) = aggregator.call(swapData);
    require(success, "swap failed");

    // ✅ Delta check on output too
    uint256 received = IERC20(tokenOut).balanceOf(address(this)) - balOutBefore;
    require(received >= minAmountOut, "Slippage Exceeded");
}
```

---

## Detection Patterns

### Code Patterns to Search For

```
# Absolute balance check after aggregator call (no snapshot before)
grep -rn "balanceOf.*>=.*min\|balanceOf.*>.*_min" --include="*.sol" | grep -v "Before\|before\|snapshot"

# 1inch/aggregator call followed immediately by balance check (no before snapshot)
grep -rn -A 5 "ONEINCH.*\.call\|aggregator\.call\|one_inch.*call" --include="*.sol" | grep "balanceOf"

# Flash loan callbacks with strict equality on received amounts
grep -rn "require.*amount.*==\|==.*expectedAmount" --include="*.sol"

# Approve using nominal (pre-fee) amount for fee-on-transfer tokens
grep -rn "transferFrom.*amountIn.*approve.*amountIn" --include="*.sol"
```

### Audit Checklist

- [ ] Is slippage protection implemented as `delta = balanceAfter - balanceBefore >= minOut`?
- [ ] Are there any absolute balance checks after aggregator calls?
- [ ] Does the contract ever hold residual output token balances between operations?
- [ ] Is the protocol compatible with fee-on-transfer tokens in the swap path?
- [ ] Do flash loan callbacks use `>=` (not `==`) for received amount validation?
- [ ] Is the actual token-in amount (post fee-on-transfer) measured before approval/swap?

---

### Keywords for Search

`slippage check bypass`, `absolute balance slippage`, `pre-existing balance slippage`, `balanceBefore snapshot`, `minAmountOut bypass`, `1inch slippage ineffective`, `aggregator slippage check`, `delta balance check`, `fee on transfer slippage`, `flash loan callback amount`, `swap output validation`, `swapOn1INCH vulnerability`, `dex aggregator output check`, `residual balance exploit`, `oneinch balance check`, `slippage protection dex`, `received amount validation`

### Related Vulnerabilities

- [DB/general/slippage-protection/slippage-protection.md](DB/general/slippage-protection/slippage-protection.md) — General slippage protection patterns
- [DB/general/arbitrary-call/dex-aggregator-unvalidated-call-data.md](DB/general/arbitrary-call/dex-aggregator-unvalidated-call-data.md) — Unvalidated DEX aggregator calldata
- [DB/general/fee-on-transfer-tokens/](DB/general/fee-on-transfer-tokens/) — Fee-on-transfer token compatibility

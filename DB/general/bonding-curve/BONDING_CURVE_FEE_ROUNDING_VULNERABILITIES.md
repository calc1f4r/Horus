---
# Core Classification (Required)
protocol: generic
chain: everychain
category: bonding_curve
vulnerability_type: fee_calculation_rounding

# Attack Vector Details (Required)
attack_type: economic_exploit|logical_error
affected_component: fee_calculation|rounding|precision|swap_fee|reward_distribution

# Technical Primitives (Required)
primitives:
  - bonding_curve
  - fee_calculation
  - rounding_error
  - precision_loss
  - swap_fee
  - integer_division
  - fee_on_transfer
  - PRECISION
  - feeBps
  - cumulativeFeePerToken
  - reserveRatio
  - invariant

# Impact Classification (Required)
severity: high|medium
impact: fund_loss|value_leak|dos
exploitability: 0.70
financial_impact: medium

# Context Tags
tags:
  - defi
  - bonding_curve
  - fee_calculation
  - rounding
  - precision
  - swap_fee
  - dust
  - invariant

# Version Info
language: solidity|rust
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Fee Calculation Errors
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Stardusts - Fee on totalCost vs ethNeeded | `reports/bonding_curve_findings/h-01-incorrect-fee-calculation-occurs-on-bonding-curve-buys.md` | HIGH | Pashov Audit Group |
| PumpScience - Last Buy Fee Mismatch | `reports/bonding_curve_findings/m-01-last-buy-on-bonding-curve-may-have-an-incorrect-fee-calculation.md` | MEDIUM | Code4rena |
| Dango - Omitted Swap Fee in reflect_curve | `reports/bonding_curve_findings/m-1-omission-of-swap-fee-in-reflect_curve-causes-undervaluation-and-inconsistent.md` | MEDIUM | Code4rena |
| Bunni - Inconsistent Swap Fee Between Quoter and Hook | `reports/bonding_curve_findings/m-03-inconsistent-swap-fee-implementation-in-virtual-bonding-curve.md` | MEDIUM | Code4rena |

### Rounding & Precision Errors
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Mento Good$ - Expansion Mint Rounding DOS | `reports/bonding_curve_findings/m-2-rounding-issue-in-bonding-curves-mintfromexpansion-can-cause-a-permanent-dos.md` | MEDIUM | Sherlock |
| Fei - Roots Library Truncation | `reports/bonding_curve_findings/m03-roots-library-is-inaccurate.md` | MEDIUM | OpenZeppelin |
| Notional - Invariant Rounding Mismatch | `reports/bonding_curve_findings/h-2-rounding-in-the-wrong-direction-in-fcashinvariant-leads-to-the-ability-to-fr.md` | HIGH | Sherlock |
| GTE - Underpriced Quote Rounding | `reports/bonding_curve_findings/m-23-underpriced-quote-in-bondingcurve-due-to-rounding-error.md` | MEDIUM | Code4rena |
| PumpScience - Invariant Rent Inclusion | `reports/bonding_curve_findings/m-02-bonding-curve-invariant-check-incorrectly-validates-sol-balance-due-to-rent.md` | MEDIUM | Code4rena |

### Fee Distribution Issues
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Curves - Stuck FeeSplitter Rewards | `reports/bonding_curve_findings/m-05-feesplitter-reward-tokens-can-become-stuck-in-the-contract.md` | MEDIUM | Code4rena |

---

# Bonding Curve Fee Calculation & Rounding Vulnerabilities

**Comprehensive Patterns for Fee Miscalculations, Rounding Errors, Precision Loss, and Reward Distribution Issues**

---

## Table of Contents

1. [Fee Calculated on Wrong Base Amount](#1-fee-calculated-on-wrong-base-amount)
2. [Last Buy Fee Mismatch on Bonding Curve](#2-last-buy-fee-mismatch-on-bonding-curve)
3. [Swap Fee Omitted in Order Reflections](#3-swap-fee-omitted-in-order-reflections)
4. [Inconsistent Fee Between Quoter and Execution](#4-inconsistent-fee-between-quoter-and-execution)
5. [Expansion Mint Precision Loss Causes DOS](#5-expansion-mint-precision-loss-causes-dos)
6. [Root/Exponent Library Truncation Compounds Error](#6-rootexponent-library-truncation-compounds-error)
7. [Invariant Rounding Direction Mismatch](#7-invariant-rounding-direction-mismatch)
8. [Underpriced Quote via Integer Division Truncation](#8-underpriced-quote-via-integer-division-truncation)
9. [Invariant Check Invalidated by Rent Inclusion](#9-invariant-check-invalidated-by-rent-inclusion)
10. [Fee Reward Dust Permanently Stuck in Contract](#10-fee-reward-dust-permanently-stuck-in-contract)
11. [Fee-on-Transfer Token Accounting Mismatch](#11-fee-on-transfer-token-accounting-mismatch)

---

## 1. Fee Calculated on Wrong Base Amount

### Overview

When a buy order exceeds the remaining tokens on a bonding curve, the fee is initially calculated on the full `msg.value` but should be recalculated based on the actual ETH needed (`ethNeeded`). If the recalculation uses `ethNeeded` as the base but the fee formula expects the total *including* the fee, the fee is underestimated.

> 📖 Reference: `reports/bonding_curve_findings/h-01-incorrect-fee-calculation-occurs-on-bonding-curve-buys.md`

### Vulnerability Description

#### Root Cause
The fee is `(ethNeeded * feeBps) / 10000` which gives the fee *on the pre-fee amount*. But `totalCost = ethNeeded + fee` means the user pays less total than they should, since `fee / totalCost < feeBps / 10000`.

### Vulnerable Pattern Examples

**Example 1: Fee Underestimate on Remaining Tokens** [HIGH]
```solidity
// ❌ VULNERABLE: Fee calculated ON ethNeeded, not inclusive of fee
function _validateBondingCurveBuy(uint256 minOrderSize)
    internal returns (uint256 totalCost, uint256 trueOrderSize, uint256 fee, uint256 refund, bool shouldGraduate)
{
    totalCost = msg.value;
    fee = (totalCost * feeBps) / 10000;  // First pass: fee on full msg.value
    uint256 remainingEth = totalCost - fee;

    if (trueOrderSize > maxRemainingTokens) {
        trueOrderSize = maxRemainingTokens;
        uint256 ethNeeded = Y1 - virtualEthLiquidity;
        
        fee = (ethNeeded * feeBps) / 10000;  // BUG: fee on net, not gross
        totalCost = ethNeeded + fee;          // totalCost < intended
    }
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Calculate totalCost inclusive of fee, then derive fee
if (trueOrderSize > maxRemainingTokens) {
    trueOrderSize = maxRemainingTokens;
    uint256 ethNeeded = Y1 - virtualEthLiquidity;
    
    totalCost = (10000 * ethNeeded) / (10000 - feeBps);  // Gross-up
    fee = totalCost - ethNeeded;                           // Correct fee
}
```

### Detection Patterns
```
- fee = (amount * feeBps) / 10000 followed by totalCost = amount + fee
- Edge case handling when buy exceeds maxRemainingTokens
- Fee recalculation path that uses net amount instead of gross
```

---

## 2. Last Buy Fee Mismatch on Bonding Curve

### Overview

In Solana bonding curves, the fee is calculated on `exact_in_amount` before `apply_buy()`, but the "last buy" adjusts the actual SOL consumed to fit exactly on the curve—making the pre-computed fee incorrect.

> 📖 Reference: `reports/bonding_curve_findings/m-01-last-buy-on-bonding-curve-may-have-an-incorrect-fee-calculation.md`

### Vulnerable Pattern Examples

**Example 1: Pre-Computed Fee Diverges from Actual** [MEDIUM]
```rust
// ❌ VULNERABLE: Fee calculated before actual amount is known
fee_lamports = bonding_curve.calculate_fee(exact_in_amount, clock.slot)?;
buy_amount_applied = exact_in_amount - fee_lamports;

// apply_buy may adjust sol_amount for "last buy" scenario
let buy_result = ctx.accounts.bonding_curve.apply_buy(buy_amount_applied)?;
// buy_result.sol_amount != buy_amount_applied for last buy!
```

### Secure Implementation

```rust
// ✅ SECURE: Recalculate fee after apply_buy if amounts differ
let buy_result = ctx.accounts.bonding_curve.apply_buy(buy_amount_applied)?;
if buy_result.sol_amount != buy_amount_applied {
    fee_lamports = bonding_curve.calculate_fee(buy_result.sol_amount, clock.slot)?;
}
```

---

## 3. Swap Fee Omitted in Order Reflections

### Overview

An orderbook DEX that `reflect_curve`s a bonding curve's reserves into passive orders may omit the `(1-f)` swap fee factor when sizing those reflected orders. Takers fill at the effective price without paying the fee, leaking LP fee revenue.

> 📖 Reference: `reports/bonding_curve_findings/m-1-omission-of-swap-fee-in-reflect_curve-causes-undervaluation-and-inconsistent.md`

### Vulnerable Pattern Examples

**Example 1: Missing Fee Factor in Order Sizing** [MEDIUM]
```rust
// ❌ VULNERABLE: Missing (1-f) multiplier on bid/ask sizing
// Bids — should be: s = R_q * (1 - f) / p - R_b
let size = quote_reserve_div_price.checked_sub(base_reserve).ok()?;

// Asks — should be: s = R_b * (1 - f) - R_q / p
let size = base_reserve.checked_sub(quote_reserve_div_price).ok()?;
```

### Secure Implementation

```rust
// ✅ SECURE: Include fee factor in order calculation
let fee_adjusted_quote = quote_reserve.checked_mul(1_000_000 - fee_rate)? / 1_000_000;
let size = fee_adjusted_quote.checked_div(price)?.checked_sub(base_reserve).ok()?;
```

---

## 4. Inconsistent Fee Between Quoter and Execution

### Overview

When a DEX has separate quoter and execution contracts, fee logic must be identical. If the quoter applies a hook fee modifier but execution doesn't (or vice versa), users receive worse execution than quoted.

> 📖 Reference: `reports/bonding_curve_findings/m-03-inconsistent-swap-fee-implementation-in-virtual-bonding-curve.md`

### Vulnerable Pattern Examples

**Example 1: Quoter vs Hook Fee Mismatch** [MEDIUM]
```solidity
// ❌ VULNERABLE: Quoter adds hook fee but execution doesn't
// BunniQuoter::quoteSwap:
swapFee += uint24(hookFeesBaseSwapFee.mulDivUp(hookFeeModifier, MODIFIER_BASE));

// BunniHookLogic::beforeSwap:
// Does NOT add hookFeeModifier to swapFee!

// Additionally, quoter omits curator fee deduction:
// curatorFeeAmount = baseSwapFeeAmount.mulDivUp(curatorFees.feeRate, CURATOR_FEE_BASE);
```

### Secure Implementation

```solidity
// ✅ SECURE: Extract fee calculation into shared library
library FeeLib {
    function computeEffectiveFee(uint24 baseFee, uint24 hookMod, uint24 curatorRate) 
        internal pure returns (uint24 effectiveFee, uint256 curatorFee) 
    {
        effectiveFee = baseFee + uint24(uint256(baseFee).mulDivUp(hookMod, MODIFIER_BASE));
        curatorFee = uint256(baseFee).mulDivUp(curatorRate, CURATOR_FEE_BASE);
    }
}
```

### Detection Patterns
```
- Separate quoter and executor contracts with duplicated fee logic
- Hook fee modifiers applied in one path but not another
- Curator/protocol fee subtracted inconsistently
```

---

## 5. Expansion Mint Precision Loss Causes DOS

### Overview

When `reserveRatio` is stored at lower precision (e.g., 1e8) but computed at higher precision (1e18), the downscaling truncation changes the effective price after each expansion mint. Over time, the drift accumulates and can cause the system to fail invariant checks.

> 📖 Reference: `reports/bonding_curve_findings/m-2-rounding-issue-in-bonding-curves-mintfromexpansion-can-cause-a-permanent-dos.md`

### Vulnerable Pattern Examples

**Example 1: Precision Loss in Reserve Ratio Storage** [MEDIUM]
```solidity
// ❌ VULNERABLE: newRatio computed at 1e18, stored at 1e8 precision
uint256 newRatio = reserveRatioScalar * currentRatio / 1e18;  // Full precision
exchange.reserveRatio = uint32(newRatio / 1e10);               // Truncated to 1e8

// Next call: price = reserve / (supply * reserveRatio)
// reserveRatio has lost 10 digits of precision → price drifts
```

### Secure Implementation

```solidity
// ✅ SECURE: Truncate BEFORE using for calculations
uint256 newRatio = reserveRatioScalar * currentRatio / 1e18;
newRatio = (newRatio / 1e10) * 1e10;  // Pre-truncate to storage precision
// Now use newRatio for minting calculations, ensuring consistency
exchange.reserveRatio = uint32(newRatio / 1e10);
```

---

## 6. Root/Exponent Library Truncation Compounds Error

### Overview

Mathematical libraries for computing cube roots, square roots, or fractional exponents may truncate intermediate results. When these are chained (e.g., `cubeRoot` then `square`, or `sqrt` then `cube`), the error compounds significantly, causing the bonding curve's `getAmountOut` to be systematically biased.

> 📖 Reference: `reports/bonding_curve_findings/m03-roots-library-is-inaccurate.md`

### Vulnerability Description

#### Root Cause
`twoThirdsRoot(x)` computes `cubeRoot(x)^2` — the truncation in `cubeRoot` is squared. Similarly, `threeHalfsRoot(x)` computes `sqrt(x)^3` — truncation is cubed. Both propagate large downward bias into bonding curve pricing.

### Vulnerable Pattern Examples

**Example 1: Truncation Before Exponentiation** [MEDIUM]
```solidity
// ❌ VULNERABLE: cubeRoot truncates, then squaring amplifies the error
function twoThirdsRoot(uint256 x) internal pure returns (uint256) {
    return cubeRoot(x) ** 2;  // Error from cubeRoot is squared
}

function threeHalfsRoot(uint256 x) internal pure returns (uint256) {
    return sqrt(x) ** 3;  // Error from sqrt is cubed
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Combine operations to minimize truncation
function twoThirdsRoot(uint256 x) internal pure returns (uint256) {
    // Compute x^(2/3) directly instead of chaining cubeRoot + square
    return nthRoot(x * x, 3);  // Single truncation step
}
```

### Detection Patterns
```
- Chained root/power operations: cubeRoot(x)**2, sqrt(x)**3
- Integer arithmetic roots used in pricing formulas
- Libraries that truncate intermediate results before exponentiation
```

---

## 7. Invariant Rounding Direction Mismatch

### Overview

When a vault computes an AMM pool's invariant with `roundUp = true` but the pool itself always rounds down, the vault's notion of "fair price" diverges from the pool's actual invariant. This can mask pool manipulation or allow free-riding.

> 📖 Reference: `reports/bonding_curve_findings/h-2-rounding-in-the-wrong-direction-in-fcashinvariant-leads-to-the-ability-to-fr.md`

### Vulnerable Pattern Examples

**Example 1: Notional vs Balancer Invariant Mismatch** [HIGH]
```solidity
// ❌ VULNERABLE: Notional rounds up, Balancer always rounds down
// Notional's oracle check:
uint256 invariant = StableMath._calculateInvariant(
    oracleContext.ampParam, 
    balances, 
    true  // roundUp = true
);

// Balancer's ComposableStablePool (V2+):
// Always rounds DOWN, no parameter for direction
```

### Detection Patterns
```
- External protocol calling StableMath._calculateInvariant with roundUp=true
- Invariant computed in vault doesn't match invariant in the underlying pool
- Any integration comparing invariants computed with different rounding
```

---

## 8. Underpriced Quote via Integer Division Truncation

### Overview

A constant-product bonding curve's `_getQuoteAmount` returns `(quoteReserve * baseAmount) / baseReserveAfter`, which truncates toward zero. For buy operations, this means the buyer pays less than the ideal price. Repeated small buys compound the error, draining the curve.

> 📖 Reference: `reports/bonding_curve_findings/m-23-underpriced-quote-in-bondingcurve-due-to-rounding-error.md`

### Vulnerable Pattern Examples

**Example 1: Rounding Down on Buys** [MEDIUM]
```solidity
// ❌ VULNERABLE: Integer division always truncates — favors buyer
function _getQuoteAmount(
    uint256 baseAmount, 
    uint256 quoteReserve, 
    uint256 baseReserve, 
    bool isBuy
) internal pure returns (uint256 quoteAmount) {
    uint256 baseReserveAfter = isBuy 
        ? baseReserve - baseAmount 
        : baseReserve + baseAmount;
    return (quoteReserve * baseAmount) / baseReserveAfter;  // Rounds down
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Round up for buys, round down for sells (favor protocol)
function _getQuoteAmount(
    uint256 baseAmount, 
    uint256 quoteReserve, 
    uint256 baseReserve, 
    bool isBuy
) internal pure returns (uint256 quoteAmount) {
    uint256 baseReserveAfter = isBuy 
        ? baseReserve - baseAmount 
        : baseReserve + baseAmount;
    uint256 numerator = quoteReserve * baseAmount;
    if (isBuy) {
        // Round UP for buys — protocol collects slightly more
        quoteAmount = (numerator + baseReserveAfter - 1) / baseReserveAfter;
    } else {
        quoteAmount = numerator / baseReserveAfter;
    }
}
```

### Detection Patterns
```
- Integer division in getAmountOut/getQuoteAmount without rounding consideration
- Same rounding direction for both buys and sells
- No use of mulDivUp/ceilDiv for buyer-pays calculations
```

---

## 9. Invariant Check Invalidated by Rent Inclusion

### Overview

On Solana, `sol_escrow.lamports()` includes the rent-exemption deposit. If the bonding curve's invariant check compares this (rent-inclusive) value against `real_sol_reserves` (rent-exclusive), the check is weaker than intended and can pass when actual available SOL is insufficient.

> 📖 Reference: `reports/bonding_curve_findings/m-02-bonding-curve-invariant-check-incorrectly-validates-sol-balance-due-to-rent.md`

### Vulnerable Pattern Examples

**Example 1: Rent Inflates Invariant Check** [MEDIUM]
```rust
// ❌ VULNERABLE: lamports() includes rent, real_sol_reserves does not
let sol_escrow_lamports = sol_escrow.lamports();  // Includes ~0.002 SOL rent
if sol_escrow_lamports < bonding_curve.real_sol_reserves {
    return Err(ContractError::BondingCurveInvariant.into());
}
// Passes even when actual available SOL < real_sol_reserves by up to rent amount
```

### Secure Implementation

```rust
// ✅ SECURE: Subtract rent before comparing
let rent = Rent::get()?.minimum_balance(8 + BondingCurve::INIT_SPACE as usize);
let bonding_curve_pool_lamports = sol_escrow.lamports() - rent;
if bonding_curve_pool_lamports < bonding_curve.real_sol_reserves {
    return Err(ContractError::BondingCurveInvariant.into());
}
```

### Detection Patterns
```
- account.lamports() compared to a "real" or "virtual" reserve value
- Missing rent subtraction in Solana balance checks
- Invariant checks that use raw lamport balance
```

---

## 10. Fee Reward Dust Permanently Stuck in Contract

### Overview

When fee distribution uses `cumulativeFeePerToken += (msg.value * PRECISION) / totalSupply`, integer division truncation creates dust that can never be claimed. With no sweep mechanism, rewards accumulate in the contract forever.

> 📖 Reference: `reports/bonding_curve_findings/m-05-feesplitter-reward-tokens-can-become-stuck-in-the-contract.md`

### Vulnerable Pattern Examples

**Example 1: Integer Division Dust in Fee Accumulator** [MEDIUM]
```solidity
// ❌ VULNERABLE: Division truncation creates permanent dust
function addFees(address token) public payable onlyManager {
    uint256 totalSupply_ = totalSupply(token);
    TokenData storage data = tokensData[token];
    data.cumulativeFeePerToken += (msg.value * PRECISION) / totalSupply_;
    // Lost dust per call: msg.value - (msg.value * PRECISION / totalSupply_ * totalSupply_ / PRECISION)
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Track unallocated dust and re-add it next time
function addFees(address token) public payable onlyManager {
    uint256 totalSupply_ = totalSupply(token);
    TokenData storage data = tokensData[token];
    uint256 amountWithDust = msg.value + data.pendingDust;
    uint256 perToken = (amountWithDust * PRECISION) / totalSupply_;
    data.pendingDust = amountWithDust - (perToken * totalSupply_ / PRECISION);
    data.cumulativeFeePerToken += perToken;
}
```

### Detection Patterns
```
- cumulativeFeePerToken += (value * PRECISION) / totalSupply without dust tracking
- No sweep/withdraw mechanism for contract balance
- Fee splitter contracts without dust re-accumulation
```

---

## 11. Fee-on-Transfer Token Accounting Mismatch

### Overview

When a bonding curve tracks buy/sell amounts using the input parameter rather than the actual received amount, fee-on-transfer tokens cause the internal accounting to overstate reserves, leading to either failed withdrawals or arbitrage opportunities.

### Vulnerable Pattern Examples

**Example: Trusting Input Amount Instead of Actual** [MEDIUM]
```solidity
// ❌ VULNERABLE: Assumes full amount is received
function buy(uint256 amount) external {
    token.transferFrom(msg.sender, address(this), amount);
    reserves += amount;  // BUG: actual received = amount - transferFee
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Measure actual received amount
function buy(uint256 amount) external {
    uint256 balBefore = token.balanceOf(address(this));
    token.transferFrom(msg.sender, address(this), amount);
    uint256 received = token.balanceOf(address(this)) - balBefore;
    reserves += received;
}
```

---

## Prevention Guidelines

### Development Best Practices
1. **Always gross-up fee calculations** — compute `totalCost = netAmount * 10000 / (10000 - feeBps)`, then derive fee
2. **Round in favor of the protocol** — use `ceilDiv` for amounts the user pays, `floorDiv` for amounts the user receives
3. **Match rounding direction** across all integrations (vault, pool, oracle)
4. **Subtract rent** from Solana account balances before invariant checks
5. **Track division dust** in fee accumulators to prevent permanent lockup
6. **Measure actual received amounts** for fee-on-transfer token compatibility
7. **Extract shared fee logic** into libraries used by both quoter and executor

### Testing Requirements
- Test fee calculation when buy exceeds remaining tokens
- Test rounding direction for both buy and sell paths
- Test invariant checks with rent-inclusive balances
- Test fee dust accumulation over many small transactions
- Test quoter vs execution fee consistency

### Keywords for Search

`fee calculation`, `rounding`, `precision`, `feeBps`, `cumulativeFeePerToken`, `integer division`, `truncation`, `roundUp`, `ceilDiv`, `dust`, `fee-on-transfer`, `swap fee`, `hook fee`, `curator fee`, `reserveRatio`, `invariant`, `rent`, `lamports`, `cubeRoot`, `expansion mint`, `underpriced quote`, `getQuoteAmount`

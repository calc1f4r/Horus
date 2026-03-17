---
# Core Classification (Required)
protocol: generic
chain: sui
category: arithmetic_precision
vulnerability_type: overflow|precision_loss|rounding|faulty_constant

# Attack Vector Details (Required)
attack_type: data_manipulation|logical_error
affected_component: math_operations|type_casting|reward_calculation|price_calculation|share_accounting

# Technical Primitives (Required)
primitives:
  - u64
  - u128
  - u256
  - MAX_U64
  - checked_shlw
  - get_delta_a
  - get_delta_b
  - mul_div
  - ceil_div
  - floor_div
  - sqrt_price
  - liquidity
  - tick_math
  - full_math
  - clmm_math
  - redeem_rate
  - exchange_rate

# Impact Classification (Required)
severity: high
impact: fund_loss|protocol_insolvency|dos|incorrect_accounting
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - sui
  - move
  - arithmetic
  - overflow
  - precision
  - rounding
  - defi
  - amm
  - clmm
  - vault
  - staking
  - rewards

# Version Info
language: move
version: all

# Pattern Identity (Required)
root_cause_family: arithmetic_error
pattern_key: arithmetic_error | math_operations | overflow

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - MAX_U64
  - calculate_epoch_reward
  - calculate_rewards
  - calculate_share
  - ceil_div
  - checked_shlw
  - clmm_math
  - convert_amount
  - deposit
  - exchange_rate
  - execute
  - execute_trade
  - fill_order
  - floor_div
  - full_math
  - get_delta_a
  - get_delta_b
  - get_price
  - get_sui_for_shares
  - get_sui_for_shares_round_up
---

## References & Source Reports

> **For Agents**: Read the full report for each finding at the referenced path.

### Integer Overflow Vulnerabilities
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Overflow in Calculating Delta B | `reports/sui_move_findings/overflow-in-calculating-delta-b.md` | HIGH | OtterSec | Cetus CLMM |
| Overflow in Calculation of Delta A | `reports/sui_move_findings/overflow-in-calculation-of-delta-a.md` | MEDIUM | OtterSec | Cetus CLMM |
| BigVector Size Overflow | `reports/sui_move_findings/bigvector-size-overflow.md` | MEDIUM | OtterSec | DeepBook V3 |
| Possible Overflow Due to Exceeding Type Limit | `reports/sui_move_findings/possible-overflow-due-to-exceeding-the-type-limit.md` | MEDIUM | OtterSec | Security Token |
| Potential Overflow in Threshold | `reports/sui_move_findings/potential-overflow-in-threshold.md` | MEDIUM | OtterSec | Mysten Labs Sui |
| RPC Node Crash Due to Overflow | `reports/sui_move_findings/rpc-node-crashes-due-to-an-overflow.md` | HIGH | OtterSec | Mysten Labs Sui |
| Risk of Arithmetic Overflow | `reports/sui_move_findings/risk-of-arithmetic-overflow.md` | HIGH | OtterSec | Aftermath Finance |
| Volume Overflow Risk | `reports/sui_move_findings/volume-overflow-risk.md` | MEDIUM | OtterSec | DeepBook V3 |
| Faulty Constant Definition | `reports/sui_move_findings/faulty-constant-definition.md` | HIGH | OtterSec | BlueFin |

### Precision Loss / Rounding Vulnerabilities
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Precision Loss in Redistribution | `reports/sui_move_findings/precision-loss-in-redistribution.md` | MEDIUM | OtterSec | Bucket Protocol |
| Rounding Errors Result in Lost Accrued Rewards | `reports/sui_move_findings/rounding-errors-result-in-lost-accrued-rewards.md` | MEDIUM | OtterSec | Sui Core |
| Round Up Shares | `reports/sui_move_findings/round-up-shares.md` | HIGH | OtterSec | Volo |
| Share Price Inflation | `reports/sui_move_findings/share-price-inflation.md` | MEDIUM | OtterSec | BlueFin |
| Share Price Manipulation | `reports/sui_move_findings/share-price-manipulation.md` | HIGH | OtterSec | BlueFin |

### Incorrect Calculation / Conversion Vulnerabilities
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Improper Conversion | `reports/sui_move_findings/improper-conversion.md` | HIGH | OtterSec | Bucket Protocol |
| Incorrect Price Calculation | `reports/sui_move_findings/incorrect-price-calculation.md` | HIGH | OtterSec | Aftermath Finance |
| Incorrect Base Quantity Calculation | `reports/sui_move_findings/incorrect-base-quantity-calculation.md` | HIGH | OtterSec | DeepBook V3 |
| Incorrectly Calculated Reward Period | `reports/sui_move_findings/incorrectly-calculated-reward-period.md` | MEDIUM | OtterSec | Turbos Finance |

### Artifacts Index
| Artifact | Source | Type |
|----------|--------|------|
| `artifacts/6-sherlock-contest-857.html` | Deepbook V3 Sherlock Contest | HTML |
| `artifacts/2-github.com-AftermathFinance-aftermath-core-.html` | Aftermath Finance GitHub | HTML |
| `artifacts/4-github.com-Bucket-Protocol-v1-periphery-2f6.html` | Bucket Protocol GitHub | HTML |
| `artifacts/5-github.com-MystenLabs-deepbookv3-77d3d535.html` | DeepBook V3 GitHub | HTML |

---

# Sui Move Arithmetic, Precision & Overflow Vulnerabilities — Comprehensive Database

**A Complete Pattern-Matching Guide for Mathematical Safety in Sui/Move DeFi**

---

## Table of Contents

1. [CLMM Sqrt-Price Overflow](#1-clmm-sqrt-price-overflow)
2. [CLMM Delta Computation Overflow](#2-clmm-delta-computation-overflow)
3. [BigVector / Container Size Overflow](#3-bigvector--container-size-overflow)
4. [Accumulator / Volume Counter Overflow](#4-accumulator--volume-counter-overflow)
5. [Type Boundary Overflow (u64 → u128)](#5-type-boundary-overflow-u64--u128)
6. [RPC / Node-Crash Overflow](#6-rpc--node-crash-overflow)
7. [Faulty Constant Definitions](#7-faulty-constant-definitions)
8. [Precision Loss in Token Redistribution](#8-precision-loss-in-token-redistribution)
9. [Reward Calculation Rounding Errors](#9-reward-calculation-rounding-errors)
10. [Share Price Inflation / First-Depositor Attack](#10-share-price-inflation--first-depositor-attack)
11. [Share-to-Asset Rounding Direction](#11-share-to-asset-rounding-direction)
12. [Incorrect Price Scaling / Conversion](#12-incorrect-price-scaling--conversion)
13. [Incorrect Quantity Calculation in Order Books](#13-incorrect-quantity-calculation-in-order-books)
14. [Reward Period Miscalculation](#14-reward-period-miscalculation)
15. [Improper Integer Type Conversion](#15-improper-integer-type-conversion)

---

## 1. CLMM Sqrt-Price Overflow

### Overview

Concentrated Liquidity Market Maker (CLMM) protocols like Cetus compute token deltas using square root price values. Intermediate computations can overflow u128 or u256 when the price range is extreme (near MIN_TICK or MAX_TICK).

> **Validation strength**: Strong — 2 reports from OtterSec on Cetus CLMM
> **Frequency**: 2/69 reports



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of arithmetic_error"
- Pattern key: `arithmetic_error | math_operations | overflow`
- Interaction scope: `single_contract`
- Primary affected component(s): `math_operations|type_casting|reward_calculation|price_calculation|share_accounting`
- High-signal code keywords: `MAX_U64`, `calculate_epoch_reward`, `calculate_rewards`, `calculate_share`, `ceil_div`, `checked_shlw`, `clmm_math`, `convert_amount`
- Typical sink / impact: `fund_loss|protocol_insolvency|dos|incorrect_accounting`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `math_operations.function -> price_calculation.function -> reward_calculation.function`
- Trust boundary crossed: `internal`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: Arithmetic operation on user-controlled input without overflow protection
- Signal 2: Casting between different-width integer types without bounds check
- Signal 3: Multiplication before division where intermediate product can exceed type max
- Signal 4: Accumulator variable can wrap around causing incorrect accounting

#### False Positive Guards

- Not this bug when: Solidity >= 0.8.0 with default checked arithmetic
- Safe if: SafeMath library used for all arithmetic on user-controlled values
- Requires attacker control of: specific conditions per pattern

### Vulnerability Description

#### Root Cause

`get_delta_b` computes `liquidity * (sqrt_price_b - sqrt_price_a)` which can overflow when liquidity is large and the tick range approaches extreme values. The `checked_shlw` implementation may also fail to properly detect overflow.

#### Attack Scenario

1. Create or interact with a pool at extreme tick ranges (near MIN_TICK = -443636 or MAX_TICK = 443636)
2. Provide large liquidity values
3. Delta computation overflows, producing incorrect token amounts
4. Swap operates with corrupted amounts, draining pools

### Vulnerable Pattern Examples

**Example 1: Delta B Overflow in CLMM** [HIGH]
> 📖 Reference: `reports/sui_move_findings/overflow-in-calculating-delta-b.md`
```move
// ❌ VULNERABLE: Multiplication can overflow u128/u256
public fun get_delta_b(
    sqrt_price_a: u128,
    sqrt_price_b: u128,
    liquidity: u128,
    round_up: bool
): u64 {
    let diff = if (sqrt_price_a > sqrt_price_b) {
        sqrt_price_a - sqrt_price_b
    } else {
        sqrt_price_b - sqrt_price_a
    };
    // This multiplication overflows when liquidity * diff > MAX_U128
    let result = full_math_u128::mul_div_floor(liquidity, diff, (1u128 << 64));
    (result as u64)
}
```

**Example 2: Delta A Overflow from checked_shlw** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/overflow-in-calculation-of-delta-a.md`
```move
// ❌ VULNERABLE: checked_shlw does not properly detect overflow
public fun get_delta_a(
    sqrt_price_a: u128,
    sqrt_price_b: u128,
    liquidity: u128,
    round_up: bool
): u64 {
    let sqrt_price_diff = sqrt_price_b - sqrt_price_a;
    // checked_shlw(liquidity, 64) can overflow
    let numerator = math_u256::checked_shlw(u256::from_u128(liquidity), 64);
    let quotient = full_math_u256::mul_div_floor(
        numerator,
        u256::from_u128(sqrt_price_diff),
        u256::from_u128(sqrt_price_b)
    );
    (u256::as_u64(quotient))
}
```

### Impact Analysis

#### Technical Impact
- Pool state corrupted with incorrect token delta computations
- Swaps execute with wrong amounts, allowing value extraction
- Liquidity providers receive wrong amounts on position changes

#### Financial Impact
- Direct fund loss from incorrect swap amounts (HIGH, 2/69 reports)
- Pool insolvency if exploited systematically

### Secure Implementation

**Fix: Use Wider Types and Explicit Overflow Checks**
```move
// ✅ SECURE: Use u256 throughout and assert no truncation
public fun get_delta_b(
    sqrt_price_a: u128,
    sqrt_price_b: u128,
    liquidity: u128,
    round_up: bool
): u64 {
    let diff = if (sqrt_price_a > sqrt_price_b) {
        sqrt_price_a - sqrt_price_b
    } else {
        sqrt_price_b - sqrt_price_a
    };
    // Compute in u256 to prevent intermediate overflow
    let result_256 = (liquidity as u256) * (diff as u256) / ((1u256 << 64));
    assert!(result_256 <= (MAX_U64 as u256), E_OVERFLOW);
    if (round_up && (liquidity as u256) * (diff as u256) % ((1u256 << 64)) > 0) {
        ((result_256 + 1) as u64)
    } else {
        (result_256 as u64)
    }
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- get_delta_a / get_delta_b using u128 multiplication
- checked_shlw without post-check assertions
- full_math mul_div operations near type boundaries
- CLMM tick math at extreme tick values (±443636)
- Casting u128/u256 results to u64 without bounds check
```

#### Audit Checklist
- [ ] Verify all intermediate CLMM math uses u256 to prevent overflow
- [ ] Test delta calculations at MIN_TICK and MAX_TICK boundaries
- [ ] Check checked_shlw implementation for correct overflow detection
- [ ] Verify result truncation from u256→u64 has explicit guards
- [ ] Fuzz with maximum liquidity values at extreme tick ranges

---

## 2. CLMM Delta Computation Overflow

See [Section 1](#1-clmm-sqrt-price-overflow) — this section covers the same pattern with additional delta_a-specific variants.

> **Frequency**: Combined 2/69 reports for delta_a and delta_b overflow

---

## 3. BigVector / Container Size Overflow

### Overview

DeepBook V3's BigVector (a B-tree-like data structure for order books) uses configurable `max_slice_size` and `max_fan_out` parameters. Improper choices cause internal nodes to exceed Sui's 256KB object size limit.

> **Validation strength**: Moderate — 1 report from OtterSec on DeepBook V3
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Effective Slice Size Overflow** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/bigvector-size-overflow.md`
```move
// ❌ VULNERABLE: depth > 0 causes max_slice_size ^ (depth + 1) nodes
// BigVector with max_slice_size=64, max_fan_out=64
// At depth 2: up to 64*64 = 4096 items per leaf → exceeds 256KB
let book = big_vector::empty<Order>(64, 64, ctx);
// Effective max_slice_size = 64^2 = 4,096 at one level of nesting
```

### Secure Implementation

```move
// ✅ SECURE: Size parameters chosen to stay under 256KB at maximum depth
// Assuming each Order ~ 100 bytes: 256,000 / 100 = 2560 max items per leaf
let book = big_vector::empty<Order>(1000, 256, ctx);
// max_slice_size=1000 ensures 1000 * 100 = 100KB per leaf (well under limit)
```

---

## 4. Accumulator / Volume Counter Overflow

### Overview

Volume tracking fields using u64 can overflow when cumulative trading volumes are high. A single 8 ETH trade generating 8 * 10^18 volume units can quickly approach the u64 maximum.

> **Validation strength**: Moderate — 1 report from OtterSec on DeepBook V3
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Volume Tracking Overflow** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/volume-overflow-risk.md`
```move
// ❌ VULNERABLE: u64 volume accumulator overflows with high-volume pairs
struct Pool has key, store {
    // ...
    total_volume: u64,  // MAX_U64 = 1.84 * 10^19
    // For a SUI/USDC pair: 8 ETH trade = 8 * 10^18 → only ~2 trades to overflow
}

public fun execute_trade(pool: &mut Pool, quantity: u64) {
    // ...
    pool.total_volume = pool.total_volume + quantity;  // OVERFLOW
}
```

### Secure Implementation

```move
// ✅ SECURE: Use u128 or u256 for volume accumulators
struct Pool has key, store {
    total_volume: u128,  // MAX_U128 = 3.4 * 10^38 → safe for all practical volumes
}

public fun execute_trade(pool: &mut Pool, quantity: u64) {
    pool.total_volume = pool.total_volume + (quantity as u128);
}
```

---

## 5. Type Boundary Overflow (u64 → u128)

### Overview

Several Sui protocols store values that can exceed u64 (1.84 × 10^19) during normal operation, especially when combining large token amounts with timestamp-based multipliers or precision scales.

> **Validation strength**: Moderate — 2 reports across Security Token and Aftermath
> **Frequency**: 2/69 reports

### Vulnerable Pattern Examples

**Example 1: Reward Scaling Exceeds u64** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/possible-overflow-due-to-exceeding-the-type-limit.md`
```move
// ❌ VULNERABLE: amount * PRECISION can exceed u64
const PRECISION: u64 = 1_000_000_000_000;  // 10^12
public fun calculate_share(amount: u64, total: u64): u64 {
    amount * PRECISION / total  // If amount > 1.84 * 10^7, overflows u64
}
```

**Example 2: Threshold Overflow in Sui Core** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/potential-overflow-in-threshold.md`
```move
// ❌ VULNERABLE: Stress test may use voting_power near u64 max
let threshold = (2 * total_voting_power / 3) + 1;
// If total_voting_power > MAX_U64 / 2, this overflows
```

### Secure Implementation

```move
// ✅ SECURE: Use u128 for intermediate calculations
public fun calculate_share(amount: u64, total: u64): u64 {
    let result = (amount as u128) * (PRECISION as u128) / (total as u128);
    assert!(result <= (MAX_U64 as u128), E_OVERFLOW);
    (result as u64)
}
```

---

## 6. RPC / Node-Crash Overflow

### Overview

An overflow in the Sui RPC node's coin selection algorithm causes the node to crash, enabling denial of service against any node.

> **Validation strength**: Strong — 1 report from OtterSec on Sui Core
> **Frequency**: 1/69 reports (L1-level severity)

### Vulnerable Pattern Examples

**Example 1: Coin Selection Overflow Crash** [HIGH]
> 📖 Reference: `reports/sui_move_findings/rpc-node-crashes-due-to-an-overflow.md`
```rust
// ❌ VULNERABLE (Rust, Sui fullnode): Unchecked subtraction in select_coins
fn select_coins(coins: &[CoinData], amount: u64) -> Vec<ObjectID> {
    let mut remaining = amount;
    for coin in coins {
        if remaining == 0 { break; }
        remaining -= coin.balance;  // PANICS if coin.balance > remaining
        // This happens when a single coin exceeds the requested amount
    }
}
```

### Secure Implementation

```rust
// ✅ SECURE: Use saturating subtraction
fn select_coins(coins: &[CoinData], amount: u64) -> Vec<ObjectID> {
    let mut remaining = amount;
    for coin in coins {
        if remaining == 0 { break; }
        remaining = remaining.saturating_sub(coin.balance);
        result.push(coin.id);
    }
    result
}
```

---

## 7. Faulty Constant Definitions

### Overview

A missing character in a constant definition caused MAX_U64 to be incorrectly defined as 1844674407370955161 instead of 18446744073709551615, off by a factor of 10.

> **Validation strength**: Strong — 1 report from OtterSec on BlueFin
> **Frequency**: 1/69 reports (common mistake, high impact)

### Vulnerable Pattern Examples

**Example 1: MAX_U64 Off by 10x** [HIGH]
> 📖 Reference: `reports/sui_move_findings/faulty-constant-definition.md`
```move
// ❌ VULNERABLE: Missing digit — value is 10x too small
const MAX_U64: u64 = 1844674407370955161;   // Missing final '5'
// Correct: 18446744073709551615

// Impact: Any overflow check using this constant is bypassable
fun safe_mul(a: u64, b: u64): u64 {
    assert!(a <= MAX_U64 / b, E_OVERFLOW);  // Check is 10x too permissive
    a * b
}
```

### Secure Implementation

```move
// ✅ SECURE: Use built-in constants or verify manually
const MAX_U64: u64 = 18446744073709551615;  // 2^64 - 1
// Or use: 0xFFFFFFFFFFFFFFFF
// Or use: (1u128 << 64 - 1) as u64 in a test to verify

#[test]
fun test_max_u64() {
    assert!(MAX_U64 == 18446744073709551615, 0);
}
```

### Detection Patterns

```
- Manually defined MAX_U64, MAX_U128 constants (verify each digit)
- Constants used in overflow checks are critical — any error negates the check
- Prefer hex representation (0xFFFFFFFFFFFFFFFF) for readability
```

---

## 8. Precision Loss in Token Redistribution

### Overview

When distributing rewards or redistributing tokens across multiple holders, dividing by total quantities first causes precision loss. The "dust" from rounding is effectively lost.

> **Validation strength**: Moderate — 1 report from OtterSec on Bucket Protocol
> **Frequency**: 1/69 reports (generalizable DeFi pattern)

### Vulnerable Pattern Examples

**Example 1: Redistribution Rounding Loss** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/precision-loss-in-redistribution.md`
```move
// ❌ VULNERABLE: Integer division truncates, losing dust
public fun redistribute(tank: &mut Tank, amount: u64) {
    let per_unit = amount / tank.total_collateral;  // Truncation here
    // If amount = 100, total_collateral = 30, per_unit = 3 (lost 10)
    let i = 0;
    while (i < vector::length(&tank.depositors)) {
        let depositor = vector::borrow_mut(&mut tank.depositors, i);
        depositor.balance = depositor.balance + per_unit * depositor.share;
        i = i + 1;
    };
    // Lost: amount - (per_unit * total_collateral) = 100 - 90 = 10
}
```

### Secure Implementation

```move
// ✅ SECURE: Track cumulative distribution and handle remainder
public fun redistribute(tank: &mut Tank, amount: u64) {
    let distributed = 0u64;
    let i = 0;
    while (i < vector::length(&tank.depositors)) {
        let depositor = vector::borrow_mut(&mut tank.depositors, i);
        let share_amount = (amount as u128) * (depositor.share as u128) / 
                          (tank.total_collateral as u128);
        depositor.balance = depositor.balance + (share_amount as u64);
        distributed = distributed + (share_amount as u64);
        i = i + 1;
    };
    // Remainder goes to dust collector or last depositor
    tank.dust = tank.dust + (amount - distributed);
}
```

---

## 9. Reward Calculation Rounding Errors

### Overview

Sui staking and reward systems accumulate rewards per-epoch. Small rounding errors in per-epoch calculations compound over time, leading to significant reward loss for stakers.

> **Validation strength**: Moderate — 1 report from OtterSec on Sui Core
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Truncated Reward Accrual** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/rounding-errors-result-in-lost-accrued-rewards.md`
```move
// ❌ VULNERABLE: Accumulated rounding dust is silently lost each epoch
public fun calculate_epoch_reward(
    pool_reward: u64,
    user_stake: u64,
    total_stake: u64
): u64 {
    user_stake * pool_reward / total_stake
    // Example: 99 * 100 / 1000 = 9 (lost 0.9)
    // Over 100 epochs: lost ~90 tokens
}
```

### Secure Implementation

```move
// ✅ SECURE: Use scaled accumulator pattern
struct RewardPool has store {
    accumulated_reward_per_share: u128,  // Scaled by PRECISION
    pending_dust: u64,
}

const PRECISION: u128 = 1_000_000_000_000;  // 10^12

public fun update_reward_per_share(pool: &mut RewardPool, reward: u64) {
    pool.accumulated_reward_per_share = pool.accumulated_reward_per_share + 
        (reward as u128) * PRECISION / (pool.total_stake as u128);
}

public fun pending_reward(pool: &RewardPool, user: &UserStake): u64 {
    let raw = (user.stake as u128) * pool.accumulated_reward_per_share / PRECISION;
    ((raw - user.reward_debt) as u64)
}
```

---

## 10. Share Price Inflation / First-Depositor Attack

### Overview

Classic first-depositor attack adapted to Sui Move vaults. The first depositor can inflate the share price by donating tokens directly, causing subsequent depositors to receive zero shares due to rounding.

> **Validation strength**: Strong — 2 reports from OtterSec on BlueFin
> **Frequency**: 2/69 reports (common DeFi pattern)

### Vulnerable Pattern Examples

**Example 1: Classic Share Inflation** [HIGH]
> 📖 Reference: `reports/sui_move_findings/share-price-manipulation.md`
```move
// ❌ VULNERABLE: No minimum deposit, shares round to zero
public fun deposit(vault: &mut Vault, coin: Coin<SUI>): u64 {
    let amount = coin::value(&coin);
    let shares = if (vault.total_shares == 0) {
        amount  // First depositor: 1 SUI = 1 share
    } else {
        amount * vault.total_shares / vault.total_assets
        // After attacker donates: 100 * 1 / 1_000_000 = 0 shares!
    };
    coin::put(&mut vault.balance, coin);
    vault.total_shares = vault.total_shares + shares;
    vault.total_assets = vault.total_assets + amount;
    shares
}
```

**Example 2: Share Price Drift Through Rounding** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/share-price-inflation.md`
```move
// ❌ VULNERABLE: Persistent rounding errors inflate share price over time
public fun process_withdrawal(vault: &mut Vault, shares: u64): u64 {
    let amount = shares * vault.total_assets / vault.total_shares;
    // Always rounds down → vault retains dust → share price slowly inflates
    vault.total_shares = vault.total_shares - shares;
    vault.total_assets = vault.total_assets - amount;
    amount
}
```

### Impact Analysis

- First depositor attack: subsequent depositors lose their entire deposit (HIGH, 1/69)
- Persistent rounding: slow share price inflation causing withdrawal losses (MEDIUM, 1/69)

### Secure Implementation

**Fix: Virtual Offset (ERC4626 Pattern Adapted to Move)**
```move
// ✅ SECURE: Virtual offset prevents the first-depositor inflation attack
const VIRTUAL_SHARES: u64 = 1_000_000;  // 10^6
const VIRTUAL_ASSETS: u64 = 1;

public fun deposit(vault: &mut Vault, coin: Coin<SUI>): u64 {
    let amount = coin::value(&coin);
    let shares = amount * (vault.total_shares + VIRTUAL_SHARES) / 
                 (vault.total_assets + VIRTUAL_ASSETS);
    assert!(shares > 0, E_ZERO_SHARES);
    coin::put(&mut vault.balance, coin);
    vault.total_shares = vault.total_shares + shares;
    vault.total_assets = vault.total_assets + amount;
    shares
}
```

---

## 11. Share-to-Asset Rounding Direction

### Overview

When converting between shares and assets in staking/vault protocols, the rounding direction must favor the protocol (round down on withdraw, round up on deposit). Incorrect rounding allows value extraction.

> **Validation strength**: Strong — 1 report from OtterSec on Volo
> **Frequency**: 1/69 reports (fundamental DeFi safety pattern)

### Vulnerable Pattern Examples

**Example 1: Rounding Down on Staking Mints Excess Shares** [HIGH]
> 📖 Reference: `reports/sui_move_findings/round-up-shares.md`
```move
// ❌ VULNERABLE: Rounds DOWN when calculating SUI needed for shares
// Users pay less SUI than they should for their shares
public fun get_sui_for_shares(total_sui: u64, total_shares: u64, shares: u64): u64 {
    shares * total_sui / total_shares  // Rounds DOWN → user pays less
}

// Correct direction depends on context:
// - Deposit (user → vault): round UP shares-to-asset to charge more
// - Withdraw (vault → user): round DOWN asset-to-shares to pay less
```

### Secure Implementation

```move
// ✅ SECURE: Round up when user is paying (deposit), round down when user is receiving
public fun get_sui_for_shares_round_up(total_sui: u64, total_shares: u64, shares: u64): u64 {
    let result = (shares as u128) * (total_sui as u128);
    let denominator = (total_shares as u128);
    let quotient = result / denominator;
    if (result % denominator > 0) { 
        ((quotient + 1) as u64)  // Round UP — user pays more
    } else { 
        (quotient as u64) 
    }
}
```

---

## 12. Incorrect Price Scaling / Conversion

### Overview

DeFi protocols on Sui often handle prices with different decimal scales. Incorrect conversion between scales (e.g., missing decimal adjustment, wrong exponent) corrupts all downstream calculations.

> **Validation strength**: Moderate — 1 report from OtterSec on Aftermath Finance
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Missing Decimal Adjustment** [HIGH]
> 📖 Reference: `reports/sui_move_findings/incorrect-price-calculation.md`
```move
// ❌ VULNERABLE: Price feed uses 8 decimals but pool expects 18 decimals
public fun get_price(oracle_price: u64): u64 {
    oracle_price  // Raw oracle value (8 decimals) used as 18-decimal price
    // Price is 10^10 too small → all calculations are wrong
}
```

### Secure Implementation

```move
// ✅ SECURE: Explicit decimal conversion
const ORACLE_DECIMALS: u8 = 8;
const PRICE_DECIMALS: u8 = 18;

public fun get_price(oracle_price: u64): u128 {
    let scale = math::pow(10, (PRICE_DECIMALS - ORACLE_DECIMALS as u8));
    (oracle_price as u128) * (scale as u128)
}
```

---

## 13. Incorrect Quantity Calculation in Order Books

### Overview

DeepBook V3's order book calculates base and quote quantities during order matching. Incorrect calculations in fill operations lead to wrong amounts being transferred.

> **Validation strength**: Strong — 2 reports from OtterSec on DeepBook V3
> **Frequency**: 2/69 reports

### Vulnerable Pattern Examples

**Example 1: Base Quantity Off-by-One** [HIGH]
> 📖 Reference: `reports/sui_move_findings/incorrect-base-quantity-calculation.md`
```move
// ❌ VULNERABLE: Uses wrong quantity field in fill calculation
public fun fill_order(order: &Order, fill_qty: u64): (u64, u64) {
    let base_qty = fill_qty;  // Should use order.quantity, not fill_qty
    let quote_qty = base_qty * order.price / PRICE_SCALE;
    (base_qty, quote_qty)  // Both values are wrong
}
```

**Example 2: Improper Order Quantity** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/improper-order-quantity-calculation.md`
```move
// ❌ VULNERABLE: quantity not updated correctly after partial fill
public fun process_partial_fill(order: &mut Order, filled: u64) {
    order.unfilled_quantity = order.original_quantity - filled;
    // BUG: should be order.unfilled_quantity - filled
    // After second partial fill, unfilled_quantity is wrong
}
```

### Secure Implementation

```move
// ✅ SECURE: Track unfilled quantity independently
public fun process_partial_fill(order: &mut Order, filled: u64) {
    assert!(filled <= order.unfilled_quantity, E_OVERFILL);
    order.unfilled_quantity = order.unfilled_quantity - filled;
    order.cumulative_filled = order.cumulative_filled + filled;
}
```

---

## 14. Reward Period Miscalculation

### Overview

Reward distribution protocols track active/inactive periods. Off-by-one errors in period calculations cause rewards to be distributed during periods when they shouldn't be, or not distributed when they should.

> **Validation strength**: Moderate — 1 report from OtterSec on Turbos Finance
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Wrong Reward Period Boundary** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/incorrectly-calculated-reward-period.md`
```move
// ❌ VULNERABLE: Inclusive vs exclusive boundary error
public fun calculate_rewards(
    start_time: u64,
    end_time: u64,
    current_time: u64,
    reward_rate: u64
): u64 {
    let elapsed = current_time - start_time;  // Should be min(current_time, end_time) - start_time
    elapsed * reward_rate
    // If current_time > end_time, distributes rewards beyond the intended period
}
```

### Secure Implementation

```move
// ✅ SECURE: Clamp to reward period boundaries
public fun calculate_rewards(
    start_time: u64,
    end_time: u64,
    current_time: u64,
    reward_rate: u64
): u64 {
    let effective_start = math::max(start_time, last_claim_time);
    let effective_end = math::min(end_time, current_time);
    if (effective_end <= effective_start) { return 0 };
    (effective_end - effective_start) * reward_rate
}
```

---

## 15. Improper Integer Type Conversion

### Overview

Move's type system allows explicit casts between integer types (u8, u64, u128, u256). When converting from wider to narrower types without bounds checking, values are silently truncated.

> **Validation strength**: Strong — 1 report from OtterSec on Bucket Protocol
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: u128 to u64 Truncation** [HIGH]
> 📖 Reference: `reports/sui_move_findings/improper-conversion.md`
```move
// ❌ VULNERABLE: Intermediate u128 result truncated to u64
public fun convert_amount(amount: u64, price: u64, decimals: u8): u64 {
    let intermediate = (amount as u128) * (price as u128);
    let scaled = intermediate / math::pow_u128(10, decimals);
    (scaled as u64)  // If scaled > MAX_U64, silently truncates!
}
```

### Secure Implementation

```move
// ✅ SECURE: Assert before truncation
public fun convert_amount(amount: u64, price: u64, decimals: u8): u64 {
    let intermediate = (amount as u128) * (price as u128);
    let scaled = intermediate / math::pow_u128(10, decimals);
    assert!(scaled <= (MAX_U64 as u128), E_OVERFLOW);
    (scaled as u64)
}
```

---

## Prevention Guidelines

### Development Best Practices
1. Use u128 or u256 for all intermediate arithmetic in DeFi calculations
2. Always round in the protocol's favor (up on deposit, down on withdrawal)
3. Use hex constants for MAX values (0xFFFFFFFFFFFFFFFF for MAX_U64) to prevent typos
4. Apply the virtual offset pattern for share-based vaults
5. Use scaled accumulators (10^12 precision) for reward distribution
6. Validate all type casts from wider to narrower integers
7. Test at extreme value boundaries (0, 1, MAX-1, MAX)
8. Track dust/remainder from divisions explicitly

### Testing Requirements
- Fuzz all arithmetic functions with extreme values (0, 1, MAX_U64, MAX_U128)
- Test CLMM math at MIN_TICK and MAX_TICK
- Verify first-depositor attack on all vault implementations
- Test volume accumulators with realistic high-volume scenarios
- Property test: `deposit(amount).withdraw() >= amount - 1` (max 1 wei loss)

---

### Keywords for Search

`overflow`, `underflow`, `precision`, `rounding`, `truncation`, `u64`, `u128`, `u256`, `MAX_U64`, `checked_shlw`, `get_delta_a`, `get_delta_b`, `sqrt_price`, `liquidity`, `mul_div`, `ceil_div`, `floor_div`, `share_price`, `inflation`, `first_depositor`, `virtual_offset`, `exchange_rate`, `redeem_rate`, `accumulator`, `volume`, `BigVector`, `max_slice_size`, `256KB`, `CLMM`, `tick_math`, `full_math`, `dust`, `remainder`, `type_cast`, `faulty_constant`, `reward_per_share`, `precision_loss`

### Related Vulnerabilities
- `DB/general/arithmetic/` — Generic integer overflow patterns
- `DB/amm/` — AMM-specific math vulnerabilities
- `DB/tokens/erc4626/` — ERC4626 vault inflation patterns (EVM equivalent)

### Detection Patterns

#### Code Patterns to Look For
```
- See vulnerable pattern examples above for specific code smells
- Check for missing validation on critical state-changing operations
- Look for assumptions about external component behavior
```

#### Audit Checklist
- [ ] Verify all state-changing functions have appropriate access controls
- [ ] Check for CEI pattern compliance on external calls
- [ ] Validate arithmetic operations for overflow/underflow/precision loss
- [ ] Confirm oracle data freshness and sanity checks

### Keywords for Search

> These keywords enhance vector search retrieval:

`MAX_U64`, `amm`, `arithmetic`, `arithmetic_precision`, `calculate_epoch_reward`, `calculate_rewards`, `calculate_share`, `ceil_div`, `checked_shlw`, `clmm`, `clmm_math`, `convert_amount`, `defi`, `deposit`, `exchange_rate`, `execute`, `execute_trade`, `fill_order`, `floor_div`, `full_math`, `get_delta_a`, `get_delta_b`, `get_price`, `get_sui_for_shares`, `get_sui_for_shares_round_up`, `liquidity`, `move`, `mul_div`, `overflow`, `overflow|precision_loss|rounding|faulty_constant`, `precision`, `redeem_rate`, `rewards`, `rounding`, `sqrt_price`, `staking`, `sui`, `tick_math`, `u128`, `u256`, `u64`, `vault`

---
protocol: generic
chain: sui, aptos, movement
category: arithmetic
vulnerability_type: precision_loss, overflow, underflow, division_by_zero, rounding_error
attack_type: economic_exploit, logical_error
affected_component: calculation_logic, token_conversion, fee_computation
primitives:
  - fixed_point_arithmetic
  - token_conversion
  - share_calculation
  - fee_computation
  - rounding
  - overflow_protection
  - division_safety
severity: high
impact: fund_loss, incorrect_pricing, protocol_insolvency
exploitability: 0.7
financial_impact: high
tags:
  - move
  - sui
  - aptos
  - arithmetic
  - precision
  - overflow
  - rounding
  - defi
language: move
version: all
---

## References
| # | Source | Protocol | Auditor | Severity |
|---|--------|----------|---------|----------|
| [R1] | reports/ottersec_move_audits/markdown/aftermath_marketmaking_v2_audit_final.md | Aftermath Finance | OtterSec | Critical/High |
| [R2] | reports/ottersec_move_audits/markdown/bluefin_spot_audit_final.md | Bluefin Spot | OtterSec | Critical/High |
| [R3] | reports/ottersec_move_audits/markdown/deepbook_v3_audit_draft.md | DeepBook V3 | OtterSec | High |
| [R4] | reports/ottersec_move_audits/markdown/kuna_labs_audit_final.md | Kuna Labs | OtterSec | High |
| [R5] | reports/ottersec_move_audits/markdown/thalaswap_v2_audit_final.md | ThalaSwap V2 | OtterSec | Critical |
| [R6] | reports/ottersec_move_audits/markdown/solend_steamm_audit_final.md | Solend Steamm | OtterSec | High |
| [R7] | reports/ottersec_move_audits/markdown/thala_lsd_audit_final.md | Thala LSD | OtterSec | High |
| [R8] | reports/ottersec_move_audits/markdown/wagmitt_kofi_audit_final.md | Kofi Finance | OtterSec | Critical/High |
| [R9] | reports/ottersec_move_audits/markdown/mysten_walrus_contracts.md | Mysten Walrus | OtterSec | High |
| [R10] | reports/ottersec_move_audits/markdown/ethsign_merkle_token_distributor_audit_final.md | EthSign | OtterSec | High |
| [R11] | reports/ottersec_move_audits/markdown/mysten_republic_audit_final_v2.md | Mysten Republic | OtterSec | Medium |
| [R12] | reports/ottersec_move_audits/markdown/echelon_audit_final.md | Echelon | OtterSec | Medium |
| [R13] | reports/ottersec_move_audits/markdown/aftermath_perps_oracle_audit_final.md | Aftermath Perps | OtterSec | Medium |
| [R14] | reports/ottersec_move_audits/markdown/aptos_securitize_audit_final.md | Aptos Securitize | OtterSec | High |
| [R15] | reports/ottersec_move_audits/markdown/aave_aptos_v3_audit_final.md | Aave Aptos V3 | OtterSec | Low |
| [R16] | reports/ottersec_move_audits/markdown/magna_audit_final.md | Magna | OtterSec | Informational |
| [R17] | reports/ottersec_move_audits/markdown/lombard_finance_audit_final.md | Lombard Finance | OtterSec | Critical |

## Move Arithmetic and Precision Vulnerabilities

**Comprehensive patterns for arithmetic, precision, overflow, underflow, rounding, and division-by-zero vulnerabilities in Move-based smart contracts across Sui, Aptos, and Movement chains.**

### Overview

Arithmetic and precision errors are the most common vulnerability class in Move-based DeFi protocols. Move's type system prevents raw integer overflow (it aborts on overflow), but this creates new attack vectors: attackers can trigger aborts to cause DoS, and developers must handle rounding/precision carefully to prevent fund loss. Found in 18/29 OtterSec audit reports (62%).

### Vulnerability Description

#### Root Cause

Move uses unsigned integers (u8, u64, u128, u256) that abort on overflow/underflow rather than wrapping. This differs from Solidity's historical wrapping behavior but creates analogous issues:
- Division-before-multiplication loses precision
- Rounding direction matters for protocol solvency
- Overly strict assertions on rounded values cause DoS
- Type casting between sizes can silently truncate
- Double-scaling or inconsistent scaling corrupts invariants

---

## Pattern 1: Double Scaling in Invariant Checks — move-arith-001

**Frequency**: 2/29 reports (ThalaSwap V2 [R5], Solend Steamm [R6])
**Severity consensus**: CRITICAL (lowest across auditors)
**Validation**: Moderate — 2 independent protocols

### Attack Scenario
1. Protocol applies scaling factor to balance amounts before computing invariant
2. Due to code error, scaling is applied twice to post-operation balances
3. Invariant check passes with insufficient repayment because double-scaled values are compared against single-scaled values
4. Attacker borrows via flashloan and repays less than borrowed amount

### Vulnerable Pattern Example

**Example 1: ThalaSwap V2 — Double Upscaling Enables Flashloan Fund Theft** [CRITICAL] [R5]
```move
// ❌ VULNERABLE: Double upscaling in flashloan repayment validation
public fun pay_flashloan(
    pool: &mut Pool,
    borrow_amounts: vector<u64>,
    repay_coins: vector<Coin>,
) {
    // First upscaling of borrow amounts
    let scaled_borrows = upscale_metastable_amounts(&borrow_amounts);
    
    // Balances already upscaled once here
    let balances = get_upscaled_balances(pool);
    
    // Calculate post-repayment balances
    let balances_after = vector::empty();
    let i = 0;
    while (i < vector::length(&balances)) {
        let bal = *vector::borrow(&balances, i) + coin::value(vector::borrow(&repay_coins, i));
        vector::push_back(&mut balances_after, bal);
        i = i + 1;
    };
    
    // ❌ BUG: Second upscaling applied to already-upscaled balances
    let scaled_after = upscale_metastable_amounts(&balances_after);
    
    // Invariant check uses double-scaled post values vs single-scaled pre values
    assert!(compute_invariant(&scaled_after) >= compute_invariant(&balances), E_INVARIANT);
}
```

**Example 2: Solend Steamm — Assertion Failure Due to Rounding in CToken Conversions** [HIGH] [R6]
```move
// ❌ VULNERABLE: Overly strict assertion doesn't account for rounding
public fun recall(bank: &mut Bank, lending: &mut LendingMarket, amount: u64) {
    let ctoken_amount = convert_to_ctokens(amount, lending);
    let recalled_amount = redeem_ctokens(lending, ctoken_amount);
    
    // ❌ BUG: This assertion fails due to rounding in cToken conversions
    // ctoken_amount * exchange_rate may not equal recalled_amount exactly
    assert!(
        ctoken_amount * bank.funds_deployed_rate() <= lending.ctokens * recalled_amount,
        E_INVALID_RECALL
    );
}
```

### Secure Implementation

**Fix 1: Single Scaling Application**
```move
// ✅ SECURE: Apply metastable upscaling exactly once
public fun pay_flashloan(pool: &mut Pool, borrow_amounts: vector<u64>, repay_coins: vector<Coin>) {
    let balances = get_raw_balances(pool);  // Raw, unscaled
    
    let balances_after = vector::empty();
    let i = 0;
    while (i < vector::length(&balances)) {
        let bal = *vector::borrow(&balances, i) + coin::value(vector::borrow(&repay_coins, i));
        vector::push_back(&mut balances_after, bal);
        i = i + 1;
    };
    
    // ✅ Scale both sides exactly once for comparison
    let scaled_before = upscale_metastable_amounts(&balances);
    let scaled_after = upscale_metastable_amounts(&balances_after);
    
    assert!(compute_invariant(&scaled_after) >= compute_invariant(&scaled_before), E_INVARIANT);
}
```

---

## Pattern 2: Division Before Multiplication Precision Loss — move-arith-002

**Frequency**: 3/29 reports (Kuna Labs [R4], Kofi Finance [R8], Solend Steamm [R6])
**Severity consensus**: HIGH
**Validation**: Strong — 3 independent protocols

### Attack Scenario
1. Protocol computes token amounts using division before multiplication
2. Integer truncation in division step loses significant precision
3. Result is smaller/larger than correct value
4. Attacker exploits incorrect calculations in liquidation/conversion logic

### Vulnerable Pattern Example

**Example 1: Kuna Labs — Precision Loss in LP Position Calculation** [HIGH] [R4]
```move
// ❌ VULNERABLE: Division before multiplication loses precision
fun calculate_token_x_amount(liquidity: u128, price: u128, tick_range: u128): u64 {
    // Division first truncates the intermediate result
    let intermediate = liquidity / price;       // ❌ Truncation here
    let result = intermediate * tick_range;      // Multiplied truncated value
    (result as u64)
}
```

**Example 2: Kofi Finance — Inconsistent Scaling in Conversion Rate** [MEDIUM] [R8]
```move
// ❌ VULNERABLE: Two branches apply different scaling factors
fun calculate_conversion_rate(staked: u64, total_supply: u64, locked: u64): u64 {
    if (locked > THRESHOLD) {
        // Branch A: scales by PRECISION first, then divides
        let rate = (staked * PRECISION) / total_supply;
        rate
    } else {
        // ❌ Branch B: different scaling factor applied
        let rate = staked / (total_supply / PRECISION);  // Different result
        rate
    }
}
```

### Secure Implementation

**Fix: Multiply Before Divide**
```move
// ✅ SECURE: Multiplication before division preserves precision
fun calculate_token_x_amount(liquidity: u128, price: u128, tick_range: u128): u64 {
    // Multiply first, then divide
    let result = (liquidity * tick_range) / price;
    (result as u64)
}
```

---

## Pattern 3: Division by Zero in Pool/Staking Operations — move-arith-003

**Frequency**: 4/29 reports (Solend Steamm [R6], Mysten Walrus [R9], Kofi Finance [R8], Aftermath MM [R1])
**Severity consensus**: HIGH
**Validation**: Strong — 4 independent protocols

### Attack Scenario
1. Pool or staking contract uses share-based accounting
2. Total shares or reserve amount reaches zero through withdrawal/manipulation
3. Subsequent operations divide by zero, causing transaction abort
4. Protocol becomes permanently unusable (DoS)

### Vulnerable Pattern Example

**Example 1: Solend Steamm — Division by Zero When Pool Reserve Empties** [HIGH] [R6]
```move
// ❌ VULNERABLE: No guard against zero reserve in division
public fun tokens_to_deposit(pool: &Pool, amount_a: u64): u64 {
    let reserve_a = pool.reserve_a;
    let reserve_b = pool.reserve_b;
    // ❌ Aborts if reserve_a is 0
    let amount_b = (amount_a * reserve_b) / reserve_a;
    amount_b
}
```

**Example 2: Mysten Walrus — Division by Zero in Committee Selection** [HIGH] [R9]
```move
// ❌ VULNERABLE: Weight can be zero if node's stake is too low
fun select_committee_and_calculate_votes(pool: &StakingPool, n_shards: u32): u64 {
    let weight = pool.total_stake / WEIGHT_DIVISOR;
    // ❌ Aborts when weight == 0
    let capacity_vote = (pool.node_capacity() * (n_shards as u64)) / weight;
    capacity_vote
}
```

**Example 3: Mysten Walrus — Zero Share Amount Manipulation** [HIGH] [R9]
```move
// ❌ VULNERABLE: share_amount can be manipulated to zero
public fun convert_to_wal_amount(rate: &ExchangeRate, shares: u64): u64 {
    // ❌ Aborts when rate.share_amount == 0
    (shares * rate.wal_amount) / rate.share_amount
}
```

### Secure Implementation

**Fix: Guard Against Zero Denominators**
```move
// ✅ SECURE: Check for zero before division
public fun tokens_to_deposit(pool: &Pool, amount_a: u64): u64 {
    assert!(pool.reserve_a > 0 && pool.reserve_b > 0, E_EMPTY_POOL);
    let amount_b = (amount_a * pool.reserve_b) / pool.reserve_a;
    amount_b
}

// ✅ SECURE: Enforce minimum share amount
public fun convert_to_wal_amount(rate: &ExchangeRate, shares: u64): u64 {
    assert!(rate.share_amount > 0, E_INVALID_RATE);
    (shares * rate.wal_amount) / rate.share_amount
}
```

---

## Pattern 4: Rounding Direction Exploits in Share Minting/Burning — move-arith-004

**Frequency**: 5/29 reports (Thala LSD [R7], Kofi Finance [R8], Solend Steamm [R6], Aftermath MM [R1], Kuna Labs [R4])
**Severity consensus**: HIGH
**Validation**: Strong — 5 independent protocols

### Attack Scenario
1. Share minting rounds down, so small deposits mint 0 shares
2. Share burning/redemption rounds up, so withdrawals extract more than proportional share
3. Attacker manipulates exchange rate so victim deposits receive 0 shares
4. Or attacker performs many small operations to extract rounding dust

### Vulnerable Pattern Example

**Example 1: Kofi Finance — Overpayment from Rounding to 1 Share** [MEDIUM] [R8]
```move
// ❌ VULNERABLE: Rounding to 1 causes overpayment
public fun unstake(pool: &mut Pool, amount: u64): Coin<APT> {
    let shares = (amount * pool.total_shares) / pool.total_staked;
    
    // ❌ If shares rounds to 0, setting to 1 causes overpayment
    let shares_to_burn = if (shares == 0 && amount > 0) { 1 } else { shares };
    
    // User gets more value per share than they deposited
    let apt_out = (shares_to_burn * pool.total_staked) / pool.total_shares;
    // ...
}
```

**Example 2: Solend Steamm — Overestimation from Rounding Up** [HIGH] [R6]
```move
// ❌ VULNERABLE: Rounding up causes users to supply more than needed
fun tokens_to_deposit(pool: &Pool, lp_amount: u64): (u64, u64) {
    // safe_mul_div_up rounds UP, causing dust amount beyond what's necessary
    let amount_a = safe_mul_div_up(lp_amount, pool.reserve_a, pool.total_lp);
    let amount_b = safe_mul_div_up(lp_amount, pool.reserve_b, pool.total_lp);
    (amount_a, amount_b)
}
```

### Secure Implementation

**Fix: Consistent Rounding Direction That Favors Protocol**
```move
// ✅ SECURE: Round DOWN on minting (fewer shares), round UP on burning (more tokens needed)
public fun mint_shares(pool: &Pool, deposit_amount: u64): u64 {
    if (pool.total_shares == 0) {
        return deposit_amount  // First depositor
    };
    // Round DOWN: user gets fewer shares (favors protocol)
    let shares = (deposit_amount * pool.total_shares) / pool.total_staked;
    assert!(shares > 0, E_ZERO_SHARES);  // Prevent zero-share deposits
    shares
}

public fun burn_shares(pool: &Pool, shares: u64): u64 {
    // Round DOWN: user gets fewer tokens (favors protocol)
    let tokens = (shares * pool.total_staked) / pool.total_shares;
    tokens
}
```

---

## Pattern 5: Overflow in Fee/Reward Calculations — move-arith-005

**Frequency**: 3/29 reports (EthSign [R10], Mysten Republic [R11], Aftermath Perps [R13])
**Severity consensus**: HIGH
**Validation**: Strong — 3 independent protocols

### Attack Scenario
1. Fee or reward calculation multiplies large token amounts by basis points
2. Intermediate multiplication exceeds u64 or u128 max
3. Transaction aborts, causing DoS for high-value operations
4. Protocol becomes unusable for large deposits/transfers

### Vulnerable Pattern Example

**Example 1: EthSign — Overflow in Fee Calculation** [HIGH] [R10]
```move
// ❌ VULNERABLE: Overflow when token_amount * fee_bips exceeds u64::MAX
public fun get_fee(token_transferred: u64, fee_bips: u64): u64 {
    // ❌ For large token amounts, this overflows and aborts
    let fee = (token_transferred * fee_bips) / BIPS_PRECISION;
    fee
}
```

**Example 2: Mysten Republic — Overflow in Dividend Calculation** [MEDIUM] [R11]
```move
// ❌ VULNERABLE: u64 multiplication can overflow
fun calculate_available_dividends(balance: u64, total_dividends: u64, total_supply: u64): u64 {
    // ❌ balance * total_dividends may exceed u64::MAX
    (balance * total_dividends) / total_supply
}
```

### Secure Implementation

**Fix: Use Wider Types for Intermediate Calculations**
```move
// ✅ SECURE: Cast to u128 for intermediate calculation
public fun get_fee(token_transferred: u64, fee_bips: u64): u64 {
    let fee = ((token_transferred as u128) * (fee_bips as u128)) / (BIPS_PRECISION as u128);
    (fee as u64)
}
```

---

## Pattern 6: Negative Value Mishandling in Signed Arithmetic — move-arith-006

**Frequency**: 3/29 reports (Aftermath MM [R1], Aftermath Perps [R13], Aptos Securitize [R14])
**Severity consensus**: HIGH
**Validation**: Strong — 3 independent protocols

### Attack Scenario
1. Protocol uses custom signed integer types (Move has no native signed ints)
2. Negative intermediate values are cast to unsigned, becoming very large positive numbers
3. Validation or conversion logic misinterprets the large value
4. Attacker receives unexpected funds or triggers incorrect state changes

### Vulnerable Pattern Example

**Example 1: Aftermath MM — Negative Slippage Converted to Positive Funds** [CRITICAL] [R1]
```move
// ❌ VULNERABLE: Negative balance converted to large positive
public fun end_withdraw_session(vault: &mut Vault, ctx: &TxContext) {
    let withdrawal_balance = vault.pending_withdrawal;
    let accumulated_slippage = vault.accumulated_slippage;  // Can be negative
    
    // ❌ If slippage exceeds withdrawal, result is "negative"
    // ifixed::to_balance() converts this to a large u64
    let final_amount = ifixed::to_balance(withdrawal_balance + accumulated_slippage);
    
    // Attacker receives unexpected profit
    transfer::public_transfer(coin::from_balance(final_amount), ctx.sender());
}
```

**Example 2: Aftermath Perps — Invalid Overflow Assertion in Fixed-Point** [MEDIUM] [R13]
```move
// ❌ VULNERABLE: Sign bit confused with overflow
public fun from_u256balance(a: u256, b: u256, is_negative_b: bool): IFixed {
    let result = a * b;
    // ❌ When b is negative, the sign bit is set, but code treats it as overflow
    assert!(result < GREATEST_BIT, E_OVERFLOW);  // False positive!
    // ...
}
```

**Example 3: Aptos Securitize — Underflow in Time Difference** [HIGH] [R14]
```move
// ❌ VULNERABLE: Subtraction can underflow if lock_time > current time
fun get_transferable_tokens(time: u64, lock_time: u64): u64 {
    // ❌ Aborts if lock_time > time
    let difference = time - lock_time;
    // ...
}
```

### Secure Implementation

**Fix: Explicit Negative Value Checks**
```move
// ✅ SECURE: Check sign before conversion
public fun end_withdraw_session(vault: &mut Vault, ctx: &TxContext) {
    let net_amount = vault.pending_withdrawal + vault.accumulated_slippage;
    
    // ✅ Only transfer if net amount is positive
    assert!(ifixed::is_positive(net_amount), E_NEGATIVE_BALANCE);
    let final_amount = ifixed::to_balance(net_amount);
    transfer::public_transfer(coin::from_balance(final_amount), ctx.sender());
}

// ✅ SECURE: Guard against underflow
fun get_transferable_tokens(time: u64, lock_time: u64): u64 {
    if (time <= lock_time) { return 0 };
    let difference = time - lock_time;
    // ...
}
```

---

## Pattern 7: Faulty Constant Definitions — move-arith-007

**Frequency**: 2/29 reports (Bluefin Spot [R2], Echelon [R12])
**Severity consensus**: HIGH (Bluefin was Critical)
**Validation**: Moderate — 2 independent protocols

### Vulnerable Pattern Example

**Example 1: Bluefin Spot — Incorrect MAX_U64 Constant (Missing Digit)** [CRITICAL] [R2]
```move
// ❌ VULNERABLE: Missing final digit in MAX_U64 constant
// Correct value: 18446744073709551615 (20 digits)
const MAX_U64: u64 = 1844674407370955161;  // ❌ Only 19 digits!

// This causes least_significant_bit() to ignore the highest bit
public fun least_significant_bit(x: u256): u8 {
    // Uses MAX_U64 for masking — incorrect mask truncates results
    let masked = (x & (MAX_U64 as u256));
    // ...
}
```

**Example 2: Echelon — Incorrect BPS Comment** [LOW] [R12]
```move
// ❌ VULNERABLE: Comment says 0.01% but value is 0.10%
/// 10 bps or 0.01% of the borrowed asset  ← WRONG: 10 bps = 0.10%
const DEFAULT_ORIGINATION_FEE_BPS: u64 = 10;
```

### Secure Implementation

**Fix: Verify Constants with Tests**
```move
// ✅ SECURE: Use compiler-checked maximum value
const MAX_U64: u64 = 18446744073709551615;  // 2^64 - 1

#[test]
fun test_max_u64() {
    assert!(MAX_U64 == (1u128 << 64) - 1, 0);
}
```

---

## Pattern 8: Fee Accounting Denomination Errors — move-arith-008

**Frequency**: 2/29 reports (DeepBook V3 [R3], EthSign [R10])
**Severity consensus**: HIGH
**Validation**: Moderate — 2 independent protocols

### Vulnerable Pattern Example

**Example 1: DeepBook V3 — Fee Paid in Wrong Denomination** [HIGH] [R3]
```move
// ❌ VULNERABLE: Fallthrough when deep_quantity is zero
public fun fee_quantity(order: &Order, deep_quantity: u64): (u64, u64, u64) {
    if (order.pay_with_deep && deep_quantity > 0) {
        // Pay fee in DEEP token
        let fee = calculate_deep_fee(order.quantity, deep_quantity);
        (fee, 0, 0)
    }
    // ❌ When deep_quantity == 0 but pay_with_deep is true,
    // falls through to base/quote fee calculation
    else {
        let fee = calculate_base_fee(order.quantity);
        (0, fee, 0)  // Fee incorrectly charged in base token
    }
}
```

**Example 2: EthSign — Fee Bypass at Max Fee Bips** [HIGH] [R10]
```move
// ❌ VULNERABLE: Returns 0 when fee_bips == MAX_FEE_BIPS
public fun collect_fee(amount: u64, fee_bips: u64): u64 {
    if (fee_bips >= MAX_FEE_BIPS) {
        return 0  // ❌ BUG: Should return full amount as fee, not zero
    };
    (amount * fee_bips) / MAX_FEE_BIPS
}
```

### Secure Implementation

**Fix: Explicit Denomination Handling**
```move
// ✅ SECURE: Handle all fee denomination cases explicitly
public fun fee_quantity(order: &Order, deep_quantity: u64): (u64, u64, u64) {
    if (order.pay_with_deep) {
        assert!(deep_quantity > 0, E_INSUFFICIENT_DEEP);
        let fee = calculate_deep_fee(order.quantity, deep_quantity);
        (fee, 0, 0)
    } else {
        let fee = calculate_base_fee(order.quantity);
        (0, fee, 0)
    }
}
```

---

## Pattern 9: Rounding Assertion Failure in Token Conversions — move-arith-009

**Frequency**: 3/29 reports (Solend Steamm [R6], Kofi Finance [R8], Magna)
**Severity consensus**: MEDIUM (lowest across auditors)
**Validation**: Strong — 3 independent auditors

### Attack Scenario
1. Protocol converts between token representations (cTokens ↔ underlying, shares ↔ tokens)
2. Strict assertion checks equality between pre- and post-conversion values
3. Due to integer division rounding, the converted-then-reconverted value is off by 1
4. Assertion fails, blocking legitimate user operations (deposits, recalls, withdrawals)

### Vulnerable Pattern Example

**Example 1: Solend Steamm — CToken Ratio Assertion Fails on Rounding** [MEDIUM] [R6]
```move
// ❌ VULNERABLE: Strict inequality doesn't account for rounding
fun recall<P, T, BToken>(bank: &mut Bank<P, T, BToken>, amount_to_recall: u64) {
    let ctoken_amount = convert_to_ctokens(amount_to_recall);
    let recalled_amount = redeem_ctokens(ctoken_amount);
    // BUG: ctoken_amount * rate may not equal recalled_amount due to rounding
    assert!(
        ctoken_amount * bank.funds_deployed() <= lending.ctokens * recalled_amount,
        EInvalidCTokenRatio,
    );
}
```

**Example 2: Kofi Finance — Conversion Rate Scaling Branches Produce Inconsistent Results** [MEDIUM] [R8]
```move
// ❌ VULNERABLE: Two branches with different scaling yield different results
fun convert(amount: u64, total_staked: u64, total_supply: u64): u64 {
    if (total_staked > OVERFLOW_THRESHOLD) {
        // Branch A: scale down first
        (amount * (total_supply / SCALE)) / (total_staked / SCALE)
    } else {
        // Branch B: full precision
        (amount * total_supply) / total_staked
    }
    // Results diverge near the threshold boundary
}
```

### Secure Implementation
```move
// ✅ SECURE: Use tolerance-based comparison or consistent scaling
fun recall_safe(bank: &mut Bank, amount_to_recall: u64) {
    let ctoken_amount = convert_to_ctokens(amount_to_recall);
    let recalled_amount = redeem_ctokens(ctoken_amount);
    // Allow 1 unit of rounding tolerance
    assert!(
        recalled_amount + 1 >= expected_amount,
        EInvalidCTokenRatio,
    );
}
```

---

## Pattern 10: Overestimation from Rounding Up in Deposit Calculations — move-arith-010

**Frequency**: 2/29 reports (Solend Steamm [R6], Kofi Finance [R8])
**Severity consensus**: MEDIUM (lowest across auditors)
**Validation**: Moderate — 2 independent protocols

### Attack Scenario
1. Protocol uses `mul_div_up` (ceiling division) for deposit amount calculations
2. Rounding up causes users to supply more tokens than necessary to maintain pool ratio
3. Over time, dust accumulates as excess tokens in the pool, disrupting balance ratios
4. In extreme cases, pool becomes insolvent from accumulated rounding errors favoring users

### Vulnerable Pattern Example

**Example: Solend Steamm — Rounding Up Overestimates Required Deposit** [MEDIUM] [R6]
```move
// ❌ VULNERABLE: safe_mul_div_up rounds up, causing overestimation
fun tokens_to_deposit(reserve_a: u64, reserve_b: u64, max_a: u64, max_b: u64): (u64, u64) {
    if (reserve_a == 0 && reserve_b == 0) {
        (max_a, max_b)
    } else {
        // BUG: Rounding up means b_star may be slightly more than needed
        let b_star = safe_mul_div_up(max_a, reserve_b, reserve_a);
        if (b_star <= max_b) { (max_a, b_star) }
        else {
            let a_star = safe_mul_div_up(max_b, reserve_a, reserve_b);
            (a_star, max_b)
        }
    }
}
```

### Secure Implementation
```move
// ✅ SECURE: Round down for amounts taken from users
fun tokens_to_deposit_safe(reserve_a: u64, reserve_b: u64, max_a: u64, max_b: u64): (u64, u64) {
    let b_star = math64::mul_div(max_a, reserve_b, reserve_a); // rounds down
    if (b_star <= max_b) { (max_a, b_star) }
    else {
        let a_star = math64::mul_div(max_b, reserve_a, reserve_b);
        (a_star, max_b)
    }
}
```

---

## Pattern 11: Fee Calculation Overflow in Basis Point Multiplication — move-arith-011

**Frequency**: 2/29 reports (EthSign [R10], Mysten Republic [R11])
**Severity consensus**: MEDIUM (lowest across auditors)
**Validation**: Moderate — 2 independent protocols

### Attack Scenario
1. Fee calculation uses `(token_amount * fee_bips) / BIPS_PRECISION` in u64
2. For large token amounts, the intermediate multiplication overflows u64
3. Transaction aborts, blocking token distribution or dividend claims
4. If protocol catches overflow, fee may be computed incorrectly

### Vulnerable Pattern Example

**Example 1: EthSign — Fee Calculation Overflows on Large Token Amounts** [MEDIUM] [R10]
```move
// ❌ VULNERABLE: u64 multiplication overflows for large amounts
public fun get_fee(distributor_address: address, token_transferred: u64): u64 {
    let fee_bips = get_fee_bips(distributor_address);
    // BUG: token_transferred * fee_bips can exceed u64::MAX
    (token_transferred * fee_bips) / BIPS_PRECISION
}
```

**Example 2: Mysten Republic — Dividend Proportional Calculation Overflows** [MEDIUM] [R11]
```move
// ❌ VULNERABLE: Multiplying large balances causes u64 overflow
public fun calculate_available_dividends(dividends: &Dividends, snapshot: &Snapshot, addr: address): u64 {
    // BUG: total_funds * balance can exceed u64::MAX
    let addr_total = (dividends.total_funds * snapshot.address_balance(addr)) / unlocked_supply;
    addr_total - already_claimed
}
```

### Secure Implementation
```move
// ✅ SECURE: Use u128 intermediate calculation
public fun get_fee_safe(token_transferred: u64, fee_bips: u64): u64 {
    let result = ((token_transferred as u128) * (fee_bips as u128)) / (BIPS_PRECISION as u128);
    (result as u64)
}
```

---

## Pattern 12: Overpayment from Minimum Share Rounding — move-arith-012

**Frequency**: 2/29 reports (Kofi Finance [R8], Aftermath MM [R1])
**Severity consensus**: MEDIUM (lowest across auditors)
**Validation**: Moderate — 2 independent protocols

### Attack Scenario
1. When unstaking, if computed share amount rounds to 0, protocol sets shares = 1
2. At high exchange rates, 1 share is worth more than the original unstake amount
3. User receives more value than they burned, draining protocol funds
4. Repeated exploitation creates insolvency

### Vulnerable Pattern Example

**Example: Kofi Finance — Rounding to 1 Share Causes Overpayment** [MEDIUM] [R8]
```move
// ❌ VULNERABLE: Setting shares to 1 overpays at high exchange rates
fun compute_unstake_shares(amount: u64, exchange_rate: u64): u64 {
    let shares = math64::mul_div(amount, SCALE, exchange_rate);
    if (shares == 0 && amount > 0) {
        shares = 1; // BUG: 1 share may be worth more than `amount`
    };
    shares
}
```

### Secure Implementation
```move
// ✅ SECURE: Abort on zero shares instead of rounding up
fun compute_unstake_shares_safe(amount: u64, exchange_rate: u64): u64 {
    let shares = math64::mul_div(amount, SCALE, exchange_rate);
    assert!(shares > 0, E_AMOUNT_TOO_SMALL);
    shares
}
```

---

## Pattern 13: Subtraction Underflow in Time/Balance Difference Calculations — move-arith-013

**Frequency**: 4/29 reports (Aptos Securitize [R14], Mysten Walrus [R9], Magna, Aftermath MM [R1])
**Severity consensus**: LOW (lowest across auditors)
**Validation**: Strong — 4 independent auditors

### Attack Scenario
1. Code computes `difference = time_a - time_b` or `balance_a - balance_b`
2. Move aborts on unsigned underflow, but the subtraction is computed before the guard check
3. Transaction aborts, blocking user operations despite having valid data
4. Can be weaponized to DoS specific functions

### Vulnerable Pattern Example

**Example 1: Aptos Securitize — Underflow in Time Difference Calculation** [LOW] [R14]
```move
// ❌ VULNERABLE: Subtraction executes before guard check
fun get_compliance_transferable_tokens(time: u256, lock_time: u256, issuance_time: u256) {
    let difference = time - lock_time; // BUG: Aborts if lock_time > time
    if (lock_time > time || issuance_time > (difference as u256)) {
        return 0
    };
}
```

**Example 2: Mysten Walrus — Underflow in Capacity Accounting** [LOW] [R9]
```move
// ❌ VULNERABLE: deny_list_size may exceed old_epoch_used_capacity
let stored = (weight as u128) * ((old_epoch_used_capacity - deny_list_size) as u128);
```

### Secure Implementation
```move
// ✅ SECURE: Check before subtracting
fun get_compliance_transferable_tokens_safe(time: u256, lock_time: u256) {
    if (lock_time > time) { return 0 };
    let difference = time - lock_time; // Safe: lock_time <= time
}
```

---

## Pattern 14: Mutable Local Copy Instead of Dereference in State Update — move-arith-014

**Frequency**: 1/29 reports (Lombard Finance)
**Severity consensus**: CRITICAL
**Validation**: Weak — single auditor, but Critical severity

### Attack Scenario
1. Function destructures a struct with `mut field`, creating a mutable local copy
2. Update assigns to `field = new_value` instead of `*field = new_value`
3. The actual stored value is never updated — the change is lost when the function returns
4. Rate limits, counters, or caps remain at their old value permanently

### Vulnerable Pattern Example

**Example: Lombard Finance — Mint Limit Reset Writes to Local Copy** [CRITICAL]
```move
// ❌ VULNERABLE: `mut left` is a local copy, not a mutable reference
public fun mint_and_transfer<T>(treasury: &mut Treasury<T>, amount: u64, ctx: &TxContext) {
    let MinterCap { limit, epoch, mut left } = get_cap_mut(treasury, ctx.sender());
    if (ctx.epoch() > *epoch) {
        left = limit;        // BUG: assigns to local copy, stored value unchanged
        *epoch = ctx.epoch();
    };
    assert!(amount <= *left, EMintLimitExceeded);
    *left = *left - amount;
}
```

### Secure Implementation
```move
// ✅ SECURE: Dereference to update stored value
public fun mint_and_transfer_safe<T>(treasury: &mut Treasury<T>, amount: u64, ctx: &TxContext) {
    let MinterCap { limit, epoch, left } = get_cap_mut(treasury, ctx.sender());
    if (ctx.epoch() > *epoch) {
        *left = *limit;  // Correct: dereference updates the stored field
        *epoch = ctx.epoch();
    };
    assert!(amount <= *left, EMintLimitExceeded);
    *left = *left - amount;
}
```

---

## Pattern 15: Variable Shadowing Corrupts Recorded Values — move-arith-015

**Frequency**: 3/29 reports (Aptos Securitize [R14], Aave Aptos V3, Canopy)
**Severity consensus**: MEDIUM (lowest across auditors)
**Validation**: Strong — 3 independent auditors

### Attack Scenario
1. A function declares `let value = 0;` which shadows an input parameter `_value`
2. All subsequent uses refer to the shadowed zero instead of the parameter
3. Recorded issuance amounts, event values, or state updates are permanently zeroed
4. Compliance tracking, audit trails, or fee collection breaks silently

### Vulnerable Pattern Example

**Example 1: Aptos Securitize — Parameter Shadowed by Zero Declaration** [MEDIUM] [R14]
```move
// ❌ VULNERABLE: `let value = 0` shadows the `_value` parameter
fun create_issuance_information(investor: String, _value: u256, issuance_time: u256) {
    let value = 0; // BUG: Shadows _value, all records show 0
    let issuance = Issuance {
        investor,
        value,         // Always 0!
        issuance_time,
    };
    store_issuance(issuance);
}
```

**Example 2: Aave Aptos V3 — Shadowed Variable in Event Emission** [LOW]
```move
// ❌ VULNERABLE: Inner let shadows outer pending_ltv_set
let pending_ltv_set = 0;
if (freeze) {
    let pending_ltv_set = reserve_config::get_ltv(&config); // Shadows outer!
    smart_table::upsert(&mut data.pending_ltv, asset, pending_ltv_set);
};
event::emit(PendingLtvChanged { asset, pending_ltv_set }); // Always emits 0
```

### Secure Implementation
```move
// ✅ SECURE: Assign to existing variable instead of re-declaring
let mut pending_ltv_set = 0;
if (freeze) {
    pending_ltv_set = reserve_config::get_ltv(&config); // Mutates, no shadow
    smart_table::upsert(&mut data.pending_ltv, asset, pending_ltv_set);
};
event::emit(PendingLtvChanged { asset, pending_ltv_set }); // Correct value
```

---

## Pattern 16: Negative-to-Unsigned Conversion Produces Incorrect Magnitude — move-arith-016

**Frequency**: 3/29 reports (Aftermath MM [R1], Aftermath Perps [R13], Mysten Walrus [R9])
**Severity consensus**: HIGH (lowest across auditors)
**Validation**: Strong — 3 independent auditors

### Attack Scenario
1. Protocol uses a signed fixed-point library (`ifixed`) with values stored as u256 with a sign bit
2. A negative value is passed to `ifixed::to_balance()` which tries to convert to unsigned u64
3. The conversion produces an extremely large positive number (2^256 - |value|)
4. This inflated value bypasses size limits, allowing oversized orders/withdrawals

### Vulnerable Pattern Example

**Example 1: Aftermath Perps — Negative Position Size Produces Huge u64** [HIGH] [R13]
```move
// ❌ VULNERABLE: Negative `base` produces inflated u64 from to_balance
public(package) fun place_stop_order_sltp<T>(size: u64, base: u256) {
    // When base is negative, to_balance returns a massive number
    let size = min(size, ifixed::to_balance(base, constants::b9_scaling()));
    // size is NOT capped — the "min" has no effect
}
```

**Example 2: Aftermath MM — Negative Withdrawal Amount Becomes Large Positive** [HIGH] [R1]
```move
// ❌ VULNERABLE: Accumulated slippage can make balance_to_withdraw negative
let balance_to_withdraw = ifixed::add(initial_balance, accumulated_slippage);
// If accumulated_slippage is large negative, balance_to_withdraw is negative
let amount = ifixed::to_balance(balance_to_withdraw, scaling); // Huge positive!
```

### Secure Implementation
```move
// ✅ SECURE: Check sign before conversion
public fun safe_to_balance(value: u256, scaling: u256): u64 {
    assert!(!ifixed::is_negative(value), E_NEGATIVE_VALUE);
    ifixed::to_balance(value, scaling)
}
```

---

## Pattern 17: Division by Zero in Pool/Staking Operations — move-arith-017

**Frequency**: 4/29 reports (Solend Steamm [R6], Mysten Walrus [R9], Aftermath MM [R1], Kofi Finance [R8])
**Severity consensus**: MEDIUM (lowest across auditors)
**Validation**: Strong — 4 independent auditors

### Attack Scenario
1. Protocol performs division by total supply, weight, or reserve that can be zero
2. Zero occurs when pool is empty, node has no stake, or all tokens are drained
3. Move aborts on division by zero, blocking all subsequent operations
4. Attacker drains pool to zero, then permanent DoS on any function using the division

### Vulnerable Pattern Example

**Example 1: Mysten Walrus — Zero Weight Division in Committee Selection** [MEDIUM] [R9]
```move
// ❌ VULNERABLE: weight can be 0 for low-stake nodes
fun calculate_capacity_vote(pool: &StakingPool, n_shards: u64, weight: u64): u64 {
    (pool.node_capacity() * (n_shards as u64)) / weight // Aborts if weight == 0
}
```

**Example 2: Solend Steamm — Zero Reserve Division in Deposit** [MEDIUM] [R6]
```move
// ❌ VULNERABLE: reserve_a can be 0 if pool is fully drained
fun tokens_to_deposit(reserve_a: u64, reserve_b: u64, max_a: u64, max_b: u64): (u64, u64) {
    if (reserve_a == 0 && reserve_b == 0) { (max_a, max_b) }
    else {
        let b_star = safe_mul_div_up(max_a, reserve_b, reserve_a); // BUG: reserve_a could be 0
    }
}
```

### Secure Implementation
```move
// ✅ SECURE: Guard against zero denominators
fun calculate_capacity_vote_safe(pool: &StakingPool, n_shards: u64, weight: u64): u64 {
    if (weight == 0) { return 0 };
    (pool.node_capacity() * (n_shards as u64)) / weight
}
```

---

## Pattern 18: Incorrect `round_up` Division Overflow — move-arith-018

**Frequency**: 2/29 reports (Kuna Labs, Magna)
**Severity consensus**: LOW (lowest across auditors)
**Validation**: Moderate — 2 independent protocols

### Attack Scenario
1. Protocol uses `divide_and_round_up(a, b) = (a + b - 1) / b`
2. When `a` is close to `u128::MAX` or `u256::MAX`, `a + b - 1` overflows
3. Transaction aborts, blocking operations that use ceiling division
4. Attacker triggers overflow by manipulating values near max range

### Vulnerable Pattern Example

**Example: Kuna Labs — Round-up Division Overflows** [LOW]
```move
// ❌ VULNERABLE: a + b - 1 can overflow
public fun divide_and_round_up_u128(a: u128, b: u128): u128 {
    (a + b - 1) / b // BUG: overflows when a + b > u128::MAX
}
```

### Secure Implementation
```move
// ✅ SECURE: Avoid intermediate overflow
public fun divide_and_round_up_safe(a: u128, b: u128): u128 {
    if (a == 0) { return 0 };
    (a - 1) / b + 1
}
```

---

## Pattern 19: Overflow in Signed Fixed-Point Multiplication Check — move-arith-019

**Frequency**: 2/29 reports (Aftermath MM [R1], Aftermath Perps [R13])
**Severity consensus**: MEDIUM (lowest across auditors)
**Validation**: Moderate — same auditor, 2 different protocols

### Attack Scenario
1. Signed fixed-point library uses `GREATEST_BIT` to detect sign/overflow
2. When one operand is negative, the raw product has the sign bit set
3. Overflow check treats sign bit as overflow, aborting valid negative multiplications
4. Legitimate operations with negative PnL, slippage, etc. are blocked

### Vulnerable Pattern Example

**Example: Aftermath — Sign Bit Confused with Overflow** [MEDIUM] [R13]
```move
// ❌ VULNERABLE: Treats sign bit as overflow
public fun from_u256balance(balance: u256, scaling_factor: u256): u256 {
    let z = balance * scaling_factor;
    if (balance ^ scaling_factor < GREATEST_BIT) {
        assert!(z < GREATEST_BIT, OVERFLOW_ERROR); // False positive on negative results
        return z
    };
    assert!(z <= GREATEST_BIT, OVERFLOW_ERROR); // Blocks valid negative products
    (GREATEST_BIT - z) ^ GREATEST_BIT
}
```

### Secure Implementation
```move
// ✅ SECURE: Separate overflow check from sign handling
public fun from_u256balance_safe(balance: u256, scaling_factor: u256): u256 {
    let abs_result = abs(balance) * abs(scaling_factor) / SCALE;
    assert!(abs_result < GREATEST_BIT, OVERFLOW_ERROR);
    if (is_negative(balance) != is_negative(scaling_factor)) {
        negate(abs_result)
    } else {
        abs_result
    }
}
```

---

## Pattern 20: Zero Mint After Fixed-Point Precision Loss — move-arith-020

**Frequency**: 2/29 reports (Aftermath MM [R1], Kofi Finance [R8])
**Severity consensus**: LOW (lowest across auditors)
**Validation**: Moderate — 2 independent protocols

### Attack Scenario
1. Protocol checks `lp_to_mint != 0` at fixed-point precision
2. Converts to balance via `ifixed::to_balance(lp_to_mint, scaling)`
3. Precision loss in conversion makes the balance 0 despite non-zero fixed-point value
4. Zero LP tokens are minted — user's deposit is consumed with nothing received

### Vulnerable Pattern Example

**Example: Aftermath MM — Zero-Check Before Precision-Lossy Conversion** [LOW] [R1]
```move
// ❌ VULNERABLE: Non-zero fixed-point can become zero after conversion
fun end_deposit_session(vault: &mut Vault, lp_to_mint: u256) {
    assert!(lp_to_mint != 0, E_ZERO_MINT); // Passes check
    let lp_balance = mint_lp_balance(
        &mut vault,
        ifixed::to_balance(lp_to_mint, constants::b9_scaling()), // Can be 0!
    );
    // User deposited funds but lp_balance is 0
}
```

### Secure Implementation
```move
// ✅ SECURE: Check after conversion to actual balance
fun end_deposit_session_safe(vault: &mut Vault, lp_to_mint: u256) {
    let lp_amount = ifixed::to_balance(lp_to_mint, constants::b9_scaling());
    assert!(lp_amount > 0, E_ZERO_MINT); // Check the actual minted amount
    let lp_balance = mint_lp_balance(&mut vault, lp_amount);
}
```

---

## Pattern 21: Faulty Constant Definition Corrupts Bit Manipulation — move-arith-021

**Frequency**: 1/29 reports (Bluefin Spot [R2])
**Severity consensus**: HIGH
**Validation**: Weak — single auditor, but High severity

### Attack Scenario
1. A constant for `MAX_U64` or similar bit mask is defined with wrong number of digits
2. Bit manipulation operations (LSB, MSB, tick lookup) use incorrect mask
3. The highest bit is ignored, causing tick positions to be misidentified
4. Swaps execute at wrong prices or fail to find valid tick positions

### Vulnerable Pattern Example

**Example: Bluefin Spot — MAX_U64 Constant Missing a Digit** [HIGH] [R2]
```move
// ❌ VULNERABLE: 15 hex chars instead of 16
const MAX_U64: u64 = 0xFFFFFFFFFFFFFFF; // Missing one F — should be 0xFFFFFFFFFFFFFFFF

public fun least_significant_bit(mask: u256): u8 {
    let bit = 255;
    // Uses MAX_U64 as bitmask — misses the top bit of the u64 range
    if (mask & (MAX_U64 as u256) > 0) {
        bit = bit - 64;
    } else {
        mask = mask >> 64;
    };
    bit
}
```

### Secure Implementation
```move
// ✅ SECURE: Verified constant with proper digit count
const MAX_U64: u64 = 0xFFFFFFFFFFFFFFFF; // Exactly 16 hex digits = 2^64 - 1

// Additionally validate at compile time or in tests:
#[test]
fun test_max_u64() {
    assert!(MAX_U64 == 18446744073709551615, 0);
}
```

---

## Pattern 22: Excess Recall/Withdrawal Rounded Beyond Available Reserves — move-arith-022

**Frequency**: 2/29 reports (Solend Steamm [R6], Kofi Finance [R8])
**Severity consensus**: MEDIUM (lowest across auditors)
**Validation**: Moderate — 2 independent protocols

### Attack Scenario
1. Protocol rounds recall/withdrawal amounts up to a minimum block size
2. After rounding, the requested amount exceeds available reserves
3. Transaction either aborts (DoS) or overdraws the pool (insolvency)
4. Repeated triggering at block-size boundaries drains excess tokens

### Vulnerable Pattern Example

**Example: Solend Steamm — Recall Amount Exceeds Reserves After Rounding** [MEDIUM] [R6]
```move
// ❌ VULNERABLE: Rounding up can exceed available funds
fun recall(bank: &mut Bank, amount: u64) {
    // Round up to minimum block size
    let recall_amount = ((amount + bank.min_block_size - 1) / bank.min_block_size) * bank.min_block_size;
    // BUG: recall_amount may now exceed bank.reserves
    bank.reserves.split(recall_amount); // Aborts or overdraws
}
```

### Secure Implementation
```move
// ✅ SECURE: Cap rounded amount to available reserves
fun recall_safe(bank: &mut Bank, amount: u64) {
    let recall_amount = ((amount + bank.min_block_size - 1) / bank.min_block_size) * bank.min_block_size;
    let recall_amount = math64::min(recall_amount, balance::value(&bank.reserves));
    bank.reserves.split(recall_amount);
}
```

---

### Impact Analysis

#### Technical Impact
- Direct fund loss through incorrect calculations (8/29 reports)
- Protocol insolvency through rounding exploits (5/29 reports)
- Denial of service through overflow/division-by-zero aborts (4/29 reports)
- Inflation attacks via zero-share minting (3/29 reports)

#### Business Impact
- Loss of user deposits and protocol reserves
- Broken exchange rate pegs in liquid staking
- Permanent DoS if pool state reaches zero
- Incorrect fee collection reducing protocol revenue

#### Affected Scenarios
- AMMs with metastable pool scaling (ThalaSwap V2)
- Liquid staking share calculations (Thala LSD, Kofi Finance)
- CLOB fee denomination selection (DeepBook V3)
- Cross-chain bridge minting limits (Lombard)
- Storage/staking committee calculations (Mysten Walrus)

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: `upscale` or `scale` called more than once on same variable
- Pattern 2: Division before multiplication: `(a / b) * c` instead of `(a * c) / b`
- Pattern 3: Division without zero-check on denominator: `x / pool.total_supply`
- Pattern 4: Rounding to 1 on zero result: `if (shares == 0) { shares = 1 }`
- Pattern 5: `(amount * bips) / PRECISION` without u128 cast
- Pattern 6: Missing negative/underflow guard: `time - lock_time`
- Pattern 7: Hardcoded numeric constants with many digits
- Pattern 8: Fee fallthrough logic: `if (pay_deep && deep > 0)` else...
- Pattern 9: Strict equality assertions on rounded conversion values
- Pattern 10: `mul_div_up` or `safe_mul_div_up` in deposit token calculation
- Pattern 11: `(amount * bips)` without u128 intermediate cast
- Pattern 12: `if (shares == 0) { shares = 1 }` in unstake path
- Pattern 13: `a - b` subtraction before `if (b > a)` guard
- Pattern 14: `mut field` destructure with `field = value` instead of `*field = value`
- Pattern 15: `let value = 0` shadowing an input parameter `_value`
- Pattern 16: `ifixed::to_balance(negative_value)` without sign check
- Pattern 17: Division by `weight`, `supply`, or `reserve` that can be zero
- Pattern 18: `(a + b - 1) / b` round-up where `a + b` overflows
- Pattern 19: Sign bit == GREATEST_BIT treated as overflow in signed math
- Pattern 20: Zero-check on fixed-point value BEFORE lossy conversion to u64
- Pattern 21: Hex constant with wrong digit count: `0xFFFFFFFFFFFFFFF`
- Pattern 22: Rounded amount exceeds available reserves after `round_up_to_block`
```

#### Audit Checklist
- [ ] Verify scaling functions are applied exactly once per calculation path
- [ ] Check all division operations have zero-denominator guards
- [ ] Confirm multiplication happens before division in multi-step calculations
- [ ] Verify rounding direction consistently favors the protocol
- [ ] Check fee calculations handle edge cases (max bips, zero quantities)
- [ ] Validate numeric constants against known max values (u64::MAX, etc.)
- [ ] Ensure signed arithmetic properly handles negative intermediate values
- [ ] Verify type casts between u64/u128/u256 don't lose precision
- [ ] Check assertions allow rounding tolerance in conversion comparisons
- [ ] Verify `mut` destructured fields use dereference (`*field = val`) for state updates
- [ ] Look for variable shadowing (re-declaration with `let` hiding parameters)
- [ ] Check `ifixed::to_balance` callers handle negative input before conversion
- [ ] Validate `round_up` helper doesn't overflow: use `(a - 1) / b + 1`
- [ ] Verify zero-mint checks happen AFTER conversion, not before

### Keywords for Search

> `arithmetic`, `precision`, `overflow`, `underflow`, `division by zero`, `rounding`, `truncation`, `scaling`, `double scaling`, `fee calculation`, `share calculation`, `token conversion`, `exchange rate`, `basis points`, `bps`, `mul_div`, `safe_mul_div`, `move arithmetic`, `sui arithmetic`, `aptos arithmetic`, `u64 overflow`, `u128`, `fixed point`, `signed integer`, `negative value`, `constant definition`, `MAX_U64`, `type cast`, `variable shadowing`, `mut local copy`, `dereference`, `ifixed`, `to_balance`, `round_up`, `ceil division`, `precision loss`, `zero mint`, `ctoken ratio`, `conversion rate`, `exchange rate scaling`

### Related Vulnerabilities

- [SUI_MOVE_ARITHMETIC_PRECISION_VULNERABILITIES.md](SUI_MOVE_ARITHMETIC_PRECISION_VULNERABILITIES.md) — Sui-specific arithmetic patterns from Solodit
- [MOVE_TOKEN_SUPPLY_INFLATION_VULNERABILITIES.md](MOVE_TOKEN_SUPPLY_INFLATION_VULNERABILITIES.md) — Inflation attacks exploiting rounding
- [MOVE_DEFI_PROTOCOL_LOGIC_VULNERABILITIES.md](MOVE_DEFI_PROTOCOL_LOGIC_VULNERABILITIES.md) — Logic errors in DeFi calculations

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

### Keywords for Search

> `arithmetic`, `precision`, `overflow`, `underflow`, `division by zero`, `rounding`, `truncation`, `scaling`, `double scaling`, `fee calculation`, `share calculation`, `token conversion`, `exchange rate`, `basis points`, `bps`, `mul_div`, `safe_mul_div`, `move arithmetic`, `sui arithmetic`, `aptos arithmetic`, `u64 overflow`, `u128`, `fixed point`, `signed integer`, `negative value`, `constant definition`, `MAX_U64`, `type cast`

### Related Vulnerabilities

- [SUI_MOVE_ARITHMETIC_PRECISION_VULNERABILITIES.md](SUI_MOVE_ARITHMETIC_PRECISION_VULNERABILITIES.md) — Sui-specific arithmetic patterns from Solodit
- [MOVE_TOKEN_SUPPLY_INFLATION_VULNERABILITIES.md](MOVE_TOKEN_SUPPLY_INFLATION_VULNERABILITIES.md) — Inflation attacks exploiting rounding
- [MOVE_DEFI_PROTOCOL_LOGIC_VULNERABILITIES.md](MOVE_DEFI_PROTOCOL_LOGIC_VULNERABILITIES.md) — Logic errors in DeFi calculations

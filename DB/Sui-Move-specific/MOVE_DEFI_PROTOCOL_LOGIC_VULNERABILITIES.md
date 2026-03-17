---
protocol: generic
chain: sui, aptos, movement
category: defi_logic
vulnerability_type: reward_miscalculation, solvency_failure, withdrawal_logic, claim_exploit, liquidation_flaw, fee_manipulation
attack_type: fund_extraction, protocol_insolvency, accounting_manipulation
affected_component: rewards, vaults, lending, staking, fee_logic, liquidation
primitives:
  - reward_distribution
  - solvency_check
  - withdrawal_logic
  - claim_mechanism
  - liquidation_flow
  - fee_calculation
  - lp_token
  - vesting
severity: critical
impact: fund_loss, protocol_insolvency, incorrect_accounting
exploitability: 0.7
financial_impact: critical
tags:
  - move
  - sui
  - aptos
  - defi
  - rewards
  - solvency
  - withdrawal
  - claim
  - liquidation
  - fee
  - lending
  - staking
  - vesting
language: move
version: all

# Pattern Identity (Required)
root_cause_family: arithmetic_error
pattern_key: arithmetic_error | rewards, vaults, lending, staking, fee_logic, liquidation | reward_miscalculation, solvency_failure, withdrawal_logic, claim_exploit, liquidation_flaw, fee_manipulation

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - add_reward_program
  - boundary
  - burn
  - calculate_fee
  - cancel_schedule_interval
  - cancel_schedule_interval_safe
  - cancel_vesting
  - claim_mechanism
  - claim_reward
  - claim_tokens
  - create_obligation
  - create_pool
  - create_pool_safe
  - deposit
  - distribute_rewards
  - end_withdraw_session
  - execute
  - fee_calculation
  - flashloan_repay
  - force_withdraw
---

## References
| # | Source | Protocol | Auditor | Severity |
|---|--------|----------|---------|----------|
| [R1] | reports/ottersec_move_audits/markdown/echelon_audit_final.md | Echelon | OtterSec | HIGH |
| [R2] | reports/ottersec_move_audits/markdown/thalaswap_v2_audit_final.md | ThalaSwap V2 | OtterSec | CRITICAL |
| [R3] | reports/ottersec_move_audits/markdown/solend_steamm_audit_final.md | Solend Steamm | OtterSec | HIGH |
| [R4] | reports/ottersec_move_audits/markdown/aftermath_marketmaking_v2_audit_final.md | Aftermath MM | OtterSec | CRITICAL |
| [R5] | reports/ottersec_move_audits/markdown/bluefin_spot_audit_final.md | Bluefin Spot | OtterSec | HIGH |
| [R6] | reports/ottersec_move_audits/markdown/deepbook_v3_audit_draft.md | DeepBook V3 | OtterSec | HIGH |
| [R7] | reports/ottersec_move_audits/markdown/kuna_labs_audit_final.md | Kuna Labs | OtterSec | HIGH |
| [R8] | reports/ottersec_move_audits/markdown/mysten_walrus_audit_final.md | Mysten Walrus | OtterSec | HIGH |
| [R9] | reports/ottersec_move_audits/markdown/kofi_finance_audit_final.md | Kofi Finance | OtterSec | CRITICAL |
| [R10] | reports/ottersec_move_audits/markdown/aptos_securitize_audit_final.md | Aptos Securitize | OtterSec | HIGH |
| [R11] | reports/ottersec_move_audits/markdown/canopy_audit_final.md | Canopy | OtterSec | CRITICAL |
| [R12] | reports/ottersec_move_audits/markdown/mysten_republic_audit_final_v2.md | Mysten Republic | OtterSec | CRITICAL |
| [R13] | reports/ottersec_move_audits/markdown/magna_audit_final.md | Magna | OtterSec | HIGH |
| [R14] | reports/ottersec_move_audits/markdown/mayan_sui_audit_final.md | Mayan Sui | OtterSec | HIGH |
| [R15] | reports/ottersec_move_audits/markdown/emojicoin_audit_final.md | Emojicoin | OtterSec | HIGH |

## Move DeFi Protocol Logic Vulnerabilities

**Comprehensive patterns for reward miscalculation, solvency failures, withdrawal logic bugs, claim exploits, liquidation flaws, and fee manipulation in Move-based DeFi protocols across Sui, Aptos, and Movement chains.**

### Overview

DeFi protocol logic vulnerabilities are the most common class found in OtterSec Move audits, appearing in 15/29 reports (52%). These bugs arise from incorrect reward accounting, missing solvency constraints, conversion rounding issues, and flawed claim/withdrawal flows. Because Move's resource model enforces linear asset semantics, logic bugs manifest as fund lockups or incorrect minting rather than reentrancy-style theft.



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of arithmetic_error"
- Pattern key: `arithmetic_error | rewards, vaults, lending, staking, fee_logic, liquidation | reward_miscalculation, solvency_failure, withdrawal_logic, claim_exploit, liquidation_flaw, fee_manipulation`
- Interaction scope: `single_contract`
- Primary affected component(s): `rewards, vaults, lending, staking, fee_logic, liquidation`
- High-signal code keywords: `add_reward_program`, `boundary`, `burn`, `calculate_fee`, `cancel_schedule_interval`, `cancel_schedule_interval_safe`, `cancel_vesting`, `claim_mechanism`
- Typical sink / impact: `fund_loss, protocol_insolvency, incorrect_accounting`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `N/A`
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

#### Root Cause Categories

1. **Reward timing issues** — Incorrect initialization of reward timestamps or accumulation during inactive periods
2. **Missing solvency invariants** — No check that collateral exceeds borrowed value before withdrawals
3. **Conversion/rounding errors** — Rounding in token-to-share conversions causing dust accumulation or abort
4. **Claim logic bypass** — Missing cumulative claim tracking allowing repeated claims
5. **Fee accounting mismatch** — Wrong token denomination or missing deduction in fee calculation
6. **Forced withdrawal manipulation** — Bypassing tolerance checks via specific position states

---

## Pattern 1: Incorrect Reward Initialization Timing — move-defi-001

**Frequency**: 2/29 reports (Echelon [R1], Bluefin Spot [R5])
**Severity consensus**: HIGH
**Validation**: Moderate — 2 independent protocols

### Attack Scenario
1. Protocol starts a new reward program at time T1
2. Users who staked before T1 have their reward start initialized to T1 (current time)
3. Reward accumulation for the new program starts from T1 for all users
4. Early stakers who contributed liquidity before T1 lose proportional rewards
5. Alternatively, rewards accumulate during inactive gap periods, inflating payouts

### Vulnerable Pattern Example

**Example 1: Echelon — Reward Timestamp Initialized to Current Block** [HIGH] [R1]
```move
// ❌ VULNERABLE: New reward program starts all users at current time
public fun add_reward_program(admin: &signer, pool: &mut Pool, reward_token: TypeInfo) {
    let program = RewardProgram {
        reward_token,
        // ❌ Users who staked before this point lose rewards for pre-existing stake
        start_time: timestamp::now_seconds(),
        accumulated_per_share: 0,
    };
    vector::push_back(&mut pool.reward_programs, program);
}
```

**Example 2: Bluefin Spot — Rewards Accumulate During Inactive Gap** [HIGH] [R5]
```move
// ❌ VULNERABLE: Restart doesn't account for inactive period [t0, t1]
public fun restart_rewards(pool: &mut Pool, clock: &Clock) {
    let now = clock::timestamp_ms(clock);
    // ❌ accumulated_per_share continues from last value
    // Gap between pause and restart generates phantom rewards
    pool.reward_state.last_update = now;
    pool.reward_state.is_active = true;
    // LPs receive rewards for period with zero trading activity
}
```

### Secure Implementation
```move
// ✅ SECURE: Snapshot accumulated_per_share before restart
public fun restart_rewards(pool: &mut Pool, clock: &Clock) {
    let now = clock::timestamp_ms(clock);
    // ✅ Reset accumulated to current state, no phantom rewards
    pool.reward_state.accumulated_per_share = calculate_current_accumulated(pool);
    pool.reward_state.last_update = now;
    pool.reward_state.is_active = true;
}
```

---

## Pattern 2: Missing Solvency Check on Withdrawals — move-defi-002

**Frequency**: 3/29 reports (Echelon [R1], Kofi Finance [R9], Canopy [R11])
**Severity consensus**: HIGH
**Validation**: Strong — 3 independent protocols

### Attack Scenario
1. User has deposited collateral and borrowed against it
2. Withdrawal function does not check post-withdrawal collateral ratio
3. User withdraws collateral while keeping debt, becoming undercollateralized
4. Protocol becomes insolvent; remaining depositors cannot withdraw

### Vulnerable Pattern Example

**Example 1: Echelon — No Collateral vs Debt Validation** [HIGH] [R1]
```move
// ❌ VULNERABLE: No solvency check after withdrawal
public fun withdraw_collateral(
    account: &signer,
    pool: &mut Pool,
    amount: u64,
) {
    let user_addr = signer::address_of(account);
    let position = table::borrow_mut(&mut pool.positions, user_addr);
    
    assert!(position.collateral >= amount, E_INSUFFICIENT_COLLATERAL);
    position.collateral = position.collateral - amount;
    
    // ❌ Missing: assert!(calculate_health_factor(position) >= MIN_HEALTH_FACTOR)
    // User can withdraw all collateral while retaining debt
    
    transfer_to_user(pool, user_addr, amount);
}
```

**Example 2: Kofi Finance — Validator Removal Without Safe Unstaking** [HIGH] [R9]
```move
// ❌ VULNERABLE: Validator removed but staked funds not recovered
public fun remove_validator(admin: &signer, pool: &mut StakingPool, validator: address) {
    assert!(is_admin(pool, signer::address_of(admin)), E_UNAUTHORIZED);
    
    // ❌ Removes validator from list but doesn't unstake or migrate funds
    let (found, idx) = vector::index_of(&pool.validators, &validator);
    assert!(found, E_NOT_FOUND);
    vector::swap_remove(&mut pool.validators, idx);
    
    // Staked funds on removed validator become irretrievable
    // Pool becomes insolvent as backing < supply
}
```

### Secure Implementation
```move
// ✅ SECURE: Validate solvency after withdrawal
public fun withdraw_collateral(
    account: &signer,
    pool: &mut Pool,
    amount: u64,
) {
    let user_addr = signer::address_of(account);
    let position = table::borrow_mut(&mut pool.positions, user_addr);
    
    assert!(position.collateral >= amount, E_INSUFFICIENT_COLLATERAL);
    position.collateral = position.collateral - amount;
    
    // ✅ Post-withdrawal health factor check
    let health_factor = calculate_health_factor(position, pool);
    assert!(health_factor >= MIN_HEALTH_FACTOR, E_WOULD_BE_INSOLVENT);
    
    transfer_to_user(pool, user_addr, amount);
}
```

---

## Pattern 3: Flashloan Repayment Bypass via Double Scaling — move-defi-003

**Frequency**: 1/29 reports (ThalaSwap V2 [R2]) — but CRITICAL severity
**Severity consensus**: CRITICAL
**Validation**: Weak — single protocol, but critical impact warrants inclusion

### Vulnerable Pattern Example

**ThalaSwap V2 — Double Upscaling in Flashloan Repayment** [CRITICAL] [R2]
```move
// ❌ VULNERABLE: balances_after_flashloan applies upscaling twice
public fun flashloan_repay<X, Y>(
    pool: &mut Pool<X, Y>,
    coin_x: Coin<X>,
    coin_y: Coin<Y>,
) {
    let balance_x = coin::value(&coin_x);
    let balance_y = coin::value(&coin_y);
    
    // ❌ upscale_metastable_amounts already called when calculating expected repayment
    // Calling it again on actual balances means repayment check is:
    // upscale(actual) >= upscale(upscale(expected))  → always passes with less
    let (scaled_x, scaled_y) = upscale_metastable_amounts(balance_x, balance_y);
    
    assert!(scaled_x >= pool.expected_repay_x && scaled_y >= pool.expected_repay_y, E_INSUFFICIENT);
    // Attacker repays less than borrowed amount
}
```

### Secure Implementation
```move
// ✅ SECURE: Compare balances at same scaling level
public fun flashloan_repay<X, Y>(
    pool: &mut Pool<X, Y>,
    coin_x: Coin<X>,
    coin_y: Coin<Y>,
) {
    let balance_x = coin::value(&coin_x);
    let balance_y = coin::value(&coin_y);
    
    // ✅ No double scaling — compare raw balances against raw expected
    assert!(balance_x >= pool.expected_repay_x && balance_y >= pool.expected_repay_y, E_INSUFFICIENT);
}
```

---

## Pattern 4: Excessive Claims via Missing Cumulative Tracking — move-defi-004

**Frequency**: 2/29 reports (Mysten Republic [R12], Canopy [R11])
**Severity consensus**: CRITICAL
**Validation**: Moderate — 2 independent protocols

### Vulnerable Pattern Example

**Example 1: Mysten Republic — No Cumulative Claim Check** [CRITICAL] [R12]
```move
// ❌ VULNERABLE: Each claim only checks current unlock, not cumulative
public fun claim_tokens(
    vesting: &mut VestingSchedule,
    user: &signer,
    amount: u64,
    clock: &Clock,
) {
    let unlocked = calculate_unlocked(vesting, clock::timestamp_ms(clock));
    // ❌ Missing cumulative check: amount + total_claimed <= unlocked
    assert!(amount <= unlocked, E_EXCEEDS_UNLOCKED);
    
    // User calls claim(50) then claim(50) when only 50 total is unlocked
    vesting.tokens_transferred = vesting.tokens_transferred + amount;
    transfer_tokens(vesting, signer::address_of(user), amount);
}
```

**Example 2: Canopy — Partial Claims Not Tracked in Distribution** [HIGH] [R11]
```move
// ❌ VULNERABLE: Claim formula ignores previous partial claims
public fun claim_reward(
    deployment: &mut Deployment,
    user: &signer,
    amount: u64,
) {
    let user_share = calculate_share(deployment, signer::address_of(user));
    // ❌ Doesn't subtract previously claimed amounts
    // User can claim full share multiple times across deployments
    assert!(amount <= user_share, E_EXCEEDS_SHARE);
    transfer_reward(deployment, signer::address_of(user), amount);
}
```

### Secure Implementation
```move
// ✅ SECURE: Track cumulative claims
public fun claim_tokens(
    vesting: &mut VestingSchedule,
    user: &signer,
    amount: u64,
    clock: &Clock,
) {
    let unlocked = calculate_unlocked(vesting, clock::timestamp_ms(clock));
    // ✅ Check cumulative: already claimed + new claim <= total unlocked
    assert!(vesting.tokens_transferred + amount <= unlocked, E_EXCEEDS_UNLOCKED);
    vesting.tokens_transferred = vesting.tokens_transferred + amount;
    transfer_tokens(vesting, signer::address_of(user), amount);
}
```

---

## Pattern 5: Fee Accounting Mismatch — move-defi-005

**Frequency**: 4/29 reports (DeepBook V3 [R6], Aftermath MM [R4], Kofi Finance [R9], EthSign [related])
**Severity consensus**: HIGH
**Validation**: Strong — 4 independent protocols

### Vulnerable Pattern Example

**Example 1: DeepBook V3 — Fee Falls Through to Wrong Token** [HIGH] [R6]
```move
// ❌ VULNERABLE: Zero deep_quantity causes fee denomination switch
public fun calculate_fee(order: &Order): (u64, u64, u64) {
    let deep_fee = 0;
    let base_fee = 0;
    let quote_fee = 0;
    
    if (order.deep_quantity > 0) {
        deep_fee = calculate_deep_fee(order);
    } else {
        // ❌ Falls through: fee paid in base/quote instead of DEEP
        // Different token denomination changes economic impact
        base_fee = calculate_base_fee(order);
        quote_fee = calculate_quote_fee(order);
    };
    (deep_fee, base_fee, quote_fee)
}
```

**Example 2: Aftermath MM — LP Split Ratio Bypass** [HIGH] [R4]
```move
// ❌ VULNERABLE: provided_value_usd split incorrectly applied
public fun split_user_lp_coin(
    vault: &mut Vault,
    user_lp: &mut Coin<LP>,
    provided_value_usd: u64,
) {
    // ❌ Split ratio uses provided_value_usd but fee is calculated
    // on the smaller split portion instead of the full withdrawal
    let split_amount = calculate_split(vault, provided_value_usd);
    let fee = calculate_fee(split_amount);  // ❌ Should be on full amount
    // Users withdraw large amounts with fees only on small portion
}
```

**Example 3: Kofi Finance — Buffer Vault Drainage** [HIGH] [R9]
```move
// ❌ VULNERABLE: kAPT mint/burn ignores staking fees
public fun wrap_to_buffer(pool: &mut Pool, amount: u64) {
    let kapt_amount = calculate_kapt(amount);  // Based on full amount
    mint_kapt(pool, kapt_amount);
    
    // ❌ Actual APT staked is (amount - staking_fee)
    // But kAPT minted is based on full amount
    // Buffer has more kAPT than APT backing → burn exceeds balance
    stake_apt(pool, amount);  // Fee deducted internally
}
```

### Secure Implementation
```move
// ✅ SECURE: Deduct fees before share calculation
public fun wrap_to_buffer(pool: &mut Pool, amount: u64) {
    let net_amount = amount - calculate_staking_fee(amount);
    let kapt_amount = calculate_kapt(net_amount);  // ✅ Based on net amount
    mint_kapt(pool, kapt_amount);
    stake_apt(pool, amount);
}
```

---

## Pattern 6: Forced Withdrawal Tolerance Bypass — move-defi-006

**Frequency**: 2/29 reports (Aftermath MM [R4])
**Severity consensus**: CRITICAL
**Validation**: Weak — single protocol, but critical impact

### Vulnerable Pattern Example

**Aftermath MM — Zero Base Position Skips Tolerance Check** [CRITICAL] [R4]
```move
// ❌ VULNERABLE: Tolerance check skipped when base is zero
public fun force_withdraw(
    vault: &mut Vault,
    position: &mut Position,
    output_amount: u64,
) {
    if (position.base_amount > 0) {
        // Normal tolerance check
        assert!(is_within_tolerance(position, output_amount), E_SLIPPAGE);
    };
    // ❌ If base_amount == 0, no slippage check at all
    // Attacker sets unrealistic output_amount
    
    execute_withdrawal(vault, position, output_amount);
}
```

**Aftermath MM — Negative Slippage Conversion to Positive** [CRITICAL] [R4]
```move
// ❌ VULNERABLE: Signed-to-unsigned conversion flips negative to large positive
public fun end_withdraw_session(vault: &mut Vault, session: WithdrawSession) {
    let slippage = calculate_slippage(session);  // Returns signed value
    
    // ❌ ifixed::to_balance() converts negative to large positive u64
    // Attacker benefits from negative slippage at vault's expense
    let balance_adjustment = ifixed::to_balance(slippage);
    transfer_to_user(vault, session.user, session.amount + balance_adjustment);
}
```

### Secure Implementation
```move
// ✅ SECURE: Always enforce tolerance, handle signed values correctly
public fun force_withdraw(vault: &mut Vault, position: &mut Position, output_amount: u64) {
    // ✅ Tolerance check regardless of position size
    assert!(is_within_tolerance(position, output_amount), E_SLIPPAGE);
    execute_withdrawal(vault, position, output_amount);
}

public fun end_withdraw_session(vault: &mut Vault, session: WithdrawSession) {
    let slippage = calculate_slippage(session);
    // ✅ Only apply positive slippage (user benefit), absorb negative
    let adjustment = if (ifixed::is_positive(slippage)) {
        ifixed::to_balance(slippage)
    } else {
        0
    };
    transfer_to_user(vault, session.user, session.amount + adjustment);
}
```

---

## Pattern 7: State Desynchronization Between Modules — move-defi-007

**Frequency**: 2/29 reports (Solend Steamm [R3], Mysten Walrus [R8])
**Severity consensus**: HIGH
**Validation**: Moderate — 2 independent protocols

### Vulnerable Pattern Example

**Example 1: Solend Steamm — Bank/LendingMarket Desync** [MEDIUM] [R3]
```move
// ❌ VULNERABLE: Obligations created without Bank module awareness
public fun create_obligation(market: &mut LendingMarket, user: &signer) {
    // Created directly in LendingMarket
    let obligation = Obligation { user: signer::address_of(user), ... };
    table::add(&mut market.obligations, signer::address_of(user), obligation);
    // ❌ Bank module doesn't know about this obligation
    // Lending operations using Bank data are inconsistent
}
```

**Example 2: Mysten Walrus — Commission Rate Used From Future Epoch** [HIGH] [R8]
```move
// ❌ VULNERABLE: Future commission rate used for current distribution
public fun distribute_rewards(pool: &mut StakingPool, epoch: u64) {
    // ❌ commission_rate may have been updated for next epoch
    // but distribution is for current epoch
    let commission = pool.commission_rate;  // ❌ May be future rate
    let protocol_share = rewards * commission / 10000;
    let staker_share = rewards - protocol_share;
}
```

### Secure Implementation
```move
// ✅ SECURE: Use epoch-specific commission rate
public fun distribute_rewards(pool: &mut StakingPool, epoch: u64) {
    let commission = get_commission_for_epoch(pool, epoch);  // ✅ Epoch-specific
    let protocol_share = rewards * commission / 10000;
    let staker_share = rewards - protocol_share;
}
```

---

## Pattern 8: Permissionless Front-Running of Auctions/Orders — move-defi-008

**Frequency**: 2/29 reports (Mayan Sui [R14], Emojicoin [R15])
**Severity consensus**: HIGH
**Validation**: Moderate — 2 independent protocols

### Vulnerable Pattern Example

**Example 1: Mayan Sui — Driver Check Only After Penalty Period** [HIGH] [R14]
```move
// ❌ VULNERABLE: Anyone can fulfill before penalty period starts
public fun fulfill_order(
    state: &mut State,
    order: &mut Order,
    fulfiller: &signer,
    clock: &Clock,
) {
    let now = clock::timestamp_ms(clock);
    let penalty_start = order.created_at + AUCTION_DURATION;
    
    if (now >= penalty_start) {
        // Only designated driver can fulfill during penalty period
        assert!(signer::address_of(fulfiller) == order.driver, E_NOT_DRIVER);
    };
    // ❌ Before penalty_start, ANYONE can fulfill
    // Front-runner steals auction winner's fill
    
    execute_fill(state, order, fulfiller);
}
```

**Example 2: Emojicoin — Pool Creation Front-Running** [HIGH] [R15]
```move
// ❌ VULNERABLE: No per-address pool creation limit
public fun create_pool(creator: &signer, emoji: vector<u8>) {
    // ❌ No rate limit or cooldown per address
    // Attacker creates pools with all popular emojis
    // Inflates prices, captures matched funds from vault
    let pool = Pool { creator: signer::address_of(creator), emoji, ... };
    // ...
}
```

### Secure Implementation
```move
// ✅ SECURE: Designated driver always has priority
public fun fulfill_order(
    state: &mut State,
    order: &mut Order,
    fulfiller: &signer,
    clock: &Clock,
) {
    let now = clock::timestamp_ms(clock);
    let driver_exclusive_end = order.created_at + DRIVER_EXCLUSIVE_PERIOD;
    
    if (now < driver_exclusive_end) {
        // ✅ Only driver can fulfill during exclusive window
        assert!(signer::address_of(fulfiller) == order.driver, E_NOT_DRIVER);
    };
    execute_fill(state, order, fulfiller);
}
```

---

## Pattern 9: Incorrect Withdrawal/Vesting Abort Conditions — move-defi-009

**Frequency**: 3/29 reports (Kofi Finance [R9], Magna [R13], Aptos Securitize [R10])
**Severity consensus**: HIGH
**Validation**: Strong — 3 independent protocols

### Vulnerable Pattern Example

**Example 1: Kofi Finance — Faulty Withdrawal Split Logic** [MEDIUM] [R9]
```move
// ❌ VULNERABLE: Assumes amount > minimum_pending_inactive threshold
public fun process_withdrawal(pool: &mut Pool, amount: u64) {
    let min_threshold = get_minimum_pending_inactive();
    // ❌ If amount < min_threshold due to rounding or parameter changes,
    // subtraction underflows → transaction aborts
    let remaining = amount - min_threshold;  // ❌ Can underflow
    split_withdrawal(pool, remaining, min_threshold);
}
```

**Example 2: Magna — Cancellation Ignores Cliff** [HIGH] [R13]
```move
// ❌ VULNERABLE: Cancellation logic doesn't consider cliff_timestamp
public fun cancel_vesting(admin: &signer, schedule: &mut VestingSchedule) {
    let now = timestamp::now_seconds();
    let last_period = schedule.start + schedule.period_count * schedule.period_duration;
    
    // ❌ When cliff > last_period, this incorrectly rejects valid cancellations
    assert!(now >= schedule.start && now <= last_period, E_INVALID_TIME);
    // Valid cancellation blocked → user funds locked longer than intended
}
```

**Example 3: Aptos Securitize — Zero-Value FA Blocks Withdrawals** [HIGH] [R10]
```move
// ❌ VULNERABLE: Zero-value withdrawal increments counter
public fun withdraw(account: &signer, store: &mut TokenStore, amount: u64) {
    // ❌ No check that amount > 0
    // Withdrawing 0 increments withdrawal counter
    store.withdrawal_count = store.withdrawal_count + 1;
    
    if (store.withdrawal_count >= MAX_WITHDRAWALS) {
        // All future withdrawals blocked
        abort E_MAX_WITHDRAWALS_REACHED
    };
    // ...
}
```

### Secure Implementation
```move
// ✅ SECURE: Validate amount > 0, handle edge cases
public fun withdraw(account: &signer, store: &mut TokenStore, amount: u64) {
    assert!(amount > 0, E_ZERO_AMOUNT);
    // ✅ Only meaningful withdrawals count
    store.withdrawal_count = store.withdrawal_count + 1;
    assert!(store.withdrawal_count < MAX_WITHDRAWALS, E_MAX_WITHDRAWALS_REACHED);
    // ...
}
```

---

## Pattern 10: Reward Accumulation During Inactive/Paused Periods — move-defi-010

**Frequency**: 2/29 reports (Bluefin Spot, Thala Staked LPT)
**Severity consensus**: MEDIUM (lowest across auditors)
**Validation**: Moderate — 2 independent protocols

### Attack Scenario
1. Reward distribution is paused or ended
2. When restarted, the system includes the inactive gap in reward calculations
3. `rewards_per_second * (current_time - last_update_time)` includes the gap
4. LPs receive unearned excess rewards, depleting the reward pool faster

### Vulnerable Pattern Example

**Example: Bluefin Spot — Inactive Periods Counted in Reward Accrual** [MEDIUM]
```move
// ❌ VULNERABLE: Inactive time included in reward calculation
public(friend) fun update_reward_infos(pool: &mut Pool, current_timestamp: u64): vector<u128> {
    let reward_info = &mut pool.reward_infos[i];
    if (current_timestamp > reward_info.last_update_time) {
        let min_timestamp = math64::min(current_timestamp, reward_info.end_time);
        if (pool.liquidity != 0 && min_timestamp > reward_info.last_update_time) {
            // BUG: Includes gap between old end_time and new start_time
            let rewards = (min_timestamp - reward_info.last_update_time) * reward_info.reward_per_seconds;
            reward_info.growth_global = reward_info.growth_global + (rewards / pool.liquidity);
        };
        reward_info.last_update_time = current_timestamp;
    };
}
```

### Secure Implementation
```move
// ✅ SECURE: Reset last_update_time when restarting rewards
public(friend) fun restart_rewards(pool: &mut Pool, new_start: u64, new_end: u64, rate: u128) {
    let reward_info = &mut pool.reward_infos[i];
    reward_info.last_update_time = new_start; // Skip the gap
    reward_info.end_time = new_end;
    reward_info.reward_per_seconds = rate;
}
```

---

## Pattern 11: Tolerance Check Bypass via Forced Withdrawal Path — move-defi-011

**Frequency**: 1/29 reports (Aftermath MM)
**Severity consensus**: CRITICAL (single auditor)
**Validation**: Weak — single auditor, but Critical severity

### Attack Scenario
1. User sets unrealistically high minimum expected balance, locking the withdrawal session
2. After a timeout, forced withdrawal path is triggered
3. Forced withdrawal bypasses margin tolerance checks when closing positions
4. Market orders execute without slippage control, exposing vault to significant losses

### Vulnerable Pattern Example

**Example: Aftermath MM — Forced Withdrawal Bypasses Margin Tolerance** [CRITICAL]
```move
// ❌ VULNERABLE: Force withdraw skips tolerance validation
public fun process_force_withdraw<T>(vault: &mut Vault, clearing_house: &mut ClearingHouse<T>) {
    // No tolerance check — market orders close all positions immediately
    close_all_positions_with_market_orders(vault, clearing_house);
    let balance = calculate_final_balance(vault);
    // User gets whatever remains after uncontrolled execution
    transfer_to_user(balance);
}
```

### Secure Implementation
```move
// ✅ SECURE: Enforce tolerance even in forced withdrawal
public fun process_force_withdraw_safe<T>(vault: &mut Vault, clearing_house: &mut ClearingHouse<T>) {
    close_all_positions_with_market_orders(vault, clearing_house);
    let balance = calculate_final_balance(vault);
    assert!(
        balance >= vault.min_expected_balance * TOLERANCE_FACTOR / 100,
        E_SLIPPAGE_EXCEEDED
    );
    transfer_to_user(balance);
}
```

---

## Pattern 12: LP Fee Manipulation via Split/Merge Rounding — move-defi-012

**Frequency**: 1/29 reports (Aftermath MM)
**Severity consensus**: MEDIUM (single auditor)
**Validation**: Weak — single auditor, but clear economic exploit

### Attack Scenario
1. LP coin tracks `provided_value_usd` for fee calculation at withdrawal
2. Repeated split operations cause rounding errors that reduce `provided_value_usd`
3. Attacker splits and rejoins LP coins, each time losing rounding dust from the tracker
4. At withdrawal, reduced tracker means lower fees or even a profit

### Vulnerable Pattern Example

**Example: Aftermath MM — Split Rounding Erodes Fee Tracker** [MEDIUM]
```move
// ❌ VULNERABLE: Repeated splits cause rounding loss in provided_value_usd
public(package) fun split_user_lp_coin<L>(user_lp: &mut UserLpCoin<L>, amount: u64): UserLpCoin<L> {
    let split_ratio = ifixed::div(
        ifixed::from_balance(amount, scaling),
        ifixed::from_balance(user_lp.lp_balance.value(), scaling),
    );
    let new_provided = ifixed::mul(user_lp.provided_value_usd, split_ratio);
    user_lp.provided_value_usd = user_lp.provided_value_usd - new_provided;
    // Each split loses rounding dust from provided_value_usd
    UserLpCoin { lp_balance: user_lp.lp_balance.split(amount), provided_value_usd: new_provided }
}
```

### Secure Implementation
```move
// ✅ SECURE: Use actual LP balance ratio at withdrawal time for fees
public fun calculate_fee(user_lp: &UserLpCoin, current_vault_value: u256): u256 {
    let current_value = (user_lp.lp_balance.value() as u256) * current_vault_value / total_lp_supply;
    if (current_value > user_lp.provided_value_usd) {
        (current_value - user_lp.provided_value_usd) * FEE_RATE / PRECISION
    } else { 0 }
}
```

---

## Pattern 13: Boolean Logic Error in Time/Condition Checks — move-defi-013

**Frequency**: 3/29 reports (Aptos Securitize, Kofi Finance, Bluefin Spot)
**Severity consensus**: HIGH (lowest across auditors)
**Validation**: Strong — 3 independent auditors

### Attack Scenario
1. Time validation uses `||` (OR) where `&&` (AND) is required
2. Condition always evaluates to true because one operand is trivially true
3. Critical time-based restrictions are completely disabled
4. Attackers bypass flowback periods, trading windows, or cooldowns

### Vulnerable Pattern Example

**Example: Aptos Securitize — OR Instead of AND Disables Time Check** [HIGH]
```move
// ❌ VULNERABLE: || makes the function always return true when end_time != 0
fun is_block_flowback_end_time_ok(block_flowback_end_time: u256): bool {
    block_flowback_end_time != 0
        || (timestamp::now_seconds() as u256) < block_flowback_end_time
    // Should be && — the timestamp check is never reached
}
```

### Secure Implementation
```move
// ✅ SECURE: Use AND to require both conditions
fun is_block_flowback_end_time_ok(block_flowback_end_time: u256): bool {
    block_flowback_end_time != 0
        && (timestamp::now_seconds() as u256) < block_flowback_end_time
}
```

---

## Pattern 14: Buffer/Pool Drainage from Asymmetric Mint-Burn Accounting — move-defi-014

**Frequency**: 2/29 reports (Kofi Finance, Thala LSD)
**Severity consensus**: HIGH (lowest across auditors)
**Validation**: Moderate — 2 independent protocols

### Attack Scenario
1. Protocol mints derivative tokens for `amount - fee` but burns full `amount`
2. The burn > mint discrepancy drains the buffer/vault on each operation
3. After enough cycles, the buffer is empty and user withdrawals fail
4. Protocol becomes insolvent despite no external attack

### Vulnerable Pattern Example

**Example: Kofi Finance — Buffer Burns More Than It Mints** [HIGH]
```move
// ❌ VULNERABLE: Burns `amount_needed` but mints `amount_needed - fee`
public(friend) fun ensure_minimum_amounts_from_buffer(pool_address: address) {
    let amount_needed = min_pending_inactive - pending_inactive;
    delegation_pool::add_stake(&vault_signer, pool_address, amount_needed);
    let add_stake_fee = delegation_pool::get_add_stake_fee(pool_address, amount_needed);
    // Mints less than it burns
    kAPT_coin::mint(buffer_addr, amount_needed - add_stake_fee);
    delegation_pool::unlock(&vault_signer, pool_address, amount_needed);
    kAPT_coin::burn(&buffer_signer, amount_needed); // Burns the full amount
}
```

### Secure Implementation
```move
// ✅ SECURE: Symmetric mint and burn amounts
public(friend) fun ensure_minimum_amounts_safe(pool_address: address) {
    let amount_needed = min_pending_inactive - pending_inactive;
    delegation_pool::add_stake(&vault_signer, pool_address, amount_needed);
    let add_stake_fee = delegation_pool::get_add_stake_fee(pool_address, amount_needed);
    let net_amount = amount_needed - add_stake_fee;
    kAPT_coin::mint(buffer_addr, net_amount);
    delegation_pool::unlock(&vault_signer, pool_address, net_amount);
    kAPT_coin::burn(&buffer_signer, net_amount); // Burns same as minted
}
```

---

## Pattern 15: Validator/Operator Removal Without Stake Migration — move-defi-015

**Frequency**: 2/29 reports (Kofi Finance, Mysten Walrus)
**Severity consensus**: HIGH (lowest across auditors)
**Validation**: Moderate — 2 independent protocols

### Attack Scenario
1. Admin removes a validator from the protocol's pool set
2. Existing stakes on the removed validator have no migration path
3. Staked funds become irretrievable — protocol is temporarily insolvent
4. Users cannot unstake until the validator is re-added or emergency action is taken

### Vulnerable Pattern Example

**Example: Kofi Finance — Validator Removal Orphans Staked Funds** [HIGH]
```move
// ❌ VULNERABLE: No stake migration when validator is removed
public entry fun remove_validator(admin: &signer, pool_address: address) {
    assert!(is_admin(admin), ERR_UNAUTHORIZED);
    let pools = borrow_global_mut<ValidatorPools>(@module);
    vector::remove_value(&mut pools.active, pool_address);
    // BUG: Existing stakes on this validator are now orphaned
}
```

### Secure Implementation
```move
// ✅ SECURE: Migrate stakes before removal
public entry fun remove_validator_safe(admin: &signer, pool_address: address) {
    assert!(is_admin(admin), ERR_UNAUTHORIZED);
    // First unstake all funds from this validator
    let staked = get_validator_total_stake(pool_address);
    assert!(staked == 0, E_VALIDATOR_HAS_ACTIVE_STAKES);
    let pools = borrow_global_mut<ValidatorPools>(@module);
    vector::remove_value(&mut pools.active, pool_address);
}
```

---

## Pattern 16: Price Boundary Check Allows Swap Beyond Limits — move-defi-016

**Frequency**: 2/29 reports (Bluefin Spot, Solend Steamm)
**Severity consensus**: MEDIUM (lowest across auditors)
**Validation**: Moderate — 2 independent protocols

### Attack Scenario
1. Swap validates `sqrt_price_limit >= min_sqrt_price` using `>=` instead of `>`
2. At the exact boundary, the swap can push the price to or beyond min/max tick
3. Pool enters an invalid price state at tick boundaries
4. Subsequent operations may fail or produce incorrect results

### Vulnerable Pattern Example

**Example: Bluefin Spot — Non-Strict Boundary Check** [MEDIUM]
```move
// ❌ VULNERABLE: >= allows price at exact boundary
fun swap_in_pool(pool: &mut Pool, a2b: bool, amount: u64, sqrt_price_limit: u128) {
    if (a2b) {
        assert!(
            pool.current_sqrt_price > sqrt_price_limit
                && sqrt_price_limit >= tick_math::min_sqrt_price(), // BUG: >= allows boundary
            E_INVALID_PRICE
        );
    } else {
        assert!(
            pool.current_sqrt_price < sqrt_price_limit
                && sqrt_price_limit <= tick_math::max_sqrt_price(), // BUG: <= allows boundary
            E_INVALID_PRICE
        );
    };
}
```

### Secure Implementation
```move
// ✅ SECURE: Strict inequalities prevent boundary state
if (a2b) {
    assert!(
        pool.current_sqrt_price > sqrt_price_limit
            && sqrt_price_limit > tick_math::min_sqrt_price(),
        E_INVALID_PRICE
    );
}
```

---

## Pattern 17: Incorrect Commission/Fee Rate Applied During Epoch Transitions — move-defi-017

**Frequency**: 2/29 reports (Mysten Walrus, Kofi Finance)
**Severity consensus**: MEDIUM (lowest across auditors)
**Validation**: Moderate — 2 independent protocols

### Attack Scenario
1. During epoch transition, protocol applies pending (future) commission rate for current epoch
2. Operators receive rewards calculated at the wrong rate
3. If new rate is higher, operators receive excess commission at stakers' expense
4. If new rate is lower, operators lose legitimate commission

### Vulnerable Pattern Example

**Example: Mysten Walrus — Pending Rate Used Before Activation** [MEDIUM]
```move
// ❌ VULNERABLE: Applies new commission rate to current epoch rewards
fun advance_epoch(pool: &mut StakingPool) {
    // Update to pending rate first
    pool.commission_rate = pool.pending_commission_rate;
    // Then calculate rewards — uses the NEW rate, not the old one
    let commission = pool.epoch_rewards * pool.commission_rate / RATE_SCALE;
    transfer_commission(pool.operator, commission);
}
```

### Secure Implementation
```move
// ✅ SECURE: Calculate with old rate, then update
fun advance_epoch_safe(pool: &mut StakingPool) {
    // Calculate rewards with current (old) rate
    let commission = pool.epoch_rewards * pool.commission_rate / RATE_SCALE;
    transfer_commission(pool.operator, commission);
    // Then update to pending rate for next epoch
    pool.commission_rate = pool.pending_commission_rate;
}
```

---

## Pattern 18: Stake Threshold Bypass via Post-Registration Withdrawal — move-defi-018

**Frequency**: 1/29 reports (Mysten Walrus)
**Severity consensus**: MEDIUM (single auditor)
**Validation**: Weak — single auditor, but Medium severity

### Attack Scenario
1. Active set requires minimum stake threshold to join
2. User stakes above threshold to enter the active set
3. Immediately withdraws stake below threshold via `update` function
4. `update` doesn't re-validate minimum threshold, so user stays in the active set

### Vulnerable Pattern Example

**Example: Mysten Walrus — No Threshold Re-Check on Update** [MEDIUM]
```move
// ❌ VULNERABLE: update doesn't validate minimum threshold
public(package) fun update(set: &mut ActiveSet, node_id: ID, new_staked_amount: u64): bool {
    let idx = find_node(set, node_id);
    idx.do!(|i| {
        set.total_stake = set.total_stake + new_staked_amount - set.nodes[i].staked_amount;
        set.nodes[i].staked_amount = new_staked_amount;
        // No check: new_staked_amount >= minimum_threshold
    });
    true
}
```

### Secure Implementation
```move
// ✅ SECURE: Enforce threshold on update
public(package) fun update_safe(set: &mut ActiveSet, node_id: ID, new_staked_amount: u64): bool {
    if (new_staked_amount < set.minimum_threshold) {
        remove_node(set, node_id);
        return false
    };
    let idx = find_node(set, node_id);
    idx.do!(|i| {
        set.total_stake = set.total_stake + new_staked_amount - set.nodes[i].staked_amount;
        set.nodes[i].staked_amount = new_staked_amount;
    });
    true
}
```

---

## Pattern 19: Uncapped Minting Drains Reward Pools — move-defi-019

**Frequency**: 2/29 reports (Thala Staked LPT, Thala LSD)
**Severity consensus**: MEDIUM (lowest across auditors)
**Validation**: Moderate — 2 independent protocols (same ecosystem)

### Attack Scenario
1. Protocol allows unlimited minting of derivative tokens (xLPT, sthAPT)
2. Attacker mints massive amount and stakes to capture disproportionate rewards
3. `acc_rewards_per_share` dilution is insufficient because attacker controls majority
4. Legitimate stakers receive negligible rewards

### Vulnerable Pattern Example

**Example: Thala Staked LPT — No Rate Limit on xLPT Minting** [MEDIUM]
```move
// ❌ VULNERABLE: No cap or rate limit on minting
public entry fun mint_xlpt(user: &signer, amount: u64) acquires Farming {
    let farming = borrow_global_mut<Farming>(@module);
    // No limit check — user can mint any amount
    let xlpt = fungible_asset::mint(&farming.mint_ref, amount);
    primary_fungible_store::deposit(signer::address_of(user), xlpt);
    // User now has disproportionate share of rewards
}
```

### Secure Implementation
```move
// ✅ SECURE: Rate-limited minting per epoch
public entry fun mint_xlpt_safe(user: &signer, amount: u64) acquires Farming {
    let farming = borrow_global_mut<Farming>(@module);
    let user_addr = signer::address_of(user);
    let minted_this_epoch = get_epoch_minted(farming, user_addr);
    assert!(minted_this_epoch + amount <= MAX_MINT_PER_EPOCH, E_RATE_LIMITED);
    update_epoch_minted(farming, user_addr, minted_this_epoch + amount);
    let xlpt = fungible_asset::mint(&farming.mint_ref, amount);
    primary_fungible_store::deposit(user_addr, xlpt);
}
```

---

## Pattern 20: Snapshot Integrity Compromised by Token Merge During Capture — move-defi-020

**Frequency**: 1/29 reports (Mysten Republic)
**Severity consensus**: HIGH (single auditor)
**Validation**: Weak — single auditor, but High severity

### Attack Scenario
1. Protocol takes a snapshot of token balances for dividend distribution
2. During the snapshot process, users can merge (join) snapshotted tokens with non-snapshotted ones
3. This alters total supply and individual balances mid-snapshot
4. Dividend calculations from the corrupted snapshot are incorrect

### Vulnerable Pattern Example

**Example: Mysten Republic — Token Merge During Active Snapshot** [HIGH]
```move
// ❌ VULNERABLE: No lock on token operations during snapshot
public fun join<T>(token_a: &mut SharedToken<T>, token_b: SharedToken<T>) {
    // No check if a snapshot is in progress
    let SharedToken { id, balance } = token_b;
    token_a.balance = token_a.balance + balance;
    object::delete(id);
    // Snapshot data is now stale
}
```

### Secure Implementation
```move
// ✅ SECURE: Block merges during active snapshots
public fun join_safe<T>(token_a: &mut SharedToken<T>, token_b: SharedToken<T>) {
    assert!(!is_snapshot_active<T>(), E_SNAPSHOT_IN_PROGRESS);
    let SharedToken { id, balance } = token_b;
    token_a.balance = token_a.balance + balance;
    object::delete(id);
}
```

---

## Pattern 21: Frontrunning Pool Creation for Matched Funds — move-defi-021

**Frequency**: 1/29 reports (Emojicoin)
**Severity consensus**: MEDIUM (single auditor)
**Validation**: Weak — single auditor, but clear economic exploit

### Attack Scenario
1. Protocol selects random pools for matched fund distribution (e.g., melee crank)
2. Attacker creates many pools with small amounts to increase selection probability
3. Before the crank selects, attacker buys into their own pool to drive up price
4. If selected, attacker captures a disproportionate share of matched funds

### Vulnerable Pattern Example

**Example: Emojicoin — Uncapped Pool Creation Enables Crank Manipulation** [MEDIUM]
```move
// ❌ VULNERABLE: No limit on pools per address
public entry fun create_pool(creator: &signer, emoji_bytes: vector<u8>) {
    // Any user can create unlimited pools
    let pool = Pool {
        creator: signer::address_of(creator),
        emoji_bytes,
        total_supply: 0,
    };
    register_pool(pool);
    // Attacker creates hundreds of pools to game the crank
}
```

### Secure Implementation
```move
// ✅ SECURE: Limit pools per address
public entry fun create_pool_safe(creator: &signer, emoji_bytes: vector<u8>) {
    let creator_addr = signer::address_of(creator);
    let count = get_pool_count(creator_addr);
    assert!(count < MAX_POOLS_PER_ADDRESS, E_TOO_MANY_POOLS);
    let pool = Pool { creator: creator_addr, emoji_bytes, total_supply: 0 };
    register_pool(pool);
}
```

---

## Pattern 22: Cliff Timestamp Not Included in Fully-Unlocked Calculation — move-defi-022

**Frequency**: 1/29 reports (Magna)
**Severity consensus**: MEDIUM (single auditor)
**Validation**: Weak — single auditor, but Medium severity

### Attack Scenario
1. `cancel_schedule_interval` calculates `fully_unlocked_timestamp` from unlock + periods
2. Does not account for `cliff_timestamp` which may extend the actual lock period
3. If cliff is set after the last period, function aborts prematurely
4. Valid cancellations are incorrectly rejected — admin cannot recover unvested tokens

### Vulnerable Pattern Example

**Example: Magna — Cliff Not in Fully-Unlocked Calculation** [MEDIUM]
```move
// ❌ VULNERABLE: Ignores cliff_timestamp in fully-unlocked calculation
public entry fun cancel_schedule_interval(admin: &signer, schedule: Object<Schedule>) {
    let interval = borrow_global<Interval>(schedule_addr);
    let fully_unlocked = interval.unlock_timestamp
        + (interval.number_of_periods * interval.period_length);
    // BUG: cliff_timestamp not considered — may be after fully_unlocked
    assert!(now_seconds <= fully_unlocked, ERR_ALREADY_FULLY_UNLOCKED);
}
```

### Secure Implementation
```move
// ✅ SECURE: Include cliff in fully-unlocked calculation
public entry fun cancel_schedule_interval_safe(admin: &signer, schedule: Object<Schedule>) {
    let interval = borrow_global<Interval>(schedule_addr);
    let vesting_end = interval.unlock_timestamp
        + (interval.number_of_periods * interval.period_length);
    let fully_unlocked = math64::max(vesting_end, interval.cliff_timestamp);
    assert!(now_seconds <= fully_unlocked, ERR_ALREADY_FULLY_UNLOCKED);
}
```

---

### Impact Analysis

#### Technical Impact
- Direct fund loss via flashloan bypass (1/29 reports) — CRITICAL
- Protocol insolvency via missing solvency checks (3/29 reports)
- Excessive token claims via missing cumulative tracking (2/29 reports) — CRITICAL
- Fee revenue loss via accounting mismatch (4/29 reports)
- Permanent fund lockup via withdrawal aborts (3/29 reports)
- Incorrect reward distribution (2/29 reports)

#### Business Impact
- Total protocol drainage (ThalaSwap V2 flashloan, Aftermath MM forced withdrawal)
- Depositor losses from bad debt (Echelon, Kofi, Canopy)
- Revenue leakage from fee bypass (DeepBook V3, Aftermath MM)
- User trust loss from locked withdrawals (Kofi, Magna, Securitize)

#### Affected Scenarios
- Lending/borrowing protocols (Echelon, Solend Steamm, Kuna Labs)
- AMM/DEX protocols (ThalaSwap V2, Aftermath MM, DeepBook V3)
- Liquid staking (Kofi Finance, Mysten Walrus)
- Token distribution/vesting (Mysten Republic, Magna, Canopy)
- Cross-chain DEX (Mayan Sui)

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: Reward initialization with `timestamp::now_seconds()` in add_program
- Pattern 2: `withdraw` functions missing health_factor/solvency assertions
- Pattern 3: `upscale` or `scale` called multiple times on same value
- Pattern 4: `claim` functions checking `amount <= unlocked` without `+ total_claimed`
- Pattern 5: Fee calculated on split/partial amount instead of full amount
- Pattern 6: `if (position.X > 0)` guarding tolerance/slippage checks
- Pattern 7: Signed-to-unsigned conversion via `to_balance()` or `to_u64()`
- Pattern 8: `withdraw` accepting amount=0 without guard
```

#### Audit Checklist
- [ ] Reward programs snapshot accumulated state before restart
- [ ] All withdrawal paths check post-withdrawal solvency
- [ ] Flashloan repayment compared at same scaling level
- [ ] Claim functions enforce `total_claimed + amount <= unlocked`
- [ ] Fees calculated on full amount before splits
- [ ] Slippage/tolerance checks cannot be bypassed by zero positions
- [ ] Signed-to-unsigned conversions handle negative values safely
- [ ] Zero-amount operations rejected at entry point
- [ ] Vesting cancellation considers cliff timestamps
- [ ] Module state synchronized across all entry points

### Keywords for Search

> `reward distribution`, `solvency check`, `health factor`, `withdrawal logic`, `claim exploit`, `cumulative claim`, `flashloan repayment`, `double scaling`, `upscale`, `fee calculation`, `fee bypass`, `forced withdrawal`, `tolerance check`, `slippage bypass`, `negative slippage`, `ifixed`, `to_balance`, `state desync`, `commission rate`, `front-running`, `auction`, `vesting abort`, `zero withdrawal`, `minimum liquidity`, `split ratio`, `LP token`, `move defi`, `sui defi`, `aptos defi`

### Related Vulnerabilities

- [MOVE_ARITHMETIC_PRECISION_VULNERABILITIES.md](MOVE_ARITHMETIC_PRECISION_VULNERABILITIES.md) — Precision/rounding patterns
- [MOVE_TOKEN_SUPPLY_INFLATION_VULNERABILITIES.md](MOVE_TOKEN_SUPPLY_INFLATION_VULNERABILITIES.md) — Inflation/supply manipulation
- [SUI_MOVE_DEFI_LOGIC_VULNERABILITIES.md](SUI_MOVE_DEFI_LOGIC_VULNERABILITIES.md) — Sui-specific DeFi patterns from Solodit

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

`add_reward_program`, `aptos`, `boundary`, `burn`, `calculate_fee`, `cancel_schedule_interval`, `cancel_schedule_interval_safe`, `cancel_vesting`, `claim`, `claim_mechanism`, `claim_reward`, `claim_tokens`, `create_obligation`, `create_pool`, `create_pool_safe`, `defi`, `defi_logic`, `deposit`, `distribute_rewards`, `end_withdraw_session`, `execute`, `fee`, `fee_calculation`, `flashloan_repay`, `force_withdraw`, `lending`, `liquidation`, `liquidation_flow`, `lp_token`, `move`, `reward_distribution`, `reward_miscalculation, solvency_failure, withdrawal_logic, claim_exploit, liquidation_flaw, fee_manipulation`, `rewards`, `solvency`, `solvency_check`, `staking`, `sui`, `vesting`, `withdrawal`, `withdrawal_logic`

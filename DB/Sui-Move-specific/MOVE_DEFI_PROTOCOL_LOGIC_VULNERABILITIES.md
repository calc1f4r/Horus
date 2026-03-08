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

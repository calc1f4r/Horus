---
protocol: generic
chain: sui, aptos, movement
category: denial_of_service
vulnerability_type: unbounded_growth, front_running_creation, object_limit, division_by_zero, hash_collision, overflow_abort
attack_type: denial_of_service, griefing, protocol_halt
affected_component: storage, gas, entry_points, epoch_management, pool_creation
primitives:
  - vector_growth
  - smart_table
  - primary_store
  - object_size
  - event_emission
  - resource_account
severity: high
impact: protocol_halt, fund_lockup, operational_disruption
exploitability: 0.8
financial_impact: high
tags:
  - move
  - sui
  - aptos
  - dos
  - denial_of_service
  - unbounded_growth
  - front_running
  - griefing
  - gas_exhaustion
  - division_by_zero
  - overflow
  - object_limit
  - event_limit
  - defi
language: move
version: all
---

## References
| # | Source | Protocol | Auditor | Severity |
|---|--------|----------|---------|----------|
| [R1] | reports/ottersec_move_audits/markdown/aave_aptos_v3_audit_final.md | Aave Aptos V3 | OtterSec | CRITICAL |
| [R2] | reports/ottersec_move_audits/markdown/echelon_audit_final.md | Echelon | OtterSec | HIGH |
| [R3] | reports/ottersec_move_audits/markdown/solend_steamm_audit_final.md | Solend Steamm | OtterSec | HIGH |
| [R4] | reports/ottersec_move_audits/markdown/aftermath_marketmaking_v2_audit_final.md | Aftermath MM | OtterSec | HIGH |
| [R5] | reports/ottersec_move_audits/markdown/mysten_walrus_audit_final.md | Mysten Walrus | OtterSec | HIGH |
| [R6] | reports/ottersec_move_audits/markdown/kofi_finance_audit_final.md | Kofi Finance | OtterSec | HIGH |
| [R7] | reports/ottersec_move_audits/markdown/aptos_securitize_audit_final.md | Aptos Securitize | OtterSec | HIGH |
| [R8] | reports/ottersec_move_audits/markdown/lombard_finance_move_audit_final.md | Lombard Sui | OtterSec | HIGH |
| [R9] | reports/ottersec_move_audits/markdown/ethsign_merkle_token_distributor_audit_final.md | EthSign | OtterSec | HIGH |
| [R10] | reports/ottersec_move_audits/markdown/magna_audit_final.md | Magna | OtterSec | HIGH |
| [R11] | reports/ottersec_move_audits/markdown/mysten_republic_audit_final_v2.md | Mysten Republic | OtterSec | MEDIUM |
| [R12] | reports/ottersec_move_audits/markdown/canopy_audit_final.md | Canopy | OtterSec | CRITICAL |
| [R13] | reports/ottersec_move_audits/markdown/movement_merkle_airdrop_audit_final.md | Movedrop L2 | OtterSec | CRITICAL |

## Move Denial of Service Vulnerabilities

**Comprehensive patterns for denial of service attacks in Move-based smart contracts, including unbounded storage growth, front-running resource creation, object/event limits, division by zero, overflow aborts, and hash collision attacks across Sui, Aptos, and Movement chains.**

### Overview

DoS vulnerabilities appeared in 13/29 OtterSec Move audit reports (45%). Move's abort-on-error semantics (no try/catch) make DoS particularly impactful — a single failing assertion halts the entire transaction. Combined with Sui's object size limits and Aptos's gas metering, attackers can permanently block critical protocol operations at low cost.

### Vulnerability Description

#### Root Cause Categories

1. **Unbounded vector/table growth** — Linear scan over growing collections exhausts gas
2. **Front-running resource creation** — Predictable addresses allow preemptive creation to block legitimate deployment
3. **Object/event limits** — Sui's object size limits and event emission caps cause transaction failure
4. **Division by zero** — Missing zero-value guards on denominators in arithmetic
5. **Overflow abort** — Multiplication or addition that exceeds u64 range causes abort
6. **Hash collision** — User-controlled keys in hash tables create bucket collisions

---

## Pattern 1: Unbounded Vector Growth Causing Gas Exhaustion — move-dos-001

**Frequency**: 2/29 reports (Aave Aptos V3 [R1], Aptos Securitize [R7])
**Severity consensus**: HIGH (Aave: CRITICAL for liquidation blocking)
**Validation**: Moderate — 2 independent protocols

### Attack Scenario
1. Protocol stores per-user data in a vector (rewards, accounts, etc.)
2. Attacker adds entries to the vector at negligible cost
3. Operations that iterate the vector (claim, withdraw, liquidate) exceed gas limit
4. Victim's positions become unliquidatable → protocol accumulates bad debt

### Vulnerable Pattern Example

**Example 1: Aave Aptos V3 — Unbounded Rewards Map Blocks Liquidation** [CRITICAL] [R1]
```move
// ❌ VULNERABLE: Vector-backed rewards map grows unbounded
struct UserRewards has store {
    // ❌ No upper bound — attacker adds dust reward entries
    rewards: vector<RewardEntry>,
}

public fun claim_rewards(user: &signer, pool: &mut Pool) acquires UserRewards {
    let user_rewards = borrow_global_mut<UserRewards>(signer::address_of(user));
    
    // ❌ Linear scan over all entries — gas exhaustion with large vectors
    let i = 0;
    while (i < vector::length(&user_rewards.rewards)) {
        let entry = vector::borrow(&user_rewards.rewards, i);
        process_reward(entry);
        i = i + 1;
    };
}

// ❌ Liquidation calls claim_rewards internally → liquidation also blocked
public fun liquidate(liquidator: &signer, position: &mut Position, pool: &mut Pool) {
    claim_rewards_internal(position.user, pool);  // ← Blocked by gas exhaustion
    // ... liquidation logic never reached
}
```

**Example 2: Aptos Securitize — Zero-Value Operations Inflate Count** [HIGH] [R7]
```move
// ❌ VULNERABLE: Zero-balance deposits/withdrawals still counted
public fun deposit(account: &signer, store: &mut TokenStore, fa: FungibleAsset) {
    // ❌ No minimum amount check
    // Zero-value FA still increments investor count
    store.investor_count = store.investor_count + 1;
    fungible_asset::deposit(store, fa);
}

public fun withdraw(account: &signer, store: &mut TokenStore, amount: u64) {
    // ❌ Zero-value withdrawal also modifies counter
    store.investor_count = store.investor_count - 1;  // Can go negative logically
    // Repeated zero-value ops corrupt investor tracking
}
```

### Secure Implementation
```move
// ✅ SECURE: Bounded rewards with cleanup
const MAX_REWARD_ENTRIES: u64 = 50;

public fun add_reward(user_rewards: &mut UserRewards, entry: RewardEntry) {
    assert!(vector::length(&user_rewards.rewards) < MAX_REWARD_ENTRIES, E_TOO_MANY_REWARDS);
    vector::push_back(&mut user_rewards.rewards, entry);
}

// ✅ Or use SmartTable with bounded iteration
public fun claim_rewards_paginated(user: &signer, pool: &mut Pool, start: u64, limit: u64) {
    let user_rewards = borrow_global_mut<UserRewards>(signer::address_of(user));
    let end = math::min(start + limit, vector::length(&user_rewards.rewards));
    let i = start;
    while (i < end) {
        process_reward(vector::borrow(&user_rewards.rewards, i));
        i = i + 1;
    };
}
```

---

## Pattern 2: Front-Running Resource/Account Creation — move-dos-002

**Frequency**: 4/29 reports (Echelon [R2], EthSign [R9], Magna [R10], Movedrop L2 [R13])
**Severity consensus**: HIGH
**Validation**: Strong — 4 independent protocols

### Attack Scenario
1. Protocol uses predictable address derivation (creator + seed) for resource accounts
2. Attacker observes creation transaction in mempool
3. Attacker front-runs by calling `aptos_account::create_account` or `create_resource_account` with the same address
4. Legitimate creation transaction aborts because account already exists
5. Protocol deployment permanently blocked

### Vulnerable Pattern Example

**Example 1: Echelon — Permissionless Primary Store Pre-Creation** [HIGH] [R2]
```move
// ❌ VULNERABLE: Anyone can create a primary store at any address
// Attacker creates primary store at package address before farm initialization
public fun initialize_farm(admin: &signer, token: TypeInfo) {
    let farm_addr = @echelon_farm;
    // ❌ If primary store already exists at farm_addr, this aborts
    primary_fungible_store::ensure_primary_store_exists(farm_addr, token);
    // Farm initialization permanently blocked
}
```

**Example 2: Magna — Predictable Vesting Address** [HIGH] [R10]
```move
// ❌ VULNERABLE: seed_id is predictable, address is derivable
public fun create_vesting(
    creator: &signer,
    seed_id: vector<u8>,
    beneficiary: address,
    amount: u64,
) {
    // ❌ Attacker can compute this address and pre-create account
    let (resource_signer, _) = account::create_resource_account(creator, seed_id);
    // Aborts if resource account already exists
    
    move_to(&resource_signer, VestingSchedule { beneficiary, amount, ... });
}
```

**Example 3: Echelon — Front-Running Pair Creation** [MEDIUM] [R2]
```move
// ❌ VULNERABLE: Deterministic pair address
public fun create_pair<X, Y>(admin: &signer) {
    let pair_addr = derive_pair_address<X, Y>();
    // ❌ Attacker front-runs with aptos_account::create_account(pair_addr)
    aptos_account::create_account(pair_addr);  // Aborts if exists
    // Pair creation permanently blocked for this token pair
}
```

### Secure Implementation
```move
// ✅ SECURE: Use unpredictable seeds or handle existing accounts
public fun create_vesting(
    creator: &signer,
    seed_id: vector<u8>,
    beneficiary: address,
    amount: u64,
) {
    // ✅ Add random nonce or creator-specific salt to make address unpredictable
    let full_seed = vector::empty();
    vector::append(&mut full_seed, seed_id);
    vector::append(&mut full_seed, bcs::to_bytes(&transaction_context::get_transaction_hash()));
    
    let (resource_signer, _) = account::create_resource_account(creator, full_seed);
    move_to(&resource_signer, VestingSchedule { beneficiary, amount, ... });
}

// ✅ Or gracefully handle pre-existing accounts
public fun initialize_farm(admin: &signer, token: TypeInfo) {
    let farm_addr = @echelon_farm;
    if (!primary_fungible_store::primary_store_exists(farm_addr, token)) {
        primary_fungible_store::create_primary_store(farm_addr, token);
    };
    // Continue initialization regardless
}
```

---

## Pattern 3: Event/Object Limit Exhaustion — move-dos-003

**Frequency**: 2/29 reports (Aftermath MM [R4], Mysten Walrus [R5])
**Severity consensus**: HIGH
**Validation**: Moderate — 2 independent protocols (Sui-specific)

### Vulnerable Pattern Example

**Example 1: Aftermath MM — Event Emission Limit Blocks Force Withdrawal** [HIGH] [R4]
```move
// ❌ VULNERABLE: Each order cancellation emits events
public fun force_withdraw(vault: &mut Vault, user: address) {
    // Cancel all pending orders for the user
    let i = 0;
    while (i < vector::length(&vault.pending_orders)) {
        let order = vector::borrow(&vault.pending_orders, i);
        if (order.user == user) {
            cancel_order(vault, i);  // ❌ Each cancel emits 1+ events
            // Sui limits: ~1024 events per transaction
        };
        i = i + 1;
    };
    // ❌ If user has 500+ small orders, force_withdraw exceeds event limit → aborts
}
```

**Example 2: Mysten Walrus — Object Size Limit via Long Public Key** [HIGH] [R5]
```move
// ❌ VULNERABLE: No length limit on public key stored in object
public fun register_node(pool: &mut StakingPool, public_key: vector<u8>) {
    // ❌ Excessively long public_key inflates object size
    pool.node_info.public_key = public_key;
    // Sui object size limit: ~256KB
    // If pool object exceeds limit, ALL operations on it fail
    // Staker withdrawals permanently blocked
}
```

### Secure Implementation
```move
// ✅ SECURE: Paginated event emission
public fun force_withdraw_batch(vault: &mut Vault, user: address, batch_size: u64) {
    let cancelled = 0;
    let i = 0;
    while (i < vector::length(&vault.pending_orders) && cancelled < batch_size) {
        let order = vector::borrow(&vault.pending_orders, i);
        if (order.user == user) {
            cancel_order(vault, i);
            cancelled = cancelled + 1;
        };
        i = i + 1;
    };
    // ✅ Multiple batched calls to stay under event limit
}

// ✅ SECURE: Validate public key length
public fun register_node(pool: &mut StakingPool, public_key: vector<u8>) {
    assert!(vector::length(&public_key) <= 128, E_KEY_TOO_LONG);
    pool.node_info.public_key = public_key;
}
```

---

## Pattern 4: Division by Zero in Pool/Epoch Operations — move-dos-004

**Frequency**: 3/29 reports (Solend Steamm [R3], Mysten Walrus [R5], Kofi Finance [R6])
**Severity consensus**: HIGH
**Validation**: Strong — 3 independent protocols

### Vulnerable Pattern Example

**Example 1: Solend Steamm — Empty Pool Reserve** [HIGH] [R3]
```move
// ❌ VULNERABLE: No guard against zero reserves
public fun calculate_exchange_rate(pool: &Pool): u128 {
    let total_supply = pool.total_supply;
    let total_reserves = pool.total_reserves;
    
    // ❌ If total_reserves drained to 0, division by zero → abort
    // All deposit operations permanently fail
    (total_supply as u128) * PRECISION / (total_reserves as u128)
}
```

**Example 2: Mysten Walrus — Zero Share Amount Blocks Epoch** [HIGH] [R5]
```move
// ❌ VULNERABLE: Share amount can be manipulated to zero
public fun convert_to_wal_amount(pool: &StakingPool, shares: u64): u64 {
    let total_shares = pool.total_shares;
    // ❌ If total_shares == 0, division by zero
    // Blocks epoch changes and ALL staker withdrawals
    shares * pool.total_wal / total_shares
}
```

**Example 3: Mysten Walrus — Zero Weight in Committee Selection** [HIGH] [R5]
```move
// ❌ VULNERABLE: Node weight can be zero
public fun calculate_shards(pool: &StakingPool, n_shards: u64): u64 {
    let weight = pool.total_staked;
    // ❌ If weight == 0 after withdrawals, division by zero
    (pool.node_capacity * n_shards) / weight
}
```

### Secure Implementation
```move
// ✅ SECURE: Guard all divisions against zero denominator
public fun calculate_exchange_rate(pool: &Pool): u128 {
    let total_reserves = pool.total_reserves;
    assert!(total_reserves > 0, E_POOL_EMPTY);
    (pool.total_supply as u128) * PRECISION / (total_reserves as u128)
}

// ✅ SECURE: Minimum stake that can never reach zero
public fun convert_to_wal_amount(pool: &StakingPool, shares: u64): u64 {
    let total_shares = pool.total_shares;
    if (total_shares == 0) return 0;
    shares * pool.total_wal / total_shares
}
```

---

## Pattern 5: Hash Collision DoS in Address-Keyed Tables — move-dos-005

**Frequency**: 1/29 reports (Aave Aptos V3 [R1])
**Severity consensus**: MEDIUM
**Validation**: Weak — single protocol

### Vulnerable Pattern Example

**Aave Aptos V3 — SmartTable Bucket Collision** [MEDIUM] [R1]
```move
// ❌ VULNERABLE: User-controlled address keys can collide
struct UserConfigs has key {
    configs: SmartTable<address, UserConfigurationMap>,
}

// SmartTable uses hash(address) for bucket assignment
// ~10K entries with same hash bucket → O(n) lookup
// New users whose address hashes to the congested bucket are permanently blocked
public fun get_user_config(configs: &UserConfigs, user: address): &UserConfigurationMap {
    // ❌ Linear scan within bucket — gas exhaustion for ~10K entries
    smart_table::borrow(&configs.configs, user)
}
```

### Secure Implementation
```move
// ✅ SECURE: Use Table (BTreeMap-based) instead of SmartTable for user-keyed data
struct UserConfigs has key {
    configs: Table<address, UserConfigurationMap>,
    // Table uses balanced tree — O(log n) guaranteed
}
```

---

## Pattern 6: Overflow Abort in Arithmetic Operations — move-dos-006

**Frequency**: 3/29 reports (EthSign [R9], Mysten Republic [R11], Kofi Finance [R6])
**Severity consensus**: HIGH
**Validation**: Strong — 3 independent protocols

### Vulnerable Pattern Example

**Example 1: EthSign — Fee Calculation Overflow** [HIGH] [R9]
```move
// ❌ VULNERABLE: Large amount * fee_bips can overflow u64
public fun calculate_fee(amount: u64, fee_bips: u64): u64 {
    // ❌ If amount > u64::MAX / fee_bips, this overflows → abort
    // Transaction panic for large distributions
    (amount * fee_bips) / BIPS_PRECISION
}
```

**Example 2: Mysten Republic — Dividend Calculation Overflow** [MEDIUM] [R11]
```move
// ❌ VULNERABLE: Multiplication exceeds u64 range
public fun calculate_available_dividends(
    total_dividends: u64,
    user_shares: u64,
    total_shares: u64,
): u64 {
    // ❌ total_dividends * user_shares can overflow u64
    (total_dividends * user_shares) / total_shares
}
```

**Example 3: Kofi Finance — Assertion Blocks Protocol** [HIGH] [R6]
```move
// ❌ VULNERABLE: Conversion ratio assertion is too strict
public fun check_conversion(pool: &Pool) {
    let ratio = pool.total_apt / pool.total_kapt;
    // ❌ Ratio naturally grows over time via rewards
    // When it exceeds MAX_RATIO, ALL staking/unstaking permanently blocked
    assert!(ratio <= MAX_RATIO, E_INVALID_RATIO);
}
```

### Secure Implementation
```move
// ✅ SECURE: Use u128 intermediate for overflow prevention
public fun calculate_fee(amount: u64, fee_bips: u64): u64 {
    ((amount as u128) * (fee_bips as u128) / (BIPS_PRECISION as u128) as u64)
}

// ✅ SECURE: Remove or relax natural growth assertions
public fun check_conversion(pool: &Pool) {
    // ✅ Only check for obviously invalid states, not growth limits
    assert!(pool.total_kapt > 0, E_ZERO_SUPPLY);
}
```

---

## Pattern 7: Mint/Rate Limit Exhaustion — move-dos-007

**Frequency**: 1/29 reports (Lombard Sui [R8])
**Severity consensus**: HIGH
**Validation**: Weak — single protocol

### Vulnerable Pattern Example

**Lombard Sui — Epoch Mint Limit via Wrap/Unwrap** [HIGH] [R8]
```move
// ❌ VULNERABLE: Wrap/unwrap count toward epoch limit
public fun wrap(treasury: &mut Treasury, amount: u64, ctx: &mut TxContext) {
    update_epoch_limit(treasury, ctx);
    // ❌ Each wrap consumes from epoch mint limit
    assert!(treasury.minted_this_epoch + amount <= treasury.epoch_limit, E_LIMIT_REACHED);
    treasury.minted_this_epoch = treasury.minted_this_epoch + amount;
    // ...
}

// Attacker wraps/unwraps in loop to exhaust epoch limit
// Legitimate users cannot mint for remainder of epoch
```

### Secure Implementation
```move
// ✅ SECURE: Per-user rate limiting or separate internal/external limits
public fun wrap(treasury: &mut Treasury, amount: u64, ctx: &mut TxContext) {
    update_epoch_limit(treasury, ctx);
    let user = tx_context::sender(ctx);
    let user_minted = table::borrow_mut_with_default(&mut treasury.user_mints, user, 0);
    assert!(*user_minted + amount <= PER_USER_LIMIT, E_USER_LIMIT);
    *user_minted = *user_minted + amount;
    treasury.minted_this_epoch = treasury.minted_this_epoch + amount;
    assert!(treasury.minted_this_epoch <= treasury.epoch_limit, E_EPOCH_LIMIT);
}
```

---

## Pattern 8: Missing Parameter Validation Causing Protocol Halt — move-dos-008

**Frequency**: 2/29 reports (Mysten Walrus [R5], Echelon [R2])
**Severity consensus**: HIGH
**Validation**: Moderate — 2 independent protocols

### Vulnerable Pattern Example

**Example 1: Mysten Walrus — Unchecked Commission Rate** [HIGH] [R5]
```move
// ❌ VULNERABLE: Commission rate not bounded
public fun set_commission_rate(pool: &mut StakingPool, rate: u64) {
    // ❌ No check that rate <= 10000 (100%)
    pool.commission_rate = rate;
    // Invalid rate > 10000 causes underflow in reward distribution
    // Blocks epoch changes for ENTIRE committee
}
```

**Example 2: Mysten Walrus — Large Capacity Causes Overflow** [HIGH] [R5]
```move
// ❌ VULNERABLE: Node capacity not bounded
public fun set_node_capacity(pool: &mut StakingPool, capacity: u64) {
    // ❌ Excessively large capacity overflows multiplication
    pool.node_capacity = capacity;
    // capacity * n_shards overflows u64 → epoch advancement fails
}
```

### Secure Implementation
```move
// ✅ SECURE: Validate all parameters at entry
public fun set_commission_rate(pool: &mut StakingPool, rate: u64) {
    assert!(rate <= 10000, E_INVALID_COMMISSION);
    pool.commission_rate = rate;
}

public fun set_node_capacity(pool: &mut StakingPool, capacity: u64) {
    assert!(capacity <= MAX_NODE_CAPACITY, E_CAPACITY_TOO_LARGE);
    pool.node_capacity = capacity;
}
```

---

### Impact Analysis

#### Technical Impact
- Permanent liquidation blocking causing bad debt (Aave Aptos V3) — CRITICAL
- Protocol deployment permanently blocked (Echelon, EthSign, Magna, Movedrop)
- Epoch advancement halted for validator networks (Mysten Walrus)
- Transaction panics on overflow (EthSign, Republic, Kofi)
- Fund lockup via DoS on withdrawal paths

#### Business Impact
- Protocol insolvency from unliquidatable positions
- Loss of user confidence from blocked operations
- Competitor can permanently grief protocol launch
- Validator network halts affecting all stakers

#### Affected Scenarios
- Lending protocols with per-user reward tracking (Aave, Echelon)
- Protocols with deterministic resource account creation (EthSign, Magna, Movedrop)
- AMM/DEX with event-heavy operations (Aftermath)
- Staking/validator networks (Mysten Walrus)
- Bridge protocols with epoch-based limits (Lombard)

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: `while (i < vector::length(...))` in functions called by liquidate/withdraw
- Pattern 2: `account::create_resource_account(creator, seed)` with predictable seed
- Pattern 3: `event::emit` inside loops without bound
- Pattern 4: Division without `assert!(denominator > 0)` guard
- Pattern 5: `(a * b) / c` without u128 cast for intermediate
- Pattern 6: `assert!(ratio <= MAX)` on naturally growing values
- Pattern 7: `primary_fungible_store::ensure_primary_store_exists` on attacker-reachable address
```

#### Audit Checklist
- [ ] All vector iterations have bounded gas cost or pagination
- [ ] Resource account seeds include unpredictable components
- [ ] Event emission in loops bounded by constant or batch size
- [ ] All division operations guarded against zero denominator
- [ ] Multiplication operations use u128 intermediate to prevent overflow
- [ ] Assertions don't block operations on naturally evolving metrics
- [ ] Primary store creation handles pre-existing stores gracefully
- [ ] Node/validator parameters (capacity, commission, key length) bounded

### Keywords for Search

> `denial of service`, `DoS`, `gas exhaustion`, `unbounded vector`, `linear scan`, `front-running creation`, `create_resource_account`, `predictable seed`, `event limit`, `object size limit`, `division by zero`, `overflow abort`, `u64 overflow`, `hash collision`, `SmartTable`, `epoch limit`, `mint limit`, `commission rate`, `node capacity`, `primary store`, `front-running`, `griefing`, `protocol halt`, `move dos`, `sui dos`, `aptos dos`

### Related Vulnerabilities

- [MOVE_ARITHMETIC_PRECISION_VULNERABILITIES.md](MOVE_ARITHMETIC_PRECISION_VULNERABILITIES.md) — Overflow/underflow patterns
- [MOVE_DEFI_PROTOCOL_LOGIC_VULNERABILITIES.md](MOVE_DEFI_PROTOCOL_LOGIC_VULNERABILITIES.md) — Withdrawal abort patterns
- [MOVE_ACCESS_CONTROL_AUTHORIZATION_VULNERABILITIES.md](MOVE_ACCESS_CONTROL_AUTHORIZATION_VULNERABILITIES.md) — Version check bypass

---
protocol: generic
chain: sui, aptos, movement
category: event_configuration
vulnerability_type: event_emission, configuration_error, initialization_flaw, upgrade_safety, reentrancy, cooldown_bypass
attack_type: logical_error, configuration_manipulation, event_abuse, upgrade_attack
affected_component: events, configuration, initialization, upgrades, module_safety
primitives:
  - event_emit
  - module_init
  - package_upgrade
  - capability_pattern
  - cooldown
  - reentrancy_guard
severity: medium
impact: monitoring_failure, configuration_corruption, operational_disruption, fund_loss
exploitability: 0.5
financial_impact: medium
tags:
  - move
  - sui
  - aptos
  - events
  - configuration
  - initialization
  - upgrade
  - reentrancy
  - cooldown
  - monitoring
  - emit
  - parameter_validation
language: move
version: all
---

## References

| Tag | Report | Protocol | Auditor |
|-----|--------|----------|---------|
| [R1] | reports/ottersec_move_audits/markdown/Securitize_Aptos_Token_Issuance.md | Securitize | OtterSec |
| [R2] | reports/ottersec_move_audits/markdown/Echelon_Market.md | Echelon | OtterSec |
| [R3] | reports/ottersec_move_audits/markdown/KoFi_Finance.md | Kofi Finance | OtterSec |
| [R4] | reports/ottersec_move_audits/markdown/Canopy_Money.md | Canopy | OtterSec |
| [R5] | reports/ottersec_move_audits/markdown/Magna_Aptos.md | Magna | OtterSec |
| [R6] | reports/ottersec_move_audits/markdown/Aave_Aptos_V3.md | Aave Aptos V3 | OtterSec |
| [R7] | reports/ottersec_move_audits/markdown/Aftermath_Finance_Market_Maker.md | Aftermath AMM | OtterSec |
| [R8] | reports/ottersec_move_audits/markdown/Aftermath_Perpetuals.md | Aftermath Perps | OtterSec |
| [R9] | reports/ottersec_move_audits/markdown/Republic_Aptos.md | Republic | OtterSec |
| [R10] | reports/ottersec_move_audits/markdown/Solend_on_Sui.md | Solend on Sui | OtterSec |
| [R11] | reports/ottersec_move_audits/markdown/Bluefin_Spot.md | Bluefin Spot | OtterSec |
| [R12] | reports/ottersec_move_audits/markdown/EthSign_Movedrop.md | EthSign | OtterSec |
| [R13] | reports/ottersec_move_audits/markdown/Emojicoin.md | Emojicoin | OtterSec |
| [R14] | reports/ottersec_move_audits/markdown/lombard_sui.md | Lombard SUI | OtterSec |
| [R15] | reports/ottersec_move_audits/markdown/Mysten_Walrus.md | Mysten Walrus | OtterSec |

## Move Event Emission, Configuration & Upgrade Safety Vulnerabilities

### Overview

Event, configuration, and upgrade safety bugs in Move are distinct from logic errors — they affect observability, parameter integrity, and upgrade correctness. Missing or incorrect events break off-chain monitoring; misconfigured parameters create exploitable protocol states; and unsafe upgrades or initializations can permanently corrupt the system. These patterns span 15/29 OtterSec audit reports.

---

## Pattern 1: Missing Events for Critical State Changes — move-evtcfg-001

**Severity**: MEDIUM  
**ID**: move-evtcfg-001  
**References**: Canopy (OS-CMP-ADV-05), Echelon (OS-ECH-ADV-07), Kofi (OS-KOF-ADV-10)

### Attack Scenario
Critical state-modifying functions (admin parameter changes, collateral factor updates, fee adjustments) don't emit events. Off-chain monitoring, dashboards, and governance watchers have no visibility into when changes occur. An attacker or compromised admin can make silent changes that go undetected until funds are lost.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: No event on critical admin change
public fun set_liquidation_bonus(admin: &signer, market: &mut Market, bonus: u64) {
    assert!(signer::address_of(admin) == market.admin, E_UNAUTHORIZED);
    // ❌ No event — off-chain systems never see this change
    market.liquidation_bonus = bonus;
}

public fun update_interest_model(admin: &signer, pool: &mut Pool, model: InterestModel) {
    assert!(signer::address_of(admin) == pool.admin, E_UNAUTHORIZED);
    // ❌ Critical financial parameter changed silently
    pool.interest_model = model;
}
```

### Secure Implementation
```move
// ✅ SECURE: Emit event for every critical change
struct LiquidationBonusChanged has copy, drop {
    market_id: u64,
    old_bonus: u64,
    new_bonus: u64,
    admin: address,
    timestamp: u64,
}

public fun set_liquidation_bonus(admin: &signer, market: &mut Market, bonus: u64, clock: &Clock) {
    assert!(signer::address_of(admin) == market.admin, E_UNAUTHORIZED);
    let old_bonus = market.liquidation_bonus;
    market.liquidation_bonus = bonus;
    event::emit(LiquidationBonusChanged {
        market_id: market.id,
        old_bonus,
        new_bonus: bonus,
        admin: signer::address_of(admin),
        timestamp: clock::timestamp_ms(clock),
    });
}
```

---

## Pattern 2: Misleading Event Type in Emissions — move-evtcfg-002

**Severity**: LOW  
**ID**: move-evtcfg-002  
**References**: Aftermath AMM (OS-AMM-ADV-04)

### Attack Scenario
An event struct uses a wrong or misleading type for one of its fields (e.g., emitting a pool ID where a user address should be, or using the wrong coin type). Off-chain indexers parsing events build incorrect state, leading to wrong dashboards, missed alerts, or incorrect analytics that inform bad governance decisions.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Event uses wrong type for a field
struct SwapEvent has copy, drop {
    pool_id: u64,
    user: address,
    amount_in: u64,
    amount_out: u64,
    coin_type: u8,  // ❌ Should be TypeName or string, not u8
}

public fun swap(pool: &mut Pool, ...) {
    // ... swap logic ...
    event::emit(SwapEvent {
        pool_id: pool.id,
        user: sender,
        amount_in,
        amount_out,
        coin_type: 1,  // ❌ Magic number — indexers can't resolve actual coin type
    });
}
```

### Secure Implementation
```move
// ✅ SECURE: Event uses proper types
struct SwapEvent has copy, drop {
    pool_id: u64,
    user: address,
    amount_in: u64,
    amount_out: u64,
    coin_in_type: TypeName,
    coin_out_type: TypeName,
}
```

---

## Pattern 3: Event Emission on No-Op State Change — move-evtcfg-003

**Severity**: LOW  
**ID**: move-evtcfg-003  
**References**: Echelon (OS-ECH-ADV-08)

### Attack Scenario
Events are emitted even when the underlying state doesn't actually change (e.g., setting a value to its current value, or a zero-amount transfer). Indexers and monitoring systems process these no-op events as real state changes, clouding analytics, triggering false alerts, and wasting storage on the indexer side.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Event emitted even when value unchanged
public fun set_reserve_factor(admin: &signer, pool: &mut Pool, factor: u64) {
    assert!(signer::address_of(admin) == pool.admin, E_UNAUTHORIZED);
    pool.reserve_factor = factor;
    // ❌ Emits even if old_factor == factor (no actual change)
    event::emit(ReserveFactorChanged { pool_id: pool.id, new_factor: factor });
}
```

### Secure Implementation
```move
// ✅ SECURE: Only emit on actual state change
public fun set_reserve_factor(admin: &signer, pool: &mut Pool, factor: u64) {
    assert!(signer::address_of(admin) == pool.admin, E_UNAUTHORIZED);
    if (pool.reserve_factor == factor) return;  // ✅ No-op check
    let old_factor = pool.reserve_factor;
    pool.reserve_factor = factor;
    event::emit(ReserveFactorChanged { pool_id: pool.id, old_factor, new_factor: factor });
}
```

---

## Pattern 4: Fee Annotation Mismatch with Actual Calculation — move-evtcfg-004

**Severity**: MEDIUM  
**ID**: move-evtcfg-004  
**References**: Aftermath AMM (OS-AMM-ADV-02)

### Attack Scenario
The protocol advertises fees as basis points (e.g., "30 bps = 0.30%") but the actual calculation uses a different denominator or formula. Users and integrators assume the documented fee rate, but the effective rate is different. If the actual fee is lower than advertised, the protocol loses revenue; if higher, users are overcharged.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Fee labeled as bps but calculated differently
const FEE_BPS: u64 = 30;  // Documented as 0.30%
const FEE_PRECISION: u64 = 100_000;  // ❌ Not 10_000 (bps standard)

public fun calculate_fee(amount: u64): u64 {
    // Actual fee: 30 / 100000 = 0.03%, NOT 0.30%
    (amount * FEE_BPS) / FEE_PRECISION  // ❌ 10x less than documented
}
```

### Secure Implementation
```move
// ✅ SECURE: Fee precision matches annotation
const FEE_BPS: u64 = 30;
const BPS_PRECISION: u64 = 10_000;  // ✅ Standard basis points

public fun calculate_fee(amount: u64): u64 {
    (amount * FEE_BPS) / BPS_PRECISION  // 30/10000 = 0.30% as documented
}
```

---

## Pattern 5: Liquidation Bonus Configuration Exceeding Bounds — move-evtcfg-005

**Severity**: HIGH  
**ID**: move-evtcfg-005  
**References**: Aave Aptos V3 (OS-AAV-ADV-06)

### Attack Scenario
The admin sets a liquidation bonus that exceeds the collateral factor. With bonus > 100%, liquidators receive more collateral than the debt they repay. Malicious liquidators can repeatedly trigger liquidations on slightly undercollateralized positions to extract more value than the debt, draining the protocol's reserves.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: No upper bound on liquidation bonus
public fun set_liquidation_params(
    admin: &signer,
    market: &mut Market,
    bonus_bps: u64,
    threshold_bps: u64
) {
    assert!(signer::address_of(admin) == market.admin, E_UNAUTHORIZED);
    // ❌ No check: bonus_bps could be > 10000 (>100%)
    market.liquidation_bonus = bonus_bps;
    market.liquidation_threshold = threshold_bps;
}
```

### Secure Implementation
```move
// ✅ SECURE: Validate bonus + threshold don't exceed 100%
public fun set_liquidation_params(
    admin: &signer,
    market: &mut Market,
    bonus_bps: u64,
    threshold_bps: u64
) {
    assert!(signer::address_of(admin) == market.admin, E_UNAUTHORIZED);
    assert!(bonus_bps <= MAX_BONUS_BPS, E_BONUS_TOO_HIGH);
    assert!(threshold_bps + bonus_bps <= 10000, E_PARAMS_EXCEED_100PCT);
    market.liquidation_bonus = bonus_bps;
    market.liquidation_threshold = threshold_bps;
}
```

---

## Pattern 6: Cooldown Bypass via Timestamp Manipulation — move-evtcfg-006

**Severity**: MEDIUM  
**ID**: move-evtcfg-006  
**References**: Kofi Finance (OS-KOF-ADV-04)

### Attack Scenario
A cooldown mechanism uses timestamps from the transaction context (which on some chains may be slightly manipulable by validators). The user triggers an action, then immediately (in the same block or next block) triggers the next action, bypassing the intended waiting period because the timestamp check has insufficient granularity.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Cooldown checked with >= instead of >
public fun unstake(state: &mut StakeState, user: address, clock: &Clock) {
    let last_stake_time = state.last_stake_time;
    let current_time = clock::timestamp_ms(clock);
    // ❌ If COOLDOWN_PERIOD == 0 or same block, this passes
    assert!(current_time >= last_stake_time + COOLDOWN_PERIOD, E_COOLDOWN);
    // ... unstake
}
```

### Secure Implementation
```move
// ✅ SECURE: Strict inequality and minimum period
const MIN_COOLDOWN_MS: u64 = 60_000;  // 1 minute minimum

public fun unstake(state: &mut StakeState, user: address, clock: &Clock) {
    let last_stake_time = state.last_stake_time;
    let current_time = clock::timestamp_ms(clock);
    let effective_cooldown = math::max(state.cooldown_period, MIN_COOLDOWN_MS);
    assert!(current_time > last_stake_time + effective_cooldown, E_COOLDOWN);
}
```

---

## Pattern 7: Missing Approval Revocation Function — move-evtcfg-007

**Severity**: MEDIUM  
**ID**: move-evtcfg-007  
**References**: Securitize (OS-ASC-ADV-07)

### Attack Scenario
A protocol allows granting approval/delegation to operators (e.g., transfer agents) but provides no function to revoke it. Once granted, the approval is permanent. If an operator is compromised or their role changes, the asset owner cannot remove their authorization, leaving funds permanently exposed.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Approval set but no revoke function exists
public fun approve_operator(owner: &signer, operator: address) {
    let state = borrow_global_mut<Approvals>(signer::address_of(owner));
    table::upsert(&mut state.approved_operators, operator, true);
}

// ❌ No revoke_operator function exists
// Operator permanently authorized
```

### Secure Implementation
```move
// ✅ SECURE: Both approve and revoke available
public fun approve_operator(owner: &signer, operator: address) {
    let state = borrow_global_mut<Approvals>(signer::address_of(owner));
    table::upsert(&mut state.approved_operators, operator, true);
    event::emit(OperatorApproved { owner: signer::address_of(owner), operator });
}

public fun revoke_operator(owner: &signer, operator: address) {
    let state = borrow_global_mut<Approvals>(signer::address_of(owner));
    assert!(table::contains(&state.approved_operators, operator), E_NOT_APPROVED);
    table::remove(&mut state.approved_operators, operator);
    event::emit(OperatorRevoked { owner: signer::address_of(owner), operator });
}
```

---

## Pattern 8: Dispatchable Token Store Missing withdraw/deposit Implementation — move-evtcfg-008

**Severity**: HIGH  
**ID**: move-evtcfg-008  
**References**: Securitize (OS-ASC-ADV-02)

### Attack Scenario
A dispatchable fungible asset (Aptos) overrides `withdraw` and `deposit` for compliance checks (e.g., KYC, blacklist). However, the overriding functions are defined but not actually registered as dispatch hooks, so the framework calls the default implementations that skip compliance checks. Anyone can transfer restricted tokens freely.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Custom functions defined but not registered as dispatch hooks
public fun custom_withdraw(store: Object<FungibleStore>, amount: u64): FungibleAsset {
    // Compliance checks here
    assert!(is_whitelisted(store_owner(store)), E_NOT_WHITELISTED);
    fungible_asset::withdraw(store, amount)
}

// ❌ NOT registered: fungible_asset framework still calls default withdraw
// Users bypass whitelist by calling standard fungible_asset::withdraw directly
```

### Secure Implementation
```move
// ✅ SECURE: Register dispatch hooks during initialization
public fun initialize(admin: &signer) {
    let constructor_ref = object::create_named_object(admin, b"token");
    primary_fungible_store::create_primary_store_enabled_fungible_asset(
        &constructor_ref, /* ... */
    );
    // ✅ Register custom dispatch functions
    fungible_asset::register_dispatch_functions(
        &constructor_ref,
        option::some(custom_withdraw),   // ✅ Override withdraw
        option::some(custom_deposit),    // ✅ Override deposit
        option::none(),                  // No derived balance override
    );
}
```

---

## Pattern 9: Version Check Missing in Upgrade-Sensitive Functions — move-evtcfg-009

**Severity**: HIGH  
**ID**: move-evtcfg-009  
**References**: Lombard SUI (OS-LSI-ADV-00), Mysten Walrus (OS-MSW-ADV-00)

### Attack Scenario
After a package upgrade on Sui, shared objects created by the old version can still be accessed by new code. If the new code assumes a different storage layout (added fields, changed types), operations on old-version objects produce corrupted state. Functions must check the object's version and migrate it before proceeding.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: No version check on shared object access
public fun deposit(state: &mut ProtocolState, amount: u64) {
    // ❌ `state` might be from version 1, but code expects version 2 fields
    state.total_deposits = state.total_deposits + amount;
    // ❌ Accessing state.new_field_v2 on a v1 object → undefined behavior
}
```

### Secure Implementation
```move
// ✅ SECURE: Version gate with migration
const CURRENT_VERSION: u64 = 2;

public fun deposit(state: &mut ProtocolState, amount: u64) {
    assert!(state.version == CURRENT_VERSION, E_VERSION_MISMATCH);
    state.total_deposits = state.total_deposits + amount;
}

public fun migrate(state: &mut ProtocolState, admin: &signer) {
    assert!(state.version == CURRENT_VERSION - 1, E_ALREADY_MIGRATED);
    // Perform migration steps
    state.version = CURRENT_VERSION;
}
```

---

## Pattern 10: Two-Step Ownership Transfer Missing — move-evtcfg-010

**Severity**: MEDIUM  
**ID**: move-evtcfg-010  
**References**: Republic (OS-REP-ADV-03), Canopy (OS-CMP-ADV-04)

### Attack Scenario
Admin/owner transfer is a single-step operation: the current owner specifies the new owner address, and ownership transfers immediately. If the owner supplies an incorrect address (typo, wrong chain format), ownership is irrevocably transferred to an inaccessible address, bricking the protocol.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Single-step ownership transfer
public fun transfer_ownership(owner: &signer, new_owner: address) {
    let state = borrow_global_mut<AdminState>(@protocol);
    assert!(signer::address_of(owner) == state.admin, E_UNAUTHORIZED);
    // ❌ Immediate transfer — if new_owner is wrong, game over
    state.admin = new_owner;
}
```

### Secure Implementation
```move
// ✅ SECURE: Two-step transfer with acceptance
public fun propose_ownership(owner: &signer, new_owner: address) {
    let state = borrow_global_mut<AdminState>(@protocol);
    assert!(signer::address_of(owner) == state.admin, E_UNAUTHORIZED);
    state.pending_admin = option::some(new_owner);
}

public fun accept_ownership(new_owner: &signer) {
    let state = borrow_global_mut<AdminState>(@protocol);
    let pending = option::extract(&mut state.pending_admin);
    assert!(signer::address_of(new_owner) == pending, E_NOT_PENDING);
    state.admin = pending;
    state.pending_admin = option::none();
}
```

---

## Pattern 11: Reentrancy via External Module Callback — move-evtcfg-011

**Severity**: HIGH  
**ID**: move-evtcfg-011  
**References**: Aftermath AMM (OS-AMM-ADV-01), Bluefin Spot (OS-BFS-ADV-04)

### Attack Scenario
Move's type system prevents classic reentrancy, but external module callbacks (e.g., flash loans, custom coin hooks, dispatchable functions) can re-enter protocol functions. If state is updated after the external call, the reentering call sees stale state and can extract value. This is the Move equivalent of the checks-effects-interactions pattern violation.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: State updated after external callback
public fun flash_loan(pool: &mut Pool, amount: u64, ctx: &mut TxContext) {
    let loan = balance::split(&mut pool.reserve, amount);
    let loan_coin = coin::from_balance(loan, ctx);
    
    // ❌ External callback — borrower can call back into pool
    transfer::public_transfer(loan_coin, tx_context::sender(ctx));
    
    // ❌ State update AFTER external interaction
    pool.total_borrows = pool.total_borrows + amount;
}
```

### Secure Implementation
```move
// ✅ SECURE: Update state before external interaction
public fun flash_loan(pool: &mut Pool, amount: u64, ctx: &mut TxContext) {
    // ✅ Effects first
    pool.total_borrows = pool.total_borrows + amount;
    pool.flash_loan_active = true;
    
    let loan = balance::split(&mut pool.reserve, amount);
    let loan_coin = coin::from_balance(loan, ctx);
    transfer::public_transfer(loan_coin, tx_context::sender(ctx));
}
```

---

## Pattern 12: Hardcoded Batch Parameters in Event Emission — move-evtcfg-012

**Severity**: LOW  
**ID**: move-evtcfg-012  
**References**: Emojicoin (OS-EMJ-ADV-00)

### Attack Scenario
Batch event emission uses hardcoded limits (e.g., max 50 items per event) that may not match the protocol's actual batch sizes. If a batch exceeds the hardcoded limit, events are silently truncated or split across multiple emissions, causing off-chain systems to miss entries or double-count from split events.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Hardcoded event batch limit
const MAX_EVENT_BATCH: u64 = 50;

public fun process_batch(items: &vector<Item>) {
    let i = 0;
    let batch = vector::empty<ItemEvent>();
    while (i < vector::length(items)) {
        if (vector::length(&batch) >= MAX_EVENT_BATCH) {
            event::emit(BatchProcessed { items: batch });
            batch = vector::empty<ItemEvent>();  // ❌ No continuation marker
        };
        vector::push_back(&mut batch, to_event(vector::borrow(items, i)));
        i = i + 1;
    };
    if (!vector::is_empty(&batch)) {
        event::emit(BatchProcessed { items: batch });
    };
}
```

### Secure Implementation
```move
// ✅ SECURE: Include batch index and total for off-chain reconciliation
public fun process_batch(items: &vector<Item>) {
    let total = vector::length(items);
    let i = 0;
    let batch_index = 0u64;
    let batch = vector::empty<ItemEvent>();
    while (i < total) {
        if (vector::length(&batch) >= MAX_EVENT_BATCH) {
            event::emit(BatchProcessed {
                items: batch,
                batch_index,
                total_items: total,
                is_last: false,
            });
            batch = vector::empty<ItemEvent>();
            batch_index = batch_index + 1;
        };
        vector::push_back(&mut batch, to_event(vector::borrow(items, i)));
        i = i + 1;
    };
    event::emit(BatchProcessed {
        items: batch,
        batch_index,
        total_items: total,
        is_last: true,
    });
}
```

---

## Pattern 13: Assertion Inconsistency Between Getter and Setter — move-evtcfg-013

**Severity**: MEDIUM  
**ID**: move-evtcfg-013  
**References**: Kofi Finance (OS-KOF-ADV-06)

### Attack Scenario
A configuration setter allows a certain range of values (e.g., `fee <= 10000`), but a getter or consumer function asserts a stricter range (e.g., `fee < 10000`). The boundary value (10000) passes the setter but causes the getter to abort, bricking any function that reads the configuration. Conversely, a loose getter with a strict setter may allow unexpected values through.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Setter allows 10000 but getter rejects it
public fun set_fee_rate(admin: &signer, state: &mut State, rate: u64) {
    assert!(rate <= 10000, E_INVALID_RATE);  // Allows 10000
    state.fee_rate = rate;
}

public fun get_fee_amount(state: &State, amount: u64): u64 {
    assert!(state.fee_rate < 10000, E_INVALID_RATE);  // ❌ Rejects 10000
    (amount * state.fee_rate) / 10000
}
```

### Secure Implementation
```move
// ✅ SECURE: Consistent bounds across setter and getter
const MAX_FEE_RATE: u64 = 10000;

public fun set_fee_rate(admin: &signer, state: &mut State, rate: u64) {
    assert!(rate <= MAX_FEE_RATE, E_INVALID_RATE);
    state.fee_rate = rate;
}

public fun get_fee_amount(state: &State, amount: u64): u64 {
    // ✅ Uses same constant — always consistent
    (amount * state.fee_rate) / MAX_FEE_RATE
}
```

---

## Pattern 14: Inability to Withdraw Collected Fees — move-evtcfg-014

**Severity**: HIGH  
**ID**: move-evtcfg-014  
**References**: Aftermath AMM (OS-AMM-ADV-08)

### Attack Scenario
The protocol collects fees into an internal balance or object, but no external function exists to withdraw those fees. The fees are permanently locked inside the protocol object, representing a direct loss for the protocol team/DAO and reducing incentives for liquidity providers if fees were supposed to be distributed.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Fees collected but no withdrawal path
struct Pool has key {
    id: UID,
    reserves: Balance<COIN>,
    collected_fees: Balance<COIN>,  // ❌ No function to withdraw this
}

public fun swap(pool: &mut Pool, input: Coin<COIN>): Coin<COIN> {
    let fee = calculate_fee(coin::value(&input));
    let fee_balance = balance::split(coin::balance_mut(&mut input), fee);
    balance::join(&mut pool.collected_fees, fee_balance);  // Fees accumulate
    // ... swap logic
    // ❌ No `withdraw_fees` or `claim_fees` function exists
}
```

### Secure Implementation
```move
// ✅ SECURE: Fee withdrawal function for authorized parties
public fun withdraw_fees(pool: &mut Pool, admin_cap: &AdminCap, ctx: &mut TxContext): Coin<COIN> {
    let fee_amount = balance::value(&pool.collected_fees);
    assert!(fee_amount > 0, E_NO_FEES);
    let fees = balance::withdraw_all(&mut pool.collected_fees);
    event::emit(FeesWithdrawn { pool_id: object::uid_to_inner(&pool.id), amount: fee_amount });
    coin::from_balance(fees, ctx)
}
```

---

## Pattern 15: Front-Running Public Validation for Initialization — move-evtcfg-015

**Severity**: HIGH  
**ID**: move-evtcfg-015  
**References**: EthSign (OS-SIG-ADV-03), Emojicoin (OS-EMJ-ADV-01)

### Attack Scenario
Protocol initialization requires a validation step (e.g., verifying the deployer address, validating initial parameters) that is exposed as a separate public function. An attacker can front-run the legitimate deployer by calling the validation function first with malicious parameters, either preventing legitimate initialization or corrupting the initial state.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Public validation can be front-run
public fun validate_deployment(deployer: address, params: vector<u8>): bool {
    // ❌ Anyone can call this — not restricted to init flow
    let valid = verify_params(params);
    if (valid) {
        store_validated_params(@protocol, params);  // ❌ Writes state
    };
    valid
}

public fun initialize(admin: &signer) {
    // Expects validate_deployment was called by admin
    let params = load_validated_params(@protocol);  // ❌ May load attacker's params
    setup_protocol(admin, params);
}
```

### Secure Implementation
```move
// ✅ SECURE: Validation and initialization are atomic
public fun initialize(admin: &signer, params: vector<u8>) {
    assert!(signer::address_of(admin) == @deployer, E_UNAUTHORIZED);
    assert!(verify_params(params), E_INVALID_PARAMS);
    setup_protocol(admin, params);  // ✅ Atomic — no front-running window
}
```

---

### Impact Analysis

#### Technical Impact
- Off-chain monitoring blind spots from missing events (3/29 reports) — MEDIUM
- Protocol bricked from incorrect admin transfer (2/29 reports) — HIGH
- Compliance bypass via unregistered dispatch hooks (1/29 reports) — HIGH
- Protocol fees permanently locked (1/29 reports) — HIGH
- Reentrancy via flash loan callbacks (2/29 reports) — HIGH

#### Business Impact
- Governance unable to detect admin changes in real-time
- Protocol team loses accumulated fee revenue permanently
- Regulatory compliance broken by dispatch hook misconfiguration
- User trust damaged by silent parameter changes
- Protocol team locked out by single-step ownership error

#### Affected Scenarios
- Lending protocols with admin-managed parameters (Aave, Echelon)
- AMMs with fee collection and flash loans (Aftermath, Bluefin)
- Compliance-focused token platforms (Securitize)
- Staking protocols with cooldown periods (Kofi)
- Cross-chain bridges with versioned upgrades (Lombard, Walrus)

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: `borrow_global_mut` → mutation → no `event::emit` in same function
- Pattern 2: `coin_type: u8` (magic number) in event structs instead of TypeName
- Pattern 3: `event::emit` without prior change-detection check
- Pattern 4: `FEE_PRECISION` != 10_000 when fee is labeled "bps"
- Pattern 5: `liquidation_bonus` set without bound against collateral_factor
- Pattern 6: `current_time >=` instead of `current_time >` in cooldown
- Pattern 7: `approve_operator` exists but no `revoke_operator`
- Pattern 8: `fungible_asset::register_dispatch_functions` call missing
- Pattern 9: Shared object accessed without `assert!(state.version == CURRENT_VERSION)`
- Pattern 10: `state.admin = new_owner` without pending/accept pattern
- Pattern 11: `transfer::public_transfer` before state update in flash loan
- Pattern 12: `event::emit(BatchProcessed { items })` without batch_index
- Pattern 13: Setter allows `<= X` but consumer asserts `< X`
- Pattern 14: `balance::join(&pool.collected_fees, ...)` with no withdraw function
- Pattern 15: Public validation function separate from initialization
```

#### Audit Checklist
- [ ] All admin parameter changes emit events with old + new values
- [ ] Event field types match semantic meaning (TypeName for coins, address for users)
- [ ] Events only emitted on actual state changes (skip no-ops)
- [ ] Fee precision constants match documented units (bps = 10000)
- [ ] Liquidation bonus + threshold ≤ 100%
- [ ] Cooldown uses strict inequality with minimum period
- [ ] Every approve/grant function has corresponding revoke/remove
- [ ] Dispatch function hooks registered during initialization
- [ ] All shared object access version-gated with migration path
- [ ] Ownership transfer uses two-step (propose + accept) pattern
- [ ] State updated before external calls (CEI pattern)
- [ ] Batch events include index, total, and is_last flag
- [ ] Setter and getter assertions use identical bounds
- [ ] All fee collection paths have corresponding withdrawal functions
- [ ] Initialization and validation are atomic (no front-running window)

### Keywords for Search

> `event emission`, `missing event`, `emit`, `event::emit`, `configuration`, `parameter validation`, `liquidation bonus`, `collateral factor`, `cooldown`, `timestamp`, `approval`, `revoke`, `operator`, `dispatch`, `dispatchable`, `fungible_asset`, `register_dispatch_functions`, `version check`, `package upgrade`, `migration`, `two-step transfer`, `ownership`, `pending_admin`, `reentrancy`, `flash loan`, `callback`, `checks effects interactions`, `batch event`, `fee precision`, `basis points`, `bps`, `assertion inconsistency`, `getter setter`, `fee withdrawal`, `locked fees`, `front-running initialization`, `validate_deployment`, `move event`, `sui event`, `aptos event`, `move config`, `sui config`, `aptos config`

### Related Vulnerabilities

- [MOVE_STATE_MANAGEMENT_VULNERABILITIES.md](MOVE_STATE_MANAGEMENT_VULNERABILITIES.md) — State tracking issues that events should detect
- [MOVE_ACCESS_CONTROL_AUTHORIZATION_VULNERABILITIES.md](MOVE_ACCESS_CONTROL_AUTHORIZATION_VULNERABILITIES.md) — Authorization-related config
- [MOVE_DENIAL_OF_SERVICE_VULNERABILITIES.md](MOVE_DENIAL_OF_SERVICE_VULNERABILITIES.md) — DoS from misconfiguration
- [MOVE_CROSS_CHAIN_BRIDGE_VULNERABILITIES.md](MOVE_CROSS_CHAIN_BRIDGE_VULNERABILITIES.md) — Version check patterns

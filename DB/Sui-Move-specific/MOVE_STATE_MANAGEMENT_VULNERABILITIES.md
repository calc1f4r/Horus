---
protocol: generic
chain: sui, aptos, movement
category: state_management
vulnerability_type: state_inconsistency, variable_shadowing, storage_desync, local_copy_mutation, resource_cleanup, attribute_tracking
attack_type: logical_error, state_manipulation, data_corruption
affected_component: global_storage, local_variables, resource_state, accounting, object_fields
primitives:
  - borrow_global_mut
  - move_to
  - copy_semantics
  - struct_fields
  - dynamic_field
  - object_state
severity: high
impact: fund_loss, accounting_error, state_corruption, operational_disruption
exploitability: 0.6
financial_impact: high
tags:
  - move
  - sui
  - aptos
  - state_management
  - storage
  - local_copy
  - variable_shadowing
  - resource_cleanup
  - accounting
  - desync
  - struct_mutation
language: move
version: all

# Pattern Identity (Required)
root_cause_family: arithmetic_error
pattern_key: arithmetic_error | global_storage, local_variables, resource_state, accounting, object_fields | state_inconsistency, variable_shadowing, storage_desync, local_copy_mutation, resource_cleanup, attribute_tracking

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - accrue_interest
  - borrow
  - borrow_global_mut
  - burn
  - check_group_limit
  - claim_rewards
  - collect_fees
  - copy_semantics
  - create_group
  - delete_group
  - deposit
  - deposit_and_stake
  - dynamic_field
  - execute
  - field
  - get_dividend
  - initialize
  - mint
  - mix
  - move_to
---

## References

| Tag | Report | Protocol | Auditor |
|-----|--------|----------|---------|
| [R1] | reports/ottersec_move_audits/markdown/Securitize_Aptos_Token_Issuance.md | Securitize | OtterSec |
| [R2] | reports/ottersec_move_audits/markdown/Echelon_Market.md | Echelon | OtterSec |
| [R3] | reports/ottersec_move_audits/markdown/KoFi_Finance.md | Kofi Finance | OtterSec |
| [R4] | reports/ottersec_move_audits/markdown/Canopy_Money.md | Canopy | OtterSec |
| [R5] | reports/ottersec_move_audits/markdown/Magna_Aptos.md | Magna | OtterSec |
| [R6] | reports/ottersec_move_audits/markdown/Republic_Aptos.md | Republic | OtterSec |
| [R7] | reports/ottersec_move_audits/markdown/Solend_on_Sui.md | Solend on Sui | OtterSec |
| [R8] | reports/ottersec_move_audits/markdown/Aftermath_Finance_Market_Maker.md | Aftermath AMM | OtterSec |
| [R9] | reports/ottersec_move_audits/markdown/Aave_Aptos_V3.md | Aave Aptos V3 | OtterSec |
| [R10] | reports/ottersec_move_audits/markdown/lombard_sui.md | Lombard SUI | OtterSec |
| [R11] | reports/ottersec_move_audits/markdown/Bluefin_Spot.md | Bluefin Spot | OtterSec |
| [R12] | reports/ottersec_move_audits/markdown/Mysten_Walrus.md | Mysten Walrus | OtterSec |

## Move State Management & Data Integrity Vulnerabilities

### Overview

State management bugs in Move arise from the language's ownership and copy semantics. Unlike Solidity's persistent storage model, Move uses local copies of global state that must be explicitly written back. Forgetting to write back mutations, operating on stale copies, or failing to clean up resources creates accounting inconsistencies that lead to fund loss, incorrect balances, and protocol corruption.

These patterns span 12/29 OtterSec audit reports across Sui, Aptos, and Movement ecosystems.

---



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of arithmetic_error"
- Pattern key: `arithmetic_error | global_storage, local_variables, resource_state, accounting, object_fields | state_inconsistency, variable_shadowing, storage_desync, local_copy_mutation, resource_cleanup, attribute_tracking`
- Interaction scope: `single_contract`
- Primary affected component(s): `global_storage, local_variables, resource_state, accounting, object_fields`
- High-signal code keywords: `accrue_interest`, `borrow`, `borrow_global_mut`, `burn`, `check_group_limit`, `claim_rewards`, `collect_fees`, `copy_semantics`
- Typical sink / impact: `fund_loss, accounting_error, state_corruption, operational_disruption`
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

## Pattern 1: Local Copy Mutation Without Write-Back — move-state-001

**Severity**: HIGH  
**ID**: move-state-001  
**References**: Securitize (OS-ASC-ADV-08), Lombard SUI (OS-LSI-ADV-03)

### Attack Scenario
A function borrows global state, makes a local copy, modifies the copy, but never writes the modified value back to global storage. The state change is lost when the function returns. This is uniquely dangerous in Move because `copy` is implicit for types with the `copy` ability, and the compiler doesn't warn about unused mutations.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Local copy modified but never written back
public fun update_mint_limit(admin: &signer, new_limit: u64) acquires Config {
    let config = *borrow_global<Config>(@protocol);  // ❌ Copies entire struct
    config.mint_limit = new_limit;  // ❌ Modifies local copy
    // ❌ Missing: *borrow_global_mut<Config>(@protocol) = config;
    // Change is silently lost
}
```

### Secure Implementation
```move
// ✅ SECURE: Mutate via borrow_global_mut
public fun update_mint_limit(admin: &signer, new_limit: u64) acquires Config {
    let config = borrow_global_mut<Config>(@protocol);
    config.mint_limit = new_limit;  // ✅ Mutates globally-stored value directly
}
```

---

## Pattern 2: Variable Shadowing Zeroing State Values — move-state-002

**Severity**: HIGH  
**ID**: move-state-002  
**References**: Securitize (OS-ASC-ADV-01)

### Attack Scenario
A variable is declared with the same name as a struct field or earlier binding, shadowing the original value. The shadowed variable is initialized to its type's default (0 for integers), and subsequent logic operates on the zero value instead of the intended state. This causes accounting errors, zero-amount transfers, or assertion bypasses.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: `amount` shadowed by new binding
public fun process_issuance(issuance: &mut Issuance) {
    let amount = issuance.total_amount;  // Original value: 1000
    // ... some logic ...
    let amount = 0u64;  // ❌ Shadows previous `amount` with zero
    // All subsequent uses see amount = 0
    issuance.distributed = issuance.distributed + amount;  // ❌ Adds 0
    transfer_tokens(issuance.recipient, amount);  // ❌ Transfers 0
}
```

### Secure Implementation
```move
// ✅ SECURE: Unique variable names prevent shadowing
public fun process_issuance(issuance: &mut Issuance) {
    let total_amount = issuance.total_amount;
    let remaining = total_amount - issuance.distributed;
    issuance.distributed = issuance.distributed + remaining;
    transfer_tokens(issuance.recipient, remaining);
}
```

---

## Pattern 3: Investor Count Arithmetic Mismatch — move-state-003

**Severity**: MEDIUM  
**ID**: move-state-003  
**References**: Securitize (OS-ASC-ADV-06)

### Attack Scenario
A counter tracking the number of active investors is incremented on deposit but decremented on every withdrawal — even partial ones. After multiple partial withdrawals, the counter goes negative (or underflows), corrupting the investor count. This breaks investor-limit checks, allowing the protocol to exceed regulatory caps or incorrectly reject new investors.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Counter decremented on partial withdrawal
public fun withdraw(state: &mut PoolState, user: address, amount: u64) {
    let balance = get_user_balance(state, user);
    assert!(balance >= amount, E_INSUFFICIENT);
    set_user_balance(state, user, balance - amount);
    // ❌ Decrements on every withdrawal, not just full exit
    state.investor_count = state.investor_count - 1;
}
```

### Secure Implementation
```move
// ✅ SECURE: Only decrement when user fully exits
public fun withdraw(state: &mut PoolState, user: address, amount: u64) {
    let balance = get_user_balance(state, user);
    assert!(balance >= amount, E_INSUFFICIENT);
    let new_balance = balance - amount;
    set_user_balance(state, user, new_balance);
    if (new_balance == 0) {
        state.investor_count = state.investor_count - 1;
    };
}
```

---

## Pattern 4: Wallet Balance Tracking Desync — move-state-004

**Severity**: HIGH  
**ID**: move-state-004  
**References**: Securitize (OS-ASC-ADV-04)

### Attack Scenario
The protocol tracks user balances in an internal registry (e.g., a table) separately from the actual token balances held in user wallets. Transfers, mints, or burns that bypass the registry create a desync: the registry shows one balance while the wallet holds another. Functions that rely on the registry for access control, dividend distribution, or compliance checks make incorrect decisions.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Direct transfer bypasses registry
public fun transfer_tokens(from: &signer, to: address, amount: u64) acquires Registry {
    // ❌ Updates on-chain coin balance but not registry
    coin::transfer<TOKEN>(from, to, amount);
    // Registry still shows old balances for `from` and `to`
}

public fun get_dividend(state: &State, user: address): u64 acquires Registry {
    let registry = borrow_global<Registry>(@protocol);
    // ❌ Uses stale registry balance, not actual wallet balance
    let balance = table::borrow(&registry.balances, user);
    (*balance * state.dividend_per_share) / PRECISION
}
```

### Secure Implementation
```move
// ✅ SECURE: All transfers update registry atomically
public fun transfer_tokens(from: &signer, to: address, amount: u64) acquires Registry {
    let registry = borrow_global_mut<Registry>(@protocol);
    let from_addr = signer::address_of(from);
    let from_bal = table::borrow_mut(&mut registry.balances, from_addr);
    assert!(*from_bal >= amount, E_INSUFFICIENT);
    *from_bal = *from_bal - amount;
    let to_bal = table::borrow_mut(&mut registry.balances, to);
    *to_bal = *to_bal + amount;
    coin::transfer<TOKEN>(from, to, amount);
}
```

---

## Pattern 5: Resource Attribute Cleanup on Removal — move-state-005

**Severity**: MEDIUM  
**ID**: move-state-005  
**References**: Magna (OS-MAG-ADV-02)

### Attack Scenario
When a resource is removed (e.g., an investor removed from a whitelist or a group deleted), associated attributes stored in separate tables or dynamic fields are not cleaned up. Stale attributes persist and may be incorrectly read by other functions, causing authorization bypasses or accounting errors. In Move, this is particularly dangerous because orphaned resources may block reuse of storage keys.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Group removal doesn't clean up member attributes
public fun remove_group(state: &mut State, group_id: u64) {
    // ❌ Only removes group entry, not member-to-group mappings
    table::remove(&mut state.groups, group_id);
    // Members still have group_id in their attributes
    // Subsequent checks: if member.group_id == some_group → passes on stale data
}
```

### Secure Implementation
```move
// ✅ SECURE: Clean up all references when removing group
public fun remove_group(state: &mut State, group_id: u64) {
    let group = table::remove(&mut state.groups, group_id);
    // ✅ Remove all member associations
    let members = group.member_list;
    let i = 0;
    while (i < vector::length(&members)) {
        let member = *vector::borrow(&members, i);
        let attrs = table::borrow_mut(&mut state.member_attrs, member);
        attrs.group_id = DEFAULT_GROUP;
        i = i + 1;
    };
}
```

---

## Pattern 6: Group ID Reuse After Deletion — move-state-006

**Severity**: MEDIUM  
**ID**: move-state-006  
**References**: Magna (OS-MAG-ADV-04)

### Attack Scenario
After a group is deleted, the group ID counter is not incremented or the ID is not marked as used. A new group created later receives the same ID, inheriting all the stale member associations from the deleted group. Members who were in the old group are silently added to the new one without authorization.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Group ID reused after deletion
struct GroupManager has key {
    next_group_id: u64,
    groups: Table<u64, GroupInfo>,
}

public fun delete_group(mgr: &mut GroupManager, id: u64) {
    table::remove(&mut mgr.groups, id);
    // ❌ next_group_id not updated — new group may reuse this ID
}

public fun create_group(mgr: &mut GroupManager): u64 {
    let id = mgr.next_group_id;
    // ❌ If id was previously deleted, stale references exist
    table::add(&mut mgr.groups, id, GroupInfo { /* ... */ });
    mgr.next_group_id = id + 1;
    id
}
```

### Secure Implementation
```move
// ✅ SECURE: Always increment, never reuse IDs
public fun delete_group(mgr: &mut GroupManager, id: u64) {
    table::remove(&mut mgr.groups, id);
    // ✅ ID is consumed — next_group_id only goes forward
    // No need to track deleted IDs since next_group_id > all previous
}

public fun create_group(mgr: &mut GroupManager): u64 {
    let id = mgr.next_group_id;
    mgr.next_group_id = id + 1;  // ✅ Monotonically increasing
    table::add(&mut mgr.groups, id, GroupInfo { /* ... */ });
    id
}
```

---

## Pattern 7: Storage Split Accounting Inconsistency — move-state-007

**Severity**: HIGH  
**ID**: move-state-007  
**References**: Kofi Finance (OS-KOF-ADV-07)

### Attack Scenario
A protocol separates its balance into multiple accounting buckets (e.g., staked, pending, fees). When tokens flow between buckets, one side of the transfer is updated but the other is missed. The total across all buckets diverges from the actual balance held, creating phantom assets or hidden liabilities.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Partial update of split accounting
public fun collect_fees(pool: &mut Pool) {
    let fee_amount = pool.uncollected_fees;
    pool.uncollected_fees = 0;
    // ❌ Credits fee_balance but doesn't debit from available_balance
    pool.fee_balance = pool.fee_balance + fee_amount;
    // pool.available_balance should decrease, but doesn't
    // Total across buckets > actual balance
}
```

### Secure Implementation
```move
// ✅ SECURE: Double-entry bookkeeping
public fun collect_fees(pool: &mut Pool) {
    let fee_amount = pool.uncollected_fees;
    pool.uncollected_fees = 0;
    pool.fee_balance = pool.fee_balance + fee_amount;
    pool.available_balance = pool.available_balance - fee_amount; // ✅ Debit
    // ✅ Invariant: available + fee + staked == actual balance
    assert!(
        pool.available_balance + pool.fee_balance + pool.staked_balance
            == balance::value(&pool.coin_balance),
        E_ACCOUNTING_MISMATCH
    );
}
```

---

## Pattern 8: Stale Share Rate in Multi-Step Operations — move-state-008

**Severity**: HIGH  
**ID**: move-state-008  
**References**: Solend (OS-SAM-ADV-03), Echelon (OS-ECH-ADV-06)

### Attack Scenario
A multi-step operation (e.g., deposit+stake, borrow+supply) reads the share exchange rate at the beginning but doesn't refresh it between steps. If step 1 modifies the rate (e.g., by accruing interest), step 2 uses a stale rate, allowing the caller to get more shares than they should or repay less debt than owed.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Rate cached before modification
public fun deposit_and_stake(pool: &mut Pool, amount: u64, ctx: &mut TxContext) {
    let rate = pool.total_assets / pool.total_shares;  // ❌ Cached rate
    
    // Step 1: Deposit (modifies total_assets)
    pool.total_assets = pool.total_assets + amount;
    accrue_interest(pool);  // ❌ Changes total_assets again
    
    // Step 2: Calculate shares using STALE rate
    let shares = amount * PRECISION / rate;  // ❌ Uses pre-interest rate
    pool.total_shares = pool.total_shares + shares;
}
```

### Secure Implementation
```move
// ✅ SECURE: Refresh rate after each state-modifying step
public fun deposit_and_stake(pool: &mut Pool, amount: u64, ctx: &mut TxContext) {
    accrue_interest(pool);  // ✅ Accrue first
    pool.total_assets = pool.total_assets + amount;
    // ✅ Calculate shares with current (post-accrue) state
    let shares = (amount * pool.total_shares) / pool.total_assets;
    pool.total_shares = pool.total_shares + shares;
}
```

---

## Pattern 9: Missing Default Group Assignment — move-state-009

**Severity**: MEDIUM  
**ID**: move-state-009  
**References**: Magna (OS-MAG-ADV-03)

### Attack Scenario
New users are created without being assigned to a default group. Functions that check group membership for access control or rate limiting return unexpected results (empty, zero, or error) for ungrouped users. This either blocks legitimate users or bypasses group-based restrictions.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: No default group for new users
public fun register_user(state: &mut State, user: address) {
    table::add(&mut state.users, user, UserInfo {
        balance: 0,
        group_id: 0,  // ❌ 0 may not correspond to any real group
    });
}

public fun check_group_limit(state: &State, user: address): bool {
    let info = table::borrow(&state.users, user);
    let group = table::borrow(&state.groups, info.group_id);  // ❌ Aborts if group 0 doesn't exist
    group.current_count < group.max_members
}
```

### Secure Implementation
```move
// ✅ SECURE: Assign to default group on creation
const DEFAULT_GROUP_ID: u64 = 1;

public fun register_user(state: &mut State, user: address) {
    assert!(table::contains(&state.groups, DEFAULT_GROUP_ID), E_NO_DEFAULT_GROUP);
    table::add(&mut state.users, user, UserInfo {
        balance: 0,
        group_id: DEFAULT_GROUP_ID,
    });
    let group = table::borrow_mut(&mut state.groups, DEFAULT_GROUP_ID);
    group.current_count = group.current_count + 1;
}
```

---

## Pattern 10: Last Modifier Tracking Failure — move-state-010

**Severity**: LOW  
**ID**: move-state-010  
**References**: Echelon (OS-ECH-ADV-03)

### Attack Scenario
The protocol tracks the last user who modified a shared object (e.g., for reward attribution or audit logging). However, internal operations (accrual, auto-compounding) also modify the object without updating the last modifier. A user can trigger an internal update to overwrite the last modifier field, gaining attribution for changes they didn't make.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Internal operations don't update last_modifier
public fun accrue_interest(pool: &mut Pool) {
    let interest = calculate_interest(pool);
    pool.total_assets = pool.total_assets + interest;
    // ❌ pool.last_modifier not updated — still shows previous user
}

public fun deposit(pool: &mut Pool, user: address, amount: u64) {
    accrue_interest(pool);  // ❌ Modifies pool but last_modifier still stale
    pool.total_assets = pool.total_assets + amount;
    pool.last_modifier = user;
}
```

### Secure Implementation
```move
// ✅ SECURE: Track modification source distinctly
public fun accrue_interest(pool: &mut Pool) {
    let interest = calculate_interest(pool);
    pool.total_assets = pool.total_assets + interest;
    pool.last_modifier = @system;  // ✅ Internal operation tagged
    pool.last_modification_type = MODIFICATION_ACCRUAL;
}
```

---

## Pattern 11: Pause State Allowing Partial Operations — move-state-011

**Severity**: MEDIUM  
**ID**: move-state-011  
**References**: Canopy (OS-CMP-ADV-02), Republic (OS-REP-ADV-01)

### Attack Scenario
A protocol implements a pause mechanism but doesn't apply it uniformly to all state-modifying functions. A paused protocol still allows certain operations (e.g., claims, withdrawals, or parameter updates) to execute, creating inconsistent state. An attacker exploits the unpaused functions to manipulate state while the protocol team believes operations are frozen.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Pause check missing on claim function
public fun deposit(state: &mut State, amount: u64) {
    assert!(!state.paused, E_PAUSED);  // ✅ Checked
    // ... deposit logic
}

public fun claim_rewards(state: &mut State, user: address) {
    // ❌ Missing pause check — claims still work when paused
    let rewards = calculate_rewards(state, user);
    transfer_rewards(state, user, rewards);
}
```

### Secure Implementation
```move
// ✅ SECURE: Centralized pause check via helper
fun assert_not_paused(state: &State) {
    assert!(!state.paused, E_PAUSED);
}

public fun deposit(state: &mut State, amount: u64) {
    assert_not_paused(state);
    // ... deposit logic
}

public fun claim_rewards(state: &mut State, user: address) {
    assert_not_paused(state);  // ✅ Now also checked
    let rewards = calculate_rewards(state, user);
    transfer_rewards(state, user, rewards);
}
```

---

## Pattern 12: Token Metadata Swap Between Objects — move-state-012

**Severity**: HIGH  
**ID**: move-state-012  
**References**: Securitize (OS-ASC-ADV-09)

### Attack Scenario
When creating multiple token types, the metadata or treasury capabilities are assigned to the wrong token. For example, token A's treasury cap is stored in token B's manager, and vice versa. This allows minting token A using token B's authority, or burns on the wrong token, corrupting both token supplies.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Treasury caps assigned to wrong tokens
public fun initialize(admin: &signer) {
    let (burn_a, freeze_a, mint_a) = coin::initialize<TokenA>(...);
    let (burn_b, freeze_b, mint_b) = coin::initialize<TokenB>(...);
    
    move_to(admin, TokenAManager {
        mint_cap: mint_a,
        burn_cap: burn_b,  // ❌ TokenB's burn cap in TokenA's manager!
    });
    move_to(admin, TokenBManager {
        mint_cap: mint_b,
        burn_cap: burn_a,  // ❌ TokenA's burn cap in TokenB's manager!
    });
}
```

### Secure Implementation
```move
// ✅ SECURE: Explicitly typed capabilities prevent mix-up
public fun initialize(admin: &signer) {
    let (burn_a, freeze_a, mint_a) = coin::initialize<TokenA>(...);
    let (burn_b, freeze_b, mint_b) = coin::initialize<TokenB>(...);
    
    move_to(admin, TokenAManager {
        mint_cap: mint_a,
        burn_cap: burn_a,  // ✅ Correct: TokenA's caps
    });
    move_to(admin, TokenBManager {
        mint_cap: mint_b,
        burn_cap: burn_b,  // ✅ Correct: TokenB's caps
    });
}
```

---

### Impact Analysis

#### Technical Impact
- Silent state mutations lost on function return (local copy bug) — HIGH
- Accounting desync between registry and actual balances — HIGH
- Phantom assets from split accounting errors — HIGH
- Stale exchange rates enabling over-minting of shares — HIGH
- Group-based access control bypassed via stale attributes — MEDIUM

#### Business Impact
- Protocol balance sheet incorrect — visible insolvency or hidden liabilities
- Regulatory violations from incorrect investor counts
- User funds stuck or misdirected from metadata swap
- Audit trail corrupted by incorrect modifier tracking
- Emergency pause ineffective due to incomplete coverage

#### Affected Scenarios
- Token issuance platforms with compliance tracking (Securitize)
- Lending protocols with multi-step operations (Echelon, Solend)
- Staking protocols with split balance accounting (Kofi)
- Investor management with group-based limits (Magna)
- Any Move protocol with copy-able struct types

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: `let x = *borrow_global<T>(@addr)` followed by mutation of `x` (local copy)
- Pattern 2: `let amount = 0u64` or re-binding same variable name in same scope
- Pattern 3: `state.counter = state.counter - 1` on partial (not full) withdrawal
- Pattern 4: `coin::transfer` without corresponding registry update
- Pattern 5: `table::remove` without cleaning associated tables
- Pattern 6: Counter/ID not monotonically increasing after deletion
- Pattern 7: `pool.bucket_a += x` without `pool.bucket_b -= x` (single-entry bookkeeping)
- Pattern 8: Exchange rate calculated before `accrue_interest()` call
- Pattern 9: New user with `group_id: 0` when no group 0 exists
- Pattern 10: `burn_cap: burn_b` in TokenAManager (capability cross-assignment)
- Pattern 11: Pause check present in some functions but absent in others
- Pattern 12: `pool.last_modifier` not updated in internal operations
```

#### Audit Checklist
- [ ] All state mutations use `borrow_global_mut`, not copied values
- [ ] No variable shadowing in state-modifying functions
- [ ] Counter decrements only on full exit (not partial withdrawal)
- [ ] All token transfers update internal registry atomically
- [ ] Resource removal cleans up all associated attributes and references
- [ ] IDs are monotonically increasing and never reused
- [ ] Split accounting uses double-entry bookkeeping with invariant checks
- [ ] Exchange rates refreshed after every state-modifying step
- [ ] New users assigned to valid default group
- [ ] Capability types match their owning manager structs
- [ ] Pause mechanism applied uniformly to all external functions
- [ ] Internal operations update tracking fields (modifier, timestamp)

### Keywords for Search

> `state management`, `local copy`, `borrow_global_mut`, `variable shadowing`, `investor count`, `balance tracking`, `registry desync`, `split accounting`, `double entry`, `exchange rate`, `stale rate`, `group assignment`, `default group`, `resource cleanup`, `orphaned resource`, `ID reuse`, `monotonic counter`, `pause check`, `incomplete pause`, `token metadata`, `capability swap`, `treasury cap`, `mint cap`, `burn cap`, `last modifier`, `copy semantics`, `move state`, `sui state`, `aptos state`, `accounting mismatch`, `phantom assets`, `storage split`

### Related Vulnerabilities

- [MOVE_ACCESS_CONTROL_AUTHORIZATION_VULNERABILITIES.md](MOVE_ACCESS_CONTROL_AUTHORIZATION_VULNERABILITIES.md) — Authorization bypass from stale state
- [MOVE_ARITHMETIC_PRECISION_VULNERABILITIES.md](MOVE_ARITHMETIC_PRECISION_VULNERABILITIES.md) — Rounding errors in rate calculations
- [MOVE_TOKEN_SUPPLY_INFLATION_VULNERABILITIES.md](MOVE_TOKEN_SUPPLY_INFLATION_VULNERABILITIES.md) — Supply corruption from state bugs
- [MOVE_DEFI_PROTOCOL_LOGIC_VULNERABILITIES.md](MOVE_DEFI_PROTOCOL_LOGIC_VULNERABILITIES.md) — Protocol logic interacting with state

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

`accounting`, `accrue_interest`, `aptos`, `borrow`, `borrow_global_mut`, `burn`, `check_group_limit`, `claim_rewards`, `collect_fees`, `copy_semantics`, `create_group`, `delete_group`, `deposit`, `deposit_and_stake`, `desync`, `dynamic_field`, `execute`, `field`, `get_dividend`, `initialize`, `local_copy`, `mint`, `mix`, `move`, `move_to`, `object_state`, `resource_cleanup`, `state_inconsistency, variable_shadowing, storage_desync, local_copy_mutation, resource_cleanup, attribute_tracking`, `state_management`, `storage`, `struct_fields`, `struct_mutation`, `sui`, `variable_shadowing`

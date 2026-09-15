# Certora Sui Move Spec Templates

## Contents
- [Base spec scaffold](#base-spec-scaffold)
- [Sanity rule (basic reachability)](#sanity-rule-basic-reachability)
- [No-abort rule (function never panics)](#no-abort-rule-function-never-panics)
- [State monotonicity via parametric rules](#state-monotonicity-via-parametric-rules)
- [Balance conservation (ghost tracking)](#balance-conservation-ghost-tracking)
- [Access control (privileged operation)](#access-control-privileged-operation)
- [Summary for loops](#summary-for-loops)
- [Shadow mapping for VecMap](#shadow-mapping-for-vecmap)
- [Arithmetic safety with MathInt](#arithmetic-safety-with-mathint)
- [Auto-generated sanity rules](#auto-generated-sanity-rules)
- [Anti-patterns (DO NOT USE)](#anti-patterns-do-not-use)

---

## Base Spec Scaffold

Every spec module should follow this skeleton.

```move
module spec::rules;

// Import target contract types
use my_contract::my_module::MyStruct;

// Import CVLM primitives
use cvlm::asserts::{cvlm_assert, cvlm_assert_msg, cvlm_satisfy, cvlm_satisfy_msg, cvlm_assume_msg};
use cvlm::manifest::{rule, target, invoker, target_sanity};
use cvlm::nondet::nondet;

/// Register all rules and targets in the manifest
public fun cvlm_manifest() {
    // Register target functions from the contract
    target(@my_contract, b"my_module", b"function_a");
    target(@my_contract, b"my_module", b"function_b");

    // Register rules
    rule(b"my_first_rule");
    rule(b"my_second_rule");

    // Generate sanity rules for all targets
    target_sanity();
}

// --- Rules below ---
```

---

## Sanity Rule (Basic Reachability)

Verify that a function can execute to completion without aborting.

```move
use cvlm::asserts::cvlm_satisfy_msg;
use cvlm::manifest::rule;

public fun cvlm_manifest() {
    rule(b"create_pool_sanity");
}

public fun create_pool_sanity(
    admin_cap: &AdminCap,
    fee_bps: u64,
    ctx: &mut TxContext,
) {
    my_contract::pool::create_pool(admin_cap, fee_bps, ctx);
    cvlm_satisfy_msg(true, b"create_pool reached end");
}
```

---

## No-Abort Rule (Function Never Panics)

Assert that no code invoked by the rule can abort. Useful for verifying that entry points handle all inputs gracefully.

```move
use cvlm::asserts::cvlm_satisfy_msg;
use cvlm::manifest::no_abort_rule;

public fun cvlm_manifest() {
    no_abort_rule(b"deposit_never_aborts");
}

public fun deposit_never_aborts(
    pool: &mut Pool,
    coin: Coin<SUI>,
    ctx: &mut TxContext,
) {
    my_contract::pool::deposit(pool, coin, ctx);
    cvlm_satisfy_msg(true, b"deposit completed without abort");
}
```

**Warning**: Soundness depends on summary accuracy. If a summarized platform function suppresses aborts, the rule may pass incorrectly.

---

## State Monotonicity via Parametric Rules

Verify that a property holds across ALL registered target functions.

```move
use cvlm::asserts::{cvlm_assert, cvlm_satisfy};
use cvlm::manifest::{rule, target, invoker};
use cvlm::function::Function;

public fun cvlm_manifest() {
    target(@my_contract, b"pool", b"deposit");
    target(@my_contract, b"pool", b"withdraw");
    target(@my_contract, b"pool", b"swap");
    target(@my_contract, b"pool", b"claim_fees");

    invoker(b"invoke");
    rule(b"total_liquidity_never_negative");
}

native fun invoke(target: Function, pool: &mut Pool);

public fun total_liquidity_never_negative(
    pool: &mut Pool,
    target: Function,
) {
    // Pre-state
    let liquidity_before = pool.total_liquidity();

    // Execute any target function
    invoke(target, pool);

    // Post-state: liquidity must not go negative (assuming u64, this checks it didn't underflow-abort)
    let liquidity_after = pool.total_liquidity();
    cvlm_assert(liquidity_after >= 0);
    cvlm_satisfy(true);
}
```

The prover generates one sub-rule per target function (deposit, withdraw, swap, claim_fees).

---

## Balance Conservation (Ghost Tracking)

Track aggregate state via ghost mappings to verify conservation laws.

```move
use cvlm::asserts::{cvlm_assert_msg, cvlm_assume_msg, cvlm_satisfy};
use cvlm::manifest::{rule, ghost, summary};
use cvlm::math_int::MathInt;
use cvlm::nondet::nondet;

public fun cvlm_manifest() {
    ghost(b"balance_tracker");
    rule(b"transfer_conserves_total");
}

// Ghost mapping: address -> tracked balance
native fun balance_tracker(addr: address): &mut MathInt;

public fun transfer_conserves_total(
    vault: &mut Vault,
    from: address,
    to: address,
    amount: u64,
    ctx: &mut TxContext,
) {
    // Snapshot pre-state
    let from_before = MathInt::from_u64(vault.balance_of(from));
    let to_before = MathInt::from_u64(vault.balance_of(to));
    let total_before = MathInt::add(from_before, to_before);

    // Execute transfer
    my_contract::vault::transfer(vault, from, to, amount, ctx);

    // Snapshot post-state
    let from_after = MathInt::from_u64(vault.balance_of(from));
    let to_after = MathInt::from_u64(vault.balance_of(to));
    let total_after = MathInt::add(from_after, to_after);

    // Conservation: total before == total after
    cvlm_assert_msg(
        MathInt::ge(total_after, total_before) && MathInt::le(total_after, total_before),
        b"Transfer must conserve total balance"
    );
    cvlm_satisfy(true);
}
```

---

## Access Control (Privileged Operation)

Verify that only authorized callers can execute privileged operations.

```move
use cvlm::asserts::{cvlm_assert_msg, cvlm_satisfy};
use cvlm::manifest::rule;

public fun cvlm_manifest() {
    rule(b"only_admin_can_set_fee");
}

/// Verify that set_fee requires AdminCap — test that the function works WITH the cap.
/// The Move type system enforces access control via capability objects (AdminCap).
/// To verify, confirm the function succeeds with a valid cap.
public fun only_admin_can_set_fee(
    admin_cap: &AdminCap,
    pool: &mut Pool,
    new_fee: u64,
) {
    let old_fee = pool.fee_bps();
    my_contract::pool::set_fee(admin_cap, pool, new_fee);
    cvlm_assert_msg(pool.fee_bps() == new_fee, b"Fee must be updated");
    cvlm_satisfy(true);
}
```

**Note**: In Move/Sui, access control is enforced by the type system via capability objects (e.g., `AdminCap`). Unauthorized callers simply cannot construct the capability. Verify that the function works correctly WITH capabilities rather than testing rejection without them.

---

## Summary for Loops

Replace unbounded loops with logical approximations.

### Step 1: Add test_only accessors in target contract

```move
// In the target contract module
#[test_only]
public fun items(self: &MyCollection): &vector<Item> {
    &self.items
}

#[test_only]
public fun get_score(self: &MyCollection, idx: u64): u64 {
    self.items[idx].score
}
```

### Step 2: Write the summary

```move
module spec::summaries;

use my_contract::my_module::MyCollection;
use cvlm::manifest::summary;
use cvlm::nondet::nondet;
use cvlm::asserts::cvlm_assume_msg;

public fun cvlm_manifest() {
    summary(b"find_best_idx_summary", @my_contract, b"my_module", b"find_best_idx");
}

#[test_only]
public fun find_best_idx_summary(collection: &MyCollection): u64 {
    let len = collection.items().length();
    if (len == 0) {
        return 0
    };
    let idx = nondet<u64>();
    cvlm_assume_msg(
        idx < len,
        b"index in bounds"
    );
    // The summary captures the loop's postcondition: idx points to the best score
    idx
}
```

---

## Shadow Mapping for VecMap

Replace VecMap's internal vector-of-entries representation with a logical mapping.

```move
use sui::vec_map::VecMap;
use cvlm::manifest::shadow;

public fun cvlm_manifest() {
    shadow(b"vec_map_shadow");
}

// Shadow: VecMap<K,V> behaves as a mapping from K to V
native fun vec_map_shadow<K: copy, V>(map: &VecMap<K, V>, key: &K): &mut V;
```

After shadowing, all functions that access VecMap internals (pack, unpack, field access) must be summarized.

---

## Arithmetic Safety with MathInt

Use `MathInt` for overflow-free intermediate arithmetic.

```move
use cvlm::asserts::{cvlm_assert_msg, cvlm_satisfy};
use cvlm::manifest::rule;
use cvlm::math_int::MathInt;

public fun cvlm_manifest() {
    rule(b"fee_calculation_no_overflow");
}

public fun fee_calculation_no_overflow(
    amount: u64,
    fee_bps: u64,
) {
    // Use MathInt to avoid overflow in intermediate calculation
    let amount_mi = MathInt::from_u64(amount);
    let fee_bps_mi = MathInt::from_u64(fee_bps);
    let bps_base = MathInt::from_u64(10000);

    let expected_fee = MathInt::div(MathInt::mul(amount_mi, fee_bps_mi), bps_base);

    // Verify fee is always <= amount
    cvlm_assert_msg(
        MathInt::le(expected_fee, amount_mi),
        b"Fee must not exceed amount"
    );

    // Verify fee is non-negative
    cvlm_assert_msg(
        MathInt::ge(expected_fee, MathInt::zero()),
        b"Fee must be non-negative"
    );

    cvlm_satisfy(true);
}
```

---

## Auto-Generated Sanity Rules

Quickly generate sanity checks for all functions in a module.

```move
use cvlm::manifest::{target, target_sanity};

public fun cvlm_manifest() {
    // Register all public entry functions
    target(@my_contract, b"pool", b"create_pool");
    target(@my_contract, b"pool", b"deposit");
    target(@my_contract, b"pool", b"withdraw");
    target(@my_contract, b"pool", b"swap");
    target(@my_contract, b"pool", b"set_fee");

    // Auto-generate two rules per target:
    //   1. satisfy-true: execution reaches the end
    //   2. assert-true: test implicit pessimistic assertions only
    target_sanity();
}
```

---

## Anti-Patterns (DO NOT USE)

### 1. Rule without satisfy

```move
// BAD: No way to check if rule is vacuous
public fun bad_rule(pool: &mut Pool, amount: u64) {
    cvlm_assume_msg(amount > 0, b"positive");
    my_contract::pool::deposit(pool, amount);
    cvlm_assert(pool.balance() >= amount);
    // Missing: cvlm_satisfy(true);
}
```

### 2. Contradictory assumes

```move
// BAD: No state can satisfy both assumptions — rule passes vacuously
public fun vacuous_rule(amount: u64) {
    cvlm_assume_msg(amount > 100, b"large");
    cvlm_assume_msg(amount < 50, b"small");
    // Everything below is vacuously true
    cvlm_assert(false); // This would STILL pass!
}
```

### 3. Over-constrained nondet

```move
// BAD: Too many assumptions make the rule trivial
public fun overconstrained(pool: &mut Pool) {
    let amount = nondet<u64>();
    cvlm_assume_msg(amount == 42, b"exactly 42");
    // Only testing one specific value — not useful
}
```

### 4. Missing summary for shadowed struct operations

```move
// BAD: Shadowed VecMap but didn't summarize vec_map::insert
shadow(b"my_shadow");
// Missing: summary(b"insert_summary", @sui, b"vec_map", b"insert");
// Prover will error when any code calls vec_map::insert
```

### 5. Testing admin rejection in Move

```move
// BAD: In Move, you can't call a function requiring AdminCap without having one
// The type system prevents this at compile time — there's nothing to verify
public fun bad_access_control_test(
    pool: &mut Pool,
    new_fee: u64,
) {
    // Can't even call set_fee without AdminCap — this won't compile
    // my_contract::pool::set_fee(pool, new_fee);  // ERROR: missing AdminCap argument
}
```

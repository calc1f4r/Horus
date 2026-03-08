---
# Core Classification (Required)
protocol: generic
chain: sui
category: sui_object_model
vulnerability_type: sui_move_object_security

# Attack Vector Details (Required)
attack_type: logical_error|data_manipulation
affected_component: object_model|uid|dynamic_fields|kiosk|bigvector|digest|verifier

# Technical Primitives (Required)
primitives:
  - uid
  - object_id
  - dynamic_field
  - kiosk
  - bigvector
  - move_package
  - id_leak_verifier
  - hash_type_and_key
  - compute_digest_for_modules_and_deps
  - set_allow_extensions
  - uid_mut
  - max_slice_size
  - sui_object
  - key_ability
  - store_ability

# Impact Classification (Required)
severity: high
impact: fund_loss|dos|state_corruption|security_bypass
exploitability: 0.6
financial_impact: high

# Context Tags
tags:
  - sui
  - move
  - object_model
  - blockchain_core
  - l1_security
  - nft
  - domain_names

# Version Info
language: move|rust
version: all
---

## References & Source Reports

> **For Agents**: Read the full report for each finding at the referenced path.

### UID / Object Identity Vulnerabilities
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Bypass ID Leak Verifier | `reports/sui_move_findings/bypass-id-leak-verifier.md` | HIGH | OtterSec | Mysten Labs Sui |
| Missing UID Validation | `reports/sui_move_findings/missing-uid-validation.md` | HIGH | OtterSec | BlueFin |

### Dynamic Field & Hash Collision Vulnerabilities
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Dynamic Field Hash Collision | `reports/sui_move_findings/dynamic-field-hash-collision.md` | HIGH | OtterSec | Mysten Labs Sui |
| Modules Digest Collision | `reports/sui_move_findings/modules-digest-collision.md` | HIGH | OtterSec | Mysten Labs Sui |

### Object Size / Limit Vulnerabilities
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| BigVector Size Overflow | `reports/sui_move_findings/bigvector-size-overflow.md` | MEDIUM | OtterSec | Mysten Deepbook |
| DoS Due to Object Limits | `reports/sui_move_findings/denial-of-service-in-several-functions-due-to-object-limits.md` | HIGH | Quantstamp | Dipcoin Vault |

### Kiosk & Extension Vulnerabilities
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Blocking User Funds in Kiosk | `reports/sui_move_findings/blocking-user-funds-in-kiosk.md` | MEDIUM | OtterSec | Mysten Labs Sui |

### Name Service / Domain Vulnerabilities
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Incorrect Value in Record Name | `reports/sui_move_findings/incorrect-value-in-record-name.md` | HIGH | OtterSec | Mysten Labs Sui |
| Absence of Checks for Max TTL | `reports/sui_move_findings/absence-of-checks-for-max-ttl.md` | MEDIUM | OtterSec | Mysten Labs Sui |

### Committee / Epoch Vulnerabilities
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Inability to End an Epoch | `reports/sui_move_findings/inability-to-end-an-epoch.md` | HIGH | OtterSec | Sui Bridge |
| Blocklist Validation Order Mismatch | `reports/sui_move_findings/blocklist-validation-order-mismatch.md` | MEDIUM | OtterSec | Sui Bridge |

### Upgrade Model Vulnerabilities
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Bypass ID Leak Verifier via Upgrade | `reports/sui_move_findings/bypass-id-leak-verifier.md` | HIGH | OtterSec | Mysten Labs Sui |
| Mixing Over Limit SuiFrens | `reports/sui_move_findings/mixing-over-limit-suifrens.md` | HIGH | OtterSec | Mysten Labs Sui |
| Arbitrary Update of Last Epoch Mixed | `reports/sui_move_findings/arbitrary-update-of-last-epoch-mixed.md` | HIGH | OtterSec | Mysten Labs Sui |

### Artifacts Index
| Artifact | Source | Type |
|----------|--------|------|
| `artifacts/12-github.com-MystenLabs-sui-3c59aa0b.html` | MystenLabs/sui GitHub | HTML |
| `artifacts/10-github.com-MystenLabs-deepbookv3-77d3d535.html` | MystenLabs/deepbookv3 GitHub | HTML |

---

# Sui Move Object Model Vulnerabilities — Comprehensive Database

**A Complete Pattern-Matching Guide for Sui/Move Object Model Security Audits**

---

## Table of Contents

1. [UID Leak / Object Identity Bypass](#1-uid-leak--object-identity-bypass)
2. [Dynamic Field Hash Collision](#2-dynamic-field-hash-collision)
3. [Package Digest Collision](#3-package-digest-collision)
4. [Object Size Limit DoS](#4-object-size-limit-dos)
5. [Kiosk Extension Fund Locking](#5-kiosk-extension-fund-locking)
6. [Missing UID Validation in DeFi](#6-missing-uid-validation-in-defi)
7. [Committee / Epoch Management Bugs](#7-committee--epoch-management-bugs)
8. [Visibility / Ability Misuse via Upgrades](#8-visibility--ability-misuse-via-upgrades)
9. [Name Service Validation Failures](#9-name-service-validation-failures)
10. [Dynamic Field Access Limit DoS](#10-dynamic-field-access-limit-dos)

---

## 1. UID Leak / Object Identity Bypass

### Overview

The `id_leak_verifier` in Sui's Move verifier ensures that a UID for a Sui Object is never reused — a critical safety property for Sui's object-centric model. However, the unique Sui upgrade model can be exploited to bypass this check, allowing UID reuse across package versions.

> **Validation strength**: Moderate — 2 reports from OtterSec across Mysten Labs Sui core
> **Frequency**: 2/69 reports (Sui-specific, L1-level severity)

### Vulnerability Description

#### Root Cause

The verifier does not validate structures without a `key` capability. During a package upgrade, a struct that originally lacked `key` can have this ability added. An object constructed with the old version (where UID packing was unchecked) can then be passed to the new version, where it appears as a valid Sui object with a reused UID.

#### Attack Scenario

1. Publish a module with struct `Bar` without `key` ability — verifier skips UID leak checks
2. Upgrade the module, adding `key` ability to `Bar`  
3. Construct `Bar` with a reused UID using the old version's functions
4. Pass the object into the new version — it is accepted as a valid keyed object with reused UID

### Vulnerable Pattern Examples

**Example 1: Bypass via Package Upgrade** [HIGH]
> 📖 Reference: `reports/sui_move_findings/bypass-id-leak-verifier.md`
```move
// ❌ VULNERABLE: V0 - struct without key, verifier doesn't check UID packing
module Test_V0::base {
    struct Bar { id: UID }  // no key ability
    
    public fun build_bar_from_foo(foo: Foo): Bar {
        let Foo { id } = foo;
        Bar { id: id }  // UID reuse allowed — no key means no verifier check
    }
}

// After upgrade: V1 adds key ability
module Test_V1::base {
    struct Bar has key { id: UID }  // now has key
    // Old V0 function still packs Bar with reused UID
}
```

**Example 2: Missing UID Validation in Vault Operations** [HIGH]
> 📖 Reference: `reports/sui_move_findings/missing-uid-validation.md`
```move
// ❌ VULNERABLE: No validation that BankV2 object matches expected instance
entry fun deposit_to_vault<USDC>(
    bluefin_bank: &mut BluefinBank<USDC>,  // which bank is this?
    vault: &mut Vault<USDC>,
    coin: &mut Coin<USDC>,
    amount: u64,
    ctx: &mut TxContext
) {
    // Checks vault version and perpetual_id but NOT bank UID
    assert!(vault.perpetual_id == object::uid_to_inner(perpetual::id_v2(bluefin_perpetual)), ...);
    // Missing: assert!(object::id(bluefin_bank) == vault.expected_bank_id, ...)
}
```

### Impact Analysis

#### Technical Impact
- UID reuse allows creating objects that collide with existing Sui objects
- Can corrupt global object storage and shared object state
- Bank/vault operations with wrong objects lead to fund loss

#### Business Impact
- L1-level security bypass threatens all Sui applications
- DeFi protocols relying on object identity can be drained
- Share minting at incorrect prices

#### Affected Scenarios
- Any protocol that relies on Sui's object uniqueness guarantee
- Vault/bank systems with multiple instances (BlueFin, Aftermath)
- Cross-version module interactions during upgrades

### Secure Implementation

**Fix 1: Restrict Ability Addition During Upgrade**
```move
// ✅ SECURE: Verifier should reject adding key ability to existing structs during upgrade
// This was fixed in Sui core — the verifier now blocks adding key to non-key structs
```

**Fix 2: Explicit Object ID Validation**
```move
// ✅ SECURE: Always validate object IDs against expected values
entry fun deposit_to_vault<USDC>(
    bluefin_bank: &mut BluefinBank<USDC>,
    vault: &mut Vault<USDC>,
    coin: &mut Coin<USDC>,
    amount: u64,
    ctx: &mut TxContext
) {
    // Validate the bank matches what the vault expects
    assert!(object::id(bluefin_bank) == vault.bank_id, errors::invalid_bank());
    assert!(vault.perpetual_id == expected_perp_id, errors::perp_not_supported());
    // ... proceed with deposit
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Structs without `key` ability that contain UID
- Package upgrades that add `key` to existing structs
- Functions accepting shared objects without UID validation
- Cross-version function calls with object parameters
- Missing assert on object::id() comparisons
```

#### Audit Checklist
- [ ] Verify all structs with UID field have `key` ability from initial publication
- [ ] Check upgrade compatibility — no ability additions that bypass verifier
- [ ] Ensure all shared object parameters have UID/ID validation
- [ ] Validate that vault/bank operations check expected object IDs

---

## 2. Dynamic Field Hash Collision

### Overview

Sui's dynamic fields use `hash_type_and_key` to compute unique identifiers. A flaw in the hash computation — missing length separators — allows crafted collisions that can corrupt the dynamic field storage.

> **Validation strength**: Strong — core framework vulnerability found by OtterSec
> **Frequency**: 1/69 reports (critical L1 impact)

### Vulnerability Description

#### Root Cause

The `hash_type_and_key` function concatenates `parent`, `k_bytes`, and `k_tag_bytes` without inserting length delimiters. Due to the semi-arbitrary structure of `Struct` and `Vector` data types, two different type/key combinations can produce identical hashes.

#### Attack Scenario

1. Attacker crafts two different dynamic field type+key combinations that produce the same hash
2. Operations like `add` and `exists_` resolve to the wrong field
3. This corrupts protocol state relying on dynamic fields for storage

### Vulnerable Pattern Examples

**Example 1: Missing Length Delimiters in Hash** [HIGH]
> 📖 Reference: `reports/sui_move_findings/dynamic-field-hash-collision.md`
```rust
// ❌ VULNERABLE: No length delimiters between components
fn hash_type_and_key(parent: &AccountAddress, k_bytes: &[u8], k_tag_bytes: &[u8]) -> [u8; 32] {
    let mut hasher = Sha3_256::default();
    hasher.update(parent);
    hasher.update(k_bytes);      // If k_bytes = [A, B] and k_tag_bytes = [C]
    hasher.update(k_tag_bytes);  // collides with k_bytes = [A] and k_tag_bytes = [B, C]
    hasher.finalize()
}
```

### Secure Implementation

**Fix: Insert Length Delimiters**
```rust
// ✅ SECURE: Length-prefix each component to prevent cross-boundary collisions
fn hash_type_and_key(parent: &AccountAddress, k_bytes: &[u8], k_tag_bytes: &[u8]) -> [u8; 32] {
    let mut hasher = Sha3_256::default();
    hasher.update(parent);
    hasher.update(k_bytes.len().to_le_bytes());  // length delimiter
    hasher.update(k_bytes);
    hasher.update(k_tag_bytes.len().to_le_bytes());  // length delimiter
    hasher.update(k_tag_bytes);
    hasher.finalize()
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Hash computations concatenating variable-length fields without separators
- Custom hash_type_and_key implementations
- Dynamic field operations with complex type parameters
```

---

## 3. Package Digest Collision

### Overview

`compute_digest_for_modules_and_deps` computes a unique hash for Move packages, but missing padding between items allows hash collisions. Protocols relying on this hash for upgrade validation can be tricked.

> **Validation strength**: Strong — demonstrated with PoC by OtterSec
> **Frequency**: 1/69 reports (L1 upgrade security)

### Vulnerable Pattern Examples

**Example 1: Missing Padding in Digest** [HIGH]
> 📖 Reference: `reports/sui_move_findings/modules-digest-collision.md`
```rust
// ❌ VULNERABLE: Sorting and concatenating without item boundaries
pub fn compute_digest_for_modules_and_deps<'a>(
    modules: impl IntoIterator<Item = &'a Vec<u8>>,
    object_ids: impl IntoIterator<Item = &'a ObjectID>,
) -> [u8; 32] {
    let mut bytes: Vec<&[u8]> = modules.into_iter().map(|x| x.as_ref())
        .chain(object_ids.into_iter().map(|obj_id| obj_id.as_ref()))
        .collect();
    bytes.sort();
    let mut digest = DefaultHash::default();
    for b in bytes { digest.update(b); }
    digest.finalize().digest
    // digest([m1, m2]) == digest([m1 || m2]) — COLLISION!
}
```

### Secure Implementation

**Fix: Hash Each Item Independently Then Combine**
```rust
// ✅ SECURE: Hash each module individually, then hash the concatenation of hashes
pub fn compute_digest_for_modules_and_deps<'a>(...) -> [u8; 32] {
    let mut item_hashes: Vec<[u8; 32]> = modules.into_iter()
        .map(|m| { let mut h = DefaultHash::default(); h.update(m); h.finalize().digest })
        .collect();
    // ... similar for object_ids
    item_hashes.sort();
    let mut final_digest = DefaultHash::default();
    for h in item_hashes { final_digest.update(&h); }
    final_digest.finalize().digest
}
```

---

## 4. Object Size Limit DoS

### Overview

Sui enforces a maximum object size of 256,000 bytes. Creating data structures with excessive internal sizes (e.g., BigVector with max_slice_size=10000) can exceed this limit, causing runtime errors that prevent core protocol functions from operating.

> **Validation strength**: Moderate — 2 reports across DeepBook and Dipcoin
> **Frequency**: 2/69 reports

### Vulnerable Pattern Examples

**Example 1: BigVector Leaf Size Overflow** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/bigvector-size-overflow.md`
```move
// ❌ VULNERABLE: max_slice_size too large, leaf objects will exceed 256KB
public(package) fun empty(...): Book {
    Book {
        bids: big_vector::empty(64, 64, ctx),  // effective max_slice_size = 10000
        asks: big_vector::empty(64, 64, ctx),  // each leaf could be > 256KB
        // ...
    }
}
```

**Example 2: Dynamic Field Access Limit (1000 per TX)** [HIGH]
> 📖 Reference: `reports/sui_move_findings/denial-of-service-in-several-functions-due-to-object-limits.md`
```move
// ❌ VULNERABLE: Unbounded iteration over dynamic fields
fun distribute_funds(vault: &mut Vault) {
    let users = &vault.users;
    let i = 0;
    while (i < vector::length(users)) {
        let user = vector::borrow(users, i);
        // Two dynamic field accesses per user:
        let pos = vault.user_positions.borrow(*user);  // access 1
        bank.transfer(...);  // access 2
        i = i + 1;
    };
    // With 500+ users, exceeds 1000 dynamic field access limit → DoS
}
```

### Secure Implementation

**Fix 1: Reasonable BigVector Sizing**
```move
// ✅ SECURE: Use max_slice_size < 2000 to stay well under 256KB limit
public(package) fun empty(...): Book {
    Book {
        bids: big_vector::empty(1000, 1000, ctx),  // safe leaf size
        asks: big_vector::empty(1000, 1000, ctx),
    }
}
```

**Fix 2: Pull Pattern Instead of Push**
```move
// ✅ SECURE: Users claim their own funds (pull pattern)
public fun claim_closed_vault_funds(vault: &Vault, ctx: &mut TxContext) {
    assert!(vault.state == CLOSED, E_NOT_CLOSED);
    let user = tx_context::sender(ctx);
    let share = calculate_user_share(vault, user);
    // Single user, bounded dynamic field accesses
    transfer::public_transfer(coin::take(&mut vault.balance, share, ctx), user);
}
```

---

## 5. Kiosk Extension Fund Locking

### Overview

Sui's kiosk extensions depend on `uid_mut` function access. When `set_allow_extensions` is set to `false`, funds transferred to extensions become permanently locked because `uid_mut` aborts.

> **Validation strength**: Moderate — 1 report from OtterSec on Sui core
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Extension Disabled Locks Funds** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/blocking-user-funds-in-kiosk.md`
```move
// ❌ VULNERABLE: Disabling extensions locks user funds
public fun uid_mut(self: &mut Kiosk): &mut UID {
    assert!(self.allow_extensions, EExtensionsDisabled);
    &mut self.id  // If allow_extensions = false, funds are locked
}
```

### Secure Implementation

**Fix: Fallback Mechanism for Extension Termination**
```move
// ✅ SECURE: Allow extension termination to recover funds even when disabled
public fun terminate_extension(self: &mut Kiosk, ext_id: ID, ctx: &mut TxContext) {
    // Bypass allow_extensions check for cleanup operations
    let ext = dynamic_field::remove(&mut self.id, ext_id);
    // Return funds to extension owner
    transfer::public_transfer(ext.balance, tx_context::sender(ctx));
}
```

---

## 6. Missing UID Validation in DeFi

### Overview

Sui DeFi protocols often accept shared objects (banks, pools, oracles) as function parameters without verifying their identity. Attackers can substitute malicious or different instances to manipulate protocol behavior.

> **Validation strength**: Strong — 2 reports across BlueFin and Aftermath
> **Frequency**: 2/69 reports

### Detection Patterns

#### Code Patterns to Look For
```
- Functions accepting &mut Bank or &Pool without asserting object::id()
- Shared objects passed as parameters without cross-referencing stored IDs
- deposit/withdraw functions lacking bank_id validation
- Any function that trusts caller-provided shared objects without verification
```

---

## 7. Committee / Epoch Management Bugs

### Overview

Sui Bridge's committee management has critical ordering assumptions. The blocklist validation assumes matching order between Ethereum addresses and committee members, and duplicate public key registration can prevent new committee creation at epoch boundaries.

> **Validation strength**: Strong — 2 reports from OtterSec on Sui Bridge
> **Frequency**: 2/69 reports

### Vulnerable Pattern Examples

**Example 1: Blocklist Order Mismatch** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/blocklist-validation-order-mismatch.md`
```move
// ❌ VULNERABLE: member_idx not reset between iterations
public(friend) fun execute_blocklist(self: &mut BridgeCommittee, blocklist: Blocklist) {
    while (list_idx < list_len) {
        // member_idx carries over from previous iteration!
        while (member_idx < vec_map::size(&self.members)) {
            // ...
            member_idx = member_idx + 1;
        };
        assert!(found, EValidatorBlocklistContainsUnknownKey);
        list_idx = list_idx + 1;
        // BUG: member_idx is NOT reset to 0 here
    };
}
```

**Example 2: Duplicate PubKey Prevents Epoch Transition** [HIGH]
> 📖 Reference: `reports/sui_move_findings/inability-to-end-an-epoch.md`
```move
// ❌ VULNERABLE: vec_map::insert fails on duplicate bridge_pubkey_bytes
vec_map::insert(&mut new_members, registration.bridge_pubkey_bytes, member);
// If two validators register with same pubkey, epoch transition fails
```

### Secure Implementation

**Fix 1: Reset Iterator Index**
```move
// ✅ SECURE: Reset member_idx for each blocklist entry
while (list_idx < list_len) {
    let member_idx = 0;  // Reset each iteration
    while (member_idx < vec_map::size(&self.members)) { ... };
    list_idx = list_idx + 1;
};
```

**Fix 2: Prevent Duplicate Registration**
```move
// ✅ SECURE: Check for existing pubkey before registration
public fun register(pubkey: vector<u8>, ...) {
    assert!(!vec_map::contains(&existing_registrations, &pubkey), EDuplicatePubKey);
    // ... proceed with registration
}
```

---

## 8. Visibility / Ability Misuse via Upgrades

### Overview

Sui Move's `public` visibility and ability system can be exploited when functions or struct abilities are not properly restricted, especially across package versions.

> **Validation strength**: Strong — 3 reports from OtterSec on Mysten Labs Sui
> **Frequency**: 3/69 reports

### Vulnerable Pattern Examples

**Example 1: Public Function Allows Cooldown Bypass** [HIGH]
> 📖 Reference: `reports/sui_move_findings/arbitrary-update-of-last-epoch-mixed.md`
```move
// ❌ VULNERABLE: Public function allows arbitrary epoch manipulation
public fun suifren_update_last_epoch_mixed<T>(fren: &mut SuiFren<T>, epoch: u64) {
    fren.last_epoch_mixed = epoch;  // Anyone can bypass cooldown period
}
// Should be: public(friend) fun ...
```

**Example 2: Wrong Variable in Limit Check (Typo)** [HIGH]
> 📖 Reference: `reports/sui_move_findings/mixing-over-limit-suifrens.md`
```move
// ❌ VULNERABLE: Typo — borrows l1 instead of l2 for second SuiFren
if (option::is_none(&l2)) {
    set_limit(sf2, app.mixing_limit - 1);
} else {
    let limit = *option::borrow(&l1);  // BUG: should be &l2
    assert!(limit > 0, EReachedMixingLimit);
    set_limit(sf2, limit - 1);
};
```

### Detection Patterns

#### Code Patterns to Look For
```
- `public fun` on state-mutation functions that should be `public(friend)` or `public(package)`
- Package upgrades adding abilities (key, store) to existing structs
- Variable name typos in symmetric loop operations (l1/l2, sf1/sf2)
- Missing access control on admin-only functions
```

---

## 9. Name Service Validation Failures

### Overview

SuiNS (Sui Name Service) had validation gaps where TTL bounds and domain record fields returned incorrect values for certain domain types.

> **Validation strength**: Moderate — 2 reports from OtterSec
> **Frequency**: 2/69 reports

### Vulnerable Pattern Examples

**Example 1: Missing MAX_TTL Validation** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/absence-of-checks-for-max-ttl.md`
```move
// ❌ VULNERABLE: ttl not validated against MAX_TTL
public entry fun set_ttl(suins: &mut SuiNS, domain_name: vector<u8>, ttl: u64, ctx: &mut TxContext) {
    authorised(suins, domain_name, ctx);
    let record = get_name_record_mut(suins, domain_name);
    *entity::name_record_ttl_mut(record) = ttl;  // No MAX_TTL check!
}
```

**Example 2: Incorrect Return Value for Domain Records** [HIGH]
> 📖 Reference: `reports/sui_move_findings/incorrect-value-in-record-name.md`
```move
// ❌ VULNERABLE: Returns empty string for normal domains, unvalidated for reverse domains
public fun get_name_record_all_fields(suins: &SuiNS, domain_name: vector<u8>)
    -> (address, address, u64, String) {
    let name_record = get_name_record(suins, utf8(domain_name));
    // Returns name_record_default_domain_name without validation
    (owner, linked_addr, ttl, name_record_default_domain_name(name_record))
}
```

---

## 10. Dynamic Field Access Limit DoS

### Overview

Sui enforces a strict limit of 1,000 dynamic field accesses per transaction. Functions that iterate over unbounded collections of users/vaults using dynamic fields can easily hit this limit, causing denial of service.

> **Validation strength**: Strong — 1 report from Quantstamp on Dipcoin Vault
> **Frequency**: 1/69 reports (generalizable to all Sui DeFi)

### Detection Patterns

#### Audit Checklist
- [ ] Check for unbounded loops accessing dynamic fields
- [ ] Verify that batch operations have pagination or limits
- [ ] Ensure push-based distribution is replaced with pull-based claims
- [ ] Test with realistic user counts (500+) to verify gas/access limits
- [ ] Check `set_vault_config_operator` and similar admin functions for unbounded iteration

---

## Prevention Guidelines

### Development Best Practices
1. Always validate object UIDs when accepting shared objects as parameters
2. Use `public(package)` or `public(friend)` instead of `public` for state-mutation functions
3. Insert length delimiters in any custom hash computation
4. Keep BigVector `max_slice_size` well under 2000 (target: 256KB / max_entry_size)
5. Never add `key` ability to structs that were published without it
6. Use pull-based patterns instead of push-based fund distribution
7. Reset loop counters explicitly when iterating over multiple collections
8. Validate domain-specific bounds (TTL, limits) on all setter functions

### Testing Requirements
- Test cross-version module interactions during upgrades
- Fuzz dynamic field operations with adversarial type/key combinations
- Test with maximum object sizes and near-limit dynamic field counts
- Verify epoch transitions with adversarial committee registrations

---

### Keywords for Search

`sui`, `move`, `uid`, `object_id`, `dynamic_field`, `kiosk`, `bigvector`, `digest`, `collision`, `hash`, `id_leak_verifier`, `key_ability`, `uid_mut`, `set_allow_extensions`, `epoch`, `committee`, `blocklist`, `suins`, `ttl`, `max_slice_size`, `object_size`, `256KB`, `dynamic_field_access`, `1000_limit`, `package_upgrade`, `ability_addition`, `public_friend`, `public_package`, `suifren`, `mixing_limit`

### Related Vulnerabilities

- `DB/Solona-chain-specific/` — Solana program account validation patterns (similar object model issues)
- `DB/general/access-control/` — Generic access control patterns

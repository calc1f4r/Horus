---
# Core Classification (Required)
protocol: generic
chain: sui
category: access_control_validation
vulnerability_type: missing_access_control|visibility_misconfiguration|input_validation|role_mismanagement

# Attack Vector Details (Required)
attack_type: privilege_escalation|authorization_bypass|input_manipulation
affected_component: access_control|visibility|role_management|input_validation|owner_verification|zk_proof

# Technical Primitives (Required)
primitives:
  - public
  - public_friend
  - public_package
  - entry
  - owner_check
  - tx_context_sender
  - assert
  - uid_to_inner
  - object_id
  - blocklist
  - security_level
  - zk_proof
  - trade_proof
  - capability_pattern
  - admin_cap
  - flash_receipt

# Impact Classification (Required)
severity: high
impact: fund_loss|unauthorized_access|state_corruption|security_bypass
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - sui
  - move
  - access_control
  - authorization
  - visibility
  - validation
  - owner_check
  - role_management
  - flash_loan
  - zk_proof
  - trade_proof

# Version Info
language: move
version: all

# Pattern Identity (Required)
root_cause_family: missing_access_control
pattern_key: missing_access_control | access_control | missing_access_control

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - admin_cap
  - assert
  - blocklist
  - capability_pattern
  - claim_tokens
  - deposit
  - donate
  - emergency_withdraw
  - entry
  - finalize_snapshot_update
  - flash_receipt
  - gas
  - generate_proof_as_owner
  - generate_proof_as_trader
  - get_share_price
  - limit
  - match_orders
  - mint
  - object_id
  - open_position
---

## References & Source Reports

> **For Agents**: Read the full report for each finding at the referenced path.

### Visibility / Capability Bypass
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Arbitrary Update of Last Epoch Mixed | `reports/sui_move_findings/arbitrary-update-of-last-epoch-mixed.md` | HIGH | OtterSec | Mysten Labs Sui |
| Bypass ID Leak Verifier | `reports/sui_move_findings/bypass-id-leak-verifier.md` | HIGH | OtterSec | Mysten Labs Sui |

### Missing Owner / Object Validation
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Missing Owner Check | `reports/sui_move_findings/missing-owner-check.md` | HIGH | OtterSec | Aftermath Finance |
| Missing UID Validation | `reports/sui_move_findings/missing-uid-validation.md` | HIGH | OtterSec | BlueFin |
| Missing Invariant Checks | `reports/sui_move_findings/missing-invariant-checks.md` | HIGH | OtterSec | Aftermath Finance |

### Role Management / Authorization
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Unsafe Role Removal | `reports/sui_move_findings/unsafe-role-removal.md` | MEDIUM | OtterSec | Cetus |
| Security Level Constraint Circumvented | `reports/sui_move_findings/security-level-constraint-can-be-circumvented.md` | HIGH | Quantstamp | Bucket Protocol V2 |

### Proof / Receipt Bypass
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Trade Proof Bypass | `reports/sui_move_findings/trade-proof-bypass.md` | HIGH | OtterSec | DeepBook V3 |
| Missing On-Chain ZK Proof Verification | `reports/sui_move_findings/missing-on-chain-zk-proof-verification.md` | HIGH | Quantstamp | Dipcoin Perpetual |
| Loss of Coin (Flash Loan Receipt Mismatch) | `reports/sui_move_findings/loss-of-coin.md` | HIGH | OtterSec | Cetus |
| Repeated Invocation Resulting in Excess Claims | `reports/sui_move_findings/repeated-invocation-resulting-in-excessive-claims.md` | HIGH | OtterSec | Security Token |

### Signature / Cryptographic Validation
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Signature Length Validation | `reports/sui_move_findings/signature-length-validation.md` | HIGH | OtterSec | BlueFin |
| Risk of Compromising Snapshot Integrity | `reports/sui_move_findings/risk-of-compromising-snapshot-integrity.md` | MEDIUM | OtterSec | Security Token |

### Input Validation
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Absence of Checks for Max TTL | `reports/sui_move_findings/absence-of-checks-for-max-ttl.md` | MEDIUM | OtterSec | Mysten Labs Sui |
| Missing Tick Step Validation | `reports/sui_move_findings/missing-tick-step-validation.md` | MEDIUM | OtterSec | Turbos Finance |
| Inconsistent Assert Statement | `reports/sui_move_findings/inconsistent-assert-statement.md` | HIGH | OtterSec | BlueFin |

### DoS via Access Control Issues
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Denial of Service via Mint Limit Exhaustion | `reports/sui_move_findings/denial-of-service-via-mint-limit-exhaustion.md` | MEDIUM | OtterSec | Lombard |
| Denial of Service Due to Excessive Gas | `reports/sui_move_findings/denial-of-service-due-to-excessive-gas-consumption.md` | MEDIUM | OtterSec | DeepBook V3 |
| Blocking User Funds in Kiosk | `reports/sui_move_findings/blocking-user-funds-in-kiosk.md` | MEDIUM | OtterSec | Mysten Labs Sui |

### Artifacts Index
| Artifact | Source | Type |
|----------|--------|------|
| `artifacts/1-certificate.quantstamp.com-full-report-2.html` | Quantstamp Dipcoin Perpetual | HTML |
| `artifacts/3-certificate.quantstamp.com-full-report-4.html` | Quantstamp Dipcoin Vault | HTML |
| `artifacts/8-certificate.quantstamp.com-full-report-3.html` | Quantstamp Bucket V2 | HTML |
| `artifacts/9-github.com-AftermathFinance-aftermath-core-.html` | Aftermath Finance GitHub | HTML |

---

# Sui Move Access Control & Validation Vulnerabilities — Comprehensive Database

**A Complete Pattern-Matching Guide for Authorization, Visibility, and Input Validation in Sui/Move**

---

## Table of Contents

1. [Public vs Public(package) Visibility Misuse](#1-public-vs-publicpackage-visibility-misuse)
2. [Missing Owner/Authority Check](#2-missing-ownerauthority-check)
3. [Missing Object UID/ID Validation](#3-missing-object-uidid-validation)
4. [Trade Proof / Capability Bypass](#4-trade-proof--capability-bypass)
5. [Flash Loan Receipt Manipulation](#5-flash-loan-receipt-manipulation)
6. [Missing ZK Proof Verification](#6-missing-zk-proof-verification)
7. [Signature Length / Format Validation](#7-signature-length--format-validation)
8. [Security Level Constraint Bypass](#8-security-level-constraint-bypass)
9. [Unsafe Role Removal](#9-unsafe-role-removal)
10. [Repeated Invocation / Replay](#10-repeated-invocation--replay)
11. [Inconsistent Assert Conditions](#11-inconsistent-assert-conditions)
12. [Missing Range / Bounds Validation](#12-missing-range--bounds-validation)
13. [Mint Limit Exhaustion DoS](#13-mint-limit-exhaustion-dos)
14. [Excessive Gas Consumption DoS](#14-excessive-gas-consumption-dos)
15. [Snapshot Integrity Bypass](#15-snapshot-integrity-bypass)
16. [Missing Invariant Enforcement](#16-missing-invariant-enforcement)
17. [Blocklist Implementation Flaws](#17-blocklist-implementation-flaws)
18. [Price Manipulation via Missing Guards](#18-price-manipulation-via-missing-guards)

---

## 1. Public vs Public(package) Visibility Misuse

### Overview

Sui Move's visibility modifiers (`public`, `public(friend)`, `public(package)`, `entry`) control who can call functions. Using `public` when `public(package)` is intended allows any module to call state-mutation functions.

> **Validation strength**: Strong — 1 report from OtterSec on Sui Core + generalizable
> **Frequency**: 1/69 reports explicitly, but underlying pattern is systemic



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of missing_access_control"
- Pattern key: `missing_access_control | access_control | missing_access_control`
- Interaction scope: `single_contract`
- Primary affected component(s): `access_control|visibility|role_management|input_validation|owner_verification|zk_proof`
- High-signal code keywords: `admin_cap`, `assert`, `blocklist`, `capability_pattern`, `claim_tokens`, `deposit`, `donate`, `emergency_withdraw`
- Typical sink / impact: `fund_loss|unauthorized_access|state_corruption|security_bypass`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `access_control.function -> input_validation.function -> owner_verification.function`
- Trust boundary crossed: `internal`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: A state-changing `public` or `entry` function mutates protocol objects without requiring an `AdminCap`, owner object, signer-derived address, or package-only visibility.
- Signal 2: Object identity checks compare only type or shape, not the expected `UID`, parent object, owner, pool ID, market ID, or epoch-scoped authority.
- Signal 3: Proof, receipt, or capability objects can be reused, forged across contexts, or consumed without binding to caller, amount, market, nonce, or action.
- Signal 4: Role removal, security-level changes, blocklist updates, snapshot changes, or mint-limit state can be changed into an unsafe state by a non-governance caller.

#### False Positive Guards

- Not this bug when: The callable function only operates on caller-owned objects and cannot mutate shared protocol state or mint/burn/withdraw assets.
- Safe if: Authority is enforced by unforgeable capability objects, `tx_context::sender(ctx)` checks, `public(package)` visibility, and exact object ID/owner validation at the mutation site.
- Requires attacker control of: a transaction that can pass arbitrary shared objects, receipts, proofs, role targets, or user-owned objects into the vulnerable entry function.

#### Code Patterns to Look For

```text
- public/entry functions mutating Pool, Vault, Market, Role, Blocklist, Snapshot, Treasury, or Config objects without capability arguments
- assert!(object::id(obj) == expected_id) missing before using shared or dynamic-field objects
- proof/receipt structs lacking consumed flags, nonce binding, or caller/market/amount fields
- role removal paths that allow removing the last admin, bypassing timelocks, or downgrading security levels
- limits, TTLs, tick steps, mint caps, or gas bounds accepted without explicit range checks
```

### Vulnerability Description

#### Root Cause

Functions that modify protocol-critical state (cooldown periods, limits, prices) are declared `public` instead of `public(package)` or `public(friend)`, allowing external modules to call them directly.

### Vulnerable Pattern Examples

**Example 1: SuiFren Cooldown Bypass** [HIGH]
> 📖 Reference: `reports/sui_move_findings/arbitrary-update-of-last-epoch-mixed.md`
```move
// ❌ VULNERABLE: Public function allows anyone to reset cooldown
public fun suifren_update_last_epoch_mixed<T>(fren: &mut SuiFren<T>, epoch: u64) {
    fren.last_epoch_mixed = epoch;
    // Any external module can call this to bypass mixing cooldown
}
```

### Secure Implementation

```move
// ✅ SECURE: Restrict to same package only
public(package) fun suifren_update_last_epoch_mixed<T>(fren: &mut SuiFren<T>, epoch: u64) {
    fren.last_epoch_mixed = epoch;
}
```

### Detection Patterns

```
- `public fun` on functions that mutate critical state fields
- Functions accepting &mut on shared objects without capability parameters
- State-modification functions callable by anyone (no AdminCap parameter)
- Functions that update prices, rates, limits, cooldowns
```

---

## 2. Missing Owner/Authority Check

### Overview

Functions that should only be callable by the owner of an object or a specific authority lack proper `tx_context::sender()` validation. This allows unauthorized users to operate on others' assets.

> **Validation strength**: Strong — 1 report from OtterSec on Aftermath Finance
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: No Owner Check on Farming Position** [HIGH]
> 📖 Reference: `reports/sui_move_findings/missing-owner-check.md`
```move
// ❌ VULNERABLE: Anyone can withdraw from another user's farming position
public entry fun unstake_and_withdraw<CoinType>(
    farming: &mut Farming,
    position: &mut FarmingPosition,  // Shared object — no owner check
    amount: u64,
    ctx: &mut TxContext
) {
    // Missing: assert!(farming_position::owner(position) == tx_context::sender(ctx), E_NOT_OWNER);
    let coin = farming::unstake(farming, position, amount, ctx);
    transfer::public_transfer(coin, tx_context::sender(ctx));
    // Attacker withdraws victim's farming position to attacker's address
}
```

### Secure Implementation

```move
// ✅ SECURE: Validate caller is position owner
public entry fun unstake_and_withdraw<CoinType>(
    farming: &mut Farming,
    position: &mut FarmingPosition,
    amount: u64,
    ctx: &mut TxContext
) {
    assert!(farming_position::owner(position) == tx_context::sender(ctx), E_NOT_OWNER);
    let coin = farming::unstake(farming, position, amount, ctx);
    transfer::public_transfer(coin, tx_context::sender(ctx));
}
```

### Detection Patterns

```
- entry/public entry functions accepting &mut SharedObject without sender check
- Functions operating on user positions without ownership validation
- transfer::public_transfer to tx_context::sender without prior owner assertion
- Withdraw/unstake/claim functions on shared objects
```

---

## 3. Missing Object UID/ID Validation

### Overview

When Sui DeFi protocols accept multiple shared objects as function parameters (e.g., a bank and a vault), they must validate that the objects match expected relationships. Without validation, attackers can substitute different object instances.

> **Validation strength**: Strong — 2 reports across BlueFin and Aftermath
> **Frequency**: 2/69 reports

### Vulnerable Pattern Examples

**Example 1: Bank Object Not Validated Against Vault** [HIGH]
> 📖 Reference: `reports/sui_move_findings/missing-uid-validation.md`
```move
// ❌ VULNERABLE: BlueFin accepts any BankV2 — doesn't check it matches the vault
entry fun deposit_to_vault<USDC>(
    bluefin_bank: &mut BluefinBank<USDC>,  // Could be ANY bank instance
    vault: &mut Vault<USDC>,
    coin: &mut Coin<USDC>,
    amount: u64,
    ctx: &mut TxContext
) {
    // Checks perpetual_id but NOT bank identity
    assert!(vault.perpetual_id == expected_id, E_WRONG_PERP);
    // Missing: assert!(object::id(bluefin_bank) == vault.bank_id, E_WRONG_BANK);
    
    bank::deposit(bluefin_bank, coin, amount);
    // If attacker passes their own bank, deposit goes to wrong bank
}
```

### Secure Implementation

```move
// ✅ SECURE: Validate all shared object identities
entry fun deposit_to_vault<USDC>(
    bluefin_bank: &mut BluefinBank<USDC>,
    vault: &mut Vault<USDC>,
    coin: &mut Coin<USDC>,
    amount: u64,
    ctx: &mut TxContext
) {
    // Validate bank matches vault's expected bank
    assert!(object::id(bluefin_bank) == vault.bank_id, E_WRONG_BANK);
    assert!(vault.perpetual_id == expected_id, E_WRONG_PERP);
    
    bank::deposit(bluefin_bank, coin, amount);
}
```

---

## 4. Trade Proof / Capability Bypass

### Overview

DeepBook V3 uses `TradeProof` as a capability to authorize trades. However, the proof can be generated through an alternative path (`generate_proof_as_owner`) that bypasses the intended `BalanceManager` authorization flow.

> **Validation strength**: Strong — 1 report from OtterSec on DeepBook V3
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: TradeProof Generation Bypass** [HIGH]
> 📖 Reference: `reports/sui_move_findings/trade-proof-bypass.md`
```move
// ❌ VULNERABLE: Alternative proof generation path bypasses trader authorization
public fun generate_proof_as_owner(balance_manager: &mut BalanceManager, ctx: &TxContext): TradeProof {
    // Only checks ownership, not trader authorization
    assert!(object::uid_to_inner(&balance_manager.id) == balance_manager.owner, E_NOT_OWNER);
    TradeProof { balance_manager_id: object::uid_to_inner(&balance_manager.id), trader: tx_context::sender(ctx) }
    // This bypasses check_trader() and trade_cap validation
}

// Normal path with proper checks:
public fun generate_proof_as_trader(balance_manager: &mut BalanceManager, trade_cap: &TradeCap): TradeProof {
    check_trader(balance_manager, trade_cap);  // Validates trader authorization
    TradeProof { ... }
}
```

### Secure Implementation

```move
// ✅ SECURE: Both paths should enforce the same authorization
public fun generate_proof_as_owner(balance_manager: &mut BalanceManager, ctx: &TxContext): TradeProof {
    assert!(balance_manager.owner == tx_context::sender(ctx), E_NOT_OWNER);
    // Apply same restrictions as trader path
    assert!(balance_manager.trade_params_match(ctx), E_TRADE_RESTRICTED);
    TradeProof { ... }
}
```

---

## 5. Flash Loan Receipt Manipulation

### Overview

Flash loan protocols issue receipts that must be returned to confirm repayment. If the receipt validation doesn't match the exact pool/coin that issued the flash loan, attackers can repay to a different pool.

> **Validation strength**: Strong — 1 report from OtterSec on Cetus
> **Frequency**: 1/69 reports (common DeFi pattern)

### Vulnerable Pattern Examples

**Example 1: Flash Loan Receipt Pool Mismatch** [HIGH]
> 📖 Reference: `reports/sui_move_findings/loss-of-coin.md`
```move
// ❌ VULNERABLE: Receipt doesn't bind to specific pool
struct FlashReceipt has key, store {
    amount: u64,
    fee: u64,
    // Missing: pool_id to identify which pool issued the loan
}

public fun repay_flash_loan<CoinA, CoinB>(
    pool: &mut Pool<CoinA, CoinB>,
    receipt: FlashReceipt,
    payment: Coin<CoinA>,
) {
    let FlashReceipt { amount, fee } = receipt;
    assert!(coin::value(&payment) >= amount + fee, E_INSUFFICIENT);
    // Accepts repayment to ANY pool — borrower can repay to cheaper pool
    balance::join(&mut pool.balance_a, coin::into_balance(payment));
}
```

### Secure Implementation

```move
// ✅ SECURE: Receipt binds to specific pool
struct FlashReceipt has key, store {
    pool_id: ID,  // Bind to originating pool
    amount: u64,
    fee: u64,
}

public fun repay_flash_loan<CoinA, CoinB>(
    pool: &mut Pool<CoinA, CoinB>,
    receipt: FlashReceipt,
    payment: Coin<CoinA>,
) {
    let FlashReceipt { pool_id, amount, fee } = receipt;
    assert!(pool_id == object::id(pool), E_WRONG_POOL);  // Enforce same pool
    assert!(coin::value(&payment) >= amount + fee, E_INSUFFICIENT);
    balance::join(&mut pool.balance_a, coin::into_balance(payment));
}
```

---

## 6. Missing ZK Proof Verification

### Overview

Some Sui DeFi protocols use ZK proofs for off-chain computation verification. If on-chain verification is omitted (relying solely on off-chain checks), the proofs provide no security guarantees.

> **Validation strength**: Moderate — 1 report from Quantstamp on Dipcoin
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: No On-Chain ZK Proof Validation** [HIGH]
> 📖 Reference: `reports/sui_move_findings/missing-on-chain-zk-proof-verification.md`
```move
// ❌ VULNERABLE: ZK proof accepted without on-chain verification
public entry fun settle_perpetual(
    perp: &mut Perpetual,
    proof: vector<u8>,  // ZK proof passed but never verified
    settlement_data: SettlementData,
    ctx: &mut TxContext
) {
    // Missing: verify_zk_proof(&proof, &settlement_data)
    apply_settlement(perp, settlement_data);
    // Attacker submits fake proof with arbitrary settlement data
}
```

### Secure Implementation

```move
// ✅ SECURE: Verify ZK proof on-chain before applying state changes
public entry fun settle_perpetual(
    perp: &mut Perpetual,
    proof: vector<u8>,
    settlement_data: SettlementData,
    verifying_key: &VerifyingKey,
    ctx: &mut TxContext
) {
    // Verify proof on-chain using the Move-native verifier
    let public_inputs = settlement_data_to_public_inputs(&settlement_data);
    assert!(groth16::verify(verifying_key, &proof, &public_inputs), E_INVALID_PROOF);
    apply_settlement(perp, settlement_data);
}
```

---

## 7. Signature Length / Format Validation

### Overview

Signature validation must check not only the content but also the length and format of the signature bytes. Missing length checks allow malformed signatures to pass validation or cause unexpected behavior.

> **Validation strength**: Moderate — 1 report from OtterSec on BlueFin
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Missing Signature Length Check** [HIGH]
> 📖 Reference: `reports/sui_move_findings/signature-length-validation.md`
```move
// ❌ VULNERABLE: No length validation on signature bytes
public fun verify_signature(
    message: vector<u8>,
    signature: vector<u8>,
    public_key: vector<u8>
) {
    // Missing: assert!(vector::length(&signature) == 64, E_INVALID_SIG_LENGTH);
    // Missing: assert!(vector::length(&public_key) == 32, E_INVALID_KEY_LENGTH);
    let valid = ed25519::ed25519_verify(&signature, &public_key, &message);
    assert!(valid, E_INVALID_SIGNATURE);
    // Malformed signatures may cause unpredictable behavior in the verifier
}
```

### Secure Implementation

```move
// ✅ SECURE: Validate signature and key lengths before verification
public fun verify_signature(
    message: vector<u8>,
    signature: vector<u8>,
    public_key: vector<u8>
) {
    assert!(vector::length(&signature) == 64, E_INVALID_SIG_LENGTH);
    assert!(vector::length(&public_key) == 32, E_INVALID_KEY_LENGTH);
    let valid = ed25519::ed25519_verify(&signature, &public_key, &message);
    assert!(valid, E_INVALID_SIGNATURE);
}
```

---

## 8. Security Level Constraint Bypass

### Overview

Protocols implementing tiered security levels (e.g., different withdrawal limits per level) can have their constraints bypassed if the level-checking logic has gaps.

> **Validation strength**: Moderate — 1 report from Quantstamp on Bucket Protocol V2
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Security Level Check Bypass** [HIGH]
> 📖 Reference: `reports/sui_move_findings/security-level-constraint-can-be-circumvented.md`
```move
// ❌ VULNERABLE: Security level check can be bypassed via alternative code path
public fun withdraw(vault: &mut Vault, amount: u64, ctx: &mut TxContext) {
    let user = tx_context::sender(ctx);
    let level = get_security_level(vault, user);
    // Check only applies to SOME withdrawal paths
    if (amount > get_limit_for_level(level)) {
        abort E_EXCEEDS_LIMIT
    };
    // ...
}

// But this function has no security level check:
public fun emergency_withdraw(vault: &mut Vault, ctx: &mut TxContext) {
    // Missing: security level constraint
    let amount = get_full_balance(vault, tx_context::sender(ctx));
    // Allows unlimited withdrawal regardless of security level
}
```

### Secure Implementation

```move
// ✅ SECURE: Enforce security level on ALL withdrawal paths
fun check_security_level(vault: &Vault, user: address, amount: u64) {
    let level = get_security_level(vault, user);
    assert!(amount <= get_limit_for_level(level), E_EXCEEDS_LIMIT);
}

public fun withdraw(vault: &mut Vault, amount: u64, ctx: &mut TxContext) {
    check_security_level(vault, tx_context::sender(ctx), amount);
    // ...
}

public fun emergency_withdraw(vault: &mut Vault, ctx: &mut TxContext) {
    let amount = get_full_balance(vault, tx_context::sender(ctx));
    check_security_level(vault, tx_context::sender(ctx), amount);
    // ...
}
```

---

## 9. Unsafe Role Removal

### Overview

Role/access control removal functions that don't properly validate the role being removed can allow users to remove roles they shouldn't have access to, or remove the last admin.

> **Validation strength**: Moderate — 1 report from OtterSec on Cetus
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Unsafe Member Removal from ACL** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/unsafe-role-removal.md`
```move
// ❌ VULNERABLE: Can remove any member, including the last admin
public fun remove_member(acl: &mut ACL, member: address, ctx: &mut TxContext) {
    assert!(is_admin(acl, tx_context::sender(ctx)), E_NOT_ADMIN);
    // Missing: assert!(member != last_admin(acl), E_CANNOT_REMOVE_LAST_ADMIN);
    // Missing: assert!(member != tx_context::sender(ctx), E_CANNOT_REMOVE_SELF);
    vec_set::remove(&mut acl.members, &member);
}
```

### Secure Implementation

```move
// ✅ SECURE: Prevent removing last admin and validate member exists
public fun remove_member(acl: &mut ACL, member: address, ctx: &mut TxContext) {
    let sender = tx_context::sender(ctx);
    assert!(is_admin(acl, sender), E_NOT_ADMIN);
    assert!(vec_set::size(&acl.admins) > 1 || !is_admin(acl, member), E_LAST_ADMIN);
    assert!(vec_set::contains(&acl.members, &member), E_NOT_MEMBER);
    vec_set::remove(&mut acl.members, &member);
}
```

---

## 10. Repeated Invocation / Replay

### Overview

Functions that grant claims, rewards, or minting rights can be called repeatedly if there's no mechanism to track whether a user has already claimed.

> **Validation strength**: Moderate — 1 report from OtterSec on Security Token
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Repeated Claim Without Tracking** [HIGH]
> 📖 Reference: `reports/sui_move_findings/repeated-invocation-resulting-in-excessive-claims.md`
```move
// ❌ VULNERABLE: No tracking of whether user already claimed
public entry fun claim_tokens(
    distribution: &mut Distribution,
    amount: u64,
    ctx: &mut TxContext
) {
    let user = tx_context::sender(ctx);
    assert!(is_eligible(distribution, user), E_NOT_ELIGIBLE);
    // Missing: assert!(!has_claimed(distribution, user), E_ALREADY_CLAIMED);
    let coin = coin::take(&mut distribution.balance, amount, ctx);
    transfer::public_transfer(coin, user);
    // Missing: mark_claimed(distribution, user);
    // User can call repeatedly to drain all tokens
}
```

### Secure Implementation

```move
// ✅ SECURE: Track claims and prevent replay
public entry fun claim_tokens(
    distribution: &mut Distribution,
    amount: u64,
    ctx: &mut TxContext
) {
    let user = tx_context::sender(ctx);
    assert!(is_eligible(distribution, user), E_NOT_ELIGIBLE);
    assert!(!table::contains(&distribution.claimed, user), E_ALREADY_CLAIMED);
    let coin = coin::take(&mut distribution.balance, amount, ctx);
    transfer::public_transfer(coin, user);
    table::add(&mut distribution.claimed, user, true);
}
```

---

## 11. Inconsistent Assert Conditions

### Overview

Assert statements that use wrong comparison operators or reference wrong variables fail to enforce the intended invariant.

> **Validation strength**: Moderate — 1 report from OtterSec on BlueFin
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Wrong Comparison Direction** [HIGH]
> 📖 Reference: `reports/sui_move_findings/inconsistent-assert-statement.md`
```move
// ❌ VULNERABLE: Assert condition is inverted
public fun update_margin(position: &mut Position, margin: u64) {
    let min_margin = calculate_min_margin(position);
    // BUG: Should be margin >= min_margin
    assert!(margin <= min_margin, E_BELOW_MIN_MARGIN);
    // This actually PREVENTS valid margins and ALLOWS invalid ones
    position.margin = margin;
}
```

### Secure Implementation

```move
// ✅ SECURE: Correct comparison direction
public fun update_margin(position: &mut Position, margin: u64) {
    let min_margin = calculate_min_margin(position);
    assert!(margin >= min_margin, E_BELOW_MIN_MARGIN);
    position.margin = margin;
}
```

---

## 12. Missing Range / Bounds Validation

### Overview

Numeric parameters (TTL, tick indices, amounts) must be validated against protocol-defined bounds. Missing validation allows out-of-range values that corrupt protocol state.

> **Validation strength**: Moderate — 2 reports from OtterSec
> **Frequency**: 2/69 reports

### Vulnerable Pattern Examples

**Example 1: Missing TTL Upper Bound** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/absence-of-checks-for-max-ttl.md`
```move
// ❌ VULNERABLE: TTL not checked against maximum
public entry fun set_ttl(suins: &mut SuiNS, domain: vector<u8>, ttl: u64, ctx: &mut TxContext) {
    authorised(suins, domain, ctx);
    let record = get_name_record_mut(suins, domain);
    *entity::name_record_ttl_mut(record) = ttl;
    // Missing: assert!(ttl <= MAX_TTL, E_TTL_TOO_HIGH);
}
```

**Example 2: Missing Tick Step Validation** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/missing-tick-step-validation.md`
```move
// ❌ VULNERABLE: Tick index not validated against tick spacing
public fun open_position(pool: &mut Pool, tick_lower: i32, tick_upper: i32) {
    // Missing: assert!(tick_lower % pool.tick_spacing == 0, E_INVALID_TICK);
    // Missing: assert!(tick_upper % pool.tick_spacing == 0, E_INVALID_TICK);
    // Invalid ticks create positions at non-standard price points
}
```

### Secure Implementation

```move
// ✅ SECURE: Validate all bounds
public entry fun set_ttl(suins: &mut SuiNS, domain: vector<u8>, ttl: u64, ctx: &mut TxContext) {
    authorised(suins, domain, ctx);
    assert!(ttl <= MAX_TTL, E_TTL_TOO_HIGH);
    let record = get_name_record_mut(suins, domain);
    *entity::name_record_ttl_mut(record) = ttl;
}

public fun open_position(pool: &mut Pool, tick_lower: i32, tick_upper: i32) {
    assert!(tick_lower % pool.tick_spacing == 0, E_INVALID_TICK);
    assert!(tick_upper % pool.tick_spacing == 0, E_INVALID_TICK);
    assert!(tick_lower < tick_upper, E_TICK_ORDER);
    assert!(tick_lower >= MIN_TICK && tick_upper <= MAX_TICK, E_TICK_RANGE);
    // ...
}
```

---

## 13. Mint Limit Exhaustion DoS

### Overview

Protocols with per-epoch or per-period mint limits can be attacked by minting small amounts repeatedly to exhaust the limit, preventing legitimate users from minting.

> **Validation strength**: Moderate — 1 report from OtterSec on Lombard
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Mint Limit Griefing** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/denial-of-service-via-mint-limit-exhaustion.md`
```move
// ❌ VULNERABLE: No minimum mint amount, attacker can exhaust limit with dust
public entry fun mint(treasury: &mut Treasury, amount: u64, ctx: &mut TxContext) {
    assert!(treasury.minted_this_epoch + amount <= treasury.epoch_limit, E_LIMIT_REACHED);
    // Missing: assert!(amount >= MIN_MINT_AMOUNT, E_DUST_MINT);
    treasury.minted_this_epoch = treasury.minted_this_epoch + amount;
    let coin = coin::mint(&mut treasury.cap, amount, ctx);
    transfer::public_transfer(coin, tx_context::sender(ctx));
}
```

### Secure Implementation

```move
// ✅ SECURE: Enforce minimum mint amount
const MIN_MINT_AMOUNT: u64 = 1_000_000;  // Minimum 1 token (6 decimals)

public entry fun mint(treasury: &mut Treasury, amount: u64, ctx: &mut TxContext) {
    assert!(amount >= MIN_MINT_AMOUNT, E_DUST_MINT);
    assert!(treasury.minted_this_epoch + amount <= treasury.epoch_limit, E_LIMIT_REACHED);
    treasury.minted_this_epoch = treasury.minted_this_epoch + amount;
    let coin = coin::mint(&mut treasury.cap, amount, ctx);
    transfer::public_transfer(coin, tx_context::sender(ctx));
}
```

---

## 14. Excessive Gas Consumption DoS

### Overview

Functions that perform unbounded work (large loops, many dynamic field accesses) in a single transaction can exceed Sui's gas limit, causing denial of service.

> **Validation strength**: Moderate — 1 report from OtterSec on DeepBook V3
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Matching Loop Without Gas Limit** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/denial-of-service-due-to-excessive-gas-consumption.md`
```move
// ❌ VULNERABLE: Order matching loop can process unlimited orders
public fun match_orders(book: &mut OrderBook, incoming: Order) {
    while (!is_empty(&book.best_bid)) {
        let best = pop_best_bid(book);
        fill(incoming, best);
        // No limit on iterations — can process thousands of orders
        // Exceeds gas limit → transaction fails → legitimate trades blocked
    };
}
```

### Secure Implementation

```move
// ✅ SECURE: Limit matching iterations per transaction
const MAX_FILLS_PER_TX: u64 = 100;

public fun match_orders(book: &mut OrderBook, incoming: &mut Order): u64 {
    let fills = 0u64;
    while (!is_empty(&book.best_bid) && fills < MAX_FILLS_PER_TX && incoming.remaining > 0) {
        let best = pop_best_bid(book);
        fill(incoming, best);
        fills = fills + 1;
    };
    fills
}
```

---

## 15. Snapshot Integrity Bypass

### Overview

Snapshot-based systems (e.g., for airdrops or governance) rely on cryptographic commitments. If the snapshot root can be updated without proper authorization, all claims can be manipulated.

> **Validation strength**: Moderate — 1 report from OtterSec on Security Token
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Snapshot Root Update Without Multi-sig** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/risk-of-compromising-snapshot-integrity.md`
```move
// ❌ VULNERABLE: Single admin can override snapshot root
public entry fun update_snapshot_root(
    admin: &AdminCap,
    distribution: &mut Distribution,
    new_root: vector<u8>
) {
    distribution.merkle_root = new_root;
    // Single point of failure — compromised admin can redirect all claims
}
```

### Secure Implementation

```move
// ✅ SECURE: Require multi-sig or time-locked update
public entry fun propose_snapshot_update(
    admin: &AdminCap,
    distribution: &mut Distribution,
    new_root: vector<u8>,
    clock: &Clock,
) {
    distribution.pending_root = new_root;
    distribution.pending_root_activation = clock::timestamp_ms(clock) + TIMELOCK_PERIOD;
}

public entry fun finalize_snapshot_update(distribution: &mut Distribution, clock: &Clock) {
    assert!(clock::timestamp_ms(clock) >= distribution.pending_root_activation, E_TIMELOCK);
    distribution.merkle_root = distribution.pending_root;
}
```

---

## 16. Missing Invariant Enforcement

### Overview

DeFi protocols must maintain key invariants (e.g., total supply == sum of all balances). When state-mutation functions don't assert these invariants, bugs can silently corrupt state.

> **Validation strength**: Strong — 1 report from OtterSec on Aftermath Finance
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Missing Supply Invariant Check** [HIGH]
> 📖 Reference: `reports/sui_move_findings/missing-invariant-checks.md`
```move
// ❌ VULNERABLE: LP supply not validated after swap
public fun swap(pool: &mut Pool, coin_in: Coin<A>): Coin<B> {
    let amount_in = coin::value(&coin_in);
    let amount_out = calculate_swap_output(pool, amount_in);
    balance::join(&mut pool.reserve_a, coin::into_balance(coin_in));
    let coin_out = coin::take(&mut pool.reserve_b, amount_out, ctx);
    // Missing: assert invariant k = reserve_a * reserve_b (constant product)
    coin_out
}
```

### Secure Implementation

```move
// ✅ SECURE: Assert invariant after state mutation
public fun swap(pool: &mut Pool, coin_in: Coin<A>, ctx: &mut TxContext): Coin<B> {
    let k_before = (balance::value(&pool.reserve_a) as u128) * (balance::value(&pool.reserve_b) as u128);
    
    let amount_in = coin::value(&coin_in);
    let amount_out = calculate_swap_output(pool, amount_in);
    balance::join(&mut pool.reserve_a, coin::into_balance(coin_in));
    let coin_out = coin::take(&mut pool.reserve_b, amount_out, ctx);
    
    let k_after = (balance::value(&pool.reserve_a) as u128) * (balance::value(&pool.reserve_b) as u128);
    assert!(k_after >= k_before, E_INVARIANT_VIOLATED);
    coin_out
}
```

---

## 17. Blocklist Implementation Flaws

### Overview

Bridge and compliance systems use blocklists to prevent sanctioned addresses from transacting. Implementation bugs (like iterator state not being reset) can cause incorrect blocklist enforcement.

> **Validation strength**: Strong — 1 report from OtterSec on Sui Bridge
> **Frequency**: 1/69 reports
> See also: Object Model Vulnerabilities entry for full details

---

## 18. Price Manipulation via Missing Guards

### Overview

DeFi protocols that allow donation or direct balance modification without corresponding share/state updates enable price manipulation attacks.

> **Validation strength**: Moderate — 1 report from OtterSec on Aftermath Finance
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Direct Pool Balance Donation** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/price-manipulation.md`
```move
// ❌ VULNERABLE: Pool NAV manipulated by direct coin transfer
public fun donate(pool: &mut Pool, coin: Coin<SUI>) {
    balance::join(&mut pool.reserve, coin::into_balance(coin));
    // NAV increases but total LP shares unchanged → price manipulated
    // Affects all downstream calculations using pool.reserve / pool.total_shares
}
```

### Secure Implementation

```move
// ✅ SECURE: Track "virtual" balance separately from actual balance
struct Pool has key, store {
    actual_balance: Balance<SUI>,
    accounted_balance: u64,  // Only updated by protocol operations
    total_shares: u64,
}

public fun get_share_price(pool: &Pool): u128 {
    (pool.accounted_balance as u128) * PRECISION / (pool.total_shares as u128)
    // Uses accounted_balance, immune to donation attacks
}
```

---

## Prevention Guidelines

### Sui-Specific Access Control Best Practices
1. Always use `public(package)` for internal state-mutation functions
2. Validate object UIDs when accepting shared objects as parameters
3. Use the Capability pattern (AdminCap, TradeCap) for privileged operations
4. Bind flash loan receipts to the specific pool/coin that issued them
5. Track claims/invocations to prevent replay attacks
6. Enforce minimum amounts to prevent limit-exhaustion griefing
7. Assert key invariants after every state mutation
8. Validate signature lengths before calling verification functions
9. Use multi-sig or timelocks for critical parameter updates
10. Limit loop iterations per transaction to prevent gas DoS

### Testing Requirements
- Test all functions with unauthorized callers
- Verify flash loan receipts cannot be cross-used between pools
- Test claim functions for replay resistance
- Fuzz assert conditions with boundary values
- Test mint limit exhaustion with dust amounts
- Verify blocklist enforcement with various address orderings

---

### Keywords for Search

`access_control`, `visibility`, `public`, `public_package`, `public_friend`, `entry`, `owner_check`, `tx_context_sender`, `capability`, `AdminCap`, `TradeCap`, `TradeProof`, `flash_loan`, `receipt`, `UID`, `object_id`, `assert`, `invariant`, `security_level`, `role_removal`, `ACL`, `blocklist`, `replay`, `repeated_invocation`, `mint_limit`, `gas_limit`, `zk_proof`, `groth16`, `signature_length`, `ed25519`, `TTL`, `tick_spacing`, `snapshot`, `merkle_root`, `price_manipulation`, `donation_attack`

### Related Vulnerabilities
- `DB/general/access-control/` — Generic access control patterns
- `DB/general/flash-loans/` — Flash loan patterns
- `DB/general/signatures/` — Signature validation patterns

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

`access_control`, `access_control_validation`, `admin_cap`, `assert`, `authorization`, `blocklist`, `capability_pattern`, `claim_tokens`, `deposit`, `donate`, `emergency_withdraw`, `entry`, `finalize_snapshot_update`, `flash_loan`, `flash_receipt`, `gas`, `generate_proof_as_owner`, `generate_proof_as_trader`, `get_share_price`, `limit`, `match_orders`, `mint`, `missing_access_control|visibility_misconfiguration|input_validation|role_mismanagement`, `move`, `object_id`, `open_position`, `owner_check`, `public`, `public_friend`, `public_package`, `role_management`, `security_level`, `sui`, `trade_proof`, `tx_context_sender`, `uid_to_inner`, `validation`, `visibility`, `zk_proof`

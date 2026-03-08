---
protocol: generic
chain: sui, aptos, movement
category: access_control
vulnerability_type: missing_authorization, signer_exposure, role_escalation, capability_misuse
attack_type: privilege_escalation, unauthorized_access
affected_component: access_control, authorization_logic, capability_management
primitives:
  - signer_capability
  - access_control
  - role_management
  - capability_pattern
  - object_ownership
  - version_check
severity: critical
impact: fund_loss, unauthorized_access, privilege_escalation
exploitability: 0.8
financial_impact: critical
tags:
  - move
  - sui
  - aptos
  - movement
  - access_control
  - authorization
  - signer
  - capability
  - defi
language: move
version: all
---

## References
| # | Source | Protocol | Auditor | Severity |
|---|--------|----------|---------|----------|
| [R1] | reports/ottersec_move_audits/markdown/aftermath_marketmaking_v2_audit_final.md | Aftermath Finance | OtterSec | Critical |
| [R2] | reports/ottersec_move_audits/markdown/aftermath_perps_oracle_audit_final.md | Aftermath Perps | OtterSec | High |
| [R3] | reports/ottersec_move_audits/markdown/ethsign_merkle_token_distributor_audit_final.md | EthSign | OtterSec | Critical |
| [R4] | reports/ottersec_move_audits/markdown/mayan_sui_audit_final.md | Mayan Sui | OtterSec | High |
| [R5] | reports/ottersec_move_audits/markdown/movement_merkle_airdrop_audit_final.md | Movedrop L2 | OtterSec | Critical |
| [R6] | reports/ottersec_move_audits/markdown/deepbook_v3_audit_draft.md | DeepBook V3 | OtterSec | High |
| [R7] | reports/ottersec_move_audits/markdown/lombard_finance_move_audit_final.md | Lombard SUI | OtterSec | High |
| [R8] | reports/ottersec_move_audits/markdown/canopy_audit_final.md | Canopy | OtterSec | High |
| [R9] | reports/ottersec_move_audits/markdown/mysten_republic_audit_final_v2.md | Mysten Republic | OtterSec | Medium |
| [R10] | reports/ottersec_move_audits/markdown/aave_aptos_v3_audit_final.md | Aave Aptos V3 | OtterSec | High |
| [R11] | reports/ottersec_move_audits/markdown/echelon_audit_final.md | Echelon | OtterSec | High |
| [R12] | reports/ottersec_move_audits/markdown/bluefin_spot_audit_final.md | Bluefin Spot | OtterSec | High |
| [R13] | reports/ottersec_move_audits/markdown/aptos_securitize_audit_final.md | Aptos Securitize | OtterSec | High |

## Move Access Control and Authorization Vulnerabilities

**Comprehensive patterns for access control, authorization, signer capability exposure, role management, and capability misuse in Move-based smart contracts across Sui, Aptos, and Movement chains.**

### Overview

Access control vulnerabilities are the second most impactful class in Move-based protocols, frequently rated Critical. Move's capability-based access model (Sui's object ownership, Aptos's signer/capability pattern) introduces unique attack surfaces absent in Solidity. Found in 13/29 OtterSec audit reports (45%).

### Vulnerability Description

#### Root Cause

Move uses different access control paradigms per chain:
- **Aptos**: Signer-based + SignerCapability for resource accounts
- **Sui**: Object ownership + capability objects for delegated access
- **Movement**: Similar to Aptos with minor differences

Common failure modes:
- Public functions exposing signer capabilities (allowing anyone to act as resource account)
- Missing authorization checks on sensitive functions
- Role separation violations (one role gaining another's privileges)
- Missing capability revocation mechanisms
- Version check bypass allowing use of outdated package logic

---

## Pattern 1: Public Signer Capability Exposure — move-acl-001

**Frequency**: 2/29 reports (EthSign [R3], Movedrop L2 [R5])
**Severity consensus**: CRITICAL
**Validation**: Moderate — 2 independent protocols on different chains

### Attack Scenario
1. Protocol creates a resource account with SignerCapability stored
2. A public function returns the signer from the capability without authorization
3. Attacker calls this function to get signer for the resource account
4. Attacker uses signer to withdraw all funds from the resource account

### Vulnerable Pattern Example

**Example 1: EthSign — Public Signer Retrieval Drains All Funds** [CRITICAL] [R3]
```move
// ❌ VULNERABLE: Public function returns signer for any distributor
public fun get_distribution_signer(distributor_addr: address): signer 
    acquires DistributorConfig 
{
    let config = borrow_global<DistributorConfig>(distributor_addr);
    // ❌ Anyone can call this and get full signer access
    account::create_signer_with_capability(&config.signer_cap)
}

// Attacker exploits:
public entry fun steal_all_funds(attacker: &signer, target_distributor: address) {
    let distributor_signer = get_distribution_signer(target_distributor);
    // Now has full control of distributor's resource account
    let balance = primary_fungible_store::balance(target_distributor, token_metadata);
    primary_fungible_store::transfer(&distributor_signer, token_metadata, 
        signer::address_of(attacker), balance);
}
```

**Example 2: Movedrop L2 — Resource Address Mismatch Locking Funds** [CRITICAL] [R5]
```move
// ❌ VULNERABLE: Initialization uses signer-derived address, but access uses hardcoded
public fun initialize_airdrop(creator: &signer, seed: vector<u8>, ...) {
    // Resource account derived from creator + seed
    let (resource_signer, _) = account::create_resource_account(creator, seed);
    let resource_addr = signer::address_of(&resource_signer);
    
    // Stores config at resource_addr
    move_to(&resource_signer, AirdropConfig { ... });
}

// ❌ But claim uses a FIXED predetermined address
public fun claim(user: &signer, ...) acquires AirdropConfig {
    // ❌ Uses hardcoded address instead of derived one
    let config = borrow_global_mut<AirdropConfig>(@fixed_resource_address);
    // If creator != expected signer, funds are permanently locked
}
```

### Secure Implementation

**Fix: Restrict Signer Access to Internal Modules Only**
```move
// ✅ SECURE: Make signer retrieval friend-only or internal
friend merkle_distributor::claim;

public(friend) fun get_distribution_signer(distributor_addr: address): signer 
    acquires DistributorConfig 
{
    let config = borrow_global<DistributorConfig>(distributor_addr);
    account::create_signer_with_capability(&config.signer_cap)
}
```

---

## Pattern 2: Missing Authorization on Sensitive Functions — move-acl-002

**Frequency**: 5/29 reports (Aftermath MM [R1], Aftermath Perps [R2], Canopy [R8], Lombard SUI [R7], Mayan [R4])
**Severity consensus**: HIGH
**Validation**: Strong — 5 independent protocols

### Attack Scenario
1. Protocol exposes a function that performs a sensitive action (trading, payload marking, messaging)
2. No check verifies the caller is authorized
3. Any user can invoke the function to manipulate state or front-run legitimate users

### Vulnerable Pattern Example

**Example 1: Aftermath MM — Unrestricted Trading Account Access** [CRITICAL] [R1]
```move
// ❌ VULNERABLE: No access control on trading account retrieval
public fun account<L, C>(vault: &Vault<L, C>): &TradingAccount {
    // ❌ Anyone can access the vault's trading account
    &vault.trading_account
    // Can be used to manipulate positions, collateral
}
```

**Example 2: Lombard SUI — Front-Running via Public Payload Marking** [HIGH] [R7]
```move
// ❌ VULNERABLE: Anyone can mark payloads as used
public fun validate_and_store_payload(
    consortium: &mut Consortium,
    payload: vector<u8>,
    proof: vector<u8>,
) {
    // Validates payload signature — good
    let hash = validate_signature(consortium, payload, proof);
    
    // ❌ But ANYONE can call this to mark payload as used
    // Attacker front-runs legitimate mint by calling this first
    consortium.used_payloads.add(hash, true);
}
```

**Example 3: Canopy — Unrestricted Cross-Chain Messaging** [HIGH] [R8]
```move
// ❌ VULNERABLE: No authorization check on cross-chain message sending
public fun send_cross_chain_message(
    oapp: &OApp,
    destination_chain: u16,
    message: vector<u8>,
) {
    // ❌ Any user can send arbitrary messages from this OApp
    // No signer check, no capability check
    layerzero::send(oapp, destination_chain, message);
}
```

### Secure Implementation

**Fix: Add Authorization Checks**
```move
// ✅ SECURE: Capability-gated access
public fun account<L, C>(vault: &Vault<L, C>, cap: &VaultOwnerCap): &TradingAccount {
    assert!(object::id(vault) == cap.vault_id, E_UNAUTHORIZED);
    &vault.trading_account
}

// ✅ SECURE: Move payload marking into treasury with access control
public(friend) fun validate_and_store_payload(
    treasury: &mut Treasury,
    consortium: &mut Consortium,
    payload: vector<u8>,
    proof: vector<u8>,
) {
    let hash = validate_signature(consortium, payload, proof);
    consortium.used_payloads.add(hash, true);
}
```

---

## Pattern 3: Role Separation Violations — move-acl-003

**Frequency**: 3/29 reports (Aave Aptos V3 [R10], Aptos Securitize [R13], Echelon [R11])
**Severity consensus**: HIGH
**Validation**: Strong — 3 independent protocols

### Attack Scenario
1. Protocol defines multiple admin roles with different permissions
2. Role checking logic uses OR instead of AND, or checks are incomplete
3. Lower-privileged role can perform actions reserved for higher-privileged role
4. Role escalation allows unauthorized configuration changes

### Vulnerable Pattern Example

**Example 1: Aave Aptos V3 — Asset Listing Admin Gets Pool Admin Powers** [HIGH] [R10]
```move
// ❌ VULNERABLE: OR logic lets listing admin do pool admin actions
public fun set_reserve_configuration_with_guard(
    account: &signer, asset: address, reserve_config_map: ReserveConfigurationMap
) acquires Reserves, ReserveData {
    assert!(
        // ❌ OR check: listing admin can ALSO set any reserve config
        acl_manage::is_asset_listing_admin(signer::address_of(account))
            || acl_manage::is_pool_admin(signer::address_of(account)),
        error_config::get_ecaller_not_asset_listing_or_pool_admin()
    );
    // Listing admin effectively has super-admin privileges
    set_reserve_configuration(asset, reserve_config_map);
}
```

**Example 2: Aptos Securitize — Inverted Assertion on Wallet Creation** [HIGH] [R13]
```move
// ❌ VULNERABLE: Inverted assertion — only allows special wallets
public fun add_wallet_by_investor(investor: &signer, wallet_addr: address) {
    // ❌ Should be !is_special_wallet (reject special), but includes them instead
    assert!(is_special_wallet(wallet_addr), E_INVALID_WALLET);
    // Only special wallets can be added; legitimate wallets are rejected
}
```

**Example 3: Aptos Securitize — Inconsistent Role Checks Across Functions** [HIGH] [R13]
```move
// ❌ VULNERABLE: Some functions check issuer role, others check transfer_agent
// Documentation says only issuer should have access, but implementation allows transfer_agent
public fun sensitive_operation(account: &signer) {
    assert!(
        is_issuer(signer::address_of(account)) 
            || is_transfer_agent(signer::address_of(account)),  // ❌ Should not be here
        E_UNAUTHORIZED
    );
}
```

### Secure Implementation

**Fix: Strict Role Separation**
```move
// ✅ SECURE: Separate functions for separate roles
public fun set_reserve_configuration(account: &signer, asset: address, config: ReserveConfigurationMap) {
    // Only pool admin can modify existing reserves
    assert!(acl_manage::is_pool_admin(signer::address_of(account)), E_NOT_POOL_ADMIN);
    set_reserve_configuration_internal(asset, config);
}

public fun add_new_reserve(account: &signer, asset: address, config: ReserveConfigurationMap) {
    // Listing admin can only add new reserves
    assert!(acl_manage::is_asset_listing_admin(signer::address_of(account)), E_NOT_LISTING_ADMIN);
    assert!(!reserve_exists(asset), E_RESERVE_ALREADY_EXISTS);
    set_reserve_configuration_internal(asset, config);
}
```

---

## Pattern 4: Missing Capability Revocation — move-acl-004

**Frequency**: 2/29 reports (DeepBook V3 [R6], Aftermath MM [R1])
**Severity consensus**: HIGH
**Validation**: Moderate — 2 independent protocols

### Vulnerable Pattern Example

**Example 1: DeepBook V3 — No Revoke for Deposit/Withdraw Caps** [HIGH] [R6]
```move
// ❌ VULNERABLE: Caps can be generated but never revoked
public fun generate_deposit_cap(manager: &mut BalanceManager, account: &signer): DepositCap {
    let cap = DepositCap { manager_id: object::id(manager) };
    // Added to active list
    vector::push_back(&mut manager.active_depositors, signer::address_of(account));
    cap
}

// ❌ No corresponding revoke function exists
// Once granted, access cannot be removed
```

**Example 2: Aftermath MM — No Timestamp Update Allows Cooldown Bypass** [MEDIUM] [R1]
```move
// ❌ VULNERABLE: Parameter update doesn't update last_used timestamp
public fun update_fee_rate(cap: &mut VaultCap, new_rate: u64) {
    // ❌ Missing: cap.last_used = clock::timestamp_ms(clock);
    // Cooldown check uses stale timestamp, allowing rapid successive updates
    assert!(clock::timestamp_ms(clock) - cap.last_used >= COOLDOWN_PERIOD, E_COOLDOWN);
    cap.fee_rate = new_rate;
}
```

### Secure Implementation

**Fix: Complete Lifecycle Management**
```move
// ✅ SECURE: Generate and revoke capabilities
public fun generate_deposit_cap(manager: &mut BalanceManager, account: &signer): DepositCap {
    let addr = signer::address_of(account);
    vector::push_back(&mut manager.active_depositors, addr);
    DepositCap { manager_id: object::id(manager) }
}

public fun revoke_deposit_cap(manager: &mut BalanceManager, admin: &signer, depositor: address) {
    assert!(is_admin(manager, signer::address_of(admin)), E_UNAUTHORIZED);
    let (found, idx) = vector::index_of(&manager.active_depositors, &depositor);
    assert!(found, E_NOT_FOUND);
    vector::swap_remove(&mut manager.active_depositors, idx);
}
```

---

## Pattern 5: Missing Version Checks on State Objects — move-acl-005

**Frequency**: 3/29 reports (Mayan Sui [R4], Bluefin Spot [R12], Echelon [R11])
**Severity consensus**: HIGH
**Validation**: Strong — 3 independent protocols

### Attack Scenario
1. Protocol upgrades package to a new version with security fixes
2. Admin functions or critical operations don't verify the state object version
3. Attacker uses outdated package version to bypass new security checks
4. Security fixes are effectively nullified

### Vulnerable Pattern Example

**Example 1: Mayan Sui — Admin Functions Missing Version Check** [HIGH] [R4]
```move
// ❌ VULNERABLE: Admin functions don't check state version
public fun update_config(state: &mut State, admin: &signer, new_config: Config) {
    assert!(is_admin(state, signer::address_of(admin)), E_UNAUTHORIZED);
    // ❌ No version check — admin can call this from old package version
    // Bypasses security restrictions added in newer versions
    state.config = new_config;
}
```

**Example 2: Bluefin Spot — Absence of Version Update Functionality** [HIGH] [R12]
```move
// ❌ VULNERABLE: No way to update the version at all
module bluefin::config {
    struct GlobalConfig has key {
        version: u64,
        // ... other fields
    }
    
    // ❌ No update_version function exists
    // Can never migrate to new version, breaking upgrade path
}
```

### Secure Implementation

**Fix: Version Guard on All Public Functions**
```move
// ✅ SECURE: Version check on all entry points
const CURRENT_VERSION: u64 = 2;

public fun update_config(state: &mut State, admin: &signer, new_config: Config) {
    assert!(state.version == CURRENT_VERSION, E_VERSION_MISMATCH);
    assert!(is_admin(state, signer::address_of(admin)), E_UNAUTHORIZED);
    state.config = new_config;
}

public fun migrate_version(state: &mut State, admin: &signer) {
    assert!(is_admin(state, signer::address_of(admin)), E_UNAUTHORIZED);
    state.version = CURRENT_VERSION;
}
```

---

## Pattern 6: Unverified Object/Pool Instance in Operations — move-acl-006

**Frequency**: 2/29 reports (Kuna Labs [R4 from batch2], Echelon [R11])
**Severity consensus**: HIGH
**Validation**: Moderate — 2 independent protocols

### Vulnerable Pattern Example

**Example 1: Kuna Labs — Supply Pool Validation Bypass in Liquidation** [HIGH]
```move
// ❌ VULNERABLE: Doesn't verify correct SupplyPool instance
public fun liquidate<X, SX>(
    position: &mut Position,
    supply_pool: &mut SupplyPool<X, SX>,  // ❌ Any SupplyPool<X, *> accepted
    amount: u64,
    ctx: &TxContext,
) {
    // Liquidator provides SupplyPool<X, SX1> instead of SupplyPool<X, SX0>
    // Repayment logic fails silently (no shares burned from wrong pool)
    let _shares = burn_from_pool(supply_pool, amount);
    
    // ❌ But collateral reward is still granted
    transfer_collateral(position, ctx.sender(), calculate_reward(amount));
}
```

### Secure Implementation

**Fix: Verify Pool Instance ID**
```move
// ✅ SECURE: Verify supply pool matches position's expected pool
public fun liquidate<X, SX>(
    position: &mut Position,
    supply_pool: &mut SupplyPool<X, SX>,
    amount: u64,
    ctx: &TxContext,
) {
    // ✅ Verify this is the correct supply pool for the position
    assert!(object::id(supply_pool) == position.supply_pool_id, E_WRONG_POOL);
    let shares = burn_from_pool(supply_pool, amount);
    assert!(shares > 0, E_NO_SHARES_BURNED);
    transfer_collateral(position, ctx.sender(), calculate_reward(amount));
}
```

---

## Pattern 7: Publicly Exposed Signer Capability Enables Fund Theft — move-acl-007

**Frequency**: 2/29 reports (EthSign, Canopy)
**Severity consensus**: CRITICAL (lowest across auditors)
**Validation**: Moderate — 2 independent protocols

### Attack Scenario
1. A public function returns a signer created from a stored `SignerCapability`
2. Any external caller retrieves the signer for the resource account holding funds
3. Attacker uses the signer to call `primary_fungible_store::withdraw` or `coin::withdraw`
4. All tokens in the resource account are stolen

### Vulnerable Pattern Example

**Example: EthSign — Public Function Returns Resource Account Signer** [CRITICAL]
```move
// ❌ VULNERABLE: Any caller can get the signer for any distribution
public fun get_distribution_signer(distribution_addr: address): signer acquires DistributorFactory {
    let factory = borrow_global<DistributorFactory>(@module_addr);
    let signer_cap = table::borrow(&factory.signer_caps, distribution_addr);
    account::create_signer_with_capability(signer_cap)
}
```

### Secure Implementation
```move
// ✅ SECURE: Restrict signer access to friend modules only
public(friend) fun get_distribution_signer(distribution_addr: address): signer acquires DistributorFactory {
    let factory = borrow_global<DistributorFactory>(@module_addr);
    let signer_cap = table::borrow(&factory.signer_caps, distribution_addr);
    account::create_signer_with_capability(signer_cap)
}
```

---

## Pattern 8: Excessive Admin Privileges Beyond Intended Scope — move-acl-008

**Frequency**: 3/29 reports (Aave Aptos V3, Aptos Securitize, Canopy)
**Severity consensus**: MEDIUM (lowest across auditors)
**Validation**: Strong — 3 independent auditors

### Attack Scenario
1. Access control check uses OR to allow multiple admin roles
2. A lower-privilege role (listing admin) gains full configuration power intended for pool admin
3. Compromised listing admin can modify any existing reserve's risk parameters
4. Malicious configuration enables market manipulation or fund extraction

### Vulnerable Pattern Example

**Example: Aave Aptos V3 — Listing Admin Can Modify Existing Reserves** [MEDIUM]
```move
// ❌ VULNERABLE: Listing admin gets full config modify power
public fun set_reserve_configuration_with_guard(account: &signer, asset: address, config: ReserveConfigMap) {
    assert!(
        acl_manage::is_asset_listing_admin(signer::address_of(account))
            || acl_manage::is_pool_admin(signer::address_of(account)),
        E_NOT_AUTHORIZED
    );
    set_reserve_configuration(asset, config); // Full modify power for both roles
}
```

### Secure Implementation
```move
// ✅ SECURE: Separate paths for different admin scopes
public fun set_reserve_configuration_with_guard(account: &signer, asset: address, config: ReserveConfigMap) {
    let caller = signer::address_of(account);
    if (acl_manage::is_asset_listing_admin(caller)) {
        assert!(!reserve_exists(asset), E_LISTING_ADMIN_CANNOT_MODIFY);
        set_reserve_configuration(asset, config);
    } else {
        assert!(acl_manage::is_pool_admin(caller), E_NOT_AUTHORIZED);
        set_reserve_configuration(asset, config);
    };
}
```

---

## Pattern 9: Inverted Assertion Logic Allows Prohibited Actions — move-acl-009

**Frequency**: 2/29 reports (Aptos Securitize, ThalaSwap V2)
**Severity consensus**: MEDIUM (lowest across auditors)
**Validation**: Moderate — 2 independent protocols

### Attack Scenario
1. Developer writes `assert!(is_special_wallet(addr), E_WALLET_SPECIAL)` intending to block special wallets
2. The assertion is inverted — it requires the wallet to BE special, blocking normal wallets instead
3. Only special (prohibited) wallets pass the check and get registered
4. Normal user wallets are rejected while prohibited ones succeed

### Vulnerable Pattern Example

**Example: Aptos Securitize — Inverted Special Wallet Check** [MEDIUM]
```move
// ❌ VULNERABLE: Assertion is backwards — only special wallets pass
public entry fun add_wallet_by_investor(authorizer: &signer, wallet_addr: address) {
    assert!(is_special_wallet(wallet_addr), EWALLET_SPECIAL); // BUG: Inverted!
    // Intent was: assert!(!is_special_wallet(wallet_addr), ...)
    register_wallet(wallet_addr);
}
```

### Secure Implementation
```move
// ✅ SECURE: Negated check blocks special wallets
public entry fun add_wallet_by_investor(authorizer: &signer, wallet_addr: address) {
    assert!(!is_special_wallet(wallet_addr), EWALLET_SPECIAL);
    register_wallet(wallet_addr);
}
```

---

## Pattern 10: Signature Replay in Claim Functions — move-acl-010

**Frequency**: 2/29 reports (Canopy, Movedrop L2)
**Severity consensus**: MEDIUM (lowest across auditors)
**Validation**: Moderate — 2 independent protocols

### Attack Scenario
1. Claim function uses signature-based authorization without nonce tracking
2. A valid signature can be retransmitted within the deadline window
3. Attacker replays claim transactions, withdrawing funds on behalf of users
4. If phase transitions occur, users incur additional penalties from unauthorized claims

### Vulnerable Pattern Example

**Example: Canopy — No Nonce Protection on Signature Claims** [MEDIUM]
```move
// ❌ VULNERABLE: No nonce prevents replaying the same signature
public entry fun claim_with_signature(
    amount: u64,
    deadline: u64,
    signature: vector<u8>,
) {
    assert!(timestamp::now_seconds() < deadline, E_EXPIRED);
    let message = bcs::to_bytes(&amount);
    vector::append(&mut message, bcs::to_bytes(&deadline));
    assert!(verify_signature(message, signature), E_INVALID_SIG);
    // No nonce tracking — same signature can be replayed
    transfer_tokens(amount);
}
```

### Secure Implementation
```move
// ✅ SECURE: Include nonce in signature and track used nonces
public entry fun claim_with_signature_safe(
    amount: u64,
    nonce: u64,
    deadline: u64,
    signature: vector<u8>,
) acquires NonceTracker {
    let tracker = borrow_global_mut<NonceTracker>(@module_addr);
    assert!(!table::contains(&tracker.used_nonces, nonce), E_NONCE_USED);
    table::add(&mut tracker.used_nonces, nonce, true);
    assert!(timestamp::now_seconds() < deadline, E_EXPIRED);
    let message = bcs::to_bytes(&amount);
    vector::append(&mut message, bcs::to_bytes(&nonce));
    vector::append(&mut message, bcs::to_bytes(&deadline));
    assert!(verify_signature(message, signature), E_INVALID_SIG);
    transfer_tokens(amount);
}
```

---

## Pattern 11: Cumulative Claim Exceeds Entitlement — move-acl-011

**Frequency**: 2/29 reports (Mysten Republic, Movedrop L2)
**Severity consensus**: CRITICAL (lowest across auditors)
**Validation**: Moderate — 2 independent protocols

### Attack Scenario
1. Claim function checks `amount <= unlocked_tokens` per call
2. Does NOT verify cumulative claims (`amount + tokens_transferred <= unlocked_tokens`)
3. User calls claim repeatedly, each time extracting the maximum unlocked amount
4. Total claims far exceed actual entitlement, draining the vesting/airdrop contract

### Vulnerable Pattern Example

**Example: Mysten Republic — Per-Call Check Without Cumulative Tracking** [CRITICAL]
```move
// ❌ VULNERABLE: Checks per-call, not cumulative
public fun claim<T>(self: &mut Timelock<T>, amount: Option<u64>, clock: &Clock, ctx: &mut TxContext) {
    let unlocked = calculate_unlocked(self, clock);
    let amount = amount.destroy_or!(unlocked);
    assert!(amount <= unlocked, ENotEnoughBalanceUnlocked); // Per-call only!
    self.tokens_transferred = self.tokens_transferred + amount;
    let coin = self.left_balance.split(amount).into_coin(ctx);
    transfer(coin, ctx.sender());
}
```

### Secure Implementation
```move
// ✅ SECURE: Check cumulative claims against total unlocked
public fun claim_safe<T>(self: &mut Timelock<T>, amount: Option<u64>, clock: &Clock, ctx: &mut TxContext) {
    let unlocked = calculate_unlocked(self, clock);
    let amount = amount.destroy_or!(unlocked - self.tokens_transferred);
    assert!(amount + self.tokens_transferred <= unlocked, ENotEnoughBalanceUnlocked);
    self.tokens_transferred = self.tokens_transferred + amount;
    let coin = self.left_balance.split(amount).into_coin(ctx);
    transfer(coin, ctx.sender());
}
```

---

## Pattern 12: Permissionless Function Before Time-Based Gate — move-acl-012

**Frequency**: 2/29 reports (Mayan Sui, Canopy)
**Severity consensus**: HIGH (lowest across auditors)
**Validation**: Moderate — 2 independent protocols

### Attack Scenario
1. Access control is only enforced during a penalty period (e.g., after a deadline)
2. Before the penalty period, any caller can invoke the restricted operation
3. An unauthorized party front-runs the legitimate actor before the time gate activates
4. Attacker fulfills orders, manipulates state, or extracts value

### Vulnerable Pattern Example

**Example: Mayan Sui — Driver Check Only Enforced During Penalty Period** [HIGH]
```move
// ❌ VULNERABLE: No identity check before penalty period
public fun prepare_fulfill_winner(order: &Order, msg_driver: address, ctx: &TxContext) {
    let now = clock.timestamp_ms() / 1000;
    assert!(order.deadline() > now, EDeadlineIsPassed);
    // Only checks driver during penalty period — anyone can fulfill before that
    if (now >= order.deadline() - (order.penalty_period() as u64)) {
        assert!(msg_driver == ctx.sender(), EInvalidDriver);
    };
    process_fulfillment(order);
}
```

### Secure Implementation
```move
// ✅ SECURE: Always enforce driver identity
public fun prepare_fulfill_winner_safe(order: &Order, msg_driver: address, ctx: &TxContext) {
    let now = clock.timestamp_ms() / 1000;
    assert!(order.deadline() > now, EDeadlineIsPassed);
    assert!(msg_driver == ctx.sender(), EInvalidDriver); // Always check
    process_fulfillment(order);
}
```

---

## Pattern 13: Missing Capability-to-Object Ownership Validation — move-acl-013

**Frequency**: 2/29 reports (Aftermath MM, Kuna Labs)
**Severity consensus**: MEDIUM (lowest across auditors)
**Validation**: Moderate — 2 independent protocols

### Attack Scenario
1. Function accepts a capability object (VaultOwnerCap) and a target resource (Vault)
2. It never validates that the capability belongs to the specific target resource
3. A cap holder for Vault A can operate on Vault B, C, etc.
4. Attacker creates a vault, gets a cap, then uses it to modify other users' vaults

### Vulnerable Pattern Example

**Example: Aftermath MM — VaultOwnerCap Not Validated Against Vault** [MEDIUM]
```move
// ❌ VULNERABLE: No check that cap belongs to this specific vault
public(package) fun update_vault_version<L, C>(
    _vault_owner_cap: &VaultOwnerCap,
    vault: &mut Vault<L, C>,
) {
    vault.version = constants::version(); // Any cap holder can update any vault
}
```

### Secure Implementation
```move
// ✅ SECURE: Validate cap ownership against vault
public(package) fun update_vault_version_safe<L, C>(
    vault_owner_cap: &VaultOwnerCap,
    vault: &mut Vault<L, C>,
) {
    assert!(vault_owner_cap.vault_id == object::id(vault), E_CAP_VAULT_MISMATCH);
    vault.version = constants::version();
}
```

---

## Pattern 14: Missing Approval Revocation Mechanism — move-acl-014

**Frequency**: 2/29 reports (Aptos Securitize, DeepBook V3)
**Severity consensus**: LOW (lowest across auditors)
**Validation**: Moderate — 2 independent protocols

### Attack Scenario
1. Protocol allows granting approval/deposit capabilities to addresses
2. No function exists to revoke granted capabilities
3. A compromised approved address retains permanent access
4. Only workaround is setting allowance to 0, which doesn't delete the entry

### Vulnerable Pattern Example

**Example 1: Aptos Securitize — No Approval Removal Function** [LOW]
```move
// ❌ VULNERABLE: Can add allowances but never remove them
public entry fun approve(owner: &signer, spender: address, amount: u64) {
    let allowances = borrow_global_mut<Allowances>(signer::address_of(owner));
    table::upsert(&mut allowances.list, spender, amount);
    // No corresponding remove function exists
}
```

**Example 2: DeepBook V3 — DepositCap Not Tracked for Revocation** [LOW]
```move
// ❌ VULNERABLE: Cap is created but never added to revocable list
public fun generate_proof_as_depositor(
    balance_manager: &BalanceManager,
    deposit_cap: &DepositCap,
): TradeProof {
    assert!(balance_manager.id() == deposit_cap.balance_manager_id, E_MISMATCH);
    // No way to revoke this cap later
    TradeProof { balance_manager_id: object::id(balance_manager), trader: tx_context::sender() }
}
```

### Secure Implementation
```move
// ✅ SECURE: Track and allow revocation of approvals
public entry fun revoke_approval(owner: &signer, spender: address) {
    let allowances = borrow_global_mut<Allowances>(signer::address_of(owner));
    if (table::contains(&allowances.list, spender)) {
        table::remove(&mut allowances.list, spender);
    };
}
```

---

## Pattern 15: Front-Running Payload Consumption to Block Legitimate Users — move-acl-015

**Frequency**: 2/29 reports (Lombard SUI, EthSign)
**Severity consensus**: MEDIUM (lowest across auditors)
**Validation**: Moderate — 2 independent protocols

### Attack Scenario
1. A public `validate_and_store_payload` function marks payloads as consumed
2. Attacker monitors mempool for legitimate minting transactions
3. Attacker front-runs by calling validate with the same payload first
4. Legitimate transaction fails because payload is already marked as used

### Vulnerable Pattern Example

**Example: Lombard SUI — Public Payload Validation Enables Front-Running** [MEDIUM]
```move
// ❌ VULNERABLE: Anyone can call this to mark a payload as used
public fun validate_and_store_payload(
    consortium: &mut Consortium,
    payload: vector<u8>,
    proof: vector<u8>,
) {
    let hash = hash::sha2_256(payload);
    assert!(!consortium.is_payload_used(hash), EUsedPayload);
    verify_signatures(consortium, payload, proof);
    consortium.used_payloads.add(hash, true); // Payload now consumed
}
```

### Secure Implementation
```move
// ✅ SECURE: Inline validation into the minting function
public(friend) fun mint_with_payload(
    treasury: &mut Treasury,
    consortium: &mut Consortium,
    payload: vector<u8>,
    proof: vector<u8>,
) {
    let hash = hash::sha2_256(payload);
    assert!(!consortium.is_payload_used(hash), EUsedPayload);
    verify_signatures(consortium, payload, proof);
    consortium.used_payloads.add(hash, true);
    let amount = decode_mint_amount(payload);
    mint_tokens(treasury, amount);
}
```

---

## Pattern 16: Emergency Withdrawal Bypasses Access Restrictions — move-acl-016

**Frequency**: 2/29 reports (Canopy, Aftermath MM)
**Severity consensus**: HIGH (lowest across auditors)
**Validation**: Moderate — 2 independent protocols

### Attack Scenario
1. Protocol has emergency withdrawal pathway intended for crisis situations
2. A privileged actor (deployer creator, vault owner) can bypass normal restrictions
3. The FA API allows the creator to directly interact with the primary fungible store
4. Emergency withdrawal restrictions can be circumvented through direct API access

### Vulnerable Pattern Example

**Example: Canopy — Creator Bypasses Emergency Withdrawal Restrictions** [HIGH]
```move
// ❌ VULNERABLE: Creator can bypass emergency restrictions via FA API
// The deployer's creator has direct access to primary_fungible_store
// Even when emergency_withdrawal is restricted, creator can call:
//   primary_fungible_store::withdraw(creator_signer, metadata, amount)
// This bypasses all emergency withdrawal checks
```

### Secure Implementation
```move
// ✅ SECURE: Use a non-creator resource account as the store owner
fun init_module(admin: &signer) {
    // Create a resource account — admin is NOT the creator of FA stores
    let (resource_signer, resource_cap) = account::create_resource_account(admin, SEED);
    // FA stores owned by resource_signer are not directly accessible by admin
    move_to(&resource_signer, DeployerData { resource_cap, ... });
}
```

---

## Pattern 17: Group/Role ID Reuse After Deletion — move-acl-017

**Frequency**: 1/29 reports (Mysten Republic)
**Severity consensus**: LOW (single auditor)
**Validation**: Weak — single auditor, but clear vulnerability

### Attack Scenario
1. Admin removes a group, freeing up its numeric ID
2. A new group is created with the same ID as the removed one
3. Group-pair permissions that reference the old group's ID now apply to the new group
4. New group members inherit unauthorized privileges from the deleted group's ACL entries

### Vulnerable Pattern Example

**Example: Mysten Republic — Reused Group ID Inherits Old Permissions** [LOW]
```move
// ❌ VULNERABLE: Group IDs can be reused after removal
public fun add_group<T>(policy: &mut TokenPolicy<T>, group_id: u64, group_name: String) {
    // No check if group_id was previously used and has lingering permissions
    policy.add_group(group_id, group_name);
}
```

### Secure Implementation
```move
// ✅ SECURE: Use monotonically increasing IDs that are never reused
public fun add_group_safe<T>(policy: &mut TokenPolicy<T>, group_name: String) {
    let group_id = policy.next_group_id;
    policy.next_group_id = policy.next_group_id + 1;
    policy.add_group(group_id, group_name);
}
```

---

## Pattern 18: Irrevocable Token Freeze Without Unfreeze — move-acl-018

**Frequency**: 1/29 reports (Thala LSD)
**Severity consensus**: LOW (single auditor)
**Validation**: Weak — single auditor, but permanent fund lock

### Attack Scenario
1. Admin can freeze token stores via `coin::freeze_coin_store`
2. No corresponding unfreeze function exists in the module
3. Once frozen, users permanently lose access to their tokens
4. Admin error or malicious action results in irreversible fund lock

### Vulnerable Pattern Example

**Example: Thala LSD — Freeze Without Unfreeze** [LOW]
```move
// ❌ VULNERABLE: No corresponding unfreeze function
public entry fun freeze_thapt_coin_stores(manager: &signer, accounts: vector<address>) acquires TLSD {
    assert!(manager::is_authorized(manager), ERR_UNAUTHORIZED);
    let freeze_cap = &borrow_global<TLSD>(@resource).thAPT_freeze_capability;
    vector::for_each(accounts, |addr| {
        coin::freeze_coin_store(addr, freeze_cap);
    });
    // No unfreeze function exists in the module
}
```

### Secure Implementation
```move
// ✅ SECURE: Provide both freeze and unfreeze capabilities
public entry fun unfreeze_thapt_coin_stores(manager: &signer, accounts: vector<address>) acquires TLSD {
    assert!(manager::is_authorized(manager), ERR_UNAUTHORIZED);
    let freeze_cap = &borrow_global<TLSD>(@resource).thAPT_freeze_capability;
    vector::for_each(accounts, |addr| {
        coin::unfreeze_coin_store(addr, freeze_cap);
    });
}
```

---

### Impact Analysis

#### Technical Impact
- Complete fund drainage through signer exposure (2/29 reports) — CRITICAL
- Unauthorized state manipulation via missing auth checks (5/29 reports)
- Role escalation bypassing governance controls (3/29 reports)
- Irrevocable access grants (2/29 reports)
- Security upgrade bypass via missing version checks (3/29 reports)

#### Business Impact
- Total loss of protocol funds (EthSign, Movedrop L2)
- Governance undermined through role escalation (Aave Aptos)
- Security fixes ineffective without version enforcement
- Compliance violations from role management bugs (Aptos Securitize)

#### Affected Scenarios
- Airdrop/token distribution protocols using resource accounts (EthSign, Movedrop L2)
- Cross-chain bridges with public validation functions (Lombard, Canopy)
- DeFi protocols with multi-role admin systems (Aave, Echelon, Securitize)
- DEX/CLOB with delegated access (DeepBook V3, Aftermath)

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: `public fun` returning `signer` or exposing signer capability
- Pattern 2: `public fun` modifying shared/global state without signer/capability check
- Pattern 3: `assert!(is_role_A(...) || is_role_B(...))` with different privilege levels
- Pattern 4: `generate_*_cap` without corresponding `revoke_*_cap` 
- Pattern 5: Entry functions missing `assert!(state.version == CURRENT_VERSION)`
- Pattern 6: Functions accepting generic type params for pool/store without ID verification
```

#### Audit Checklist
- [ ] All public functions returning signers are friend-only or internal
- [ ] Every state-modifying public function has authorization check
- [ ] Role checks use AND for higher privilege, not OR
- [ ] All capabilities have generation AND revocation functions
- [ ] Package version checked on all entry points
- [ ] Generic type parameters verified against expected object IDs

### Keywords for Search

> `access control`, `authorization`, `signer capability`, `signer exposure`, `role management`, `privilege escalation`, `capability`, `move access control`, `sui capability`, `aptos signer`, `resource account`, `create_signer_with_capability`, `SignerCapability`, `AdminCap`, `OwnerCap`, `version check`, `package upgrade`, `friend function`, `public fun`, `role separation`, `front-running`, `payload marking`, `cross-chain messaging`, `deposit cap`, `withdraw cap`, `revoke`

### Related Vulnerabilities

- [SUI_MOVE_ACCESS_CONTROL_VALIDATION_VULNERABILITIES.md](SUI_MOVE_ACCESS_CONTROL_VALIDATION_VULNERABILITIES.md) — Sui-specific access control from Solodit
- [MOVE_CROSS_CHAIN_BRIDGE_VULNERABILITIES.md](MOVE_CROSS_CHAIN_BRIDGE_VULNERABILITIES.md) — Bridge-specific authorization issues
- [MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md](MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md) — Verification bypass patterns

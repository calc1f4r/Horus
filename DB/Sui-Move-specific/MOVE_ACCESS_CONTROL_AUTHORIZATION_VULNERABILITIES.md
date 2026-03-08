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

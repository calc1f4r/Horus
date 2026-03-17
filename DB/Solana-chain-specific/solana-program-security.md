---
# Core Classification (Required)
protocol: generic
chain: solana
category: program_security
vulnerability_type: solana_program_integration

# Attack Vector Details (Required)
attack_type: access_control|data_manipulation|logical_error|dos
affected_component: account_validation|cpi|token_operations|state_management

# Solana-Specific Fields
program_type: anchor|native
account_validation_vector: signer|owner|pda|writer|token_account
cpi_attack_vector: arbitrary_cpi|seed_mismatch|missing_bump|account_ordering

# Technical Primitives (Required)
primitives:
  - signer_check
  - owner_check
  - pda_validation
  - cpi_accounts
  - token_program
  - system_program
  - account_reallocation
  - account_closure
  - lamports_transfer
  - remaining_accounts
  - init_if_needed
  - bump_seed

# Impact Classification (Required)
severity: critical
impact: fund_theft|unauthorized_access|dos|state_corruption|account_takeover
exploitability: 0.70
financial_impact: high

# Context Tags
tags:
  - solana
  - anchor
  - spl_token
  - token_2022
  - pda
  - cpi
  - account_validation

# Version Info
language: rust
version: all

# Pattern Identity (Required)
root_cause_family: missing_access_control
pattern_key: missing_access_control | account_validation | solana_program_integration

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - account_closure
  - account_reallocation
  - borrow
  - bump_seed
  - collisions
  - cpi_accounts
  - deposit
  - emitted
  - for
  - init_if_needed
  - lamports_transfer
  - liquidate
  - mint
  - msg.sender
  - overflows
  - owner_check
  - pda_validation
  - receive
  - remaining_accounts
  - replay
---

## References & Source Reports

> **For Agents**: These patterns are derived from security best practices and real-world audit findings. Use the report paths to read detailed context.

### Account Validation Vulnerabilities
| Category | Report | Path | Severity | Audit Firm |
|----------|--------|------|----------|------------|
| Missing Signer Check | Signer Authorization Bypass | `reports/solana_findings/missing-signer-authorization.md` | CRITICAL | Various |
| Missing Owner Check | Account Owner Not Checked | `reports/solana_findings/account-owner-is-not-checked.md` | HIGH | Various |
| Missing PDA Validation | Lack of PDA Validation | `reports/solana_findings/lack-of-pda-validation.md` | HIGH | OtterSec |
| Arbitrary CPI | Arbitrary CPI Calls | `reports/solana_findings/arbitrary-cpi.md` | CRITICAL | Halborn |

### CPI and Invocation Vulnerabilities
| Category | Report | Path | Severity | Audit Firm |
|----------|--------|------|----------|------------|
| Arbitrary Callback | Arbitrary Program Execution | `reports/solana_findings/arbitrary-callbacks-can-be-used-to-receive-arbitrary-cpi-calls-to-any-program.md` | CRITICAL | Unknown |
| CPI Account Ordering | Program ID Confusion | `reports/solana_findings/cpi-account-ordering-vulnerability.md` | HIGH | Various |
| Missing Bump Value | PDA Bump Mismatch | `reports/solana_findings/missing-bump-seed-validation.md` | HIGH | Various |

### Token & Mint Vulnerabilities
| Category | Report | Path | Severity | Audit Firm |
|----------|--------|------|----------|------------|
| Freeze Authority DOS | Input Token Freeze Risk | `reports/solana_findings/m-02-risk-of-input-token-mint-with-freeze-authority-leading-to-permanent-dos.md` | MEDIUM | Shieldify |
| Missing Freeze Check | Collateral Token Freeze | `reports/solana_findings/m-01-lack-of-freeze-authority-check-for-collateral-tokens-on-create-trading-pool.md` | MEDIUM | Unknown |
| Token Escrow Freeze | Bridge Token Freeze | `reports/solana_findings/h-01-denial-of-service-risk-due-to-frozen-token_escrow-in-onftadapter.md` | HIGH | Unknown |
| MintCloseAuthority | Decimal Manipulation | `reports/token2022_findings/c-01-mint-decimal-manipulation-through-mintcloseauthority-leads-to-inflation-of-.md` | CRITICAL | Shieldify |

### DOS Vulnerabilities
| Category | Report | Path | Severity | Audit Firm |
|----------|--------|------|----------|------------|
| Storage Limit DOS | Permanent DOS via Storage | `reports/solana_findings/h-01-permanent-dos-in-liquidity_lockbox-for-under-10.md` | HIGH | Code4rena |
| Account Pre-creation | Init If Needed Front-run | `reports/solana_findings/init-if-needed-front-run.md` | HIGH | Various |

### PDA and Seed Vulnerabilities
| Category | Report | Path | Severity | Audit Firm |
|----------|--------|------|----------|------------|
| Seed Collision | PDA Seed Collision | `reports/solana_findings/pda-seed-collision.md` | HIGH | Various |
| Missing Bump Seed | Canonical Bump Not Used | `reports/solana_findings/missing-canonical-bump-validation.md` | HIGH | OtterSec |
| Cross-Protocol PDA | PDA Derivation Mismatch | `reports/solana_findings/lack-of-pda-validation.md` | HIGH | OtterSec |
| Critical PDA Flaw | Improper PDA Validation | `reports/solana_findings/c-01-critical-pda-validation-flaw-in-append_data_sandwich_validators_bitmap.md` | HIGH | Pashov |

### Account Type Confusion Vulnerabilities
| Category | Report | Path | Severity | Audit Firm |
|----------|--------|------|----------|------------|
| Type Confusion | Account Type Confusion | `reports/solana_findings/account-type-confusion.md` | MEDIUM | OtterSec |
| Discriminator Bypass | Missing Discriminator Check | `reports/solana_findings/account-type-confusion.md` | MEDIUM | OtterSec |

### Instruction Introspection Vulnerabilities
| Category | Report | Path | Severity | Audit Firm |
|----------|--------|------|----------|------------|
| Ed25519 Verification | Wrong Offset Ed25519 | `reports/solana_findings/c-02-wrongoffset-ed25519-instruction-introspection-enables-forged-approvals.md` | HIGH | Pashov |
| Sysvar Validation | Missing Sysvar Check | `reports/solana_findings/lack-of-sysvar-account-validation.md` | HIGH | OtterSec |

### Replay Attack Vulnerabilities
| Category | Report | Path | Severity | Audit Firm |
|----------|--------|------|----------|------------|
| Signature Replay | Missing Nonce Reset | `reports/solana_findings/m-31-missing-nonce-reset-during-tss-address-update-allowing-signature-replay.md` | MEDIUM | Sherlock |
| Transaction Replay | No Replay Protection | `reports/solana_findings/successful-transactions-are-not-stored-causing-a-replay-attack-on-redeemdeposits.md` | HIGH | Codehawks |

### CPI Security Vulnerabilities
| Category | Report | Path | Severity | Audit Firm |
|----------|--------|------|----------|------------|
| Unrestricted CPI | MarginSwap CPI | `reports/solana_findings/unrestricted-marginswap-cpi.md` | HIGH | OtterSec |
| Authority Bypass | Incorrect Authority | `reports/solana_findings/deposit-tokens-transferred-from-depositor-token-account-instead-of-signer.md` | MEDIUM | OpenZeppelin |
| Invalid Authority | Authority Check Bypass | `reports/solana_findings/invalid-authority-check.md` | HIGH | OtterSec |
| Remaining Accounts | Insufficient Checks | `reports/solana_findings/insufficient-account-checks.md` | MEDIUM | OtterSec |

### Lending/Collateral Vulnerabilities
| Category | Report | Path | Severity | Audit Firm |
|----------|--------|------|----------|------------|
| Collateral Bypass | Claim Without Repay | `reports/solana_findings/h-01-collateral-can-be-claimed-back-without-repaying-its-corresponding-loan-due-.md` | HIGH | Code4rena |
| Withdrawal DOS | Ticket Desync | `reports/solana_findings/dos-due-to-withdrawal-ticket-desynchronization.md` | HIGH | OtterSec |

### Initialization Vulnerabilities
| Category | Report | Path | Severity | Audit Firm |
|----------|--------|------|----------|------------|
| Front-run Init | Multisig Front-run | `reports/solana_findings/attacker-can-front-run-multisig-creation-transaction.md` | HIGH | TrailOfBits |
| Permissionless Init | Spoofed Official Instance | `reports/solana_findings/permissionless-offrampstate-initialization-under-official-program-id-enables-spo.md` | MEDIUM | Cyfrin |
| Self-Assign Admin | Super Admin Hijack | `reports/solana_findings/m-01-any-wallet-can-self-assign-as-super_admin-for-arbitrary-mint.md` | MEDIUM | Pashov |
| Pre-funding DOS | Create Account DOS | `reports/solana_findings/create_account-can-be-dosed-with-pre-funding.md` | MEDIUM | Cyfrin |

### Arithmetic Vulnerabilities
| Category | Report | Path | Severity | Audit Firm |
|----------|--------|------|----------|------------|
| Silent Overflow | TrimmedAmount Shift | `reports/solana_findings/silent-overflow-in-trimmedamountshift-could-result-in-rate-limiter-being-bypasse.md` | MEDIUM | Cyfrin |
| Right Shift Panic | Bit Length Overflow | `reports/solana_findings/right-shift-overflow-panic.md` | HIGH | OtterSec |
| Precision Attack | Mint Check Missing | `reports/solana_findings/precision-manipulation-due-to-missing-mint-check.md` | HIGH | Cyfrin |
| Decimal Mismatch | Fee Accounting Error | `reports/solana_findings/decimal-mismatch-in-fee-prepayment-accounting-causes-incorrect-balance-tracking.md` | MEDIUM | Cyfrin |

### Rent and Account Size Vulnerabilities
| Category | Report | Path | Severity | Audit Firm |
|----------|--------|------|----------|------------|
| Rent Inclusion Error | Bonding Curve Invariant | `reports/solana_findings/m-02-bonding-curve-invariant-check-incorrectly-validates-sol-balance-due-to-rent.md` | MEDIUM | Code4rena |
| Account Size Issue | Faulty Reallocation | `reports/solana_findings/faulty-reallocation-of-market-size.md` | MEDIUM | OtterSec |
| Custody Closing DOS | Token Account Close | `reports/solana_findings/custody-token-account-closing-dos.md` | HIGH | OtterSec |

### Reentrancy Vulnerabilities
| Category | Report | Path | Severity | Audit Firm |
|----------|--------|------|----------|------------|
| Module Bypass | Guard Reentrancy | `reports/solana_findings/h-3-signers-can-bypass-checks-to-add-new-modules-to-a-safe-by-abusing-reentrancy.md` | HIGH | Sherlock |

### Fluid Vault/Liquidation Vulnerabilities
| Category | Report | Path | Severity | Audit Firm |
|----------|--------|------|----------|------------|
| Tick Sentinel Confusion | Tick 0 treated as missing top tick | `reports/ZenithReports/fluidreport.md` (C-3) | CRITICAL | Zenith |
| Selective Path Validation Bypass | `debt_amt=0` bypasses reserve mint validation in liquidate flow | `reports/ZenithReports/fluidreport.md` (C-4) | CRITICAL | Zenith |
| Cross-Vault State Corruption | Missing `vault_id` check in `tick_id_data_after_operate` | `reports/ZenithReports/fluidreport.md` (C-5) | CRITICAL | Zenith |
| Saturating Math Underpricing | Overflow in price conversion underprices collateral asset | `reports/ZenithReports/fluidreport.md` (C-6) | CRITICAL | Zenith |
| Account-Borrow Runtime DoS | Double mutable borrow blocks liquidation path | `reports/ZenithReports/fluidreport.md` (H-3) | HIGH | Zenith |
| Liquidation State Cleanup Omission | Full liquidation leaves stale debt in position state | `reports/ZenithReports/fluidreport.md` (H-2) | HIGH | Zenith |
| Account-List Ceiling DoS | Branch-heavy operations exceed Solana account limits | `reports/ZenithReports/fluidreport.md` (H-1) | HIGH | Zenith |

### Treehouse Policy & Configuration Vulnerabilities
| Category | Report | Path | Severity | Audit Firm |
|----------|--------|------|----------|------------|
| Upgradeable Program Whitelist Bypass | CPI digest policy can be bypassed after program upgrade | `reports/ZenithReports/Treehousereport.md` (M-1) | MEDIUM | Zenith |
| Withdraw Authority Misconfiguration Lockout | Non-queue `withdraw_authority` can strand user withdrawals | `reports/ZenithReports/Treehousereport.md` (L-2) | LOW | Zenith |
| Retroactive Fee Parameter Effect | `set_fees` applies new rates to prior accrual period | `reports/ZenithReports/Treehousereport.md` (L-6) | LOW | Zenith |

### External Links
- [Solana Program Security Course](https://solana.com/developers/courses/program-security)
- [Neodyme Common Pitfalls](https://neodyme.io/en/blog/solana_common_pitfalls/)
- [Zellic Anchor Vulnerabilities](https://www.zellic.io/blog/the-vulnerabilities-youll-write-with-anchor/)
- [Helius Security Guide](https://www.helius.dev/blog/a-hitchhikers-guide-to-solana-program-security)
- [SlowMist Solana Best Practices](https://github.com/slowmist/solana-smart-contract-security-best-practices)
- [Token-2022 Security Part 1](https://blog.offside.io/p/token-2022-security-best-practices-part-1)
- [Token-2022 Security Part 2](https://blog.offside.io/p/token-2022-security-best-practices-part-2)

---

# Solana Program Security Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Solana Program Security Audits**

---

## Table of Contents

1. [Account Validation Vulnerabilities](#1-account-validation-vulnerabilities)
2. [Account Data Reallocation Vulnerabilities](#2-account-data-reallocation-vulnerabilities)
3. [Lamports Transfer from PDA Vulnerabilities](#3-lamports-transfer-from-pda-vulnerabilities)
4. [CPI (Cross-Program Invocation) Vulnerabilities](#4-cpi-cross-program-invocation-vulnerabilities)
5. [Unvalidated Account Vulnerabilities](#5-unvalidated-account-vulnerabilities)
6. [Account Reloading Vulnerabilities](#6-account-reloading-vulnerabilities)
7. [Account Closure Vulnerabilities](#7-account-closure-vulnerabilities)
8. [DOS Attack Vectors](#8-dos-attack-vectors)
9. [Mint & Token Extension Vulnerabilities](#9-mint--token-extension-vulnerabilities)
10. [Event Emission Vulnerabilities](#10-event-emission-vulnerabilities)
11. [Arithmetic and Data Handling Vulnerabilities](#11-arithmetic-and-data-handling-vulnerabilities)
12. [Seed Collision Vulnerabilities](#12-seed-collision-vulnerabilities)
13. [Account Type Confusion Vulnerabilities](#13-account-type-confusion-vulnerabilities)
14. [Ed25519 Instruction Introspection Vulnerabilities](#14-ed25519-instruction-introspection-vulnerabilities)
15. [Signature Replay Attack Vulnerabilities](#15-signature-replay-attack-vulnerabilities)
16. [Unrestricted CPI Vulnerabilities](#16-unrestricted-cpi-vulnerabilities)
17. [Initialization Front-Running Vulnerabilities](#17-initialization-front-running-vulnerabilities)
18. [Create Account Pre-Funding DOS](#18-create-account-pre-funding-dos)
19. [Rent Exemption Validation Errors](#19-rent-exemption-validation-errors)
20. [Liquidation and State Invariant Vulnerabilities](#20-liquidation-and-state-invariant-vulnerabilities)
21. [CPI Policy and Program Upgradeability Bypass](#21-cpi-policy-and-program-upgradeability-bypass)

---

## 1. Account Validation Vulnerabilities

### Overview

Solana programs must validate accounts passed to instructions. Unlike EVM where msg.sender is implicitly available, Solana requires explicit validation of signer authority, account ownership, PDA derivation, and write permissions. Missing any of these validations can lead to unauthorized access and fund theft.

> **📚 Source References:**
> - [Neodyme Blog - Missing Signer Check](https://neodyme.io/en/blog/solana_common_pitfalls/#missing-signer-check)
> - [Neodyme Blog - Missing Ownership Check](https://neodyme.io/en/blog/solana_common_pitfalls/#missing-ownership-check)
> - [Solana Security Course](https://solana.com/developers/courses/program-security)



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of missing_access_control"
- Pattern key: `missing_access_control | account_validation | solana_program_integration`
- Interaction scope: `multi_contract`
- Primary affected component(s): `account_validation|cpi|token_operations|state_management`
- High-signal code keywords: `account_closure`, `account_reallocation`, `borrow`, `bump_seed`, `collisions`, `cpi_accounts`, `deposit`, `emitted`
- Typical sink / impact: `fund_theft|unauthorized_access|dos|state_corruption|account_takeover`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `N/A`
- Trust boundary crossed: `callback / external call`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: State-changing function lacks `onlyOwner`/`onlyRole` modifier
- Signal 2: External function accepts arbitrary address and calls interface methods without registry validation
- Signal 3: Configuration setter is callable by non-owner accounts
- Signal 4: Initialization or migration function is unprotected

#### False Positive Guards

- Not this bug when: Function is `internal`/`private` and only called from access-controlled paths
- Safe if: Function is restricted via `onlyOwner`/`onlyRole`/`require(msg.sender == ...)`
- Requires attacker control of: specific conditions per pattern

### Vulnerability Description

#### Root Cause

Programs fail to verify that:
1. **Signer**: The account actually signed the transaction
2. **Owner**: The account is owned by the expected program
3. **PDA**: The account matches the expected program-derived address
4. **Writer**: The account is writable when modifications are needed

#### Attack Scenario

1. Attacker crafts a transaction with malicious accounts
2. Program accepts accounts without proper validation
3. Attacker gains unauthorized access to restricted functions
4. Fund theft, state corruption, or privilege escalation occurs

### Vulnerable Pattern Examples

**Example 1: Missing Signer Check** [CRITICAL]
> 📖 Reference: [Neodyme Blog](https://neodyme.io/en/blog/solana_common_pitfalls/#missing-signer-check)
```rust
// ❌ VULNERABLE: No signer validation - anyone can call as any account
pub fn withdraw(ctx: Context<Withdraw>, amount: u64) -> Result<()> {
    let account = ctx.accounts.authority;  // Not verified as signer!
    
    // Transfer funds using unverified authority
    transfer_funds(ctx.accounts.vault, ctx.accounts.recipient, amount)?;
    Ok(())
}
```

**Example 2: Missing Owner Check** [HIGH]
> 📖 Reference: [Neodyme Blog](https://neodyme.io/en/blog/solana_common_pitfalls/#missing-ownership-check)
```rust
// ❌ VULNERABLE: Account ownership not verified
pub fn process(ctx: Context<Process>) -> Result<()> {
    let account = ctx.accounts.data_account;  // Could be owned by any program!
    
    // Deserialize and use data from potentially malicious account
    let data = MyData::try_from_slice(&account.data.borrow())?;
    // ... use data
    Ok(())
}
```

**Example 3: Missing PDA Validation** [HIGH]
```rust
// ❌ VULNERABLE: PDA not verified against expected seeds
pub fn update_config(ctx: Context<UpdateConfig>) -> Result<()> {
    let pda = ctx.accounts.config_pda;  // Not validated!
    
    // Attacker can pass any account as config_pda
    let mut config = Config::try_from_slice(&pda.data.borrow())?;
    config.admin = ctx.accounts.new_admin.key();
    // ... save config
    Ok(())
}
```

**Example 4: Missing Writer Check** [MEDIUM]
```rust
// ❌ VULNERABLE: Attempting to modify non-writable account
pub fn update_balance(ctx: Context<UpdateBalance>, amount: u64) -> Result<()> {
    let account = ctx.accounts.account;  // Not verified as writable!
    
    // This will cause runtime failure if account is not writable
    account.balance = amount;
    Ok(())
}
```

### Impact Analysis

#### Technical Impact
- Unauthorized state modifications
- Arbitrary account data injection
- PDA impersonation attacks
- Runtime failures from write attempts on read-only accounts

#### Business Impact
- Direct fund theft from protocol vaults
- Complete protocol compromise via admin takeover
- Loss of user funds and trust
- Potential protocol insolvency

#### Affected Scenarios
- Admin functions without proper authorization
- Token vaults with missing ownership checks
- Configuration updates without PDA validation
- Any state-modifying instruction

### Secure Implementation

**Fix 1: Signer Check - Native Rust**
```rust
// ✅ SECURE: Explicit signer validation
pub fn withdraw(ctx: Context<Withdraw>, amount: u64) -> Result<()> {
    let authority = &ctx.accounts.authority;
    
    // Verify signer
    require!(authority.is_signer, ErrorCode::MissingSigner);
    
    transfer_funds(ctx.accounts.vault, ctx.accounts.recipient, amount)?;
    Ok(())
}
```

**Fix 2: Signer Check - Anchor**
```rust
// ✅ SECURE: Anchor constraint for signer
#[derive(Accounts)]
pub struct Withdraw<'info> {
    pub authority: Signer<'info>,  // Anchor validates signer automatically
    
    // Or with explicit constraint
    #[account(
        constraint = authority.is_signer @ ErrorCode::MissingSigner
    )]
    pub authority_alt: AccountInfo<'info>,
}
```

**Fix 3: Owner Check - Native Rust**
```rust
// ✅ SECURE: Explicit owner validation
pub fn process(ctx: Context<Process>) -> Result<()> {
    let account = &ctx.accounts.data_account;
    
    // Verify owner
    require!(
        account.owner == ctx.program_id,
        ErrorCode::InvalidOwner
    );
    
    let data = MyData::try_from_slice(&account.data.borrow())?;
    Ok(())
}
```

**Fix 4: Owner Check - Anchor**
```rust
// ✅ SECURE: Anchor Account type validates owner automatically
#[derive(Accounts)]
pub struct Process<'info> {
    // Account<'info, T> automatically validates owner == program_id
    pub data_account: Account<'info, MyData>,
    
    // For system-owned accounts
    pub token_program: Program<'info, Token>,
}
```

**Fix 5: PDA Validation - Native Rust**
```rust
// ✅ SECURE: Explicit PDA validation
pub fn update_config(ctx: Context<UpdateConfig>) -> Result<()> {
    let pda = &ctx.accounts.config_pda;
    
    // Derive expected PDA and verify
    let (expected_pda, _bump) = Pubkey::find_program_address(
        &[b"config", ctx.accounts.authority.key().as_ref()],
        ctx.program_id
    );
    require!(pda.key() == expected_pda, ErrorCode::InvalidPDA);
    
    Ok(())
}
```

**Fix 6: PDA Validation - Anchor**
```rust
// ✅ SECURE: Anchor seeds constraint validates PDA
#[derive(Accounts)]
pub struct UpdateConfig<'info> {
    #[account(
        seeds = [b"config", authority.key().as_ref()],
        bump,
    )]
    pub config_pda: Account<'info, Config>,
    
    pub authority: Signer<'info>,
}
```

**Fix 7: Writer Check - Anchor**
```rust
// ✅ SECURE: Anchor mut constraint
#[derive(Accounts)]
pub struct UpdateBalance<'info> {
    #[account(mut)]
    pub account: Account<'info, UserAccount>,
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- AccountInfo used without is_signer check
- AccountInfo used without owner validation
- PDA accounts without seeds verification
- Missing #[account(mut)] on modified accounts
- UncheckedAccount or AccountInfo in sensitive operations
```

#### Audit Checklist
- [ ] All authority accounts verify is_signer
- [ ] All program-owned accounts verify owner
- [ ] All PDAs validated against expected seeds
- [ ] All modified accounts marked as mutable
- [ ] No raw AccountInfo used without proper validation

---

## 2. Account Data Reallocation Vulnerabilities

### Overview

Solana allows dynamic resizing of account data through reallocation. Improper memory management during reallocation can lead to uninitialized memory access, data corruption, or security vulnerabilities.

### Vulnerability Description

#### Root Cause

Programs fail to:
1. Zero-initialize newly allocated memory regions
2. Handle allocation failures gracefully
3. Properly manage memory boundaries during resize operations

#### Attack Scenario

1. Account is reallocated to a larger size
2. New memory region contains garbage data or sensitive information
3. Program reads uninitialized memory as valid data
4. Data leakage or state corruption occurs

### Vulnerable Pattern Examples

**Example 1: Reallocation Without Zero-Initialization** [HIGH]
```rust
// ❌ VULNERABLE: New memory not zero-initialized
pub fn expand_account(account: &AccountInfo, new_size: usize) -> Result<()> {
    let current_size = account.data.borrow().len();
    account.realloc(new_size, false)?;
    
    // New memory region (current_size..new_size) contains garbage!
    Ok(())
}
```

**Example 2: Missing Error Handling** [MEDIUM]
```rust
// ❌ VULNERABLE: No error handling for reallocation failure
pub fn resize_account(account: &AccountInfo, new_size: usize) -> Result<()> {
    account.realloc(new_size, false);  // Ignores potential error!
    Ok(())
}
```

### Impact Analysis

#### Technical Impact
- Uninitialized memory access
- Data leakage from previous allocations
- Memory corruption
- Potential account takeover

#### Business Impact
- Sensitive data exposure
- State corruption leading to fund loss
- Unpredictable program behavior

### Secure Implementation

**Fix 1: Proper Memory Management**
```rust
// ✅ SECURE: Zero-initialize new memory regions
pub fn expand_account(account: &AccountInfo, new_size: usize) -> Result<()> {
    let current_size = account.data.borrow().len();
    account.realloc(new_size, false)?;
    
    if current_size < new_size {
        // Zero-initialize the new memory region
        let data = &mut account.data.borrow_mut();
        for i in current_size..new_size {
            data[i] = 0;
        }
    }
    
    Ok(())
}
```

**Fix 2: Using Built-in Zero Fill**
```rust
// ✅ SECURE: Use realloc's zero_init parameter
pub fn expand_account(account: &AccountInfo, new_size: usize) -> Result<()> {
    // true = zero-initialize new memory
    account.realloc(new_size, true)?;
    Ok(())
}
```

**Fix 3: Proper Error Handling**
```rust
// ✅ SECURE: Handle allocation failures
pub fn resize_account(account: &AccountInfo, new_size: usize) -> Result<()> {
    account.realloc(new_size, true)
        .map_err(|_| ProgramError::AccountDataTooSmall)?;
    Ok(())
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- realloc(..., false) without manual zero-initialization
- realloc() without error handling (missing ?)
- Reading data from newly allocated regions without initialization
```

#### Audit Checklist
- [ ] All realloc calls use zero_init=true OR manually zero-initialize
- [ ] All realloc calls handle errors properly
- [ ] No reading from newly allocated memory before initialization

---

## 3. Lamports Transfer from PDA Vulnerabilities

### Overview

When transferring SOL (lamports) out of a PDA, programs must ensure the PDA maintains rent-exempt status and use the correct transfer mechanism. Using incorrect patterns can cause account garbage collection or transaction failures.

### Vulnerability Description

#### Root Cause

1. Transferring lamports without checking rent-exempt threshold
2. Using system_program::transfer with signer seeds for PDA-owned transfers (incorrect)
3. Missing rent-exempt balance validation after transfer

#### Attack Scenario

1. Protocol transfers lamports out of PDA without rent check
2. PDA balance falls below rent-exempt threshold
3. Account is garbage collected by Solana runtime
4. Critical program state is lost

### Vulnerable Pattern Examples

**Example 1: Missing Rent-Exempt Check** [HIGH]
```rust
// ❌ VULNERABLE: No check for rent-exempt balance after transfer
pub fn withdraw_from_pda(ctx: Context<Withdraw>, amount: u64) -> Result<()> {
    let pda = &ctx.accounts.pda;
    
    // Could drain PDA below rent-exempt threshold!
    **pda.try_borrow_mut_lamports()? -= amount;
    **ctx.accounts.recipient.try_borrow_mut_lamports()? += amount;
    
    Ok(())
}
```

**Example 2: Using System Program Transfer for PDA** [MEDIUM]
```rust
// ❌ VULNERABLE: System program cannot deduct from non-system-owned accounts
pub fn withdraw_from_pda(ctx: Context<Withdraw>, amount: u64) -> Result<()> {
    let seeds = &[b"vault", ctx.accounts.authority.key().as_ref()];
    let signer = &[&seeds[..], &[ctx.bumps.pda]];
    
    // This will FAIL - system program can only transfer from system-owned accounts
    system_program::transfer(
        CpiContext::new_with_signer(
            ctx.accounts.system_program.to_account_info(),
            system_program::Transfer {
                from: ctx.accounts.pda.to_account_info(),
                to: ctx.accounts.recipient.to_account_info(),
            },
            signer,
        ),
        amount,
    )?;
    
    Ok(())
}
```

### Impact Analysis

#### Technical Impact
- PDA account garbage collection
- Loss of program state
- Transaction failures
- Denial of service

#### Business Impact
- Complete loss of vault funds if PDA is garbage collected
- Protocol becomes unusable
- User fund loss

### Secure Implementation

**Fix 1: Check Rent-Exempt Before Transfer**
```rust
// ✅ SECURE: Validate rent-exempt balance before transfer
pub fn withdraw_from_pda(ctx: Context<Withdraw>, amount: u64) -> Result<()> {
    let pda = &ctx.accounts.pda;
    let rent = Rent::get()?;
    let min_rent = rent.minimum_balance(pda.data_len());
    let current_lamports = pda.lamports();
    
    require!(
        current_lamports - amount >= min_rent,
        ErrorCode::InsufficientFundsForRent
    );
    
    **pda.try_borrow_mut_lamports()? -= amount;
    **ctx.accounts.recipient.try_borrow_mut_lamports()? += amount;
    
    Ok(())
}
```

**Fix 2: Use try_borrow_mut_lamports for PDA Transfers**
```rust
// ✅ SECURE: Direct lamport manipulation for program-owned accounts
pub fn withdraw_from_pda(ctx: Context<Withdraw>, amount: u64) -> Result<()> {
    let pda = &ctx.accounts.pda;
    let recipient = &ctx.accounts.recipient;
    
    // Direct lamport transfer - works for program-owned accounts
    **pda.try_borrow_mut_lamports()? -= amount;
    **recipient.try_borrow_mut_lamports()? += amount;
    
    Ok(())
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- try_borrow_mut_lamports without rent-exempt check
- system_program::transfer with PDA as source
- Missing Rent::get() before lamport transfers
```

#### Audit Checklist
- [ ] All lamport deductions from PDAs check rent-exempt balance
- [ ] Direct lamport manipulation used (not system_program::transfer) for PDAs
- [ ] Rent calculation uses correct account data length

---

## 4. CPI (Cross-Program Invocation) Vulnerabilities

### Overview

Cross-Program Invocation allows Solana programs to call other programs. Incorrect CPI handling can lead to arbitrary code execution, authorization bypass, or transaction failures.

### Vulnerability Description

#### Root Cause

1. Arbitrary program invocation without validation
2. Missing bump value in signer seeds
3. Incorrect seed order in PDA signing
4. Wrong account ordering in CPI calls

#### Attack Scenario

1. Attacker provides malicious program address
2. Program performs CPI to untrusted program
3. Malicious program executes arbitrary operations
4. Fund theft or state corruption occurs

### Vulnerable Pattern Examples

**Example 1: Arbitrary CPI** [CRITICAL]
```rust
// ❌ VULNERABLE: No validation of target program
pub fn execute_arbitrary(ctx: Context<Execute>) -> Result<()> {
    let arbitrary_program = &ctx.accounts.target_program;
    
    // Could invoke ANY program!
    arbitrary_program.invoke(
        &instruction,
        &[/* accounts */],
    )?;
    
    Ok(())
}
```

**Example 2: Missing Bump in Signer Seeds** [HIGH]
```rust
// ❌ VULNERABLE: Missing bump value causes signature verification failure
pub fn signed_transfer(ctx: Context<SignedTransfer>, amount: u64) -> Result<()> {
    let seeds = &[b"vault", ctx.accounts.authority.key().as_ref()];
    let signer = &[&seeds[..]];  // MISSING BUMP!
    
    // This will FAIL - signature cannot be verified without bump
    token::transfer(
        CpiContext::new_with_signer(
            ctx.accounts.token_program.to_account_info(),
            Transfer { /* ... */ },
            signer,
        ),
        amount,
    )?;
    
    Ok(())
}
```

**Example 3: Incorrect Seed Order** [MEDIUM]
```rust
// ❌ VULNERABLE: Wrong seed order generates different PDA
pub fn signed_operation(ctx: Context<SignedOp>) -> Result<()> {
    // Seeds in WRONG order
    let seeds = &[ctx.accounts.authority.key().as_ref(), b"vault"];  // Should be [b"vault", authority]
    let bump = ctx.bumps.vault;
    let signer = &[&seeds[..], &[bump]];
    
    // Signature verification will fail - wrong PDA
    Ok(())
}
```

**Example 4: Incorrect Account Ordering** [MEDIUM]
```rust
// ❌ VULNERABLE: Accounts passed in wrong order
pub fn process_cpi(ctx: Context<ProcessCpi>) -> Result<()> {
    let accounts = vec![
        ctx.accounts.account2.to_account_info(),  // WRONG ORDER
        ctx.accounts.account1.to_account_info(),
    ];
    
    // Target program expects account1 first
    invoke(&instruction, &accounts)?;
    
    Ok(())
}
```

### Impact Analysis

#### Technical Impact
- Arbitrary code execution via malicious programs
- Transaction failures from invalid signatures
- State corruption from wrong account usage
- Authorization bypass

#### Business Impact
- Complete protocol compromise
- Fund theft
- Denial of service
- Loss of user trust

### Secure Implementation

**Fix 1: Validate CPI Target Program**
```rust
// ✅ SECURE: Validate target program address
const KNOWN_PROGRAM_ID: Pubkey = pubkey!("KnownProgram111111111111111111111111111111");

pub fn execute_cpi(ctx: Context<Execute>) -> Result<()> {
    require!(
        ctx.accounts.target_program.key() == KNOWN_PROGRAM_ID,
        ErrorCode::InvalidProgram
    );
    
    // Safe to invoke verified program
    known_program::cpi::safe_instruction(/* ... */)?;
    
    Ok(())
}
```

**Fix 2: Anchor Program Type Validation**
```rust
// ✅ SECURE: Anchor validates program automatically
#[derive(Accounts)]
pub struct Execute<'info> {
    pub token_program: Program<'info, Token>,  // Must match Token program ID
}
```

**Fix 3: Correct Signer Seeds with Bump**
```rust
// ✅ SECURE: Include bump in signer seeds
pub fn signed_transfer(ctx: Context<SignedTransfer>, amount: u64) -> Result<()> {
    let authority_key = ctx.accounts.authority.key();
    let bump = ctx.bumps.vault;
    
    let seeds = &[b"vault", authority_key.as_ref(), &[bump]];
    let signer = &[&seeds[..]];
    
    token::transfer(
        CpiContext::new_with_signer(
            ctx.accounts.token_program.to_account_info(),
            Transfer {
                from: ctx.accounts.vault.to_account_info(),
                to: ctx.accounts.recipient.to_account_info(),
                authority: ctx.accounts.vault.to_account_info(),
            },
            signer,
        ),
        amount,
    )?;
    
    Ok(())
}
```

**Fix 4: Use Anchor CPI Types for Account Ordering**
```rust
// ✅ SECURE: Anchor CPI types ensure correct ordering
pub fn process_cpi(ctx: Context<ProcessCpi>) -> Result<()> {
    other_program::cpi::some_instruction(
        CpiContext::new(
            ctx.accounts.other_program.to_account_info(),
            other_program::cpi::SomeInstruction {
                account1: ctx.accounts.account1.to_account_info(),
                account2: ctx.accounts.account2.to_account_info(),
            },
        ),
    )?;
    
    Ok(())
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- invoke() or CpiContext::new() with unvalidated program address
- Signer seeds without bump value
- Seeds array with different order than PDA derivation
- Manual account array construction for CPI
```

#### Audit Checklist
- [ ] All CPI targets validated against known program IDs
- [ ] All signer seeds include correct bump value
- [ ] Seed order matches original PDA derivation
- [ ] Anchor CPI types used for account ordering
- [ ] No arbitrary program execution

---

## 5. Unvalidated Account Vulnerabilities

### Overview

Solana programs receive accounts as inputs that must be validated. System accounts (token program, rent, sysvars), token account properties, and remaining accounts all require proper validation.

### Vulnerability Description

#### Root Cause

1. Token program not validated against expected ID
2. Sysvar accounts not verified
3. Token account ownership not checked
4. Remaining accounts used without validation

### Vulnerable Pattern Examples

**Example 1: Unvalidated Token Program** [CRITICAL]
```rust
// ❌ VULNERABLE: Token program not validated
pub fn transfer_tokens(ctx: Context<Transfer>, amount: u64) -> Result<()> {
    let token_program = &ctx.accounts.token_program;
    
    // Could be a malicious program masquerading as token program!
    token::transfer(
        CpiContext::new(token_program.to_account_info(), /* ... */),
        amount,
    )?;
    
    Ok(())
}
```

**Example 2: Unvalidated Rent Sysvar** [MEDIUM]
```rust
// ❌ VULNERABLE: Rent account not verified
pub fn check_rent(ctx: Context<CheckRent>) -> Result<()> {
    let rent = &ctx.accounts.rent;
    
    // Could be any account - attacker controls rent calculation!
    let min_balance = rent.minimum_balance(100);
    Ok(())
}
```

**Example 3: Unvalidated Token Account Ownership** [HIGH]
```rust
// ❌ VULNERABLE: Token account owner not verified
pub fn claim_tokens(ctx: Context<Claim>) -> Result<()> {
    let token_account = &ctx.accounts.user_token_account;
    
    // Attacker could pass token account owned by someone else!
    token::transfer(/* ... */)?;
    Ok(())
}
```

**Example 4: Unvalidated Remaining Accounts** [HIGH]
```rust
// ❌ VULNERABLE: remaining_accounts used without validation
pub fn process_batch(ctx: Context<ProcessBatch>) -> Result<()> {
    for account in ctx.remaining_accounts {
        // No validation - could be any account!
        process_account(account)?;
    }
    Ok(())
}
```

**Example 5: Lamport-Based Account Existence Check** [MEDIUM]
```rust
// ❌ VULNERABLE: Lamports can be donated to uninitialized accounts
pub fn check_account_exists(account: &AccountInfo) -> bool {
    // Attacker can send lamports to make uninitialized account appear valid
    account.lamports() > 0
}
```

### Impact Analysis

#### Technical Impact
- Malicious token program execution
- Incorrect rent calculations
- Token theft via ownership confusion
- Arbitrary account processing

#### Business Impact
- Complete fund theft
- Protocol logic bypass
- State corruption

### Secure Implementation

**Fix 1: Token Program Validation - Anchor**
```rust
// ✅ SECURE: Anchor validates token program automatically
#[derive(Accounts)]
pub struct Transfer<'info> {
    pub token_program: Program<'info, Token>,  // Must be SPL Token program
    
    // For Token-2022
    pub token_2022_program: Program<'info, Token2022>,
}
```

**Fix 2: Sysvar Validation**
```rust
// ✅ SECURE: Anchor Sysvar type validates automatically
#[derive(Accounts)]
pub struct CheckRent<'info> {
    pub rent: Sysvar<'info, Rent>,
    pub clock: Sysvar<'info, Clock>,
}

// Native validation
pub fn validate_rent(rent_account: &AccountInfo) -> Result<()> {
    require!(
        rent_account.key() == sysvar::rent::ID,
        ErrorCode::InvalidRentAccount
    );
    Ok(())
}
```

**Fix 3: Token Account Ownership Validation**
```rust
// ✅ SECURE: Validate token account owner
#[derive(Accounts)]
pub struct Claim<'info> {
    #[account(
        mut,
        token::authority = user,  // Token account must be owned by user
    )]
    pub user_token_account: Account<'info, TokenAccount>,
    
    pub user: Signer<'info>,
}

// Alternative constraint syntax
#[derive(Accounts)]
pub struct ClaimAlt<'info> {
    #[account(
        constraint = user_token_account.owner == user.key() @ ErrorCode::InvalidTokenAccountOwner
    )]
    pub user_token_account: Account<'info, TokenAccount>,
    
    pub user: Signer<'info>,
}
```

**Fix 4: Validate Remaining Accounts**
```rust
// ✅ SECURE: Validate each remaining account
pub fn process_batch(ctx: Context<ProcessBatch>) -> Result<()> {
    for account in ctx.remaining_accounts {
        // Validate owner
        require!(
            account.owner == &spl_token::ID || account.owner == ctx.program_id,
            ErrorCode::InvalidAccountOwner
        );
        
        // Additional type-specific validation
        if account.owner == &spl_token::ID {
            let token_account = TokenAccount::try_deserialize(
                &mut &account.data.borrow()[..]
            )?;
            // Validate token account properties
        }
    }
    Ok(())
}
```

**Fix 5: Proper Account Existence Check**
```rust
// ✅ SECURE: Check data and owner, not just lamports
pub fn validate_token_account_exists(account: &AccountInfo) -> Result<()> {
    // Check data is not empty AND owner is token program
    require!(
        !account.data_is_empty() && account.owner == &spl_token::ID,
        ErrorCode::InvalidTokenAccount
    );
    
    let token_data = TokenAccount::try_deserialize(&mut &account.data.borrow()[..])?;
    // Now safe to use token_data
    Ok(())
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- AccountInfo for token_program without key validation
- AccountInfo for sysvars without key validation
- TokenAccount without owner constraint
- Unvalidated remaining_accounts iteration
- lamports() > 0 as existence check
```

#### Audit Checklist
- [ ] Token program validated against SPL Token/Token-2022 ID
- [ ] All sysvars use Sysvar<'info, T> type
- [ ] Token accounts verify ownership matches expected authority
- [ ] All remaining_accounts validated before use
- [ ] Account existence uses data_is_empty() and owner check

---

## 6. Account Reloading Vulnerabilities

### Overview

Solana loads account data at the start of a transaction. When a CPI modifies an account, the local copy becomes stale. Programs must reload account data after CPI calls to get the updated state.

### Vulnerability Description

#### Root Cause

After a CPI that modifies an account, the program continues using the stale local copy instead of refreshing the account data.

#### Attack Scenario

1. Program loads account state at transaction start
2. CPI call modifies the account
3. Program uses stale state for subsequent logic
4. Incorrect calculations or state transitions occur

### Vulnerable Pattern Examples

**Example 1: Stale Balance After CPI** [HIGH]
```rust
// ❌ VULNERABLE: Using stale balance after transfer
pub fn process_with_cpi(ctx: Context<Process>, amount: u64) -> Result<()> {
    // Balance at transaction start
    let initial_balance = ctx.accounts.source_token.amount;
    
    // CPI modifies the account
    token::transfer(
        CpiContext::new(/* ... */),
        amount,
    )?;
    
    // WRONG: Still using stale balance!
    let remaining = ctx.accounts.source_token.amount;  // This is STALE!
    msg!("Remaining balance: {}", remaining);  // Incorrect!
    
    Ok(())
}
```

### Impact Analysis

#### Technical Impact
- Incorrect calculations based on stale data
- Logic errors in sequential operations
- State inconsistencies

#### Business Impact
- Incorrect fee calculations
- Wrong balance tracking
- Potential fund loss from miscalculations

### Secure Implementation

**Fix 1: Reload Account After CPI**
```rust
// ✅ SECURE: Reload account after CPI
pub fn process_with_cpi(ctx: Context<Process>, amount: u64) -> Result<()> {
    // CPI modifies the account
    token::transfer(
        CpiContext::new(/* ... */),
        amount,
    )?;
    
    // Reload the account to get fresh state
    ctx.accounts.source_token.reload()?;
    
    // Now using current state
    let remaining = ctx.accounts.source_token.amount;
    msg!("Remaining balance: {}", remaining);  // Correct!
    
    Ok(())
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Account field access after CPI without reload()
- Multiple CPIs on same account without intermediate reloads
- Balance/state checks after token transfers
```

#### Audit Checklist
- [ ] All accounts modified by CPI are reloaded before subsequent use
- [ ] State-dependent logic follows reload() calls
- [ ] No stale data used in calculations post-CPI

---

## 7. Account Closure Vulnerabilities

### Overview

Closing Solana accounts requires careful handling to prevent unauthorized closures, fund misdirection, and data leakage. Improper closure can lead to fund theft or denial of service.

### Vulnerability Description

#### Root Cause

1. Missing authorization for account closure
2. Unvalidated lamport recipient
3. Data not cleared before closure
4. Missing owner validation

### Vulnerable Pattern Examples

**Example 1: Missing Authorization** [CRITICAL]
```rust
// ❌ VULNERABLE: No authorization check for closure
pub fn close_account(ctx: Context<CloseAccount>) -> Result<()> {
    let account = &ctx.accounts.account_to_close;
    let destination = &ctx.accounts.destination;
    
    // Anyone can close any account!
    **destination.try_borrow_mut_lamports()? += account.lamports();
    **account.try_borrow_mut_lamports()? = 0;
    
    Ok(())
}
```

**Example 2: Unvalidated Destination** [HIGH]
```rust
// ❌ VULNERABLE: Destination not validated
pub fn close_account(ctx: Context<CloseAccount>) -> Result<()> {
    let account = &ctx.accounts.account_to_close;
    let destination = &ctx.accounts.destination;  // Could be attacker's account!
    
    // Funds go to unverified destination
    **destination.try_borrow_mut_lamports()? += account.lamports();
    **account.try_borrow_mut_lamports()? = 0;
    
    Ok(())
}
```

### Impact Analysis

#### Technical Impact
- Unauthorized account closures
- Fund theft via destination manipulation
- Data leakage from non-zeroed memory

#### Business Impact
- Direct fund theft
- Loss of critical program state
- Denial of service

### Secure Implementation

**Fix 1: Anchor Close Constraint**
```rust
// ✅ SECURE: Anchor handles closure safely
#[derive(Accounts)]
pub struct CloseAccount<'info> {
    #[account(mut)]
    pub destination: SystemAccount<'info>,
    
    #[account(
        mut,
        close = destination,  // Anchor clears data and transfers lamports
        constraint = account_to_close.authority == authority.key() @ ErrorCode::Unauthorized
    )]
    pub account_to_close: Account<'info, MyAccount>,
    
    pub authority: Signer<'info>,
}
```

**Fix 2: Validate Destination**
```rust
// ✅ SECURE: Validate destination matches authority
#[derive(Accounts)]
pub struct CloseAccount<'info> {
    #[account(
        mut,
        constraint = destination.key() == authority.key() @ ErrorCode::InvalidDestination
    )]
    pub destination: SystemAccount<'info>,
    
    #[account(
        mut,
        close = destination,
    )]
    pub account_to_close: Account<'info, MyAccount>,
    
    pub authority: Signer<'info>,
}
```

**Fix 3: Manual Safe Closure**
```rust
// ✅ SECURE: Manual closure with proper validation
pub fn close_account(ctx: Context<CloseAccount>) -> Result<()> {
    let account = &ctx.accounts.account_to_close;
    let destination = &ctx.accounts.destination;
    let authority = &ctx.accounts.authority;
    
    // Verify authority
    let account_data = MyAccount::try_deserialize(&mut &account.data.borrow()[..])?;
    require!(account_data.authority == authority.key(), ErrorCode::Unauthorized);
    
    // Verify destination
    require!(destination.key() == authority.key(), ErrorCode::InvalidDestination);
    
    // Transfer lamports
    **destination.try_borrow_mut_lamports()? += account.lamports();
    **account.try_borrow_mut_lamports()? = 0;
    
    // Clear data
    let mut data = account.try_borrow_mut_data()?;
    for byte in data.iter_mut() {
        *byte = 0;
    }
    
    Ok(())
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- close = destination without authority validation
- lamports transfer without destination validation
- Missing data clearing on closure
- No authorization check before closure
```

#### Audit Checklist
- [ ] All closures verify authority/owner
- [ ] Destination address validated (usually should be authority)
- [ ] Data cleared before closure
- [ ] Anchor close constraint used where possible

---

## 8. DOS Attack Vectors

### Overview

Denial of Service attacks on Solana can exploit account initialization patterns, front-running, and resource exhaustion. Common vectors include ATA pre-creation and account front-running.

### Vulnerability Description

#### Root Cause

1. Using `init` instead of `init_if_needed` for ATA creation
2. Predictable PDA seeds allowing front-running
3. Resource exhaustion through account spam

### Vulnerable Pattern Examples

**Example 1: Init vs Init-If-Needed for ATA** [HIGH]
> 📖 Reference: [Code4rena Pump Science](https://code4rena.com/reports/2025-01-pump-science#h-01-the-lock_pool-operation-can-be-dos)
```rust
// ❌ VULNERABLE: init fails if account exists
#[derive(Accounts)]
pub struct CreateAta<'info> {
    #[account(
        init,  // FAILS if ATA already exists!
        payer = user,
        associated_token::mint = mint,
        associated_token::authority = user,
    )]
    pub token_account: Account<'info, TokenAccount>,
}
```

**Example 2: Predictable PDA Front-Running** [HIGH]
```rust
// ❌ VULNERABLE: Predictable seeds allow front-running
#[derive(Accounts)]
pub struct CreateUserAccount<'info> {
    #[account(
        init,  // Attacker can create this first!
        payer = user,
        space = 8 + UserAccount::LEN,
        seeds = [b"user", user.key().as_ref()],
        bump
    )]
    pub user_account: Account<'info, UserAccount>,
}
```

### Impact Analysis

#### Technical Impact
- Transaction failures for legitimate users
- Front-running of account creation
- Resource exhaustion

#### Business Impact
- Denial of service for users
- Failed critical operations
- Poor user experience

### Secure Implementation

**Fix 1: Use init_if_needed for ATAs**
```rust
// ✅ SECURE: Handles existing accounts gracefully
#[derive(Accounts)]
pub struct CreateAta<'info> {
    #[account(
        init_if_needed,  // Creates only if doesn't exist
        payer = user,
        associated_token::mint = mint,
        associated_token::authority = user,
    )]
    pub token_account: Account<'info, TokenAccount>,
}
```

**Fix 2: Validate Pre-Created Accounts**
```rust
// ✅ SECURE: Handle pre-created accounts with validation
#[derive(Accounts)]
pub struct CreateUserAccount<'info> {
    #[account(
        init_if_needed,
        payer = user,
        space = 8 + UserAccount::LEN,
        seeds = [b"user", user.key().as_ref()],
        bump,
        // Validate if account exists
        constraint = user_account.to_account_info().data_is_empty() 
            || user_account.owner == program_id @ ErrorCode::InvalidOwner
    )]
    pub user_account: Account<'info, UserAccount>,
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- init constraint on ATAs
- init constraint on predictable PDAs
- No handling for pre-existing accounts
```

#### Audit Checklist
- [ ] ATAs use init_if_needed
- [ ] Predictable PDAs use init_if_needed with validation
- [ ] Front-running scenarios considered
- [ ] Critical operations handle account pre-creation

---

## 9. Mint & Token Extension Vulnerabilities

### Overview

Token-2022 introduces extensions that change token behavior. Programs must validate mint properties and handle extensions like transfer fees, freeze authority, and close authority properly.

### Vulnerability Description

#### Root Cause

1. Not checking for close authority extension
2. Ignoring freeze authority presence
3. Improper handling of transfer fee extension

### Vulnerable Pattern Examples

**Example 1: Missing Close Authority Check** [MEDIUM]
```rust
// ❌ VULNERABLE: Mint could be closed, invalidating tokens
pub fn accept_mint(ctx: Context<AcceptMint>) -> Result<()> {
    let mint = &ctx.accounts.mint;
    
    // Not checking if mint has close authority!
    // Mint could be closed, making tokens worthless
    
    Ok(())
}
```

**Example 2: Missing Freeze Authority Check** [MEDIUM]
```rust
// ❌ VULNERABLE: Tokens could be frozen, blocking transfers
pub fn accept_collateral(ctx: Context<AcceptCollateral>) -> Result<()> {
    let mint = &ctx.accounts.mint;
    
    // Not checking freeze authority!
    // User tokens could be frozen at any time
    
    Ok(())
}
```

**Example 3: Fee-on-Transfer Not Handled** [MEDIUM]
> 📖 Reference: [SPL Token-2022 Transfer Fees](https://spl.solana.com/token-2022/extensions#transfer-fees)
```rust
// ❌ VULNERABLE: Fee-on-transfer tokens cause accounting errors
pub fn transfer_tokens(ctx: Context<Transfer>, amount: u64) -> Result<()> {
    // Using basic transfer with fee-enabled token
    // Recipient receives less than 'amount'!
    token::transfer(
        CpiContext::new(/* ... */),
        amount,  // Fee is deducted, but amount is recorded as-is
    )?;
    
    Ok(())
}
```

### Impact Analysis

#### Technical Impact
- Tokens become worthless if mint closed
- Transfer restrictions from frozen accounts
- Accounting errors from transfer fees

#### Business Impact
- User fund lock-up
- Incorrect balances
- Protocol insolvency from fee miscalculation

### Secure Implementation

**Fix 1: Check Close Authority**
```rust
// ✅ SECURE: Validate no close authority on mint
pub fn accept_mint(ctx: Context<AcceptMint>) -> Result<()> {
    let mint = &ctx.accounts.mint;
    
    // Check for close authority extension
    let close_authority = get_extension::<CloseAuthority>(&mint.to_account_info())?;
    require!(
        close_authority.is_none() || close_authority.unwrap().close_authority == OptionalNonZeroPubkey::default(),
        ErrorCode::UnexpectedCloseAuthority
    );
    
    Ok(())
}
```

**Fix 2: Check Freeze Authority**
```rust
// ✅ SECURE: Validate no freeze authority
pub fn accept_collateral(ctx: Context<AcceptCollateral>) -> Result<()> {
    let mint = &ctx.accounts.mint;
    
    require!(
        mint.freeze_authority.is_none(),
        ErrorCode::UnexpectedFreezeAuthority
    );
    
    Ok(())
}
```

**Fix 3: Handle Transfer Fees**
```rust
// ✅ SECURE: Use transfer_checked for fee-enabled tokens
pub fn transfer_tokens(ctx: Context<Transfer>, amount: u64) -> Result<()> {
    token::transfer_checked(
        CpiContext::new(/* ... */),
        amount,
        ctx.accounts.mint.decimals,
    )?;
    
    Ok(())
}

// Or calculate net amount
pub fn transfer_with_fee_awareness(ctx: Context<Transfer>, amount: u64) -> Result<()> {
    let fee = calculate_transfer_fee(&ctx.accounts.mint, amount)?;
    let net_amount = amount - fee;
    
    // Record net_amount, not amount
    ctx.accounts.state.received_amount = net_amount;
    
    Ok(())
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Mint accepted without close_authority check
- Mint accepted without freeze_authority check
- token::transfer used with Token-2022 mints
- Amount recorded without fee consideration
```

#### Audit Checklist
- [ ] Close authority validated on mints
- [ ] Freeze authority checked when relevant
- [ ] Transfer fees handled in accounting
- [ ] transfer_checked used for Token-2022

---

## 10. Event Emission Vulnerabilities

### Overview

Events in Solana provide transparency for off-chain systems. Missing or incorrect events can mislead users and monitoring systems.

### Vulnerability Description

#### Root Cause

1. Emitting incorrect data in events
2. Missing events for critical state changes
3. Event data not matching actual state

### Vulnerable Pattern Examples

**Example 1: Wrong Event Data** [MEDIUM]
```rust
// ❌ VULNERABLE: Event reports wrong amount
pub fn transfer_with_fee(ctx: Context<Transfer>, amount: u64, fee: u64) -> Result<()> {
    let net_amount = amount - fee;
    
    // Transfer net amount
    transfer(ctx, net_amount)?;
    
    // WRONG: Event reports gross amount, not net
    emit!(TransferEvent {
        from: ctx.accounts.sender.key(),
        to: ctx.accounts.receiver.key(),
        amount: amount,  // Should be net_amount!
    });
    
    Ok(())
}
```

**Example 2: Missing Critical Event** [LOW]
```rust
// ❌ VULNERABLE: No event for admin change
pub fn update_admin(ctx: Context<UpdateAdmin>) -> Result<()> {
    ctx.accounts.state.admin = ctx.accounts.new_admin.key();
    
    // No event emitted for critical change!
    
    Ok(())
}
```

### Secure Implementation

**Fix 1: Accurate Event Data**
```rust
// ✅ SECURE: Event reports accurate data
pub fn transfer_with_fee(ctx: Context<Transfer>, amount: u64, fee: u64) -> Result<()> {
    let net_amount = amount - fee;
    
    transfer(ctx, net_amount)?;
    
    emit!(TransferEvent {
        from: ctx.accounts.sender.key(),
        to: ctx.accounts.receiver.key(),
        amount: net_amount,
        fee: fee,
    });
    
    Ok(())
}
```

**Fix 2: Emit Events for Critical Changes**
```rust
// ✅ SECURE: Event for critical state change
pub fn update_admin(ctx: Context<UpdateAdmin>) -> Result<()> {
    let old_admin = ctx.accounts.state.admin;
    ctx.accounts.state.admin = ctx.accounts.new_admin.key();
    
    emit!(AdminChangedEvent {
        old_admin: old_admin,
        new_admin: ctx.accounts.new_admin.key(),
        timestamp: Clock::get()?.unix_timestamp,
    });
    
    Ok(())
}
```

---

## 11. Arithmetic and Data Handling Vulnerabilities

### Overview

Rust by default checks for overflow in debug builds but not in release. Solana programs must use checked arithmetic and proper type casting to prevent overflows, underflows, and precision loss.

### Vulnerability Description

#### Root Cause

1. Unchecked arithmetic operations
2. Division by zero
3. Precision loss in calculations
4. Unsafe type casting
5. Improper rounding

### Vulnerable Pattern Examples

**Example 1: Unchecked Arithmetic** [HIGH]
> 📖 Reference: [Neodyme Blog](https://neodyme.io/en/blog/solana_common_pitfalls/#integer-overflow--underflow)
```rust
// ❌ VULNERABLE: Can overflow in release builds
pub fn add_balance(balance: u64, amount: u64) -> u64 {
    balance + amount  // OVERFLOW possible!
}
```

**Example 2: Division by Zero** [HIGH]
```rust
// ❌ VULNERABLE: Division by zero panics
pub fn calculate_share(total: u64, divisor: u64) -> u64 {
    total / divisor  // PANIC if divisor is 0!
}
```

**Example 3: Unsafe Type Casting** [MEDIUM]
```rust
// ❌ VULNERABLE: Truncation on cast
pub fn unsafe_cast(big_num: u128) -> u64 {
    big_num as u64  // Truncates without warning!
}
```

### Impact Analysis

#### Technical Impact
- Integer overflow/underflow
- Division by zero panics
- Data truncation
- Precision loss

#### Business Impact
- Incorrect calculations
- Fund loss
- Transaction failures

### Secure Implementation

**Fix 1: Checked Arithmetic**
```rust
// ✅ SECURE: Checked operations
pub fn add_balance(balance: u64, amount: u64) -> Result<u64> {
    balance.checked_add(amount)
        .ok_or(ProgramError::ArithmeticOverflow.into())
}
```

**Fix 2: Safe Division**
```rust
// ✅ SECURE: Check for zero before division
pub fn calculate_share(total: u64, divisor: u64) -> Result<u64> {
    require!(divisor > 0, ErrorCode::DivisionByZero);
    Ok(total / divisor)
}
```

**Fix 3: Safe Type Casting**
```rust
// ✅ SECURE: TryFrom for safe casting
pub fn safe_cast(big_num: u128) -> Result<u64> {
    u64::try_from(big_num)
        .map_err(|_| ErrorCode::CastOverflow.into())
}
```

**Fix 4: Cargo.toml Configuration**
```toml
# ✅ SECURE: Enable overflow checks in release builds
[profile.release]
overflow-checks = true
```

---

## 12. Seed Collision Vulnerabilities

### Overview

PDA seeds must be carefully designed to prevent collisions. When two different sets of seeds can generate the same PDA, account confusion and security vulnerabilities occur.

### Vulnerability Description

#### Root Cause

1. Simple/short seed prefixes
2. User-controlled seed data without uniqueness
3. Missing contextual data in seeds
4. Overlapping seed spaces between different account types

### Vulnerable Pattern Examples

**Example 1: Simple Colliding Seeds** [HIGH]
```rust
// ❌ VULNERABLE: Vote sessions and user votes could collide
#[account(
    seeds = [b"vote", session_id.as_bytes()],
    bump
)]
pub vote_account: Account<'info, VoteAccount>,

// Different instruction with potentially colliding seeds
#[account(
    seeds = [b"vote", user_vote_id.as_bytes()],  // Could match session_id!
    bump
)]
pub user_vote: Account<'info, UserVote>,
```

### Impact Analysis

#### Technical Impact
- Account confusion
- Wrong account accessed
- State corruption

#### Business Impact
- Denial of service
- Data integrity issues
- Potential fund loss

### Secure Implementation

**Fix 1: Unique Prefixes and Context**
```rust
// ✅ SECURE: Distinct prefixes and full context
#[account(
    seeds = [b"vote_session", organizer.key().as_ref(), session_id.as_bytes()],
    bump
)]
pub vote_session: Account<'info, VoteSession>,

#[account(
    seeds = [b"user_vote", session_id.as_bytes(), voter.key().as_ref()],
    bump
)]
pub user_vote: Account<'info, UserVote>,
```

**Fix 2: Include Nonce for Uniqueness**
```rust
// ✅ SECURE: Nonce ensures uniqueness
#[account(
    seeds = [b"account", user.key().as_ref(), &nonce.to_le_bytes()],
    bump
)]
pub user_account: Account<'info, UserAccount>,
```

### Detection Patterns

#### Code Patterns to Look For
```
- Short or common seed prefixes (b"user", b"vote", b"data")
- User-controlled seeds without additional context
- Multiple account types with similar seed structures
- Missing pubkey in seeds for user-specific accounts
```

#### Audit Checklist
- [ ] Each account type has unique seed prefix
- [ ] User-specific accounts include user pubkey in seeds
- [ ] Session/instance accounts include creator pubkey
- [ ] No overlapping seed patterns between account types

---

## 13. Account Type Confusion Vulnerabilities

### Overview

Account type confusion occurs when a program deserializes account data without verifying the account's discriminator, allowing attackers to pass accounts of different types that happen to have compatible memory layouts.

> **📚 Source Report:**
> - `reports/solana_findings/account-type-confusion.md` (OtterSec - Infinex)

### Vulnerability Description

#### Root Cause

- Using raw Borsh deserialization instead of Anchor's `try_deserialize`
- Not checking the 8-byte discriminator at account start
- Accepting accounts based solely on size compatibility
- Different account types with same owner program

### Vulnerable Pattern Example

**Missing Discriminator Check** [MEDIUM]
```rust
// ❌ VULNERABLE: Uses Borsh deserialize without discriminator check
fn load_security_key(
    wallet_info: &WalletInfo,
    account_idx: usize,
    remaining_accounts: &[AccountInfo],
) -> Result<SecurityKeyV1> {
    let info = &remaining_accounts[account_idx];
    // Skips 8 bytes but doesn't verify discriminator!
    let key_account = SecurityKeyV1::deserialize(&mut &info.data.borrow_mut()[8..])
        .map_err(|_| error!(AuthorizerError::InvalidSecurityKeyAccount))?;
    Ok(key_account)
}
```

### Secure Implementation

```rust
// ✅ SECURE: Use Anchor's try_deserialize with discriminator check
fn load_security_key(
    account_info: &AccountInfo,
) -> Result<SecurityKeyV1> {
    let key_account = SecurityKeyV1::try_deserialize(
        &mut &account_info.data.borrow()[..]
    )?;
    Ok(key_account)
}
```

---

## 14. Ed25519 Instruction Introspection Vulnerabilities

### Overview

Programs that verify Ed25519 signatures by inspecting the instruction sysvar can be exploited if they don't properly validate the Ed25519 instruction's structure, offsets, and inline mode.

> **📚 Source Report:**
> - `reports/solana_findings/c-02-wrongoffset-ed25519-instruction-introspection-enables-forged-approvals.md` (Pashov - Enclave)

### Vulnerability Description

#### Root Cause

The Ed25519 program on Solana is flexible - it can read signature, public key, and message from different instruction indexes and offsets. If a contract doesn't validate:
1. Previous instruction's program_id is the Ed25519 program
2. Inline mode is enforced (index fields = 0xFFFF)
3. Offsets point to expected data ranges
4. Only one signature exists

Attackers can craft malicious "verification" instructions that pass your checks while verifying attacker-controlled data.

### Vulnerable Pattern Example

**Insufficient Ed25519 Verification** [CRITICAL]
```rust
// ❌ VULNERABLE: Doesn't validate Ed25519 instruction structure
pub fn borrow(ctx: Context<Borrow>, signature: [u8; 64]) -> Result<()> {
    let ix_sysvar = &ctx.accounts.instructions_sysvar;
    let prev_ix = get_instruction_relative(-1, ix_sysvar)?;
    
    // WRONG: Only checks signature bytes, not instruction structure
    let sig_data = &prev_ix.data[16..80];
    require!(sig_data == &signature, ErrorCode::InvalidSignature);
    
    // Attacker can place expected bytes at these offsets while
    // Ed25519 actually verifies different data!
    Ok(())
}
```

### Secure Implementation

```rust
// ✅ SECURE: Comprehensive Ed25519 verification
pub fn verify_ed25519_signature(
    ix_sysvar: &AccountInfo,
    expected_signer: &Pubkey,
    expected_message: &[u8],
) -> Result<()> {
    let prev_ix = get_instruction_relative(-1, ix_sysvar)?;
    
    // 1. Verify program ID is Ed25519
    require!(
        prev_ix.program_id == solana_program::ed25519_program::id(),
        ErrorCode::InvalidProgram
    );
    
    // 2. Parse Ed25519SignatureOffsets
    let offsets = Ed25519SignatureOffsets::try_from_slice(&prev_ix.data[2..18])?;
    
    // 3. Enforce inline mode (all indexes = 0xFFFF)
    require!(
        offsets.signature_instruction_index == u16::MAX &&
        offsets.public_key_instruction_index == u16::MAX &&
        offsets.message_instruction_index == u16::MAX,
        ErrorCode::NotInlineMode
    );
    
    // 4. Bounds check offsets
    let data_len = prev_ix.data.len();
    require!(
        (offsets.signature_offset as usize + 64) <= data_len &&
        (offsets.public_key_offset as usize + 32) <= data_len,
        ErrorCode::InvalidOffsets
    );
    
    // 5. Verify actual public key matches expected
    let pubkey_start = offsets.public_key_offset as usize;
    let inline_pubkey = &prev_ix.data[pubkey_start..pubkey_start + 32];
    require!(
        inline_pubkey == expected_signer.as_ref(),
        ErrorCode::WrongSigner
    );
    
    Ok(())
}
```

---

## 15. Signature Replay Attack Vulnerabilities

### Overview

Programs that accept off-chain signatures must implement proper replay protection. Without nonces or state tracking, valid signatures can be reused multiple times.

> **📚 Source Reports:**
> - `reports/solana_findings/m-31-missing-nonce-reset-during-tss-address-update-allowing-signature-replay.md` (Sherlock - ZetaChain)
> - `reports/solana_findings/successful-transactions-are-not-stored-causing-a-replay-attack-on-redeemdeposits.md` (Codehawks - Beanstalk)

### Vulnerability Description

#### Root Cause

1. No nonce tracking for signature-based operations
2. Nonce not reset when signing key changes
3. Processed signatures not stored to prevent reuse
4. Missing deadline checks on signatures

### Vulnerable Pattern Examples

**Example 1: Missing Nonce Reset on Key Update** [MEDIUM]
```rust
// ❌ VULNERABLE: Nonce persists across TSS key changes
pub fn update_tss(ctx: Context<UpdateTss>, tss_address: [u8; 20]) -> Result<()> {
    let pda = &mut ctx.accounts.pda;
    pda.tss_address = tss_address;  // Key updated
    // pda.nonce NOT reset - old signatures could replay!
    Ok(())
}
```

**Example 2: No Replay Tracking** [HIGH]
```rust
// ❌ VULNERABLE: Same proof can be submitted multiple times
pub fn redeem_deposits(
    ctx: Context<Redeem>,
    proof: Vec<u8>,
    deposits: Vec<Deposit>,
) -> Result<()> {
    // Verify merkle proof
    verify_merkle_proof(&proof, &deposits)?;
    
    // Process deposits - but nothing prevents replay!
    for deposit in deposits {
        transfer_tokens(&ctx, deposit)?;
    }
    
    Ok(())
}
```

### Secure Implementation

**Fix 1: Reset Nonce on Key Update**
```rust
// ✅ SECURE: Reset nonce when updating signing key
pub fn update_tss(ctx: Context<UpdateTss>, tss_address: [u8; 20]) -> Result<()> {
    let pda = &mut ctx.accounts.pda;
    pda.tss_address = tss_address;
    pda.nonce = 0;  // Reset nonce to prevent replay
    Ok(())
}
```

**Fix 2: Track Processed Operations**
```rust
// ✅ SECURE: Store processed signatures/proofs
pub fn redeem_deposits(
    ctx: Context<Redeem>,
    proof_hash: [u8; 32],
    deposits: Vec<Deposit>,
) -> Result<()> {
    // Check if already processed
    require!(
        !ctx.accounts.processed_proofs.contains(&proof_hash),
        ErrorCode::AlreadyProcessed
    );
    
    // Mark as processed
    ctx.accounts.processed_proofs.insert(proof_hash);
    
    // Now safe to process
    verify_merkle_proof(&proof_hash, &deposits)?;
    for deposit in deposits {
        transfer_tokens(&ctx, deposit)?;
    }
    
    Ok(())
}
```

---

## 16. Unrestricted CPI Vulnerabilities

### Overview

When a program passes signing authority to another program via CPI, it must carefully validate which programs can be called. Unrestricted CPI allows attackers to invoke arbitrary programs with the victim's signature.

> **📚 Source Report:**
> - `reports/solana_findings/unrestricted-marginswap-cpi.md` (OtterSec - Jet V2)

### Vulnerability Description

#### Root Cause

- Accepting arbitrary program IDs for CPI
- Passing signer seeds to untrusted adapters
- Not validating CPI target programs against allowlist
- Adapter programs that proxy to arbitrary targets

### Vulnerable Pattern Example

**Unrestricted Swap Program** [CRITICAL]
```rust
// ❌ VULNERABLE: Any swap program accepted
pub fn margin_swap(
    ctx: Context<MarginSwap>,
    amount: u64,
) -> Result<()> {
    // swap_program is user-provided and unvalidated!
    invoke_signed(
        &create_swap_instruction(
            ctx.accounts.swap_program.key(),
            amount,
        ),
        &[
            ctx.accounts.margin_account.to_account_info(),
            ctx.accounts.swap_program.to_account_info(),
        ],
        &[&ctx.accounts.margin_account.signer_seeds()],  // Signing with margin authority!
    )?;
    
    Ok(())
}
```

### Secure Implementation

```rust
// ✅ SECURE: Restrict to allowlisted programs
pub fn margin_swap(
    ctx: Context<MarginSwap>,
    amount: u64,
) -> Result<()> {
    // Validate swap program against allowlist
    let allowed_programs = [
        spl_token_swap_v2::ID,
        orca_swap_v1::ID,
        orca_swap_v2::ID,
    ];
    
    require!(
        allowed_programs.contains(&ctx.accounts.swap_program.key()),
        ErrorCode::UnauthorizedProgram
    );
    
    invoke_signed(/* ... */)?;
    
    Ok(())
}
```

---

## 17. Initialization Front-Running Vulnerabilities

### Overview

Programs with permissionless initialization can be front-run by attackers who initialize with malicious parameters before legitimate users.

> **📚 Source Reports:**
> - `reports/solana_findings/attacker-can-front-run-multisig-creation-transaction.md` (TrailOfBits - Squads v4)
> - `reports/solana_findings/m-01-any-wallet-can-self-assign-as-super_admin-for-arbitrary-mint.md` (Pashov - Pump)
> - `reports/solana_findings/permissionless-offrampstate-initialization-under-official-program-id-enables-spo.md` (Cyfrin - Securitize)

### Vulnerability Description

#### Root Cause

1. PDA seeds derived from unauthenticated accounts
2. No signer validation on initialization
3. Global state initialized permissionlessly
4. One-way configuration that can't be corrected

### Vulnerable Pattern Examples

**Example 1: Unauthenticated Create Key** [HIGH]
```rust
// ❌ VULNERABLE: create_key not required to sign
#[derive(Accounts)]
pub struct MultisigCreate<'info> {
    #[account(
        init,
        seeds = [SEED_PREFIX, SEED_MULTISIG, create_key.key().as_ref()],
        bump
    )]
    pub multisig: Account<'info, Multisig>,
    
    /// CHECK: Any random public key
    pub create_key: AccountInfo<'info>,  // Not a Signer!
}
```

**Example 2: Permissionless Admin Assignment** [MEDIUM]
```rust
// ❌ VULNERABLE: Anyone can become super_admin for any mint
#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        init,
        seeds = [SEED, mint.key().as_ref()],
        bump
    )]
    pub state: Account<'info, State>,
    
    pub mint: InterfaceAccount<'info, Mint>,  // No authority check!
    
    #[account(mut)]
    pub super_admin: Signer<'info>,  // Anyone can call this
}
```

### Secure Implementation

**Fix 1: Require Signer on Key Account**
```rust
// ✅ SECURE: create_key must sign the transaction
#[derive(Accounts)]
pub struct MultisigCreate<'info> {
    #[account(
        init,
        seeds = [SEED_PREFIX, SEED_MULTISIG, create_key.key().as_ref()],
        bump
    )]
    pub multisig: Account<'info, Multisig>,
    
    pub create_key: Signer<'info>,  // Now requires signature!
}
```

**Fix 2: Gate Behind Mint Authority**
```rust
// ✅ SECURE: Only mint authority can initialize
#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        constraint = mint.mint_authority == COption::Some(super_admin.key())
            @ ErrorCode::NotMintAuthority
    )]
    pub mint: InterfaceAccount<'info, Mint>,
    
    #[account(mut)]
    pub super_admin: Signer<'info>,
}
```

---

## 18. Create Account Pre-Funding DOS

### Overview

Solana's `system_instruction::create_account` fails if the target address already has non-zero lamports. Attackers can pre-fund PDA addresses to permanently block their creation.

> **📚 Source Report:**
> - `reports/solana_findings/create_account-can-be-dosed-with-pre-funding.md` (Cyfrin - Deriverse)

### Vulnerability Description

#### Root Cause

Using `create_account` instead of the more resilient pattern of separate fund, allocate, and assign operations.

### Vulnerable Pattern Example

**Direct Create Account** [MEDIUM]
```rust
// ❌ VULNERABLE: Fails if account already has lamports
invoke_signed(
    &system_instruction::create_account(
        payer.key,
        holder_acc.key,
        Rent::default().minimum_balance(account_size),
        account_size as u64,
        program_id,
    ),
    &[payer.clone(), holder_acc.clone()],
    &[&[HOLDER_SEED, payer.key.as_ref(), &[bump_seed]]],
)?;
```

### Secure Implementation

```rust
// ✅ SECURE: Handles pre-existing lamports
pub fn create_pda_resilient(
    payer: &AccountInfo,
    pda: &AccountInfo,
    space: usize,
    owner: &Pubkey,
    seeds: &[&[u8]],
) -> Result<()> {
    let rent = Rent::get()?;
    let required_lamports = rent.minimum_balance(space);
    
    // Fund the account (works even if it has some lamports)
    let current_lamports = pda.lamports();
    if current_lamports < required_lamports {
        invoke(
            &system_instruction::transfer(
                payer.key,
                pda.key,
                required_lamports - current_lamports,
            ),
            &[payer.clone(), pda.clone()],
        )?;
    }
    
    // Allocate space
    invoke_signed(
        &system_instruction::allocate(pda.key, space as u64),
        &[pda.clone()],
        &[seeds],
    )?;
    
    // Assign to program
    invoke_signed(
        &system_instruction::assign(pda.key, owner),
        &[pda.clone()],
        &[seeds],
    )?;
    
    Ok(())
}
```

---

## 19. Rent Exemption Validation Errors

### Overview

Programs that check SOL balances for invariants must account for rent exemption amounts. Failing to subtract rent leads to incorrect validations.

> **📚 Source Report:**
> - `reports/solana_findings/m-02-bonding-curve-invariant-check-incorrectly-validates-sol-balance-due-to-rent.md` (Code4rena - Pump Science)

### Vulnerability Description

#### Root Cause

Using `account.lamports()` (which includes rent) in comparisons with values that don't include rent.

### Vulnerable Pattern Example

**Invariant Check Without Rent** [MEDIUM]
```rust
// ❌ VULNERABLE: Compares lamports (with rent) to reserves (without rent)
pub fn check_invariant(
    sol_escrow: &AccountInfo,
    bonding_curve: &BondingCurve,
) -> Result<()> {
    let sol_escrow_lamports = sol_escrow.lamports();  // Includes rent!
    
    if sol_escrow_lamports < bonding_curve.real_sol_reserves {
        return Err(ContractError::BondingCurveInvariant.into());
    }
    // This can pass incorrectly when actual SOL < reserves
    // but rent makes up the difference
    Ok(())
}
```

### Secure Implementation

```rust
// ✅ SECURE: Subtract rent before comparison
pub fn check_invariant(
    sol_escrow: &AccountInfo,
    bonding_curve: &BondingCurve,
) -> Result<()> {
    let rent = Rent::get()?;
    let rent_exempt_amount = rent.minimum_balance(sol_escrow.data_len());
    
    let actual_sol = sol_escrow.lamports()
        .checked_sub(rent_exempt_amount)
        .ok_or(ContractError::InsufficientBalance)?;
    
    if actual_sol < bonding_curve.real_sol_reserves {
        return Err(ContractError::BondingCurveInvariant.into());
    }
    
    Ok(())
}
```

---

## 20. Liquidation and State Invariant Vulnerabilities

### Overview

Liquidation engines in Solana lending protocols often combine branch/tick state machines, dynamic remaining accounts, and oracle-derived conversion rates. The Fluid report highlights failure modes where sentinel misuse, partial-path validation, and stale state transitions can cascade into liquidation failure, bad debt misclassification, and cross-vault state corruption.

> **📚 Source Report:**
> - `reports/ZenithReports/fluidreport.md` (C-3, C-4, C-5, C-6, H-1, H-2, H-3)

### Vulnerability Description

#### Root Cause

1. **Sentinel encoding mismatch**: treating `0` as “no tick exists” even when tick `0` is valid.
2. **Conditional validation gaps**: relying on downstream CPI checks that are skipped on special branches (`debt_amt == 0`).
3. **Incomplete liquidation cleanup**: updating tick state but leaving debt fields non-zero.
4. **Unsafe arithmetic strategy**: `saturating_mul` hides overflow and yields severely discounted prices.
5. **Runtime borrowing conflicts**: overlapping mutable borrows trigger instruction failure in critical liquidation flows.

### Vulnerable Pattern Examples

**Example 1: Tick 0 Sentinel Confusion** [CRITICAL]
```rust
// ❌ VULNERABLE: 0 is treated as "no tick", but tick 0 can be valid
pub fn get_top_tick(&self) -> i32 {
    if self.topmost_tick == 0 {
        i32::MIN
    } else {
        self.topmost_tick
    }
}
```

**Example 2: Validation Bypass on Special Liquidation Path** [CRITICAL]
```rust
// ❌ VULNERABLE: reserve mint checks are assumed to happen in CPI,
// but this branch exits before CPI when debt_amt == 0
pub fn liquidate(ctx: Context<Liquidate>, debt_amt: u64) -> Result<()> {
    absorb_bad_debt(&ctx)?;

    if debt_amt == 0 {
        return Ok(()); // no downstream validation reached
    }

    cpi_to_liquidity_program(&ctx)?;
    Ok(())
}
```

**Example 3: Missing Cross-Vault ID Validation** [CRITICAL]
```rust
// ❌ VULNERABLE: account belongs to different vault but is accepted
pub fn verify_operate(ctx: &Context<Operate>) -> Result<()> {
    let tick_id_data = &ctx.accounts.tick_id_data;
    require!(tick_id_data.vault_id == ctx.accounts.vault_state.vault_id, ErrorCode::InvalidVaultId);

    // Missing equivalent check for tick_id_data_after_operate
    Ok(())
}
```

**Example 4: Saturating Overflow in Price Pipeline** [CRITICAL]
```rust
// ❌ VULNERABLE: saturation hides overflow and produces underpriced assets
rate = rate
    .saturating_mul(current_hop_rate)
    .saturating_div(10u128.pow(RATE_OUTPUT_DECIMALS));
```

**Example 5: Full Liquidation Leaves Stale Debt** [HIGH]
```rust
// ❌ VULNERABLE: full liquidation resets tick but debt is not cleared
if is_fully_liquidated {
    position_tick = i32::MIN;
    // missing: position_raw_debt = 0;
}
```

### Secure Implementation

**Fix 1: Explicit Sentinel Domain**
```rust
// ✅ SECURE: reserve i32::MIN for "no tick", allow 0 as valid tick
pub fn get_top_tick(&self) -> i32 {
    self.topmost_tick
}

pub fn reset_top_tick(&mut self) {
    self.topmost_tick = i32::MIN;
}
```

**Fix 2: Validate Before Branching**
```rust
// ✅ SECURE: enforce reserve/token-vault consistency before any early return
fn validate_reserves(vault_cfg: &VaultConfig, supply: &TokenReserve, borrow: &TokenReserve) -> Result<()> {
    require!(supply.mint == vault_cfg.supply_token, ErrorCode::InvalidSupplyReserve);
    require!(borrow.mint == vault_cfg.borrow_token, ErrorCode::InvalidBorrowReserve);
    Ok(())
}
```

**Fix 3: Checked Math for Price Conversions**
```rust
// ✅ SECURE: fail safely on overflow instead of saturating to MAX
rate = rate
    .checked_mul(current_hop_rate)
    .ok_or(ErrorCode::MathOverflow)?
    .checked_div(10u128.pow(RATE_OUTPUT_DECIMALS))
    .ok_or(ErrorCode::MathUnderflow)?;
```

### Detection Patterns

#### Code Patterns to Look For
```
- sentinel checks that map 0 -> no value for signed domains where 0 is valid
- early return branches that skip expected downstream CPI-based validation
- liquidation/full-close flows that modify tick/status but not debt/principal fields
- saturating_* arithmetic in price, collateral, or liquidation threshold calculations
- repeated mutable borrows (`load_mut`) of same account in nested liquidation helpers
```

#### Audit Checklist
- [ ] Tick sentinel encoding distinguishes "unset" from valid tick 0
- [ ] All reserve mint and vault_id checks run before path-specific early returns
- [ ] Full liquidation paths zero debt and synchronize all derived fields
- [ ] Oracle price conversion uses checked math (or wider integer types)
- [ ] Liquidation helpers avoid overlapping mutable account borrows
- [ ] Branch/tick account requirements are bounded to avoid account-count DoS

---

## 21. CPI Policy and Program Upgradeability Bypass

### Overview

Instruction-digest allowlists are only meaningful when the target program implementation is immutable. If a vault whitelists CPI operations by digest but does not enforce target-program immutability (or frozen upgrade authority), a later program upgrade can preserve digest shape while changing behavior.

> **📚 Source Report:**
> - `reports/ZenithReports/Treehousereport.md` (M-1)

### Vulnerability Description

#### Root Cause

1. CPI policy stores digest/operator rules for an instruction payload but not upgradeability guarantees for `program_id`.
2. Policy update and execution paths trust that whitelisted programs remain semantically stable.
3. Upgradeable loader programs can change code after being allowlisted.

### Vulnerable Pattern Examples

**Example 1: Digest Validation Without Upgradeability Check** [MEDIUM]
```rust
// ❌ VULNERABLE: digest checks pass, but target program may be upgradeable
pub fn update_cpi_digest(ctx: Context<UpdateCpiDigest>, digest: [u8; 32]) -> Result<()> {
    ctx.accounts.cpi_digest.digest = digest;
    // Missing: verify target program is immutable / non-upgradeable
    Ok(())
}
```

**Example 2: Execution Path Trusts Mutable Program** [MEDIUM]
```rust
// ❌ VULNERABLE: invoke path relies on stale trust from old digest registration
pub fn manage(ctx: Context<Manage>, ix_data: Vec<u8>) -> Result<()> {
    require!(matches_digest(&ctx.accounts.cpi_digest, &ix_data), ErrorCode::DigestMismatch);
    invoke_signed(&build_ix(&ctx.accounts.target_program, &ix_data), &ctx.remaining_accounts, &[])?;
    Ok(())
}
```

### Secure Implementation

**Fix 1: Enforce Immutability at Policy Registration**
```rust
// ✅ SECURE: reject upgradeable targets unless upgrade authority is None
fn validate_program_immutability(program: &AccountInfo, programdata: Option<&AccountInfo>) -> Result<()> {
    if is_builtin_program(program.key) {
        return Ok(());
    }

    require!(program.owner == &bpf_loader::ID || program.owner == &bpf_loader_deprecated::ID, ErrorCode::InvalidProgramOwner);

    if program.owner == &bpf_loader_upgradeable::ID {
        let data = read_programdata(programdata.ok_or(ErrorCode::MissingProgramData)?)?;
        require!(data.upgrade_authority_address.is_none(), ErrorCode::ProgramIsUpgradeable);
    }

    Ok(())
}
```

**Fix 2: Bind Policy to Program Identity + Mutability State**
```rust
// ✅ SECURE: store program id and immutability fingerprint with digest
pub struct CpiPolicy {
    pub program_id: Pubkey,
    pub digest: [u8; 32],
    pub immutable: bool,
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- CPI digest/allowlist updates that omit checks for bpf_loader_upgradeable ownership
- policy engines that validate instruction bytes but not target-program mutability
- comments asserting CPI safety due to digest checks alone
```

#### Audit Checklist
- [ ] Every allowlisted CPI target is immutable or has `upgrade_authority == None`
- [ ] Policy stores `program_id` and rejects digest reuse across different programs
- [ ] Built-in programs are explicitly handled as trusted immutable exceptions
- [ ] Policy updates are independent of pause-state constraints during incidents

---

## Prevention Guidelines

### Development Best Practices

1. **Always use Anchor types** (Account, Signer, Program, Sysvar) instead of raw AccountInfo
2. **Enable overflow checks** in release builds via Cargo.toml
3. **Use init_if_needed** for ATAs and predictable PDAs
4. **Reload accounts** after any CPI that modifies them
5. **Validate remaining_accounts** before processing
6. **Use unique seed prefixes** for each account type
7. **Check token extensions** when accepting Token-2022 mints
8. **Emit events** for all critical state changes
9. **Use checked arithmetic** for all calculations
10. **Validate destinations** for account closures and transfers

### Testing Requirements

- Unit tests for all validation logic
- Integration tests for CPI interactions
- Fuzzing for arithmetic operations
- Security test cases for each vulnerability pattern

---

## Keywords for Search

> These keywords enhance vector search retrieval:

`solana`, `anchor`, `spl_token`, `token_2022`, `pda`, `cpi`, `signer_check`, `owner_check`, `account_validation`, `missing_signer`, `missing_owner`, `pda_validation`, `arbitrary_cpi`, `seed_collision`, `account_closure`, `init_if_needed`, `dos_attack`, `front_running`, `account_reloading`, `stale_state`, `reallocation`, `rent_exempt`, `lamports_transfer`, `freeze_authority`, `close_authority`, `transfer_fee`, `remaining_accounts`, `bump_seed`, `signer_seeds`, `checked_arithmetic`, `overflow`, `underflow`, `type_casting`, `event_emission`, `token_program`, `system_program`, `sysvar`, `account_pre_creation`, `type_confusion`, `discriminator`, `ed25519`, `instruction_introspection`, `signature_replay`, `nonce_reset`, `unrestricted_cpi`, `adapter_program`, `initialization_frontrun`, `multisig`, `create_key`, `permissionless_init`, `pre_funding_dos`, `create_account`, `rent_inclusion`, `bonding_curve`, `invariant_check`, `canonical_bump`, `reentrancy`, `guard_bypass`, `decimal_mismatch`, `precision_manipulation`, `tss_address`, `merkle_proof`, `tick_sentinel`, `liquidation_state_cleanup`, `cross_vault_write`, `saturating_overflow`, `account_borrow_conflict`, `account_count_limit`, `cpi_digest`, `upgradeable_loader`, `program_upgrade_authority`, `policy_bypass`, `immutable_program`

---

## Related Vulnerabilities

- [Reentrancy](../general/reentrancy/) - CPI can enable reentrancy-like patterns
- [Access Control](../general/access-control/) - Account validation is Solana's access control
- [Fee-on-Transfer Tokens](../general/fee-on-transfer-tokens/) - Token-2022 specific handling

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

`account_closure`, `account_reallocation`, `account_validation`, `anchor`, `borrow`, `bump_seed`, `collisions`, `cpi`, `cpi_accounts`, `deposit`, `emitted`, `for`, `init_if_needed`, `lamports_transfer`, `liquidate`, `mint`, `msg.sender`, `overflows`, `owner_check`, `pda`, `pda_validation`, `program_security`, `receive`, `remaining_accounts`, `replay`, `signer_check`, `solana`, `solana_program_integration`, `spl_token`, `system_program`, `token_2022`, `token_program`

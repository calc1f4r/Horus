---
# Core Classification (Required)
protocol: generic
chain: solana
category: token_security
vulnerability_type: token_2022_extensions

# Attack Vector Details (Required)
attack_type: economic_exploit|data_manipulation|dos
affected_component: mint|token_account|extensions

# Solana-Specific Fields
program_type: spl_token_2022
token_extension_vector: close_authority|freeze_authority|transfer_fee|permanent_delegate|confidential_transfer|transfer_hook|interest_bearing|non_transferable|cpi_guard|memo_transfer|metadata_pointer|group_pointer

# Technical Primitives (Required)
primitives:
  - mint_close_authority
  - freeze_authority
  - transfer_fee
  - permanent_delegate
  - default_account_state
  - interest_bearing
  - non_transferable
  - confidential_transfer
  - transfer_hook
  - metadata_pointer
  - group_pointer
  - group_member_pointer
  - cpi_guard
  - memo_transfer
  - immutable_owner
  - token_account_extensions

# Impact Classification (Required)
severity: critical|high|medium|low
impact: fund_theft|dos|accounting_errors|token_manipulation
exploitability: 0.75
financial_impact: high

# Context Tags
tags:
  - solana
  - token_2022
  - spl_token
  - token_extensions
  - mint
  - defi

# Version Info
language: rust
version: all
---

## References & Source Reports

> **For Agents**: These patterns are derived from real-world audit findings. Read the referenced files for detailed context.

### MintCloseAuthority Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Mint Decimal Manipulation | `reports/token2022_findings/c-01-mint-decimal-manipulation-through-mintcloseauthority-leads-to-inflation-of-.md` | CRITICAL | Shieldify |
| Mint Decimal Attack | `reports/token2022_findings/m-01-mint-decimal-manipulation.md` | MEDIUM | Shieldify |

### Freeze Authority Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Missing Freeze Authority Check | `reports/solana_findings/m-01-lack-of-freeze-authority-check-for-collateral-tokens-on-create-trading-pool.md` | MEDIUM | Unknown |
| Freeze Authority DOS Risk | `reports/solana_findings/m-02-risk-of-input-token-mint-with-freeze-authority-leading-to-permanent-dos.md` | MEDIUM | Unknown |
| Token Escrow Freeze | `reports/solana_findings/h-01-denial-of-service-risk-due-to-frozen-token_escrow-in-onftadapter.md` | HIGH | Unknown |
| Bridge Token Freeze | `reports/solana_findings/possibility-of-freezing-any-bridge-token-account-due-to-lack-of-freeze-authority.md` | MEDIUM | Unknown |

### Transfer Fee Extension Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Fee-on-Transfer Not Handled | `reports/token2022_findings/fee-on-transfer-tokens-are-not-explicitly-denied-in-swap.md` | MEDIUM | Unknown |
| Lack of FOT Support | `reports/token2022_findings/m-33-lack-of-support-for-fee-on-transfer-token.md` | MEDIUM | Unknown |
| FeeTaker Incompatibility | `reports/token2022_findings/m-02-feetaker-is-incompatible-with-fee-on-transfer-tokens.md` | MEDIUM | Unknown |

### Token Extension Invariant Manipulation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Arbitrary Token Extensions | `reports/solana_findings/m-01-arbitrary-input-tokens-and-token-extensions-leading-to-invariant-manipulati.md` | MEDIUM | Shieldify |
| Fixed Token Account Size | `reports/solana_findings/fixed-token-account-size-causes-initialization-failures-for-token-accounts-whose.md` | MEDIUM | Unknown |
| Hard-coded Vault Size | `reports/solana_findings/hard-coded-165-byte-vault-account-is-too-small-for-raydium-token-2022-mints-with.md` | MEDIUM | Unknown |
| Token-2022 Extension Compatibility Gaps (M-5) | `reports/ZenithReports/fluidreport.md` | MEDIUM | Zenith |
| Mixed Legacy + Token-2022 Incompatibility (L-17) | `reports/ZenithReports/fluidreport.md` | LOW | Zenith |

### Permanent Delegate Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Permanent Delegate Token Drain | Illustrative Pattern - No specific report | CRITICAL | N/A |

### Interest Bearing Token Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Interest Rate Manipulation | Illustrative Pattern - No specific report | MEDIUM | N/A |

### Non-Transferable Token Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Non-Transferable Token Bypass | Illustrative Pattern - No specific report | MEDIUM | N/A |

### Token Account Closing Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Custody Token Account Closing DOS | `reports/solana_findings/custody-token-account-closing-dos.md` | HIGH | OtterSec |

### External Links
- [SPL Token-2022 Documentation](https://spl.solana.com/token-2022)
- [Token-2022 Extensions Guide](https://spl.solana.com/token-2022/extensions)
- [Token-2022 Security Part 1](https://blog.offside.io/p/token-2022-security-best-practices-part-1)
- [Token-2022 Security Part 2](https://blog.offside.io/p/token-2022-security-best-practices-part-2)

---

# Token-2022 Extension Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Token-2022 Security Audits**

---

## Table of Contents

1. [MintCloseAuthority Extension Vulnerabilities](#1-mintcloseauthority-extension-vulnerabilities)
2. [Freeze Authority Vulnerabilities](#2-freeze-authority-vulnerabilities)
3. [Transfer Fee Extension Vulnerabilities](#3-transfer-fee-extension-vulnerabilities)
4. [Permanent Delegate Extension Vulnerabilities](#4-permanent-delegate-extension-vulnerabilities)
5. [Token Account Size Vulnerabilities](#5-token-account-size-vulnerabilities)
6. [Default Account State Extension Vulnerabilities](#6-default-account-state-extension-vulnerabilities)
7. [Transfer Hook Extension Vulnerabilities](#7-transfer-hook-extension-vulnerabilities)
8. [Interest Bearing Extension Vulnerabilities](#8-interest-bearing-extension-vulnerabilities)
9. [Confidential Transfer Vulnerabilities](#9-confidential-transfer-vulnerabilities)
10. [General Token-2022 Integration Vulnerabilities](#10-general-token-2022-integration-vulnerabilities)
11. [Non-Transferable Token Extension Vulnerabilities](#11-non-transferable-token-extension-vulnerabilities)
12. [Confidential Transfer Extension Vulnerabilities (Extended)](#12-confidential-transfer-extension-vulnerabilities)
13. [Metadata Pointer Extension Vulnerabilities](#13-metadata-pointer-extension-vulnerabilities)
14. [Group and Group Member Extension Vulnerabilities](#14-group-and-group-member-extension-vulnerabilities)
15. [CPI Guard Extension Vulnerabilities](#15-cpi-guard-extension-vulnerabilities)
16. [Required Memo Extension Vulnerabilities](#16-required-memo-extension-vulnerabilities)
17. [Immutable Owner Extension Vulnerabilities](#17-immutable-owner-extension-vulnerabilities)
18. [Comprehensive Token-2022 Extension Whitelist Pattern](#18-comprehensive-token-2022-extension-whitelist-pattern)
19. [Token-2022 Account Extension Validation](#19-token-2022-account-extension-validation)

---

## 1. MintCloseAuthority Extension Vulnerabilities

### Overview

The `MintCloseAuthority` extension allows a designated authority to close a mint account when its supply is zero. This creates a critical attack vector where the mint's decimals can be manipulated after closing and recreating the mint at the same address.

> **📚 Source Reports for Deep Dive:**
> - `reports/token2022_findings/c-01-mint-decimal-manipulation-through-mintcloseauthority-leads-to-inflation-of-.md`
> - `reports/token2022_findings/m-01-mint-decimal-manipulation.md`

### Vulnerability Description

#### Root Cause

When a protocol accepts any Token-2022 mint without checking for the `MintCloseAuthority` extension:
1. Attacker creates mint with 18 decimals and MintCloseAuthority enabled
2. Protocol initializes using this mint, calculating ld2sd_rate based on 18 decimals
3. Attacker closes the mint (when supply is 0)
4. Attacker recreates mint at same address with different decimals (e.g., 6)
5. Protocol now operates with incorrect decimal assumptions

#### Attack Scenario

1. Create Token-2022 mint with 18 decimals and MintCloseAuthority extension
2. Initialize protocol configuration using this mint
3. Protocol calculates `ld2sd_rate` = 10^(18-6) = 10^12
4. Close the mint (supply must be 0)
5. Reinitialize mint at same address with 6 decimals
6. Protocol still uses rate 10^12 but mint operates at 10^6
7. Massive accounting errors occur, enabling arbitrage/theft

### Vulnerable Pattern Examples

**Example 1: No MintCloseAuthority Check** [CRITICAL]
> 📖 Reference: `reports/token2022_findings/c-01-mint-decimal-manipulation-through-mintcloseauthority-leads-to-inflation-of-.md`
```rust
// ❌ VULNERABLE: Accepts any mint without checking close authority
#[derive(Accounts)]
pub struct InitPool<'info> {
    #[account(mint::token_program = token_program)]
    pub token_mint: InterfaceAccount<'info, Mint>,  // No extension check!
    
    pub token_program: Interface<'info, TokenInterface>,
}

impl InitPool<'_> {
    pub fn apply(ctx: &Context<InitPool>) -> Result<()> {
        // Uses mint.decimals for rate calculation
        let ld2sd_rate = 10u64.pow((ctx.accounts.token_mint.decimals - SHARED_DECIMALS) as u32);
        // Rate can become stale if mint is closed and recreated
        Ok(())
    }
}
```

**Example 2: Bridge/Cross-chain Rate Manipulation** [CRITICAL]
```rust
// ❌ VULNERABLE: Cross-chain protocol with decimal-based rate
pub fn init_oft_config(
    ctx: Context<InitOft>,
    shared_decimals: u8
) -> Result<()> {
    let local_decimals = ctx.accounts.mint.decimals;
    
    // This rate becomes exploitable if mint decimals change
    ctx.accounts.config.ld2sd_rate = 10u64.pow((local_decimals - shared_decimals) as u32);
    
    Ok(())
}
```

### Impact Analysis

#### Technical Impact
- Decimal rate calculations become incorrect
- Token amounts inflated or deflated by orders of magnitude
- Cross-chain bridges transfer incorrect amounts
- All protocol calculations based on decimals become invalid

#### Business Impact
- Massive fund theft via arbitrage
- Legitimate transfers treated as dust and lost
- Protocol insolvency
- Cross-chain value extraction

### Secure Implementation

**Fix 1: Check for MintCloseAuthority Extension**
```rust
use spl_token_2022::extension::{BaseStateWithExtensions, StateWithExtensions};
use spl_token_2022::extension::mint_close_authority::MintCloseAuthority;

// ✅ SECURE: Reject mints with close authority
pub fn validate_mint_no_close_authority(
    mint_account: &InterfaceAccount<Mint>
) -> Result<()> {
    let mint_info = mint_account.to_account_info();
    let mint_data = mint_info.data.borrow();
    
    if let Ok(mint) = StateWithExtensions::<spl_token_2022::state::Mint>::unpack(&mint_data) {
        // Check if MintCloseAuthority extension exists
        if mint.get_extension::<MintCloseAuthority>().is_ok() {
            return Err(ErrorCode::UnsupportedMintExtension.into());
        }
    }
    
    Ok(())
}
```

**Fix 2: Comprehensive Extension Validation Helper**
```rust
// ✅ SECURE: Full mint validation for Token-2022
pub fn is_supported_mint(mint_account: &InterfaceAccount<Mint>) -> bool {
    let mint_info = mint_account.to_account_info();
    let mint_data = mint_info.data.borrow();
    
    let Ok(mint) = StateWithExtensions::<spl_token_2022::state::Mint>::unpack(&mint_data) else {
        return false;
    };
    
    // Reject dangerous extensions
    if mint.get_extension::<MintCloseAuthority>().is_ok() {
        return false;  // Can manipulate decimals
    }
    
    if mint.base.freeze_authority.is_some() {
        return false;  // Can freeze accounts
    }
    
    // Add more extension checks as needed
    true
}
```

**Fix 3: Anchor Constraint with Validation**
```rust
// ✅ SECURE: Anchor pattern with validation
#[derive(Accounts)]
pub struct InitPool<'info> {
    #[account(
        mint::token_program = token_program,
        constraint = validate_supported_mint(&token_mint).is_ok() @ ErrorCode::UnsupportedMint
    )]
    pub token_mint: InterfaceAccount<'info, Mint>,
    
    pub token_program: Interface<'info, TokenInterface>,
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- InterfaceAccount<Mint> without extension validation
- Decimal-based rate calculations stored on-chain
- Cross-chain protocols using local decimals
- No validation of Token-2022 extensions before accepting mint
```

#### Audit Checklist
- [ ] Check for MintCloseAuthority extension before accepting mints
- [ ] Validate that decimals-based calculations cannot be exploited
- [ ] Consider storing mint address and re-fetching decimals on each operation
- [ ] Block mints with dangerous extensions in protocol initialization

---

## 2. Freeze Authority Vulnerabilities

### Overview

Token-2022 and SPL Token mints can have a freeze authority that can freeze any token account, preventing transfers. Protocols that accept tokens with freeze authority are vulnerable to DOS attacks where the authority freezes protocol-owned token accounts.

> **📚 Source Reports for Deep Dive:**
> - `reports/solana_findings/m-01-lack-of-freeze-authority-check-for-collateral-tokens-on-create-trading-pool.md`
> - `reports/solana_findings/m-02-risk-of-input-token-mint-with-freeze-authority-leading-to-permanent-dos.md`
> - `reports/solana_findings/h-01-denial-of-service-risk-due-to-frozen-token_escrow-in-onftadapter.md`

### Vulnerability Description

#### Root Cause

Protocols accept mints with freeze authority set, allowing the mint authority to:
1. Freeze protocol-owned token vaults/escrows
2. Block all deposits, withdrawals, and transfers
3. Permanently lock user funds in the protocol

#### Attack Scenario

1. Attacker creates mint with freeze authority
2. Attacker deposits tokens into protocol vault
3. Attacker freezes the protocol's token vault
4. All users' funds in the vault become permanently locked
5. Protocol cannot withdraw or transfer any tokens

### Vulnerable Pattern Examples

**Example 1: No Freeze Authority Check on Pool Creation** [HIGH]
> 📖 Reference: `reports/solana_findings/m-01-lack-of-freeze-authority-check-for-collateral-tokens-on-create-trading-pool.md`
```rust
// ❌ VULNERABLE: Accepts mints with freeze authority
#[derive(Accounts)]
pub struct CreatePool<'info> {
    #[account(mint::token_program = token_program)]
    pub input_token_mint: Box<InterfaceAccount<'info, Mint>>,  // No freeze check!
    
    #[account(
        init,
        payer = payer,
        token::authority = pool,
        token::mint = input_token_mint,
    )]
    pub pool_vault: Box<InterfaceAccount<'info, TokenAccount>>,
}
```

**Example 2: Bridge Token Escrow Vulnerable to Freeze** [HIGH]
> 📖 Reference: `reports/solana_findings/h-01-denial-of-service-risk-due-to-frozen-token_escrow-in-onftadapter.md`
```rust
// ❌ VULNERABLE: Escrow can be frozen, blocking all bridge operations
pub fn init_oft_adapter(ctx: Context<InitAdapter>) -> Result<()> {
    // Token escrow created without checking mint's freeze authority
    // If frozen, all cross-chain transfers halt
    Ok(())
}
```

### Impact Analysis

#### Technical Impact
- Protocol token accounts become frozen
- All token operations blocked (transfer, burn, close)
- Accounts remain frozen indefinitely until authority unfreezes

#### Business Impact
- Permanent loss of user funds
- Complete protocol denial of service
- No recovery possible without freeze authority cooperation
- Potential ransom attacks

### Secure Implementation

**Fix 1: Reject Mints with Freeze Authority**
```rust
// ✅ SECURE: Validate no freeze authority
#[derive(Accounts)]
pub struct CreatePool<'info> {
    #[account(
        mint::token_program = token_program,
        constraint = input_token_mint.freeze_authority.is_none() @ ErrorCode::FreezableMintNotSupported
    )]
    pub input_token_mint: Box<InterfaceAccount<'info, Mint>>,
}
```

**Fix 2: Native Freeze Authority Check**
```rust
// ✅ SECURE: Check freeze authority before accepting mint
pub fn validate_mint_no_freeze_authority(mint: &InterfaceAccount<Mint>) -> Result<()> {
    require!(
        mint.freeze_authority.is_none(),
        ErrorCode::FreezableMintNotSupported
    );
    Ok(())
}
```

**Fix 3: Comprehensive Mint Validation**
```rust
// ✅ SECURE: Full mint safety check
pub fn is_safe_collateral_mint(mint: &InterfaceAccount<Mint>) -> bool {
    // Check freeze authority
    if mint.freeze_authority.is_some() {
        return false;
    }
    
    // For Token-2022, also check extensions
    let mint_info = mint.to_account_info();
    if *mint_info.owner == spl_token_2022::id() {
        let mint_data = mint_info.data.borrow();
        if let Ok(state) = StateWithExtensions::<spl_token_2022::state::Mint>::unpack(&mint_data) {
            // Check for permanent delegate (can drain tokens)
            if state.get_extension::<PermanentDelegate>().is_ok() {
                return false;
            }
            // Check for close authority (decimal manipulation)
            if state.get_extension::<MintCloseAuthority>().is_ok() {
                return false;
            }
        }
    }
    
    true
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- InterfaceAccount<Mint> without freeze_authority check
- Protocol vaults for user-provided mints
- Collateral/escrow accounts without mint validation
- Cross-chain bridges accepting arbitrary mints
```

#### Audit Checklist
- [ ] All accepted mints checked for freeze_authority == None
- [ ] Consider allowlisting specific mints for high-value protocols
- [ ] Document risks if freeze authority mints are intentionally supported
- [ ] Implement escape hatches or governance overrides where possible

---

## 3. Transfer Fee Extension Vulnerabilities

### Overview

Token-2022's Transfer Fee extension deducts a fee on every transfer. Protocols that don't account for this receive less tokens than expected, causing accounting errors and potential fund loss.

> **📚 Source Reports for Deep Dive:**
> - `reports/token2022_findings/fee-on-transfer-tokens-are-not-explicitly-denied-in-swap.md`
> - `reports/token2022_findings/m-33-lack-of-support-for-fee-on-transfer-token.md`
> - `reports/token2022_findings/m-02-feetaker-is-incompatible-with-fee-on-transfer-tokens.md`

### Vulnerability Description

#### Root Cause

Protocols assume `transfer(amount)` results in recipient receiving exactly `amount`. With transfer fee tokens:
- `transfer(1000)` with 1% fee means recipient gets 990 tokens
- Protocol records 1000 tokens received, but actually has 990
- Accounting discrepancies grow over time

### Vulnerable Pattern Examples

**Example 1: Basic Transfer Without Fee Awareness** [MEDIUM]
```rust
// ❌ VULNERABLE: Doesn't account for transfer fees
pub fn deposit(ctx: Context<Deposit>, amount: u64) -> Result<()> {
    // Transfer tokens to vault
    token::transfer(
        CpiContext::new(
            ctx.accounts.token_program.to_account_info(),
            Transfer {
                from: ctx.accounts.user_token_account.to_account_info(),
                to: ctx.accounts.vault.to_account_info(),
                authority: ctx.accounts.user.to_account_info(),
            },
        ),
        amount,
    )?;
    
    // WRONG: Records full amount, but vault received less
    ctx.accounts.user_state.deposited += amount;
    
    Ok(())
}
```

**Example 2: Swap Without Fee Accounting** [MEDIUM]
> 📖 Reference: `reports/token2022_findings/fee-on-transfer-tokens-are-not-explicitly-denied-in-swap.md`
```rust
// ❌ VULNERABLE: Swap doesn't handle transfer fees
pub fn swap(ctx: Context<Swap>, amount_in: u64) -> Result<()> {
    // Transfer in
    transfer_to_pool(ctx, amount_in)?;
    
    // Calculate output based on full amount_in
    let amount_out = calculate_output(amount_in);  // Wrong! Pool received less
    
    // Transfer out
    transfer_from_pool(ctx, amount_out)?;
    
    Ok(())
}
```

### Impact Analysis

#### Technical Impact
- Protocol under-records actual token balances
- Swap calculations based on incorrect amounts
- Accumulated accounting errors over time
- Potential insolvency as users withdraw more than exists

#### Business Impact
- Last withdrawers unable to withdraw (insufficient funds)
- Arbitrage opportunities against miscalculated swaps
- Protocol insolvency from accumulated errors
- User fund loss

### Secure Implementation

**Fix 1: Measure Actual Transfer Amount**
```rust
// ✅ SECURE: Measure actual tokens received
pub fn deposit(ctx: Context<Deposit>, amount: u64) -> Result<()> {
    // Get balance before transfer
    let balance_before = ctx.accounts.vault.amount;
    
    // Transfer tokens
    token::transfer(CpiContext::new(/* ... */), amount)?;
    
    // Reload to get updated balance
    ctx.accounts.vault.reload()?;
    let balance_after = ctx.accounts.vault.amount;
    
    // Calculate actual amount received (accounts for fees)
    let actual_received = balance_after.checked_sub(balance_before)
        .ok_or(ErrorCode::ArithmeticError)?;
    
    // Record actual amount
    ctx.accounts.user_state.deposited += actual_received;
    
    Ok(())
}
```

**Fix 2: Calculate Fee and Net Amount**
```rust
use spl_token_2022::extension::transfer_fee::{TransferFeeConfig, TransferFee};

// ✅ SECURE: Pre-calculate transfer fee
pub fn calculate_transfer_fee(
    mint: &InterfaceAccount<Mint>,
    amount: u64
) -> Result<u64> {
    let mint_info = mint.to_account_info();
    let mint_data = mint_info.data.borrow();
    
    if let Ok(state) = StateWithExtensions::<spl_token_2022::state::Mint>::unpack(&mint_data) {
        if let Ok(fee_config) = state.get_extension::<TransferFeeConfig>() {
            let epoch = Clock::get()?.epoch;
            let fee = fee_config
                .get_epoch_fee(epoch)
                .calculate_fee(amount)
                .ok_or(ErrorCode::FeeCalculationError)?;
            return Ok(fee);
        }
    }
    
    Ok(0)  // No fee for non-fee tokens
}

pub fn deposit_with_fee_awareness(ctx: Context<Deposit>, amount: u64) -> Result<()> {
    let fee = calculate_transfer_fee(&ctx.accounts.mint, amount)?;
    let net_amount = amount.checked_sub(fee).ok_or(ErrorCode::ArithmeticError)?;
    
    token::transfer(/* ... */, amount)?;
    
    // Record net amount
    ctx.accounts.user_state.deposited += net_amount;
    
    Ok(())
}
```

**Fix 3: Reject Transfer Fee Tokens**
```rust
// ✅ SECURE: Explicitly reject transfer fee tokens
pub fn validate_no_transfer_fee(mint: &InterfaceAccount<Mint>) -> Result<()> {
    let mint_info = mint.to_account_info();
    let mint_data = mint_info.data.borrow();
    
    if let Ok(state) = StateWithExtensions::<spl_token_2022::state::Mint>::unpack(&mint_data) {
        if state.get_extension::<TransferFeeConfig>().is_ok() {
            return Err(ErrorCode::TransferFeeTokensNotSupported.into());
        }
    }
    
    Ok(())
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- token::transfer used without balance checks before/after
- Amount parameter used directly in accounting
- No TransferFeeConfig extension check
- Swaps calculating output from input without fee consideration
```

#### Audit Checklist
- [ ] Check for TransferFeeConfig extension on accepted mints
- [ ] Use balance-before/after pattern for fee tokens
- [ ] Or explicitly reject transfer fee tokens
- [ ] Validate swap calculations account for fees

---

## 4. Permanent Delegate Extension Vulnerabilities

### Overview

The Permanent Delegate extension designates an authority that can transfer or burn tokens from ANY token account for that mint, bypassing normal owner authorization. Accepting mints with permanent delegate is extremely dangerous.

### Vulnerability Description

#### Root Cause

The permanent delegate can:
1. Transfer tokens from any token account holding that mint
2. Burn tokens from any account
3. This power persists indefinitely and cannot be revoked

### Vulnerable Pattern Examples

**Example 1: Accepting Mints with Permanent Delegate** [CRITICAL]
```rust
// ❌ VULNERABLE: Permanent delegate can drain vault
#[derive(Accounts)]
pub struct CreateVault<'info> {
    pub token_mint: InterfaceAccount<'info, Mint>,  // No permanent delegate check!
    
    #[account(
        init,
        token::authority = vault_authority,
        token::mint = token_mint,
    )]
    pub vault: InterfaceAccount<'info, TokenAccount>,
}
```

### Impact Analysis

#### Technical Impact
- Permanent delegate can drain all protocol vaults
- Users' deposited funds can be stolen at any time
- No protection possible once tokens are in vault

#### Business Impact
- Complete fund theft possible
- No trust in protocol security
- Attacker can wait for large deposits then drain

### Secure Implementation

**Fix 1: Check for Permanent Delegate**
```rust
use spl_token_2022::extension::permanent_delegate::PermanentDelegate;

// ✅ SECURE: Reject mints with permanent delegate
pub fn validate_no_permanent_delegate(mint: &InterfaceAccount<Mint>) -> Result<()> {
    let mint_info = mint.to_account_info();
    let mint_data = mint_info.data.borrow();
    
    if let Ok(state) = StateWithExtensions::<spl_token_2022::state::Mint>::unpack(&mint_data) {
        if state.get_extension::<PermanentDelegate>().is_ok() {
            return Err(ErrorCode::PermanentDelegateNotSupported.into());
        }
    }
    
    Ok(())
}
```

---

## 5. Token Account Size Vulnerabilities

### Overview

Token-2022 accounts with extensions require more than the standard 165 bytes used for SPL Token accounts. Protocols that hardcode 165 bytes fail when interacting with Token-2022 mints.

> **📚 Source Reports for Deep Dive:**
> - `reports/solana_findings/fixed-token-account-size-causes-initialization-failures-for-token-accounts-whose.md`
> - `reports/solana_findings/hard-coded-165-byte-vault-account-is-too-small-for-raydium-token-2022-mints-with.md`

### Vulnerability Description

#### Root Cause

Hardcoding `space = 165` for token accounts fails for Token-2022 because:
1. Token-2022 base account is larger
2. Extensions add additional space requirements
3. Dynamic space calculation required

### Vulnerable Pattern Examples

**Example 1: Hardcoded Token Account Size** [MEDIUM]
```rust
// ❌ VULNERABLE: Hardcoded size fails for Token-2022
#[account(
    init,
    payer = payer,
    space = 165,  // Wrong for Token-2022!
    token::authority = pool,
    token::mint = mint,
)]
pub vault: Account<'info, TokenAccount>,
```

### Secure Implementation

**Fix 1: Use Anchor's Automatic Sizing**
```rust
// ✅ SECURE: Let Anchor/Token program handle sizing
#[account(
    init,
    payer = payer,
    token::authority = pool,
    token::mint = mint,
    token::token_program = token_program,  // Works with Token-2022
)]
pub vault: InterfaceAccount<'info, TokenAccount>,

pub token_program: Interface<'info, TokenInterface>,
```

**Fix 2: Calculate Size Dynamically**
```rust
// ✅ SECURE: Calculate required space
pub fn get_token_account_size(mint: &AccountInfo) -> Result<usize> {
    let mint_data = mint.data.borrow();
    
    if *mint.owner == spl_token_2022::id() {
        let state = StateWithExtensions::<spl_token_2022::state::Mint>::unpack(&mint_data)?;
        let extensions = state.get_extension_types()?;
        
        Ok(ExtensionType::try_calculate_account_len::<TokenAccountState>(&extensions)?)
    } else {
        Ok(TokenAccount::LEN)  // Standard SPL Token
    }
}
```

---

## 6. Default Account State Extension Vulnerabilities

### Overview

The Default Account State extension allows mints to specify that all new token accounts start in a frozen state. This can cause unexpected failures for protocols expecting accounts to be immediately usable.

### Vulnerable Pattern Examples

**Example 1: Assuming Accounts Start Unfrozen** [MEDIUM]
```rust
// ❌ VULNERABLE: Doesn't handle frozen default state
pub fn deposit(ctx: Context<Deposit>, amount: u64) -> Result<()> {
    // May fail if user's token account is frozen by default
    token::transfer(/* ... */, amount)?;
    Ok(())
}
```

### Secure Implementation

**Fix 1: Check Default Account State**
```rust
use spl_token_2022::extension::default_account_state::DefaultAccountState;
use spl_token_2022::state::AccountState;

// ✅ SECURE: Validate default state is not frozen
pub fn validate_unfrozen_default(mint: &InterfaceAccount<Mint>) -> Result<()> {
    let mint_info = mint.to_account_info();
    let mint_data = mint_info.data.borrow();
    
    if let Ok(state) = StateWithExtensions::<spl_token_2022::state::Mint>::unpack(&mint_data) {
        if let Ok(default_state) = state.get_extension::<DefaultAccountState>() {
            if default_state.state == AccountState::Frozen as u8 {
                return Err(ErrorCode::FrozenDefaultStateNotSupported.into());
            }
        }
    }
    
    Ok(())
}
```

---

## 7. Transfer Hook Extension Vulnerabilities

### Overview

Transfer Hook allows mints to specify a program that is called on every transfer. This can introduce:
- Unexpected transfer failures
- Additional CPI costs
- Re-entrancy-like patterns
- Validation bypass if hook is malicious

### Vulnerability Description

#### Root Cause

Transfer hooks can:
1. Reject transfers arbitrarily
2. Cause DOS by reverting
3. Introduce reentrancy through CPI
4. Add unpredictable gas costs

### Vulnerable Pattern Examples

**Example 1: Not Accounting for Transfer Hook Failures** [MEDIUM]
```rust
// ❌ VULNERABLE: Hook can cause unexpected failures
pub fn atomic_swap(ctx: Context<AtomicSwap>) -> Result<()> {
    // First transfer succeeds
    transfer_a_to_pool()?;
    
    // Second transfer may fail due to hook - leaves protocol in bad state
    transfer_b_to_user()?;  // If this fails, user lost tokens
    
    Ok(())
}
```

### Secure Implementation

**Fix 1: Check for Transfer Hook and Handle Carefully**
```rust
use spl_token_2022::extension::transfer_hook::TransferHook;

// ✅ SECURE: Validate transfer hook presence
pub fn validate_no_transfer_hook(mint: &InterfaceAccount<Mint>) -> Result<()> {
    let mint_info = mint.to_account_info();
    let mint_data = mint_info.data.borrow();
    
    if let Ok(state) = StateWithExtensions::<spl_token_2022::state::Mint>::unpack(&mint_data) {
        if state.get_extension::<TransferHook>().is_ok() {
            return Err(ErrorCode::TransferHookNotSupported.into());
        }
    }
    
    Ok(())
}
```

---

## 8. Interest Bearing Extension Vulnerabilities

### Overview

The Interest Bearing extension allows token balances to accrue interest over time. The actual balance is calculated based on the stored amount and the elapsed time since the last update. Protocols that read balances directly without accounting for accrued interest will have incorrect values.

### Vulnerability Description

#### Root Cause

With interest-bearing tokens:
1. `token_account.amount` returns the base amount, not the actual balance with interest
2. Protocols must use `amount_to_ui_amount` or calculate interest manually
3. Rate changes can occur, affecting calculations between reads

### Vulnerable Pattern Examples

**Example 1: Direct Balance Read Without Interest** [MEDIUM]
```rust
// ❌ VULNERABLE: Doesn't account for accrued interest
pub fn get_collateral_value(ctx: Context<GetValue>) -> Result<u64> {
    // For interest-bearing tokens, this is the BASE amount only!
    let raw_amount = ctx.accounts.collateral_vault.amount;
    
    // Calculation is wrong - missing accrued interest
    let value = raw_amount * ctx.accounts.price_feed.price;
    Ok(value)
}
```

### Secure Implementation

**Fix 1: Calculate Interest-Adjusted Balance**
```rust
use spl_token_2022::extension::interest_bearing_mint::InterestBearingConfig;

// ✅ SECURE: Account for interest when reading balance
pub fn get_interest_adjusted_balance(
    mint: &InterfaceAccount<Mint>,
    token_account: &InterfaceAccount<TokenAccount>,
) -> Result<u64> {
    let mint_info = mint.to_account_info();
    let mint_data = mint_info.data.borrow();
    
    let base_amount = token_account.amount;
    
    if let Ok(state) = StateWithExtensions::<spl_token_2022::state::Mint>::unpack(&mint_data) {
        if let Ok(config) = state.get_extension::<InterestBearingConfig>() {
            let current_time = Clock::get()?.unix_timestamp;
            
            // Calculate accrued interest
            let rate_bps = i128::from(config.current_rate);
            let time_elapsed = current_time
                .checked_sub(i64::from(config.last_update_timestamp))
                .ok_or(ErrorCode::ArithmeticError)?;
            
            // Simple interest calculation (actual formula may be more complex)
            let interest_multiplier = 10000i128 + (rate_bps * time_elapsed as i128 / 31536000);
            let adjusted = (base_amount as i128 * interest_multiplier / 10000) as u64;
            
            return Ok(adjusted);
        }
    }
    
    // No interest bearing extension - return base amount
    Ok(base_amount)
}
```

**Fix 2: Reject Interest Bearing Tokens**
```rust
// ✅ SECURE: Reject if protocol can't handle interest calculations
pub fn validate_no_interest_bearing(mint: &InterfaceAccount<Mint>) -> Result<()> {
    let mint_info = mint.to_account_info();
    let mint_data = mint_info.data.borrow();
    
    if let Ok(state) = StateWithExtensions::<spl_token_2022::state::Mint>::unpack(&mint_data) {
        if state.get_extension::<InterestBearingConfig>().is_ok() {
            return Err(ErrorCode::InterestBearingNotSupported.into());
        }
    }
    
    Ok(())
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Direct reads of token_account.amount without interest adjustment
- Balance comparisons that don't account for time-based changes
- Snapshot-based logic that becomes stale over time
```

---

## 9. Confidential Transfer Vulnerabilities

### Overview

Confidential Transfer is one of the most complex Token-2022 extensions, enabling encrypted token balances using zero-knowledge proofs. The on-chain balance becomes a ciphertext that can only be decrypted by the account owner.

### Vulnerability Description

#### Root Cause

With confidential transfers:
1. Public balance (`amount`) may be 0 or a pending balance waiting for transfer
2. Actual balance is encrypted in `confidential_transfer_account` extension data
3. Third parties (including protocols) cannot verify true balances
4. Requires special transfer instructions that include ZK proofs

### Impact Analysis

#### Technical Impact
- Collateral verification impossible without user cooperation
- Liquidation logic cannot verify undercollateralization
- Balance-based access control fails
- Accounting and reporting systems break

#### Business Impact
- Cannot implement trustless collateralized lending
- Unable to enforce minimum balance requirements
- Protocol risk management compromised
- Regulatory compliance challenges

### Secure Implementation

**Fix 1: Reject Confidential Transfer Tokens for DeFi**
```rust
use spl_token_2022::extension::confidential_transfer::ConfidentialTransferMint;

// ✅ SECURE: Reject for protocols requiring balance visibility
pub fn validate_no_confidential_transfer(mint: &InterfaceAccount<Mint>) -> Result<()> {
    let mint_info = mint.to_account_info();
    let mint_data = mint_info.data.borrow();
    
    if let Ok(state) = StateWithExtensions::<spl_token_2022::state::Mint>::unpack(&mint_data) {
        if state.get_extension::<ConfidentialTransferMint>().is_ok() {
            return Err(ErrorCode::ConfidentialTransferNotSupported.into());
        }
    }
    
    Ok(())
}
```

### Detection Patterns

#### Audit Checklist
- [ ] Protocol rejects mints with ConfidentialTransferMint extension
- [ ] Or protocol explicitly handles confidential balances with ZK proofs
- [ ] No reliance on public balance for security-critical decisions
- [ ] Clear documentation of confidential transfer stance

---

## 10. General Token-2022 Integration Vulnerabilities

### Comprehensive Extension Validation

```rust
use spl_token_2022::extension::*;

// ✅ SECURE: Comprehensive Token-2022 safety check
pub fn validate_safe_mint(mint: &InterfaceAccount<Mint>) -> Result<()> {
    let mint_info = mint.to_account_info();
    let mint_data = mint_info.data.borrow();
    
    // Check if Token-2022
    if *mint_info.owner != spl_token_2022::id() {
        return Ok(());  // Standard SPL Token, basic checks only
    }
    
    let state = StateWithExtensions::<spl_token_2022::state::Mint>::unpack(&mint_data)?;
    
    // Check freeze authority
    require!(
        state.base.freeze_authority.is_none(),
        ErrorCode::FreezableMintNotSupported
    );
    
    // Check dangerous extensions
    require!(
        state.get_extension::<MintCloseAuthority>().is_err(),
        ErrorCode::MintCloseAuthorityNotSupported
    );
    
    require!(
        state.get_extension::<PermanentDelegate>().is_err(),
        ErrorCode::PermanentDelegateNotSupported
    );
    
    // Optional: Check transfer fee
    if state.get_extension::<TransferFeeConfig>().is_ok() {
        // Either reject or ensure protocol handles fees
        msg!("Warning: Transfer fee token detected");
    }
    
    // Optional: Check transfer hook
    if state.get_extension::<TransferHook>().is_ok() {
        return Err(ErrorCode::TransferHookNotSupported.into());
    }
    
    // Optional: Check default account state
    if let Ok(default_state) = state.get_extension::<DefaultAccountState>() {
        require!(
            default_state.state != spl_token_2022::state::AccountState::Frozen as u8,
            ErrorCode::FrozenDefaultStateNotSupported
        );
    }
    
    Ok(())
}
```

### Token-2022 Extension Quick Reference

| Extension | Risk Level | Issue | Recommendation |
|-----------|------------|-------|----------------|
| MintCloseAuthority | CRITICAL | Decimal manipulation | Reject |
| PermanentDelegate | CRITICAL | Can drain any account | Reject |
| FreezeAuthority | HIGH | Can freeze accounts | Reject or allowlist |
| TransferFee | MEDIUM | Accounting errors | Handle or reject |
| TransferHook | MEDIUM | Unpredictable behavior | Reject or audit hook |
| DefaultAccountState | LOW | Frozen by default | Check state |
| InterestBearing | LOW | Balance calculation | Update on each read |
| NonTransferable | LOW | Transfer restrictions | May be intentional |
| ConfidentialTransfer | LOW | Hidden balances | May need special handling |

---

## Prevention Guidelines

### Development Best Practices

1. **Always validate Token-2022 extensions** before accepting any mint
2. **Create allowlists** for known-safe mints in high-value protocols
3. **Reject dangerous extensions** by default (MintCloseAuthority, PermanentDelegate)
4. **Handle transfer fees** by measuring balance changes or pre-calculating fees
5. **Use InterfaceAccount and Interface** for Token-2022 compatibility
6. **Calculate dynamic account sizes** for Token-2022 accounts
7. **Test with Token-2022 mints** including various extension combinations
8. **Document extension requirements** for supported tokens

---

## Keywords for Search

`token_2022`, `spl_token_2022`, `mint_close_authority`, `freeze_authority`, `transfer_fee`, `permanent_delegate`, `transfer_hook`, `default_account_state`, `token_extensions`, `decimal_manipulation`, `fee_on_transfer`, `token_account_size`, `extension_validation`, `interface_account`, `token_interface`, `confidential_transfer`, `interest_bearing`, `non_transferable`, `metadata_pointer`, `group_pointer`

---

## 11. Non-Transferable Token Extension Vulnerabilities

### Overview

The Non-Transferable extension creates soulbound tokens that cannot be transferred after minting. Protocols integrating these tokens must understand that standard transfer operations will fail, and some extensions may still allow burning.

### Vulnerability Description

#### Root Cause

Protocols that accept arbitrary Token-2022 mints may:
1. Allow deposits of non-transferable tokens that can never be withdrawn
2. Break liquidation mechanisms that require token transfers
3. Create permanently locked positions in vaults or pools

### Vulnerable Pattern Examples

**Example 1: Non-Transferable Tokens in Vault** [MEDIUM]
```rust
// ❌ VULNERABLE: Accepts non-transferable tokens
#[derive(Accounts)]
pub struct Deposit<'info> {
    pub token_mint: InterfaceAccount<'info, Mint>,  // No extension check!
    
    #[account(mut)]
    pub user_token_account: InterfaceAccount<'info, TokenAccount>,
    
    #[account(mut)]
    pub vault: InterfaceAccount<'info, TokenAccount>,
}

// If user deposits non-transferable tokens, they cannot be withdrawn
pub fn deposit(ctx: Context<Deposit>, amount: u64) -> Result<()> {
    token::transfer(/* ... */, amount)?;  // This works for deposit
    // But withdrawal will FAIL for non-transferable tokens!
    Ok(())
}
```

### Impact Analysis

#### Technical Impact
- Tokens deposited to vaults become permanently locked
- Liquidations fail as tokens cannot be transferred
- Protocol state becomes inconsistent

#### Business Impact
- User funds locked forever
- Protocol becomes unusable for specific token types
- Potential for griefing attacks

### Secure Implementation

**Fix 1: Check for Non-Transferable Extension**
```rust
use spl_token_2022::extension::non_transferable::NonTransferable;

// ✅ SECURE: Reject non-transferable tokens
pub fn validate_transferable_token(mint: &InterfaceAccount<Mint>) -> Result<()> {
    let mint_info = mint.to_account_info();
    let mint_data = mint_info.data.borrow();
    
    if let Ok(state) = StateWithExtensions::<spl_token_2022::state::Mint>::unpack(&mint_data) {
        if state.get_extension::<NonTransferable>().is_ok() {
            return Err(ErrorCode::NonTransferableTokenNotSupported.into());
        }
    }
    
    Ok(())
}
```

---

## 12. Confidential Transfer Extension Vulnerabilities

### Overview

The Confidential Transfer extension enables encrypted token balances using zero-knowledge proofs. This creates unique challenges for protocols that need to verify balances or enforce minimum amounts.

### Vulnerability Description

#### Root Cause

With confidential transfers:
1. On-chain balance is encrypted and cannot be read directly
2. Traditional balance checks (e.g., `token_account.amount`) return 0 or encrypted values
3. Protocols relying on balance visibility break or make incorrect decisions

### Vulnerable Pattern Examples

**Example 1: Balance Check with Confidential Tokens** [MEDIUM]
```rust
// ❌ VULNERABLE: Assumes balance is readable
pub fn check_collateral_ratio(ctx: Context<CheckRatio>) -> Result<()> {
    // For confidential tokens, this may return 0 or meaningless value!
    let collateral = ctx.accounts.collateral_vault.amount;
    let debt = ctx.accounts.debt_amount;
    
    require!(
        collateral >= debt * 150 / 100,
        ErrorCode::InsufficientCollateral
    );
    Ok(())
}
```

### Secure Implementation

**Fix 1: Reject Confidential Transfer Tokens**
```rust
use spl_token_2022::extension::confidential_transfer::ConfidentialTransferMint;

// ✅ SECURE: Reject confidential transfer tokens if balance visibility required
pub fn validate_no_confidential_transfer(mint: &InterfaceAccount<Mint>) -> Result<()> {
    let mint_info = mint.to_account_info();
    let mint_data = mint_info.data.borrow();
    
    if let Ok(state) = StateWithExtensions::<spl_token_2022::state::Mint>::unpack(&mint_data) {
        if state.get_extension::<ConfidentialTransferMint>().is_ok() {
            return Err(ErrorCode::ConfidentialTransferNotSupported.into());
        }
    }
    
    Ok(())
}
```

---

## 13. Metadata Pointer Extension Vulnerabilities

### Overview

The Metadata Pointer extension allows token metadata to be stored in a separate account or within the mint itself. Incorrect assumptions about metadata location can lead to failed lookups or manipulation.

### Vulnerability Description

#### Root Cause

Protocols may:
1. Assume metadata is stored in Metaplex metadata accounts
2. Fail to follow the metadata pointer to the correct account
3. Not validate that metadata actually exists at the pointer location

### Secure Implementation

**Fix 1: Follow Metadata Pointer**
```rust
use spl_token_2022::extension::metadata_pointer::MetadataPointer;

// ✅ SECURE: Follow metadata pointer correctly
pub fn get_token_metadata(mint: &InterfaceAccount<Mint>) -> Result<Option<Pubkey>> {
    let mint_info = mint.to_account_info();
    let mint_data = mint_info.data.borrow();
    
    if let Ok(state) = StateWithExtensions::<spl_token_2022::state::Mint>::unpack(&mint_data) {
        if let Ok(pointer) = state.get_extension::<MetadataPointer>() {
            // Metadata address might be in the mint itself or external account
            return Ok(Option::<Pubkey>::from(pointer.metadata_address));
        }
    }
    
    Ok(None)  // No metadata pointer
}
```

---

## 14. Group and Group Member Extension Vulnerabilities

### Overview

The Group Pointer and Group Member Pointer extensions enable token grouping functionality. These extensions can affect how tokens are treated in collections and may have implications for NFT protocols.

### Secure Implementation

**Fix 1: Validate Group Extensions**
```rust
use spl_token_2022::extension::{group_pointer::GroupPointer, group_member_pointer::GroupMemberPointer};

// ✅ SECURE: Check for group extensions
pub fn validate_group_extensions(mint: &InterfaceAccount<Mint>) -> Result<()> {
    let mint_info = mint.to_account_info();
    let mint_data = mint_info.data.borrow();
    
    if let Ok(state) = StateWithExtensions::<spl_token_2022::state::Mint>::unpack(&mint_data) {
        // Handle group pointer if present
        if let Ok(group_ptr) = state.get_extension::<GroupPointer>() {
            msg!("Token has group pointer: {:?}", group_ptr.group_address);
        }
        
        // Handle group member pointer if present
        if let Ok(member_ptr) = state.get_extension::<GroupMemberPointer>() {
            msg!("Token is group member: {:?}", member_ptr.member_address);
        }
    }
    
    Ok(())
}
```

---

## 15. CPI Guard Extension Vulnerabilities

### Overview

The CPI Guard extension protects token accounts from unauthorized Cross-Program Invocation (CPI) operations. When enabled, certain CPI operations are restricted to prevent malicious programs from draining tokens.

### Vulnerability Description

#### Root Cause

Protocols may:
1. Fail to account for CPI Guard being enabled on user accounts
2. Attempt restricted CPI operations that fail unexpectedly
3. Not provide clear error messages when CPI Guard blocks operations

### Vulnerable Pattern Examples

**Example 1: CPI Operation Blocked by Guard** [MEDIUM]
```rust
// ❌ VULNERABLE: May fail if CPI Guard is enabled on source account
pub fn transfer_via_cpi(ctx: Context<TransferCpi>, amount: u64) -> Result<()> {
    // This CPI call may fail if user has CPI Guard enabled
    token::transfer(
        CpiContext::new(
            ctx.accounts.token_program.to_account_info(),
            Transfer {
                from: ctx.accounts.user_token.to_account_info(),
                to: ctx.accounts.vault.to_account_info(),
                authority: ctx.accounts.user.to_account_info(),
            },
        ),
        amount,
    )?;
    Ok(())
}
```

### Secure Implementation

**Fix 1: Handle CPI Guard Gracefully**
```rust
use spl_token_2022::extension::cpi_guard::CpiGuard;

// ✅ SECURE: Check for CPI Guard and handle appropriately
pub fn check_cpi_guard_enabled(
    token_account: &InterfaceAccount<TokenAccount>
) -> Result<bool> {
    let account_info = token_account.to_account_info();
    let account_data = account_info.data.borrow();
    
    if let Ok(state) = StateWithExtensions::<spl_token_2022::state::Account>::unpack(&account_data) {
        if let Ok(guard) = state.get_extension::<CpiGuard>() {
            return Ok(guard.lock_cpi.into());
        }
    }
    
    Ok(false)
}

// In your instruction
pub fn transfer_with_guard_check(ctx: Context<Transfer>, amount: u64) -> Result<()> {
    let guard_enabled = check_cpi_guard_enabled(&ctx.accounts.user_token)?;
    
    if guard_enabled {
        // User must sign directly, not via CPI
        return Err(ErrorCode::CpiGuardEnabled.into());
    }
    
    // Proceed with CPI transfer
    token::transfer(/* ... */)?;
    Ok(())
}
```

---

## 16. Required Memo Extension Vulnerabilities

### Overview

The Required Memo extension enforces that all transfers to a token account must include a memo instruction in the same transaction. Protocols failing to include memos will have their transfers rejected.

### Vulnerability Description

#### Root Cause

When transferring to accounts with Required Memo extension:
1. Transfers without accompanying memo instruction fail
2. Automated systems may not know to include memos
3. Protocol operations that don't use memos break

### Secure Implementation

**Fix 1: Add Memo to Transfers**
```rust
use spl_memo::instruction::build_memo;

// ✅ SECURE: Include memo when required
pub fn transfer_with_memo(
    ctx: Context<TransferWithMemo>,
    amount: u64,
    memo: String,
) -> Result<()> {
    // Add memo instruction
    invoke(
        &build_memo(memo.as_bytes(), &[&ctx.accounts.authority.key()]),
        &[ctx.accounts.authority.to_account_info()],
    )?;
    
    // Then transfer
    token::transfer(/* ... */, amount)?;
    
    Ok(())
}
```

**Fix 2: Reject Required Memo Accounts**
```rust
use spl_token_2022::extension::memo_transfer::MemoTransfer;

// ✅ SECURE: Reject accounts requiring memo if not supported
pub fn validate_no_memo_required(
    token_account: &InterfaceAccount<TokenAccount>
) -> Result<()> {
    let account_info = token_account.to_account_info();
    let account_data = account_info.data.borrow();
    
    if let Ok(state) = StateWithExtensions::<spl_token_2022::state::Account>::unpack(&account_data) {
        if let Ok(memo) = state.get_extension::<MemoTransfer>() {
            if bool::from(memo.require_incoming_transfer_memos) {
                return Err(ErrorCode::MemoRequiredNotSupported.into());
            }
        }
    }
    
    Ok(())
}
```

---

## 17. Immutable Owner Extension Vulnerabilities

### Overview

The Immutable Owner extension prevents the owner of a token account from being changed. While generally a security feature, protocols must understand this when designing account recovery or migration mechanisms.

### Impact Analysis

#### Design Considerations
- Token accounts with immutable owner cannot be reassigned
- Account recovery mechanisms relying on owner change will fail
- This is generally desirable for security but affects flexibility

---

## 18. Comprehensive Token-2022 Extension Whitelist Pattern

### Overview

For high-security protocols, the safest approach is to explicitly whitelist only the extensions you support rather than blacklisting dangerous ones.

### Secure Implementation

**Complete Extension Whitelist Validator**
```rust
use spl_token_2022::extension::*;

/// Comprehensive Token-2022 extension validator with whitelist approach
pub fn validate_supported_extensions(mint: &InterfaceAccount<Mint>) -> Result<()> {
    let mint_info = mint.to_account_info();
    
    // SPL Token (not Token-2022) is always safe
    if *mint_info.owner == spl_token::id() {
        return validate_spl_token_mint(mint);
    }
    
    // Must be Token-2022
    require!(
        *mint_info.owner == spl_token_2022::id(),
        ErrorCode::UnsupportedTokenProgram
    );
    
    let mint_data = mint_info.data.borrow();
    let state = StateWithExtensions::<spl_token_2022::state::Mint>::unpack(&mint_data)?;
    
    // Get all extension types
    let extension_types = state.get_extension_types()?;
    
    for ext_type in extension_types {
        match ext_type {
            // SAFE extensions - explicitly allow
            ExtensionType::MetadataPointer => {},
            ExtensionType::TokenMetadata => {},
            ExtensionType::ImmutableOwner => {},
            
            // CONDITIONALLY SAFE - allow with checks
            ExtensionType::TransferFeeConfig => {
                msg!("Warning: Transfer fee token - ensure fee handling");
            },
            ExtensionType::InterestBearingConfig => {
                msg!("Warning: Interest bearing - recalculate amounts");
            },
            ExtensionType::DefaultAccountState => {
                // Check it's not frozen by default
                if let Ok(default_state) = state.get_extension::<DefaultAccountState>() {
                    require!(
                        default_state.state != spl_token_2022::state::AccountState::Frozen as u8,
                        ErrorCode::FrozenDefaultState
                    );
                }
            },
            
            // DANGEROUS extensions - reject
            ExtensionType::MintCloseAuthority => {
                return Err(ErrorCode::DangerousExtension.into());
            },
            ExtensionType::PermanentDelegate => {
                return Err(ErrorCode::DangerousExtension.into());
            },
            ExtensionType::TransferHook => {
                return Err(ErrorCode::DangerousExtension.into());
            },
            ExtensionType::ConfidentialTransferMint => {
                return Err(ErrorCode::DangerousExtension.into());
            },
            ExtensionType::NonTransferable => {
                return Err(ErrorCode::DangerousExtension.into());
            },
            
            // UNKNOWN extensions - reject by default
            _ => {
                msg!("Unknown extension type: {:?}", ext_type);
                return Err(ErrorCode::UnknownExtension.into());
            }
        }
    }
    
    // Check freeze authority
    require!(
        state.base.freeze_authority.is_none(),
        ErrorCode::FreezableMint
    );
    
    Ok(())
}

fn validate_spl_token_mint(mint: &InterfaceAccount<Mint>) -> Result<()> {
    // For SPL Token, just check freeze authority
    require!(
        mint.freeze_authority.is_none(),
        ErrorCode::FreezableMint
    );
    Ok(())
}
```

---

## 19. Token-2022 Account Extension Validation

### Overview

Token accounts (not just mints) can also have extensions in Token-2022. Programs must validate token account extensions separately from mint extensions.

### Secure Implementation

**Token Account Extension Validator**
```rust
// ✅ SECURE: Validate token account extensions
pub fn validate_token_account_extensions(
    token_account: &InterfaceAccount<TokenAccount>
) -> Result<()> {
    let account_info = token_account.to_account_info();
    
    // Skip if not Token-2022
    if *account_info.owner != spl_token_2022::id() {
        return Ok(());
    }
    
    let account_data = account_info.data.borrow();
    let state = StateWithExtensions::<spl_token_2022::state::Account>::unpack(&account_data)?;
    
    // Check CPI Guard
    if let Ok(guard) = state.get_extension::<CpiGuard>() {
        if bool::from(guard.lock_cpi) {
            msg!("Warning: Account has CPI Guard enabled");
        }
    }
    
    // Check Memo Transfer requirement
    if let Ok(memo) = state.get_extension::<MemoTransfer>() {
        if bool::from(memo.require_incoming_transfer_memos) {
            msg!("Warning: Account requires memos on incoming transfers");
        }
    }
    
    Ok(())
}
```

---

## Prevention Guidelines

### Development Best Practices

1. **Always validate Token-2022 extensions** before accepting any mint
2. **Create allowlists** for known-safe mints in high-value protocols
3. **Reject dangerous extensions** by default (MintCloseAuthority, PermanentDelegate, TransferHook)
4. **Handle transfer fees** by measuring balance changes or pre-calculating fees
5. **Use InterfaceAccount and Interface** for Token-2022 compatibility
6. **Calculate dynamic account sizes** for Token-2022 accounts
7. **Test with Token-2022 mints** including various extension combinations
8. **Document extension requirements** for supported tokens
9. **Validate token account extensions** separately from mint extensions
10. **Use whitelist approach** for critical protocols - only allow known-safe extensions

### Token-2022 Extension Risk Matrix (Extended)

| Extension | Risk Level | Issue | Recommendation |
|-----------|------------|-------|----------------|
| MintCloseAuthority | CRITICAL | Decimal manipulation | Reject |
| PermanentDelegate | CRITICAL | Can drain any account | Reject |
| FreezeAuthority | HIGH | Can freeze accounts | Reject or allowlist |
| TransferFee | MEDIUM | Accounting errors | Handle or reject |
| TransferHook | MEDIUM-HIGH | Unpredictable behavior, reentrancy | Reject or audit hook |
| DefaultAccountState | LOW-MEDIUM | Frozen by default | Check state |
| InterestBearing | LOW | Balance calculation | Update on each read |
| NonTransferable | MEDIUM | Transfer restrictions, locked funds | Reject for vaults |
| ConfidentialTransfer | MEDIUM | Hidden balances | Reject if visibility needed |
| CpiGuard | LOW | CPI restrictions | Handle gracefully |
| MemoTransfer | LOW | Memo required | Include memo or reject |
| ImmutableOwner | LOW | Cannot reassign owner | Generally safe |
| MetadataPointer | LOW | Metadata location | Follow pointer correctly |
| GroupPointer | LOW | Token grouping | Handle for NFT protocols |
| GroupMemberPointer | LOW | Group membership | Handle for NFT protocols |

---

## Related Vulnerabilities

- [Solana Program Security](./solana-program-security.md) - General Solana security patterns
- [Fee-on-Transfer Tokens](../general/fee-on-transfer-tokens/) - EVM equivalent issues

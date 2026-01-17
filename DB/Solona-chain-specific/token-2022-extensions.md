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
token_extension_vector: close_authority|freeze_authority|transfer_fee|permanent_delegate|confidential_transfer|transfer_hook

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

`token_2022`, `spl_token_2022`, `mint_close_authority`, `freeze_authority`, `transfer_fee`, `permanent_delegate`, `transfer_hook`, `default_account_state`, `token_extensions`, `decimal_manipulation`, `fee_on_transfer`, `token_account_size`, `extension_validation`, `interface_account`, `token_interface`

---

## Related Vulnerabilities

- [Solana Program Security](./solana-program-security.md) - General Solana security patterns
- [Fee-on-Transfer Tokens](../general/fee-on-transfer-tokens/) - EVM equivalent issues

---
# Core Classification
protocol: Composable Bridge + PR
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47050
audit_firm: OtterSec
contest_link: https://www.composablefoundation.com/
source_link: https://www.composablefoundation.com/
github_link: https://github.com/ComposableFi/bridge-contract

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Ajay Shankar Kunapareddy
  - Robert Chen
  - Akash Gurugunti
---

## Vulnerability Title

Token Amount Mismatch

### Overview

See description below for full details.

### Original Finding Content

In the deposit instruction, the `deposit_sol` operation deposits SOL into a stake pool and receives a certain amount of stake pool tokens in return. These tokens are received in an account with the `mint` `common_state.lst_delegation_mint`, not necessarily the same as the staker’s token account. After the SOL deposit, the function transfers an amount of tokens from the staker’s token account to the escrow token account. The amount transferred is based on the updated balance of the token account after the SOL deposit.

> **Source:** `instructions/deposit.rs` (Rust)
```rust
pub fn deposit<'a, 'info>(
    ctx: Context<'a, 'a, 'a, 'info, Deposit<'info>>,
    amount: u64,
    deposit_sol: bool,
) -> Result<()> {
    [...]
    if deposit_sol {
        if ctx.remaining_accounts.len() != LIQUID_STAKE_ACCOUNTS_LEN as usize {
            return Err(ErrorCode::InsufficientAccounts.into());
        }
        if ctx.remaining_accounts[5].key != &common_state.lst_delegation_mint {
            return Err(ErrorCode::InvalidMint.into());
        }
        [...]
    }
    let transfer_ix = Transfer {
        from: ctx.accounts.staker_token_account.to_account_info(),
        to: ctx.accounts.escrow_token_account.to_account_info(),
        authority: ctx.accounts.staker.to_account_info(),
    };
    let cpi_ctx = CpiContext::new(ctx.accounts.token_program.to_account_info(), transfer_ix);
    [...]
}
```

However, the function does not ensure that the token account receiving the tokens (`lst_token_acc`) is the same as the staker’s token account (`staker_token_account`). It also does not check that the token mint (`lst_delegation_mint`) for the received tokens is the same as the token mint (`token_mint`) utilized for the staker’s token account. Consequently, the number of tokens transferred may not align with what was actually deposited into the stake pool.

## Remediation

Add checks to ensure that `lst_token_acc` matches `staker_token_account` to confirm that tokens are deposited and received as expected. Also, verify that the token mint of the tokens received (`lst_delegation_mint`) is the same as the token mint of the staker’s token account (`token_mint`).

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Composable Bridge + PR |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen, Akash Gurugunti |

### Source Links

- **Source**: https://www.composablefoundation.com/
- **GitHub**: https://github.com/ComposableFi/bridge-contract
- **Contest**: https://www.composablefoundation.com/

### Keywords for Search

`vulnerability`


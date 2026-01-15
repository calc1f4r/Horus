---
# Core Classification
protocol: Symmetry
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48608
audit_firm: OtterSec
contest_link: https://www.symmetry.fi/
source_link: https://www.symmetry.fi/
github_link: https://github.com/symmetry-protocol/funds-program

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
finders_count: 4
finders:
  - Robert Chen
  - Ajay Kunapareddy
  - OtterSec
  - Rajvardhan Agarwal
---

## Vulnerability Title

Account Validation

### Overview

See description below for full details.

### Original Finding Content

## Audit Findings

## Inconsistent Account Checks

It was discovered that account checks were performed in an inconsistent manner in the program. Some account checks were performed inside the instruction logic, while others used anchor constraints. It is recommended to separate account validation from the program’s logic as much as possible. Specifically, validation for `TokenAccounts` and `fund_state` were performed within the instructions. Some of the examples can be found in the code snippets below.

### Example: `buy_fund` Function

```rust
pub fn buy_fund(ctx: Context<BuyFund>, amount: u64) -> Result<()> {
    [...]
    if fund_state.sell_state == 1 {
        return Err(error!(ErrorCode::SellState));
    }
    if token_info.pda_token_account[USDC_TOKEN_ID] != *ctx.accounts.pda_usdc_account.key {
        return Err(error!(ErrorCode::IncorrectPdaUsdcAccount));
    }
    if ctx.accounts.buyer_fund_token_account.mint != fund_state.fund_token {
        return Err(error!(ErrorCode::IncorrectTokenAccount));
    }
    if ctx.accounts.host_usdc_account.owner != fund_state.host_pubkey {
        return Err(error!(ErrorCode::IncorrectRefferalFeeAccount));
    }
    if ctx.accounts.manager_usdc_account.owner != fund_state.manager {
        return Err(error!(ErrorCode::IncorrectManagerAccount));
    }
}
```

### Example: `swap_fund_tokens` Function

```rust
pub fn swap_fund_tokens(
    [...]
) {
    if fund_state.sell_state == 1 {
        return Err(error!(ErrorCode::SellState));
    }
    let token_info = ctx.accounts.token_info.load()?;
    let pyth_accounts: &[AccountInfo] = ctx.remaining_accounts;
    if token_info.pda_token_account[from_token_id as usize] != *ctx.accounts.pda_from_token_account.to_account_info().key {
        return Err(error!(ErrorCode::IncorrectPdaUsdcAccount));
    }
    if token_info.pda_token_account[to_token_id as usize] != *ctx.accounts.pda_to_token_account.to_account_info().key {
        return Err(error!(ErrorCode::IncorrectPdaUsdcAccount));
    }
}
```

## Remediation

Validation for all accounts except for `remaining_accounts` should be performed using anchor attributes. For example, in the `SwapFundTokens` instruction, the program could use an anchor constraint to ensure that `fund_state.sell_state` is `0`.

© 2022 OtterSec LLC. All Rights Reserved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Symmetry |
| Report Date | N/A |
| Finders | Robert Chen, Ajay Kunapareddy, OtterSec, Rajvardhan Agarwal |

### Source Links

- **Source**: https://www.symmetry.fi/
- **GitHub**: https://github.com/symmetry-protocol/funds-program
- **Contest**: https://www.symmetry.fi/

### Keywords for Search

`vulnerability`


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
solodit_id: 47047
audit_firm: OtterSec
contest_link: https://www.composablefoundation.com/
source_link: https://www.composablefoundation.com/
github_link: https://github.com/ComposableFi/bridge-contract

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

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

Failure To Burn Receipt Tokens

### Overview


The bug report states that there is an issue with the code for withdrawing tokens from the restaking program. After the tokens are withdrawn, there is no step to destroy or invalidate the receipt tokens, which represent the user's stake in the program. This means that the receipt tokens can still be used even after they have been redeemed or unlocked from the program. The suggested solution is to ensure that the receipt tokens are burned before interacting with the MarginFi program. This issue has been resolved in the code update f49a0ad.

### Original Finding Content

## Withdraw Instruction Overview

In the withdraw instruction, tokens are withdrawn from the restaking program and deposited into the `restake_receipt_token_account`. These tokens are supposed to represent the user’s stake or deposit in the restaking program. After the tokens are withdrawn from the restaking program, the code does not include a step to burn or destroy these receipt tokens. Burning these tokens is relevant because they should be invalidated once they are redeemed or unlocked from the restaking program.

## Code Example

```rust
pub fn withdraw<'a, 'info>(
    ctx: Context<'a, 'a, 'a, 'info, Withdraw<'info>>,
    amount: u64,
) -> Result<()> {
    [...]
    let accounts = restaking_v2_interface::instructions::WithdrawAccounts {
        staker: &common_state.to_account_info(),
        common_state: &ctx.accounts.restake_common_state.to_account_info(),
        token_mint: &ctx.accounts.restake_token_mint.to_account_info(),
        staker_token_account: &ctx.accounts.restake_receipt_token_account.to_account_info(),
        escrow_token_account: &ctx.accounts.restake_escrow_token_account.to_account_info(),
        receipt_token_mint: &ctx.accounts.restake_receipt_token_mint.to_account_info(),
        staker_receipt_token_account: &ctx.accounts.restake_staker_receipt_token_account.to_account_info(),
        token_program: &ctx.accounts.token_program,
        [...]
    };
    [...]
}
```

## Remediation

Ensure that the receipt tokens in `restake_receipt_token_account` are burned after withdrawing tokens from the restaking program and before interacting with the MarginFi program.

## Patch

Resolved in `f49a0ad`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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


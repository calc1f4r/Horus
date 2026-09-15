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
solodit_id: 48604
audit_firm: OtterSec
contest_link: https://www.symmetry.fi/
source_link: https://www.symmetry.fi/
github_link: https://github.com/symmetry-protocol/funds-program

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

Fund Token Manipulation

### Overview


This bug report discusses a vulnerability in a program called "Symmetry" that allows an attacker to manipulate the performance of a fund. The issue occurs in the "buy_state_rebalance" instruction, where the program does not properly validate the instruction and accounts being passed to another program called "prism aggregator." This allows the attacker to transfer funds between different assets and manipulate the fund's performance. The report recommends that the program should validate the data and accounts being passed to the prism aggregator and only allow transfers between specific accounts. The issue has been resolved in a recent patch.

### Original Finding Content

## Symmetry Audit 05 | Vulnerabilities

In the `buy_state_rebalance` instruction, the program does not validate the instruction id/data being passed over to the prism aggregator CPI. The accounts are passed directly through `remaining_accounts` and are not validated either. As seen in the code snippets below, the program only checks the change in balance for the `pda_usdc_account` and `pda_token_account` `TokenAccounts`.

The attacker can, however, pass in `TokenAccounts` for different fund assets and transfer the funds in between them to manipulate the fund performance. The swap will succeed because the balance for `pda_usdc_account` and `pda_token_account` remains unchanged. Technically, the attacker could’ve also transferred the funds to themselves but prism aggregator ensures that both `from_account` and `to_account` `TokenAccounts` have the same owner. It is still recommended to perform all the validation in the symmetry program itself.

## Code Snippets

### funds/src/swap.rs RUST

```rust
pub fn buy_state_rebalance(
    [...]
    let (from_amount, to_amount) = swap(
        ctx.remaining_accounts,
        &ctx.accounts.pda_account,
        &ctx.accounts.pda_usdc_account,
        &ctx.accounts.pda_token_account,
        &instruction_id,
        &instruction_data[0..instruction_size as usize],
        amount_to_spend,
        0,
        bump
    )?;
```

### funds/src/swap.rs RUST

```rust
pub fn swap(
    [...]
    let from_amount_after = 
        token::accessor::amount(&from_token_account.to_account_info())?;
    let to_amount_after = 
        token::accessor::amount(&to_token_account.to_account_info())?;
    
    let from_amount = 
        from_amount_before.checked_sub(from_amount_after).unwrap();
    let to_amount = 
        to_amount_after.checked_sub(to_amount_before).unwrap();
    
    // minimum_amount_out is 0
    if amount_in < from_amount || minimum_amount_out > to_amount {
        return Err(ErrorCode::SlippageError.into());
    }
```

## Proof of Concept

- User invokes the `buy_fund` instruction to buy a position in the fund.
- Attacker invokes the `buy_state_rebalance` instruction but uses `TokenAccounts` for assets other than USDC and the supplied token id for the prism aggregator CPI.
- As the `TokenAccounts` are passed in through `remaining_accounts` and not validated, the swap succeeds and the attacker is able to manipulate fund performance.

## Remediation

The instruction data and the accounts being passed to the prism aggregator program should be properly validated by the symmetry program. It should be ensured that funds are only transferred between the `pda_usdc_account` and `pda_token_account` `TokenAccounts`.

## Patch

Resolved in `6bde2b9`.

© 2022 OtterSec LLC. All Rights Reserved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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


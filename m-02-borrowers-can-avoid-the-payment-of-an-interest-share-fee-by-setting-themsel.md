---
# Core Classification
protocol: Lavarage
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33180
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-lavarage
source_link: https://code4rena.com/reports/2024-04-lavarage
github_link: https://github.com/code-423n4/2024-04-lavarage-findings/issues/18

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
finders_count: 5
finders:
  - rvierdiiev
  - Koolex
  - Arabadzhiev
  - DadeKuma
---

## Vulnerability Title

[M-02] Borrowers can avoid the payment of an interest share fee by setting themselves as a `fee_receipient`

### Overview


The bug report discusses a potential issue with the `repay_sol` function in the `swapback.rs` and `repay_sol.rs` files. The issue allows borrowers to avoid paying a 20% interest share fee by passing in a user-specified public key as the `fee_receipient` account. This means that the designated recipient may not receive the fee as intended. The report recommends implementing restrictions on the `fee_receipient` public key, such as making it a property of the `Pool` struct. The issue has been confirmed by a member of the team and is classified as an "Invalid Validation" type of bug.

### Original Finding Content


`src/processor/swapback.rs#L185`

`src/processor/swapback.rs#L192`

`src/context/repay_sol.rs#L23`

### Impact

Borrowers can avoid the payment of the 20% interest share fee on their accumulated interest.

### Proof of Concept

The current implementation of the `repay_sol` function sends a 20% interest share fee to the specified `fee_receipient` account that is passed in to it. However, as it can be seen, that account is a user specified one:

```rust
    let transfer_instruction3 = system_instruction::transfer(
    &ctx.accounts.trader.key(),
    &ctx.accounts.fee_receipient.key(),
    interest_share,
    );
    anchor_lang::solana_program::program::invoke(
        &transfer_instruction3,
        &[
            ctx.accounts.trader.to_account_info(),
            ctx.accounts.fee_receipient.to_account_info(),
        ],
    )?;
```

```rust
    /// CHECK: We just want the value of this account
    #[account(mut)]
    pub fee_receipient: UncheckedAccount<'info>,
```

What this means, is that the user can take advantage of that and avoid the payment of an interest share fee by simply passing in a public key that is controlled by them for that value. It is unclear who exactly is supposed to be the on the receiving end for the fee payment, but what's important is that that they can easily be easily be prevented from receiving it.

### Recommended Mitigation Steps

Apply some restrictions on the `fee_receipient` public key value. For example, you can make it be a property of the `Pool` struct that is set on the creation of each new trading pool by its operator.

### Assessed type

Invalid Validation

**[piske-alex (Lavarage) confirmed](https://github.com/code-423n4/2024-04-lavarage-findings/issues/18#issuecomment-2087770512)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Lavarage |
| Report Date | N/A |
| Finders | rvierdiiev, Koolex, Arabadzhiev, DadeKuma |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-lavarage
- **GitHub**: https://github.com/code-423n4/2024-04-lavarage-findings/issues/18
- **Contest**: https://code4rena.com/reports/2024-04-lavarage

### Keywords for Search

`vulnerability`


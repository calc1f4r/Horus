---
# Core Classification
protocol: Cashmere
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48775
audit_firm: OtterSec
contest_link: https://www.cashmere.finance/
source_link: https://www.cashmere.finance/
github_link: github.com/cashmere-inc/multisig.

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
  - Robert Chen
  - OtterSec
  - Rajvardhan Agarwal
---

## Vulnerability Title

Wallet Creation Fee Bypass

### Overview


The create_multisig instruction in the multisig program does not properly check the treasury account, allowing users to bypass the fee when creating a wallet by using their own account. This bug can be exploited by invoking the create_multisig instruction with a self-owned account as the treasury account, resulting in the fee being transferred back to the user. The program can be fixed by including a constant for the treasury account and checking it during wallet creation. The patch for this bug has been moved to the frontend and is available in the latest update.

### Original Finding Content

## Create Multisig Instruction Vulnerability

The `create_multisig` instruction does not properly validate the treasury account. This could allow users to bypass the fee when creating a wallet by passing their own fee account into the instruction. The following code snippets show the affected code.

## Affected Code Snippets

### multisig/src/lib.rs

```rust
pub struct CreateMultisig<'info> {
    #[account(init, payer = payer, space = Multisig::space(max_owners))]
    multisig: Account<'info, Multisig>,
    #[account(mut)]
    /// CHECK:
    pub treasury: UncheckedAccount<'info>,
}
```

### multisig/src/lib.rs

```rust
anchor_lang::solana_program::program::invoke(
    &anchor_lang::solana_program::system_instruction::transfer(
        &ctx.accounts.payer.key(),
        &ctx.accounts.treasury.key(),
        100000000,
    )
);
```

## Proof of Concept

1. Invoke the `create_multisig` instruction with a self-owned account as the treasury account.
2. The wallet is created. However, the fee for wallet creation is transferred back to the user.

## Remediation

The program can include as a constant the Pubkey for the treasury account, which can be checked when creating the wallet via an Anchor constraint.

## Patch

The fee collection code was moved to the frontend. Updated in #235.

© 2022 OtterSec LLC. All Rights Reserved. 6 / 23

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Cashmere |
| Report Date | N/A |
| Finders | Robert Chen, OtterSec, Rajvardhan Agarwal |

### Source Links

- **Source**: https://www.cashmere.finance/
- **GitHub**: github.com/cashmere-inc/multisig.
- **Contest**: https://www.cashmere.finance/

### Keywords for Search

`vulnerability`


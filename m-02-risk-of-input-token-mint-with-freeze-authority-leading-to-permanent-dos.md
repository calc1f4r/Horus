---
# Core Classification
protocol: Adrastea
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43983
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Adrastea-Security-Review.md
github_link: none

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
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[M-02] Risk of Input Token Mint with Freeze Authority Leading to Permanent DoS

### Overview


This bug report describes a potential issue with the current implementation of a pool, which could result in a denial of service (DoS) attack and permanent loss of funds for users. The problem lies in the fact that the input token mint, which the pool relies on, can be controlled by a freeze authority. This could lead to the pool's input token vault being frozen, preventing users from accessing their funds. To prevent this, the report recommends validating the absence of a freeze authority for the input token mint. The team has acknowledged the issue and is working on a response.

### Original Finding Content

## Severity

Medium Risk

## Description

The current implementation allows the input token mint to have a freeze authority, which can result in a potential denial of service (DoS) attack on the pool. If the input token mint’s freeze authority exercises control, the pool’s input token vault can be frozen, leading to a **permanent loss of funds** for users. This is a critical issue, as frozen token accounts cannot transfer tokens, rendering the pool inoperable.

Here’s the relevant code:

```rust
#[account(
    mint::token_program = token_program,
)]
input_token_mint: Box<InterfaceAccount<'info, Mint>>,

#[account(
    mut,
    associated_token::authority = pool,
    associated_token::mint = input_token_mint,
    associated_token::token_program = token_program
)]
pool_input_token_vault: Box<InterfaceAccount<'info, TokenAccount>>,
```

The pool relies on the assumption that the input token mint is safe, but if the input token mint has a freeze authority, that authority can freeze the pool's input token vault. This could prevent further deposits, withdrawals, or transfers, effectively freezing user funds.

## Impact

- **Denial of Service (DoS)**: The pool’s input token vault can be frozen by the mint’s freeze authority, halting all operations that involve this vault.
- **Permanent Loss of Funds**: If the vault is frozen, users will not be able to withdraw their funds, leading to a potential permanent loss of funds if the freeze is never lifted.

## Recommendations

1. **Validate Absence of Freeze Authority**:
   Ensure that the input token mint does not have a freeze authority or that the pool controls the freeze authority, preventing any external actor from freezing the pool's input token vault.

   Example:

   ```rust
   #[account(
       mint::freeze_authority = COption::None, // Ensure no freeze authority exists
       mint::token_program = token_program,
   )]
   input_token_mint: Box<InterfaceAccount<'info, Mint>>,
   ```

## Team Response

See response for [M-01](#m-01-team-response).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Adrastea |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Adrastea-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


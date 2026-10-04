---
# Core Classification
protocol: Enclave_2025-10-25
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63518
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Enclave-security-review_2025-10-25.md
github_link: none

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

protocol_categories:
  - algo-stables
  - bridge
  - cross_chain
  - decentralized_stablecoin
  - dexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[C-01] Funds can be redirected

### Overview


This bug report describes a problem with a Rust program that can allow an attacker to steal funds from a pool. The program does not properly check the ownership of a user's token account, which means that an attacker can use a legitimate signature to siphon funds directly to themselves. The report recommends adding code to validate the token account and restrict it to the user's associated token account. 

### Original Finding Content


_Resolved_

## Severity

**Impact:** High

**Likelihood:** High

## Description

```rust
 #[account(mut)]
    pub user_token_account: Account<'info, TokenAccount>
```

In `programs/solver-fund-pool-anchor/src/instructions/borrow.rs:142-143`, the `user_token_account` is only required to be writable; the program never checks whether `owner == user.key()`. The signed message also omits the `user_token_account`, and the contract does not validate that `user_token_account.owner` equals `user`, nor that it is the user’s associated token account (ATA).

As a result, an attacker can obtain a legitimate signature (which only binds `user/mint/amount/time window/nonce/...`) but replace `user_token_account` with their own token account, siphoning pool funds directly to themselves.

## Recommendations

```rust
#[account(
    mut,
    constraint = user_token_account.mint == token_mint.key() @ ErrorCode::InvalidTokenAccountMint,
    constraint = user_token_account.owner == user.key() @ ErrorCode::InvalidTokenAccountOwner,
)]
pub user_token_account: Account<'info, TokenAccount>,
```

Or restrict to the user’s ATA:

```rust
use anchor_spl::associated_token::get_associated_token_address;
require_keys_eq!(
    user_token_account.key(),
    get_associated_token_address(&Pubkey::try_from(user.key())?, &token_mint.key()),
    ErrorCode::NotUserATA
);
```





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Enclave_2025-10-25 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Enclave-security-review_2025-10-25.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


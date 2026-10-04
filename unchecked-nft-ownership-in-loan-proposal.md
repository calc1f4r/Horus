---
# Core Classification
protocol: Frakt
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48677
audit_firm: OtterSec
contest_link: https://frakt.xyz/
source_link: https://frakt.xyz/
github_link: github.com/frakt-solana/frakt-lending-protocol-

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
  - Harrison Green
  - Ethan Wu
  - OtterSec
  - William Wang
---

## Vulnerability Title

Unchecked NFT ownership in loan proposal

### Overview


The report discusses a bug in a loan contract where the program fails to verify if a token account contains the necessary token before accepting it as collateral. This can be exploited by an attacker who creates an empty token account and proposes a loan, causing the program to either freeze or take ownership of the account. If the loan is approved, the attacker receives lamports and the protocol cannot liquidate anything, resulting in loss of funds. The suggested solution is to add a verification step to ensure the token account has a balance of one. A patch has been provided to fix this issue.

### Original Finding Content

## Loan Proposal Issue with NFT Collateral

When a user proposes a loan via the `proposeLoan` instruction, the contract accepts a token account containing the NFT to be used as collateral. However, it fails to validate that the token account actually contains the token.

## Instructions

### propose_loan.rs (RUST)

```rust
#[account(mut,
// owner = token::ID,
associated_token::mint = nft_mint,
associated_token::authority = user)]
pub nft_user_token_account: Box<Account<'info, TokenAccount>>,
```

Consider the scenario where an attacker creates an empty token account for an NFT’s mint. When they propose a loan with the empty token account, the program either freezes or takes ownership of it. If the admin approves the loan, the attacker receives lamports. The attacker may keep the borrowed lamports, yet the protocol cannot liquidate anything; this constitutes a loss of funds.

## Remediation

Verify that the `nft_user_token_account` has a balance of one.

## Patch

### Diff

```diff
--- a/nft_lending_v2/src/instructions/propose_loan.rs
+++ b/nft_lending_v2/src/instructions/propose_loan.rs
@@ -34,6 +34,7 @@ pub struct ProposeLoan<'info> {
#[account(mut,
// owner = token::ID,
+ constraint = nft_user_token_account.amount == TOKEN_MINT_SUPPLY,
associated_token::mint = nft_mint,
associated_token::authority = user)]
pub nft_user_token_account: Box<Account<'info, TokenAccount>>,
```

© 2022 OtterSec LLC. All Rights Reserved. 6 / 25

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Frakt |
| Report Date | N/A |
| Finders | Harrison Green, Ethan Wu, OtterSec, William Wang |

### Source Links

- **Source**: https://frakt.xyz/
- **GitHub**: github.com/frakt-solana/frakt-lending-protocol-
- **Contest**: https://frakt.xyz/

### Keywords for Search

`vulnerability`


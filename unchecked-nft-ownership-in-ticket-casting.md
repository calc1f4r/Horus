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
solodit_id: 48680
audit_firm: OtterSec
contest_link: https://frakt.xyz/
source_link: https://frakt.xyz/
github_link: github.com/frakt-solana/frakt-lending-protocol-

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
finders_count: 4
finders:
  - Harrison Green
  - Ethan Wu
  - OtterSec
  - William Wang
---

## Vulnerability Title

Unchecked NFT ownership in ticket casting

### Overview


The bug report discusses an issue with the getLotTicket instruction, which allows the owner of a specific type of digital asset (NFT) to obtain raffle tickets. However, the instruction does not properly check if the user is the actual owner of the NFT, allowing an attacker to obtain raffle tickets by specifying the mint of any approved NFT, even if they do not own it. The suggested solution is to verify that the user obtaining the ticket is the owner of the NFT token account. A patch has been proposed to fix this issue, which includes adding a constraint to check if the NFT token account contains the correct NFT and specifying the associated token mint and authority.

### Original Finding Content

## getLotTicket Instruction Overview

The `getLotTicket` instruction allows the owner of an NFT to obtain raffle tickets. However, it does not verify that the NFT is actually owned by the invoker. This allows an attacker to obtain raffle tickets by specifying the mint of any Frakt-approved NFT — regardless of whether or not they own it.

## Remediation

Verify that the user obtaining the ticket is the NFT token account’s owner.

## Patch

```diff
--- a/nft_lending_v2/src/instructions/get_lot_ticket.rs
+++ b/nft_lending_v2/src/instructions/get_lot_ticket.rs
@@ -44,6 +44,13 @@ pub struct GetLotTicket<'info> {
 pub system_program: Program<'info, System>,
+
+ #[account(mut,
+ // owner = token::ID,
+ constraint = nft_user_token_account.amount == TOKEN_MINT_SUPPLY
,→ @ ErrorCodes::TokenAccountDoesntContainNft,
+ associated_token::mint = attempts_nft_mint,
+ associated_token::authority = user)]
+ pub nft_user_token_account: Box<Account<'info, TokenAccount>>,
 }
 pub fn handler(ctx: Context<GetLotTicket>,) -> Result<()> {
```

© 2022 OtterSec LLC. All Rights Reserved. 9 / 25

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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


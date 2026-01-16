---
# Core Classification
protocol: Honey
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48580
audit_firm: OtterSec
contest_link: https://honey.finance/
source_link: https://honey.finance/
github_link: github.com/honey-labs/nftLendBorrow.

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
finders_count: 3
finders:
  - Shiva Genji
  - OtterSec
  - William Wang
---

## Vulnerability Title

Denial of Service Affecting NFT Deposit

### Overview


The bug report is about an issue with the InitializeNFTAccount instruction in a code called RUST. This instruction is used to create an account to hold a non-fungible token (NFT) as collateral. However, the report states that the current code does not allow for the reuse of this account, meaning that an NFT can only be used as collateral once. This can also be exploited by attackers to cause a denial of service attack. To fix this issue, the report suggests replacing the current code with a new one that allows for the reuse of the collateral account. This issue has been fixed in the 9f04e0c patch. 

### Original Finding Content

## InitializeNFTAccount Instruction

In the `InitializeNFTAccount` instruction, `collateral_account` is created to hold an NFT as collateral. Notice that it is an associated token account, whose address is a PDA derived from the mint and authority. In particular, anyone attempting to initialize an NFT account will be required to use the same address. On the other hand, the `init` constraint will throw an error if the account already exists.

```rust
/// The account that will store the deposit notes
#[account(init,
associated_token::mint = deposit_nft_mint,
associated_token::authority = market_authority,
payer = owner)]
pub collateral_account: Box<Account<'info, TokenAccount>>,
```

This effectively means that an NFT can only be used as collateral once. An attacker can also cause a denial of service attack by intentionally invoking `InitializeNFTAccount` for arbitrary NFTs in the market.

## Remediation

Replace the `init` constraint with `init_if_needed`, so that `collateral_account` may be reused.

## Patch

Fixed in commit `9f04e0c`.

© 2022 OtterSec LLC. All Rights Reserved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Honey |
| Report Date | N/A |
| Finders | Shiva Genji, OtterSec, William Wang |

### Source Links

- **Source**: https://honey.finance/
- **GitHub**: github.com/honey-labs/nftLendBorrow.
- **Contest**: https://honey.finance/

### Keywords for Search

`vulnerability`


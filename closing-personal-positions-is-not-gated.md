---
# Core Classification
protocol: Raydium AMM V3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48450
audit_firm: OtterSec
contest_link: https://raydium.io/
source_link: https://raydium.io/
github_link: github.com/raydium-io/raydium-amm-v3.

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
  - Michal Bochnak
  - Maher Azzouzi
  - Robert Chen
  - OtterSec
  - William Wang
---

## Vulnerability Title

Closing Personal Positions Is Not Gated

### Overview


This bug report states that there is a problem with the ClosePosition instruction in a program that creates a personal position and mints an NFT to the user's wallet. While other instructions properly check for NFT ownership, the ClosePosition instruction does not, allowing attackers to create their own NFT account and steal funds. To fix this issue, the ClosePosition instruction should verify that the NFT account is non-empty. This has been addressed in a code patch.

### Original Finding Content

## Personal Position and NFT Ownership

When a personal position is created, the program mints an NFT to the user’s wallet. Subsequent instructions that require authorization of the position, such as increasing and decreasing liquidity, use the `is_authorized_for_token` function to check that the signer holds the NFT.

The `ClosePosition` instruction should also be privileged, but it does not check NFT ownership. An attacker can create their own empty NFT account, thus spoofing NFT ownership. This allows them to harvest the lamports used for rent.

## Remediation

In order for the issue to be remediated, the `ClosePosition` instruction should verify that the position NFT account, which should hold the NFT, is non-empty. This can be done with `is_authorized_for_token` or, as shown below, with an Anchor constraint.

```rust
src/instructions/close_position.rs
#[account(
mut,
associated_token::mint = position_nft_mint,
associated_token::authority = nft_owner,
constraint = position_nft_account.amount == 1
)]
pub position_nft_account: Box<Account<'info, TokenAccount>>,
```

## Patch

Fixed in #26.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Raydium AMM V3 |
| Report Date | N/A |
| Finders | Michal Bochnak, Maher Azzouzi, Robert Chen, OtterSec, William Wang |

### Source Links

- **Source**: https://raydium.io/
- **GitHub**: github.com/raydium-io/raydium-amm-v3.
- **Contest**: https://raydium.io/

### Keywords for Search

`vulnerability`


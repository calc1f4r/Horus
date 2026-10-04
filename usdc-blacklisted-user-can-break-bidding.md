---
# Core Classification
protocol: Kim Exchange
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46415
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/f4fbb598-ae17-4ef2-8290-864a0ab3d83e
source_link: https://cdn.cantina.xyz/reports/cantina_kim_exchange_november2024.pdf
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
finders_count: 2
finders:
  - cccz
  - Chinmay Farkya
---

## Vulnerability Title

USDC Blacklisted user can break bidding 

### Overview


This bug report discusses an issue with a specific line of code in the KimNFTMarketplace contract. The problem occurs when there is a higher bid, the listing is canceled, or the listing is bought directly. In these cases, the bid should be returned to the bidder. However, for some tokens, this refund is not always successful. For example, if a bidder is added to the blacklist after bidding, the transaction to send the token back will fail. This can be exploited by an attacker who can bid a small amount and prevent the listing from being canceled. This can result in the seller's NFT being stuck in the contract or only being able to accept the attacker's bid. The report recommends a solution to save the bidder, refunded token, and amount in case of a failed transfer and provide a way for the bidder to claim the tokens later. The issue has been fixed in a recent update, but there is still a low risk that it could occur.

### Original Finding Content

## KimNFTMarketplace.sol Analysis

## Context
- Location: `KimNFTMarketplace.sol#L236-L239`

## Description
When there is a higher bid, or the listing is canceled, or the listing is bought directly, if there is an existing bid, the bid will be returned to the bidder. For some tokens, refunds are not always successful. 

For example, for USDC, if a bidder is added to the USDC blacklist after bidding, sending USDC to the bidder will revert the transaction. Especially for `BUY_IT_NOW_WITH_BIDS` type listings, since there is no need to set a reserve price, an attacker can bid 0.01 USDC. After this, the listing cannot be canceled and the bid cannot be rejected. This will result in the seller's NFT being frozen in the contract or only able to accept the attacker's bid.

**Note:** This kind of DoS (due to the push funds approach) also affects `revealBlindBid()` and all other flows leading to `_deleteBidAndReturnFunds()`.

## Recommendation
If USDC (or other token) transfer fails, save the bidder, refunded token, and amount, continue with the subsequent logic, and provide a public function to allow the bidder to claim the transferred failed tokens later.

## Additional Information
- **KIM Exchange:** Fixed in PR 8.
- **Cantina Managed:** This fix sends the refund to the DAO when the bidder rejects it, which addresses the issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Kim Exchange |
| Report Date | N/A |
| Finders | cccz, Chinmay Farkya |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_kim_exchange_november2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/f4fbb598-ae17-4ef2-8290-864a0ab3d83e

### Keywords for Search

`vulnerability`


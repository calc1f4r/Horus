---
# Core Classification
protocol: NiftyApes - Seller Financing
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60494
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/nifty-apes-seller-financing/edbc671f-08c9-44ab-b24c-c3807c9ef43d/index.html
source_link: https://certificate.quantstamp.com/full/nifty-apes-seller-financing/edbc671f-08c9-44ab-b24c-c3807c9ef43d/index.html
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

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Michael Boyle
  - Ibrahim Abouzied
  - Hytham Farah
  - Jonathan Mevs
---

## Vulnerability Title

Underlying NFTs are Assigned Incorrect `nftId` for Collections

### Overview


The client has marked a bug in the code as "Fixed". The bug is in the `SellerFinancing.sol` file and specifically in the `_createLoan()` function. When financing collection offers, the `nftId` is incorrectly assigned for both the buyer and seller's underlying NFT. This is because the `offer.nftId` value, which is used to indicate the entire collection, is assigned instead of the individual NFT that is being purchased. This could cause issues with delegate.cash functionality if the buyer transfers their ticket. The recommendation is to make sure that the correct `nftId` is assigned to the underlying NFT.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `cf0c09a0c59961622a93ea527023538e91df8358`. The client provided the following explanation: Specify nftId for underlying nft in `_createLoan()`.

**File(s) affected:**`SellerFinancing.sol`

**Description:**`_createLoan()` incorrectly assigns the `nftId` of both the `buyerUnderlyingNFT` and `sellerUnderlyingNFT` when financing collection offers. Collection offers have the `offer.nftId` value assigned as `~uint256(0)`, which is used to denote that the offer exists for the entire collection instead of an individual NFT. When buying from a collection offer, the buyer specifies the individual NFT they are purchasing in `nftId` field in `buyWithFinancing()`. However, the individual `nftId` is not assigned to the buyer and seller's underlying NFT, rather the `offer.nftId` is, which would be the maximum value for a `uint256`.

This incorrect assignment would break the delegate.cash functionality if a buyer transfers their ticket, as delegate.cash would be attempting to delegate an NFT that does not exist.

**Recommendation:** Ensure that the underlying NFT is assigned the `nftId` of the NFT that is being purchased.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | NiftyApes - Seller Financing |
| Report Date | N/A |
| Finders | Michael Boyle, Ibrahim Abouzied, Hytham Farah, Jonathan Mevs |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/nifty-apes-seller-financing/edbc671f-08c9-44ab-b24c-c3807c9ef43d/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/nifty-apes-seller-financing/edbc671f-08c9-44ab-b24c-c3807c9ef43d/index.html

### Keywords for Search

`vulnerability`


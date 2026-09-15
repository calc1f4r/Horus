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
solodit_id: 46408
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/f4fbb598-ae17-4ef2-8290-864a0ab3d83e
source_link: https://cdn.cantina.xyz/reports/cantina_kim_exchange_november2024.pdf
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
finders_count: 2
finders:
  - cccz
  - Chinmay Farkya
---

## Vulnerability Title

Escrow check for ERC1155 tokens can DOS all auction interactions 

### Overview


This bug report is about a problem with a code that manages auctions for NFTs (non-fungible tokens). The code has a function called _isListingValid() which checks if the NFT is still being held by the marketplace. This check can sometimes return false and cause the entire auction process to fail, making it impossible to close the auction or cancel bids. This can happen when two sellers list the same NFT for sale, causing the balance of the marketplace to be greater than the value of any one listing. This bug affects all types of auctions. The recommendation is to use a different method to validate listings, which has been fixed in a recent update. The severity of this bug is considered medium.

### Original Finding Content

## Context
- **File Locations**: 
  - KimNFTMarketplace.sol#L76-L79
  - KimNFTMarketplace.sol#L395-L408

## Description
All interactions with a listing/auction involve checking that the NFT is still escrowed with the marketplace contract in order to ensure that the listing is still valid. This logic is present in `_isListingValid()`. For ERC1155 NFTs, the following check is employed:

```solidity
isMarketplaceStillHoldingNFT = _get1155NftBalanceOfUser(listing.nft, listing.tokenId, address(this)) == listing.amount;
```

This check can return false and deny service (DOS) to the whole auction process, which includes functions such as `settleAuction()`, `cancelBidForNFT()`, `cancelListing()`, `bidForNFT()`, `buyItNow()`, `acceptBidForNFT()`, and `rejectBidForNFT()`. Essentially, these are all the ways to settle or cancel the auction or retrieve funds from a bid.

### Example Scenario
Imagine this situation:
- **Seller A** lists an ERC1155 `tokenID` for sale: **amount X**.
- **Seller B** lists the same ERC1155 `tokenID` for sale: **amount Y**.

Now, all auction interactions will be permanently denied service (DOS) because none of these listings can be closed. This occurs because the `balanceOf(address(this))` will actually be greater than any one listing's value (it will be **X + Y**).

Both the `tokenIDs` and any existing bids from the first listing (prior to the creation of the second listing) will be stuck indefinitely. This issue can arise for all types of auctions.

## Recommendation
This method of validating a listing presents numerous issues. It should be reconfigured to use a state variable in the listing struct that indicates whether the listing has been finalized. Implementing this change will resolve the problem for ERC1155 tokens.

## KIM Exchange
- **Resolution**: Fixed in PR 8.

## Cantina Managed
The protocol reimplemented the `_isListingValid()` function to utilize `isNoLongerEscrowed` to track listing closure, and thus determine whether the listing is valid. These changes have resolved the issue with the ERC1155 escrow check, as listing validity no longer depends on the `balanceOf` for the `tokenID`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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


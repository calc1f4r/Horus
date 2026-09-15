---
# Core Classification
protocol: RipIt_2025-04-25
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62557
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/RipIt-security-review_2025-04-25.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-13] Buy request executed by providing `request.owner`

### Overview


This bug report is about a problem in a code that is used for buying items. When someone tries to buy an item, the code checks if the person who created the listing has signed it and if the receiver has also signed it. However, there is a way for someone to trick the code by allowing them to buy the item even if they are not the receiver. This could result in the wrong person receiving the item and the fee being paid to the wrong person. To fix this, the code needs to be changed so that the person who created the listing cannot also be the receiver.

### Original Finding Content


_Resolved_

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

When `buy` is executed, it first validates `isValidListing`, ensuring that `request.owner` has indeed signed the listing, and that listing.receiver has also signed the listing if the caller is not the `listing.receiver`.

```solidity
function isValidListing(ListingParams calldata listing) public view returns (bool) {
        if (listing.request.price == 0) revert InvalidPrice();
        if (block.timestamp > listing.request.deadline) revert ListingExpired();
        if (listing.request.chainId != block.chainid) revert InvalidChainId();
        bytes32 listingHash = generateListingSignatureHash(listing.request);
        if (usedListings[listingHash]) revert ListingAlreadyUsed();
        if (!IWhitelistRegistry(whitelistRegistry).isWhitelisted(listing.request.tokenContractAddress)) {
            revert NFTNotWhitelisted();
        }
        if (IERC721(listing.request.tokenContractAddress).ownerOf(listing.request.tokenId) != listing.request.owner) {
            revert NotOwner();
        }

>>>     if (!SignatureChecker.isValidSignatureNow(listing.request.owner, listingHash, listing.sig)) {
            revert InvalidSignature();
        }
     
>>>     if (msg.sender != listing.receiver && !SignatureChecker.isValidSignatureNow(listing.receiver, listingHash, listing.receiverSig)) {
            revert InvalidSignature();
        }

        return true;
    }
```

However, if the request owner has `acceptedCurrency` allowance to the contract, this could allow an attacker to trigger `buy`, designate the owner as the receiver, and provide a valid signature, causing the `buy` to be executed. This would result in the listing owner's request being fulfilled and the fee being paid to the contract.

## Recommendations

Prevent `buy` operation from being executed if the provided receiver is the owner.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | RipIt_2025-04-25 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/RipIt-security-review_2025-04-25.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


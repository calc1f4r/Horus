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
solodit_id: 62546
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

[M-02] Lack of nonce mechanism in signature hash generation

### Overview


The bug report is about a function called `generateListingSignatureHash` in the Marketplace contract. This function creates a hash for a listing request, but it does not include a nonce mechanism. This means that once the owner signs the listing, the signature remains valid even if the owner changes the price. This creates a vulnerability where a malicious attacker could use the original signed price to execute a purchase, potentially causing financial losses for the seller. To fix this issue, it is recommended to implement a nonce mechanism that is unique for each listing and can be disabled by the owner if needed.

### Original Finding Content


_Resolved_

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The `generateListingSignatureHash` function in the Marketplace contract creates a hash for a listing request that does not include a nonce mechanism.

```solidity
    function generateListingSignatureHash(ListingRequest calldata listing) public view returns (bytes32) {
        return _hashTypedDataV4(
            keccak256(
                abi.encode(
                    LISTING_TYPEHASH,
                    listing.tokenContractAddress,
                    listing.tokenId,
                    listing.price,
                    listing.acceptedCurrency,
                    listing.deadline,
                    listing.owner,
                    listing.chainId
                )
            )
        );
    }
```

This omission means that once the owner signs the listing, the signature remains valid (until `deadline`) even if the owner subsequently modifies the price. **And once a signature is signed, there is no way to revoke it.**

This creates a vulnerability where a malicious attacker could withhold the owner's signature until the `deadline`. If the price of the asset increases (a common occurrence with volatile assets), the attacker could use the original signed price to execute a purchase, undermining the integrity of the listing process and potentially leading to financial losses for the seller.

```solidity
        bytes32 listingHash = generateListingSignatureHash(listing.request);
        if (usedListings[listingHash]) revert ListingAlreadyUsed();
        if (!IWhitelistRegistry(whitelistRegistry).isWhitelisted(listing.request.tokenContractAddress)) {
            revert NFTNotWhitelisted();
        }
        if (IERC721(listing.request.tokenContractAddress).ownerOf(listing.request.tokenId) != listing.request.owner) {
            revert NotOwner();
        }

        if (!SignatureChecker.isValidSignatureNow(listing.request.owner, listingHash, listing.sig)) {
            revert InvalidSignature();
        }
```

This is the same for other signature generation in `isValidTrade` and `isValidBid`.

## Recommendations

To enhance the security of the listing process, implement a nonce mechanism that is included in the signature hash generation. This nonce should be unique for each listing and should be incremented with each new listing request from the owner.  **More specifically, the owner should be able to disable a signature once it becomes invalid.**





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


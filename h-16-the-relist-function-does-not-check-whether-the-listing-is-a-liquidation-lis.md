---
# Core Classification
protocol: Flayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41754
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/468
source_link: none
github_link: https://github.com/sherlock-audit/2024-08-flayer-judging/issues/547

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
finders_count: 19
finders:
  - Tendency
  - 0xNirix
  - 0xAlix2
  - zzykxx
  - Sentryx
---

## Vulnerability Title

H-16: The `relist` function does not check whether the listing is a liquidation listing causing users to pay taxes and refunds being paid to the listing owner who did not pay taxes

### Overview


This bug report is about a function called `relist` that does not check if a listing is a liquidation listing. This can cause users to pay taxes and refunds to be paid to the original listing owner who did not pay taxes. This can result in a loss of funds within the system. The code snippet and tool used for this report were a manual review. The recommendation is to add a check in the `relist` function to prevent taxes from being paid for liquidated listings.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-08-flayer-judging/issues/547 

## Found by 
0x37, 0xAlix2, 0xNirix, BADROBINX, BugPull, Ollam, Sentryx, Tendency, almantare, almurhasan, araj, blockchain555, h2134, kuprum, merlinboii, t.aksoy, utsav, valuevalk, zzykxx
## Summary
Since liquidated listings are created without the original owner paying taxes, the lack of a check for the liquidation status means the system might incorrectly process a tax refund for a listing that was liquidated, allowing the original owner to receive funds they should not be entitled to
## Vulnerability Detail
Liquidated listings are created without the original owner paying taxes. If the system lacks a check for liquidation status, it might process a tax refund incorrectly, The absence of a liquidation status check can lead to the original owner receiving tax refunds for liquidated listings, which they are not entitled to. This creates an opportunity for the owner to receive funds improperly

The problem arises because the `relist` function does not check if the Listing being relisted was from a liquidation or not, therefore causing the "relister" to pay taxes and the contract depositing refunds to the "liquidated user" who did not pay taxes.
## Impact
Without checking liquidation status, the system may wrongly process tax refunds for liquidated listings, allowing the original owner to receive undeserved funds. This error could result in a loss of funds within the protocol.

## Code Snippet
- https://github.com/sherlock-audit/2024-08-flayer/blob/main/flayer/src/contracts/Listings.sol#L644
<details>
<summary>Whole Function</summary>

```solidity
    function relist(CreateListing calldata _listing, bool _payTaxWithEscrow) public nonReentrant lockerNotPaused {
  // Load our tokenId
  address _collection = _listing.collection;
  uint _tokenId = _listing.tokenIds[0];

  // Read the existing listing in a single read
  Listing memory oldListing = _listings[_collection][_tokenId];

  // Ensure the caller is not the owner of the listing
  if (oldListing.owner == msg.sender) revert CallerIsAlreadyOwner();

  // Load our new Listing into memory
  Listing memory listing = _listing.listing;

  // Ensure that the existing listing is available
  (bool isAvailable, uint listingPrice) = getListingPrice(_collection, _tokenId);
  if (!isAvailable) revert ListingNotAvailable();

  // We can process a tax refund for the existing listing
@>(uint _fees,) = _resolveListingTax(oldListing, _collection, true);
  if (_fees != 0) {
    emit ListingFeeCaptured(_collection, _tokenId, _fees);
  }

  // Find the underlying {CollectionToken} attached to our collection
  ICollectionToken collectionToken = locker.collectionToken(_collection);

  // If the floor multiple of the original listings is different, then this needs
  // to be paid to the original owner of the listing.
  uint listingFloorPrice = 1 ether * 10 ** collectionToken.denomination();
  if (listingPrice > listingFloorPrice) {
    unchecked {
      collectionToken.transferFrom(msg.sender, oldListing.owner, listingPrice - listingFloorPrice);
    }
  }

  // Validate our new listing
  _validateCreateListing(_listing);

  // Store our listing into our Listing mappings
  _listings[_collection][_tokenId] = listing;

  // Pay our required taxes
  payTaxWithEscrow(address(collectionToken), getListingTaxRequired(listing, _collection), _payTaxWithEscrow);

  // Emit events
  emit ListingRelisted(_collection, _tokenId, listing);
}
```

</details>

## Tool used

Manual Review

## Recommendation
Add a check inside the `relist` Function to prevent taxes being paid for listings that were liquidated
```diff
  // We can process a tax refund for the existing listing
+  if (!_isLiquidation[_collection][_tokenId]) {
  (uint _fees,) = _resolveListingTax(oldListing, _collection, true);
  if (_fees != 0) {
    emit ListingFeeCaptured(_collection, _tokenId, _fees);
      }
+  } else {
+      delete _isLiquidation[_collection][_tokenId];
+     }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Flayer |
| Report Date | N/A |
| Finders | Tendency, 0xNirix, 0xAlix2, zzykxx, Sentryx, blockchain555, 0x37, valuevalk, almantare, BugPull, kuprum, Ollam, BADROBINX, t.aksoy, h2134, utsav, araj, merlinboii, almurhasan |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-08-flayer-judging/issues/547
- **Contest**: https://app.sherlock.xyz/audits/contests/468

### Keywords for Search

`vulnerability`


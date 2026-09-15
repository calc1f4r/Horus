---
# Core Classification
protocol: Abacus
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48703
audit_firm: OtterSec
contest_link: https://abacus.wtf/
source_link: https://abacus.wtf/
github_link: github.com/0xMedici/abacusLend.

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
  - Robert Chen
  - Ajay Kunapareddy
  - OtterSec
  - Rajvardhan Agarwal
---

## Vulnerability Title

endAuction on Arbitrary NFTs in Closure Contract . . . . . .

### Overview


The Closure contract has a bug where an arbitrary contract can be used to end an auction and transfer the NFT to the highest bidder. This can lead to the liveAuctions counter being decremented even if the NFT is invalid. To fix this, a check for the existence of an NFT in the auction has been added in the endAuction function. This bug has been fixed in the a08c71c patch.

### Original Finding Content

## Closure Contract Vulnerability

In the Closure contract, `endAuction(address _nft, uint256 _id)` is used to end the auction and transfer the NFT to the highest bidder. As there is no validation on the NFT address, an arbitrary contract can be used. Invoking `endAuction` also decrements the `liveAuctions` counter (even if the NFT is invalid).

### Code Snippet

```solidity
// contracts/Closure.sol
auctionComplete[_nft][_id] = true;
IERC721(_nft).transferFrom(
    address(this),
    highestBidder[_nft][_id],
    _id
);
liveAuctions--;
```

The `liveAuctions` counter is subsequently used in the Vault contract to reset the pool.

## Proof of Concept

```solidity
// FakeNFT.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FakeNFT {
    // ERC721 functions
    function transferFrom(address from, address to, uint256 tokenId) external {}
}
```

Call the Closure contract: `endAuction(FakeNFT address, id)`.

## Remediation

Add a check for the existence of an NFT in auctions.

---

© 2022 OtterSec LLC. All Rights Reserved. 

### Abacus Audit 04 | Vulnerabilities

```solidity
// contracts/Closure.sol
function endAuction(address _nft, uint256 _id) external nonReentrant {
    require(
        block.timestamp > auctionEndTime[_nft][_id]
        && auctionEndTime[_nft][_id] != 0
        && !auctionComplete[_nft][_id]
    );
}
```

### Patch

Added a check to ensure the existence of an NFT in auction. Fixed in a08c71c.

```diff
// contracts/Closure.sol
@@ -145,6 +145,7 @@ contract Closure is ReentrancyGuard, Initializable {
 
 /// @param _id NFT ID
 function endAuction(address _nft, uint256 _id) external nonReentrant {
     uint256 _nonce = nonce[_nft][_id] - 1;
 +    require(auctionEndTime[_nonce][_nft][_id] != 0);
     require(
         block.timestamp > auctionEndTime[_nonce][_nft][_id]
         && !auctionComplete[_nonce][_nft][_id]
     );
}
```

© 2022 OtterSec LLC. All Rights Reserved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Abacus |
| Report Date | N/A |
| Finders | Robert Chen, Ajay Kunapareddy, OtterSec, Rajvardhan Agarwal |

### Source Links

- **Source**: https://abacus.wtf/
- **GitHub**: github.com/0xMedici/abacusLend.
- **Contest**: https://abacus.wtf/

### Keywords for Search

`vulnerability`


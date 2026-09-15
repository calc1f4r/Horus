---
# Core Classification
protocol: Babylon
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62354
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-01-17-Babylon.md
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
finders_count: 1
finders:
  - Hexens
---

## Vulnerability Title

[BAB-3] Stealing ETH using reentrancy in minting pass

### Overview


The report describes a critical bug in the BabylonCore smart contract, specifically in the `participate` function. This function allows users to buy tickets, which are NFTs that are minted and given to the user. However, there is a vulnerability that allows for reentrancy, meaning that the function can be called multiple times before it finishes executing. This can be exploited to inflate the number of tickets and steal ETH from the contract. The bug has been fixed by moving the `mint` function to the end of the `participate` function or by adding a reentrancy guard.

### Original Finding Content

**Severity:** Critical

**Path:** BabylonCore.sol:participate (L89-114)

**Description:** In `BabylonCore.sol:participate` a user can buy tickets, which are minting pass NFTs and minted to the user. The minting pass contracts uses `_safeMint`, which makes an external call with `onERC721Received` to the receiver user and thus that execution is passed to the user upon minting. 

As a result, a reentrancy vulnerability exists because there are state changing effects after the call to mint on L102, e.g. the current tickets total on L104 and the listing’s state on L110.

This vulnerability can be abused to inflate the listing’s current tickets beyond the total tickets and refund/burn tickets without cancelling the listing. The creator could buy and refund a part of the tickets but still gain the full amount of ETH when the listing is finalized, netting a positive amount and thus effectively stealing ETH.
```
function participate(uint256 id, uint256 tickets) external payable {
    ListingInfo storage listing =  _listingInfos[id];
    require(
        _tokensController.checkApproval(listing.creator, listing.item),
        "BabylonCore: Token is no longer owned or approved to the controller"
    );
    require(listing.state == ListingState.Active, "BabylonCore: Listing state should be active");
    require(block.timestamp >= listing.timeStart, "BabylonCore: Too early to participate");
    uint256 current = listing.currentTickets;
    require(current + tickets <= listing.totalTickets, "BabylonCore: no available tickets");
    uint256 totalPrice = listing.price * tickets;
    require(msg.value == totalPrice, "BabylonCore: msg.value doesn't match price for tickets");

    IBabylonMintPass(listing.mintPass).mint(msg.sender, tickets);

    listing.currentTickets = current + tickets;

    emit NewParticipant(id, msg.sender, tickets);

    if (listing.currentTickets == listing.totalTickets) {
        listing.randomRequestId = _randomProvider.requestRandom(id);
        listing.state = ListingState.Resolving;

        emit ListingResolving(id, listing.randomRequestId);
    }
}
```

**Remediation:**  The call to `mint` should be done at the end of the function or a reentrancy guard should be added to the function.

**Status:**  Fixed


- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Babylon |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-01-17-Babylon.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


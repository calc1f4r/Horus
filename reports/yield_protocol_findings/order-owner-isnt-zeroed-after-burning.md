---
# Core Classification
protocol: CLOBER
chain: everychain
category: uncategorized
vulnerability_type: nft

# Attack Vector Details
attack_type: nft
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7261
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - nft
  - don't_update_state

protocol_categories:
  - dexes
  - bridge
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Desmond Ho
  - Grmpyninja
  - Christoph Michel
  - Throttle
  - Taek Lee
---

## Vulnerability Title

Order owner isn't zeroed after burning

### Overview


This bug report is about an issue with the OrderBook and OrderNFT contracts. The problem is that when an NFT is burnt, the order's owner is not zeroed out. This means that while the onBurn() method records the NFT as being transferred to the zero address, ownerOf() still returns the current order's owner. This can lead to malicious actors being able to call approve() and safeTransferFrom() functions on non-existent tokens. This allows them to sell the NFTs on secondary exchanges for profit, even though they have no monetary value. 

To fix the issue, the owner should be zeroed in the _burnToken() function. The fix was implemented in PR 334 and verified by Spearbit. The owner of the order is now correctly zeroed in the OrderBook after burning the NFT.

### Original Finding Content

## Severity: Medium Risk

## Context
- `OrderBook.sol#L821-L823`
- `OrderNFT.sol#L78-L82`
- `OrderNFT.sol#L189`

## Description
The order's owner is not zeroed out when the NFT is burnt. As a result, while the `onBurn()` method records the NFT to have been transferred to the zero address, `ownerOf()` still returns the current order's owner. This allows for unexpected behaviour, like being able to call `approve()` and `safeTransferFrom()` functions on non-existent tokens.

A malicious actor could sell such resurrected NFTs on secondary exchanges for profit even though they have no monetary value. Such NFTs will revert on cancellation or claim attempts since `openOrderAmount` is zero.

### Code Example
```solidity
function testNFTMovementAfterBurn() public {
    _createOrderBook(0, 0);
    address attacker2 = address(0x1337);
    // Step 1: make 2 orders to avoid bal sub overflow when moving burnt NFT in step 3
    uint256 orderIndex1 = _createPostOnlyOrder(Constants.BID, Constants.RAW_AMOUNT);
    _createPostOnlyOrder(Constants.BID, Constants.RAW_AMOUNT);
    CloberOrderBook.OrderKey memory orderKey = CloberOrderBook.OrderKey({
        isBid: Constants.BID,
        priceIndex: Constants.PRICE_INDEX,
        orderIndex: orderIndex1
    });
    uint256 tokenId = orderToken.encodeId(orderKey);
    // Step 2: burn 1 NFT by cancelling one of the orders
    vm.startPrank(Constants.MAKER);
    orderBook.cancel(Constants.MAKER, _toArray(orderKey));
    // verify ownership is still maker
    assertEq(orderToken.ownerOf(tokenId), Constants.MAKER, "NFT_OWNER");
    // Step 3: resurrect burnt token by calling safeTransferFrom
    orderToken.safeTransferFrom(Constants.MAKER, attacker2, tokenId);
    // verify ownership is now attacker2
    assertEq(orderToken.ownerOf(tokenId), attacker2, "NFT_OWNER");
}
```

## Recommendation
The owner should be zeroed in `_burnToken()`.
```solidity
function _burnToken(OrderKey memory orderKey) internal {
    CloberOrderNFT(orderToken).onBurn(orderKey.isBid, orderKey.priceIndex, orderKey.orderIndex);
    _getOrder(orderKey).owner = address(0);
}
```

## Status
- **Clober**: Fixed in PR 334.
- **Spearbit**: Verified. The owner of the order is correctly zeroed in the `OrderBook` after burning the NFT.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | CLOBER |
| Report Date | N/A |
| Finders | Desmond Ho, Grmpyninja, Christoph Michel, Throttle, Taek Lee |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf

### Keywords for Search

`NFT, Don't update state`


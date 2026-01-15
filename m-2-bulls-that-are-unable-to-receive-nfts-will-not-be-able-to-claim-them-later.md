---
# Core Classification
protocol: Bull v Bear
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3712
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/23
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-bullvbear-judging/issues/4

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 1

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - cross_chain
  - rwa
  - payments

# Audit Details
report_date: unknown
finders_count: 10
finders:
  - cccz
  - bin2chen
  - WATCHPUG
  - 0xmuxyz
  - hansfriese
---

## Vulnerability Title

M-2: Bulls that are unable to receive NFTs will not be able to claim them later

### Overview


This bug report is about an issue found in the BullvBear protocol, which is a decentralized exchange protocol. The issue is that if a bull has a contract address that doesn't accept ERC721s (Non-Fungible Tokens), the NFT is saved to `withdrawableCollectionTokenId` for later withdrawal. However, because there is no way to withdraw this token to a different address (and the original address doesn't accept NFTs), it will never be able to be claimed. 

This vulnerability was found by GimelSec, bin2chen, 0xadrii, rvierdiiev, cccz, obront, 0xmuxyz, carrot, hansfriese, and WATCHPUG. The issue was found through manual review.

The impact of this issue is that if a bull is a contract that can't receive NFTs, their orders will be matched, the bear will be able to withdraw their assets, but the bull's NFT will remain stuck in the BVB protocol contract.

There are a few possible solutions to this issue, such as adding a `to` field in the `withdrawToken` function, which allows the bull to withdraw the NFT to another address; creating a function similar to `transferPosition` that can be used to transfer owners of a withdrawable NFT; or deciding that you want to punish bulls who aren't able to receive NFTs, in which case there is no need to save their address or implement a `withdrawToken` function. The issue has been fixed with the PR#14, which allows users to transfer their positions to whatever EOA or smart contract they want before calling reclaimContract() to retrieve ERC20 assets or ERC721.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-bullvbear-judging/issues/4 

## Found by 
GimelSec, bin2chen, 0xadrii, rvierdiiev, cccz, obront, 0xmuxyz, carrot, hansfriese, WATCHPUG

## Summary

A lot of care has been taken to ensure that, if a bull has a contract address that doesn't accept ERC721s, the NFT is saved to `withdrawableCollectionTokenId` for later withdrawal. However, because there is no way to withdraw this token to a different address (and the original address doesn't accept NFTs), it will never be able to be claimed.

## Vulnerability Detail

To settle a contract, the bear calls `settleContract()`, which sends their NFT to the bull, and withdraws the collateral and premium to the bear.

```solidity
try IERC721(order.collection).safeTransferFrom(bear, bull, tokenId) {}
catch (bytes memory) {
    // Transfer NFT to BvbProtocol
    IERC721(order.collection).safeTransferFrom(bear, address(this), tokenId);
    // Store that the bull has to retrieve it
    withdrawableCollectionTokenId[order.collection][tokenId] = bull;
}

uint bearAssetAmount = order.premium + order.collateral;
if (bearAssetAmount > 0) {
    // Transfer payment tokens to the Bear
    IERC20(order.asset).safeTransfer(bear, bearAssetAmount);
}
```
In order to address the case that the bull is a contract that can't accept NFTs, the protocol uses a try-catch setup. If the transfer doesn't succeed, it transfers the NFT into the contract, and sets `withdrawableCollectionTokenId` so that the specific NFT is attributed to the bull for later withdrawal.

However, assuming the bull isn't an upgradeable contract, this withdrawal will never be possible, because their only option is to call the same function `safeTransferFrom` to the same contract address, which will fail in the same way.

```solidity
function withdrawToken(bytes32 orderHash, uint tokenId) public {
    address collection = matchedOrders[uint(orderHash)].collection;

    address recipient = withdrawableCollectionTokenId[collection][tokenId];

    // Transfer NFT to recipient
    IERC721(collection).safeTransferFrom(address(this), recipient, tokenId);

    // This token is not withdrawable anymore
    withdrawableCollectionTokenId[collection][tokenId] = address(0);

    emit WithdrawnToken(orderHash, tokenId, recipient);
}
```

## Impact

If a bull is a contract that can't receive NFTs, their orders will be matched, the bear will be able to withdraw their assets, but the bull's NFT will remain stuck in the BVB protocol contract.

## Code Snippet

https://github.com/sherlock-audit/2022-11-bullvbear/blob/main/bvb-protocol/src/BvbProtocol.sol#L394-L406

https://github.com/sherlock-audit/2022-11-bullvbear/blob/main/bvb-protocol/src/BvbProtocol.sol#L450-L462

## Tool used

Manual Review

## Recommendation

There are a few possible solutions:
- Add a `to` field in the `withdrawToken` function, which allows the bull to withdraw the NFT to another address
- Create a function similar to `transferPosition` that can be used to transfer owners of a withdrawable NFT
- Decide that you want to punish bulls who aren't able to receive NFTs, in which case there is no need to save their address or implement a `withdrawToken` function

## Discussion

**datschill**

PR fixing another issue, removing the withdrawToken() method : https://github.com/BullvBear/bvb-solidity/pull/14

**datschill**

This issue isn't High, because in the default behavior, no smart contract can match an Order. So for a Bull to be a smart contract, the user needs to match an order (as a maker or a taker) with an EOA, then transfer his position to a smart contract. This would be kind of a poweruser move, so we consider that he should be aware that his smart contract should handle NFT reception.
Whatsoever, the issue is fixed thanks to the PR#14, the user will be able to transfer his position to whatever EOA or smart contract he wants before calling reclaimContract() to retrieve ERC20 assets or ERC721.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 1/5 |
| Audit Firm | Sherlock |
| Protocol | Bull v Bear |
| Report Date | N/A |
| Finders | cccz, bin2chen, WATCHPUG, 0xmuxyz, hansfriese, 0xadrii, rvierdiiev, obront, GimelSec, carrot |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-bullvbear-judging/issues/4
- **Contest**: https://app.sherlock.xyz/audits/contests/23

### Keywords for Search

`vulnerability`


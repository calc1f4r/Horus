---
# Core Classification
protocol: Bull v Bear
chain: everychain
category: dos
vulnerability_type: gas_limit

# Attack Vector Details
attack_type: gas_limit
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3709
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/23
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-bullvbear-judging/issues/111

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - gas_limit
  - dos

protocol_categories:
  - dexes
  - cdp
  - cross_chain
  - rwa
  - payments

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Bahurum
  - ElKu
  - WATCHPUG
  - KingNFT
  - ak1
---

## Vulnerability Title

H-3: Bull can prevent `settleContract()`

### Overview


This bug report concerns the `settleContract()` function in the BvbProtocol.sol file. It was found by Bahurum, KingNFT, ak1, ElKu, and WATCHPUG. The issue is that the bull can intentionally cause out-of-gas and revert the transaction and prevent `settleContract()`. This is possible because `IERC721(order.collection).safeTransferFrom()` is used in `settleContract()` which calls `IERC721Receiver(to).onERC721Received()` when the `to` address is an contract. This means the bull can use up all the gas to prevent the transaction from happening. As a result, the bear (victim) cannot `settleContract()` and cannot exercise their put option rights, and the bull (attacker) always wins. The code snippet and recommendation for a fix are included in the report. A Pull Request (PR) has already been created to fix the issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-bullvbear-judging/issues/111 

## Found by 
Bahurum, KingNFT, ak1, ElKu, WATCHPUG

## Summary

The bull can intentionally cause out-of-gas and revert the transaction and prevent `settleContract()`.

## Vulnerability Detail

As `IERC721(order.collection).safeTransferFrom()` is used in `settleContract()` which will call `IERC721Receiver(to).onERC721Received()` when the `to` address is an contract. 

This gives the bull a chance to intentionally prevent the transaction from happening by consuming a lot of gas and revert the whole transaction.

## Impact

The bear (victim) can not `settleContract()` therefore cannot exercise their put option rights. The bull (attacker) always wins.

## Code Snippet

https://github.com/sherlock-audit/2022-11-bullvbear/blob/main/bvb-protocol/src/BvbProtocol.sol#L374-L411


## Tool used

Manual Review

## Recommendation

```diff
function settleContract(Order calldata order, uint tokenId) public nonReentrant {
    bytes32 orderHash = hashOrder(order);

    // ContractId
    uint contractId = uint(orderHash);

    address bear = bears[contractId];

    // Check that only the bear can settle the contract
    require(msg.sender == bear, "ONLY_BEAR");

    // Check that the contract is not expired
    require(block.timestamp < order.expiry, "EXPIRED_CONTRACT");

    // Check that the contract is not already settled
    require(!settledContracts[contractId], "SETTLED_CONTRACT");

    address bull = bulls[contractId];

-    // Try to transfer the NFT to the bull (needed in case of a malicious bull that block transfers)
-    try IERC721(order.collection).safeTransferFrom(bear, bull, tokenId) {}
-    catch (bytes memory) {
        // Transfer NFT to BvbProtocol
        IERC721(order.collection).safeTransferFrom(bear, address(this), tokenId);
        // Store that the bull has to retrieve it
        withdrawableCollectionTokenId[order.collection][tokenId] = bull;
-    }

    uint bearAssetAmount = order.premium + order.collateral;
    if (bearAssetAmount > 0) {
        // Transfer payment tokens to the Bear
        IERC20(order.asset).safeTransfer(bear, bearAssetAmount);
    }

    settledContracts[contractId] = true;

    emit SettledContract(orderHash, tokenId, order);
}
```

## Discussion

**datschill**

PR fixing this issue : https://github.com/BullvBear/bvb-solidity/pull/14

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Bull v Bear |
| Report Date | N/A |
| Finders | Bahurum, ElKu, WATCHPUG, KingNFT, ak1 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-bullvbear-judging/issues/111
- **Contest**: https://app.sherlock.xyz/audits/contests/23

### Keywords for Search

`Gas Limit, DOS`


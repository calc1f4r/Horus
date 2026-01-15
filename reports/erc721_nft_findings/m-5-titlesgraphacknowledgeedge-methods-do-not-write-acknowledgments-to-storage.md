---
# Core Classification
protocol: TITLES Publishing Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33130
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/326
source_link: none
github_link: https://github.com/sherlock-audit/2024-04-titles-judging/issues/212

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
finders_count: 15
finders:
  - kennedy1030
  - i3arba
  - radin200
  - 4rdiii
  - KupiaSec
---

## Vulnerability Title

M-5: TitlesGraph::acknowledgeEdge() methods do not write acknowledgments to storage

### Overview


This bug report discusses an issue with the `acknowledgeEdge()` method in the `TitlesGraph` contract. The issue was found by multiple users and involves the caching of data in memory instead of storage, which prevents changes to the `Edge` struct from being saved. This results in the `acknowledgeEdge()` method not working as intended. The impact of this bug is that edges cannot be acknowledged. The report includes a code snippet and a test that can be used to reproduce the issue. The recommendation is to change `memory` to `storage` in the `_setAcknowledged()` function to fix the issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-04-titles-judging/issues/212 

## Found by 
4rdiii, AlexCzm, CodeWasp, KupiaSec, alexzoid, brakeless, cducrest-brainbot, den\_sosnovskyi, fugazzi, i3arba, ironside, kennedy1030, radin200, recursiveEth, ubl4nk
## Summary
When `acknowledgeEdge()` is called, the downstream call to the `_setAcknowledged()` method caches `edges[edgeId_]` in memory, instead of storage, which does not preserve changes to the `Edge` struct after the transaction concludes. 

## Vulnerability Detail
```solidity
function acknowledgeEdge(bytes32 edgeId_, bytes calldata data_)
    external
    override
    returns (Edge memory edge)
{
    if (!_isCreatorOrEntity(edges[edgeId_].to, msg.sender)) revert Unauthorized();
    return _setAcknowledged(edgeId_, data_, true);
}

function _setAcknowledged(bytes32 edgeId_, bytes calldata data_, bool acknowledged_)
    internal
    returns (Edge memory edge)
{
    if (!_edgeIds.contains(edgeId_)) revert NotFound();
    edge = edges[edgeId_];
    edge.acknowledged = acknowledged_;    // @audit does this actually write to storage? the state isn't saved? 

    if (acknowledged_) {
        emit EdgeAcknowledged(edge, msg.sender, data_);
    } else {
        emit EdgeUnacknowledged(edge, msg.sender, data_);
    }
}
```

In the code snippet above, `edges[edgeId_]` is cached in `edge`, then modified.

The issue is that `edge`, the return variable, is marked as memory, which does not save the state after the transaction ends.

Therefore, the `acknowledged` value never changes and the `acknowledgeEdge()` methods do not work as intended.

Add the following test to `TitlesGraph.t.sol`. 

Run with the following command: `forge test --match-test test_acknowledgeEdgeFailure -vvvv`
```solidity
function test_acknowledgeEdgeFailure() public {
    Node memory from = Node({
        nodeType: NodeType.COLLECTION_ERC1155,
        entity: Target({target: address(1), chainId: block.chainid}),
        creator: Target({target: address(2), chainId: block.chainid}),
        data: ""
    });

    Node memory to = Node({
        nodeType: NodeType.TOKEN_ERC1155,
        entity: Target({target: address(3), chainId: block.chainid}),
        creator: Target({target: address(4), chainId: block.chainid}),
        data: abi.encode(42)
    });

    // Only the `from` node's entity can create the edge.
    vm.prank(from.entity.target);
    titlesGraph.createEdge(from, to, "");

    vm.expectEmit(true, true, true, true);
    emit IEdgeManager.EdgeAcknowledged(
        Edge({from: from, to: to, acknowledged: true, data: ""}), to.creator.target, ""
    );

    // Only the `to` node's creator (or the entity itself) can acknowledge it
    vm.prank(to.creator.target);
    titlesGraph.acknowledgeEdge(keccak256(abi.encode(from, to)), "");

    (Node memory nodeTo,
        Node memory nodeFrom,
        bool ack,
        bytes memory dataResult
    ) = titlesGraph.edges(titlesGraph.getEdgeId(from, to));
    console.log(ack);

    // edge[edgeId].acknowledged should be set to true after successful call to titlesGraph.acknowledgeEdge()
    // However, the value is still false.
    assert(true == ack);
}
```

```solidity
[FAIL. Reason: panic: assertion failed (0x01)] test_acknowledgeEdgeFailure() (gas: 429897)
Logs:
  false
```

## Impact
Edges are unable to be acknowledged.

## Code Snippet
https://github.com/sherlock-audit/2024-04-titles/blob/main/wallflower-contract-v2/src/graph/TitlesGraph.sol#L103-L124

## Tool used
Manual Review

## Recommendation
The simplest fix would be to change `memory` to `storage`.
```solidity
function _setAcknowledged(bytes32 edgeId_, bytes calldata data_, bool acknowledged_)
     internal
-    returns (Edge memory edge)
+    returns (Edge storage edge) 
 {
     if (!_edgeIds.contains(edgeId_)) revert NotFound();
     edge = edges[edgeId_];
     edge.acknowledged = acknowledged_;    

     if (acknowledged_) {
         emit EdgeAcknowledged(edge, msg.sender, data_);
     } else {
         emit EdgeUnacknowledged(edge, msg.sender, data_);
     }
 }
```




## Discussion

**pqseags**

This will be fixed

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | TITLES Publishing Protocol |
| Report Date | N/A |
| Finders | kennedy1030, i3arba, radin200, 4rdiii, KupiaSec, cducrest-brainbot, alexzoid, fugazzi, CodeWasp, recursiveEth, brakeless, den\_sosnovskyi, ironside, AlexCzm, ubl4nk |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-04-titles-judging/issues/212
- **Contest**: https://app.sherlock.xyz/audits/contests/326

### Keywords for Search

`vulnerability`


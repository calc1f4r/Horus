---
# Core Classification
protocol: Y2K
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18542
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/57
source_link: none
github_link: https://github.com/sherlock-audit/2023-03-Y2K-judging/issues/172

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
finders_count: 13
finders:
  - TrungOre
  - ShadowForce
  - immeas
  - bin2chen
  - hickuphh3
---

## Vulnerability Title

M-5: Malicious user can make rolloverQueue never get processed

### Overview


This bug report is about the issue M-5, which is related to the Carousel contract of the 2023-03-Y2K-judging project. It was found by Ace-30, ElKu, Respx, ShadowForce, TrungOre, bin2chen, ck, evan, hickuphh3, immeas, minhtrng, nobody2018, and twicek.

The issue is that a malicious user can make the `rolloverQueue` shared by all epochs never get processed. This is done by making the `rolloverQueue.length` huge, causing the relayer to consume a huge amount of gas for every round of epoch. As a result, Carousel will not be able to send relayerFee to the relayer, making them unwilling to call `mintRollovers`. Ultimately, the `rolloverQueue` will never be processed, resulting in a permanent DOS.

The vulnerability is explained with an example. Bob creates 1000 addresses, each address has `setApprovalForAll` to Bob. He calls two functions for each address, namely `Carousel.safeTransferFrom` and `Carousel.enlistInRollover`. This makes the `rolloverQueue.length` equal to 1010 (1000+10). These 1000 addresses will never call `delistInRollover` to exit the rolloverQueue, so no matter whether they win or lose, their QueueItems will always be in the rolloverQueue. This makes the relayer process at least 1000 QueueItems in each round of epoch, resulting in a huge amount of gas consumption.

The code snippet and manual review were used to analyze the issue. The recommendation given is to change the single queue to queue mapping, so that the relayer only needs to process the queue corresponding to the epochId. 3xHarry and IAm0x52 have given their opinions about the feasibility of the attack. The issue has been acknowledged by the sponsor.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-03-Y2K-judging/issues/172 

## Found by 
Ace-30, ElKu, Respx, ShadowForce, TrungOre, bin2chen, ck, evan, hickuphh3, immeas, minhtrng, nobody2018, twicek

## Summary

`rolloverQueue` is **shared by all epochs**. For each round of epoch, `mintRollovers` will process `rolloverQueue` from the beginning. A normal user calls `enlistInRollover` to enter the rolloverQueue, and in the next round of epoch, he will call `delistInRollover` to exit the rolloverQueue. In this case, `rolloverQueue.length` is acceptable. However, malicious user can make the `rolloverQueue.length` huge, causing the relayer to **consume a huge amount of gas for every round of epoch**. Carousel will send relayerFee to relayer in order to encourage external relayer to call `mintRollovers`. Malicious user can make external relayer unwilling to call `mintRollovers`. **Ultimately, rolloverQueue will never be processed.**

## Vulnerability Detail

Let's assume the following scenario:

**relayerFee is 1e18**. The current epochId is E1, and the next epochId is E2. At present, `rolloverQueue` has 10 normal user `QueueItem`. Bob has deposited 1000e18 assets before the start of E1, so `balanceOf(bob, E1) = 1000e18`.

1.  Bob creates 1000 addresses, each address has `setApprovalForAll` to bob. He calls two functions for each address:
    
    `Carousel.safeTransferFrom(bob, eachAddress, E1, 1e18)`
    
    `Carousel.enlistInRollover(E1, 1e18, eachAddress)`, **1e18 equal to minRequiredDeposit**.
    
2.  `rolloverQueue.length` equals to 1010(1000+10). 
    

These 1000 addresses will **never** call `delistInRollover` to exit the rolloverQueue, so no matter whether these addresses win or lose, **their QueueItem will always be in the rolloverQueue**. In each round of epoch, the relayer has to process at least 1000 QueueItems, and these QueueItems are useless. **Malicious users only need to do it once to cause permanent affects**. 

**When a normal user loses in a certain round of epoch, he may not call delistInRollover to exit the rolloverQueue**. For example, he left the platform and stopped playing. **In this case, rolloverQueue.length will become larger and larger as time goes by**.

**Carousel contract will not send any relayerFee to the relayer, because these useless QueueItem will not increase the value of  [[executions](https://github.com/sherlock-audit/2023-03-Y2K/blob/main/Earthquake/src/v2/Carousel/Carousel.sol#L447)](https://github.com/sherlock-audit/2023-03-Y2K/blob/main/Earthquake/src/v2/Carousel/Carousel.sol#L447). Obviously, calling `mintRollovers` has no benefit for the relayer. Therefore, no relayer is willing to do this.**

## Impact

The relayer consumes a huge amount of gas for calling `mintRollovers` for each round of epoch. **In other words, as long as the rolloverQueue is unacceptably long, it is a permanent DOS**.

## Code Snippet

https://github.com/sherlock-audit/2023-03-Y2K/blob/main/Earthquake/src/v2/Carousel/Carousel.sol#L361-L459

https://github.com/sherlock-audit/2023-03-Y2K/blob/main/Earthquake/src/v2/Carousel/Carousel.sol#L238-L271

## Tool used

Manual Review

## Recommendation

We should change the single queue to **queue mapping**. In this way, relayer only needs to process the queue corresponding to the epochId.

```solidity
--- a/Earthquake/src/v2/Carousel/Carousel.sol
+++ b/Earthquake/src/v2/Carousel/Carousel.sol
@@ -23,7 +23,7 @@ contract Carousel is VaultV2 {
     IERC20 public immutable emissionsToken;
 
     mapping(address => uint256) public ownerToRollOverQueueIndex;
-    QueueItem[] public rolloverQueue;
+    mapping(uint256 => QueueItem[]) public rolloverQueues;
     QueueItem[] public depositQueue;
     mapping(uint256 => uint256) public rolloverAccounting;
     mapping(uint256 => mapping(address => uint256)) public _emissionsBalances;
```




## Discussion

**3xHarry**

I would disagree with the feasibility of this attack. 
1. there is a non neglectable minDeposit which makes this attack much more expensive
2. the queue can be processed in multiple transactoins and the relayerFee is supposed to be configured so much so that each processed item gas consumption is reimbursed with a profit 


**IAm0x52**

Issue has been acknowledged by sponsor

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Y2K |
| Report Date | N/A |
| Finders | TrungOre, ShadowForce, immeas, bin2chen, hickuphh3, ElKu, Respx, Ace-30, twicek, evan, nobody2018, minhtrng, ck |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-03-Y2K-judging/issues/172
- **Contest**: https://app.sherlock.xyz/audits/contests/57

### Keywords for Search

`vulnerability`


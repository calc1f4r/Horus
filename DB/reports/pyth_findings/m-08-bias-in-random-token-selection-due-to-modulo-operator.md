---
# Core Classification
protocol: apDAO_2024-10-03
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44409
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/apDAO-security-review_2024-10-03.md
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

[M-08] Bias in random token selection due to modulo operator

### Overview


This bug report discusses an issue with the function `_createAuctionWithRandomNumber` in the file ApiologyDAOAuctionHouse.sol. The function uses a modulo operation to select a random index from the `auctionQueue`, which can lead to an uneven distribution of selection probabilities. This can potentially favor certain NFTs over others in the auction queue, especially in large queues. The report recommends using a different method to select a random index to mitigate this bias.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The function `_createAuctionWithRandomNumber` uses a modulo operation to select a random index from the `auctionQueue`:

```solidity
File: ApiologyDAOAuctionHouse.sol
378:     function _createAuctionWithRandomNumber(bytes32 randomNumber) internal {
...
390:         if (auctionQueue.length > 0) {
391:>>>          uint256 randomIndex = uint256(randomNumber) % auctionQueue.length;
392:             apdaoId = auctionQueue[randomIndex];
393:
394:             // Remove the selected token from the queue
395:             auctionQueue[randomIndex] = auctionQueue[auctionQueue.length - 1];
396:             auctionQueue.pop();
397:
398:             // Emit the removal event
399:             uint256[] memory removedTokens = new uint256[](1);
400:             removedTokens[0] = apdaoId;
401:             emit TokensRemovedFromAuctionQueue(removedTokens, nftOwners[apdaoId]);
402:         } else {
...
```

This can lead to an uneven distribution of selection probabilities across the tokens in the queue, the [pyth documentation](https://docs.pyth.network/entropy/best-practices) says:

> Notice that using the modulo operator can distort the distribution of random numbers if it's not a power of 2. This is negligible for small and medium ranges, but it can be noticeable for large ranges. For example, if you want to generate a random number between 1 and 52, the probability of having value 5 is approximately 10^-77 higher than the probability of having value 50 which is infinitesimal.

In this case, if `auctionQueue.length` does not evenly divide the range of `randomNumber`, some indices may have a higher probability of being chosen than others. This can lead to an uneven selection process, potentially favoring certain NFTs over others in the auction queue. This is particularly concerning in large queues.

## Recommendations

To mitigate the bias introduced by the modulo operation, consider using a different method to select a random index.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | apDAO_2024-10-03 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/apDAO-security-review_2024-10-03.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


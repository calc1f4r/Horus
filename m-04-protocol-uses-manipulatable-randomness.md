---
# Core Classification
protocol: Subsquid
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58252
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Subsquid-security-review.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 2

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-04] Protocol uses manipulatable randomness

### Overview


This bug report discusses an issue with how a protocol generates a random number to choose a distributor for rewards. The current method is not safe and can be manipulated, which could lead to malicious actors being able to control the rewards. The report suggests using a different method for generating randomness and considering using a different system in the future.

### Original Finding Content

## Severity

**Impact**: Medium, distributors are generally trusted actors, but this could be a vector for manipulation.

**Likelihood**: Medium, randomness can be manipulated via multiple vectors

## Description

The protocol generates a random number to choose which distributor will be able to commit rewards for a span of blocks. The issue is in the way the protocol generates this randomness.

```solidity
function distributorIndex() public view returns (uint256) {
    uint256 slotStart = (block.number / 256) * 256;
    return uint256(blockhash(slotStart)) % distributors.length();
}
```

After this `distributionIndex` is calculated, it is used to select a distributor from the array.

There are two issues with this design:

1. Using `blockhash` is an unsafe way to generate randomness
2. The `slotStart` is manipulatable every 256 blocks

### 1. `blockhash` as source of randomness

In Arbitrum, transactions are ordered in first-come-first-serve ordering, and the sequencer responsible for ordering the transactions is centralized. However, the Arbitrum DAO plans to decentralize the sequencer in the future, meaning that malicious sequencers can keep including and broadcasting transactions until they can get a favourable hash for the block. Due to the nature of Arbitrum this is more difficult to pull of than in Ethereum mainnet, but is still possible once sequencer decentralization is achieved.

### 2. `slotStart` is manipulatable

`slotStart` is calculated as `(block.number / 256) * 256`. Now every time the `block.number` is a multiple of 256, `slotStart` will be calculated as the `block.number` itself.

According to the ethereum yellow paper, `blockhash` of the current block always returns 0. This is because the block hash of the current block hasnt been calculated yet. So every time the `block.number` is a multiple of 256, the `uint256(blockhash(slotStart))` will be calculated as 0. This allows the 0th distributor to make a commit everytime the `block.number` is a multiple of 256.

Since the randomness of the system is broken in these two ways, this is an issue

## Recommendations

Firstly, `blockhash` should never be called on the current block, which is what happens in scenario 2 above. So using the bloackhash of `slotStart-1` will give the same effect without the 0th index being able to manipulate the randomness.

Secondly, in the future the blockhash on arbitrum might be more manipulatable. considering using chainlink VRF to generate randomness in a more robust manner.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 2/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Subsquid |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Subsquid-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


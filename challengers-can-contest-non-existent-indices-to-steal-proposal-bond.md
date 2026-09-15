---
# Core Classification
protocol: Rocketpool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53684
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/rocket-pool/rocket-pool-8-houston-pdao/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/rocket-pool/rocket-pool-8-houston-pdao/review.pdf
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

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Challengers Can Contest Non-Existent Indices To Steal Proposal Bond

### Overview


The `getPollardRootIndex()` function has errors that allow users to create challenges for indices that are not supposed to be contested. This can result in lost proposal bonds for valid proposals. The issue occurs when calculating the `pollardRootIndex` of an index for a Merkle pollard with a depth of less than 5. This can be exploited if the challenger provides a valid witness for a non-existent node. The issue only affects trees with less than 32 indices and has been fixed in the latest commit. The recommended solution is to revert if the index depth exceeds the maxDepth of the Network Voting Tree. 

### Original Finding Content

## Description

Due to errors in the `getPollardRootIndex()` function, users are able to create challenges for indices that exceed the Network Voting Tree length under specific conditions. This issue allows users to directly challenge indices they should not be able to contest, which could lead to lost proposal bonds for valid proposals.

When calculating the `pollardRootIndex` of an index for a Merkle pollard with depth less than 5, the pollard root index will return 1 for all indices of depth at least 5. If we consider a case with 8 nodes, an index depth of 31 will return a pollard root index of 1. However, this exceeds the max depth of our Network Voting Tree’s Merkle pollard. The correct response would be a revert.

If the challenger can provide a valid witness for this non-existent node, the challenge hash will be updated to the 31st index. This will result in a challenge that cannot be responded to.

Note, this issue is only applicable to trees with less than 32 indices, hence a low likelihood of exploitation as there is a significant number of Rocket Pool nodes on the network already.

## Recommendations

The testing team recommends reverting if the index depth exceeds the maxDepth of the Network Voting Tree. This could be achieved as follows:

```solidity
// Index is within the first pollard depth
if (_index < 2 ** depthPerRound) {
    if (_index > maxDepth) {
        revert("index exceeds network tree");
    }
    return 1;
}
```

## Resolution

The issue has been addressed in commit `60684a7` as per the recommendations. The RocketPool has also provided the following comment:

"This also highlighted another unintentional behaviour. A challenge could be made at any of the first 5 depths of either the network tree or a node tree. This has been corrected so that only indices that are in depths of multiples of 5 can be challenged. This was the intended behaviour previously but was misimplemented. This improved `getPollardRootIndex()` also makes it impossible to submit a challenge deeper than the maximum depth of the tree as was intended."

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Rocketpool |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/rocket-pool/rocket-pool-8-houston-pdao/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/rocket-pool/rocket-pool-8-houston-pdao/review.pdf

### Keywords for Search

`vulnerability`


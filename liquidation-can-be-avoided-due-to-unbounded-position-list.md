---
# Core Classification
protocol: Panoptic Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33814
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/panoptic-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Liquidation Can Be Avoided Due to Unbounded Position List

### Overview


The Panoptic Pool has a feature called `positionIdList` that keeps track of all active positions for each account. However, this feature has some risks that could potentially harm the pool. One risk is that accounts with a large `positionIdList` can avoid being liquidated, which is a problem because liquidation is necessary for maintaining the pool's stability. Another risk is that well-collateralized accounts may not be able to mint more positions if their `positionIdList` becomes too long, which could lead to a loss of potential profits for the pool. To address these risks, it is recommended to set a limit on the length of `positionIdList` to ensure the pool's stability. This issue has been resolved.

### Original Finding Content

Each account in the Panoptic Pool has a `positionIdList` associated with it, containing all active positions. This list is used to validate the input holdings via the positionHash, calculate collateral requirements as well as compute the premia when minting a new `tokenId` or liquidating an entire account. The `positionIdList` is an unbounded array that could potentially expose the Panoptic pool to the following key risks.


**Underwater accounts with large `positionIdList` can avoid liquidation**


Account liquidation requires the burning of all active options associated with an account. It is possible to avoid liquidation of a margin-called account by keeping a large array of dummy positions to use up the block gas limit. Due to the many loops involved in the `liquidateAccount` call, it takes less than 200 tokenIds to exceed the block gas limit of 30 million.


**Well-collateralized account may not be able to mint further**


When minting an option, all past positions in `positionIdList` are passed in `mintOptions` as a parameter with the new position to mint appended at the end. The past positions are used to validate the position hash for the `msg.sender` and check the solvency status of the account. When the list of past positions becomes too large, the gas expense of processing the past checks could exceed the block gas limit. This will disable the account to mint a further position. From our experimentation, the limit is approximately of the magnitude of 2000 tokenIds for the current implementation.


In summary, the asymmetry of being able to mint much further than getting liquidated could allow malicious actors to expose the pool to unwanted losses by blocking liquidation. Since it is crucial for the system to evaluate the past positions of an account, consider setting an upper limit on the length of `positionIdList` to ensure that the liquidation of an underwater account can be executed.


***Update:** Resolved.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Panoptic Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/panoptic-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


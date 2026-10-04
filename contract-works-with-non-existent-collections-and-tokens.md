---
# Core Classification
protocol: Fantium
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28049
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Fantium/Fantium/README.md#1-contract-works-with-non-existent-collections-and-tokens
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
  - MixBytes
---

## Vulnerability Title

Contract works with non-existent collections and tokens

### Overview


This bug report discusses an issue with the View methods (`getRoyalties()`, `tokenURI()`) in that they work with non-existent collections. This means that incorrect royalty is returned for a non-existent collection, and that athletes and Platform Manager can change parameters for non-existent collections. Additionally, a user can try to mint non-existent collections for free via `FantiumMinterV1.mint()` if `maxInvocations` is set.

The bug report recommends checking the existing `collectionId` and `tokenId` to prevent this issue. An example of a classical implementation is given, which involves using the `require` and `_requireMinted` functions to ensure that the token exists prior to accessing it.

### Original Finding Content

##### Description
1. View methods (`getRoyalties()`, `tokenURI()`) work with non-existent collections.

In this example, incorrect royalty is returned for a non-existent collection:
```
await nftContract.getRoyalties(0);
## returns:
recipients: [
    '0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC',
    '0x0000000000000000000000000000000000000000'
]
bps: [
    BigNumber { value: "250" }, 
    BigNumber { value: "0" }
]
```

2. Athletes and Platform Manager can change parameters for non-existent collections. For example, function `updateCollectionAthleteAddress` (https://github.com/metaxu-art/fantium-smart-contracts/blob/cb2d97bc30c40321991fe5ab8fc798babba1610f/contracts/FantiumNFTV1.sol#L308).

3. A user can try to mint non-existent collections for free via `FantiumMinterV1.mint()` if `maxInvocations` is set. (https://github.com/metaxu-art/fantium-smart-contracts/blob/cb2d97bc30c40321991fe5ab8fc798babba1610f/contracts/FantiumMinterV1.sol#L241)

##### Recommendation
We recommend checking the existing `collectionId` and `tokenId`. An example of classical implementation:
```
require(_exists(tokenId), "Nonexistent token");
## or
function tokenURI(uint256 tokenId) public view virtual override
returns (string memory) {
    _requireMinted(tokenId);
    ...
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Fantium |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Fantium/Fantium/README.md#1-contract-works-with-non-existent-collections-and-tokens
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


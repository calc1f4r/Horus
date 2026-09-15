---
# Core Classification
protocol: EYWA
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44354
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/EYWA/DAO/README.md#8-missing-validation-in-proposalmanager_slice
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Missing validation in `ProposalManager._slice()`

### Overview

See description below for full details.

### Original Finding Content

##### Description
The `_slice()` function in the `ProposalManager` contract lacks proper validation of slice parameters:
```solidity
function _slice(
    bytes memory data_, 
    uint256 start_, 
    uint256 length_
) private pure returns (bytes memory result_) {
    if (data_.length < start_ + length_) {
        revert InvalidSliceParameters();
    }
    // No other checks for start_ and length_
    ...
}
```
https://gitlab.ubertech.dev/blockchainlaboratory/eywa-dao/blob/29465033f28c8d3f09cbc6722e08e44f443bd3b2/contracts/ProposalManager.sol#L265

Also it does not ensure that `start_` and `length_` are within valid bounds or properly aligned for memory operations. If `data_` is not a multiple of 32 bytes, a memory error can occur when using mload, which may attempt to access non-existent memory regions. This can lead to unexpected behavior or contract failure.

##### Recommendation
We recommend adding checks for `start_` and `length_` parameters are multiples of 32 bytes.

***

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | EYWA |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/EYWA/DAO/README.md#8-missing-validation-in-proposalmanager_slice
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


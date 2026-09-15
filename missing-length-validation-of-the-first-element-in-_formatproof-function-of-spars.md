---
# Core Classification
protocol: Linea ENS
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34973
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2024/06/linea-ens/
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
finders_count: 0
finders:
---

## Vulnerability Title

Missing Length Validation of the First Element in _formatProof Function of SparseMerkleProof Contract ✓ Fixed

### Overview


This bug report discusses a problem in the `_formatProof` function of the `SparseMerkleProof` contract. The function does not validate the length of the first element in the `_rawProof` array before extracting the first 32 bytes, which can lead to an error. The bug has been fixed in a pull request and the recommendation is to validate the length before extraction.

### Original Finding Content

#### Resolution



 The problem has been fixed in the [PR\#179](https://github.com/Consensys/linea-resolver/pull/179/files).
 

#### Description


In the `_formatProof` function in the `SparseMerkleProof` contract there is no length validation of the first element in the `_rawProof` array. The function extracts the first `32` bytes of the `_rawProof[0]` array element to assign to `nextFreeNode` without ensuring that this element contains at least `32` bytes, which can lead to a panic error if the length of `_rawProof[0]` is less than `32` bytes.


#### Examples


**packages/l1\-contracts/contracts/linea\-verifier/lib/SparseMerkleProof.sol:L162\-L169**



```
function _formatProof(
    bytes[] calldata _rawProof
) private pure returns (bytes32, bytes32, bytes32[] memory) {
    uint256 rawProofLength = _rawProof.length;
    uint256 formattedProofLength = rawProofLength - 2;

    bytes32[] memory proof = new bytes32[](formattedProofLength);
    bytes32 nextFreeNode = bytes32(_rawProof[0][:32]);

```
#### Recommendation


We recommend validating that the length of `_rawProof[0]` is at least `32` bytes before proceeding with the extraction of the first `32` bytes.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Linea ENS |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2024/06/linea-ens/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


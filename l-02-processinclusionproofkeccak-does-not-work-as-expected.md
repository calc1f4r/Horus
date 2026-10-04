---
# Core Classification
protocol: EigenLayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20061
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-04-eigenlayer
source_link: https://code4rena.com/reports/2023-04-eigenlayer
github_link: https://github.com/code-423n4/2023-04-eigenlayer-findings/issues/22

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

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-02] `processInclusionProofKeccak` does not work as expected

### Overview

See description below for full details.

### Original Finding Content


### Proof of Concept
The function `verifyInclusionKeccak` is not used anywhere but its in the scope of this audit. There is no validation that proof is a tree and a valid tree like it described in the comments. E.x. if proof is less than 32 length, that function will just return a leaf without reverting. In my opinion, function doesn't work as expected and can be exploited. I've submitted the same issue with `processInclusionProofSha256` function that lead to loss a funds for validator due the same issue.

```solidity
    function processInclusionProofKeccak(bytes memory proof, bytes32 leaf, uint256 index) internal pure returns (bytes32) {
        bytes32 computedHash = leaf;
        for (uint256 i = 32; i <= proof.length; i+=32) {
            if(index % 2 == 0) {
                // if ith bit of index is 0, then computedHash is a left sibling
                assembly {
                    mstore(0x00, computedHash)
                    mstore(0x20, mload(add(proof, i)))
                    computedHash := keccak256(0x00, 0x40)
                    index := div(index, 2)
                }
            } else {
                // if ith bit of index is 1, then computedHash is a right sibling
                assembly {
                    mstore(0x00, mload(add(proof, i)))
                    mstore(0x20, computedHash)
                    computedHash := keccak256(0x00, 0x40)
                    index := div(index, 2)
                }            
            }
        }
        return computedHash;
    }
```
[src/contracts/libraries/Merkle.sol#L49](https://github.com/code-423n4/2023-04-eigenlayer/blob/398cc428541b91948f717482ec973583c9e76232/src/contracts/libraries/Merkle.sol#L48)

### Recommended Mitigation Steps
I think its important to add security to that function like this:

```diff
    function processInclusionProofKeccak(bytes memory proof, bytes32 leaf, uint256 index) internal pure returns (bytes32) {
+        require(proof.length % 32 == 0 && proof.length > 0, "Invalid proof length");

        bytes32 computedHash = leaf;
        for (uint256 i = 32; i <= proof.length; i+=32) {
            if(index % 2 == 0) {
                // if ith bit of index is 0, then computedHash is a left sibling
                assembly {
                    mstore(0x00, computedHash)
                    mstore(0x20, mload(add(proof, i)))
                    computedHash := keccak256(0x00, 0x40)
                    index := div(index, 2)
                }
            } else {
                // if ith bit of index is 1, then computedHash is a right sibling
                assembly {
                    mstore(0x00, mload(add(proof, i)))
                    mstore(0x20, computedHash)
                    computedHash := keccak256(0x00, 0x40)
                    index := div(index, 2)
                }            
            }
        }
        return computedHash;
    }
```

**[Sidu28 (EigenLayer) confirmed](https://github.com/code-423n4/2023-04-eigenlayer-findings/issues/22#issuecomment-1545180646)**

**[Alex the Entreprenerd (judge) decreased severity to QA and commented](https://github.com/code-423n4/2023-04-eigenlayer-findings/issues/22#issuecomment-1572151682):**
 > https://github.com/code-423n4/2023-04-eigenlayer/blob/398cc428541b91948f717482ec973583c9e76232/src/contracts/operators/MerkleDelegationTerms.sol#L97-L107

```solidity
        // check inclusion of the leafHash in the tree corresponding to `merkleRoots[rootIndex]`
        require(
            Merkle.verifyInclusionKeccak(
                proof,
                merkleRoots[rootIndex].root,
                leafHash,
                nodeIndex
            ),
            "MerkleDelegationTerms.proveEarningsAndWithdraw: proof of inclusion failed"
        );

```

>Which calls `processInclusionProofKeccak`
>
>For this reason, I believe the finding to be a Refactoring. Adding the check in the function is a good idea, but the code in scope is safe.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | EigenLayer |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2023-04-eigenlayer
- **GitHub**: https://github.com/code-423n4/2023-04-eigenlayer-findings/issues/22
- **Contest**: https://code4rena.com/reports/2023-04-eigenlayer

### Keywords for Search

`vulnerability`


---
# Core Classification
protocol: Arbitrum Chains Challenge Protocol v2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43750
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-8-offchain-challenge-protocol-V2-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-8-offchain-challenge-protocol-V2-securityreview.pdf
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

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Simone Monica
  - Jaime Iglesias
---

## Vulnerability Title

Missing validation in Golang’s GeneratePreﬁxProof function

### Overview

See description below for full details.

### Original Finding Content

## Diﬃculty: Low

## Type: Patching

## Description

The Golang implementation of the `GeneratePrefixProof` function lacks data validation for certain cases. The `GeneratePrefixProof` function allows validators to generate a consistency proof that some Merkle expansion is a prefix of another. The function will first perform some checks and then generate the corresponding proof.

```go
func GeneratePrefixProof(
    prefixHeight uint64,
    prefixExpansion MerkleExpansion,
    leaves []common.Hash,
    rootFetcher MerkleExpansionRootFetcherFunc,
) ([]common.Hash, error) {
    height := prefixHeight
    postHeight := height + uint64(len(leaves))
    proof, _ := prefixExpansion.Compact()
    for height < postHeight {
        [...]
    }
    return proof, nil
}
```
*Figure 7.1: `GeneratePrefixProof` function in `prefix_proofs.go#L296-L351`*

Once a proof is generated, it can be verified through the `VerifyPrefixProof` function.

```go
func VerifyPrefixProof(cfg *VerifyPrefixProofConfig) error {
    if cfg.PreSize == 0 {
        return errors.Wrap(ErrCannotBeZero, "presize was 0")
    }
    root, rootErr := Root(cfg.PreExpansion)
    if rootErr != nil {
        return errors.Wrap(rootErr, "pre expansion root error")
    }
    if root != cfg.PreRoot {
        return errors.Wrap(ErrRootMismatch, "pre expansion root mismatch")
    }
    if cfg.PreSize != TreeSize(cfg.PreExpansion) {
        return errors.Wrap(ErrTreeSize, "pre expansion tree size")
    }
    if cfg.PreSize >= cfg.PostSize {
        return errors.Wrapf(
            ErrStartNotLessThanEnd,
            "presize %d >= postsize %d",
            cfg.PreSize,
            cfg.PostSize,
        )
    }
    [...]
}
```
*Figure 7.2: `VerifyPrefixProof` function in `prefix_proofs.go#L365-L440`*

The `VerifyPrefixProof` function will perform additional checks on the proof, such as checking whether the size of the prefix is zero or not. However, these checks could also be performed by the `GeneratePrefixProof` function to avoid the creation of proofs that are outright invalid once verified.

Finally, comparing the Golang implementation to the Solidity implementation found in the test folder shows that the Solidity version does explicitly include these checks, which indicates a divergence in the implementations of the `GeneratePrefixProof` function.

```solidity
function generatePrefixProof(uint256 preSize, bytes32[] memory newLeaves)
    internal
    pure
    returns (bytes32[] memory)
{
    require(preSize > 0, "Pre-size cannot be 0");
    require(newLeaves.length > 0, "No new leaves added");
    [...]
}
```
*Figure 7.3: `generatePrefixProof` function in `Utils.sol#L66-L99`*

## Exploit Scenario

The creation of proofs that cannot be verified is allowed. This hides implementation bugs, as validators running the code will see their proofs being rejected by the `VerifyPrefixProof` instead of the `GeneratePrefixProof` function.

## Recommendations

- **Short term:** Include the additional checks in the `GeneratePrefixProof`.
- **Long term:** Thoroughly document the divergent behavior and the expected behavior. The codebase would benefit from the implementation of property testing by first creating a list of properties each function would need to enforce; using unit tests to validate those properties; and finally expanding the fuzz tests using those properties as a baseline.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Arbitrum Chains Challenge Protocol v2 |
| Report Date | N/A |
| Finders | Simone Monica, Jaime Iglesias |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2023-8-offchain-challenge-protocol-V2-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2023-8-offchain-challenge-protocol-V2-securityreview.pdf

### Keywords for Search

`vulnerability`


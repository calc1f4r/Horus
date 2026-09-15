---
# Core Classification
protocol: NFTfi - GenArt
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50284
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/nftfi/nftfi-genart
source_link: https://www.halborn.com/audits/nftfi/nftfi-genart
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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

Predictable sources of randomness

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `Collection.sol` contracts rely on a pseudo-random number generation technique that introduces predictability. The generation of `tokenIdRandWordHash` in the `_mintInternal` function is based on elements that are inherently predictable, such as the global variables `blockhash(block.number - 1)` and `msg.sender`, and also the incrementing `startTokenId`.

- contracts/Collection.sol [Lines: 108-117]

```
        for (; i < _quantity; ) {
            bytes32 tokenIdRandWordHash = keccak256(
                abi.encodePacked(startTokenId + i, blockhash(block.number - 1), msg.sender)
            );
            tokenGenerationParams[startTokenId + i] = tokenIdRandWordHash;
            tokenGenerationParamsEvent[i] = tokenIdRandWordHash;
            unchecked {
                ++i;
            }
        }
```

  

The `tokenIdRandWordHash` is constructed by hashing a combination of the previous **blockhash**, an incremental **token ID** and the **msg.sender**. This approach presents two primary concerns:

* Predictability of `blockhash` : Utilizing the hash of the preceding block as part of the randomness source is inherently insecure. Given that the `blockhash` is publicly available and can be predicted by the time a transaction is mined, it does not provide a robust foundation for randomness, allowing the manipulation of `tokenIdRandWordHash`.
* The other components of the hash function, namely the incremented `startTokenId + i` and `msg.sender`, are predictable within the context of a transaction: `msg.sender` remains unchanged, and `startTokenId + i` follows a sequential order.

This could potentially allow users to gain undue advantage in the NFT minting process, such as preferential access to rare or valuable attributes or traits, by anticipating the associated hashes because they are relying on a predictable source of randomness.

##### BVSS

[AO:A/AC:L/AX:L/C:L/I:L/A:N/D:N/Y:N/R:N/S:C (3.9)](/bvss?q=AO:A/AC:L/AX:L/C:L/I:L/A:N/D:N/Y:N/R:N/S:C)

##### Recommendation

Adopting a more robust mechanism for randomness is advisable. Employing a Verifiable Random Function (VRF) from established third-party providers, like [Chainlink VRF](https://docs.chain.link/vrf), is recommended. This would guarantee the unpredictability and integrity of the randomness in `tokenIdRandWordHash` creation.

  

### Remediation Plan

**RISK ACCEPTED:** The **NFTfi team** accepted the risk related to this issue.

##### Remediation Hash

<https://github.com/NFTfi-Genesis/eth.gen-art/commit/6e5e3636dc2fca07a699078a444646baac1ecdac>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | NFTfi - GenArt |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/nftfi/nftfi-genart
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/nftfi/nftfi-genart

### Keywords for Search

`vulnerability`


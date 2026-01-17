---
# Core Classification
protocol: Aligned Layer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38368
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2024/08/aligned-layer/
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
finders_count: 2
finders:
  - Martin Ortner
  -  George Kobakhidze
                        
---

## Vulnerability Title

Use EIP-712-style Signed Hashing to Prevent Cross-Chain Signature Replaying ✓ Fixed

### Overview


This bug report discusses a potential security vulnerability in the implementation of a payment service contract. The current method of verifying user signatures is susceptible to cross-network replay attacks, which can compromise the security of the system. To address this issue, the report recommends implementing domain-bound signatures using the OpenZeppelin EIP712 and ECDSA libraries. This will provide a more robust and secure solution for signature validation. The bug has been resolved in stages through a series of pull requests, including adding the chainId to the hashed data and modifying the signed struct to be fully EIP-712 compliant. 

### Original Finding Content

#### Resolution



Addressed in stages:


* [PR 822](https://github.com/yetanotherco/aligned_layer/pull/822) by adding the chainId to the hashed data.
* [PR 916](https://github.com/yetanotherco/aligned_layer/pull/916), [PR 1041](https://github.com/yetanotherco/aligned_layer/pull/1041), and [PR 1054](https://github.com/yetanotherco/aligned_layer/pull/1054) by modifying the signed struct to be fully [EIP\-712](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-712.md) compliant.




#### Description


The current implementation uses a raw `ecrecover` function to verify whether a user signed a data structure by hashing the data directly. This approach is susceptible to cross\-network replay attacks. To enhance security and prevent such issues, the implementation should use a domain separator as specified in EIP\-712\.


**contracts/src/core/BatcherPaymentService.sol:L230\-L244**



```
function verifySignatureAndDecreaseBalance(
    bytes32 hash,
    SignatureData calldata signatureData,
    uint256 feePerProof
) private {
    bytes32 noncedHash = keccak256(
        abi.encodePacked(hash, signatureData.nonce)
    );

    address signer = ecrecover(
        noncedHash,
        signatureData.v,
        signatureData.r,
        signatureData.s
    );

```
#### Recommendation


Utilize the OpenZeppelin [EIP712](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/cryptography/EIP712.sol) and [ECDSA](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/cryptography/ECDSA.sol) libraries to implement domain\-bound signatures. These libraries provide robust and battle\-tested solutions for signature validation, mitigating common issues associated with ECDSA and preventing cross\-network replay attacks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Aligned Layer |
| Report Date | N/A |
| Finders | Martin Ortner,  George Kobakhidze
                         |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2024/08/aligned-layer/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


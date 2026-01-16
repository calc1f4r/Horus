---
# Core Classification
protocol: Nomic
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43743
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-11-nomic-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-11-nomic-securityreview.pdf
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
finders_count: 2
finders:
  - Tjaden Hess
  - Anish Naik
---

## Vulnerability Title

Potential output commitment collision

### Overview


This bug report discusses a potential issue in the Nomic sidechain where a malicious relayer could redirect deposited funds to an ETH account instead of a Nomic native sidechain account. This is due to a lack of domain separation and the use of the same commitment format for both types of accounts. The report recommends short-term and long-term solutions to address this issue, including serializing commitments with unique prefixes and documenting commitment formats and message hashing schemes. The client had already addressed this issue before the review, but the updated code was not included in the commit under review. 

### Original Finding Content

## Target: nomic/src/app.rs

## Description

Deposits to the Nomic sidechain from Bitcoin accounts include a commitment to a destination, indicating where the sidechain funds should be sent. Due to a lack of domain separation, a malicious relayer could cause deposited funds to be redirected to an ETH account rather than a Nomic native sidechain account. 

Figure 7.1 shows the commitment formats for each type of account:

```rust
pub fn commitment_bytes(&self) -> Result<Vec<u8>> {
    use sha2::{Digest, Sha256};
    use Dest::*;

    let bytes = match self {
        NativeAccount(addr) => addr.bytes().into(),
        Ibc(dest) => Sha256::digest(dest.encode()?).to_vec(),
        Fee => vec![1],
        EthAccount(addr) => addr.bytes().into(),
        EthCall(call, addr) => Sha256::digest((call.clone(), *addr).encode()?).to_vec(),
    };

    Ok(bytes)
}
```

Figure 1.1: Commitments for `NativeAccount` and `EthAccount` use the same 20-byte format (nomic/src/app.rs#1153–1165).

The `NativeAccount` and `EthAccount` destinations both use arbitrary 20-byte strings, while the `Ibc` and `EthCall` formats use Sha256 digests of arbitrary-length data. A malicious relayer could process a deposit using an `EthAccount` rather than the depositor’s `NativeAccount`, in which case the deposited funds would be burned.

Note that the client had already addressed this issue before the start of the review, but the updated code was not included in the commit under review.

## Exploit Scenario

A malicious relayer wants to harm depositors or the network’s reputation. She relays all incoming native deposits as `EthAccount` deposits, causing the deposited funds to be sent to an Ethereum account for which nobody holds the private key.

## Recommendations

- **Short term**: Serialize all commitments using unique prefixes to indicate what type of deposit the commitment is for.
- **Long term**: Document the formats of all commitments and message hashing schemes for signatures. Ensure that commitments and message encodings are injective by providing a decoding routine that can be used in unit testing.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Nomic |
| Report Date | N/A |
| Finders | Tjaden Hess, Anish Naik |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2024-11-nomic-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2024-11-nomic-securityreview.pdf

### Keywords for Search

`vulnerability`


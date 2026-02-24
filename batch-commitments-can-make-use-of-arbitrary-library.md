---
# Core Classification
protocol: Scroll EIP-4844 Support Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33398
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/scroll-eip-4844-support-audit
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
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Batch Commitments Can Make Use of Arbitrary Library

### Overview


The `commitBatch` function in the `ScrollChain` contract has a bug where the `_version` parameter can be set to any value, causing the function to use the wrong code and potentially leading to errors. This can happen if a version 1 batch is committed but the `_version` is set to 0. This issue is currently low risk as only authorized parties can access the function, but it could become more serious if more parties are given access in the future. The Scroll team has acknowledged this bug and plans to fix it in the future.

### Original Finding Content

In the [`commitBatch` function](https://github.com/scroll-tech/scroll/blob/8bd4277c13ec17670963848a24e4e1b135504f3f/contracts/src/L1/rollup/ScrollChain.sol#L267) of the `ScrollChain` contract, the [`_version`](https://github.com/scroll-tech/scroll/blob/8bd4277c13ec17670963848a24e4e1b135504f3f/contracts/src/L1/rollup/ScrollChain.sol#L268) parameter is used to define whether the version of the batch to commit is 0 or 1, as any other values will cause the `commitBatch` function to revert. If the [`_version` is 0](https://github.com/scroll-tech/scroll/blob/8bd4277c13ec17670963848a24e4e1b135504f3f/contracts/src/L1/rollup/ScrollChain.sol#L288-L310), the `_commitChunksV0` function, as well as the `BatchHeaderV0Codec` library, will be used to handle the data. Otherwise, if the [`_version` is 1](https://github.com/scroll-tech/scroll/blob/8bd4277c13ec17670963848a24e4e1b135504f3f/contracts/src/L1/rollup/ScrollChain.sol#L311-L335), the function will use the `_commitChunksV1` function, as well as the `BatchHeaderV1Codec` library.


However, the sequencer can arbitrarily define the `_version` value. This means a version 0 batch commitment can be forced to follow a version 1 commitment path and vice versa. For instance, if a version 1 batch was committed, but the `_version` parameter is set to 0, the `commitBatch` function will gracefully pass without throwing any error.


Note that this scenario has a low likelihood since, at the time of this audit, the `commitBatch` function is guarded by the `OnlySequencer` modifier, which allows access only to the Scroll relayer EOAs. However, the severity of this issue could increase if additional parties are granted the sequencer role in the future.


Consider validating the `_version` parameter to match the version of the committed batch.


***Update:** Acknowledged, will resolve. The Scroll team added [PR 1264](https://github.com/scroll-tech/scroll/pull/1264) at [commit c03cdad](https://github.com/scroll-tech/scroll/commit/c03cdada92b6c4bd6087298295a047cc66c8957f) explaining the rationale of addressing this potential risk in the future:*



> *We initially excluded the KZG commitment by assuming lack of presence of malicious Sequencer entities that collude with malicious Provers in the current threat model. Upon considering such a scenario (which is ruled out at present, but could eventually be possible in a decentralized setting), and as per cryptographic hygiene, we decided to include the KZG commitment (in the form of the blob's versioned hash, i.e. a hash of the commitment) while computing the Fiat-Shamir challenge. Since the blob's versioned hash is accepted as private witness to our circuits, we also include it in the preimage of the batch's public input hash (the public instance to our circuits).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Scroll EIP-4844 Support Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/scroll-eip-4844-support-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


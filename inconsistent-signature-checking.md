---
# Core Classification
protocol: UMA Across V2 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10605
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/uma-across-v2-audit/
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

protocol_categories:
  - dexes
  - bridge
  - cdp
  - cross_chain
  - indexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Inconsistent signature checking

### Overview


This bug report is concerning depositors who can update the relay fee associated with their transfer by signing a message describing this intention. The message is verified on the origin chain before emitting the event that notifies relayers, and verified again on the destination chain before the new fee can be used to fill the relay. The issue is that if the depositor uses a static ECDSA signature and both chains support the `ecrecover` opcode, both verifications should be identical. However, the OpenZeppelin Signature Checker library is also being used, which supports EIP-1271 validation for smart contracts. If the smart contract validation behaves differently on the two chains, valid contract signatures may be rejected on the destination chain. 

The bug was fixed in pull request #79 as of commit 2a41086f0d61caf0be8c2f3d1cdaf96e4f67f718. To mitigate the issue, consider including the `RequestedSpeedUpDeposit` event in the off-chain UMIP specification so that relayers that comply with the event would be reimbursed. Alternatively, consider removing support for EIP-1271 validation and relying entirely on ECDSA signatures.

### Original Finding Content

Depositors can [update the relay fee](https://github.com/across-protocol/contracts-v2/blob/bf03255cbd1db3045cd2fbf1580f24081f46b43a/contracts/SpokePool.sol#L329) associated with their transfer by signing a message describing this intention. The message is [verified on the origin chain](https://github.com/across-protocol/contracts-v2/blob/bf03255cbd1db3045cd2fbf1580f24081f46b43a/contracts/SpokePool.sol#L335) before emitting the event that notifies relayers, and [verified again on the destination chain](https://github.com/across-protocol/contracts-v2/blob/bf03255cbd1db3045cd2fbf1580f24081f46b43a/contracts/SpokePool.sol#L438) before the new fee can be used to fill the relay. If the depositor used a static ECDSA signature and both chains support the `ecrecover` opcode, both verifications should be identical. However, verification uses the [OpenZeppelin Signature Checker](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v4.4/contracts/utils/cryptography/SignatureChecker.sol) library, which also supports [EIP-1271](https://eips.ethereum.org/EIPS/eip-1271) validation for smart contracts. If the smart contract validation behaves differently on the two chains, valid contract signatures may be rejected on the destination chain. A plausible example would be a multisignature wallet on the source chain that is not replicated on the destination chain.


Instead of validating the signature on the destination chain, consider including the [`RequestedSpeedUpDeposit` event](https://github.com/across-protocol/contracts-v2/blob/5a65be1701ddf6673f42b7e06dc122bf8e1a6b0b/contracts/SpokePool.sol#L339) in the off-chain UMIP specification, so that relayers that comply with the event would be reimbursed. This mitigation would need a mechanism to handle relayers that incorrectly fill relays with excessively large relayer fees, which would prevent the recipient from receiving their full payment. Alternatively, consider removing support for EIP-1271 validation and relying entirely on ECDSA signatures.


**Update**: *Fixed in [pull request #79](https://github.com/across-protocol/contracts-v2/pull/79) as of commit [`2a41086f0d61caf0be8c2f3d1cdaf96e4f67f718`](https://github.com/across-protocol/contracts-v2/pull/79/commits/2a41086f0d61caf0be8c2f3d1cdaf96e4f67f718).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | UMA Across V2 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/uma-across-v2-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


---
# Core Classification
protocol: P2P.org
chain: everychain
category: uncategorized
vulnerability_type: signature_malleability

# Attack Vector Details
attack_type: signature_malleability
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45348
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/P2P.org/Lending%20Proxy/README.md#4-signature-replay-allows-unauthorized-use-of-permits
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
  - signature_malleability
  - replay_attack

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Signature Replay Allows Unauthorized Use of Permits

### Overview


The `isValidSignature` function in the `P2pLendingProxy` contract has a bug where signatures are not being verified against the contract's address or any unique identifier. This means that an attacker can use the same signature multiple times on different `P2pLendingProxy` instances owned by the same user, potentially allowing for unauthorized transfers. This issue is considered medium severity because it could lead to unauthorized operations. To fix this issue, it is recommended to include the contract address or a unique identifier in the signed data, which will prevent replay attacks across different addresses. 

### Original Finding Content

##### Description
This issue has been identified within the signature verification flow of the `isValidSignature` function in the `P2pLendingProxy` contract. 

Currently, signatures are verified against `s_client`, but the contract’s address or any unique identifier is not included in the signed data. An attacker can replay the same signature across multiple `P2pLendingProxy` instances owned by the same user. For example, the replayed signature could authorize unwanted or additional transfers. 

In the context of `Permit2`, such reuse could allow multiple proxies to be drained using a single signature. Moreover, any message a client signs for themselves may inadvertently be valid for their proxies, and vice versa. 

This issue is classified as **medium** severity because, while the proxy contracts are not designed to store tokens on balance, replay attacks still pose a risk of unauthorized operations.

##### Recommendation
We recommend incorporating the contract address (or a unique contract-specific field) into the signed data, such as via an EIP-712 domain separator. By doing so, signatures become valid exclusively for the intended `P2pLendingProxy` contract, mitigating replay across different addresses.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | P2P.org |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/P2P.org/Lending%20Proxy/README.md#4-signature-replay-allows-unauthorized-use-of-permits
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Signature Malleability, Replay Attack`


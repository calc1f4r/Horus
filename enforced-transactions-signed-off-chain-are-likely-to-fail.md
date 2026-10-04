---
# Core Classification
protocol: Scroll Phase 1 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32936
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/scroll-phase-1-audit
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

Enforced Transactions Signed Off-Chain Are Likely to Fail

### Overview


The EnforcedTxGateway contract has a bug that causes transactions to fail if there is a delay between when a user signs the transaction and when it is submitted. This is because the queue index, which is used to verify the signature, can change if other transactions are submitted in the meantime. To fix this, the queue index should be repurposed as a nonce and an expiration timestamp and chain id should be added to the message to prevent replay attacks. This bug has been resolved in a recent update to the contract.

### Original Finding Content

The `EnforcedTxGateway` contract allows users to sign a transaction hash that authorizes an L1 to L2 transaction. During the verification of the signature, the [signed hash is computed](https://github.com/scroll-tech/scroll/blob/3bc8a3f5c6ac816ddffadca41024331dcf4d3064/contracts/src/L1/gateways/EnforcedTxGateway.sol#L86) given the `sendTransaction` function parameters, except for the `_queueIndex` value, which is fetched as the supposedly following index from the message queue.


Timing this queue index during signing becomes challenging considering the following scenario:


1. User A signs the transaction off-chain for index `i`.
2. User B queues a transaction unrelated to A, thereby incrementing the queue index to `i+1`.
3. User C tries to submit user A's transaction, which reverts due to the mismatching queue indices.


Depending on the activity of the messenger contract and the delay between users A and C, it is likely that this call reverts.


Consider repurposing the queue index to a `nonce` that is signed as part of the transaction hash by taking it as an additional function parameter. The replayability must therefore be prevented by keeping track of used transaction hashes in a mapping. Also, consider adding an expiration timestamp and chain id to the message such that signed messages are not indefinitely valid and are chain dependent. Otherwise, a signature can be reused for a rollup that follows the same message format and is signed by the same user. It's important to note that the transaction hash should not be constructed over the signature when an OpenZeppelin library version lower than 4.7.3 is used, due to a [signature malleability issue](https://github.com/OpenZeppelin/openzeppelin-contracts/security/advisories/GHSA-4h98-2769-gh6h).


***Update:** Resolved in [pull request #620](https://github.com/scroll-tech/scroll/pull/620) at commit [af8a4c9](https://github.com/scroll-tech/scroll/pull/620/commits/af8a4c9ac808bf70e27c4d3ef4ede18ede565075). The data is now signed using the EIP-712 standard. Expiration and replayability were addressed by adding a deadline and nonce.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Scroll Phase 1 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/scroll-phase-1-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


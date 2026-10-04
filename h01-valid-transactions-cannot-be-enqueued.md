---
# Core Classification
protocol: Optimism Smart Contracts Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10721
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/optimism-smart-contracts-audit/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[H01] Valid transactions cannot be enqueued

### Overview


A bug was reported in the Ethereum Optimism repository, where transactions coming from the Sequencer were not limited in size to the `MAX_ROLLUP_TX_SIZE` (10000 bytes). This meant that it was possible for transactions to be larger than this size, making it impossible to enqueue them in L1. To avoid censorship by the Sequencer, it was proposed to enforce an upper bound of `MAX_ROLLUP_TX_SIZE` in the size of transactions that go through the Sequencer. The bug was fixed in pull request #361 of the archived `ethereum-optimism` repository.

### Original Finding Content

Transactions to be appended to the Canonical Transaction Chain (CTC) can come from two sources: the L1 queue and the Sequencer. When transactions are enqueued in the `OVM_CanonicalTransactionChain` contract via its public [`enqueue` function](https://github.com/ethereum-optimism/contracts/blob/18e128343731b9bde23812ce932e24d81440b6b7/contracts/optimistic-ethereum/OVM/chain/OVM_CanonicalTransactionChain.sol#L256), they are [explicitly limited](https://github.com/ethereum-optimism/contracts/blob/18e128343731b9bde23812ce932e24d81440b6b7/contracts/optimistic-ethereum/OVM/chain/OVM_CanonicalTransactionChain.sol#L264-L267) in size to [`MAX_ROLLUP_TX_SIZE`](https://github.com/ethereum-optimism/contracts/blob/18e128343731b9bde23812ce932e24d81440b6b7/contracts/optimistic-ethereum/OVM/chain/OVM_CanonicalTransactionChain.sol#L41) (10000 bytes). However, transactions coming from the Sequencer do not follow the same restriction – they can actually be larger than `MAX_ROLLUP_TX_SIZE`. As a result, it might be impossible to enqueue transactions in L1 that could be effectively included via the Sequencer.


To avoid censorship by the Sequencer, it should be possible for any valid sequenced transaction to instead be enqueued in L1. Therefore, consider enforcing an upper bound of `MAX_ROLLUP_TX_SIZE` in the size of transactions that go through the Sequencer.


***Update**: Fixed in [pull request #361](https://github.com/ethereum-optimism/contracts/pull/361/commits/8da1c24bb08b8a10b56747add78c414e58ebadf4) of the archived `ethereum-optimism` repository.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Optimism Smart Contracts Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/optimism-smart-contracts-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


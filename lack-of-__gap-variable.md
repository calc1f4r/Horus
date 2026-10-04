---
# Core Classification
protocol: zkSync Fee Model and Token Bridge Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10322
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/zksync-fee-model-and-token-bridge-audit/
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
  - cdp
  - services
  - cross_chain
  - indexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Lack of __gap Variable

### Overview


This bug report is about the [`L1ERC20Bridge`](https://github.com/matter-labs/zksync-2-contracts/blob/9f3c6944e6320166edd96ef6586a9dd4548a27f2/ethereum/contracts/bridge/L1ERC20Bridge.sol) and [`L2StandardERC20`](https://github.com/matter-labs/zksync-2-contracts/blob/9f3c6944e6320166edd96ef6586a9dd4548a27f2/zksync/contracts/bridge/L2StandardERC20.sol) contracts, which are intended to be used as logic contracts with a proxy. The bug is that these contracts do not have a `__gap` variable. This could cause a storage collision if a subsequent version of the contract were to inherit one of these contracts and add storage variables, as the storage slots would not sum up to a fixed amount.

The suggestion is to add a `__gap` variable to these contracts, such that the storage slots sum up to a fixed amount. This would help protect against storage layout changes in the base contract. However, the Matter Labs team has acknowledged the issue but stated that they do not believe the issue has a significant security risk, as the specified contracts are not expected to be inherited.

### Original Finding Content

The [`L1ERC20Bridge`](https://github.com/matter-labs/zksync-2-contracts/blob/9f3c6944e6320166edd96ef6586a9dd4548a27f2/ethereum/contracts/bridge/L1ERC20Bridge.sol) and [`L2StandardERC20`](https://github.com/matter-labs/zksync-2-contracts/blob/9f3c6944e6320166edd96ef6586a9dd4548a27f2/zksync/contracts/bridge/L2StandardERC20.sol) contract are intended to be used as logic contracts with a proxy, but do not have a `__gap` variable. This would become problematic if a subsequent version was to inherit one of these contracts. If the derived version were to have storage variables itself and additional storage variables were subsequently added to the inherited contract, a storage collision would occur.


Consider appending a [`__gap` variable](https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps) as the last storage variable to these upgradeable contracts, such that the storage slots sum up to a fixed amount (e.g. 50). This will proof any future storage layout changes to the base contract. Note that the `__gap` variable space will need to be adjusted accordingly as subsequent versions include more storage variables, in order to maintain the fixed amount of slots (e.g. 50).


***Update:** Acknowledged, not resolved. The Matter Labs team stated:*



> *While we appreciate your insights and suggestions, we do not believe the issue has a significant security risk. Specified contracts are not expected to be inherited, since they are complete logical contracts.*
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | zkSync Fee Model and Token Bridge Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/zksync-fee-model-and-token-bridge-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


---
# Core Classification
protocol: MCDEX Mai Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11405
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/mcdex-mai-protocol-audit/
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
  - services
  - derivatives
  - rwa
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M03] Re-entrancy possibilities

### Overview


This bug report is about the potential security issues caused by not following the Check-Effects-Interactions Pattern in Solidity. This pattern is recommended by Solidity to avoid reentrancy, which could lead to potential security issues. Examples of interactions preceding effects were found in the `deposit`, `_withdraw`, `depositToInsuranceFund`, `depositEtherToInsuranceFund`, and `withdrawFromInsuranceFund` functions of the `Collateral` and `Perpetual` contracts. Even when a correctly implemented ERC20 contract is used for collateral, incoming and outgoing transfers could execute arbitrary code if the contract is also ERC777 compliant, which could confuse external clients about the state of the system.

To fix this bug, the ReentrancyGuard contract was used to protect the functions mentioned above. This contract prevents reentrancy by using a mutex lock and ensuring that any function calls are completed before the lock is released. This ensures that the order and contents of emitted events is not affected and external clients can accurately determine the state of the system.

### Original Finding Content

[Solidity recommends the usage of the Check-Effects-Interaction Pattern](https://solidity.readthedocs.io/en/latest/security-considerations.html#use-the-checks-effects-interactions-pattern) to avoid potential security issues, such as reentrancy. However, there are several examples of interactions preceding effects:


* In the `deposit` function of the `Collateral` contract, [collateral is retrieved](https://github.com/mcdexio/mai-protocol-v2/blob/4b198083ec4ae2d6851e101fc44ea333eaa3cd92/contracts/perpetual/Collateral.sol#L51) before [the user balance is updated and an event is emitted](https://github.com/mcdexio/mai-protocol-v2/blob/4b198083ec4ae2d6851e101fc44ea333eaa3cd92/contracts/perpetual/Collateral.sol#L54-L56).
* In the `_withdraw` function of the `Collateral` contract, [collateral is sent](https://github.com/mcdexio/mai-protocol-v2/blob/4b198083ec4ae2d6851e101fc44ea333eaa3cd92/contracts/perpetual/Collateral.sol#L81-L85) before the [event is emitted](https://github.com/mcdexio/mai-protocol-v2/blob/4b198083ec4ae2d6851e101fc44ea333eaa3cd92/contracts/perpetual/Collateral.sol#L86)
* The same pattern occurs in the [`depositToInsuranceFund`](https://github.com/mcdexio/mai-protocol-v2/blob/4b198083ec4ae2d6851e101fc44ea333eaa3cd92/contracts/perpetual/Perpetual.sol#L180), [`depositEtherToInsuranceFund`](https://github.com/mcdexio/mai-protocol-v2/blob/4b198083ec4ae2d6851e101fc44ea333eaa3cd92/contracts/perpetual/Perpetual.sol#L192) and [`withdrawFromInsuranceFund`](https://github.com/mcdexio/mai-protocol-v2/blob/4b198083ec4ae2d6851e101fc44ea333eaa3cd92/contracts/perpetual/Perpetual.sol#L204) functions of the `Perpetual` contract.


It should be noted that even when a correctly implemented ERC20 contract is used for collateral, incoming and outgoing transfers could execute arbitrary code if the contract is also ERC777 compliant. These re-entrancy opportunities are unlikely to corrupt the internal state of the system, but they would effect the order and contents of emitted events, which could confuse external clients about the state of the system. Consider always following the “Check-Effects-Interactions” pattern.


**Update:** *Fixed. The [`ReentrancyGuard`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/utils/ReentrancyGuard.sol) contract is now used to protect those functions.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | MCDEX Mai Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/mcdex-mai-protocol-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


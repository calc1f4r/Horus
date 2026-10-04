---
# Core Classification
protocol: Primitive Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11354
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/primitive-audit/
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
  - synthetics
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M07] Convoluted implementation of exercise and flash loan features

### Overview


This bug report is regarding the 'exercise' function of the 'Option' contract in the Primitive Protocol. The function is intended to allow option-token holders to exchange strike assets for underlying assets at a certain strike price. However, depending on the arguments passed to the function, it can change its behavior to allow flash loans of underlying tokens. Merging these two functionalities under a single function makes the code more difficult to read and understand, and increases the complexity of the business logic, making it more error-prone and harder to test. The suggested solution is to split the exercise and flash loan features into two separate, independent, functions. However, the Primitive team has decided not to apply the suggested changes, arguing that the proposed separation of functionalities would lead to code duplication.

### Original Finding Content

The [`exercise` function](https://github.com/primitivefinance/primitive-protocol/blob/78a8e64b7618e9199203ab84042876c580ae1e90/packages/primitive-contracts/contracts/option/primitives/Option.sol#L179) of the `Option` contract is intended to allow option-token holders to exercise the right of exchanging strike assets for underlying assets at a certain strike price.


Nevertheless, [depending on the arguments passed to the function](https://github.com/primitivefinance/primitive-protocol/blob/78a8e64b7618e9199203ab84042876c580ae1e90/packages/primitive-contracts/contracts/option/primitives/Option.sol#L204), the `exercise` function can change its behavior to allow flash loans of underlying tokens.


Exercising an option and taking out flash loans of underlying tokens are two different use cases of the Primitive protocol. Merging these two functionalities under a single function renders the code more difficult to read and understand by users, developers and auditors alike. Additionally, the added complexity in the business logic to handle both features makes the implementation more error-prone and harder to test.


Consider splitting the exercise and flash loan features into two separate, independent, functions.


**Update:** *Acknowledged in [PR #37](https://github.com/primitivefinance/primitive-protocol/pull/37), and will not fix. The Primitive team has decided not to apply the suggested changes, arguing that the proposed separation of functionalities would lead to code duplication.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Primitive Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/primitive-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


---
# Core Classification
protocol: EIP-4337 – Ethereum Account Abstraction Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10619
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/eth-foundation-account-abstraction-audit/
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
  - services

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[H02] Duplicate validation gas accounting [core]

### Overview


This bug report is about an issue in the `handleOp` function of the `EntryPoint` contract. The issue is that the function tracks and records both the pre-operation gas and the gas consumed before the final `postOp` call, but both values use the same `preGas` value. This means that the gas used during payment validation is accounted for twice, and the wallet or paymaster will be overcharged for the operation. The issue has been fixed in Pull Request #61, where the `handleOp` function has been removed.

### Original Finding Content

The [`handleOp` function](https://github.com/eth-infinitism/account-abstraction/blob/8832d6e04b9f4f706f612261c6e46b3f1745d61a/contracts/EntryPoint.sol#L52) of the `EntryPoint` contract tracks and records both the [pre-operation gas](https://github.com/eth-infinitism/account-abstraction/blob/8832d6e04b9f4f706f612261c6e46b3f1745d61a/contracts/EntryPoint.sol#L64) and the [gas consumed before the final `postOp` call](https://github.com/eth-infinitism/account-abstraction/blob/8832d6e04b9f4f706f612261c6e46b3f1745d61a/contracts/EntryPoint.sol#L72). However, in contrast to the [equivalent](https://github.com/eth-infinitism/account-abstraction/blob/8832d6e04b9f4f706f612261c6e46b3f1745d61a/contracts/EntryPoint.sol#L112) [calculations](https://github.com/eth-infinitism/account-abstraction/blob/8832d6e04b9f4f706f612261c6e46b3f1745d61a/contracts/EntryPoint.sol#L129) in `handleOps`, both values use [the same `preGas` value](https://github.com/eth-infinitism/account-abstraction/blob/8832d6e04b9f4f706f612261c6e46b3f1745d61a/contracts/EntryPoint.sol#L54). This means that the gas used during payment validation is accounted for twice, and the wallet or paymaster will be overcharged for the operation.


***Update**: Fixed in pull request [#61](https://github.com/eth-infinitism/account-abstraction/pull/61/files). The `handleOp` function has been removed.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | EIP-4337 – Ethereum Account Abstraction Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/eth-foundation-account-abstraction-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


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
solodit_id: 10639
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/eth-foundation-account-abstraction-audit/
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

[L13] Missing validations [core]

### Overview

See description below for full details.

### Original Finding Content

* The [`compensate`](https://github.com/eth-infinitism/account-abstraction/blob/8832d6e04b9f4f706f612261c6e46b3f1745d61a/contracts/EntryPoint.sol#L80) function in `EntryPoint` takes a `beneficiary` address as input and sends the amount specified to that address. This happens as the final step of a `handleOps` or `handleOp` function call. The code does not check that `beneficiary` is not 0, which could lead to accidental loss of funds. Consider adding a check to verify that `beneficiary` is a non-zero value.
* In the [`EntryPoint` constructor](https://github.com/eth-infinitism/account-abstraction/blob/8832d6e04b9f4f706f612261c6e46b3f1745d61a/contracts/EntryPoint.sol#L42-L45), there are no checks to ensure the immutable contract variables are set to non-zero values. If `_create2factory`, `_paymasterStake`, or `_unstakeDelaySec` were accidentally set to 0, the contract would need to be redeployed because there is no mechanism to update these values. Consider adding a non-zero check for each of the constructor parameters.


***Update**: Fixed in pull requests [#59](https://github.com/eth-infinitism/account-abstraction/pull/59/files) and [#63](https://github.com/eth-infinitism/account-abstraction/pull/63/files). Checks that reject zero values have been added for `beneficiary`, `_create2factory`, `_paymasterStake`, and `unstakeDelaySec`.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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


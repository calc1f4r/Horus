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
solodit_id: 10622
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

[H05] Incorrect gas price [core]

### Overview


The Ethereum Foundation identified an issue during an audit of the account abstraction software. The issue was related to the gas price to charge the user for an operation. The calculation was set to take the minimum of the transaction gas price and the user-specified gas price. This was not ideal, as the user should always pay their specified price to provide an incentive for the bundler to process the user operation. To fix this issue, the `tx.gasprice` value was removed from the gas price calculation in pull request [#55](https://github.com/eth-infinitism/account-abstraction/pull/55/files). This issue has now been resolved.

### Original Finding Content

**Client reported:** *The Ethereum Foundation identified this issue during the audit.*


The gas price to charge the user (potentially through the paymaster) for the operation is [calculated](https://github.com/eth-infinitism/account-abstraction/blob/8832d6e04b9f4f706f612261c6e46b3f1745d61a/contracts/UserOperation.sol#L34-L38) as the minimum of the transaction gas price and the user-specified gas price (after accounting for any `basefee`). However, the user should always pay their specified price so the bundler can receive the excess, which provides the incentive to process the user operation in the first place. Consider allowing the user’s gas price to exceed the transaction gas price.


***Update**: Fixed in pull request [#55](https://github.com/eth-infinitism/account-abstraction/pull/55/files). The `tx.gasprice` value has been removed from the gas price calculation.*

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


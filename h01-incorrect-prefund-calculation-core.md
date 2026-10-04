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
solodit_id: 10618
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

[H01] Incorrect prefund calculation [core]

### Overview


A bug was discovered in the account-abstraction project where the maximum amount of gas needed to finance a user operation was calculated incorrectly. This could lead to two problems: users without enough funds could have their operation overcharged, and paymasters with insufficient stakes could still pass validation and be unable to fund the operation. The bug was fixed in pull request #51, where the calculation was updated to match the execution behavior.

### Original Finding Content

In order to ensure a user operation can be financed, the maximum amount of gas it could consume is calculated. This depends on the individual gas limits specified in the transaction. Since the paymaster may use `verificationGas` to limit up to three function calls, operations that have a paymaster should multiply `verificationGas` by 3 when calculating the maximum gas. However, the [calculation is inverted](https://github.com/eth-infinitism/account-abstraction/blob/8832d6e04b9f4f706f612261c6e46b3f1745d61a/contracts/UserOperation.sol#L46). This means that valid user operations could fail in two ways:


* Operations that do not rely on paymasters will be initially overcharged, and the wallet may have insufficient funds to proceed. It should be noted that wallets with sufficient funds will still have any unused gas (including the overcharge) refunded after the operation is executed.
* Paymasters that are insufficently staked may nevertheless pass validation, which introduces the possibility that they will be unable to fund the operation. In practice, the excess funds will probably simply be deducted from their stake. Even so, this allows users to craft operations that would unexpectedly cause the paymaster to become unstaked.


Consider updating the maximum gas calculation to match the execution behavior.


***Update**: Fixed in pull request [#51](https://github.com/eth-infinitism/account-abstraction/pull/51/files).*

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


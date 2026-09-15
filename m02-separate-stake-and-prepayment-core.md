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
solodit_id: 10624
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/eth-foundation-account-abstraction-audit/
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
  - services

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M02] Separate stake and prepayment [core]

### Overview


The StakeManager contract holds ETH on behalf of users for two different reasons: as an anti-sybil mechanism to lock a deposit and to preemptively transfer funds to pay the gas costs associated with user operations. However, the contract treats these funds equivalently, making the boundary difficult to identify, enforce and reason about. This can lead to paymasters not being able to safely lock capital in the StakeManager without risking it being used to pay for user transactions. Additionally, this unclear boundary may have caused the Paymasters can spend locked state issue.

To resolve this issue, developers proposed separating the handling of transaction prepayments and paymaster stake to better encapsulate the two concepts. This issue has now been fixed in pull request #76.

### Original Finding Content

The [`StakeManager` contract](https://github.com/eth-infinitism/account-abstraction/blob/8832d6e04b9f4f706f612261c6e46b3f1745d61a/contracts/StakeManager.sol) holds ETH on behalf of users for two different reasons:


* Paymasters lock a deposit as an anti-sybil mechanism
* Wallets and paymasters preemptively transfer funds to pay the gas costs associated with user operations


However, the `StakeManager` contract treats these funds equivalently, making the boundary harder to identify, enforce and reason about. For example, paymasters are unable to decrease the amount of funds available to users without first unstaking and waiting for the withdrawal period. Moreover, miners may choose different thresholds for the minimum paymaster stake, which means they can unilaterally partition a paymaster’s deposit between the two amounts on a per-transaction basis. Consequently, unless they explicitly account for this in their validation function, paymasters cannot safely lock capital in the `StakeManager` without risking that it will be used to pay for user transactions.


Additionally, we believe the [Paymasters can spend locked state](#paymasters-can-spend-locked-stake) issue is a consequence of this unclear boundary.


Consider separating the handling of transaction prepayments and paymaster stake to better encapsulate the two concepts.


***Update**: Fixed in pull request [#76](https://github.com/eth-infinitism/account-abstraction/pull/76).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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


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
solodit_id: 10620
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

[H03] Paymasters can spend locked stake [core]

### Overview


A bug was discovered in the StakeManager contract of the account-abstraction repository on Github. Wallets were able to spend funds that were supposed to be locked as stake, which bypassed the reputation system and allowed them to consume their locked funds after being throttled. This bug was fixed in pull request #53, which added a check to the _validateWalletPrepayment function. This check now confirms that the sender of the user operation does not have a staked deposit with the EntryPoint contract, and rejects the user operation if the wallet is staked. This requirement is more conservative than necessary, but it correctly mitigates the issue and does not prevent valid use cases.

### Original Finding Content

Wallets pay for their operations using the funds [deposited with the `StakeManager`](https://github.com/eth-infinitism/account-abstraction/blob/8832d6e04b9f4f706f612261c6e46b3f1745d61a/contracts/EntryPoint.sol#L255), whether or not those funds are locked. This is usually acceptable because wallets are not required to lock their funds. However, if a paymaster contract is also a wallet, it will be able to spend funds that are supposed to be locked as stake. This means that it can bypass the reputation system by consuming its locked funds after being throttled. Consider ensuring that wallets cannot spend locked funds.


***Update**: Fixed in pull request [#53](https://github.com/eth-infinitism/account-abstraction/pull/53/files). If a paymaster has not been specified for a given user operation, the `_validateWalletPrepayment` function now checks if the `sender` has a staked deposit with the `EntryPoint` contract, and rejects the user operation if the wallet is staked. The particular requirement is more conservative than strictly necessary, but it correctly mitigates the issue and does not prevent valid use cases.*

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


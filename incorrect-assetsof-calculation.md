---
# Core Classification
protocol: Pods Finance Ethereum Volatility Vault Audit #2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10396
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/pods-finance-ethereum-volatility-vault-audit-2/
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

Incorrect assetsOf calculation

### Overview


A bug was discovered in the `assetsOf` function within `BaseVault`. This function is used to calculate the combination of a user’s idle and withdrawable assets, and should depict the number of underlying assets a user could potentially receive from the vault at any given time. During testing, it was found that the sum of three items - the number of assets the user’s entire share balance would currently convert to, the number of idle assets a user has in the queue, and the number of assets the user’s entire share balance would convert to if the conversion rate factored in all idle assets - was at least double the amount of assets a user could actually receive from the protocol.

To resolve this bug, the `assetsOf` calculation was changed to match the behavior if a user were to perform both a `redeem` of their total balance of shares and a `refund` of all of their idle assets in the same transaction. This bug has since been resolved, with the commit `602122efed209eed23f14b5eb906be1fab01cec5` being the last one added to the pull request #98.

### Original Finding Content

The [`assetsOf`](https://github.com/pods-finance/yield-contracts/blob/c4b401ce674c24798de5f9d02c82e466ee0a2600/contracts/vaults/BaseVault.sol#L251) function within `BaseVault` is used to calculate the combination of a user’s idle and withdrawable assets. This should depict the number of underlying assets a user could potentially receive from the vault at any given time. The formula it uses, however, incorrectly sums three separate items:


* The number of assets the user’s entire share balance would currently convert to
* The number of idle assets a user has in the queue
* The number of assets the user’s entire share balance would convert to if the conversion rate factored in all idle assets


During testing, it was observed that the sum of these three items were at least double the amount of assets a user could actually receive from the protocol.


Consider changing the `assetsOf` calculation to match the behavior if a user were to perform both a [`redeem`](https://github.com/pods-finance/yield-contracts/blob/c4b401ce674c24798de5f9d02c82e466ee0a2600/contracts/vaults/BaseVault.sol#L168) of their total balance of shares and a [`refund`](https://github.com/pods-finance/yield-contracts/blob/c4b401ce674c24798de5f9d02c82e466ee0a2600/contracts/vaults/BaseVault.sol#L326) of all of their idle assets in the same transaction.


**Update:** *Resolved in [PR#98](https://github.com/pods-finance/yield-contracts/pull/98), with commit `602122efed209eed23f14b5eb906be1fab01cec5` being the last one added.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Pods Finance Ethereum Volatility Vault Audit #2 |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/pods-finance-ethereum-volatility-vault-audit-2/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


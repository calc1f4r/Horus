---
# Core Classification
protocol: Pods Finance Ethereum Volatility Vault Audit #1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10413
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/pods-finance-ethereum-volatility-vault-audit-1/
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
  - dexes
  - yield
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

The vault can be drained one share at a time

### Overview


This bug report is about a vulnerability in the withdrawal process of the Pods Finance Yield Contracts. During the withdrawal process, users can specify the amount of assets to withdraw, which is then rounded down to shares. However, if the amount of assets specified by the user is less than the minimum amount that can be converted to a unit share, the shares argument is zero in the internal withdraw function but the assets argument is not. This allows attackers to drain the entire vault by repeatedly withdrawing non-zero amounts of asset tokens without burning any shares. Since the vault is expected to become more valuable over time, this could lead to a profitable attack when one share is worth more than the cost. To fix this vulnerability, the developers suggested rounding up the shares for a given amount of assets during withdrawal. This issue has been fixed in pull request #46 with commit 5ac5e3c being the last one added.

### Original Finding Content

During the withdrawal process, users can specify the [amount of assets](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/BaseVault.sol#L163-L167) to withdraw, which is then [rounded down to shares](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/BaseVault.sol#L169).


When the asset amount specified by the user is less than the minimum amount that can be converted to a unit share, the `shares` argument is zero in the [internal withdraw function](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/BaseVault.sol#L170) but the `assets` argument is not. Hence, with zero shares, [all internal calls can succeed](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/STETHVault.sol#L135-L143) and a non-zero amount of asset token will be [transferred out](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/STETHVault.sol#L151) to the receiver without burning any shares. This process can be repeated many times to drain the entire vault. The attack can also be executed with any asset amount by burning a rounded-down amount of shares and extracting the excess assets.


Since the vault is expected to become more valuable over time due to its yield strategy, this could lead to a profitable attack when one share is worth more than the cost.


Consider rounding up the shares for a given amount of assets during withdrawal.


**Update:** *Fixed in [PR#46](https://github.com/pods-finance/yield-contracts/pull/46), with commit `5ac5e3c` being the last one added.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Pods Finance Ethereum Volatility Vault Audit #1 |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/pods-finance-ethereum-volatility-vault-audit-1/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


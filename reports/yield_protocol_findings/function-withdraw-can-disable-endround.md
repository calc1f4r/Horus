---
# Core Classification
protocol: Pods Finance Ethereum Volatility Vault Audit #1
chain: everychain
category: uncategorized
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10414
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
  - wrong_math
  - overflow/underflow

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

Function withdraw can disable endRound

### Overview


This bug report is about the controller not being able to call the `endRound()` function after a round starts to remove a portion of the accrued interest from the vault to the `investor` account for the execution of investment strategies. The problem is due to the `totalAssets()` being compared to the `lastRoundAssets` to compute the accrued interest, and when a user withdraws assets before the `endRound`, the `lastRoundAssets` is updated in the `_beforeWithdraw()` hook. This can result in the `lastRoundAssets` being more than the `totalAssets()` when a user calls the `withdraw` function, leading to a revert due to underflow.

To fix this, the developers proposed keeping track of the withdrawn asset directly and making sure the key system functionality is not impeded by users' actions. This was fixed in PR#73, with commit `b258ca9` being the last one added.

### Original Finding Content

The controller should be able to call the [`endRound()`](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/BaseVault.sol#L320) function any time after a round starts to remove a portion of the accrued interest from the vault to the `investor` account for the execution of investment strategies. In the [`_afterRoundEnd`](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/STETHVault.sol#L77) hook, the `totalAssets()` is compared to the `lastRoundAssets` to compute the accrued interest. When a user withdraws assets before the `endRound`, the `lastRoundAssets` is updated in the [`_beforeWithdraw()`](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/STETHVault.sol#L101) hook, where the withdrawn shares are rounded down to the corresponding asset value, which is subsequently subtracted from the `lastRoundAssets`.


This may cause the `lastRoundAssets` to be more than the `totalAssets()` when a user calls the [`withdraw`](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/BaseVault.sol#L163-L167) function. This can result in a [revert due to underflow](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/STETHVault.sol#L77). In such a case, the controller cannot end a round and must wait for the accrued interest to accumulate enough value.


Consider keeping track of the withdrawn asset directly. Also, consider making sure the key system functionality is not impeded by users’ actions.


**Update:** *Fixed in [PR#73](https://github.com/pods-finance/yield-contracts/pull/73), with commit `b258ca9` being the last one added.*

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

`Wrong Math, Overflow/Underflow`


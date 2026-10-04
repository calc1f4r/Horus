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
solodit_id: 10421
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/pods-finance-ethereum-volatility-vault-audit-1/
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

Maximum mintable and depositable amounts returned are incorrect

### Overview


This bug report is about the [`availableCap`](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/mixins/Capped.sol#L20) variable in the [`EIP4626`](https://eips.ethereum.org/EIPS/eip-4626) standard. This variable limits the amount of assets that can be deposited and converted into vault shares for the depositor. The [`maxMint`](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/BaseVault.sol#L236) and [`maxDeposit`](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/BaseVault.sol#L229) functions do not take into account the `availableCap` variable and instead return the maximum `uint256` value when called.

The bug report suggests changing the `maxMint` and `maxDeposit` functions to return a value that accounts for the `availableCap`, so that they conform to the [`EIP4626`](https://eips.ethereum.org/EIPS/eip-4626) standard. The bug has been fixed in pull request [#42](https://github.com/pods-finance/yield-contracts/pull/42) with the commit `3159de5` being the last one added.

### Original Finding Content

The amount of vault shares available for minting is limited by the [`availableCap`](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/mixins/Capped.sol#L20). Similarly, the `availableCap` also limits the amount of assets that may be deposited and then later converted into vault shares for the depositor. The [`maxMint`](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/BaseVault.sol#L236) and [`maxDeposit`](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/BaseVault.sol#L229) functions do not account for the `availableCap` and instead return the max `uint256` value when called. In order to conform to the [`EIP4626`](https://eips.ethereum.org/EIPS/eip-4626) standard, these functions must return the real amount that can be minted or deposited.


Consider changing the `maxMint` and `maxDeposit` functions to return a value that accounts for the `availableCap`.


**Update:** *Fixed in [PR#42](https://github.com/pods-finance/yield-contracts/pull/42), with commit `3159de5` being the last one added.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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


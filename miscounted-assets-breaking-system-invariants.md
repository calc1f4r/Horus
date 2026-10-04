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
solodit_id: 10412
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

Miscounted assets breaking system invariants

### Overview


A bug has been identified in the code of the yield-contracts project, which can lead to incorrect calculations for the amount of shares minted to depositors in the queue. This bug occurs when the `processedDeposits` variable is reset to 0 at the beginning of each round, and the amount of assets that have been processed are removed from `totalIdleAssets`. This could lead to users not processed in the first round receiving fewer assets than they deposited when they redeem their shares, which breaks a system invariant that 100% withdrawal in stETH should always be equal to or higher than the initial deposit amount.

The bug has been fixed in Pull Request #54, with commit `3ad9b76` being the last one added. This correction ensures that the processed amount is accounted for accurately, and the number of splits will not modify the result when processing the deposits.

### Original Finding Content

When processing queued deposits, the amount of assets that have been processed are [accounted for](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/BaseVault.sol#L376) in the `processedDeposits` variable and [used to calculate the amount of shares](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/BaseVault.sol#L392) to be minted. This variable is [reset to 0](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/BaseVault.sol#L312) at the beginning of each round.


However, each time the `processQueuedDeposits` function concludes, the processed amount will be [removed](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/BaseVault.sol#L381) from `totalIdleAssets`, hence increasing the [`totalAssets`](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/STETHVault.sol#L108). When the queue is processed the next time, the [`totalAssets`](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/BaseVault.sol#L374) value already contains the amount of assets processed during the round. By [adding the `processedDeposits` to the `totalAssets` again](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/BaseVault.sol#L376), the previously processed amount is double counted, which leads to an incorrect calculation for the amount of shares minted to the next depositor in the queue.


This penalizes depositors by minting fewer shares if they are not included in the first call of the `processQueuedDeposits` function. This issue is particularly severe if each deposit is processed individually. Hence it breaks the system invariant that the number of splits should not modify the result when processing the deposits.


Additionally, this means users not processed in the first round may receive fewer assets than they deposited when they redeem their shares. This breaks another important system invariant that 100% withdrawal in stETH should always be equal to or higher than the initial deposit amount.


Consider correcting the total asset calculation to ensure the processed amount is accounted for accurately.


**Update:** *Fixed in [PR#54](https://github.com/pods-finance/yield-contracts/pull/54), with commit `3ad9b76` being the last one added.*

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


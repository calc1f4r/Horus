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
solodit_id: 10422
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

Refund does not restore the cap

### Overview


This bug report concerns the Pods Finance yield contracts, which are used to manage deposits into a vault. When a user joins the deposit queue, the corresponding shares are deducted from the spending cap immediately. However, when the user decides to use the refund function to leave the queue before the round ends, the spending cap is not restored. This means that a malicious user with a large amount of assets could repeatedly deposit and refund to reach the cap limit, thus preventing other eligible users from joining the queue. 

The spending cap cannot be manually restored, but the owner can reset the cap to a higher value to unlock the deposit. To fix this bug, the available cap must be accounted for during refunds from the queue. The bug has since been fixed in commit 4a2e475fb1242cf3306291afff53be55b8c214d0.

### Original Finding Content

When a user deposits into the vault by joining the deposit queue, the corresponding shares, yet to be minted, are [deducted from the spending cap](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/BaseVault.sol#L412) immediately. The spending cap is [restored](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/BaseVault.sol#L436) only at withdrawal when the shares are burned.


If one user decides to use the [refund](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/BaseVault.sol#L333) function to leave the queue before the round ends, the spending cap will not be restored. When the [cap is not zero](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/mixins/Capped.sol#L22), a malicious user with a sufficiently large amount of assets could repeatedly deposit and `refund` to reach the cap limit and stop other eligible users from joining the queue.


Note that the [`spendCap`](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/mixins/Capped.sol#L9) variable cannot be manually restored, but the owner can [reset](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/configuration/ConfigurationManager.sol#L55) the cap to a higher value to unlock the deposit.


Consider accounting for the available cap during refunds from the queue.


**Update:** *Fixed in commit [`4a2e475`](https://github.com/pods-finance/yield-contracts/pull/43/commits/4a2e475fb1242cf3306291afff53be55b8c214d0).*

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


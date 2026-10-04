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
solodit_id: 10432
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/pods-finance-ethereum-volatility-vault-audit-1/
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

Migration risks

### Overview

See description below for full details.

### Original Finding Content

The system allows users to migrate their shares to a new vault with the same underlying asset. There are a few risks regarding the current migration mechanism design.


* **Unclear migration path**: Currently, two migration mechanisms exist. A user can either call the [`migrate`](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/BaseVault.sol#L352) function in the old vault or through the exclusive [`Migration`](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/proxy/Migration.sol) contract. There is no clarity on which route is preferred as both essentially perform the same functionality. Consider removing duplicate actions that can lead to user confusion.
* **Incomplete migration**: In both migration routes, users first [redeem their shares from the old vault and then re-deposit the assets](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/proxy/Migration.sol#L21-L28) into the new vault. If the queueing system works the same way in the new vault, this only lets the user join the deposit queue. Hence the migration is not complete until the queued deposits are processed with the shares minted. Consider documenting this to make it clear to users who migrate.
* **Migration re-usability:** The `Migration` contract sets both the old vault and the new vault addresses as [immutable variables in the constructor](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/proxy/Migration.sol#L12-L19). This limits its use case to one single migration. It would not be reusable across multiple vaults with the same underlying assets and different investment strategies.
* **Not robust against trapped funds**: When assets are present in the `Migration` contract due to direct transfers or mistaken withdrawals, the [entire balance](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/proxy/Migration.sol#L25) of the contract will be deposited to the new vault by the next user. This design is not resistant to genuine user mistakes and prohibits recovering user funds. Consider using the returned value from the [`redeem`](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/proxy/Migration.sol#L22) function to migrate the correct amount of assets and establishing a sweep or rescue function for funds locked in the contract.


**Update:** *Partially fixed in commit [`d97672d`](https://github.com/pods-finance/yield-contracts/pull/88/commits/d97672da3363edaa84a947b746dfd3f0a2af1c07#diff-8e065cf34dc3d3ae1fa0e2256e8ebab0a8ad0142c607b2b9275efaf1cbf8683e).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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


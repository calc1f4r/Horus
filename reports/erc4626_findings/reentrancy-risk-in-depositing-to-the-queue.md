---
# Core Classification
protocol: Pods Finance Ethereum Volatility Vault Audit #1
chain: everychain
category: reentrancy
vulnerability_type: erc777

# Attack Vector Details
attack_type: erc777
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10415
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
  - erc777
  - weird_erc20
  - reentrancy

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

Reentrancy risk in depositing to the queue

### Overview


A bug report has been filed regarding the internal `_deposit` function in the `BaseVault` contract. This function is responsible for transferring a specified amount of `stETH` from the sender to the vault, and before doing this, it adds the deposit to the queue. It is possible for a malicious user to use hooks in the underlying token to re-enter the `deposit` function multiple times, resulting in an increment in the receiver balance on the queue, even though this balance will not correspond to the actual amount deposited into the vault. 

The `_deposit` function in the `BaseVault` contract has been overridden by the implementation in the `STETHVault`, which has the correct order of operation. However, the `BaseVault` is likely to be inherited by future vaults, so it is important to have the correct `_deposit` implementation in this contract in case it is not overridden. It is suggested to reorder the calls, doing the transfer first, and then adding the receiver to the queue to prevent this reentrancy scenario. Additionally, OpenZeppelin’s ERC4626 implementation, which already has this solution implemented, can also be used. 

The bug has been fixed in PR#41, with commit `2ffcb1e` being the last one added.

### Original Finding Content

The internal [`_deposit`](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/BaseVault.sol#L407) function handles user deposits, transferring a specified amount of `stETH` from `msg.sender` to the vault. Before moving the funds, it adds the deposit to the queue, which is processed later by the [`processQueuedDeposits`](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/BaseVault.sol#L371) function.


As the underlying token could have hooks that allow the token sender to execute code before the transfer (e.g., ERC777 standard), a malicious user could use those hooks to re-enter the `deposit` function multiple times.


This re-entrancy will result in an increment in the receiver balance on the queue, even though this balance will not correspond to the actual amount deposited into the vault.


In the current implementation, the `_deposit` function in the `BaseVault` contract is overridden by the [implementation in the `STETHVault`](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/STETHVault.sol#L113-L126), which has the correct order of operation. However, the `BaseVault` is likely to be inherited by future vaults, so it is crucial to have the correct `_deposit` implementation in this contract in case it is not overridden.


Consider reordering the calls, doing the transfer first, and then adding the receiver to the queue to prevent this reentrancy scenario. Also, consider using [OpenZeppelin’s ERC4626 implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/extensions/ERC4626.sol), which already has this solution implemented.


**Update:** *Fixed in [PR#41](https://github.com/pods-finance/yield-contracts/pull/41), with commit `2ffcb1e` being the last one added.*

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

`ERC777, Weird ERC20, Reentrancy`


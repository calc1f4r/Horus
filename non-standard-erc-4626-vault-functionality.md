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
solodit_id: 10399
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

Non-standard ERC-4626 vault functionality

### Overview


This bug report is about an issue with the ERC-4626 [BaseVault](https://github.com/pods-finance/yield-contracts/blob/c4b401ce674c24798de5f9d02c82e466ee0a2600/contracts/vaults/BaseVault.sol) not conforming to the ERC-4626 specifications. Specifically, the functions `previewWithdraw`, `maxDeposit`, `maxMint`, and `maxWithdraw` are not returning 0 when deposits or withdrawals are disabled, and `previewWithdraw` does not include withdrawal fees.

The issue has been partially resolved in [PR#132](https://github.com/pods-finance/yield-contracts/pull/132), with the commit `87e7de33e0a7a699263624641305a8e06ec178b2` being the last one added. The issues regarding `maxDeposit`, `maxMint`, `maxWithdraw` and `maxRedeem` have been resolved and these functions now return 0 when deposits or withdrawals are disabled. However, the `previewWithdraw` function does not include withdrawal fees. Docstrings have been added to `previewWithdraw` and `withdraw` to inform integrators of the presence of withdrawal fees.

It is recommended that the above issues be corrected to meet the ERC-4626 specifications, allowing future vault developers to expect certain protocol behaviors.

### Original Finding Content

There are multiple locations in the ERC-4626 [`BaseVault`](https://github.com/pods-finance/yield-contracts/blob/c4b401ce674c24798de5f9d02c82e466ee0a2600/contracts/vaults/BaseVault.sol) that do not conform to [ERC-4626 specifications](https://eips.ethereum.org/EIPS/eip-4626):


* [`previewWithdraw`](https://github.com/pods-finance/yield-contracts/blob/c4b401ce674c24798de5f9d02c82e466ee0a2600/contracts/vaults/BaseVault.sol#L194) does not include [withdrawal fees](https://eips.ethereum.org/EIPS/eip-4626#previewwithdraw)
* [`maxDeposit`](https://github.com/pods-finance/yield-contracts/blob/c4b401ce674c24798de5f9d02c82e466ee0a2600/contracts/vaults/BaseVault.sol#L209) does not return 0 when [deposits are disabled](https://eips.ethereum.org/EIPS/eip-4626#maxdeposit)
* [`maxMint`](https://github.com/pods-finance/yield-contracts/blob/c4b401ce674c24798de5f9d02c82e466ee0a2600/contracts/vaults/BaseVault.sol#L220) does not return 0 when [withdrawals are disabled](https://eips.ethereum.org/EIPS/eip-4626#maxmint)
* [`maxWithdraw`](https://github.com/pods-finance/yield-contracts/blob/c4b401ce674c24798de5f9d02c82e466ee0a2600/contracts/vaults/BaseVault.sol#L227) does not return 0 when [withdrawals are disabled](https://eips.ethereum.org/EIPS/eip-4626#maxwithdraw)


Consider correcting the above issues to meet the ERC-4626 specifications, allowing future vault developers to expect certain protocol behaviors.


**Update:** *Partially resolved in [PR#132](https://github.com/pods-finance/yield-contracts/pull/132), with commit `87e7de33e0a7a699263624641305a8e06ec178b2` being the last one added. The issues regarding `maxDeposit`, `maxMint`, `maxWithdraw` and `maxRedeem` have been resolved and these functions now return 0 when deposits or withdrawals are disabled. The `previewWithdraw` function does not include withdrawal fees. However, we note that there is ambiguity in how fees on withdrawal should be implemented according to EIP-4626, and that `previewWithdraw` does return the correct number of shares that would be burned in a `withdraw` call. Docstrings have been added to `previewWithdraw` and `withdraw` to inform integrators of the presence of withdrawal fees.*

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


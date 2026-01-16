---
# Core Classification
protocol: Pods Finance Ethereum Volatility Vault Audit #1
chain: everychain
category: arithmetic
vulnerability_type: rounding

# Attack Vector Details
attack_type: rounding
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10416
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
  - rounding

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

Rounding up in minting shares

### Overview


A bug report has been identified in the processing of queued deposits in the yield contracts. When processing the queued deposits, shares are minted to the receiver in the queue according to the amount of assets deposited. However, the amount of shares minted is always rounded up. This means that one can always receive 1 vault share with a 1-wei deposit.

This poses a security risk as a malicious user can spam the deposit queue with 1-wei deposit from many accounts to get 1 share each and then redeem them for more assets when each share is worth more. To address the issue, it has been suggested that the vault shares should be rounded down when minting.

The bug has been fixed in Pull Request #46, with the last commit being 5ac5e3c.

### Original Finding Content

When processing the queued deposits, shares are minted to the receiver in the queue according to the amount of assets deposited. However, the amount of shares minted is always [rounded up](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/BaseVault.sol#L392). This means that one can always receive 1 vault share with a 1-wei deposit.


As the vault is expected to be increasing in value from yield rewards, 1 vault share will be worth more than 1 wei asset eventually. A malicious user can spam the deposit queue with 1-wei deposit from many accounts to get 1 share each and then redeem them for more assets when each share is worth more.


Consider rounding down when minting vault shares.


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

`Rounding`


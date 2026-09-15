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
solodit_id: 10406
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/pods-finance-ethereum-volatility-vault-audit-2/
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

Missing ConfigurationManager check during vault initialization

### Overview

See description below for full details.

### Original Finding Content

As part of the [`constructor`](https://github.com/pods-finance/yield-contracts/blob/c4b401ce674c24798de5f9d02c82e466ee0a2600/contracts/vaults/BaseVault.sol#L53) in the `BaseVault` contract, the `configuration` [state variable is set](https://github.com/pods-finance/yield-contracts/blob/c4b401ce674c24798de5f9d02c82e466ee0a2600/contracts/vaults/BaseVault.sol#L59). However, there is no check to ensure the passed-in `ConfigurationManager` address instance has the [`VAULT_CONTROLLER`](https://github.com/pods-finance/yield-contracts/blob/c4b401ce674c24798de5f9d02c82e466ee0a2600/contracts/vaults/BaseVault.sol#L290) parameter set for the vault contract that is being created. Having the `VAULT_CONTROLLER` parameter be the default value of the zero address for the new vault could result in a loss of the `fee` taken as part of the withdraw control flow, since that fee will be transferred to the `VAULT_CONTROLLER` address designated by the `ConfigurationManager`.


Consider adding a check in the `constructor` of the `BaseVault` contract to ensure calling `getParameter` with the address of the vault being created, and `VAULT_CONTROLLER` does not return the zero address.


***Update:** Acknowledged, not resolved. Pods Finance team stated:*



> *Instead of enforcing it at the code level, that would require us to deploy the vault using CREATE2 in order to know in advance the vault address, we will monitor the VAULT\_CONTROLLER variable to make sure that it was set after the deploy.*
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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


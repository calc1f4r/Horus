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
solodit_id: 10423
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

Refund can be over-credited in a negative yield event

### Overview


This bug report is about deposits added to the queue in Pods Finance's yield contracts. The deposits are recorded as stETH balance amounts, but the stETH token balance can rebase regularly to account for yield, and in the event of slashing, may be subject to a negative yield. This could cause the vault to over credit the user by the rebase difference when the user requests a refund. The report suggests handling the deposits in the queue in shares instead of balances to account for rebase changes on refunds. However, the Pods Finance team has acknowledged the issue, but won't prioritize it right now due to timing. They state that in the event of a slashing event, they can refund the vault by transferring funds directly to the contract.

### Original Finding Content

Deposits added to the queue are [point in time](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/libs/DepositQueueLib.sol#L22) stETH balance amounts. The stETH token balance rebases regularly to account for yield, and in the event of [slashing](https://docs.lido.fi/guides/steth-integration-guide/#risks), may be subject to a negative yield. In the event that a stETH token rebase is negative between the time a user deposits and calls for a [refund](https://github.com/pods-finance/yield-contracts/blob/9389ab46e9ecdd1ea1fd7228c9d9c6821c00f057/contracts/vaults/BaseVault.sol#L334-L346), the vault will over credit the user by the rebase difference.


Consider handling the deposits in the queue in [shares](https://docs.lido.fi/guides/steth-integration-guide/#steth-internals-share-mechanics) instead of balances to account for rebase changes on refunds.


***Update:** Acknowledged, will not fix. Pods Finance team’s statement:*



> *Although we agree with the issue, we won’t prioritize it right now because of timing. In case of a slashing event, we can refund the vault, transferring funds directly to the contract.*
> 
>

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


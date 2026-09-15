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
solodit_id: 10401
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

Refunds will be over-credited in a negative yield event

### Overview


A bug report has been submitted regarding deposits added to the queue in point-in-time stETH balance amounts. These amounts may be subject to a negative yield due to a rebase that could occur between the time a user deposits and calls for a refund. The issue is that the vault will over credit the user by the rebase difference. The suggestion is to handle the deposits in the queue in stETH share amounts to account for rebase changes on refunds. The Pods Finance team has acknowledged the issue but stated that they will not prioritize it right now as it would require a secondary share queue system and parts of the code to change. They have stated that they will prioritize the issue in a future version.

### Original Finding Content

Deposits added to the queue are [point-in-time](https://github.com/pods-finance/yield-contracts/blob/c4b401ce674c24798de5f9d02c82e466ee0a2600/contracts/vaults/BaseVault.sol#L413) stETH balance amounts. The stETH token rebases to account for yield, and in the event of [slashing](https://docs.lido.fi/guides/steth-integration-guide/#the-beacon-chain-oracle), may be subject to a negative yield. In the event that a stETH token rebase is negative between the time a user deposits and calls for a [refund](https://github.com/pods-finance/yield-contracts/blob/c4b401ce674c24798de5f9d02c82e466ee0a2600/contracts/vaults/BaseVault.sol#L327), the vault will over credit the user by the rebase difference.


Consider handling the deposits in the queue in [stETH share](https://docs.lido.fi/guides/steth-integration-guide/#wsteth) amounts to account for rebase changes on refunds.


***Update:** Acknowledged, not resolved. Pods Finance team stated:*



> *Although we agree with the issue, we won’t prioritize it right now. It would require us to implement a secondary share queue system that would require few parts of the code to change. We will prioritize this issue in a future version.*
> 
>

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


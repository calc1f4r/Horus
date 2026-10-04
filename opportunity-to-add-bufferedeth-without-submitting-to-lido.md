---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28123
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20Protocol/README.md#1-opportunity-to-add-bufferedeth-without-submitting-to-lido
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Opportunity to add bufferedETH without submitting to LIDO

### Overview


This bug report is about the `LidoMevTxFeeVault` contract, which is used to store ETH. The issue is that it is possible to send ETH to this contract from any address, which could lead to the fluctuation of the price of lido shares. The recommendation is that the contract should only receive ETH from authorized addresses or the `withdrawRewards()` function should have limits. This will help to prevent unauthorized changes to the price of lido shares.

### Original Finding Content

##### Description
It is possible to send ETH to the `LidoMevTxFeeVault` contract and when the oracle reports contract sends ETH to LIDO, which will be used to rewards, it may fluctuate the price of lido shares.
https://github.com/lidofinance/lido-dao/blob/801d3e854efb33ff33a59fe51187e187047a6be2/contracts/0.8.9/LidoMevTxFeeVault.sol#L79
##### Recommendation
We recommend that the `LidoMevTxFreeVault` contract should receive ETH only from authorized addresses or the `withdrawRewards()` function should have limits.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20Protocol/README.md#1-opportunity-to-add-bufferedeth-without-submitting-to-lido
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


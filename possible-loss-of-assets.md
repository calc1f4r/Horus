---
# Core Classification
protocol: AAVE
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28382
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/AAVE/Governance%20Crosschain%20Bridges%20V2/README.md#1-possible-loss-of-assets
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Possible loss of assets

### Overview


This bug report describes an issue with the BridgeExecutorBase.sol contract, where when calling the payable functions with the transfer of assets, it is not always possible to set the exact amount of an asset when making a transaction. This is especially true for numbers with a lot of decimal points. To solve this issue, it is recommended to add functionality for the ability to withdraw assets from the contract balance. This would allow for a value to be transferred with a slightly larger amount of an asset during a transaction, and then the remaining assets can be withdrawn from the contract balance.

### Original Finding Content

##### Description
At the line https://github.com/aave/governance-crosschain-bridges/blob/763ef5da8befff3a129443a3ff4ef7ca4d3bb446/contracts/BridgeExecutorBase.sol#L253, a call is made to the payable functions with the transfer of assets.
But it is not always possible to set the exact amount of an asset when making a transaction. Especially if the number has a lot of numbers after the decimal point.
It is convenient to transfer a value with a slightly larger amount of an asset during a transaction. But now there is no functionality in the contract to get the remaining asset back.
All additional assets will remain on the balance sheet of the contract. 

##### Recommendation
It is recommended to add functionality for the ability to withdraw assets from the contract balance.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | AAVE |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/AAVE/Governance%20Crosschain%20Bridges%20V2/README.md#1-possible-loss-of-assets
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


---
# Core Classification
protocol: Gearbox Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30773
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Gearbox%20Protocol/Gearbox%20Protocol%20v.1/README.md#1-incorrect-calculation-of-borrowed-amount
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

Incorrect calculation of borrowed amount

### Overview


In the code for Gearbox protocol, there is a bug where the total borrowed amount for credit accounts is not being calculated correctly. This means that the total amount of borrowed money on credit accounts is less than what is being shown on the PoolService, leading to incorrect calculations for the LP (liquidity pool) of the PoolService. To fix this, it is recommended to change the calculation method for borrowed amounts on credit accounts.

### Original Finding Content

##### Description
Total borrowed amount increases unequally, so total borrowed amount on credit accounts would be less than `totalBorrowed` on a `PoolService` which would lead to incorrect calcultaions for LP of a `PoolService`:
https://github.com/Gearbox-protocol/gearbox-contracts/blob/0ac33ba87212ce056ac6b6357ad74161d417158a/contracts/credit/CreditManager.sol#L661
##### Recommendation
We recommend to change calculation of borrowed amount for credit accounts.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Gearbox Protocol |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Gearbox%20Protocol/Gearbox%20Protocol%20v.1/README.md#1-incorrect-calculation-of-borrowed-amount
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


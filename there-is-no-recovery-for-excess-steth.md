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
solodit_id: 28129
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20Protocol/README.md#6-there-is-no-recovery-for-excess-steth
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

There is no recovery for excess `stETH`

### Overview


This bug report is about the possibility of transferring stETH to wstETH, which would cause it to be frozen in the contract. The recommendation is to add a function to recover any excess stETH and maintain the amount of wrapped shares. This would help to ensure that all of the stETH is accounted for and not lost in the contract. This would also help to ensure that the amount of wrapped shares is maintained and not lost due to any transfer errors.

### Original Finding Content

##### Description
It is possible to transfer `stETH` to `wstETH` so it will be frozen in the contract. 
https://github.com/lidofinance/lido-dao/blob/801d3e854efb33ff33a59fe51187e187047a6be2/contracts/0.6.12/WstETH.sol#L28-L118
##### Recommendation
It is necessary to add a function to recover excess `stETH` and keep the wrapped shares amount.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20Protocol/README.md#6-there-is-no-recovery-for-excess-steth
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


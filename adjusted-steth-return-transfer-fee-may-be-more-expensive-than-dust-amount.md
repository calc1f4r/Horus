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
solodit_id: 28189
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Anchor%20Collateral%20stETH/README.md#3-adjusted-steth-return-transfer-fee-may-be-more-expensive-than-dust-amount
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

Adjusted stETH return transfer fee may be more expensive than dust amount

### Overview


This bug report is about an issue with the AnchorVault.vy contract where the difference between the `steth_amount` and `steth_amount_adj` may be less than the `transfer` fee cost. This is a problem because it could lead to a negative return amount. 

To address this issue, it is recommended to include a check for the minimum value to ensure that the difference between the two values is sufficient to return a positive amount. This can be done by adding a check for the minimum value.

### Original Finding Content

##### Description
`steth_amount - steth_amount_adj` value may be less than `transfer` fee cost. 
https://github.com/lidofinance/anchor-collateral-steth/blob/8d52ce72cb42d48dff1851222e3b624c941ddb30/contracts/AnchorVault.vy#L383
The same situation is there for the variable `steth_to_sell` at line:
https://github.com/lidofinance/anchor-collateral-steth/blob/8d52ce72cb42d48dff1851222e3b624c941ddb30/contracts/AnchorVault.vy#L488
##### Recommendation
It is recommended to calculate if there is a sufficient difference between the adjusted eth and original amount to return. 
You can add a check for the minimum value.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Anchor%20Collateral%20stETH/README.md#3-adjusted-steth-return-transfer-fee-may-be-more-expensive-than-dust-amount
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


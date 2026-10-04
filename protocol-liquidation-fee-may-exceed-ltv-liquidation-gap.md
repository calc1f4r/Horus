---
# Core Classification
protocol: Liquorice
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49443
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Liquorice/README.md#3-protocol-liquidation-fee-may-exceed-ltv-liquidation-gap
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

Protocol liquidation fee may exceed LTV liquidation gap

### Overview

The `Repository.setFees()` function has a bug that allows users to set the `protocolLiquidationFee` higher than the `LiquidationThreshold`. This can lead to unprofitable liquidations and potentially cause bad debt accumulation. To fix this, it is recommended to check the relationship between these two parameters and ensure that their sum is always less than 100%.

### Original Finding Content

##### Description
`Repository.setFees()` allows setting `protocolLiquidationFee > 100% - LiquidationThreshold`, making any liquidation unprofitable and potentially leading to bad debt accumulation.
##### Recommendation
We recommend checking the relationship between `protocolLiquidationFee` and `LiquidationThreshold` when setting these parameters. The sum of the `protocolLiquidationFee` and the asset's liquidation LTV threshold must always be less than 100%.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Liquorice |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Liquorice/README.md#3-protocol-liquidation-fee-may-exceed-ltv-liquidation-gap
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


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
solodit_id: 28188
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Anchor%20Collateral%20stETH/README.md#2-no-checking-value-for-zero
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

No checking value for zero

### Overview


This bug report is about a possible scenario where rewards may be sent to a zero address if the `rewards_distributor` is uninitialized. This issue can be found on the link provided in the report. To prevent this issue from occurring, it is recommended to check if `rewards_distributor` is uninitialized. This is important as sending rewards to a zero address could result in the loss of these rewards. This bug report is important to read and understand as it can help prevent the loss of rewards when using the `rewards_distributor` feature.

### Original Finding Content

##### Description
There is a possible scenario where collected rewards may be sent to zero address if `rewards_distributor` is uninitialized 
https://github.com/lidofinance/anchor-collateral-steth/blob/8d52ce72cb42d48dff1851222e3b624c941ddb30/contracts/AnchorVault.vy#L491
##### Recommendation
It is recommended to check if `rewards_distributor` is uninitialized.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Anchor%20Collateral%20stETH/README.md#2-no-checking-value-for-zero
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


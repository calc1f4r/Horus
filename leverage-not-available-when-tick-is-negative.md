---
# Core Classification
protocol: Panoptic Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33817
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/panoptic-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Leverage Not Available When Tick Is Negative

### Overview


A bug was found where the available leverage for a new option is based on the current pool usage. This is determined by comparing the current tick with the median tick, and if there is too much difference, the utilization will be set to over 100%. This results in the required collateral being the same as the short position amount, even if the median tick and current tick are both negative and close together. This means that leverage cannot be accessed in some cases. The bug has now been fixed.

### Original Finding Content

The available leverage for a newly minted option is based on the current pool utilization. A check is performed comparing the current tick with the median tick, and the utilization will be set to over 100% if there is too much deviation between the ticks. For short positions, this results in `max_sell_ratio` being used as the collateral ratio (i.e., 100%) so the required collateral will be the same as the `shortAmounts`. If the median tick and current tick are both negative and close together (the same, for example), the statement will return true not allowing leverage to be accessible. Consider accounting for negative tick values or checking price deviations instead of tick deviations to correctly set the collateral requirement.


***Update:** Resolved.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Panoptic Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/panoptic-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


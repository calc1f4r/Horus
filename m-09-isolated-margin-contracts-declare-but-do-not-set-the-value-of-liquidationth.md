---
# Core Classification
protocol: Marginswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3874
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-04-marginswap-contest
source_link: https://code4rena.com/reports/2021-04-marginswap
github_link: https://github.com/code-423n4/2021-04-marginswap-findings/issues/40

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
  - yield_aggregator
  - indexes

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-09] Isolated margin contracts declare but do not set the value of liquidationThresholdPercent

### Overview


This bug report is about a vulnerability in CrossMarginTrading contracts. The liquidationThresholdPercent is set to 110 in the constructor, however, Isolated margin contracts declare it but do not set the value. This makes the function belowMaintenanceThreshold to always return true unless a value is set via function setLiquidationThresholdPercent. The impact of this vulnerability is that it could lead to incorrect calculations when the holdings or loan is below the 1.1 threshold. The recommended mitigation steps for this issue is to set the initial value for the liquidationThresholdPercent in Isolated margin contracts.

### Original Finding Content


CrossMarginTrading sets value of liquidationThresholdPercent in the constructor: `liquidationThresholdPercent = 110;` Isolated margin contracts declare but do not set the value of liquidationThresholdPercent.

Recommend setting the initial value for the liquidationThresholdPercent in Isolated margin contracts.

This makes function belowMaintenanceThreshold to always return true unless a value is set via function setLiquidationThresholdPercent. Comments indicate that the value should also be set to 110:

```solidity
// The following should hold:
// holdings / loan >= 1.1
// => holdings >= loan \* 1.1
```



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Marginswap |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-04-marginswap
- **GitHub**: https://github.com/code-423n4/2021-04-marginswap-findings/issues/40
- **Contest**: https://code4rena.com/contests/2021-04-marginswap-contest

### Keywords for Search

`vulnerability`


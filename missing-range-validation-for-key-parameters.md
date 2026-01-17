---
# Core Classification
protocol: NUTS Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62700
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/NUTS%20Finance/Pike/README.md#3-missing-range-validation-for-key-parameters
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

Missing Range Validation for Key Parameters

### Overview

See description below for full details.

### Original Finding Content

##### Description
This issue has been identified in several parameter setters and configuration functions—such as `setProtocolSeizeShare()`, `setCloseFactor()`, `configureMarket()`, `configureEMode()`, and the handling of `borrowRateMaxMantissa_`. None of these parameters are currently constrained by explicit interval checks.

Specific risks include:
- **`setProtocolSeizeShare()`**: Failing to ensure that `reserveFactorMantissa + protocolSeizeShareMantissa` remains under 1e18 could result in seizing more collateral than exists.
- **`setCloseFactor()`**: The `closeFactor` could be set to an extreme value above 1e18, breaking normal liquidation assumptions.
- **`configureMarket()`, `configureEMode()`**: The `liquidationIncentiveMantissa` may be set to an unreasonably high or low value, distorting the liquidation process.

##### Recommendation
We recommend introducing explicit validation in each function to ensure these parameters remain within sensible intervals.


### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | NUTS Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/NUTS%20Finance/Pike/README.md#3-missing-range-validation-for-key-parameters
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


---
# Core Classification
protocol: BadgerDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 741
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-09-bvecvx-by-badgerdao-contest
source_link: https://code4rena.com/reports/2021-09-bvecvx
github_link: https://github.com/code-423n4/2021-09-bvecvx-findings/issues/50

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

protocol_categories:
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[L-02] CvxLocker.setStakeLimits missing validation

### Overview

See description below for full details.

### Original Finding Content

## Handle

cmichel


## Vulnerability details

## Vulnerability Details
The `CvxLocker.setStakeLimits` function does not check `_minimum <= _maximum`.

## Recommended Mitigation Steps
Implement these two checks instead:

```solidity
require(_minimum <= _maximum, "min range");
require(_maximum <= denominator, "max range");
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | BadgerDAO |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-bvecvx
- **GitHub**: https://github.com/code-423n4/2021-09-bvecvx-findings/issues/50
- **Contest**: https://code4rena.com/contests/2021-09-bvecvx-by-badgerdao-contest

### Keywords for Search

`vulnerability`


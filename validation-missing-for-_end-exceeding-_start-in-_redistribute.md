---
# Core Classification
protocol: Velodrome
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63393
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Velodrome/CLGaugeFactory/README.md#2-validation-missing-for-_end-exceeding-_start-in-_redistribute
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

Validation Missing for `_end` Exceeding `_start` in `_redistribute()`

### Overview

See description below for full details.

### Original Finding Content

##### Description
The `Redistributor._redistribute()` function lacks validation to ensure that `_end` is greater than `_start`, which could lead to an underflow in the loop condition and subsequent out-of-bounds array access. If `_start > _end`, the expression `_end - _start` will underflow in Solidity 0.7.6, causing the transaction to revert with an unclear error message. 

Although this is a rare case since the function is restricted to `onlyUpkeepOrKeeper`, it is still better to provide a clear error message rather than relying on panic errors. 
<br/>
##### Recommendation
We recommend adding a validation check to ensure that `_end > _start`.

> **Client's Commentary**
> Fixed in https://github.com/aerodrome-finance/slipstream/commit/7e3da16236a997db202f16c385021f739dbf516c



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Velodrome |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Velodrome/CLGaugeFactory/README.md#2-validation-missing-for-_end-exceeding-_start-in-_redistribute
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


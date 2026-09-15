---
# Core Classification
protocol: Vaultka
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37465
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-06-Vaultka.md
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
  - Zokyo
---

## Vulnerability Title

Missing validation in the `addGmPool()` method

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low

**Status**: Resolved 

**Description**

In the contract GlmManager.sol, the method `addGmPool()` allows the owner to set the pool info but without the following checks:
```solidity
 require(_targetWeight <= DECIMAL_PRECISION, "Target weight is too high"); 
       require(_targetWeight >= gmPools[_index].minimumWeight, "Target weight is too low");
       require(_targetWeight >= 1e28 && _minimumWeight >= 1e28, "weight has to be >1%");
```
This means Owner can bypass this checks when adding a pool but this seems to be important as `targetWeight` for a pool getting set more than `minimumWeight` can affect deposit/withdrawal process.

**Recommendation**: 

Consider adding these checks in `addPool()` as well.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Vaultka |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-06-Vaultka.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


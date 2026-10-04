---
# Core Classification
protocol: Steadefi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35562
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-05-15-Steadefi.md
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
  - Zokyo
---

## Vulnerability Title

PRECISION LOSS

### Overview


The report discusses a bug in the `lendingAPR()` function which calculates the current lendingAPR. The bug is caused by a division before a multiplication in the formula, which can result in rounding errors. The recommended solution is to execute all multiplications before divisions in the formula. This will prevent rounding errors and ensure accurate calculations. The bug has been resolved and the status of the issue is marked as resolved.

### Original Finding Content

**Severity**: Medium	

**Status**: Resolved

**Description**

The `lendingAPR()` function which returns the current lendingAPR, calculated as `borrowAPR * utilizationRate * ( 1 - performanceFee)` implements a division before a multiplication in the formula which can lead to rounding error as Solidity rounds down decimals.

The used formula: 
```solidity
return borrowAPR_ * utilizationRate_
                        / SAFE_MULTIPLIER
                        * ((1 * SAFE_MULTIPLIER) - performanceFee)                        			/ SAFE_MULTIPLIER;
```
	

**Recommendation:**

Execute every multiplication before divisions, the new formula would be: 
```solidity
return borrowAPR_ * utilizationRate_
                        * ((1 * SAFE_MULTIPLIER) - performanceFee) 
                        / SAFE_MULTIPLIER  / SAFE_MULTIPLIER;
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Steadefi |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-05-15-Steadefi.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


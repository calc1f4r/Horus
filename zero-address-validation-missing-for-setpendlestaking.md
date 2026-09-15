---
# Core Classification
protocol: Magpie
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44784
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-22-Magpie.md
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

Zero address validation missing for setPendleStaking

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low

**Status**: Resolved

**Description**

In mPendleConverted.sol contract, the method `setPendleStaking(address _pendleStaking)` does not check if address _pendleStaking is zero-address or not. Setting a zero-address accidentally can cause DoS for method lockAllPendle().
 
**Recommendation**: 

Add zero-address validation for the _pendleStaking parameter. 

**Fix**: As of commit 0097c, issue is fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Magpie |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-22-Magpie.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


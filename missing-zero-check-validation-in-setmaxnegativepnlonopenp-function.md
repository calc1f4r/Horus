---
# Core Classification
protocol: Narwhal Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44712
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal Finance.md
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

Missing Zero Check Validation in setMaxNegativePnlOnOpenP Function

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low

**Status**: Resolved

**Description**:

The setMaxNegativePnlOnOpenP function in the PairInfos contract sets the maximum negative profit and loss percentage that can be incurred on opening a trade. However, there is no check for whether the value passed as the input parameter is zero, which could lead to unexpected results.
If a manager passes a value of zero as the input parameter, it would effectively disable the maximum negative PnL check, which could result in trades being opened that incur significantly higher losses than expected. 

**Recommendation**:

To address this vulnerability, a zero check validation should be added to the setMaxNegativePnlOnOpenP function to prevent the input parameter from being set to zero. This would ensure that the maximum negative PnL check is always enforced, which would help to prevent unexpected losses.

**Fixed**: Issue fixed in commit a72e06b

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Narwhal Finance |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


---
# Core Classification
protocol: Umami
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44771
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-16-Umami.md
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

High hardcoded tolerance (slippage)

### Overview


This bug report discusses a potential issue in the AaavePositionManager contract. The bug involves a hardcoded value for the swap tolerance, which is set at 2% instead of the usual 0.5%. This can lead to smaller than expected amounts in swap transactions and make the contract vulnerable to MEV extractors using sandwich attacks. The recommendation is to make this value configurable at the contract level and set it at 0.5% as a starting point. The bug has been resolved.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

In the AaavePositionManager contract  the swap `TOLERANCE_BIPS` in bips is hardcoded to a high value (2%) relative to the usual slippage (0.5%) present in swap transactions. This can lead to smaller than expected out amounts given the in amount and it will make the contract an open target for MEV extractors that are using sandwich attacks. 

**Recommendation**: 

Allow for this value to be configurable at least at contract level in case it needs adjustments and start with an value of 0.5% for it.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Umami |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-16-Umami.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


---
# Core Classification
protocol: Avantis
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37125
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-12-23-Avantis.md
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

Function returns wrong values

### Overview


The bug report describes an issue with a function called traderReferralDiscount() in the Referral.sol file. This function is returning incorrect values for traderFeesPostDiscount and rebateShare when the discount percentage is set to zero. The recommendation is to fix this issue by returning the correct values when the discount percentage is zero. The bug has been resolved by the client by removing an if statement.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

Referral.sol - Function traderReferralDiscount() returns significant false values of traderFeesPostDiscount and rebateShare.
That takes place in a scenario where tiers[_tierId].feeDiscountPct is zero. In that case traderFeesPostDiscount should be equal to _fee because there is zero discount. And so rebateShare should be non-zero since it is derived from traderFeesPostDiscount.

**Recommendation** 

Return the correct values in the case of zero `tiers[_tierId].feeDiscountPct`.

**Fix**:  Issue was addressed successfullthe y by client in dad4a2c6e161294019e0fd1ea7a89e797647c2e5  by removing the if statement.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Avantis |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-12-23-Avantis.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


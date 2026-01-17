---
# Core Classification
protocol: Creditswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37106
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-12-22-CreditSwap.md
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

Missing zero address checks for CreditUSDMinter

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low

**Status**:  Resolved

**Description**

There is missing zero address check for creditUSD_ and controller_ parameter of function initialize(). Also there is missing zero address check in the setCollateralCreditLimit() function for collateralAsset parameter. This can lead to CreditLimit of zero address being set, which is a logical error. It can also lead to unintended or undiscovered issues. Similarly, there is missing zero address check for backingAsset parameter of the setBackingDeduction() function.

**Recommendation**: It is advised to add a zero address check for the above functions.

**Comments**: The client added zero address check for creditUSD_ but not controller as they said it would not be required as it would revert if set to 0.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Creditswap |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-12-22-CreditSwap.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


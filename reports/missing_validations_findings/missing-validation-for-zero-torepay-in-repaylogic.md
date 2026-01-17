---
# Core Classification
protocol: Evoq
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45930
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2025-01-09-Evoq.md
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

Missing Validation for Zero toRepay in repayLogic

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Informational

**Status**: Acknowledged 

**Description**:

The repayLogic function calculates the toRepay value as the minimum of _getUserBorrowBalanceInOf(_poolToken, _onBehalf) and _amount. However, the function does not check whether toRepay is zero after this calculation. If toRepay is zero, the function continues to execute and incurs unnecessary gas costs without performing any meaningful repayment.
This issue arises when:
The user's debt for the specified _poolToken is already fully repaid (_getUserBorrowBalanceInOf(_poolToken, _onBehalf) == 0).
The _amount provided by the caller is greater than zero.
In such cases, the contract performs operations that ultimately have no effect, leading to wasted gas.

**Recommendation:**

Introduce a validation check after calculating toRepay to ensure it is greater than zero before proceeding. If toRepay is zero, revert the transaction to prevent unnecessary execution

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Evoq |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2025-01-09-Evoq.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


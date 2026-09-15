---
# Core Classification
protocol: Rwa
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48936
audit_firm: Kann
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Kann Audits/2025-01-19-RWA.md
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
  - Kann Audits
---

## Vulnerability Title

[I-01] Ensure Collateral Addresses and Amounts Arrays Have Matching Lengths

### Overview


The bug report is about a function that does not check the lengths of two arrays, collaterals and collateralAmounts, which can cause unexpected behavior or errors. The report suggests adding a check to ensure that both arrays are the same length before processing them.

### Original Finding Content

**Description**

The lengths of the collaterals and collateralAmounts arrays are not explicitly checked within the function. If their lengths differ, this can lead to mismatched indexing, potentially causing unexpected behavior or errors when processing collateral addresses and their corresponding amounts.

This issue assumes the off-chain logic ensures both arrays are correctly populated. However, without a validation check in the contract, there's no guarantee of alignment, which could result in incorrect collateral handling.

**Recommendations**

Consider adding this check:

```solidity
if (collaterals.lenght != collateralAmounts.lenght) revert
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Kann |
| Protocol | Rwa |
| Report Date | N/A |
| Finders | Kann Audits |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Kann Audits/2025-01-19-RWA.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


---
# Core Classification
protocol: Echelon Market
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61349
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/echelon-market/9ee15c30-6a0f-4a70-b5ce-63b8a887bd4e/index.html
source_link: https://certificate.quantstamp.com/full/echelon-market/9ee15c30-6a0f-4a70-b5ce-63b8a887bd4e/index.html
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
finders_count: 3
finders:
  - Hamed Mohammadi
  - Adrian Koegl
  - Roman Rohleder
---

## Vulnerability Title

[Initia] Removal of Accrual Functions Before Protocol Changes Leading to Interest Distortion

### Overview


The bug report discusses an issue with the functions used to calculate interest in the `isolated_lending/sources/isolated_lending.move` file. These functions, `set_interest_fee_bps()` and `set_pair_jump_interest_rate_model()`, were previously used to accrue interest before changing protocol parameters. However, they have since been removed, which can result in distorted interest calculations and unexpected changes in interest rates. The report recommends adding back the accrual functions to ensure a fair protocol behavior.

### Original Finding Content

**Update**
Addressed in: `f43ade3`. The recommended accrual function calls are added.

**File(s) affected:**`isolated_lending/sources/isolated_lending.move`

**Description:** The following functions used to accrue interest before changing protocol parameters. This ensure that up to the point of the changes all interest would be accumulated as per the previous configuration.

1.   `set_interest_fee_bps()`.
2.   `set_pair_jump_interest_rate_model()`.

Removing the accrual functions would lead to distorted interests as pending interest accrual would assume the new values, which could lead to sudden unexpectedly high or low interest changes.

**Recommendation:** We recommend adding back the accrual functions to ensure a more fair protocol behavior.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Echelon Market |
| Report Date | N/A |
| Finders | Hamed Mohammadi, Adrian Koegl, Roman Rohleder |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/echelon-market/9ee15c30-6a0f-4a70-b5ce-63b8a887bd4e/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/echelon-market/9ee15c30-6a0f-4a70-b5ce-63b8a887bd4e/index.html

### Keywords for Search

`vulnerability`


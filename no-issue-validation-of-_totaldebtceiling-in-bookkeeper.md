---
# Core Classification
protocol: Fathom Stablecoin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31008
audit_firm: Oxorio
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom Stablecoin.md
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
  - Oxorio
---

## Vulnerability Title

[NO ISSUE] Validation of `_totalDebtCeiling` in `BookKeeper`

### Overview

See description below for full details.

### Original Finding Content

##### Location
File | Location | Line
--- | --- | ---
[BookKeeper.sol](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/BookKeeper.sol#L150 "/contracts/main/stablecoin-core/BookKeeper.sol" "/contracts/main/stablecoin-core/BookKeeper.sol") | contract `BookKeeper` > function `setTotalDebtCeiling` | 150

##### Description
In the function [`setTotalDebtCeiling`](https://github.com/Into-the-Fathom/fathom-stablecoin-smart-contracts/tree/3768c87367d286ae0e82f444b2f9d760417b507e/contracts/main/stablecoin-core/BookKeeper.sol#L150 "/contracts/main/stablecoin-core/BookKeeper.sol") of the contract `BookKeeper`, the `_totalDebtCeiling` parameter must be passed in rad, which is not enforced. Incorrect variable passed will lead to the failed calls of the `adjustPosition` transactions in the `BookKeeper`.
##### Recommendation
We recommend validating the parameter to be passed in rad.
##### Update
###### Client's response
Fix no need. 
The `debtCeiling` can be theoretically 0.5 FXD, which is below 1 `RAD` of debt ceiling.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Oxorio |
| Protocol | Fathom Stablecoin |
| Report Date | N/A |
| Finders | Oxorio |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-01-19-Fathom Stablecoin.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


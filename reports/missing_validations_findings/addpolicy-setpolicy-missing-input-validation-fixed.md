---
# Core Classification
protocol: Tidal
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27170
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/05/tidal/
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
finders_count: 2
finders:
  - Heiko Fisch
  -  David Oz

---

## Vulnerability Title

addPolicy, setPolicy – Missing Input Validation ✓ Fixed

### Overview


This bug report describes an issue with the `addPolicy` and `setPolicy` functions in the Pool.sol file of TidalFinance, where essential input validation is missing on two parameters, `collateralRatio_` and `weeklyPremium_`. The `collateralRatio_` should be validated to be non-zero, and it might be worth adding a range check. The `weeklyPremium_` should be less than `RATIO_BASE` at least, and it might be worth adding a maximum value check. The issue has been fixed in 3bbafab926df0ea39f444ef0fd5d2a6197f99a5d by implementing the auditor’s recommendation.

### Original Finding Content

#### Resolution



Fixed in [3bbafab926df0ea39f444ef0fd5d2a6197f99a5d](https://github.com/TidalFinance/tidal-contracts-v2/tree/3bbafab926df0ea39f444ef0fd5d2a6197f99a5d) by implementing the auditor’s recommendation.


#### Description and Recommendation


Both `addPolicy` and `setPolicy` are missing essential input validation on two main parameters:


1. `collateralRatio_` – Should be validated to be non-zero, and it might be worth adding a range check.
2. `weeklyPremium_` – Should be less than `RATIO_BASE` at least, and it might be worth adding a maximum value check.


#### Examples


**contracts/Pool.sol:L159**



```
function addPolicy(

```
**contracts/Pool.sol:L143**



```
function setPolicy(

```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Tidal |
| Report Date | N/A |
| Finders | Heiko Fisch,  David Oz
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2023/05/tidal/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


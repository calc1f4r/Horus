---
# Core Classification
protocol: Resolv
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44363
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Resolv/PoR%20Oracles/README.md#6-missing-validation-in-constructor-parameters-of-usrredemptionextension
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
  - MixBytes
---

## Vulnerability Title

Missing Validation in Constructor Parameters of `UsrRedemptionExtension`

### Overview

See description below for full details.

### Original Finding Content

##### Description
This issue has been identified in the constructor of the contract `UsrRedemptionExtension`.

1. **Potentially Large `_lastResetTime`:**
   The constructor does not include validation to ensure that `_lastResetTime` is within a reasonable range. If an excessively large value is mistakenly provided, it could result in the `currentRedemptionUsage` being reset far into the future. Furthermore, an incorrectly large `lastResetTime` cannot be corrected after deployment.

2. **Duplicate Entries in `_allowedWithdrawalTokenAddresses`:**
   The constructor does not validate that the addresses provided in `_allowedWithdrawalTokenAddresses` are unique. While this does not affect the correctness of the contract, it could make debugging and identification of invalid parameters more challenging.

The issue is classified as **low** severity because it does not compromise the protocol's security directly but could lead to operational inefficiencies and errors.

##### Recommendation
1. Add a check in the constructor to ensure that `_lastResetTime` is not excessively large and falls within a sensible range.
2. Add a check in `UsrRedemptionExtension.addAllowedWithdrawalToken()` that the token being added has not already been added.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Resolv |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Resolv/PoR%20Oracles/README.md#6-missing-validation-in-constructor-parameters-of-usrredemptionextension
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


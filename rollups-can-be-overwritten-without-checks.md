---
# Core Classification
protocol: Polygon zkEVM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53616
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/polygon/Sigma_Prime_Polygon_LXLY_Bridge_Security_Assessment_Report_v2_1.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/polygon/Sigma_Prime_Polygon_LXLY_Bridge_Security_Assessment_Report_v2_1.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Rollups Can Be Overwritten Without Checks

### Overview


The report discusses a bug where users are able to overwrite an existing rollup by calling a specific function. This can lead to the loss of important information and requires a contract upgrade to fix. The bug is not easily triggered, but the development team has acknowledged it and is working on a solution in their latest code update.

### Original Finding Content

## Description

It is possible to overwrite an existing rollup by calling `addExistingRollup()` with a rollup address relating to an existing rollup. This then allows the user to arbitrarily overwrite the other parameters stored about a rollup in `PolygonRollupManager`. If done on an existing rollup, then `rollupAddressToID` will be overwritten for this address and cannot be reset to its original value without a contract upgrade. 

It is worth noting that this is an access-controlled function that is normally only accessible to the timelock contract and requires a different `chainId` to the existing value to succeed. Hence, the risk of this bug occurring is low.

## Recommendations

Checks should be added to `addExistingRollup()` to ensure the rollup address does not already exist in the system. This can be done by checking the `rollupAddressToID` mapping to ensure it returns a zero `rollupID`.

## Resolution

The development team has acknowledged these comments and added extra checks to `addExistingRollup()` in PR #167.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Polygon zkEVM |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/polygon/Sigma_Prime_Polygon_LXLY_Bridge_Security_Assessment_Report_v2_1.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/polygon/Sigma_Prime_Polygon_LXLY_Bridge_Security_Assessment_Report_v2_1.pdf

### Keywords for Search

`vulnerability`


---
# Core Classification
protocol: SOFA.org
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36041
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/sofa/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/sofa/review.pdf
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

COLLATERAL Token Is Not Part of The digest

### Overview


There is a bug in the COLLATERAL token where it is not included in the digest that the market maker signs. This means that if the vault is upgraded to a new implementation that allows for a different collateral token, a user can use a signature intended for the old token to call the mint() function. This could lead to unexpected and potentially harmful consequences, especially if the new collateral token has a different value than the old one. The development team has acknowledged the issue and stated that significant governance protections will prevent the collateral token from being modified in an existing vault. This bug has been identified in the Sofa Protocol Contract Review and is labeled as SFA-06.

### Original Finding Content

## Description

The COLLATERAL token is not part of the digest that the market maker signs. This means that if the vault is upgraded to a new implementation that allows the admin to change to another collateral token, a user can call the `mint()` function using a signature intended for the old token, if it has not expired yet. This scenario, whilst improbable, could be especially impactful if the new collateral token has a different value than the previous one. For example, consider an MM signing a transaction for 1e9 USDC and then this being used to trade with 1e9 WBTC.

## Recommendations

Include the COLLATERAL in the digest.

## Resolution

The development team acknowledged the issue and stated that significant governance protections would prevent the COLLATERAL token of an existing vault from being modified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | SOFA.org |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/sofa/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/sofa/review.pdf

### Keywords for Search

`vulnerability`


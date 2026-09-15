---
# Core Classification
protocol: Aave
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19249
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/aave/aave-protocol/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/aave/aave-protocol/review.pdf
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

Limitations of Exposure Ceiling

### Overview


A bug was reported in Aave Protocol v2.0 where an exposure ceiling was intended to be added as a control against supply attacks and disabling an asset to be used as collateral on new loans. The exposure ceiling would reduce the Loan to Value (LTV) ratio of an asset to zero once the total supply of an asset breached the exposure cap. It was deemed infeasible to implement the exposure cap without enforcing strict conditions which significantly reduce the user experience and increase gas cost. 

As an alternative solution, the LTV of an asset was manually set to zero and additional checks were added to transfer(), withdraw(), and setUserUseReserveAsCollateral() which enforce the user to remove any collateralised assets with LTV set to zero before other collateralised assets may be modified. This enforces condition b) in that if the LTV of an asset is set to zero, new loans cannot be made using the exposed asset as collateral (unless there is also sufficient collateral in assets with LTV non-zero). The solution can be seen in PR #197.

### Original Finding Content

## Description
An exposure ceiling was intended to be added as a control 
- a) against supply attacks such as infinite minting which would allow draining of all funds in the pool 
- b) disabling an asset to be used as collateral on new loans. 

The exposure ceiling would reduce the Loan to Value (LTV) ratio of an asset to zero once the total supply of an asset breached the exposure cap without reducing the ability of this asset to be used as collateral for existing loans (through the liquidation threshold).

## Recommendations
It was deemed infeasible to implement the exposure cap solving both issues mentioned above without enforcing strict conditions which significantly reduce the user experience and increase gas cost.

## Resolution
A contrary solution to the exposure cap was implemented where the LTV of an asset will be manually set to zero. 

Additional checks were added to `transfer()`, `withdraw()`, and `setUserUseReserveAsCollateral()` which enforce the user to remove any collateralised assets with LTV set to zero before other collateralised assets may be modified. 

This enforces condition b) in that if the LTV of an asset is set to zero, new loans cannot be made using the exposed asset as collateral (unless there is also sufficient collateral in assets with LTV non-zero).

The solution can be seen in PR #197.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Aave |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/aave/aave-protocol/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/aave/aave-protocol/review.pdf

### Keywords for Search

`vulnerability`


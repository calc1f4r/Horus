---
# Core Classification
protocol: Synthetix
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19670
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/synthetix/ethercollateral/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/synthetix/ethercollateral/review.pdf
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

Contract Owner Can Arbitrarily Change Minting Fees and Interest Rates

### Overview


This bug report is regarding the EtherCollateral contract, which allows the owner to change both the issueFeeRate and interestRate variables after loans have been opened. This could lead to a situation where the owner can control fees to an extent that they are equal to, or even exceed, the collateral for any given loan. The development team has acknowledged the issue and stated that Synthetix reserves the right to change the Interest and minting fee for the benefit of SNX holders and to use as a mechanism to incentivise or disincentivise loan opening and closing. As a resolution, it is recommended that the minting fee (issueFeeRate) be made a constant, and not be changed by the owner.

### Original Finding Content

## Description
The `issueFeeRate` and `interestRate` variables can both be changed by the EtherCollateral contract owner after loans have been opened. As a result, the owner can control fees such that they equal/exceed the collateral for any given loan.

## Recommendations
While "dynamic" interest rates are common, we recommend considering the minting fee (`issueFeeRate`) to be a constant that cannot be changed by the owner.

## Resolution
The development team acknowledged the issue and provided the following response:

> "Synthetix reserves the right to change the Interest and minting fee for the benefit of SNX holders and to use as a mechanism to incentivise or disincentivise loan opening and closing."

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Synthetix |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/synthetix/ethercollateral/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/synthetix/ethercollateral/review.pdf

### Keywords for Search

`vulnerability`


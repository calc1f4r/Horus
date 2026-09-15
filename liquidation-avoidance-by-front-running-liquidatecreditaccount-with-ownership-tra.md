---
# Core Classification
protocol: Gearbox
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19387
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

Liquidation Avoidance by Front-Running liquidateCreditAccount() with Ownership Transfer

### Overview


This bug report is about the Gearbox v2.0 protocol, where a user could potentially avoid liquidation by front-running calls to liquidateCreditAccount() and transferring CreditAccount ownership to a different address. This could lead to a shortage of collateral when a liquidator closes an uncollateralized credit account, leaving liquidity providers to cover the shortage. 

The development team was able to mitigate this issue by reverting calls to transferAccountOwnership() when the account has a health factor below zero. This was done in commit 1e10d15 and was also modified in the final retesting target. 

In conclusion, to prevent this issue from occurring again, it is important to ensure that liquidations operate on the address of the credit account and not the borrower. Changes in credit account ownership should not affect the overall functionality of the Gearbox protocol.

### Original Finding Content

## Description

Due to liquidations being performed on the borrower’s address and not the CreditAccount, users can feasibly avoid liquidation by front-running calls to `liquidateCreditAccount()` and transferring CreditAccount ownership to a different address.

Considering that Gearbox intends to deploy their contracts on low-cost blockchains, it is entirely possible for users to sustain such an attack until the borrower’s collateral does not sufficiently cover the loss. As a result, liquidity providers will have to cover the shortage in collateral when a liquidator closes an uncollateralised credit account.

## Recommendations

- Ensure that liquidations operate on the address of the credit account and not the borrower.
- Changes in credit account ownership should not affect the overall functionality of the Gearbox protocol.

## Resolution

The development team mitigated this issue in commit `1e10d15` by reverting calls to `transferAccountOwnership()` when the account has a health factor below zero.

Note that the checks have been modified in the final retesting target, albeit to the same effect.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Gearbox |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/gearbox/review.pdf

### Keywords for Search

`vulnerability`


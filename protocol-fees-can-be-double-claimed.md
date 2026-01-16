---
# Core Classification
protocol: Tracer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19704
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/tracer/tracer-3/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/tracer/tracer-3/review.pdf
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

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - derivatives

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Protocol Fees Can be Double Claimed

### Overview


This bug report is about the feeTransfer() function which is used to handle the payment of fees associated with an asset being tracked. The logic of the function has been changed with the addition of the claimPrimaryFees() and claimSecondaryFees() functions. This causes the fees to be paid out multiple times if either of these functions is called subsequently. It is recommended that the use of safeTransfer() be removed from the feeTransfer() function so that fees are only transferred when either of the two functions is called.

### Original Finding Content

## Description

On each update interval, a keeper will perform an upkeep which executes a price change in the asset being tracked before transferring the associated fees to the primary and secondary accounts. The `feeTransfer()` function handles how fee amounts are paid; however, the logic has been altered with the addition of the `claimPrimaryFees()` and `claimSecondaryFees()` functions. 

`feeTransfer()` will transfer fees to the respective accounts and increment two storage variables, `secondaryFees` and `primaryFees`. As a result, if anyone subsequently calls `claimPrimaryFees()` or `claimSecondaryFees()`, fees will be paid out to these accounts again.

## Recommendations

Consider removing the use of `safeTransfer()` in `feeTransfer()` such that fees are only transferred when `claimPrimaryFees()` or `claimSecondaryFees()` is called.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Tracer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/tracer/tracer-3/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/tracer/tracer-3/review.pdf

### Keywords for Search

`vulnerability`


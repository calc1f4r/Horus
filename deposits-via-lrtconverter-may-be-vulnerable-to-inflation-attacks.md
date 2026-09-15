---
# Core Classification
protocol: Kelp
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53640
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-withdrawals/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-withdrawals/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Deposits Via LRTConverter May Be Vulnerable To Inflation Attacks

### Overview

See description below for full details.

### Original Finding Content

## Description

The function `convertEigenlayerAssetToRsEth()` allows users to convert their EigenLayer assets and receive rsETH in return, enabling an alternative way to deposit assets into the protocol. However, in contrast to depositing via `LRTDepositPool`, there are 2 protections missing, exposing the user to price manipulation attacks such as inflation attacks:

1. **No minimumExpectedReturn parameter**: This means a user has no control over the amount of rsETH they wish to receive. As a result, an attacker could frontrun a deposit and skew the price of rsETH, resulting in the user receiving less rsETH than they may expect.
2. **No minimum deposit required**: This allows an attacker to deposit a very small amount of assets, opening up the possibility for inflation attacks.

The testing team understands that the function `convertEigenlayerAssetToRsEth()` currently can only be called by the `LRTOperator`. Depending on how this is handled offchain, this could significantly decrease the likelihood of exploitation. Regardless, since the protocol team expressed interest in potentially allowing users to execute this function in the future, it is advisable to highlight these issues.

## Recommendations

Add the two mentioned protections, similar to how they are implemented in `LRTDepositPool`.

## Resolution

The development team has fixed the above issue as per commit `7db0e43`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Kelp |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-withdrawals/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/kelp/lrt-withdrawals/review.pdf

### Keywords for Search

`vulnerability`


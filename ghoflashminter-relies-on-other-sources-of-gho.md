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
solodit_id: 19220
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/aave/aave-gho-core/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/aave/aave-gho-core/review.pdf
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

GhoFlashMinter relies on other sources of GHO

### Overview

See description below for full details.

### Original Finding Content

## Description

**GhoFlashMinter** mints and burns exclusively within `flashLoan()`, where it mints and burns the exact same amounts. It is therefore neither a net producer nor a consumer of GHO. However, because there is a transfer of GHO on line [103] of `flashLoan()`, the contract does require access to additional GHO to function. This is not necessarily a problem, but it does mean that the flash minter is dependent on other facilitators for this supply of GHO and will have the long-term effect of transferring their GHO to the treasury.

## Recommendations

Be aware of this issue and consider its effect on the protocol as a whole, in particular its potential impact on GHO-02.

## Resolution

The development team has acknowledged the issue and decided to make no code changes at this time.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Aave |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/aave/aave-gho-core/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/aave/aave-gho-core/review.pdf

### Keywords for Search

`vulnerability`


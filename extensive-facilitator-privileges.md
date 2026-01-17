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
solodit_id: 19219
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

Extensive facilitator privileges

### Overview

See description below for full details.

### Original Finding Content

## Description
As facilitators have the ability to mint GHO simply by calling `GhoToken.mint()`, and because the AAVE price oracles will set GHO’s value at a hardcoded $1, it is worth emphasizing the power that facilitators have. 

Any new facilitator should be thoroughly reviewed, in particular for any exploit that might cause it to call `GhoToken.mint()` in an unapproved manner. The bucket allowance system is a worthwhile mitigation for this risk, but it offers limited protection. If GHO were minted excessively by a compromised facilitator, the price of the token on decentralized exchanges could suddenly drop, allowing other actors to purchase it and continue exploiting the protocol even if the bucket limits have been reached.

## Recommendations
Be aware of this issue and keep all relevant considerations in mind with each facilitator added.

## Resolution
The development team is aware of the issue and has provided the following comments: Introducing new facilitators is a major risk. All new facilitators should be reviewed and go through the utmost level of security review. Additionally, new facilitators should be added with low capacities, which can be increased over time.

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


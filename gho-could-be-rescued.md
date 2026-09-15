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
solodit_id: 53748
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/aave/aave-gho-core/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/aave/aave-gho-core/review.pdf
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

GHO could be rescued

### Overview

See description below for full details.

### Original Finding Content

## Description
The `rescueTokens()` function specifically blocks rescue of `underlyingAsset`, which would be the GHO token. However, in the case of GHO, it is not clear that this strictly needs to be the case. The GhoAToken contract does not hold a pool of GHO long term, although GHO is held during repayments to the pool. Furthermore, it does seem like the token most likely to be sent to the GhoAToken contract in error would be GHO.

## Recommendations
Consider whether it is in the protocol’s interests to allow rescue of GHO tokens. If such a measure is implemented, it might be prudent to automatically send them to a specific safe address, perhaps the treasury.

## Resolution
Changes made to the design of the GhoAToken contract have rendered this issue null as the contract now holds tokens. However, the development team have clarified that the protocol’s governance would have the option to distribute GHO funds that need to be rescued from this contract.

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

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/aave/aave-gho-core/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/aave/aave-gho-core/review.pdf

### Keywords for Search

`vulnerability`


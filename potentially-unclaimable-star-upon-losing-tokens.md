---
# Core Classification
protocol: Urbit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19759
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/urbit/stardust/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/urbit/stardust/review.pdf
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

Potentially Unclaimable Star Upon Losing Tokens

### Overview

See description below for full details.

### Original Finding Content

## Description
The Treasury contract requires a fixed amount of 1e18 STAR tokens to redeem a star asset. Since STAR tokens are only minted when users deposit stars, the amount of tokens held by the Treasury must be 1e18 multiplied by Treasury’s asset count (equal to the number of deposited stars). That way, when all stars are redeemed, the total balance of STAR equals zero.

This coupling between Treasury and STAR tokens means that if even one token is lost, i.e. sent to an address without a known related private key, then there should be at least one unclaimable star in the Treasury’s asset.

## Recommendations
Make sure this behaviour is intended.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Urbit |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/urbit/stardust/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/urbit/stardust/review.pdf

### Keywords for Search

`vulnerability`


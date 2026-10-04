---
# Core Classification
protocol: vusd-stablecoin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61776
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/vusd-stablecoin/f4e8fad4-3c79-4e7b-b0f3-260ef5f0acf6/index.html
source_link: https://certificate.quantstamp.com/full/vusd-stablecoin/f4e8fad4-3c79-4e7b-b0f3-260ef5f0acf6/index.html
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 1.00
financial_impact: low

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Paul Clemson
  - Leonardo Passos
  - Tim Sigl
---

## Vulnerability Title

Unfair Token Redemptions when an Underlying Stablecoin Depegs

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> Planned to fix it in future release of treasury contract

**Description:** The protocol currently has no clear contingency plan on how it would handle the event where one of the stablecoins backing VUSD depegs. Currently, `redeem()` function allows the user to specify which token they wish to withdraw for their USDC, therefore in a depeg scenario holders of VUSD would race to withdraw their tokens for one of the whitelisted stablecoins that has not depegged, leaving the last users holding a token that is now only backed by the depegged stablecoin.

**Recommendation:** Consider having the `redeem()` function return to users a percentage share of the underlying treasury. This would mean that in the event of one of the whitelisted stablecoins depegging all users would be able to redeem their fair share of the treasury, rather than only rewarding the users who are fastest to withdraw.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Quantstamp |
| Protocol | vusd-stablecoin |
| Report Date | N/A |
| Finders | Paul Clemson, Leonardo Passos, Tim Sigl |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/vusd-stablecoin/f4e8fad4-3c79-4e7b-b0f3-260ef5f0acf6/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/vusd-stablecoin/f4e8fad4-3c79-4e7b-b0f3-260ef5f0acf6/index.html

### Keywords for Search

`vulnerability`


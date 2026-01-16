---
# Core Classification
protocol: Derive
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53726
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/derive/review-round2.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/derive/review-round2.pdf
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

Precision Loss in CashAsset.withdraw()

### Overview


The `CashAsset.withdraw()` function is not working properly and can cause unexpected errors when using certain stable assets with more than 18 decimal places. This is because the function rounds up the requested amount to the closest 18th decimal place, which can result in trying to withdraw more than what is available. The recommendation is to not round up the amounts and instead find a different way to handle leftover dust. The development team has acknowledged the issue but will not be fixing it as it is unlikely to have a significant impact on users.

### Original Finding Content

## Description

`CashAsset.withdraw()` appears to have some precision loss, which can lead to reverts when using stable assets with native decimals larger than 18 digits. The `withdraw()` function converts the requested `stableAmount` by calling `to18DecimalsRoundUp()` on it, which rounds up the result to the closest 18th decimal place in an attempt to clear any dust. This result is then passed to `_withdrawCashAmount()`, which converts that amount back to 18 decimals via `from18Decimals()` for withdrawal. As such, it will attempt to withdraw more than available assets, which will result in an unexpected revert.

## Recommendations

Do not round up the amounts before withdrawal; instead, use the actual amount and, if necessary, implement separate mechanisms to harvest any leftover dust.

## Resolution

The development team has acknowledged the finding with the following comment:

> "The likelihood of this having any effect (i.e. tokens with > 18dp) is near zero. In practice, the underlying token used for the CashAsset contract is USDC, which has 6 decimal places. Thus, we will not be fixing this issue. Even in the case where the underlying token is > 18dp, the effect to the user is minimal, as the rounding would be causing issues with the least significant digits."

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Derive |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/derive/review-round2.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/derive/review-round2.pdf

### Keywords for Search

`vulnerability`


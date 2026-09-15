---
# Core Classification
protocol: Fungify
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31822
audit_firm: ZachObront
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-fungify.md
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
  - Zach Obront
---

## Vulnerability Title

[M-09] `topUpInterestShortfall()` does not accrue interest on tokens

### Overview


The `topUpInterestShortfall()` function in the code does not properly accrue interest for certain tokens, causing potential issues. These issues include the `getAccountLiquidity()` function possibly not working correctly, inaccurate interest shortfall calculations, and using outdated exchange rates. The recommendation is to explicitly call `accrueInterest()` on both tokens when using `topUpInterestShortfall()`. This issue has been fixed in a recent code update.

### Original Finding Content

Similar to the above issue, the `topUpInterestShortfall()` function does not explicitly accrue interest for either the interest market token or the collateral token.

This leads to a number of possible problems:
- The call to `getAccountLiquidity()` can revert if the user is in shortfall before accrual but would be in good standing after.
- The call to `getAccountLiquidity()` can pass if accruing interest on a borrowed token would have pushed the user into a shortfall.
- The call to `getAccountLiquidity()` can return an inaccurate interest shortfall if the interest market has not been recently accrued.
- The `_adjustTopUpValues()` calculation will use out of date exchange rates for both tokens, skewing results.

**Recommendation**

Explicitly call `accrueInterest()` on both tokens when `topUpInterestShortfall()` is called.

**Review**

Fixed as recommended in [7e0ee60622ddcbf384657da480ef9c851f2adc11](https://github.com/fungify-dao/taki-contracts/pull/9/commits/7e0ee60622ddcbf384657da480ef9c851f2adc11).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ZachObront |
| Protocol | Fungify |
| Report Date | N/A |
| Finders | Zach Obront |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-fungify.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


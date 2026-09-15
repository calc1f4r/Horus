---
# Core Classification
protocol: AgoraStableSwap_2025-06-05
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63850
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/AgoraStableSwap-security-review_2025-06-05.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-01] Wrong price calculation with inverse base and negative interest rates

### Overview


This bug report discusses a problem with calculating the `token0OverToken1` value for tokens that gain value. The issue arises when using the `swapStorage.perSecondInterestRate` to adjust the base price of the asset, as it can result in a positive or negative value depending on the token order. This approach is flawed, as applying a negative interest rate to the inverse price does not give the correct result. The report recommends always using the price of the non-AUSD token as the base price to avoid this issue, and suggests enforcing AUSD as token0 in the code.

### Original Finding Content


## Severity

**Impact:** High

**Likelihood:** Low

## Description

To calculate `token0OverToken1` for tokens that accrue value, `swapStorage.perSecondInterestRate` is used to adjust the base price of the asset. Depending on the order of the tokens, this value can be positive or negative.

However, this approach is flawed, as applying a negative interest rate over the inverse price does not yield the correct result.

Consider the following example:
- XYZ is token0 (6 decimals).
- AUSD is token1 (6 decimals).
- XYZ price is $2 and its annual interest rate is 50%.
- token0OverToken1 is set to 0.5e18 (1/2 * 1e18) and annualizedInterestRate is set to -0.5e18 (negative 50% interest rate).
- After 1 year, XYZ price is $3, so token0OverToken1 should be ~0.33e18 (1/3 * 1e18).
- token0OverToken1 is calculated as 0.5e18 * (1 - 0.5) = 0.25e18, which is incorrect.

## Recommendations

Use always the price of the non-AUSD token as the base price and avoid using the inverse price, as this breaks the linear interest calculations. This will require that AUSD is always token0 in the pair. Note that given that the AUSD address has 8 leading zeros, inverting the order of the tokens will result in AUSD being token0 in most cases, but this is not guaranteed. So it should be required to enforce it explicitly in the code.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | AgoraStableSwap_2025-06-05 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/AgoraStableSwap-security-review_2025-06-05.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


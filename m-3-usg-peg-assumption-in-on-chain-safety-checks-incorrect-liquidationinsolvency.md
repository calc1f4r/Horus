---
# Core Classification
protocol: USG - Tangent
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63049
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1073
source_link: none
github_link: https://github.com/sherlock-audit/2025-08-usg-tangent-judging/issues/102

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
finders_count: 8
finders:
  - oxelmiguel
  - tobi0x18
  - X0sauce
  - Xmanuel
  - AMOW
---

## Vulnerability Title

M-3: USG peg assumption in on-chain safety checks incorrect liquidation/insolvency decisions when USG depegs

### Overview


The team has acknowledged an issue with the `MarketCore` code, which calculates health, LTV, and liquidation eligibility using collateral USD price but does not convert USG-denominated debt to USD. This means that if the USG token depegs, the safety checks can produce incorrect results and cause silent insolvency or unfair liquidations. The code does not properly compare the USD-valued collateral with the USG-denominated debt, assuming that 1 USG is equal to $1 on-chain. This can lead to operational risks and incorrect liquidations. The recommendation is to convert the debt to USD for safety checks.

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-08-usg-tangent-judging/issues/102 

This issue has been acknowledged by the team but won't be fixed at this time.

## Found by 
AMOW, BADROBINX, X0sauce, Xmanuel, covey0x07, oxelmiguel, sl1, tobi0x18

Summary
`MarketCore` computes health, LTV and liquidation eligibility using collateral USD price but does not convert USG-denominated debt to USD (it assumes 1 USG == $1), so a USG depeg causes incorrect safety checks that can produce silent insolvency or unfair liquidations.
The code compares USD-valued collateral (via a collateral oracle) against USG token units without converting the USG amount into USD using a USG price oracle. This is a unit mismatch: collateral is valued in USD, debt is denominated in USG, yet the comparison assumes 1 USG == $1 on-chain.

https://github.com/sherlock-audit/2025-08-usg-tangent/blob/main/tangent-contracts/src/USG/Market/abstract/Collateral.sol#L192

The function returns:
https://github.com/sherlock-audit/2025-08-usg-tangent/blob/main/tangent-contracts/src/USG/Market/abstract/Collateral.sol#L194
returns USD price (1e18), but `userDebt_` is raw USG token units; there is no multiplication by USG price to convert debt → USD.

Impacts
Silent insolvency
Incorrect liquidation / incentive mismatch
Operational risk due to off-chain keepers

Recommendation
Convert debt to USD for safety checks



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | USG - Tangent |
| Report Date | N/A |
| Finders | oxelmiguel, tobi0x18, X0sauce, Xmanuel, AMOW, BADROBINX, covey0x07, sl1 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-08-usg-tangent-judging/issues/102
- **Contest**: https://app.sherlock.xyz/audits/contests/1073

### Keywords for Search

`vulnerability`


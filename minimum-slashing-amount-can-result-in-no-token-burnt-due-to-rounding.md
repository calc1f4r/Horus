---
# Core Classification
protocol: EigenLayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53558
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
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

Minimum Slashing Amount Can Result In No Token Burnt Due To Rounding

### Overview

See description below for full details.

### Original Finding Content

## Description

When the `slashOperator()` function is called with a small `wadToSlash` value, such as `1`, rounding can result in no tokens being added to `burnableShares[strategy]`, even though the slashing still effectively takes place through reductions in the operator's maximum and encumbered magnitude. 

This occurs because the calculation of slashed tokens uses round-down division when converting from magnitude to shares, which can result in zero tokens being marked for burning in cases with small slashing amounts. While this does not negatively impact other stakers or operators, it means the token burning mechanism can be circumvented in certain cases, leaving tokens permanently locked in the contract rather than being burned as intended.

## Recommendations

Consider adding a note in the documentation that small slashing amounts may not result in actual token burns due to rounding, which will result in small amounts of tokens locked in the contract rather than fully burnable through the burn mechanism.

## Resolution

The Eigenlayer team has added a Natspec comment for the `slashOperator()` function to inform users of this particular edge case. This issue has been resolved in PR #1088.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | EigenLayer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf

### Keywords for Search

`vulnerability`


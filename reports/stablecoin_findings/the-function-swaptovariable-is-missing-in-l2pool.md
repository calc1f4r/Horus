---
# Core Classification
protocol: AAVE
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54233
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/2c5aba7f-d561-4b2b-bbcc-184095521c35
source_link: https://cdn.cantina.xyz/reports/cantina_competition_aave_may2024.pdf
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
  - ladboy233
---

## Vulnerability Title

The function swaptovariable() is missing in l2pool 

### Overview

See description below for full details.

### Original Finding Content

## L2Pool.swapToVariable Function Overview

## Context
`L2Pool.sol#L83-L89`

## Description
The function `swapToVariable()` allows a borrower to swap their debt between stable and variable modes.

According to the Aave documentation:
> Implementation-wise, this adds a `swapToVariable()` function in the Aave pool, allowing any address to swap any stable rate user to variable, without changing anything else in the position.

While the `Pool` contract implements the function `swapToVariable()`, the `L2Pool` contract does not implement this function, preventing any address from swapping any stable rate user to variable without changing anything else in the position.

## Impact
- **Notice**: Calldata optimized extension of the Pool contract allowing users to pass compact calldata representation to reduce transaction costs on rollups.

However, a user cannot reduce the transaction costs on rollups by calling `swapToVariableRate`.

## Recommendation
Add the `swapToVariable()` function to `L2Pool`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | AAVE |
| Report Date | N/A |
| Finders | ladboy233 |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_aave_may2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/2c5aba7f-d561-4b2b-bbcc-184095521c35

### Keywords for Search

`vulnerability`


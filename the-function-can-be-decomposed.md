---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28191
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Anchor%20Collateral%20stETH/README.md#1-the-function-can-be-decomposed
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
  - MixBytes
---

## Vulnerability Title

The function can be decomposed

### Overview

See description below for full details.

### Original Finding Content

##### Description
At the line
https://github.com/lidofinance/anchor-collateral-steth/blob/8d52ce72cb42d48dff1851222e3b624c941ddb30/contracts/RewardsLiquidator.vy#L262-L357
`liquidate()` function can be decomposed to three internal functions.
##### Recommendation
It is recommended to make three separate internal functions instead of one long function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Anchor%20Collateral%20stETH/README.md#1-the-function-can-be-decomposed
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


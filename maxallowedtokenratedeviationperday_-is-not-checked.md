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
solodit_id: 33856
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20on%20Optimism/README.md#6-maxallowedtokenratedeviationperday_-is-not-checked
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

`maxAllowedTokenRateDeviationPerDay_` is not checked

### Overview

See description below for full details.

### Original Finding Content

##### Description
`maxAllowedTokenRateDeviationPerDay_` cannot exceed the value of `BASIS_POINT_SCALE` https://github.com/lidofinance/lido-l2-with-steth/blob/792071cdeaf61de927cc144e8c1c02d5f5996a01/contracts/optimism/TokenRateOracle.sol#L74.

##### Recommendation
We recommend adding a check that `maxAllowedTokenRateDeviationPerDay_` is less than `BASIS_POINT_SCALE`.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20on%20Optimism/README.md#6-maxallowedtokenratedeviationperday_-is-not-checked
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


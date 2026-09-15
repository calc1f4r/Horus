---
# Core Classification
protocol: Basin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37887
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-08-basin
source_link: https://code4rena.com/reports/2024-08-basin
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
finders_count: 0
finders:
---

## Vulnerability Title

[03] Potential precision and stability issues with equal values for amplification parameter

### Overview

See description below for full details.

### Original Finding Content


In `Stable2` we have an amplification param `a` and amplification precision scaling parameter [A_PRECISION](https://github.com/code-423n4/2024-08-basin/blob/7e08ff591df0a2ade7d5618113dda2621cd899bc/src/functions/Stable2.sol#L38-L39). [a](https://github.com/code-423n4/2024-08-basin/blob/7e08ff591df0a2ade7d5618113dda2621cd899bc/src/functions/StableLUT/Stable2LUT1.sol#L19-L22) is supposed to be scaled by `A_PRECISION` to maintain precision in calculations, but currently, both values are set to `100`. The following results in having amplification factor equal to 1 and will result in an invariant, which looks more like uniswap constant product formula and swaps may be more exposed to slippage.

### Proof of Concept

The formula will have the following graph:
- **Yellow** is the formula in Basin Stable implementation
- **Pink** is Uniswap constant product formula
- **White** is Constant sum formula

*Note: to view the provided image, please see the original submission [here](https://github.com/code-423n4/2024-08-basin-findings/blob/main/data/Egis_Security-Q.md#qa-04-potential-precision-and-stability-issues-with-equal-values-for-amplification-parameter).*

### Recommended Mitigation Steps

Make `A` coefficient larger, or introduce a setter to dynamically adjust the value.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Basin |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-08-basin
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-08-basin

### Keywords for Search

`vulnerability`


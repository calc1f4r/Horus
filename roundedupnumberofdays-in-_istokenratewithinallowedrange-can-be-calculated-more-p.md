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
solodit_id: 33868
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20on%20Optimism/README.md#18-roundedupnumberofdays-in-_istokenratewithinallowedrange-can-be-calculated-more-precisely
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

`roundedUpNumberOfDays` in `_isTokenRateWithinAllowedRange()` can be calculated more precisely

### Overview

See description below for full details.

### Original Finding Content

##### Description
If `rateL1TimestampDiff` is divided by `ONE_DAY_SECONDS` without remainder, `roundedUpNumberOfDays` will be 1 more than it should be:
https://github.com/lidofinance/lido-l2-with-steth/blob/792071cdeaf61de927cc144e8c1c02d5f5996a01/contracts/optimism/TokenRateOracle.sol#L150

##### Recommendation
We recommend changing
```solidity=
uint256 roundedUpNumberOfDays = 
    rateL1TimestampDiff / ONE_DAY_SECONDS + 1;
```
to
```solidity=
uint256 roundedUpNumberOfDays = 
    (rateL1TimestampDiff + ONE_DAY_SECONDS - 1) / ONE_DAY_SECONDS;
```

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20on%20Optimism/README.md#18-roundedupnumberofdays-in-_istokenratewithinallowedrange-can-be-calculated-more-precisely
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


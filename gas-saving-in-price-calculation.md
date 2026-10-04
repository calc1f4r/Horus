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
solodit_id: 28449
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20Price%20Oracle/README.md#3-gas-saving-in-price-calculation
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

Gas saving in price calculation

### Overview

See description below for full details.

### Original Finding Content

##### Description
In the function for calculating price, you can save gas when calculating the variables `S_` and` c` in case if `i=1`, `j=0`, `N_COINS=2`:
https://github.com/lidofinance/curve-merkle-oracle/blob/ae093b308999a564ed3f23d52c6c5dce946dbfa7/contracts/StableSwapPriceHelper.vy#L63-L72

##### Recommendation
We recommendto calculate variables using following formula:
```vyper=
S_ = x
c = D * D / (x * N_COINS)
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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20Price%20Oracle/README.md#3-gas-saving-in-price-calculation
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


---
# Core Classification
protocol: Aftermath
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48143
audit_firm: OtterSec
contest_link: https://aftermath.finance/
source_link: https://aftermath.finance/
github_link: https://github.com/AftermathFinance/indices

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - OtterSec
  - Robert Chen
  - Ajay Kunapareddy
  - Sangsoo Kang
---

## Vulnerability Title

Incorrect Price Calculation

### Overview


The bug report is about a function called calc_spot_price_fixed, which is supposed to calculate the price of one type of coin in terms of another type of coin. However, it is currently calculating the price of the second coin in terms of the first coin. This is not the intended behavior and needs to be fixed. The fix has been implemented in a new version of the code. To fix this issue, the values of the coins need to be passed in a specific way.

### Original Finding Content

## Math Move

In `math.move`, `calc_oracle_price` and `calc_spot_price` are intended to calculate the price of BASE coin in terms of a QUOTE coin. The values of BASE coin are passed as values of in-coin, and values of QUOTE coin are passed as values of out-coin. 

However, `calc_spot_price_fixed` computes the price of the out-coin in terms of the in-coin, meaning that the price of the QUOTE coin is calculated in terms of the BASE coin.

## Remediation

Pass the values of BASE coin to out-coin and the values of QUOTE coin to in-coin.

## Patch

Fixed in `85927a3`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Aftermath |
| Report Date | N/A |
| Finders | OtterSec, Robert Chen, Ajay Kunapareddy, Sangsoo Kang |

### Source Links

- **Source**: https://aftermath.finance/
- **GitHub**: https://github.com/AftermathFinance/indices
- **Contest**: https://aftermath.finance/

### Keywords for Search

`vulnerability`


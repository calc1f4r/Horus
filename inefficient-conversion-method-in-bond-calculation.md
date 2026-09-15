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
solodit_id: 41223
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#1-inefficient-conversion-method-in-bond-calculation
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

Inefficient Conversion Method in Bond Calculation

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is identified within the [several](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/CSAccounting.sol#L535-L572) view functions of the contract `CSAccounting`. The function currently uses `WSTETH.getWstETHByStETH()` to convert stEth amount to shares. However, it would be more efficient to use `_sharesByEth()` instead of `WSTETH.getWstETHByStETH()` for the conversion process.

The issue is classified as **Low** severity because it does not impact the security or core functionality but could lead to inefficiencies.

##### Recommendation
We recommend replacing the use of `WSTETH.getWstETHByStETH()` with `_sharesByEth()` in the functions from the description to improve efficiency and consistency in bond calculations.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#1-inefficient-conversion-method-in-bond-calculation
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


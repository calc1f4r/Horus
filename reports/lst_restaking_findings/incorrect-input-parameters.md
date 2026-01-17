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
solodit_id: 28414
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20Price%20Feed/README.md#3-incorrect-input-parameters
github_link: none

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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Incorrect input parameters

### Overview


This bug report is related to the function for calculating price in the StEthPriceFeed.vy contract. The problem is that the relative difference `old` argument can be zero in this function. This can cause problems as it could lead to incorrect calculations. 

The recommendation is to add a simple check to ensure that the `old` argument is greater than zero. This check would be in the form of an assert statement that reads "assert old > 0, "oracle price not init". This will help ensure that the calculations are correct and that the code will not cause any issues.

### Original Finding Content

##### Description
In the function for calculating price, relative difference `old` argument can be zero:
https://github.com/lidofinance/steth-price-feed/blob/459495f07c97d04f6e3839e7a3b32acfcade22ad/contracts/StEthPriceFeed.vy#L58
##### Recommendation
We recommend to add simple check:
```python=
assert old > 0, "oracle price not init"
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20Price%20Feed/README.md#3-incorrect-input-parameters
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


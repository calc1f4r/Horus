---
# Core Classification
protocol: Aries Markets
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47309
audit_firm: OtterSec
contest_link: https://ariesmarkets.xyz/
source_link: https://ariesmarkets.xyz/
github_link: https://github.com/aries-markets/aries-markets

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
finders_count: 2
finders:
  - Robert Chen
  - Andreas Mantzoutas
---

## Vulnerability Title

Enhancing Pyth Price Validation

### Overview

See description below for full details.

### Original Finding Content

## Oracle Price Retrieval

The `oracle::get_pyth_price` function currently retrieves the latest price from the Pyth oracle without explicitly considering the confidence deviation. To enhance the reliability and accuracy of the prices obtained, it is advisable to validate that Pyth’s confidence deviation is less than 10% of the retrieved price. This validation can be incorporated directly within the `get_pyth_price` function to ensure that the price data used is within an acceptable range of certainty.

## Remediation

Add a validation in `get_pyth_price` to ensure that Pyth’s confidence deviation is less than 10% of the price retrieved.

© 2024 Otter Audits LLC. All Rights Reserved. 14/16

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Aries Markets |
| Report Date | N/A |
| Finders | Robert Chen, Andreas Mantzoutas |

### Source Links

- **Source**: https://ariesmarkets.xyz/
- **GitHub**: https://github.com/aries-markets/aries-markets
- **Contest**: https://ariesmarkets.xyz/

### Keywords for Search

`vulnerability`


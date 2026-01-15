---
# Core Classification
protocol: Elusiv
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48634
audit_firm: OtterSec
contest_link: https://elusiv.io/
source_link: https://elusiv.io/
github_link: github.com/elusiv-privacy/elusiv.

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
finders_count: 3
finders:
  - Harrison Green
  - Ajay Kunapareddy
  - OtterSec
---

## Vulnerability Title

Use Pyth Oracle Confidence Interval

### Overview

See description below for full details.

### Original Finding Content

## Elusiv Program and Pyth Oracles

The Elusiv program uses Pyth oracles to convert between USDC, USDT, and native SOL in order to compute fee amounts for SPL-token transfers. Currently, the code does not utilize the confidence metric in the Pyth oracle.

## Market Conditions and Rate Variance

In times of strange market conditions or potentially malicious activity, these rates may have a high variance and therefore a large confidence interval. Since token conversion only occurs to compute fixed computation fees (and not the actual value being transferred), the implication of using a bad exchange rate is minor.

## Remediation

It is recommended to utilize the confidence interval when computing the exchange rate. For example, by using the side of the rate that is beneficial for Elusiv such that computation fees are always covered.

© 2022 OtterSec LLC. All Rights Reserved. 
21 / 31

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Elusiv |
| Report Date | N/A |
| Finders | Harrison Green, Ajay Kunapareddy, OtterSec |

### Source Links

- **Source**: https://elusiv.io/
- **GitHub**: github.com/elusiv-privacy/elusiv.
- **Contest**: https://elusiv.io/

### Keywords for Search

`vulnerability`


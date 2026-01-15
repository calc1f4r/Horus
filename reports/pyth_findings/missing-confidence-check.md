---
# Core Classification
protocol: Scallop
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47947
audit_firm: OtterSec
contest_link: https://scallop.io/
source_link: https://scallop.io/
github_link: https://github.com/scallop-io/sui-lending-protocol

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
finders_count: 5
finders:
  - Akash Gurugunti
  - Ilardi Marco
  - Sangsoo Kang
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Missing Confidence Check

### Overview

See description below for full details.

### Original Finding Content

## Code Review Feedback

In `pyth_rule::set_price`, the confidence value returned from `get_pyth_price` is not validated. While there is a check to confirm the primary oracle’s price against at least half of the secondary oracles’ prices, it is advisable to verify that the confidence level is not excessively high.

## Remediation

Check that the returned value of confidence is not too high in `pyth_rule::set_price`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Scallop |
| Report Date | N/A |
| Finders | Akash Gurugunti, Ilardi Marco, Sangsoo Kang, Robert Chen, OtterSec |

### Source Links

- **Source**: https://scallop.io/
- **GitHub**: https://github.com/scallop-io/sui-lending-protocol
- **Contest**: https://scallop.io/

### Keywords for Search

`vulnerability`


---
# Core Classification
protocol: Exponent Generic Standard
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53218
audit_firm: OtterSec
contest_link: https://www.exponent.finance/income
source_link: https://www.exponent.finance/income
github_link: https://github.com/exponent-finance/exponent-core

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
  - Ajay Shankar Kunapareddy
  - Robert Chen
---

## Vulnerability Title

Missing Validation Logic

### Overview

See description below for full details.

### Original Finding Content

## Issues Identified

1. The `ModifyHook` instruction does not validate whether the `meta.interface_type` is set to `Fragmetric`, even though the hook being modified is intended only for the `Fragmetric` interface type.
2. In `Utils::get_index`, the `price.exponent` is utilized to scale the price and confidence interval. In the `InterfaceType::Pyth` case, it is assumed to always be negative. However, if `price.exponent` were unexpectedly positive, it would result in incorrect scaling.

## Remediation

1. Add a validation step to ensure that the `meta.interface_type` is `Fragmetric`.
2. Ensure that `price.exponent` is negative before processing to enforce expected behavior and mitigate unexpected scenarios.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Exponent Generic Standard |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen |

### Source Links

- **Source**: https://www.exponent.finance/income
- **GitHub**: https://github.com/exponent-finance/exponent-core
- **Contest**: https://www.exponent.finance/income

### Keywords for Search

`vulnerability`


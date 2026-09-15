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
solodit_id: 48487
audit_firm: OtterSec
contest_link: https://ariesmarkets.xyz/
source_link: https://ariesmarkets.xyz/
github_link: github.com/Aries-Markets/aries-markets.

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
  - Akash Gurugunti
  - Robert Chen
  - OtterSec
  - Shiva Shankar Genji
---

## Vulnerability Title

Improper Oracle Calculations

### Overview


The bug report states that there is an error in the Pyth price calculations in the oracle.move file. This file is written in the programming language RUST. The code is supposed to divide the price by the magnitude, but it is currently doing the opposite. Additionally, the code will also produce an error if the magnitude is negative. The solution to this bug is to multiply the price by the magnitude instead of dividing it. This issue has been resolved in the patch 2a62fc8.

### Original Finding Content

## Pyth Price Calculations Issue

Pyth price calculations in `oracle.move` are performed incorrectly.

## Location
- File: `oracle/sources/oracle.move` 
- Language: RUST

## Code Snippet
```rust
pyth_price = option::some(decimal::div(
    decimal::from_u64(pyth::i64::get_magnitude_if_positive(&pyth::price::get_price(&
    decimal::from_u128(math128::pow(10,
    (pyth::i64::get_magnitude_if_positive(&pyth::price::get_expo(&price))
    as u128)))
))
```

## Problem
The price should be multiplied by, not divided by, the magnitude. This code also errors if the magnitude is negative.

## Remediation
Multiply by the magnitude.

## Patch
Resolved in commit `2a62fc8`.

---

© 2022 OtterSec LLC. All Rights Reserved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Aries Markets |
| Report Date | N/A |
| Finders | Akash Gurugunti, Robert Chen, OtterSec, Shiva Shankar Genji |

### Source Links

- **Source**: https://ariesmarkets.xyz/
- **GitHub**: github.com/Aries-Markets/aries-markets.
- **Contest**: https://ariesmarkets.xyz/

### Keywords for Search

`vulnerability`


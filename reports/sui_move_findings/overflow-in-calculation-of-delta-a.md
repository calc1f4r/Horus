---
# Core Classification
protocol: Cetus
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48430
audit_firm: OtterSec
contest_link: https://www.cetus.zone/
source_link: https://www.cetus.zone/
github_link: github.com/CetusProtocol/cetus-clmm.

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
finders_count: 3
finders:
  - Michal Bochnak
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Overflow In Calculation Of Delta A

### Overview


The bug report states that the value of the numerator is not being checked before a calculation is performed on it. This can result in the removal of non-zero bytes, leading to an incorrect calculation. A proof of concept is provided, showing the incorrect calculation of the value. To fix this issue, the usage of u256::shlw should be replaced with u256::checked_shlw. This has been fixed in a recent patch.

### Original Finding Content

## Vulnerability Report

## Description
The `numberator` value is not validated before running `u256::shlw` on it. As a result, the non-zero bytes might be removed, which leads to an incorrect calculation of the value.

```rust
let numberator = u256::shlw(full_math_u128::full_mul(liquidity, sqrt_price_diff));
```

## Proof of Concept
```rust
get_delta_a(tick_math::max_sqrt_price(), tick_math::min_sqrt_price(), 
    56315830353026631512438212669420532741, true);
```

### Result
```rust
numberator: [debug] 0x1::u256::U256 {
    n0: 535693272949614043,
    n1: 11711318139720635722,
    n2: 15182355392690797918,
    n3: 710792351
}

numberator >> 64: [debug] 0x1::u256::U256 {
    n0: 0,
    n1: 535693272949614043,
    n2: 11711318139720635722,
    n3: 15182355392690797918
}
```

## Remediation
Replace `u256::shlw` usage with `u256::checked_shlw`.

### Code Changes
```rust
- let numberator = u256::shlw(full_math_u128::full_mul(liquidity, 
    sqrt_price_diff));
+ let (numberator, overflow) = u256::checked_shlw(full_math_u128::full_mul(liquidity, 
    sqrt_price_diff));
+ if (overflow) {
+     abort ERROR;
+ }
```

## Patch
Fixed in commit `f6a3888`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Cetus |
| Report Date | N/A |
| Finders | Michal Bochnak, Robert Chen, OtterSec |

### Source Links

- **Source**: https://www.cetus.zone/
- **GitHub**: github.com/CetusProtocol/cetus-clmm.
- **Contest**: https://www.cetus.zone/

### Keywords for Search

`vulnerability`


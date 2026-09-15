---
# Core Classification
protocol: Solend Steamm
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53243
audit_firm: OtterSec
contest_link: https://save.finance/
source_link: https://save.finance/
github_link: https://github.com/solendprotocol/steamm

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
  - Michał Bochnak
  - Robert Chen
  - Sangsoo Kang
---

## Vulnerability Title

Overestimation of Tokens Resulting in Oversupply

### Overview

See description below for full details.

### Original Finding Content

## Pool Math: Token Deposit Calculation

`pool_math::tokens_to_deposit` attempts to calculate the optimal deposit amounts `a_star` (for token A) and `b_star` (for token B) based on the current reserve ratios while adhering to user-specified maximum constraints `max_a` and `max_b`. However, the approach may overestimate the required tokens under certain conditions.

### Code Snippet
```rust
fun tokens_to_deposit(reserve_a: u64, reserve_b: u64, max_a: u64, max_b: u64): (u64, u64) {
    assert!(max_a > 0, EDepositMaxAParamCantBeZero);
    if (reserve_a == 0 && reserve_b == 0) {
        (max_a, max_b)
    } else {
        let b_star = safe_mul_div_up(max_a, reserve_b, reserve_a);
        if (b_star <= max_b) { 
            (max_a, b_star) 
        } else {
            let a_star = safe_mul_div_up(max_b, reserve_a, reserve_b);
            assert!(a_star > 0, EDepositRatioLeadsToZeroA);
            assert!(a_star <= max_a, EDepositRatioInvalid);
            (a_star, max_b)
        }
    }
}
```

### Important Observations
When calculating `b_star`, if `max_a * reserve_b` is not divisible by `reserve_a`, the returned values may include a dust amount. This implies that users may inadvertently attempt to supply more tokens than necessary to maintain the correct reserve balance.

### Remediation
Calculate the liquidity based on both `max_a` and `max_b`, considering the pool’s current reserve ratio, and then back-calculate the corresponding `a_star` and `b_star`.

### Patch
Acknowledged by the Solend development team.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Solend Steamm |
| Report Date | N/A |
| Finders | Michał Bochnak, Robert Chen, Sangsoo Kang |

### Source Links

- **Source**: https://save.finance/
- **GitHub**: https://github.com/solendprotocol/steamm
- **Contest**: https://save.finance/

### Keywords for Search

`vulnerability`


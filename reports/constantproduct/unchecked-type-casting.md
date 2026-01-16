---
# Core Classification
protocol: Raydium AMM V3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48449
audit_firm: OtterSec
contest_link: https://raydium.io/
source_link: https://raydium.io/
github_link: github.com/raydium-io/raydium-amm-v3.

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
finders_count: 5
finders:
  - Michal Bochnak
  - Maher Azzouzi
  - Robert Chen
  - OtterSec
  - William Wang
---

## Vulnerability Title

Unchecked Type Casting

### Overview


The bug report highlights an issue in the get_delta_amount_0_signed function where there are unchecked conversions from u64 to i64. This can lead to faulty conversions if the u64 value is larger than what i64 can represent. The same issue also applies to the get_delta_amount_1_signed function. A proof of concept test case has been provided to demonstrate how this could be exploited against the burn liquidity instruction. The suggested solution is to use i64::try_from instead of an unchecked cast. This issue has been fixed in patch #27.

### Original Finding Content

## Audit Report: get_delta_amount_0_signed Function

In the `get_delta_amount_0_signed` function, there are unchecked conversions from `u64` (which `get_delta_amount_0_unsigned` returns) to `i64`. The issue is that the value of the `u64` returned by `get_delta_amount_0_unsigned` might be larger than what `i64` can represent, which would result in a faulty conversion.

### Code Snippet
```rust
pub fn get_delta_amount_0_signed(
    sqrt_ratio_a_x64: u128,
    sqrt_ratio_b_x64: u128,
    liquidity: i128,
) -> i64 {
    if liquidity < 0 {
        -(get_delta_amount_0_unsigned(
            sqrt_ratio_a_x64,
            sqrt_ratio_b_x64,
            -liquidity as u128,
            false,
        ) as i64)
    } else {
        // TODO check overflow, since i64::MAX < u64::MAX
        get_delta_amount_0_unsigned(sqrt_ratio_a_x64, sqrt_ratio_b_x64,
            liquidity as u128, true) as i64
    }
}
```

The same applies for `get_delta_amount_1_signed`. 

We prepared a simple proof of concept test case demonstrating that this could be exploited against the burn liquidity instruction.

### Test Case
```bash
amount_0: 11760396439755885211, amount_1: 33593848103203582
real profit = amount_0 - (amount_0_add * 40) = 253215768394719371
test
instructions::decrease_liquidity::burn_liquidity_test::burn_liquidity_test_overf
... ok
```

## Vulnerability Summary
**Raydium AMM v3 Audit 04 | Vulnerabilities**

### Remediation
A possible method of remediation is using `i64::try_from` instead of an unchecked cast.

### Patch
Fixed in #27.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Raydium AMM V3 |
| Report Date | N/A |
| Finders | Michal Bochnak, Maher Azzouzi, Robert Chen, OtterSec, William Wang |

### Source Links

- **Source**: https://raydium.io/
- **GitHub**: github.com/raydium-io/raydium-amm-v3.
- **Contest**: https://raydium.io/

### Keywords for Search

`vulnerability`


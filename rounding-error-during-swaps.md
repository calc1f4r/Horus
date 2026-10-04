---
# Core Classification
protocol: Sanctum
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47587
audit_firm: OtterSec
contest_link: https://www.sanctum.so/
source_link: https://www.sanctum.so/
github_link: https://github.com/igneous-labs/S/tree/ottersec-231220

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
finders_count: 4
finders:
  - OtterSec
  - Robert Chen
  - Tamta Topuria
  - Thibault Marboud
---

## Vulnerability Title

Rounding Error During Swaps

### Overview


The bug report describes a rounding issue in the swap_exact_in function during a cross-program invocation call. This rounding behavior can result in users receiving one more lamport than they should, which can affect the resulting dst_lst amount in a token swap. This issue only becomes exploitable if the flat-fee program is configured with zero fees. The fix for this bug is to round down the result of U64RatioFloor:reverse in the instructions. This issue has been addressed in the latest patch.

### Original Finding Content

## Swap Exact In and Rounding Behavior

Within `swap_exact_in` during the cross-program invocation call to `sol_to_lst`, `U64RatioFloor:reverse` rounds up the resulting value. This rounding behavior may allow users to receive one more lamport than they should. In the context of a token swap, this rounding behavior may result in a situation where the resulting `dst_lst` amount is slightly higher than it would be with rounding down. 

It should be noted that this issue becomes exploitable only if the flat-fee program is configured with zero fees since, due to the absence of fees, the exact amount of tokens received becomes critical for users looking to maximize their gains.

## Code Example

```rust
// s-src/processor/swap_exact_in.rs
pub fn process_swap_exact_in(accounts: &[AccountInfo], args: SwapExactInIxArgs) -> ProgramResult {
    [...]
    let out_sol_value = pricing_cpi.invoke_price_exact_in(PricingProgramIxArgs {
        amount,
        sol_value: in_sol_value,
    })?;
    let dst_lst_out = dst_lst_cpi.invoke_sol_to_lst(out_sol_value)?.min;
    [...]
}
```

## Remediation

Round down the result of `U64RatioFloor:reverse` in the instructions.

## Patch

Fixed in `87832e3`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Sanctum |
| Report Date | N/A |
| Finders | OtterSec, Robert Chen, Tamta Topuria, Thibault Marboud |

### Source Links

- **Source**: https://www.sanctum.so/
- **GitHub**: https://github.com/igneous-labs/S/tree/ottersec-231220
- **Contest**: https://www.sanctum.so/

### Keywords for Search

`vulnerability`


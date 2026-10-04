---
# Core Classification
protocol: Adrena
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46785
audit_firm: OtterSec
contest_link: https://www.adrena.xyz/
source_link: https://www.adrena.xyz/
github_link: https://github.com/AdrenaDEX/adrena

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
finders_count: 2
finders:
  - Robert Chen
  - Tamta Topuria
---

## Vulnerability Title

Deduction Of Swap From Liquidity Pool

### Overview


The report describes a bug in the swap instruction code, where the fees are not being subtracted from the user's input before calculating the output token amount. As a result, the user is receiving the full value of their input tokens without the fees being deducted. This leads to an imbalance where the pool loses value over time due to continuously paying out fees from its own funds. The suggested solution is to ensure that the fees are deducted from the user's input before converting to output tokens and transferring to the user. The bug has been resolved in the latest patch.

### Original Finding Content

## Swap Instruction Overview

In the swap instruction, `amount_out` is calculated utilizing the entire `params.amount_in` value, which represents the total number of input tokens provided by the user. The fees are calculated based on the `params.amount_in` and `amount_out` values. However, these fees are not subtracted from the user’s input before calculating the `amount_out`. As a result, the user receives the full value of their input tokens converted to the output tokens without the fees being subtracted upfront.

> _Instructions: public/liquidity/swap.rs_

```rust
pub fn swap(ctx: Context<Swap>, params: &SwapParams) -> Result<()> {
    [...]
    let fees_in_amount = match is_internal_swap {
        true => 0,
        false => pool.get_swap_in_fees(
            token_id_in,
            params.amount_in,
            &receiving_custody,
            &received_token_price_high,
            &dispensing_custody,
        )?,
    };
    [...]
}
```

Nevertheless, the swap instructions still calculate the fee amount and subsequently distribute the fees after the amount is transferred to the user, implying that the fees are taken from the pool’s funds rather than from the user’s input. This effectively means that the user is not bearing the cost of the fees. Over time, as more swaps are executed, the pool's value diminishes because it continuously pays out fees from its own funds. This gradual depletion results in an imbalance where the pool loses value, affecting the liquidity providers.

## Remediation

Ensure the swap instruction calculates and deducts the fee amount from `amount_in` before converting to `amount_out` tokens and transferring to the user.

## Patch

Resolved in `47271d5`

© 2024 Otter Audits LLC. All Rights Reserved. 10/59

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Adrena |
| Report Date | N/A |
| Finders | Robert Chen, Tamta Topuria |

### Source Links

- **Source**: https://www.adrena.xyz/
- **GitHub**: https://github.com/AdrenaDEX/adrena
- **Contest**: https://www.adrena.xyz/

### Keywords for Search

`vulnerability`


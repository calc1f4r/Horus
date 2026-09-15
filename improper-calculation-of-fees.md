---
# Core Classification
protocol: LayerZero V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47232
audit_firm: OtterSec
contest_link: https://layerzero.network/
source_link: https://layerzero.network/
github_link: https://github.com/LayerZero-Labs/monorepo

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
  - Jessica Clendinen
---

## Vulnerability Title

Improper Calculation Of Fees

### Overview


The bug report describes an issue with the function "calculate_pre_fee_amount" in the program "mod.rs" which is written in the Rust programming language. The function is used to calculate the pre-fee amount for a transaction, but it consistently returns zero when the transfer fee is set to 100%. This is problematic because the correct pre-fee amount should take into account the fact that the entire post-fee amount will be consumed by the fee. The report suggests a fix that has been implemented in a patch.

### Original Finding Content

## Issue with calculate_pre_fee_amount Function

The function `calculate_pre_fee_amount` invokes `get_pre_fee_amount_ld`. However, there is an issue within `calculate_pre_fee_amount` when `transfer_fee_basis_points` is equal to `MAX_FEE_BASIS_POINTS`, which represents a 100% fee. In such a case, the function consistently returns zero as the pre-fee amount.

> _program-2022/src/extension/transfer_fee/mod.rs_

```rust
pub fn calculate_pre_fee_amount(&self, post_fee_amount: u64) -> Option<u64> {
    let maximum_fee = u64::from(self.maximum_fee);
    let transfer_fee_basis_points = u16::from(self.transfer_fee_basis_points) as u128;
    if transfer_fee_basis_points == 0 {
        Some(post_fee_amount)
    } else if transfer_fee_basis_points == ONE_IN_BASIS_POINTS || post_fee_amount == 0 {
        Some(0)
    } [...]
}
```

This is problematic because, under a 100% fee rate, the correct pre-fee amount should account for the fact that the entire post-fee amount would be consumed up by the fee.

## Remediation

Back-port to PR #6704, which fixes this issue by returning the pre-fee amount as `post_fee_amount + maximum_fee`, when `transfer_fee_basis_points == MAX_FEE_BASIS_POINTS`.

## Patch

Fixed in `555f16`.

© 2024 Otter Audits LLC. All Rights Reserved. 6/16

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | LayerZero V2 |
| Report Date | N/A |
| Finders | Robert Chen, Jessica Clendinen |

### Source Links

- **Source**: https://layerzero.network/
- **GitHub**: https://github.com/LayerZero-Labs/monorepo
- **Contest**: https://layerzero.network/

### Keywords for Search

`vulnerability`


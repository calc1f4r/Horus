---
# Core Classification
protocol: Meso Lending
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47131
audit_firm: OtterSec
contest_link: https://meso.finance/
source_link: https://meso.finance/
github_link: https://github.com/MesoLendingFi/meso-smartcontract

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
  - Andreas Mantzoutas
---

## Vulnerability Title

Utilization Of Unsuitable Rounding Direction

### Overview


This bug report highlights a potential issue in the lending_pool system where incorrect rounding may result in a loss of funds for users. The problem occurs when converting assets into shares, as the rounding direction used may lead to a discrepancy between the two. This can result in users owing more assets than their shares represent, leading to them earning funds for free. The issue has been addressed in recent patches, which ensure proper rounding direction is used in share calculations.

### Original Finding Content

## Loss of Funds Scenario in Lending Pool

There is a possibility of a loss of funds scenario in `lending_pool` due to the incorrect rounding direction in the share calculations during borrowing and withdrawing, resulting in inaccurate conversion between the amount of assets and the corresponding shares. 

When users borrow or withdraw assets, the system converts these amounts into shares based on the pool’s current state in `calculate_shares`.

> **Code Snippet:**
> 
> ```rust
> fun calculate_shares(amount: u128, total_shares: u128, total: u128): u128 {
>     if (total_shares > 0) {
>         math128::mul_div(amount, total_shares, total)
>     } else {
>         amount
>     }
> }
> ```

However, the rounding direction in the share calculations may result in a discrepancy between the assets and shares. When `calculate_shares` performs a floor rounding (rounding down) in share calculations in `borrow_internal` and `withdraw`, the user may end up with fewer debt shares than they are entitled to, resulting in them owing more assets than the value represented by their shares. As a result, users will effectively earn funds for free because they are receiving fewer debt shares for their borrowings. The pool’s total debt increases without the user receiving proportional debt shares.

## Remediation

Ensure that the share calculations utilize proper rounding direction.

## Patch

Fixed in `030d9cb` and `01beccb`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Meso Lending |
| Report Date | N/A |
| Finders | Robert Chen, Andreas Mantzoutas |

### Source Links

- **Source**: https://meso.finance/
- **GitHub**: https://github.com/MesoLendingFi/meso-smartcontract
- **Contest**: https://meso.finance/

### Keywords for Search

`vulnerability`


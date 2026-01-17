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
solodit_id: 46793
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

Reduced Borrow Fee due to Resetting of Accrued Interest

### Overview


The vulnerability involves an issue with how the cumulative_interest_snapshot field is reset when increasing the position in the increase_position_long and increase_position_short instructions. This field reflects the total interest accumulated on the position over time and is used to calculate the interest fee. However, when increasing a position, the current cumulative_interest_snapshot is set to the most recent value, essentially discarding any previous interest accumulated. This allows attackers to exploit the situation by avoiding paying the interest that has accrued since the position was created. The solution is to avoid resetting the cumulative_interest_snapshot when increasing the position and instead calculate the total interest based on the full history of the position. The issue has been resolved in version 5546c35.

### Original Finding Content

## Vulnerability in Cumulative Interest Snapshot

The vulnerability involves an issue with how the `cumulative_interest_snapshot` field is reset when increasing the position in the `increase_position_long` and `increase_position_short` instructions. The cumulative interest reflects the total interest accumulated on the position over time. It is utilized to calculate the interest fee (`borrow_fee_usd`), which is applied when the position is closed or liquidated.

When increasing a position, the current `cumulative_interest_snapshot` is set to the most recent cumulative interest at that moment. This implies the interest accumulated up to the point of the increase is essentially discarded.

## Code Example

```rust
> _position/increase_position_short.rs_
pub fn increase_position_short(
    ctx: Context<IncreasePositionShort>,
    params: &IncreasePositionShortParams,
) -> Result<()> {
    [...]
    position.cumulative_interest_snapshot =
        U128Split::from(collateral_custody.get_cumulative_interest(current_time)?);
    [...]
}
```

If the position had been open for a while before it was increased, there would have been interest accrued during that period. However, when the `cumulative_interest_snapshot` is reset, this old interest is omitted from the calculation for the borrow fee. Since interest from the initial period is not considered when calculating the borrow fee for the position, the borrower does not pay for the interest accumulated before the position increases. An attacker can exploit this situation by timing the increase of the position in such a way that they avoid paying the interest that has accrued since the position’s creation, allowing users to avoid paying substantial fees on the borrowed amount.

## Remediation

Avoid resetting the `cumulative_interest_snapshot` when increasing the position; the protocol should calculate the total interest based on the full history of the position, including the period before the increase.

## Patch

Resolved in 5546c35

© 2024 Otter Audits LLC. All Rights Reserved. 23/59

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


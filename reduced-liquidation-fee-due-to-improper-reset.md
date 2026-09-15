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
solodit_id: 46794
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

Reduced Liquidation Fee due to Improper Reset

### Overview


This bug report discusses an issue where the liquidation fee for a position is not properly calculated when the position size is increased. This can be exploited by attackers who make a small incremental increase to their position before closing or liquidating it, resulting in a significantly smaller fee than it should be. The suggested solution is to update the liquidation fee to reflect the combined effect of the original and incremental position sizes. This issue has been resolved in a patch. 

### Original Finding Content

## Liquidation Fee Calculation in Position Size Increase

When the position size is increased in `increase_position_long` and `increase_position_short` instructions, the `position.liquidation_fee_usd` field is recalculated proportionally to the increment, essentially discarding the previously accumulated liquidation fee. This implies that even a very large position may have a liquidation fee close to zero if the position is slightly increased just before closing it.

## Code Snippet
```rust
pub fn increase_position_short(
    ctx: Context<IncreasePositionShort>,
    params: &IncreasePositionShortParams,
) -> Result<()> {
    [...]
    {
        position.update_time = current_time;
        [...]
        position.liquidation_fee_usd = liquidation_fee_usd;
    }
    [...]
}
```

Thus, an attacker holding a large position may exploit this by making a small incremental increase to their position just before closing or liquidating it. Since the liquidation fee is reset during the increase and recalculated based only on the small increment, the overall fee becomes significantly smaller than it should be for the full position.

## Remediation
Preserve and update the liquidation fee when the position increases to reflect the combined effect of the original and incremental position sizes.

## Patch
Resolved in commit `57416be`.

© 2024 Otter Audits LLC. All Rights Reserved. 24/59

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


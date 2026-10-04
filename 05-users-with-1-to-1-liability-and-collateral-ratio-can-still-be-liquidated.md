---
# Core Classification
protocol: Blend
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62084
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-02-blend-v2-audit-certora-formal-verification
source_link: https://code4rena.com/reports/2025-02-blend-v2-audit-certora-formal-verification
github_link: none

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
finders_count: 0
finders:
---

## Vulnerability Title

[05] Users with 1 to 1 liability and collateral ratio can still be liquidated

### Overview

See description below for full details.

### Original Finding Content


<https://github.com/code-423n4/2025-02-blend/blob/f23b3260763488f365ef6a95bfb139c95b0ed0f9/blend-contracts-v2/pool/src/auctions/user_liquidation_auction.rs# L50-L53>

### Finding description and impact

In `create_user_liq_auction_data`, it’s intended that a user has less collateral than liabilities before he can be liquidated. However, due to incorrect check, a user could have same liability as collateral (technically not being at a loss), but still be liquidated. This is because the function reverts only if `liability_base` is < `collateral_base`. If they’re equal, a user can unfairly liquidated.
```

    // ensure the user has less collateral than liabilities
>   if position_data.liability_base < position_data.collateral_base {
        panic_with_error!(e, PoolError::InvalidLiquidation);
    }
```

### Recommended mitigation steps

Update the function to use `<=` operator instead.

**Comments from the Script3 team:**

> This was addressed [here](https://github.com/blend-capital/blend-contracts-v2/commit/96fac37e96b11dc76f005a5053236c89e30acb29) to block user liquidations when liabilities equal collateral.

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Blend |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2025-02-blend-v2-audit-certora-formal-verification
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2025-02-blend-v2-audit-certora-formal-verification

### Keywords for Search

`vulnerability`


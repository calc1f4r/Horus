---
# Core Classification
protocol: Starknet Perpetual
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57700
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-03-starknet-perpetual
source_link: https://code4rena.com/reports/2025-03-starknet-perpetual
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

[L-02] Error in Using the same max funding rate for all synthetic ASSETS.

### Overview

See description below for full details.

### Original Finding Content


<https://github.com/starkware-libs/starknet-perpetual/blob/9e48514c6151a9b65ee23b4a6f9bced8c6f2b793/workspace/apps/perpetuals/contracts/src/core/types/funding.cairo# L93-L117>

Some assets move wildly (DOGE, PEPE), others are relatively stable (ETH, BTC), and some are nearly flat (e.g. real-world assets or stablecoin synths).

If you set `max_funding_rate` too high:

* Low-volatility assets will allow unrealistic funding jumps.
* Could lead to price manipulation or unexpected liquidations.

If you set it too low:

* High-volatility assets like DOGE or SOL won’t allow fast-enough funding corrections.
* Traders can exploit the spread without paying the proper funding cost.

Example:

You set `max_funding_rate` = 1e-6 per second.

For ETH it might be okay.

But for DOGE, if longs heavily outweigh shorts during a 30-minute rally, funding can’t rise fast enough → short traders take losses, system gets imbalance exposure.
```

/// Validates the funding rate by ensuring that the index difference is bounded by the max funding
/// rate.
///
/// The max funding rate represents the rate of change **per second**, so it is multiplied by
/// `time_diff`.
/// Additionally, since the index includes the synthetic price,
/// the formula also multiplies by `synthetic_price`.
///
/// Formula:
/// `index_diff <= max_funding_rate * time_diff * synthetic_price`
pub fn validate_funding_rate(
    synthetic_id: AssetId,
    // index_diff scale is the same as the `FUNDING_SCALE` (2^32).
    index_diff: u64,
    // max_funding_rate scale is the same as the `FUNDING_SCALE` (2^32).
    max_funding_rate: u32,
    time_diff: u64,
    synthetic_price: Price,
) {
    assert_with_byte_array(
@here         condition: index_diff.into() <= synthetic_price.mul(rhs: max_funding_rate)
            * time_diff.into(),
        err: invalid_funding_rate_err(:synthetic_id),
    );
}
```

When funding isn’t tuned per asset:

* The protocol either over-penalizes or under-collects.
* It breaks the balance between long/short incentives.
* And it can lead to bad liquidations

### Recommendation

Use per-asset `max_funding_rate`, and not a single one for all synthetic assets.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Starknet Perpetual |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2025-03-starknet-perpetual
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2025-03-starknet-perpetual

### Keywords for Search

`vulnerability`


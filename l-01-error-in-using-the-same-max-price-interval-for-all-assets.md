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
solodit_id: 57699
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

[L-01] Error in Using the same max Price interval for all ASSETS.

### Overview

See description below for full details.

### Original Finding Content


Most tokens have different heart beats , with meme coins been highly volatile and other token like stable coin also. The code incorrectly assign a single value to track all asset price staleness.

<https://github.com/starkware-libs/starknet-perpetual/blob/9e48514c6151a9b65ee23b4a6f9bced8c6f2b793/workspace/apps/perpetuals/contracts/src/core/components/assets/assets.cairo# L579>

<https://github.com/starkware-libs/starknet-perpetual/blob/9e48514c6151a9b65ee23b4a6f9bced8c6f2b793/workspace/apps/perpetuals/contracts/src/core/components/assets/assets.cairo# L764-L777>
```

    fn _validate_synthetic_prices(
            self: @ComponentState<TContractState>,
            current_time: Timestamp,
            max_price_interval: TimeDelta,
        ) {
            for (synthetic_id, synthetic_timely_data) in self.synthetic_timely_data {
                // Validate only active asset
                if self._get_synthetic_config(:synthetic_id).status == AssetStatus::ACTIVE {
                    assert(
@here                        max_price_interval >= current_time
                            .sub(synthetic_timely_data.last_price_update),
                        SYNTHETIC_EXPIRED_PRICE,
                    );
                }
            };
```

This will allow for some tokens with smaller intervals as per the oracle design to return stale prices or revert when prices are still fresh for the other.

### Recommendation

Consider configuring `max_price_interval` for each synthetic asset individually.



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


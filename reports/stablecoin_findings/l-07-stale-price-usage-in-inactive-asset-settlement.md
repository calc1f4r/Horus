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
solodit_id: 57705
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-03-starknet-perpetual
source_link: https://code4rena.com/reports/2025-03-starknet-perpetual
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 1.00
financial_impact: low

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-07] Stale Price Usage in Inactive Asset Settlement

### Overview

See description below for full details.

### Original Finding Content


<https://github.com/starkware-libs/starknet-perpetual/blob/9e48514c6151a9b65ee23b4a6f9bced8c6f2b793/workspace/apps/perpetuals/contracts/src/core/core.cairo# L913-L914>
```

        fn reduce_inactive_asset_position(
            ref self: ContractState,
            operator_nonce: u64,
            position_id_a: PositionId,
            position_id_b: PositionId,
            base_asset_id: AssetId,
            base_amount_a: i64,
        ) {
            /// Validations:
            self.pausable.assert_not_paused();
            self.operator_nonce.use_checked_nonce(:operator_nonce);
            self.assets.validate_assets_integrity();

            let position_a = self.positions.get_position_snapshot(position_id: position_id_a);
            let position_b = self.positions.get_position_snapshot(position_id: position_id_b);

            // Validate base asset is inactive synthetic.
            if let Option::Some(config) = self.assets.synthetic_config.read(base_asset_id) {
                assert(config.status == AssetStatus::INACTIVE, SYNTHETIC_IS_ACTIVE);
            } else {
                panic_with_felt252(NOT_SYNTHETIC);
            }
            let base_balance: Balance = base_amount_a.into();
            let quote_amount_a: i64 = -1
                * self
                    .assets
@here                     .get_synthetic_price(synthetic_id: base_asset_id)
                    .mul(rhs: base_balance)
                    .try_into()
                    .expect('QUOTE_AMOUNT_OVERFLOW');
            self
```

The `reduce_inactive_asset_position` function allows settlement involving inactive synthetic assets.

However, it uses `get_synthetic_price` without validating the freshness of the price. Since inactive assets cannot have their prices updated (`_set_price` rejects them), these prices can become stale and inaccurate over time.

### Recommendation

Allow Admin Price Updates for Inactive Assets:

* Introduce a governor-only function to manually update prices for inactive assets.

Add Price Freshness Check:

* Validate timestamp of inactive asset prices before using them in settlements.

Allow Operator-Provided Prices (With Constraints):

* Let trusted operators provide recent price inputs during settlement, verified off-chain and within tolerances to prevent abuse.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
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


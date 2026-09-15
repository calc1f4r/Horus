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
solodit_id: 57704
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

[L-06] Unnecessary Active Asset Checks Block Inactive Position Resolution

### Overview

See description below for full details.

### Original Finding Content


<https://github.com/starkware-libs/starknet-perpetual/blob/9e48514c6151a9b65ee23b4a6f9bced8c6f2b793/workspace/apps/perpetuals/contracts/src/core/core.cairo# L898>

<https://github.com/starkware-libs/starknet-perpetual/blob/9e48514c6151a9b65ee23b4a6f9bced8c6f2b793/workspace/apps/perpetuals/contracts/src/core/components/assets/assets.cairo# L575-L588>

The `reduce_inactive_asset_position` function unnecessarily validates all ACTIVE synthetic assets via `validate_assets_integrity()`, even though it only involves an INACTIVE asset.
```

   /// - Adjust collateral balances based on `quote_amount`.
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

@here             self.assets.validate_assets_integrity();

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
```

This causes unrelated checks (e.g., funding/price freshness) to fail and block the operation.
```

self.assets.validate_assets_integrity(); // Triggers global funding/price checks
```

This introduces a Denial of Service (DoS) risk:

Valid inactive asset operations can fail due to stale data in unrelated active assets, preventing clean-up or resolution of deprecated positions.

### Recommendation

Update the flow to skip global validations when reducing inactive positions.

This ensures inactive asset operations remain available, reducing protocol fragility and preserving solvency mechanisms.



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


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
solodit_id: 57706
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

[L-08] Collateral Transfers and Withdrawals Blocked by Irrelevant Synthetic Asset Validations

### Overview

See description below for full details.

### Original Finding Content


<https://github.com/starkware-libs/starknet-perpetual/blob/9e48514c6151a9b65ee23b4a6f9bced8c6f2b793/workspace/apps/perpetuals/contracts/src/core/core.cairo# L405>

<https://github.com/starkware-libs/starknet-perpetual/blob/9e48514c6151a9b65ee23b4a6f9bced8c6f2b793/workspace/apps/perpetuals/contracts/src/core/core.cairo# L293>

The transfer and withdraw functions always call `validate_assets_integrity()`, which enforces synthetic asset funding and price freshness checks. While this is critical for users with active synthetic positions, it introduces unintended friction for users who only hold collateral.
```

   fn withdraw(
            ref self: ContractState,
            operator_nonce: u64,
            recipient: ContractAddress,
            position_id: PositionId,
            amount: u64,
            expiration: Timestamp,
            salt: felt252,
        ) {
            self.pausable.assert_not_paused();
            self.operator_nonce.use_checked_nonce(:operator_nonce);

@here             self.assets.validate_assets_integrity();
```


```

        fn transfer(
            ref self: ContractState,
            operator_nonce: u64,
            recipient: PositionId,
            position_id: PositionId,
            amount: u64,
            expiration: Timestamp,
            salt: felt252,
        ) {
            self.pausable.assert_not_paused();
            self.operator_nonce.use_checked_nonce(:operator_nonce);

@here             self.assets.validate_assets_integrity();
```

Users with no synthetic exposure may be blocked from transferring or withdrawing collateral if synthetic prices are stale or funding has expired.

This is because `validate_assets_integrity()` is executed unconditionally, regardless of the user’s asset holdings.

### Recommendation

Conditionally execute synthetic validation only if the user has an active synthetic position:
```

let position = self.positions.get_position_snapshot(position_id);
if position.has_synthetic_assets() {
    self.assets.validate_assets_integrity();
}
```

This ensures:

* Correct behavior for users actively trading synthetic assets.
* Uninterrupted access for users managing only collateral.
* Reduced system fragility and better user experience across edge cases.

---



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


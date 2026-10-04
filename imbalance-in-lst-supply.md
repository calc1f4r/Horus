---
# Core Classification
protocol: Solend
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46870
audit_firm: OtterSec
contest_link: https://save.finance/
source_link: https://save.finance/
github_link: https://github.com/solendprotocol/liquid-staking

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
finders_count: 2
finders:
  - Michał Bochnak
  - Robert Chen
---

## Vulnerability Title

Imbalance in LST Supply

### Overview

See description below for full details.

### Original Finding Content

## Issue Report: Validation of Relationship in `create_lst_with_stake`

Currently, the `create_lst_with_stake` function does not validate the relationship between the SUI, `fungible_staked_sui`, and `lst_treasury_cap.total_supply` values. The function only ensures that `lst_treasury_cap.total_supply` and the total staked SUI in the system are greater than zero.

```rust
// contracts/sources/liquid_staking.move
public fun create_lst_with_stake<P: drop>(
    system_state: &mut SuiSystemState,
    fee_config: FeeConfig,
    lst_treasury_cap: TreasuryCap<P>,
    mut fungible_staked_suis: vector<FungibleStakedSui>,
    sui: Coin<SUI>,
    ctx: &mut TxContext
) -> (AdminCap<P>, LiquidStakingInfo<P>) {
    [...]
    vector::destroy_empty(fungible_staked_suis);
    storage.join_to_sui_pool(sui.into_balance());
    assert!(lst_treasury_cap.total_supply() > 0 && storage.total_sui_supply() > 0,
            EInvalidLstCreation);
    
    create_lst_with_storage(
        fee_config,
        lst_treasury_cap,
        storage,
        ctx
    )
}
```

The LST created should ideally represent a proportional claim on the underlying staked SUI assets. If there is no relationship between the total LST supply and the staked SUI, users may receive LST tokens that over- or under-represent the actual value of the staked assets. The misalignment between LST and staked SUI may result in incorrect pricing when users interact with the liquid staking system.

## Remediation

Implement a check that will validate whether the amounts are reasonable.

## Patch

Resolved in commit `288ce2a`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Solend |
| Report Date | N/A |
| Finders | Michał Bochnak, Robert Chen |

### Source Links

- **Source**: https://save.finance/
- **GitHub**: https://github.com/solendprotocol/liquid-staking
- **Contest**: https://save.finance/

### Keywords for Search

`vulnerability`


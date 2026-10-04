---
# Core Classification
protocol: Fluid Protocol (Hydrogen Labs)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46893
audit_firm: OtterSec
contest_link: https://fluidprotocol.xyz/
source_link: https://fluidprotocol.xyz/
github_link: https://github.com/Hydrogen-Labs/fluid-protocol

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - James Wang
  - Alpha Toure
  - Renato Eugenio Maria Marziano
---

## Vulnerability Title

Imprecise Reward Distribution Calculation

### Overview


This bug report is about an issue in a program called trove-manager. The problem is with a function called internal_redistribute_debt_and_coll, which is used to calculate rewards for users. The issue is that the total_stakes variable, which is used in the calculation, does not take into account pending rewards that have not yet been given to users. This means that rewards may be distributed inaccurately, with some users getting less than they should and others getting more. The report suggests that the program should be changed to include pending rewards in the calculation. The bug has been fixed in a recent update.

### Original Finding Content

## Issue in `internal_redistribute_debt_and_coll` within `trove-manager`

The issue in `internal_redistribute_debt_and_coll` within `trove-manager`, where `total_stakes` is utilized as the denominator for calculating `asset_reward_per_unit_staked`, arises because `total_stakes` represents the sum of all the stakes in the system. However, it does not account for pending rewards that may not yet be applied to individual troves. This creates a semantic imprecision in the reward distribution.

## Code Snippet

```sway
>_ libraries/src/oracle_interface.sw sway
fn internal_redistribute_debt_and_coll(debt: u64, coll: u64) {
    let asset_contract_cache = storage.asset_contract.read();
    if (debt == 0) {
        return;
    }
    let asset_numerator: U128 = U128::from_u64(coll) * U128::from_u64(DECIMAL_PRECISION) +
        U128::from_u64(storage.last_asset_error_redistribution.read());
    let usdf_numerator: U128 = U128::from_u64(debt) * U128::from_u64(DECIMAL_PRECISION) +
        U128::from_u64(storage.last_usdf_error_redistribution.read());
    let asset_reward_per_unit_staked = asset_numerator /
        U128::from_u64(storage.total_stakes.read());
    [...]
}
```

If pending rewards are not considered, the `asset_reward_per_unit_staked` and `usdf_reward_per_unit_staked` values will be inaccurately distributed. Thus, troves that have not yet applied their rewards may get less than they are owed, while troves with all rewards applied may receive more than their fair share. Additionally, the `total_stakes_snapshot` and `total_collateral_snapshot` variables remain unutilized or unchanged throughout the `trove-manager` contract and may be removed.

## Remediation

Ensure that the denominator in the reward calculation accounts for both the active stakes and the pending rewards.

## Patch

Resolved in f8006a0.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Fluid Protocol (Hydrogen Labs) |
| Report Date | N/A |
| Finders | James Wang, Alpha Toure, Renato Eugenio Maria Marziano |

### Source Links

- **Source**: https://fluidprotocol.xyz/
- **GitHub**: https://github.com/Hydrogen-Labs/fluid-protocol
- **Contest**: https://fluidprotocol.xyz/

### Keywords for Search

`vulnerability`


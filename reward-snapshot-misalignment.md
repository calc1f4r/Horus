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
solodit_id: 46886
audit_firm: OtterSec
contest_link: https://fluidprotocol.xyz/
source_link: https://fluidprotocol.xyz/
github_link: https://github.com/Hydrogen-Labs/fluid-protocol

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
finders_count: 3
finders:
  - James Wang
  - Alpha Toure
  - Renato Eugenio Maria Marziano
---

## Vulnerability Title

Reward Snapshot Misalignment

### Overview


This bug report discusses an issue in the trove-manager program where partial liquidation of a trove does not update the borrower's reward snapshot, leading to incorrect reward calculations in the future. The report suggests updating the snapshot immediately after partial liquidation and utilizing a specific variable during liquidation calculations. The issue has been resolved in a recent patch.

### Original Finding Content

## Partial Liquidation and Reward Snapshot Update in Trove Manager

In `internal_apply_liquidation` within `trove-manager`, when a trove is partially liquidated, it is important to update the borrower’s reward snapshot (the record of pending collateral and debt rewards). This is because the liquidation process calculates and accounts for the rewards that have accrued up to the moment of liquidation.

## Code Snippet

```sway
fn internal_apply_liquidation(
    borrower: Identity,
    liquidation_values: LiquidationValues,
    upper_partial_hint: Identity,
    lower_partial_hint: Identity,
) {
    let asset_contract_cache = storage.asset_contract.read();
    // partial liquidation reinserted into sorted troves
    if (liquidation_values.is_partial_liquidation) {
        let mut trove = storage.troves.get(borrower).read();
        [...]
    }
    [...]
}
```

The snapshot stores values representing the borrower’s position at a particular point in time. After liquidation, the borrower’s new trove position (with updated collateral and debt) should reflect a fresh starting point for accumulating future rewards. Failing to update the snapshot after a partial liquidation may result in double-counting rewards or incorrect reward calculations in the future because the borrower’s old snapshot would still reflect the pre-liquidation state.

Additionally, in `internal_get_totals_from_batch_liquidate`, `usdf_in_stability_pool` is utilized, and as a result, the function will always refer to the initial amount of USDF, ignoring the fact that some USDF has already been utilized.

## Remediation

Update the reward snapshot for the borrower immediately after the partial liquidation in `internal_apply_liquidation`, and utilize `vars.remaining_usdf_in_stability_pool` during liquidation calculations in `internal_get_totals_from_batch_liquidate`.

## Patch

Resolved in a9279b2.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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


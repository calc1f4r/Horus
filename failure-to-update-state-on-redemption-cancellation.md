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
solodit_id: 46887
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

Failure to Update State on Redemption Cancellation

### Overview


The internal_redeem_collateral_from_trove function in the trove-manager-contract fails to update the stakes and reinsert the trove into the sorted list when a redemption is cancelled due to the new debt falling below a minimum limit. This results in inconsistencies in the contract's state. The issue has been resolved in two patches, which track a compounded value for stake instead of collateral and consider pending rewards in the calculation of the nominal collateralization ratio.

### Original Finding Content

## Issue with `internal_redeem_collateral_from_trove`

`internal_redeem_collateral_from_trove` fails to update the stakes and reinsert the trove into the sorted list when the redemption is canceled. The cancellation condition occurs when the new debt after redemption falls below a predefined minimum debt limit (`MIN_NET_DEBT`). In such cases, the function sets the `cancelled_partial` flag to `true` and returns early without applying the redemption changes.

> _trove-manager-contract/src/main.sw sway_
>
> #[storage(read, write)]
> fn internal_redeem_collateral_from_trove(
> [...]
> ) -> SingleRedemptionValues {
> [...]
> else {
> // Calculate the new nominal collateralization ratio
> let new_nicr = fm_compute_nominal_cr(new_coll, new_debt);
> // If the new debt is below the minimum allowed, cancel the partial redemption
> if (new_debt < MIN_NET_DEBT) {
> single_redemption_values.cancelled_partial = true;
> return single_redemption_values;
> }
> [...]
> }
> [...]
> }

Since these values would have been altered during `apply_pending_rewards`, failing to update the stakes and reinsert the trove into the sorted list will result in inconsistencies in the state of the contract.

## Remediation

Track a compounded value as stake instead of collateral directly. This eliminates the need to update stake when distributing rewards. Also, consider pending rewards in NICR calculation to remove the need for reordering troves on reward distribution.

## Patch

Resolved in `f8006a0` and `89ba7f0`.

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


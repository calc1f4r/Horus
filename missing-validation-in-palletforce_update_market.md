---
# Core Classification
protocol: Parallel Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18225
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/ParallelFinance.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/ParallelFinance.pdf
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
finders_count: 1
finders:
  - Artur Cygan Will Song Fredrik Dahlgren
---

## Vulnerability Title

Missing validation in Pallet::force_update_market

### Overview

See description below for full details.

### Original Finding Content

## Data Validation Assessment

**Difficulty:** High  
**Type:** Data Validation  
**Target:** pallets/loans/src/lib.rs  

## Description

The `Pallet::force_update_market` method can be used to replace the stored market instance for a given asset. Other methods used to update market parameters perform extensive validation of the market parameters, but `force_update_market` checks only the rate model.

```rust
pub fn force_update_market(
    origin: OriginFor<T>,
    asset_id: AssetIdOf<T>,
    market: Market<BalanceOf<T>>,
) -> DispatchResultWithPostInfo {
    T::UpdateOrigin::ensure_origin(origin)?;
    ensure!(
        market.rate_model.check_model(),
        Error::<T>::InvalidRateModelParam
    );
    let updated_market = Self::mutate_market(asset_id, |stored_market| {
        *stored_market = market;
        stored_market.clone()
    })?;
    Self::deposit_event(Event::<T>::UpdatedMarket(updated_market));
    Ok(().into())
}
```

*Figure 3.1: pallets/loans/src/lib.rs:539-556*

This means that the caller (who is either the root account or half of the general council) could inadvertently change immutable market parameters like `ptoken_id` by mistake.

## Exploit Scenario

The root account calls `force_update_market` to update a set of market parameters. By mistake, the `ptoken_id` market parameter is updated, which means that `Pallet::ptoken_id` and `Pallet::underlying_id` are no longer inverses.

## Recommendations

Short term, consider adding more input validation to the `force_update_market` extrinsic. In particular, it may make sense to ensure that the `ptoken_id` market parameter has not changed. Alternatively, add validation to check whether the `ptoken_id` market parameter is updated and to update the `UnderlyingAssetId` map to ensure that the value matches the `Markets` storage map.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Parallel Finance |
| Report Date | N/A |
| Finders | Artur Cygan Will Song Fredrik Dahlgren |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/ParallelFinance.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/ParallelFinance.pdf

### Keywords for Search

`vulnerability`


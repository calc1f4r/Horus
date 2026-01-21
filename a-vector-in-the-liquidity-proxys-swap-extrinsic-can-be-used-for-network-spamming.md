---
# Core Classification
protocol: Polkaswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48901
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2021-08-soramitsu-polkaswap-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2021-08-soramitsu-polkaswap-securityreview.pdf
github_link: none

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
finders_count: 2
finders:
  - Dominik Czarnota
  - Artur Cygan
---

## Vulnerability Title

A vector in the liquidity-proxy’s swap extrinsic can be used for network spamming

### Overview


The bug report discusses a high difficulty issue in the sora2-substrate/pallets/liquidity-proxy/src/lib.rs file, specifically in the swap extrinsic. The problem is that there are not enough limits set on the selected_source_types vector, which can lead to duplicate entries and an excessively long vector. This vulnerability can be exploited by an attacker to spam the network with swap transactions, causing a denial of service. The report recommends implementing data validation for the vector and accounting for its length in calculations, as well as adding tests to prevent duplicate sources and excessive vector lengths in the future.

### Original Finding Content

## Type: Denial of Service
**Target:** sora2-substrate/pallets/liquidity-proxy/src/lib.rs

**Difficulty:** High

## Description
There are insufficient limits on `selected_source_types`, which is a vector in the liquidity-proxy pallet's swap extrinsic. Specifically, the vector can contain duplicate entries, and there is no check preventing it from becoming too long. Additionally, the vector’s length is not factored into calculations of the extrinsic's base weight (figure 18.1). These deficiencies leave the system vulnerable to the following scenarios:

1. An attacker could provide a very long `selected_source_types` vector to spam the network with swap transactions at a relatively low cost, which could lead to a denial of service.
2. An attacker could perform swaps via calls to the `generic_split` method, passing in the same source multiple times. This method is called in the `quote_single` function (figure 18.2), which is called by the swap extrinsic’s `Self::exchange` function. This transaction on the sora-staging test network shows a relatively limited instance of spamming.

```rust
#[pallet::weight(<T as Config>::WeightInfo::swap((*swap_amount).into()))]
pub fn swap (
    origin: OriginFor<T>,
    dex_id: T::DEXId,
    input_asset_id: T::AssetId,
    output_asset_id: T::AssetId,
    swap_amount: SwapAmount<Balance>,
    selected_source_types: Vec<LiquiditySourceType>,
    filter_mode: FilterMode,
) -> DispatchResultWithPostInfo {
    let who = ensure_signed(origin)?;
    if Self::is_forbidden_filter(
        &input_asset_id,
        &output_asset_id,
        &selected_source_types,
        &filter_mode,
    ) {
        fail!(Error::<T>::ForbiddenFilter);
    }
    let outcome = Self::exchange(
        &who,
        &who,
        &input_asset_id,
        &output_asset_id,
        swap_amount,
        LiquiditySourceFilter::with_mode(dex_id, filter_mode, selected_source_types),
    )?;
    // (...)
}
```
**Figure 18.1:** The swap extrinsic (`sora2-substrate/pallets/liquidity-proxy/src/lib.rs#L1575-L1625`)

```rust
fn quote_single ( /* (...) */ ) -> /* (...) */ {
    let sources =
        T::LiquidityRegistry::list_liquidity_sources(input_asset_id, output_asset_id, filter)?;
    ensure!(!sources.is_empty(), Error::<T>::UnavailableExchangePath);
  
    // Check if we have exactly one source => no split required
    if sources.len() == 1 { /* (...) */ }
  
    // Check if we have exactly two sources: the primary market and the secondary market
    // Do the "smart" swap split (with fallback)
    if sources.len() == 2 { /* (...) */ }
  
    // Otherwise, fall back to the general source-agnostic procedure based on sampling
    Self::generic_split(sources, input_asset_id, output_asset_id, amount, skip_info)
}
```
**Figure 18.2:** The `quote_single` function, called through the `Self::exchange` call in the swap extrinsic (`sora2-substrate/pallets/liquidity-proxy/src/lib.rs#L544-L598`)

## Exploit Scenario
An attacker sends numerous batch transactions that make many calls to the liquidity-proxy pallet's swap extrinsic, each with a very long `selected_source_types` vector. In this way, the attacker forces the SORA Network to spend a very long time processing swap transactions, causing a denial of service.

## Recommendations
**Short term:** Implement appropriate data validation for the `selected_source_types` vector in the liquidity-proxy pallet's swap extrinsic. Ensure that the network rejects calls if the vector is too long or if it contains duplicates. Additionally, consider accounting for the vector’s length in calculations of the extrinsic’s base weight.

**Long term:** Add tests to the liquidity-proxy pallet's swap extrinsic to ensure that it properly validates the `selected_source_types` vector and disallows duplicate sources and excessive vector lengths.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Polkaswap |
| Report Date | N/A |
| Finders | Dominik Czarnota, Artur Cygan |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2021-08-soramitsu-polkaswap-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2021-08-soramitsu-polkaswap-securityreview.pdf

### Keywords for Search

`vulnerability`


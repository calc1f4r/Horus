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
solodit_id: 57698
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-03-starknet-perpetual
source_link: https://code4rena.com/reports/2025-03-starknet-perpetual
github_link: https://code4rena.com/audits/2025-03-starknet-perpetual/submissions/F-34

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
finders_count: 7
finders:
  - kanra
  - dystopia
  - montecristo
  - SBSecurity
  - m4k2
---

## Vulnerability Title

[M-03] Stale prices can cause inaccurate validation of funding ticks in `funding_tick()`

### Overview


Summary:

The bug report addresses an issue with the `assets.funding_tick()` function in the Starknet Perpetual contracts. This function updates the funding index for active synthetic assets, but it does not properly validate the price of the assets, which can result in the use of stale prices. This can lead to incorrect validation of funding rate changes, and in some cases, erroneous updates to collateral balances of positions. The recommended mitigation step is to validate the price is up to date upon retrieving it through `get_synthetic_price()`.

### Original Finding Content



<https://github.com/code-423n4/2025-03-starknet/blob/512889bd5956243c00fc3291a69c3479008a1c8a/workspace/apps/perpetuals/contracts/src/core/components/assets/assets.cairo# L288-L323>

<https://github.com/code-423n4/2025-03-starknet/blob/512889bd5956243c00fc3291a69c3479008a1c8a/workspace/apps/perpetuals/contracts/src/core/components/assets/assets.cairo# L633-L649>

<https://github.com/code-423n4/2025-03-starknet/blob/512889bd5956243c00fc3291a69c3479008a1c8a/workspace/apps/perpetuals/contracts/src/core/components/assets/assets.cairo# L508-L516>

<https://github.com/code-423n4/2025-03-starknet/blob/512889bd5956243c00fc3291a69c3479008a1c8a/workspace/apps/perpetuals/contracts/src/core/types/funding.cairo# L103-L117>

<https://github.com/code-423n4/2025-03-starknet/blob/512889bd5956243c00fc3291a69c3479008a1c8a/workspace/apps/perpetuals/contracts/src/core/components/positions/positions.cairo# L445-L448>

<https://github.com/code-423n4/2025-03-starknet/blob/512889bd5956243c00fc3291a69c3479008a1c8a/workspace/apps/perpetuals/contracts/src/core/components/positions/positions.cairo# L534-L544>

### Finding description and impact

The function `assets.funding_tick()` updates the funding index for all active synthetic assets. This helps ensure that long and short positions are economically balanced over time. The function can be called only by the operator and takes as an input the parameter `funding_ticks` which is a list of `FundingTick` structs, each specifying an `asset_id` and its new `funding_index`. The number of `funding_ticks` provided matches the number of active synthetic assets and each active asset receives a funding tick update. For every funding tick in `funding_ticks`, the function `assets.

`_process_funding_tick()` is executed with the new funding tick for the asset and the storage read `max_funding_rate` where downstream the function `funding.validate_funding_rate()` is executed. This function validates that the change in the old and new funding index doesn’t violate the `max_funding_rate`, however, the function relies on the price of the synthetic asset fetched through `get_synthetic_price()`.

However, `get_synthetic_price()` retrieves the asset price from `self.synthetic_timely_data` but does not check if the price is up to date. This can result in the use of stale prices, which can cause incorrect validation of the funding rate. As a result, invalid funding rate changes might incorrectly pass validation, or valid funding rate updates could be wrongly rejected. The more severe case is invalid funding rate changes passing validation since the funding tick directly affects the collateral balance of positions and can lead to erroneously updated balances - modification to the collateral balance based on the funding index happens in `positions.

`_update_synthetic_balance_and_funding()` and the funding index is also considered in health validations that use `positions.get_collateral_provisional_balance()`.

### Recommended mitigation steps

Validate that the price is up to date upon retrieving the price through `get_synthetic_price()`. A call to `assets.validate_assets_integrity()` would not work properly since the function also performs a check whether the funding indexes are up to date, however, `funding_tick()` must be successful when the funding indexes are out of date.

**[oded (Starknet Perpetual) confirmed](https://code4rena.com/audits/2025-03-starknet-perpetual/submissions/F-34?commentParent=CayE5S3L8hJ)**

Code4rena judging staff adjusted the severity of Finding [M-01], after reviewing additional context provided by the sponsor.

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Starknet Perpetual |
| Report Date | N/A |
| Finders | kanra, dystopia, montecristo, SBSecurity, m4k2, 0xNirix, alexxander |

### Source Links

- **Source**: https://code4rena.com/reports/2025-03-starknet-perpetual
- **GitHub**: https://code4rena.com/audits/2025-03-starknet-perpetual/submissions/F-34
- **Contest**: https://code4rena.com/reports/2025-03-starknet-perpetual

### Keywords for Search

`vulnerability`


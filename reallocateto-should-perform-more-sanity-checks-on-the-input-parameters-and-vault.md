---
# Core Classification
protocol: Morpho
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40734
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/84fb1c99-31ff-4327-9fd4-eeee6cf59ef9
source_link: https://cdn.cantina.xyz/reports/cantina_morpho_public_allocator_feb2024.pdf
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

protocol_categories:
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Jonah Wu
  - StErMi
---

## Vulnerability Title

reallocateTo should perform more sanity checks on the input parameters and vault 's con- ﬁguration 

### Overview

See description below for full details.

### Original Finding Content

## Context: PublicAllocator.sol#L102-L148

## Description
The current implementation of `reallocateTo` should revert if the function's input parameters "do not make sense" or if they are incompatible with the current configuration and state of the MetaMorpho vaults that will execute the reallocate flow.

Some of these checks will be done automatically by the `reallocate` function, but we suggest replicating them also in `reallocateTo` to prevent any external caller from reaching the MetaMorpho vault when the constructed allocations won't contribute to a valid or meaningful execution of the logic.

These checks will improve the overall security of the vault but will also prevent the user from losing money (the fee itself) when the result of `reallocate` is a no-op (no withdrawal and no supply have happened).

## Additional Checks
Here are the list of additional checks that should be implemented by `reallocateTo`:

1. **withdrawals.length > 0**: If there are no withdrawals from any market, it means that there won't be any supply. `vault.reallocate` won't revert, but `EventsLib.PublicReallocateTo` will be emitted, and the caller will waste their `msg.value` for nothing.
   
2. **withdrawnAssets > 0**: Having only a non-withdrawal won't automatically bring up the scenario described in point (1), but it's fair to say that it's a meaningless operation that should be prevented. If this is the only withdrawal operation, it will lead to the same consequences as point (1).

3. **totalWithdrawn > 0**: Same consequences as point (1).

4. **IMetaMorpho(vault).config(id).enabled == true**: The market from which the vault is going to withdraw assets must have been enabled (added to the withdrawal queue).

5. Given `marketCap = IMetaMorpho(vault).config(supplyMarketParams.id()).cap` and `currentMarketSuppliedAssets = amount_of_assets_already_supplied_to_supplyMarketParams`:
   - **marketCap > 0**
   - **currentMarketSuppliedAssets + totalWithdrawn <= marketCap**

## Recommendation
Morpho should implement the above suggested checks to allow the execution of `vault.reallocate(...)` only if the `reallocateTo` input parameter values are valid and compatible with the state and configuration of the vaults for the markets involved in the supply and withdraw operations.

## Morpho
Addressed in PR 28.

## Cantina Managed
Part of the recommendations have been implemented in PR 28. The `reallocateTo` function will revert when:

- The supply market is not enabled.
- The withdraw market is not enabled.
- The user has specified an empty array of markets to withdraw from.
- The user tries to withdraw an empty amount of assets from a market.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | Jonah Wu, StErMi |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_morpho_public_allocator_feb2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/84fb1c99-31ff-4327-9fd4-eeee6cf59ef9

### Keywords for Search

`vulnerability`


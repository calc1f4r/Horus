---
# Core Classification
protocol: LMCV part 2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50697
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/damfinance/lmcv-part-2-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/damfinance/lmcv-part-2-smart-contract-security-assessment
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
  - Halborn
---

## Vulnerability Title

MISSING DATA VALIDATION

### Overview

See description below for full details.

### Original Finding Content

##### Description

Configuration values in the contracts are not validated; it is possible to set large and/or invalid values, causing contracts to fail.

Code Location
-------------

[`OSM.sol,` #99](https://github.com/DecentralizedAssetManagement/lmcv/blob/f5861988508a5bb291a3a7f2863693cd9762dee7/contracts/lmcv/OSM.sol#L99)

The `pokeTimeout` has no maximum value and can be set to a very large value, making calling `poke` impossible in a reasonable time.

[`RatesUpdater.sol,` #103](https://github.com/DecentralizedAssetManagement/lmcv/blob/f5861988508a5bb291a3a7f2863693cd9762dee7/contracts/lmcv/RatesUpdater.sol#L103)

The value of `stabilityRate` is not validated. When stability rate is set to an invalid value (not per the second rate), for example, percentage: 1.05, calls to `accrueInterest` will revert during rate calculation in the `_rpow` function.

`AuctionHouse.sol`, #[96](https://github.com/DecentralizedAssetManagement/lmcv/blob/f5861988508a5bb291a3a7f2863693cd9762dee7/contracts/lmcv/AuctionHouse.sol#L96), [100](https://github.com/DecentralizedAssetManagement/lmcv/blob/f5861988508a5bb291a3a7f2863693cd9762dee7/contracts/lmcv/AuctionHouse.sol#L100), [104](https://github.com/DecentralizedAssetManagement/lmcv/blob/f5861988508a5bb291a3a7f2863693cd9762dee7/contracts/lmcv/AuctionHouse.sol#L104), [108](https://github.com/DecentralizedAssetManagement/lmcv/blob/f5861988508a5bb291a3a7f2863693cd9762dee7/contracts/lmcv/AuctionHouse.sol#L108)

Bid/auction expirity do not have maximum value.
The `minimumBidIncrease` and `minimumBidDecrease` do not have max/min values. Setting `minimumBidDecrease` >= 1.0 will cause users to be able to bid any value.

`Liquidator.sol`, #[129](https://github.com/DecentralizedAssetManagement/lmcv/blob/f5861988508a5bb291a3a7f2863693cd9762dee7/contracts/lmcv/Liquidator.sol#L129), [133](https://github.com/DecentralizedAssetManagement/lmcv/blob/f5861988508a5bb291a3a7f2863693cd9762dee7/contracts/lmcv/Liquidator.sol#L133)

The `lotSize` variable can be set to `0`, causing the `liquidate` function to fail each time because of the `require` statement:

#### lmcv/Liquidator.sol

```
function liquidate(address user) external {
    require(live == 1, "Liquidator/Not live");
    require(liquidationPenalty != 0 && lotSize != 0, "Liquidator/Not set up");
    require(!lmcv.isWithinCreditLimit(user, lmcv.AccumulatedRate()), "Liquidator/Vault within credit limit");
[...]

```

##### Score

Impact: 2  
Likelihood: 2

##### Recommendation

**PARTIALLY SOLVED**: The `lotSize` validation was added in the [Liquidator.sol](https://github.com/DecentralizedAssetManagement/lmcv/blob/a4b1e5cf9d68e0f2392ac26e3867dda166e70020/contracts/lmcv/Liquidator.sol#L155) contract.
However, the `\client team` decided to leave other variables without validation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | LMCV part 2 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/damfinance/lmcv-part-2-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/damfinance/lmcv-part-2-smart-contract-security-assessment

### Keywords for Search

`vulnerability`


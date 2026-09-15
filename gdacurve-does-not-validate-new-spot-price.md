---
# Core Classification
protocol: Sudoswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18416
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-01-Sudoswap.md
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

protocol_categories:
  - dexes
  - services
  - liquidity_manager
  - nft_lending
  - payments

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Hans
  - Alex Roan
  - 0kage
  - Giovanni Di Siena
---

## Vulnerability Title

GDACurve does not validate new spot price

### Overview


This bug report is about the new spot price calculated in `GDACurve::getBuyInfo` and `GDACurve::getSellInfo` not being validated against `MIN_PRICE` (currently set to a constant value, `1 gwei`). This means that the spot price could fall below this value in certain scenarios with high `lambda`, low initial price, and low demand. 

The impact of this bug is that market-making for some pools can happen at extremely low prices in perpetuity. To mitigate this, a minimum price validation should be introduced in `GDACurve::getBuyInfo` and `GDACurve::getSellInfo` when the spot price is updated. This was fixed in the commit c4dc61 and verified.

### Original Finding Content

**Description:**
The new spot price calculated in `GDACurve::getBuyInfo` and `GDACurve::getSellInfo` is not currently validated against `MIN_PRICE`, meaning that the price could fall below this value.

```solidity
GDACurve.sol (Line 81-91)

        // The new spot price is multiplied by alpha^n and divided by the time decay so future
        // calculations do not need to track number of items sold or the initial time/price. This new spot price
        // implicitly stores the initial price, total items sold so far, and time elapsed since the start.
        {
            UD60x18 newSpotPrice_ = spotPrice_.mul(alphaPowN);
            newSpotPrice_ = newSpotPrice_.div(decayFactor);
            if (newSpotPrice_.gt(ud(type(uint128).max))) {
                return (Error.SPOT_PRICE_OVERFLOW, 0, 0, 0, 0, 0);
            } //@audit-info Missing minimum price check
            newSpotPrice = uint128(unwrap(newSpotPrice_));
        }
```

While a minimum price check is performed explicitly in `GDACurve::validateSpotPrice`, the same validation is missing when the price gets updated.

```solidity
GDACurve.sol (Line 34-36)

    function validateSpotPrice(uint128 newSpotPrice) external pure override returns (bool) {
        return newSpotPrice >= MIN_PRICE;
    }
```

Since the maximum value of the decay factor is capped at a significantly large value (2^20), in scenarios with high `lambda`, low initial price, and low demand (i.e. extended time intervals between successive purchases), there is a likelihood that spot price can drop below `MIN_PRICE` level (currently set to a constant value, `1 gwei`).

**Impact**
In most cases, dutch auctions tend to quickly find buyers long before prices hit the `MIN_PRICE` levels. Also, since the GDA bonding curve is only meant to be used for single-sided pools, there does not appear to be an immediate risk of pools trading large volumes at extremely low prices.
However, not having a reserve price could mean market-making for some pools can happen at extremely low prices in perpetuity.

**Recommended Mitigation:**
As with an exponential bonding curve, we recommend introducing minimum price validation in `GDACurve::getBuyInfo` and `GDACurve::getSellInfo` when the spot price is updated.

**Sudoswap:**
Fixed in [commit c4dc61](https://github.com/sudoswap/lssvm2/commit/c4dc6159b8e3a3252f82ef4afea1f62417994425).

**Cyfrin:**
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Sudoswap |
| Report Date | N/A |
| Finders | Hans, Alex Roan, 0kage, Giovanni Di Siena |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-01-Sudoswap.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


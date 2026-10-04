---
# Core Classification
protocol: Securitize Public Stock Ramp
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64609
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
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
finders_count: 4
finders:
  - 0ximmeas
  - Stalin
  - Dacian
  - Jorge
---

## Vulnerability Title

Incorrect rounding direction in `SecuritizeAmmNavProvider::executeBuyBase` when scaling down `execPrice`

### Overview

See description below for full details.

### Original Finding Content

**Description:** In `SecuritizeAmmNavProvider::executeBuyBase`, the execution price is scaled down from WAD precision (18 decimals) to the asset's native decimal precision using integer division. The current implementation uses floor division, which systematically rounds DOWN the execution price:

```solidity
 uint256 scaleDown = 10 ** (18 - d);

 execPrice = rawExecPriceWad / scaleDown;
```

When users buy base assets, rounding the price DOWN means they pay less than the true calculated price. For example, with a 6-decimal token where `scaleDown` = 10^12:
* True price: $100.0000007 → `rawExecPriceWad` = 100,000,000,700,000,000,000
* Rounded price: $100.000000 → `execPrice` = 100,000,000
* Loss: $0.0000007 per share (always favors the buyer)

This issue is especially significant in `CLOSED_MARKET ` mode where AMM-based curve pricing is applied. In `CLOSED_MARKET`, the execution price calculation involves:

```solidity
function _pricingFromCurveBuy(
        uint256 amountInQuote,
        uint256 curvePriceWad,
        uint256 anchorPriceWad
    ) internal view returns (uint256 baseOut, uint256 execPriceWad) {
        require(anchorPriceWad > 0, "anchor=0");
        require(priceScaleFactor > 0, "scaleFactor = 0");

        uint256 r0Wad = (quoteBaseline * WAD) / baseBaseline;
        uint256 mWad = (curvePriceWad * WAD) / r0Wad;

        uint256 baseExecPriceWad = (anchorPriceWad * mWad) / WAD;

        // Smooth towards anchor:
        // execPriceWad = anchor + (baseExec - anchor) / scaleFactor
        if (baseExecPriceWad >= anchorPriceWad) {
            uint256 diff = baseExecPriceWad - anchorPriceWad;
            execPriceWad = anchorPriceWad + (diff / priceScaleFactor);
        } else {
            uint256 diff = anchorPriceWad - baseExecPriceWad;
            execPriceWad = anchorPriceWad - (diff / priceScaleFactor);
        }

        baseOut = (amountInQuote * WAD) / execPriceWad;
    }
```

These operations produce prices with deep fractional precision that almost never align with the `scaleDown` boundaries. This means every `CLOSED_MARKET` trade experiences truncation loss, unlike `OPEN_MARKET` mode where prices are set directly to clean anchor values.

**Impact:** On buy operations the protocol systematically loses a fractional amount on every trade. While the per-trade loss is small (typically sub-cent), it accumulates over time and volume.

**Recommended Mitigation:** Round up the final `execPrice` in `executeBuyBase`. Consider:
* using OZ [Math::mulDiv](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/math/Math.sol#L282) with explicit rounding for all multiplication followed by division
* documenting with comments why the rounding direction is logically correct at every place where rounding can occur

**Securitize:** Fixed in commit [0b268e8](https://bitbucket.org/securitize_dev/bc-nav-provider-sc/commits/0b268e8282cfcacf4cbcd32e4b908a87af04b0e8).

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Securitize Public Stock Ramp |
| Report Date | N/A |
| Finders | 0ximmeas, Stalin, Dacian, Jorge |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


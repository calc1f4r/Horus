---
# Core Classification
protocol: Elytra_2025-07-10
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63571
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Elytra-security-review_2025-07-10.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-18] Deficient validation in `updatePriceOracleForValidated`

### Overview

See description below for full details.

### Original Finding Content


_Resolved_

The goal of `updatePriceOracleForValidated` in `ElytraOracleV1` is to update the oracle for a supported asset, but, also perform validations checks for it, as we can see here :

```solidity
    /// @notice Updates the price oracle for an asset with validation
    /// @param asset Asset address
    /// @param priceOracle Oracle address
    function updatePriceOracleForValidated(
        address asset,
        address priceOracle
    )
        // ...
    {
        UtilLib.checkNonZeroAddress(priceOracle);

        // Sanity check that oracle has reasonable precision
        uint256 price = IPriceFetcher(priceOracle).getAssetPrice(asset);
        if (price > 1e19 || price < 1e17) {
            revert InvalidPriceOracle();
        }

        assetPriceOracle[asset] = priceOracle;
        emit AssetPriceOracleUpdate(asset, priceOracle);
    }
```

However, the checks are incorrect and deficient since hard-coded bounds (1e17–1e19) are used instead of the protocol’s configured `minPrice`/`maxPrice`, and it does not verify the oracle’s last update timestamp against `maxAssetPriceAge`. As a result, a malicious or stale price feed could be accepted, leading to mispriced deposits or withdrawals.

**Recommendations**

Consider validating against the contract’s `minPrice`/`maxPrice` parameters instead of fixed constants, and require that the fetched price’s age (via `getLastUpdateTime`) not exceed `maxAssetPriceAge` before accepting a new oracle address, since this is the goal of the `updatePriceOracleForValidated` function. 





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Elytra_2025-07-10 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Elytra-security-review_2025-07-10.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


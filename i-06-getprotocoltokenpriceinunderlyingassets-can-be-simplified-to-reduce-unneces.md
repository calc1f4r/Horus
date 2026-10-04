---
# Core Classification
protocol: BendDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49607
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-12-benddao-invitational
source_link: https://code4rena.com/reports/2024-12-benddao-invitational
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.60
financial_impact: low

# Scoring
quality_score: 3
rarity_score: 2

# Context Tags
tags:

protocol_categories:
  - lending

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[I-06] `getProtocolTokenPriceInUnderlyingAsset`’s can be simplified to reduce unnecessary computation

### Overview

See description below for full details.

### Original Finding Content


* src/yield/susds/YieldSavingsUSDS.sol
* Instances(1)

`getProtocolTokenPriceInUnderlyingAsset` uses market price to evaluate the price of sUSDS in USDS token. Since both sUSDS oracle price and USDS oracle price use the same chainlink price fee. The key link here for the sUSDS to USDS price conversion is based on `RATE_PROVIDER.chi()` which is essentially the sUSDS contract’s share to asset conversion.

This greatly increases the unnecessary complexity and introduces risks of stale chainlink oracles. It should be using sUSDS ‘s USDS -> sUSDS converion (convertToShare) method.

[YieldSavingsUSDS.sol# L147-L148](https://github.com/code-423n4/2024-12-benddao/blob/489f8dd0f8e86e5a7550cc6b81f9edfe79efbf4e/src/yield/susds/YieldSavingsUSDS.sol# L147-L148):
```

    function getProtocolTokenPriceInUnderlyingAsset() internal view virtual override returns (uint256) {
        IPriceOracleGetter priceOracle = IPriceOracleGetter(addressProvider.getPriceOracle());
|>      uint256 sUSDSPriceInBase = priceOracle.getAssetPrice(address(susds));
|>      uint256 usdsPriceInBase = priceOracle.getAssetPrice(address(underlyingAsset));
        return sUSDSPriceInBase.mulDiv(10 ** underlyingAsset.decimals(), usdsPriceInBase);
    }
```

### Recommendation

Change the implementation into `susds.converToAssets(1 ether)`.

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 3/5 |
| Rarity Score | 2/5 |
| Audit Firm | Code4rena |
| Protocol | BendDAO |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-12-benddao-invitational
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-12-benddao-invitational

### Keywords for Search

`vulnerability`


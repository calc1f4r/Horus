---
# Core Classification
protocol: Resolv_2024-12-09
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62190
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Resolv-security-review_2024-12-09.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 1.00
financial_impact: low

# Scoring
quality_score: 5
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

[L-03] Aave V3 price source can be inaccurate

### Overview

See description below for full details.

### Original Finding Content


_Resolved_


The `UsrRedemptionExtension` contract relies on Aave V3's oracle system to determine withdrawal token amounts during redemption. However, the implementation has potential price accuracy issues due to how it interacts with `Chainlink` oracles.

```solidity
    function redeem(
        uint256 _amount,
        address _receiver,
        address _withdrawalTokenAddress
    ) public whenNotPaused allowedWithdrawalToken(_withdrawalTokenAddress) onlyRole(SERVICE_ROLE) {
        ...
        IAaveOracle aavePriceOracle = IAaveOracle(ADDRESSES_PROVIDER.getPriceOracle());
        uint256 withdrawalTokenAmount = (_amount * aavePriceOracle.getAssetPrice(_withdrawalTokenAddress))
            / (aavePriceOracle.BASE_CURRENCY_UNIT() * 10 ** (USR_DECIMALS - withdrawalTokenDecimals));
        ...
    }
```

The issue is from two main problems in Aave V3's oracle implementation:

```solidity
  function getAssetPrice(address asset) public view override returns (uint256) {
    AggregatorInterface source = assetsSources[asset];

    if (asset == BASE_CURRENCY) {
      return BASE_CURRENCY_UNIT;
    } else if (address(source) == address(0)) {
      return _fallbackOracle.getAssetPrice(asset);
    } else {
      int256 price = source.latestAnswer(); // @audit call source.latestAnswer
      if (price > 0) {
        return uint256(price);
      } else {
        return _fallbackOracle.getAssetPrice(asset);
      }
    }
```

Let's inspect Aave V3's price source of USDT: `0xC26D4a1c46d884cfF6dE9800B6aE7A8Cf48B4Ff8`

- Unsafe price fetching: The Aave oracle uses `latestAnswer` instead of `latestRoundData` when querying Chainlink price feeds. No validation of price staleness is performed.
- Artificially capped prices may not reflect true market conditions

`PriceCapAdapterStable` contract:
```solidity
  function latestAnswer() external view override returns (int256) {
    int256 basePrice = ASSET_TO_USD_AGGREGATOR.latestAnswer(); // @audit call latestAnswer instead of latestRoundData
    int256 priceCap = _priceCap;

    if (basePrice > priceCap) { // @audit price is capped
      return priceCap;
    }

    return basePrice;
  }

```

As a result, users could receive incorrect amounts during token redemptions.

It's recommended to implement direct Chainlink oracle price fetching and validate price freshness.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 5/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Resolv_2024-12-09 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Resolv-security-review_2024-12-09.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`


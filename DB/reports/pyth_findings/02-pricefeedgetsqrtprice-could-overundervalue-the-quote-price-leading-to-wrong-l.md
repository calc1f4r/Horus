---
# Core Classification
protocol: Predy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34896
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-05-predy
source_link: https://code4rena.com/reports/2024-05-predy
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
  - dexes

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[02] `PriceFeed#getSqrtPrice()` could over/undervalue the quote price leading to wrong liquidation decisions

### Overview

See description below for full details.

### Original Finding Content


https://github.com/code-423n4/2024-05-predy/blob/a9246db5f874a91fb71c296aac6a66902289306a/src/PriceFeed.sol#L45-L58

```solidity
    function getSqrtPrice() external view returns (uint256 sqrtPrice) {
        (, int256 quoteAnswer,,,) = AggregatorV3Interface(_quotePriceFeed).latestRoundData();  //@audit
        IPyth.Price memory basePrice = IPyth(_pyth).getPriceNoOlderThan(_priceId, VALID_TIME_PERIOD);

        require(basePrice.expo == -8, "INVALID_EXP");

        require(quoteAnswer > 0 && basePrice.price > 0);

        uint256 price = uint256(int256(basePrice.price)) * Constants.Q96 / uint256(quoteAnswer);
        price = price * Constants.Q96 / _decimalsDiff;

        sqrtPrice = FixedPointMathLib.sqrt(price);
    }
```

This function returns the square root of the `baseToken` price quoted in `quoteToken`, and this data is queried when [checking if the vault is in danger](https://github.com/code-423n4/2024-05-predy/blob/a9246db5f874a91fb71c296aac6a66902289306a/src/libraries/logic/LiquidationLogic.sol#L129) in order to liquidate it, with needing a confirmation via `PositionCalculator.isLiquidatable()`.

The problem, however, is that Chainlink's `latestRoundData` is being queried, but no min/max checks are applied, leading to contracts working with flawed pricing.

> Keep in mind that the `PriceFeed#getSqrtPrice()` function is heavily used within the protocol in multiple core logics from getting the vault's TVL in the Liquidation logic to see if the vault is safe or not.

### Impact

If the prices ever go over the min/max boundary then protocol is going to ingest heavily inflated/deflated pricing data as the prices returned would be wrong.

Considering protocol plans to support a lot of tokens this would to be a problem as multiple tokens would have their source feed's aggregators with this min/max circuit breakers and as such it should be checked for an asset that has it, since this has quite a high impact with a low likelihood, but would be key to note that this has happened before with `LUNA`.

### Recommended Mitigation Steps

Consider attaching the min/max checkers for aggregators that have it and then route the pricing logic to a fallback oracle in the case where the returned prices are at these boundaries.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Predy |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-05-predy
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-05-predy

### Keywords for Search

`vulnerability`


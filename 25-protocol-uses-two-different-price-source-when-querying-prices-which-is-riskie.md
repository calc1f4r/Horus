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
solodit_id: 34919
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

[25] Protocol uses two different price source when querying prices which is riskier than using one sure source or having the second confirmed source as a fallback

### Overview

See description below for full details.

### Original Finding Content


[`PriceFeed#getSqrtPrice()`](https://github.com/code-423n4/2024-05-predy/blob/a9246db5f874a91fb71c296aac6a66902289306a/src/PriceFeed.sol#L45-L58)

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

This function returns the square root of the `baseToken` price quoted in `quoteToken`, and this data is queried when [checking if the vault is in danger](https://github.com/code-423n4/2024-05-predy/blob/a9246db5f874a91fb71c296aac6a66902289306a/src/libraries/logic/LiquidationLogic.sol#L129) in order to liquidate it, with needing a confirmation via `PositionCalculator.isLiquidatable()`. The problem is that the current logic is unsafe, considering a failure from one of the supported oracle sources, causes the whole attempt to revert.

Understandably, one can assume protocol is implementing two sources to ensure an attacker manipulating one source would not easily manipulate the other, but this leaves the execution vulnerable to the bug case where if one of the sources fail, the whole attempt fails.

### Impact

Protocol seems to wrongly integrate multiple oracles, cause currently if one of the oracles bubble up an error the whole attempt at pricing the tokens fail, whereas generally adopted logic would be to query one source and if it fails, query the other, which ensures the failure would occur 50% less than what's been implemented now.

### Recommended Mitigation Steps

Consider correctly integrating multiple oracles attempt to query both prices from one source, if it fails then query the other source for both prices, or leave this implementation but have it in a try/catch and if any attempt fails, then query another source.

***



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


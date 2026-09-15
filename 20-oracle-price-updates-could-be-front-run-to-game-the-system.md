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
solodit_id: 34914
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

[20] Oracle price updates could be front run to game the system

### Overview

See description below for full details.

### Original Finding Content


https://github.com/code-423n4/2024-05-predy/blob/a9246db5f874a91fb71c296aac6a66902289306a/src/PriceFeed.sol#L44-L58

```solidity
    function getSqrtPrice() external view returns (uint256 sqrtPrice) {
        (, int256 quoteAnswer,,,) = AggregatorV3Interface(_quotePriceFeed).latestRoundData();

        IPyth.Price memory basePrice = IPyth(_pyth).getPriceNoOlderThan(_priceId, VALID_TIME_PERIOD);

        require(basePrice.expo == -8, "INVALID_EXP");

        require(quoteAnswer > 0 && basePrice.price > 0);

        uint256 price = uint256(int256(basePrice.price)) * Constants.Q96 / uint256(quoteAnswer);
        price = price * Constants.Q96 / _decimalsDiff;

        sqrtPrice = FixedPointMathLib.sqrt(price);
    }
```

This function returns the square root of the `baseToken` price quoted in `quoteToken`, and this price data ends up being used in core areas accross protocol. The issue explained in this report is the fact that the price used is gotten from Chainlink; however, there are no protections on popular bug cases like an attacker frontrunning the price update from Chainlink to gain the most from the system. More on how this bug can be of an affect to the protocol can be seen from:

- Past finding: https://github.com/code-423n4/2024-04-dyad-findings/issues/1205
- A blog on how this works [here](https://medium.com/cyfrin/chainlink-oracle-defi-attacks-93b6cb6541bf#f123).

### Impact

Seems to be QA at most, considering deployment is being done on optimistic L2s.

### Recommended Mitigation Steps

Consider applying fees to logics that directly use the price returned from here. This way, we can always ensure minimal arbitrage is done away with since the profits might be engulfed by the fees.



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


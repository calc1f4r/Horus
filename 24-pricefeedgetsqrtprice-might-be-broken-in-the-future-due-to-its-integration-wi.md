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
solodit_id: 34918
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

[24] `PriceFeed#getSqrtPrice()` might be broken in the future due to it's integration with Pyth's `expo` value

### Overview

See description below for full details.

### Original Finding Content


https://github.com/code-423n4/2024-05-predy/blob/a9246db5f874a91fb71c296aac6a66902289306a/src/PriceFeed.sol#L45-L58

```solidity
    function getSqrtPrice() external view returns (uint256 sqrtPrice) {
        (, int256 quoteAnswer,,,) = AggregatorV3Interface(_quotePriceFeed).latestRoundData();
    //@audit
        IPyth.Price memory basePrice = IPyth(_pyth).getPriceNoOlderThan(_priceId, VALID_TIME_PERIOD);

        require(basePrice.expo == -8, "INVALID_EXP");

        require(quoteAnswer > 0 && basePrice.price > 0);

        uint256 price = uint256(int256(basePrice.price)) * Constants.Q96 / uint256(quoteAnswer);
        price = price * Constants.Q96 / _decimalsDiff;

        sqrtPrice = FixedPointMathLib.sqrt(price);
    }
```

This function returns the square root of the `baseToken` price quoted in `quoteToken`, and this data is queried when [checking if the vault is in danger](https://github.com/code-423n4/2024-05-predy/blob/a9246db5f874a91fb71c296aac6a66902289306a/src/libraries/logic/LiquidationLogic.sol#L129) in order to liquidate it, with needing a confirmation via `PositionCalculator.isLiquidatable()`. Extensively, it also is used for all other pricing logics; now it includes an expo, check with has the value of the expo be `== - 8`.

However, going to the implementation of Pyth natively, i.e., the Pyth Client, we can see that the actual exp value can indeed be negative and positive:

- [add_price.rs#L44](https://github.com/pyth-network/pyth-client/blob/main/program/rust/src/processor/add_price.rs#L44): When you add a price, it checks the exponent.
    - [utils.rs#L101-L106](https://github.com/pyth-network/pyth-client/blob/main/program/rust/src/utils.rs#L101-L106): It can be between `+-MAX_NUM_DECIMALS`.
    - [c_oracle_header.rs#L14](https://github.com/pyth-network/pyth-client/blob/main/program/rust/src/c_oracle_header.rs#L14): The `MAX_NUM_DECIMALS` has a value of 12, so theoretically, it can be `+-12`.

Furthermore, based on a Spearbit discussion with the Pyth team on a previous audit, _(see 5.2.2 from [this report](https://github.com/euler-xyz/euler-price-oracle/blob/c4074ab7a7aa0c6ffbc555391d9f0bfe1ee5fd6f/audits/Euler_Price_Oracle_Spearbit_Report_DRAFT.pdf))_ the Pyth team have confirmed that currently they have set [the `expo` must be `-ve` check in the SDK](https://github.com/pyth-network/pyth-crosschain/blob/a888ba318c0325c29070eaf5afcc3a4d443b058c/target_chains/ethereum/sdk/solidity/PythUtils.sol#L18) to facilitate the discussions, but they do not exclude the fact that this value can be positive in the future.

### Impact

QA, considering this affects future code; however, this means that valid prices would not be ingested.

### Recommendation

Consider supporting positive `8` exp value also for a more generalized integration of the PythOracle.



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


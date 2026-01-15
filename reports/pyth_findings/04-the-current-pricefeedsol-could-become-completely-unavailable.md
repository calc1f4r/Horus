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
solodit_id: 34898
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

[04] The current `pricefeed.sol` could become completely unavailable

### Overview

See description below for full details.

### Original Finding Content


https://github.com/code-423n4/2024-05-predy/blob/a9246db5f874a91fb71c296aac6a66902289306a/src/PriceFeed.sol#L28-L33

```solidity

contract PriceFeed {
    address private immutable _quotePriceFeed;
    address private immutable _pyth;
    uint256 private immutable _decimalsDiff;
    bytes32 private immutable _priceId;
```

https://github.com/code-423n4/2024-05-predy/blob/a9246db5f874a91fb71c296aac6a66902289306a/src/PriceFeed.sol#L45-L58

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

We can see that this is how the pricing logic works and this is used throughout the pricing logic present in the codebase for core functionalities like liquidating, etc.

The problem here, however, is that the `feedIds` are hardcoded and have been made immutable, but this is a wrong concept considering the underlying feed address could be changed later on for whatever reasons for example by Chainlink, which would then make this function always revert `     (, int256 quoteAnswer,,,) = AggregatorV3Interface(_quotePriceFeed).latestRoundData();` since the feed would be considered non-existing. The protocol also understands how this bug logic is problematic which is why in the `AddPairLogic` there is a logic to update feeds [here](https://github.com/code-423n4/2024-05-predy/blob/a9246db5f874a91fb71c296aac6a66902289306a/src/libraries/logic/AddPairLogic.sol#L112-L117).

```solidity
    function updatePriceOracle(DataType.PairStatus storage _pairStatus, address _priceOracle) external {
        _pairStatus.priceFeed = _priceOracle;

        emit PriceOracleUpdated(_pairStatus.id, _priceOracle);
    }
```

However, since this functionality is absent in `Pricefeed.sol` this means that when an oracle goes down, completely all logics routing through the pricefeed's `getSqrtPrice()` would be permanently DOS'd.

### Impact

Borderline medium/low
Impact here is very high considering even liquidations of vaults in danger now would be impossible. However, considering the likelihood of this is very minimal, I assume it to be a low severity.

### Recommended Mitigation Steps

Consider integrating a similar functionality of updating the feeds as is present in the `AddPairLogic`.



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


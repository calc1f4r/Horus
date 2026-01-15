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
solodit_id: 36883
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-07-benddao
source_link: https://code4rena.com/reports/2024-07-benddao
github_link: https://github.com/code-423n4/2024-07-benddao-findings/issues/59

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
  - lending

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - bin2chen
  - Ch\_301
  - oakcobalt
  - SpicyMeatball
---

## Vulnerability Title

[M-01] PriceOracle has invalid checks on price staleness

### Overview


This bug report discusses an issue with the `PriceOracle::getAssetPriceFromChainlink` function. There are two checks in the function that are not valid. The first check, `updatedAt != 0`, should be used to check if the price is within an acceptable time limit, but it is not being used for this purpose. The second check, `answeredInRound >= roundId`, is deprecated and should not be used. The report recommends using asset-specific heartbeat and checking against `block.timestamp - updatedAt` instead. The bug is classified as an Oracle bug and has been acknowledged by the BendDAO team. The severity level has been suggested to be adjusted to informative.

### Original Finding Content


There are two checks on price staleness in `PriceOracle::getAssetPriceFromChainlink`, but both checks are invalid.

1. `updatedAt != 0` - In chainlink aggregator, the price is updated at a set heartbeat and a threshold of deviation. `updatedAt` should be used to check if the answer is within the heartbeat or acceptable time limits. See [doc](https://docs.chain.link/data-feeds#check-the-timestamp-of-the-latest-answer).

2. `answeredInRound >= roundId` - `answeredInRound` is deprecated and shouldn't be used. See [doc](https://docs.chain.link/data-feeds/api-reference#getrounddata).

```solidity
//src/PriceOracle.sol
  /// @notice Query the price of asset from chainlink oracle
  function getAssetPriceFromChainlink(address asset) public view returns (uint256) {
    AggregatorV2V3Interface sourceAgg = assetChainlinkAggregators[asset];
    require(address(sourceAgg) != address(0), Errors.ASSET_AGGREGATOR_NOT_EXIST);

    (uint80 roundId, int256 answer, , uint256 updatedAt, uint80 answeredInRound) = sourceAgg.latestRoundData();
    require(answer > 0, Errors.ASSET_PRICE_IS_ZERO);
|>  require(updatedAt != 0, Errors.ORACLE_PRICE_IS_STALE);
|>  require(answeredInRound >= roundId, Errors.ORACLE_PRICE_IS_STALE);

    return uint256(answer);
  }
```

https://github.com/code-423n4/2024-07-benddao/blob/117ef61967d4b318fc65170061c9577e674fffa1/src/PriceOracle.sol#L124-L125

### Recommended Mitigation Steps

Consider using asset-specific heartbeat (e.g., ETH/USD has 1 hour heartbeat) and check against (`block.timestamp - updatedAt`).

### Assessed type

Oracle

**[thorseldon (BendDAO) acknowledged and commented](https://github.com/code-423n4/2024-07-benddao-findings/issues/59#issuecomment-2297902023):**
 > Checking the stale interval or grace period of oracle price, it's maybe better do this as suggested, but it's hard to set or predict the appropriate interval time.
> 
> We suggest adjust the severity level to informative.

**[0xTheC0der (judge) commented](https://github.com/code-423n4/2024-07-benddao-findings/issues/59#issuecomment-2298639222):**
> Historically, findings like this which can have a price impact were awarded with Medium severity on C4.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | BendDAO |
| Report Date | N/A |
| Finders | bin2chen, Ch\_301, oakcobalt, SpicyMeatball |

### Source Links

- **Source**: https://code4rena.com/reports/2024-07-benddao
- **GitHub**: https://github.com/code-423n4/2024-07-benddao-findings/issues/59
- **Contest**: https://code4rena.com/reports/2024-07-benddao

### Keywords for Search

`vulnerability`


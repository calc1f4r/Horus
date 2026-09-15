---
# Core Classification
protocol: Foundry DeFi Stablecoin CodeHawks Audit Contest
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34429
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cljx3b9390009liqwuedkn0m0
source_link: none
github_link: https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin

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

# Audit Details
report_date: unknown
finders_count: 28
finders:
  - iurii2002
  - 0xPublicGoods
  - dacian
  - 0xRizwan
  - 0xSmartContract
---

## Vulnerability Title

Lack of fallbacks for price feed oracle

### Overview


The DSC protocol has a vulnerability where it does not have backup plans in case the price feed oracle fails. This could lead to the protocol not being able to function properly and potentially becoming insolvent. The issue is that if Chainlink's aggregators fail to update the price data, the protocol will not be able to operate and transactions will be reverted. To fix this, the protocol should implement fallback solutions, such as using other oracle providers or on-chain Uniswap's TWAP, to ensure the protocol can continue to function even if Chainlink's aggregators fail.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/blob/d1c5501aa79320ca0aeaa73f47f0dbc88c7b77e2/src/libraries/OracleLib.sol#L26-L27">https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/blob/d1c5501aa79320ca0aeaa73f47f0dbc88c7b77e2/src/libraries/OracleLib.sol#L26-L27</a>

<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/blob/d1c5501aa79320ca0aeaa73f47f0dbc88c7b77e2/src/libraries/OracleLib.sol#L30">https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/blob/d1c5501aa79320ca0aeaa73f47f0dbc88c7b77e2/src/libraries/OracleLib.sol#L30</a>


## Summary

The DSC protocol does not implement fallback solutions for price feed oracle. In case Chainlink's aggregators fail to update price data, the protocol will refuse to liquidate users' positions, leading to the protocol's disruption.

## Vulnerability Details

The DSC protocol utilizes the `staleCheckLatestRoundData()` for querying price data of collateral tokens through [Chainlink's price feed aggregators](https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/blob/d1c5501aa79320ca0aeaa73f47f0dbc88c7b77e2/src/libraries/OracleLib.sol#L26-L27). Nonetheless, if Chainlink's aggregators fail to update the price data, the DSC protocol will not be able to operate. In other words, [the function will revert transactions since the received price data become stale](https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/blob/d1c5501aa79320ca0aeaa73f47f0dbc88c7b77e2/src/libraries/OracleLib.sol#L30).

```solidity
    function staleCheckLatestRoundData(AggregatorV3Interface priceFeed)
        public
        view
        returns (uint80, int256, uint256, uint256, uint80)
    {
@>      (uint80 roundId, int256 answer, uint256 startedAt, uint256 updatedAt, uint80 answeredInRound) =
@>          priceFeed.latestRoundData();

        uint256 secondsSince = block.timestamp - updatedAt;
@>      if (secondsSince > TIMEOUT) revert OracleLib__StalePrice();

        return (roundId, answer, startedAt, updatedAt, answeredInRound);
    }
```

- `Chainlink's price feed aggregator`: https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/blob/d1c5501aa79320ca0aeaa73f47f0dbc88c7b77e2/src/libraries/OracleLib.sol#L26-L27

- `TX will be reverted if the received price is stale`: https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/blob/d1c5501aa79320ca0aeaa73f47f0dbc88c7b77e2/src/libraries/OracleLib.sol#L30

## Impact

Without fallback solutions, the DSC protocol will be unable to operate if Chainlink's aggregators fail to update price data. 

Consider the scenario that Chainlink's aggregators fail to update price data and collateral tokens' prices dramatically go down, the DSC protocol will refuse to liquidate users' positions. Consequently, the protocol will become insolvent eventually, leading to the protocol's disruption.

## Tools Used

Manual Review

## Recommendations

I recommend implementing fallback solutions, such as using other off-chain oracle providers and/or on-chain Uniswap's TWAP, for feeding price data in case Chainlink's aggregators fail.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Foundry DeFi Stablecoin CodeHawks Audit Contest |
| Report Date | N/A |
| Finders | iurii2002, 0xPublicGoods, dacian, 0xRizwan, 0xSmartContract, t0x1c, sashiketh, Polaristow, serialcoder, 0x0115, Bauer, pacelli, crippie, nicobevi, kutu, JohnLaw, Flint14si2o, alexzoid, Bauchibred, 97Sabit, P12473, AlexCzm, BenRai |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin
- **Contest**: https://codehawks.cyfrin.io/c/cljx3b9390009liqwuedkn0m0

### Keywords for Search

`vulnerability`


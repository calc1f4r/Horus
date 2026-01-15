---
# Core Classification
protocol: Beanstalk: The Finale
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36226
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clw9e11e4001gdv0iigjylx5n
source_link: none
github_link: https://github.com/Cyfrin/2024-05-beanstalk-the-finale

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
  - yield
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - T1MOH
---

## Vulnerability Title

LibUsdOracle inverses Chainlink TWAP price which results in incorrect price

### Overview

See description below for full details.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2024-05-beanstalk-the-finale/blob/main/protocol/contracts/libraries/Oracle/LibChainlinkOracle.sol#L96">https://github.com/Cyfrin/2024-05-beanstalk-the-finale/blob/main/protocol/contracts/libraries/Oracle/LibChainlinkOracle.sol#L96</a>

<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2024-05-beanstalk-the-finale/blob/main/protocol/contracts/libraries/Oracle/LibUsdOracle.sol#L49-L65">https://github.com/Cyfrin/2024-05-beanstalk-the-finale/blob/main/protocol/contracts/libraries/Oracle/LibUsdOracle.sol#L49-L65</a>


## Summary
Here is good article on why arithmetic mean TWAP cannot be inversed to get price of second asset:
https://blog.yacademy.dev/2024-05-24-are-inverse-TWAP-prices-inaccurate/

In short inverse of average price is not equal to average of inverse prices. The more volatile the price over the observed period, the greater the distortion will be.
That's why Uniswap V2 stores 2 prices: token0 and token1 to calculate each TWAP. But that's true only for arithmetic mean, in Uni V3 geometric mean is used, and this price can be inversed.


## Vulnerability Details
LibUsdOracle.sol returns price USD / Token by inversing price fetched from ordinary oracle:
```solidity
    function getUsdPrice(address token, uint256 lookback) internal view returns (uint256) {
        if (token == C.WETH) {
            uint256 ethUsdPrice = LibEthUsdOracle.getEthUsdPrice(lookback);
            if (ethUsdPrice == 0) return 0;
@>          return uint256(1e24).div(ethUsdPrice);
        }
        if (token == C.WSTETH) {
            uint256 wstethUsdPrice = LibWstethUsdOracle.getWstethUsdPrice(lookback);
            if (wstethUsdPrice == 0) return 0;
@>          return uint256(1e24).div(wstethUsdPrice);
        }

        // 1e18 * 1e6 = 1e24.
        uint256 tokenPrice = getTokenPriceFromExternal(token, lookback);
        if (tokenPrice == 0) return 0;
@>      return uint256(1e24).div(tokenPrice);
    }
```

One of oracle sources is Chainlink TWAP like in `LibEthUsdOracle.getEthUsdPrice()`:
```solidity
    function getEthUsdPrice(uint256 lookback) internal view returns (uint256) {
        return
            lookback > 0
                ? LibChainlinkOracle.getTwap(
                    C.ETH_USD_CHAINLINK_PRICE_AGGREGATOR,
                    LibChainlinkOracle.FOUR_HOUR_TIMEOUT,
                    lookback
                )
                : LibChainlinkOracle.getPrice(
                    C.ETH_USD_CHAINLINK_PRICE_AGGREGATOR,
                    LibChainlinkOracle.FOUR_HOUR_TIMEOUT
                );
    }
```

And finally let's see that Chainlink TWAP calculates arithmetic mean TWAP:
```solidity
    function getTwap(
        address priceAggregatorAddress,
        uint256 maxTimeout,
        uint256 lookback
    ) internal view returns (uint256 price) {
        ...

        // Secondly, try to get latest price data:
        try priceAggregator.latestRoundData() returns (
            uint80 roundId,
            int256 answer,
            uint256 /* startedAt */,
            uint256 timestamp,
            uint80 /* answeredInRound */
        ) {
            ...
                while (timestamp > t.endTimestamp) {
@>                  t.cumulativePrice = t.cumulativePrice.add(
                        uint256(answer).mul(t.lastTimestamp.sub(timestamp))
                    );
                    roundId -= 1;
                    t.lastTimestamp = timestamp;
                    (answer, timestamp) = getRoundData(priceAggregator, roundId);
                    if (
                        checkForInvalidTimestampOrAnswer(
                            timestamp,
                            answer,
                            t.lastTimestamp,
                            maxTimeout
                        )
                    ) {
                        return 0;
                    }
                }
@>              t.cumulativePrice = t.cumulativePrice.add(
                    uint256(answer).mul(t.lastTimestamp.sub(t.endTimestamp))
                );
                return t.cumulativePrice.mul(PRECISION).div(10 ** decimals).div(lookback);
            }
        } catch {
        ...
    }
```

## Impact
LibUsdOracle.sol returns incorrect price if underlying oracle is Chainlink TWAP.

## Tools Used
Manual Review

## Recommendations
Do not inverse Chainlink TWAP price, instead calculate TWAP from inversed prices. However it requires refactor of oracle libraries.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Beanstalk: The Finale |
| Report Date | N/A |
| Finders | T1MOH |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-05-beanstalk-the-finale
- **Contest**: https://codehawks.cyfrin.io/c/clw9e11e4001gdv0iigjylx5n

### Keywords for Search

`vulnerability`


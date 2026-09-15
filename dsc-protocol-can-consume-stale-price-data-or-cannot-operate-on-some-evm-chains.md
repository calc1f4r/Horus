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
solodit_id: 34424
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
finders_count: 37
finders:
  - Y403L
  - ni8mare
  - chainNue
  - dacian
  - 0xAxe
---

## Vulnerability Title

DSC protocol can consume stale price data or cannot operate on some EVM chains

### Overview


This bug report discusses an issue with the DSC protocol where it can consume outdated price data or not work properly on certain EVM chains. The problem is caused by the protocol's stale period being set to 3 hours, which is too long for some chains and too short for others. This can lead to incorrect prices being reported and causing the protocol's functions to work incorrectly, potentially disrupting the protocol's operations. The report recommends using a mapping data type and adding a setter function to update the stale period for each collateral token to prevent this issue. 

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/blob/d1c5501aa79320ca0aeaa73f47f0dbc88c7b77e2/src/libraries/OracleLib.sol#L19">https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/blob/d1c5501aa79320ca0aeaa73f47f0dbc88c7b77e2/src/libraries/OracleLib.sol#L19</a>

<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/blob/d1c5501aa79320ca0aeaa73f47f0dbc88c7b77e2/src/libraries/OracleLib.sol#L30">https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/blob/d1c5501aa79320ca0aeaa73f47f0dbc88c7b77e2/src/libraries/OracleLib.sol#L30</a>


## Summary

The stale period (3 hours) is too large for Ethereum, Polygon, BNB, and Optimism chains, leading to consuming stale price data. On the other hand, that period is too small for Arbitrum and Avalanche chains, rendering the DSC protocol unable to operate.

## Vulnerability Details

In the `OracleLib` library, the [`TIMEOUT` constant is set to *3 hours*](https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/blob/d1c5501aa79320ca0aeaa73f47f0dbc88c7b77e2/src/libraries/OracleLib.sol#L19). In other words, the `staleCheckLatestRoundData()` would consider the price data fed by Chainlink's price feed aggregators to be stale only after the last update time has elapsed *3 hours*.

Since the DSC protocol supports every EVM chain (confirmed by the client), let's consider the `ETH / USD oracles` on different chains.
- On Ethereum, the oracle will update the price data [every ~1 hour](https://data.chain.link/ethereum/mainnet/crypto-usd/eth-usd).
- On Polygon, the oracle will update the price data [every ~25 seconds](https://data.chain.link/polygon/mainnet/crypto-usd/eth-usd).
- On BNB (BSC), the oracle will update the price data [every ~60 seconds](https://data.chain.link/bsc/mainnet/crypto-usd/eth-usd).
- On Optimism, the oracle will update the price data [every ~20 minutes](https://data.chain.link/optimism/mainnet/crypto-usd/eth-usd).
- On Arbitrum, the oracle will update the price data [every ~24 hours](https://data.chain.link/arbitrum/mainnet/crypto-usd/eth-usd).
- On Avalanche, the oracle will update the price data [every ~24 hours](https://data.chain.link/avalanche/mainnet/crypto-usd/eth-usd).

On some chains such as Ethereum, Polygon, BNB, and Optimism, *3 hours* can be considered too large for the stale period, causing the `staleCheckLatestRoundData()` to return stale price data.

Whereas, on some chains, such as Arbitrum and Avalanche, *3 hours* is too small. Specifically, if the DSC protocol is deployed to Arbitrum or Avalanche, the protocol will be unable to operate because the ["`if (secondsSince > TIMEOUT)`" condition will be met](https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/blob/d1c5501aa79320ca0aeaa73f47f0dbc88c7b77e2/src/libraries/OracleLib.sol#L30), causing a transaction to be reverted in the `staleCheckLatestRoundData()`.

```solidity
    // ...SNIPPED...
	
@>  uint256 private constant TIMEOUT = 3 hours; // 3 * 60 * 60 = 10800 seconds

    function staleCheckLatestRoundData(AggregatorV3Interface priceFeed)
        public
        view
        returns (uint80, int256, uint256, uint256, uint80)
    {
        (uint80 roundId, int256 answer, uint256 startedAt, uint256 updatedAt, uint80 answeredInRound) =
            priceFeed.latestRoundData();

        uint256 secondsSince = block.timestamp - updatedAt;
@>      if (secondsSince > TIMEOUT) revert OracleLib__StalePrice();

        return (roundId, answer, startedAt, updatedAt, answeredInRound);
    }
```

- `TIMEOUT definition`: https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/blob/d1c5501aa79320ca0aeaa73f47f0dbc88c7b77e2/src/libraries/OracleLib.sol#L19

- `Use of TIMEOUT`: https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/blob/d1c5501aa79320ca0aeaa73f47f0dbc88c7b77e2/src/libraries/OracleLib.sol#L30

## Impact

Setting the stale period (`TIMEOUT` constant) too large could lead to incorrect reporting of prices of collateral tokens. The incorrect prices can cause the DSC protocol's functions (e.g., `mintDsc()`, `burnDsc()`, `redeemCollateral()`, and `liquidate()`) to operate incorrectly, affecting the protocol's disruption.

On the other hand, setting the stale period too small could render the DSC protocol unable to operate.

## Tools Used

Manual Review

## Recommendations

Even on the same chain, different collateral tokens can have different heartbeats (the period to update the price data on chain). For instance, the heartbeat for the [DAI / USD oracle on Ethereum](https://data.chain.link/ethereum/mainnet/stablecoins/dai-usd) is *~1 hour*, whereas the heartbeat for the [USDT / USD oracle on the same chain](https://data.chain.link/ethereum/mainnet/stablecoins/usdt-usd) is *~24 hours*.

Thus, I recommend using the `mapping` data type to record the `TIMEOUT` parameter of each collateral token and setting each token's `TIMEOUT` with an appropriate stale period.

Furthermore, I also recommend adding a *setter* function for updating the stale period of each specific collateral token.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Foundry DeFi Stablecoin CodeHawks Audit Contest |
| Report Date | N/A |
| Finders | Y403L, ni8mare, chainNue, dacian, 0xAxe, sobieski, t0x1c, alymurtazamemon, Breeje, iroh, Polaristow, serialcoder, golanger85, T1MOH, devival, aviggiano, ss3434, pina, pacelli, crippie, aak, kutu, Kresh, Bauchibred, n1punp, P12473, AcT3R, StErMi, darkart, rvierdiiev, BenRai, cRat1st0s, Shogoki |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin
- **Contest**: https://codehawks.cyfrin.io/c/cljx3b9390009liqwuedkn0m0

### Keywords for Search

`vulnerability`


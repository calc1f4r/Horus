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
solodit_id: 34425
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
finders_count: 91
finders:
  - Bugi
  - jprod15
  - ni8mare
  - Daniel526
  - nervouspika
---

## Vulnerability Title

Chainlink oracle will return the wrong price if the aggregator hits `minAnswer`

### Overview


The Chainlink oracle has a bug where it returns the wrong price if the aggregator hits a certain minimum price. This can happen if there is a sudden drop in the value of an asset. The bug is caused by a missing check in the code and can lead to incorrect prices being used for transactions. This has happened before on other platforms and can have a significant impact on users. The report recommends adding checks for minimum and maximum prices to prevent this issue from occurring.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/tree/main">https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/tree/main</a>


## Summary
Chainlink aggregators have a built-in circuit breaker if the price of an asset goes outside of a predetermined price band.

The result is that if an asset experiences a huge drop in value (i.e. LUNA crash) the price of the oracle will continue to return the `minPrice` instead of the actual price of the asset and vice versa.

## Vulnerability Details
The `staleCheckLatestRoundData` function in `OracleLib.sol` is only checking for the stale price. But no checks are done to handle that.

```solidity
 function staleCheckLatestRoundData(AggregatorV3Interface priceFeed)
        public
        view
        returns (uint80, int256, uint256, uint256, uint80)
    {
        (uint80 roundId, int256 answer, uint256 startedAt, uint256 updatedAt, uint80 answeredInRound) =
            priceFeed.latestRoundData();

        uint256 secondsSince = block.timestamp - updatedAt;
        if (secondsSince > TIMEOUT) revert OracleLib__StalePrice();

        return (roundId, answer, startedAt, updatedAt, answeredInRound);
    }
```
[[21](https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/blob/d1c5501aa79320ca0aeaa73f47f0dbc88c7b77e2/src/libraries/OracleLib.sol#L21C4-L33C6)]

There is no function for checking only this as well in the library.
The checks are not done in `DSCEngine.sol` file.
There are two instances of that:
```solidity
        (, int256 price,,,) = priceFeed.staleCheckLatestRoundData();
```
[[345](https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/blob/d1c5501aa79320ca0aeaa73f47f0dbc88c7b77e2/src/DSCEngine.sol#L345)]

```solidity
        (, int256 price,,,) = priceFeed.staleCheckLatestRoundData();
```
[[363](https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/blob/d1c5501aa79320ca0aeaa73f47f0dbc88c7b77e2/src/DSCEngine.sol#L363)]

## Impact
This would allow users to continue mintDsc, burnDsc etc. but at the wrong price. This is exactly what happened to Venus on BSC when LUNA crashed.

## Tools Used
chainlink docs, foundry test and previous audit reports

## Recommendations
Consider using the following checks: 
```solidity
(uint80, int256 answer, uint, uint, uint80) = oracle.latestRoundData();

// minPrice check
require(answer > minPrice, "Min price exceeded");
// maxPrice check
require(answer < maxPrice, "Max price exceeded");
```

Also some gas could be saved when used `revert` with custom `error` for doing the check.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Foundry DeFi Stablecoin CodeHawks Audit Contest |
| Report Date | N/A |
| Finders | Bugi, jprod15, ni8mare, Daniel526, nervouspika, Aamirusmani1552, dacian, klaus, 0xRizwan, 0xAxe, sm4rty, nmirchev8, 0xSmartContract, tsvetanovv, HChang26, t0x1c, Phantasmagoria, alymurtazamemon, vic43, 0xsandy, Deathstore, Tripathi, Bbash, Polaristow, Avci, Juntao, 0xhuy0512, ZanyBonzy, serialcoder, degensec, Dliteofficial, larsson, 0x0115, pks27, No12Samurai, 0x9527, T1MOH, devival, Matin, Vagner, Norah, 0xMosh, xfu, MaanVader, 0x4non, fouzantanveer, pina, cholakov, boredpukar, 0xtotem, crippie, Niki, smbv1923, chaos304, 0xdeth, 0x3b, blckhv, kutu, Flint14si2o, alexzoid, 33audits, said017, AcT3R, ABA, tsar, Dharma, gaslimit, 0xNiloy, rvierdiiev, ZedBlockchain, akhilmanga, jonatascm |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin
- **Contest**: https://codehawks.cyfrin.io/c/cljx3b9390009liqwuedkn0m0

### Keywords for Search

`vulnerability`

